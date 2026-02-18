"""Ethereum terminology: synonyms and dictionary for Meilisearch.

Provides bidirectional synonym mappings for Ethereum abbreviations and a
custom dictionary of compound terms that should be tokenized as single units.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request

__all__ = [
    "apply_terminology_settings",
    "expand_query",
    "get_ethereum_dictionary",
    "get_ethereum_synonyms",
]

# Timeout for HTTP requests to Meilisearch.
_TIMEOUT = 10

# Abbreviation-to-expansions mapping.  Each entry generates bidirectional
# synonym relationships: the key maps to all values, and each value maps
# back to the key.
_ABBREVIATIONS: dict[str, list[str]] = {
    # --- Serialization & cryptography ---
    "ssz": ["simple serialize", "simpleserialize"],
    "kzg": ["kate polynomial commitment", "kate-zaverucha-goldberg"],
    "rlp": ["recursive length prefix"],
    "mpt": ["merkle patricia trie"],
    "bls": ["boneh-lynn-shacham"],
    "snark": ["succinct non-interactive argument of knowledge"],
    "stark": ["scalable transparent argument of knowledge"],
    "vdf": ["verifiable delay function"],
    "verkle": ["vector commitment merkle tree", "verkle tree", "verkle trie"],
    # --- Data availability ---
    "das": ["data availability sampling"],
    "peerdas": ["peer data availability sampling"],
    "danksharding": ["data availability sharding"],
    # --- Consensus & finality ---
    "lmd-ghost": ["latest message driven ghost"],
    "ffg": ["friendly finality gadget", "casper ffg"],
    "gasper": ["ghost and casper combined consensus"],
    "ssf": ["single slot finality", "single-slot finality"],
    "randao": ["random number generation dao"],
    # --- Block production & MEV ---
    "pbs": ["proposer-builder separation", "proposer builder separation"],
    "epbs": ["enshrined proposer-builder separation"],
    "mev": ["maximal extractable value", "miner extractable value"],
    "pepc": ["protocol-enforced proposer commitments"],
    "aps": ["attester-proposer separation"],
    "focil": ["fork-choice enforced inclusion lists"],
    "il": ["inclusion list"],
    # --- Protocol layers & governance ---
    "evm": ["ethereum virtual machine"],
    "cl": ["consensus layer"],
    "el": ["execution layer"],
    "eip": ["ethereum improvement proposal"],
    "erc": ["ethereum request for comments"],
    "eof": ["evm object format"],
    "blob": ["binary large object"],
    # --- Staking & validators ---
    "dvt": ["distributed validator technology"],
    # --- Zero-knowledge ---
    "zkp": ["zero knowledge proof"],
    "zk-snark": ["zero knowledge succinct non-interactive argument of knowledge"],
    "zk-stark": ["zero knowledge scalable transparent argument of knowledge"],
    # --- DeFi / L2 ---
    "amm": ["automated market maker"],
    "lst": ["liquid staking token"],
}

# Compound terms that the Meilisearch tokenizer should treat as single tokens.
_DICTIONARY: list[str] = [
    # Sharding & data availability
    "proto-danksharding",
    "danksharding",
    "proto-dank-sharding",
    "data-availability-sampling",
    "peer-data-availability-sampling",
    # Consensus & finality
    "single-slot-finality",
    "lmd-ghost",
    "casper-ffg",
    # Block production & MEV
    "proposer-builder-separation",
    "enshrined-proposer-builder-separation",
    "mev-boost",
    "fork-choice-enforced-inclusion-lists",
    "inclusion-list",
    "attester-proposer-separation",
    "maximal-extractable-value",
    "protocol-enforced-proposer-commitments",
    # Trees & state
    "verkle-tree",
    "verkle-trie",
    "merkle-patricia-trie",
    "state-expiry",
    # Infrastructure
    "beacon-chain",
    "execution-layer",
    "consensus-layer",
    "account-abstraction",
    "distributed-validator-technology",
    "liquid-staking-token",
    # Zero-knowledge
    "zk-snark",
    "zk-stark",
    "zero-knowledge-proof",
    # Serialization
    "simple-serialize",
    "recursive-length-prefix",
    # Common EIP references
    "eip-4844",
    "eip-1559",
    "eip-4788",
    "eip-7594",
    "eip-4337",
    "eip-7702",
    "eip-7251",
    "eip-6110",
    "eip-7002",
]


def get_ethereum_synonyms() -> dict[str, list[str]]:
    """Return the Meilisearch synonyms mapping for Ethereum terminology.

    Every abbreviation entry is expanded into bidirectional relationships so
    that searching for either the abbreviation or any expansion finds all
    related documents.
    """
    synonyms: dict[str, list[str]] = {}
    for abbrev, expansions in _ABBREVIATIONS.items():
        # abbrev -> all expansions
        synonyms[abbrev] = list(expansions)
        # each expansion -> [abbrev] + other expansions
        for exp in expansions:
            others = [abbrev] + [e for e in expansions if e != exp]
            synonyms[exp] = others
    return synonyms


def get_ethereum_dictionary() -> list[str]:
    """Return custom dictionary entries for Meilisearch tokenizer."""
    return list(_DICTIONARY)


# ---------------------------------------------------------------------------
# Query expansion for semantic search
# ---------------------------------------------------------------------------

# Abbreviations that are safe to expand in queries.  Excludes short or
# ambiguous terms (cl, el, il, blob, eip, erc, evm) that are either too
# common in our corpus or could match non-Ethereum contexts.
_EXPANDABLE: frozenset[str] = frozenset({
    # Serialization & crypto
    "ssz", "kzg", "rlp", "mpt", "bls", "snark", "stark", "vdf", "verkle",
    # Data availability
    "das", "peerdas", "danksharding",
    # Consensus & finality
    "lmd-ghost", "ffg", "gasper", "ssf", "randao",
    # Block production & MEV
    "pbs", "epbs", "mev", "pepc", "aps", "focil",
    # Protocol
    "eof", "dvt",
    # Zero-knowledge
    "zkp", "zk-snark", "zk-stark",
    # DeFi
    "amm", "lst",
})

_TOKEN_RE = re.compile(r"[\w-]+")


def expand_query(query: str) -> str:
    """Expand Ethereum abbreviations in the query for better semantic search.

    Appends the primary expansion of recognized abbreviations so that the
    embedding model receives richer context.  Only expands terms in
    ``_EXPANDABLE`` to avoid noise from common/short abbreviations.

    Example::

        >>> expand_query("SSZ Merkleization")
        'SSZ Merkleization Simple Serialize'
    """
    tokens = {m.group().lower() for m in _TOKEN_RE.finditer(query)}
    expansions: list[str] = []
    for token in sorted(tokens):
        if token in _EXPANDABLE and token in _ABBREVIATIONS:
            expansions.append(_ABBREVIATIONS[token][0])
    if not expansions:
        return query
    return query + " " + " ".join(expansions)


def apply_terminology_settings(meili_url: str, admin_key: str, index_uid: str) -> None:
    """Apply synonyms and dictionary settings to the Meilisearch index.

    Raises ``urllib.error.HTTPError`` on API errors and ``urllib.error.URLError``
    if Meilisearch is unreachable.
    """
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if admin_key:
        headers["Authorization"] = f"Bearer {admin_key}"

    synonyms = get_ethereum_synonyms()
    _put_setting(meili_url, index_uid, "synonyms", synonyms, headers)

    dictionary = get_ethereum_dictionary()
    _put_setting(meili_url, index_uid, "dictionary", dictionary, headers)


def _put_setting(
    meili_url: str,
    index_uid: str,
    setting_name: str,
    payload: dict | list,
    headers: dict[str, str],
) -> None:
    """PUT a single index setting and wait for the task to complete."""
    url = f"{meili_url}/indexes/{index_uid}/settings/{setting_name}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
    resp = urllib.request.urlopen(req, timeout=_TIMEOUT)
    task_info = json.loads(resp.read())
    task_uid = task_info.get("taskUid")

    # Poll until the task finishes.
    if task_uid is not None:
        _wait_for_task(meili_url, headers, task_uid)


def _wait_for_task(
    meili_url: str, headers: dict[str, str], task_uid: int, *, max_polls: int = 120
) -> None:
    """Poll the task endpoint until it succeeds or fails."""
    url = f"{meili_url}/tasks/{task_uid}"
    for _ in range(max_polls):
        req = urllib.request.Request(url, headers=headers, method="GET")
        resp = urllib.request.urlopen(req, timeout=_TIMEOUT)
        info = json.loads(resp.read())
        status = info.get("status")
        if status == "succeeded":
            return
        if status == "failed":
            error = info.get("error", {})
            msg = error.get("message", "unknown error")
            raise RuntimeError(f"Meilisearch task {task_uid} failed: {msg}")
        time.sleep(1.0)
    raise TimeoutError(f"Meilisearch task {task_uid} did not complete in time")
