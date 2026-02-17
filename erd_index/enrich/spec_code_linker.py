"""Heuristic spec-to-code linker.

Finds links between EIP specifications and code nodes in the graph DB
using three heuristic strategies:

1. EIP reference in comments/docstrings (confidence 0.8)
2. Function name contains EIP number (confidence 0.9)
3. Test file for EIP (confidence 0.7)

All links use ``match_method='heuristic'``.
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
from typing import Any

from erd_index.enrich.eip_refs import extract_eip_refs

__all__ = ["find_spec_code_links"]

log = logging.getLogger(__name__)

# Matches EIP number embedded in a symbol name.
# Patterns: eipN, EIP_N, eipN_, _eipN, _eip_N, EIP-N (hyphens unlikely in
# symbol names but defensive).  Captures the number in group 1.
_SYMBOL_EIP_RE = re.compile(
    r"""
    (?:(?:^|(?<=_)|(?<=-)|(?<=[a-z])))  # start, after underscore/hyphen, or camelCase boundary
    [Ee][Ii][Pp]                        # case-insensitive "eip"
    [-_]?                               # optional separator
    (\d{1,6})                           # EIP number
    (?:$|(?=_)|(?=-)|(?=[A-Z])|(?=\b))  # end, before separator, or word boundary
    """,
    re.VERBOSE,
)

# Matches EIP number in a file path.
# Patterns: eip4844, eip_4844, eip-4844, EIP4844
_PATH_EIP_RE = re.compile(
    r"""
    [Ee][Ii][Pp]               # case-insensitive "eip"
    [-_]?                      # optional separator
    (\d{1,6})                  # EIP number
    """,
    re.VERBOSE,
)


def _get_indexed_eips(conn: sqlite3.Connection) -> set[int]:
    """Return the set of EIP numbers that have nodes in the graph."""
    rows = conn.execute(
        "SELECT DISTINCT eip FROM node WHERE eip IS NOT NULL"
    ).fetchall()
    return {row["eip"] for row in rows}


def _get_code_nodes(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return all code nodes from the graph."""
    rows = conn.execute(
        """SELECT node_id, node_type, repository, file_path, symbol_name,
                  symbol_kind, chunk_id
           FROM node
           WHERE node_type IN (
               'code_function', 'code_struct', 'code_enum',
               'code_trait', 'code_impl', 'code_class'
           )"""
    ).fetchall()
    return [dict(r) for r in rows]


def _get_code_node_text(conn: sqlite3.Connection, chunk_id: str) -> str | None:
    """Retrieve the text content for a code node.

    Code text is not stored in the graph DB node table, so we look up the
    node's chunk_id to read from the state/manifest.  However, the simplest
    approach is to look at node metadata or re-query.  Since we don't have a
    direct text column, we return None and callers fall back to other signals.

    For heuristic 1, we query the chunk_id against metadata_json if available,
    but the primary mechanism uses the node's own fields.
    """
    # We don't have chunk text stored in graph.db — return None.
    # Heuristic 1 is applied during graph building when text is available.
    return None


def _find_eip_node_id(conn: sqlite3.Connection, eip: int) -> str | None:
    """Find the primary EIP node_id for a given EIP number."""
    row = conn.execute(
        "SELECT node_id FROM node WHERE eip = ? AND node_type = 'eip' LIMIT 1",
        (eip,),
    ).fetchone()
    return row["node_id"] if row else None


def _heuristic_symbol_name(
    node: dict[str, Any],
    indexed_eips: set[int],
) -> list[dict[str, Any]]:
    """Heuristic 2: function/symbol name contains an EIP number.

    E.g. ``applyEIP1559``, ``eip4844_blob_gas_price``, ``process_blob_kzg_commitments``.
    Confidence: 0.9, relation: implements.
    """
    symbol = node.get("symbol_name")
    if not symbol:
        return []

    links: list[dict[str, Any]] = []
    seen: set[int] = set()

    for m in _SYMBOL_EIP_RE.finditer(symbol):
        eip_num = int(m.group(1))
        if eip_num > 0 and eip_num in indexed_eips and eip_num not in seen:
            seen.add(eip_num)
            links.append({
                "eip": eip_num,
                "code_node_id": node["node_id"],
                "relation": "implements",
                "match_method": "heuristic",
                "confidence": 0.9,
                "evidence_json": json.dumps({
                    "heuristic": "symbol_name",
                    "symbol": symbol,
                    "match": m.group(0),
                }),
            })

    return links


def _heuristic_file_path(
    node: dict[str, Any],
    indexed_eips: set[int],
) -> list[dict[str, Any]]:
    """Heuristic 3: test file for an EIP.

    If the file path contains ``eip`` + a number (e.g. ``test_eip4844.py``,
    ``eip1559_test.go``), link with relation ``tests``.
    Confidence: 0.7.
    """
    file_path = node.get("file_path")
    if not file_path:
        return []

    # Only apply to files that look like tests
    path_lower = file_path.lower()
    is_test_file = "test" in path_lower

    if not is_test_file:
        return []

    links: list[dict[str, Any]] = []
    seen: set[int] = set()

    for m in _PATH_EIP_RE.finditer(file_path):
        eip_num = int(m.group(1))
        if eip_num > 0 and eip_num in indexed_eips and eip_num not in seen:
            seen.add(eip_num)
            links.append({
                "eip": eip_num,
                "code_node_id": node["node_id"],
                "relation": "tests",
                "match_method": "heuristic",
                "confidence": 0.7,
                "evidence_json": json.dumps({
                    "heuristic": "test_file_path",
                    "file_path": file_path,
                    "match": m.group(0),
                }),
            })

    return links


def _heuristic_eip_ref_in_text(
    node: dict[str, Any],
    text: str,
    indexed_eips: set[int],
) -> list[dict[str, Any]]:
    """Heuristic 1: EIP reference in comments/docstrings.

    If a code chunk's text contains ``EIP-N`` or ``ERC-N``, link it to that EIP.
    If the symbol name also contains the EIP number, use ``implements`` (0.8);
    otherwise use ``references`` (0.8).
    """
    eip_refs = extract_eip_refs(text)
    if not eip_refs:
        return []

    symbol = node.get("symbol_name") or ""

    links: list[dict[str, Any]] = []
    for eip_num in eip_refs:
        if eip_num not in indexed_eips:
            continue

        # Check if symbol name also references this EIP
        symbol_has_eip = bool(_SYMBOL_EIP_RE.search(symbol)) and any(
            int(m.group(1)) == eip_num for m in _SYMBOL_EIP_RE.finditer(symbol)
        )

        relation = "implements" if symbol_has_eip else "references"

        links.append({
            "eip": eip_num,
            "code_node_id": node["node_id"],
            "relation": relation,
            "match_method": "heuristic",
            "confidence": 0.8,
            "evidence_json": json.dumps({
                "heuristic": "eip_ref_in_text",
                "eip_ref": f"EIP-{eip_num}",
                "relation": relation,
            }),
        })

    return links


def find_spec_code_links(
    conn: sqlite3.Connection,
) -> list[dict[str, Any]]:
    """Find spec-code links by querying code and EIP nodes from the graph.

    Applies three heuristics to discover links between EIP specifications
    and code nodes:

    1. EIP reference in comments/docstrings (confidence 0.8)
    2. Function name contains EIP number (confidence 0.9)
    3. Test file for EIP (confidence 0.7)

    Returns a list of link dicts ready for ``upsert_spec_code_link()``.
    """
    indexed_eips = _get_indexed_eips(conn)
    if not indexed_eips:
        log.info("No EIP nodes found in graph; skipping spec-code linking")
        return []

    code_nodes = _get_code_nodes(conn)
    if not code_nodes:
        log.info("No code nodes found in graph; skipping spec-code linking")
        return []

    log.info(
        "Linking specs to code: %d indexed EIPs, %d code nodes",
        len(indexed_eips),
        len(code_nodes),
    )

    # Deduplicate: (eip, code_node_id, relation) -> best link (highest confidence)
    best_links: dict[tuple[int, str, str], dict[str, Any]] = {}

    def _track(link: dict[str, Any]) -> None:
        key = (link["eip"], link["code_node_id"], link["relation"])
        existing = best_links.get(key)
        if existing is None or link["confidence"] > existing["confidence"]:
            best_links[key] = link

    for node in code_nodes:
        # Heuristic 2 — symbol name
        for link in _heuristic_symbol_name(node, indexed_eips):
            _track(link)

        # Heuristic 3 — test file path
        for link in _heuristic_file_path(node, indexed_eips):
            _track(link)

    # Enrich links with eip_node_id
    for link in best_links.values():
        eip_node_id = _find_eip_node_id(conn, link["eip"])
        link["eip_node_id"] = eip_node_id
        # eip_section_anchor not used by heuristics — always None
        link.setdefault("eip_section_anchor", None)

    results = list(best_links.values())
    log.info("Found %d spec-code links via heuristics", len(results))
    return results


def find_spec_code_links_from_text(
    node: dict[str, Any],
    text: str,
    indexed_eips: set[int],
) -> list[dict[str, Any]]:
    """Find spec-code links for a single code node using its text content.

    This is intended to be called during graph building when chunk text is
    available.  Returns link dicts ready for ``upsert_spec_code_link()``.
    """
    links: list[dict[str, Any]] = []

    for link in _heuristic_eip_ref_in_text(node, text, indexed_eips):
        links.append(link)

    return links
