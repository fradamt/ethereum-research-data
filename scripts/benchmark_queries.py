"""Ground truth query set for erd-search benchmark.

Derived from 4 rounds of manual testing (~500+ queries) between 2026-02-17
and 2026-02-18. Each query has relevance patterns, strong-match patterns,
anti-patterns, and expected source distributions.

Scoring methodology:
- relevance_patterns: regex matched against title + text; any hit = relevant
- strong_patterns: subset indicating a great result (not just tangentially relevant)
- anti_patterns: patterns indicating a genuinely wrong result (contamination)
- expected_source_kinds: which source types should appear in results
- expand_for_hybrid: whether to apply query expansion for hybrid/semantic modes

Categories:
- jargon: Ethereum-specific technical terms the embedding model must understand
- conceptual: abstract protocol design questions
- natural: natural language / conversational queries
- identifier: exact EIP numbers, function names
- edge: known hard cases and failure modes
"""

from __future__ import annotations

BENCHMARK_QUERIES: list[dict] = [
    # =========================================================================
    # SANITY CHECKS — should score 5/5 across all modes
    # These worked perfectly (5/5 all modes) in retest #3.
    # =========================================================================
    {
        "id": "pbs",
        "query": "proposer-builder separation",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)proposer.?builder.?sep",
            r"(?i)\bPBS\b",
            r"(?i)block\s+build(er|ing).*propos",
            r"(?i)mev.*(auction|relay|boost)",
            r"(?i)builder.*api",
        ],
        "strong_patterns": [
            r"(?i)proposer.?builder.?sep",
            r"(?i)\bPBS\b.*(?:design|mechanism|protocol|relay)",
            r"(?i)two.?slot.*PBS",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
            r"(?i)Natspec.*Radspec",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "ssf",
        "query": "single slot finality tradeoffs",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)single.?slot.?finality",
            r"(?i)\bSSF\b",
            r"(?i)finality.*slot",
            r"(?i)slot.*finality",
            r"(?i)3sf|three.?slot.?finality",
        ],
        "strong_patterns": [
            r"(?i)single.?slot.?finality.*(tradeoff|design|analysis|overhead)",
            r"(?i)\bSSF\b.*(tradeoff|latency|committee|security)",
            r"(?i)paths?\s+to\s+single\s+slot\s+finality",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "blob-propagation",
        "query": "blob propagation latency",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)blob.*propagat",
            r"(?i)propagat.*blob",
            r"(?i)blob.*latency",
            r"(?i)blob.*network",
            r"(?i)data.*propagat.*beacon",
        ],
        "strong_patterns": [
            r"(?i)blob\s+propagat.*latency",
            r"(?i)blob.*broadcast.*timing",
            r"(?i)potuz",  # potuz's blob propagation paper was key result
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "verkle-tree",
        "query": "verkle tree state",
        "category": "jargon",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)verkle",
            r"(?i)vector\s+commit.*trie",
        ],
        "strong_patterns": [
            r"(?i)verkle.*(tree|trie|state|proof|transition)",
            r"(?i)verkle.*migration",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "validator-withdrawal",
        "query": "validator withdrawal process",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)withdraw(al)?.*validat",
            r"(?i)validat.*withdraw",
            r"(?i)process_withdrawal",
            r"(?i)withdrawal.*(queue|request|credential)",
            r"(?i)BLS.*withdrawal",
        ],
        "strong_patterns": [
            r"(?i)withdrawal.*(process|mechanism|queue|spec|design)",
            r"(?i)validator.*withdrawal.*(credential|address)",
            r"(?i)EIP.?7002",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    # =========================================================================
    # TECHNICAL JARGON — test embedding model's domain understanding
    # These probe whether the model knows Ethereum-specific terms.
    # =========================================================================
    {
        "id": "kzg-commitment",
        "query": "KZG commitment verification",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bKZG\b",
            r"(?i)kate.*polynomial",
            r"(?i)polynomial.*commit",
            r"(?i)trusted\s+setup",
            r"(?i)pairing.*check",
        ],
        "strong_patterns": [
            r"(?i)\bKZG\b.*(?:commit|verif|proof|open)",
            r"(?i)kate.*polynomial.*commit",
            r"(?i)polynomial.*commit.*verif",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)\bECDSA\b",  # embedding model confused KZG with ECDSA
            r"(?i)\bPEPC\b(?!.*KZG)",  # PEPC without KZG context = wrong
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "ssz-merkleization",
        "query": "SSZ Merkleization",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bSSZ\b",
            r"(?i)simple.?serialize",
            r"(?i)merkle.?iz",
            r"(?i)hash_tree_root",
            r"(?i)generalized.?index",
        ],
        "strong_patterns": [
            r"(?i)\bSSZ\b.*(?:merkle|tree|serial|format)",
            r"(?i)simple.?serialize.*merkle",
            r"(?i)hash_tree_root",
            r"(?i)SSZ.*(?:ProgressiveList|Container|Union)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
            r"(?i)ABI.*JSON",  # nomic returned ABI/JSON code for SSZ
            r"(?i)Constantinople",  # nomic returned Constantinople fork code
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "das-polynomial",
        "query": "DAS polynomial commitment proof",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bDAS\b",
            r"(?i)data.?availability.?sampl",
            r"(?i)polynomial.*commit",
            r"(?i)erasure.?cod",
            r"(?i)PeerDAS",
            r"(?i)danksharding",
        ],
        "strong_patterns": [
            r"(?i)(?:DAS|data.?availability.?sampl).*(?:polynomial|commit|proof|opening)",
            r"(?i)polynomial.*(?:opening|proof).*(?:DAS|sampling)",
            r"(?i)PeerDAS.*(design|proof|column)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
            r"(?i)Collaborative Rollup",  # nomic returned this for DAS
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "gossipsub-mesh",
        "query": "gossipsub mesh peers",
        "category": "jargon",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)gossipsub",
            r"(?i)gossip\s+sub",
            r"(?i)mesh.*peer",
            r"(?i)peer.*mesh",
            r"(?i)pubsub.*scor",
            r"(?i)topic.*mesh",
        ],
        "strong_patterns": [
            r"(?i)gossipsub.*(mesh|peer|scoring|protocol)",
            r"(?i)mesh.*(peer|management|grafting|pruning)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
            r"(?i)sharding",  # semantic added sharding noise for gossipsub
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "attestation-aggregation",
        "query": "attestation aggregation subnet",
        "category": "jargon",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)attestation.*aggregat",
            r"(?i)aggregat.*attestation",
            r"(?i)subnet.*attestation",
            r"(?i)compute_subnet",
            r"(?i)committee.*aggregat",
        ],
        "strong_patterns": [
            r"(?i)attestation.*aggregat.*(subnet|committee|design)",
            r"(?i)subnet.*(attestation|aggregat)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    # =========================================================================
    # EXACT IDENTIFIERS — test keyword precision
    # =========================================================================
    {
        "id": "eip-4844",
        "query": "EIP-4844 proto-danksharding",
        "category": "identifier",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)EIP.?4844",
            r"(?i)proto.?danksharding",
            r"(?i)blob.?transaction",
            r"(?i)shard.?blob",
        ],
        "strong_patterns": [
            r"(?i)EIP.?4844",
            r"(?i)proto.?danksharding",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "eip-1559",
        "query": "EIP-1559 base fee mechanism",
        "category": "identifier",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)EIP.?1559",
            r"(?i)base.?fee",
            r"(?i)fee.?burn",
            r"(?i)dynamic.?fee",
        ],
        "strong_patterns": [
            r"(?i)EIP.?1559.*(?:base.?fee|mechanism|design)",
            r"(?i)base.?fee.*(?:mechanism|burn|adjustment|update)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "process-attestation",
        "query": "process_attestation",
        "category": "identifier",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)process_attestation",
            r"(?i)attestation.*process",
            r"(?i)on_attestation",
        ],
        "strong_patterns": [
            r"process_attestation",  # exact match, case-sensitive
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip", "code"],
        "modes_to_test": ["keyword", "hybrid_0.5"],
    },
    # =========================================================================
    # NATURAL LANGUAGE — test semantic understanding
    # =========================================================================
    {
        "id": "slashing-natural",
        "query": "what happens when a validator gets slashed",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)slash(ed|ing|er)",
            r"(?i)validator.*penalit",
            r"(?i)penalit.*validator",
            r"(?i)inactivity.*leak",
            r"(?i)slashing.*condition",
            r"(?i)ejection",
        ],
        "strong_patterns": [
            r"(?i)slash(ed|ing).*(?:penalty|condition|mechanism|process)",
            r"(?i)validator.*slash.*(?:what|how|when|process)",
            r"(?i)proposer.*slashing|attester.*slashing",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "eip1559-design-natural",
        "query": "why was the base fee designed to adjust each block",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)base.?fee",
            r"(?i)EIP.?1559",
            r"(?i)fee.*adjust",
            r"(?i)fee.*market",
            r"(?i)gas.*pricing",
            r"(?i)block.*fee.*updat",
        ],
        "strong_patterns": [
            r"(?i)(?:base.?fee|EIP.?1559).*(design|rationale|adjust|mechanism)",
            r"(?i)fee.*market.*(design|reform|mechanism)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "blob-network-natural",
        "query": "how do blobs get propagated across the network",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)blob.*propagat",
            r"(?i)propagat.*blob",
            r"(?i)blob.*gossip",
            r"(?i)blob.*broadcast",
            r"(?i)blob.*network",
            r"(?i)sidecar.*propagat",
        ],
        "strong_patterns": [
            r"(?i)blob.*(propagat|broadcast|gossip).*(network|p2p|peer)",
            r"(?i)potuz",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    # =========================================================================
    # EDGE CASES — known hard cases, push the quality frontier
    # =========================================================================
    {
        "id": "beacon-reorg",
        "query": "beacon chain reorganization",
        "category": "edge",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)reorg(aniz)?",
            r"(?i)chain.*reorganiz",
            r"(?i)beacon.*reorg",
            r"(?i)fork.?choice.*reorg",
            r"(?i)re-org",
            r"(?i)block.*revert",
            r"(?i)attestation.*reorg",
        ],
        "strong_patterns": [
            r"(?i)(?:beacon|chain).*reorg",
            r"(?i)reorg.*(resist|attack|depth|length)",
            r"(?i)proposer.*boost.*reorg",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "mev-extraction",
        "query": "MEV extraction techniques",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bMEV\b",
            r"(?i)maximal.?extractable.?value",
            r"(?i)miner.?extractable.?value",
            r"(?i)sandwich.*attack",
            r"(?i)front.?run",
            r"(?i)back.?run",
            r"(?i)flashbot",
        ],
        "strong_patterns": [
            r"(?i)\bMEV\b.*(extract|technique|attack|strateg|mitigat)",
            r"(?i)maximal.?extractable.*(technique|strateg)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Natspec.*Radspec",  # semantic returned Natspec for MEV
            r"(?i)Mining attacks on PoRA",
            r"(?i)\bMODEXP\b",  # expansion confused MEV with MODEXP
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "mev-consensus-security",
        "query": "MEV security implications on consensus",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bMEV\b",
            r"(?i)maximal.?extractable",
            r"(?i)consensus.*(security|attack|implication|impact)",
            r"(?i)validator.*incentive.*MEV",
            r"(?i)proposer.*MEV",
        ],
        "strong_patterns": [
            r"(?i)\bMEV\b.*(?:consensus|security|incentive|centraliz)",
            r"(?i)consensus.*(MEV|extractable)",
            r"(?i)proposer.*(?:builder|MEV).*(?:security|centraliz)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Natspec.*Radspec",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "das-security",
        "query": "data availability sampling security assumptions",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)data.?availability.?sampl",
            r"(?i)\bDAS\b",
            r"(?i)PeerDAS",
            r"(?i)erasure.*cod.*(security|assumption)",
            r"(?i)sampling.*(security|assumption|threat|attack)",
        ],
        "strong_patterns": [
            r"(?i)(?:DAS|data.?availability.?sampl).*(security|assumption|threat|attack|honest)",
            r"(?i)sampling.*(?:security|assumption|adversar)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "blob-gas-pricing",
        "query": "blob gas pricing",
        "category": "jargon",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)blob.*gas",
            r"(?i)gas.*blob",
            r"(?i)blob.*pric",
            r"(?i)blob.*fee",
            r"(?i)EIP.?4844.*gas",
            r"(?i)excess_blob_gas",
        ],
        "strong_patterns": [
            r"(?i)blob.*gas.*pric",
            r"(?i)blob.*base.*fee",
            r"(?i)blob.*fee.*market",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "lmd-ghost",
        "query": "LMD-GHOST fork choice",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)LMD.?GHOST",
            r"(?i)fork.?choice",
            r"(?i)latest.?message.?driven",
            r"(?i)greediest.?heaviest",
        ],
        "strong_patterns": [
            r"(?i)LMD.?GHOST.*fork.?choice",
            r"(?i)fork.?choice.*LMD",
            r"(?i)GHOST.*(?:FFG|Casper|fork)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
            r"(?i)Metamask",  # nomic returned Metamask for LMD-GHOST
        ],
        "expected_source_kinds": ["forum"],
    },
    # =========================================================================
    # ABBREVIATION-ONLY QUERIES — stress test for bare abbreviations
    # These are the worst case for nomic-embed-text: all return
    # "Mining attacks on PoRA" at semantic 1.0 without expansion.
    # =========================================================================
    {
        "id": "bare-ssz",
        "query": "SSZ",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bSSZ\b",
            r"(?i)simple.?serialize",
            r"(?i)hash_tree_root",
        ],
        "strong_patterns": [
            r"(?i)\bSSZ\b.*(format|spec|merkle|container|serial)",
            r"(?i)simple.?serialize",
        ],
        "anti_patterns": [
            r"(?i)Mining attacks on PoRA",
            r"(?i)TestPush",
        ],
        "expected_source_kinds": ["forum", "eip"],
        "modes_to_test": ["keyword", "hybrid_0.5", "hybrid_0.7", "semantic_1.0"],
    },
    {
        "id": "bare-ffg",
        "query": "FFG",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bFFG\b",
            r"(?i)friendly.?finality.?gadget",
            r"(?i)Casper.*finality",
            r"(?i)finality.*gadget",
            r"(?i)justif.*finaliz",
        ],
        "strong_patterns": [
            r"(?i)\bFFG\b.*(finality|Casper|gadget|justif)",
            r"(?i)friendly.?finality.?gadget",
            r"(?i)Casper.*FFG",
        ],
        "anti_patterns": [
            r"(?i)Mining attacks on PoRA",
            r"(?i)TestPush",
        ],
        "expected_source_kinds": ["forum"],
        "modes_to_test": ["keyword", "hybrid_0.5", "hybrid_0.7", "semantic_1.0"],
    },
    # =========================================================================
    # ADDITIONAL JARGON — expand domain coverage
    # =========================================================================
    {
        "id": "account-abstraction",
        "query": "account abstraction ERC-4337",
        "category": "jargon",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)account.?abstraction",
            r"(?i)ERC.?4337",
            r"(?i)EIP.?7702",
            r"(?i)smart.?account",
            r"(?i)user.?operation",
            r"(?i)paymaster",
            r"(?i)bundler",
        ],
        "strong_patterns": [
            r"(?i)account.?abstraction.*(design|mechanism|spec|proposal|ERC|EIP)",
            r"(?i)ERC.?4337.*(account|abstraction|bundler|paymaster)",
            r"(?i)EIP.?7702",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "eof-format",
        "query": "EOF EVM object format",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bEOF\b",
            r"(?i)EVM.?object.?format",
            r"(?i)EIP.?3540",
            r"(?i)code.?section",
            r"(?i)container.*format",
        ],
        "strong_patterns": [
            r"(?i)\bEOF\b.*(EVM|format|container|bytecode|v1)",
            r"(?i)EVM.?object.?format",
            r"(?i)EIP.?3540",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "inactivity-leak",
        "query": "inactivity leak mechanism",
        "category": "jargon",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)inactivity.?leak",
            r"(?i)inactivity.*penalty",
            r"(?i)leak.*penalty",
            r"(?i)offline.*validator.*penalty",
            r"(?i)quadratic.*leak",
        ],
        "strong_patterns": [
            r"(?i)inactivity.?leak.*(mechanism|penalty|design|analysis|quadratic)",
            r"(?i)quadratic.*inactivity",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "inclusion-list",
        "query": "inclusion list design FOCIL",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)inclusion.?list",
            r"(?i)\bFOCIL\b",
            r"(?i)fork.?choice.*inclusion",
            r"(?i)censorship.?resist",
            r"(?i)transaction.*inclusion.*guarantee",
        ],
        "strong_patterns": [
            r"(?i)inclusion.?list.*(design|mechanism|unconditional|FOCIL)",
            r"(?i)\bFOCIL\b",
            r"(?i)no.?free.?lunch.*inclusion",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "bls-aggregation",
        "query": "BLS signature aggregation",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bBLS\b",
            r"(?i)boneh.?lynn.?shacham",
            r"(?i)signature.*aggregat",
            r"(?i)aggregat.*signature",
            r"(?i)BLS12.?381",
        ],
        "strong_patterns": [
            r"(?i)\bBLS\b.*(?:signature|aggregat|pairing)",
            r"(?i)signature.*aggregat.*(BLS|beacon|validator)",
            r"(?i)pragmatic.*signature.*aggregation",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "proposer-boost",
        "query": "proposer boost fork choice",
        "category": "jargon",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)proposer.?boost",
            r"(?i)fork.?choice.*boost",
            r"(?i)boost.*fork.?choice",
            r"(?i)view.?merge",
            r"(?i)ex.?ante.*reorg",
        ],
        "strong_patterns": [
            r"(?i)proposer.?boost.*(fork.?choice|reorg|attack|replacement)",
            r"(?i)view.?merge.*proposer.?boost",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "rlp-encoding",
        "query": "RLP recursive length prefix encoding",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bRLP\b",
            r"(?i)recursive.?length.?prefix",
            r"(?i)RLP.*(encod|decod|serial)",
        ],
        "strong_patterns": [
            r"(?i)\bRLP\b.*(encod|decod|serial|format|prefix)",
            r"(?i)recursive.?length.?prefix",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "vdf-construction",
        "query": "VDF verifiable delay function",
        "category": "jargon",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bVDF\b",
            r"(?i)verifiable.?delay.?function",
            r"(?i)delay.*function.*verif",
            r"(?i)VDF.*(proof|RANDAO|random)",
        ],
        "strong_patterns": [
            r"(?i)\bVDF\b.*(verifiable|delay|construct|proof|RANDAO)",
            r"(?i)verifiable.?delay.?function",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "weak-subjectivity",
        "query": "weak subjectivity checkpoint",
        "category": "jargon",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)weak.?subjectiv",
            r"(?i)subjectiv.*checkpoint",
            r"(?i)checkpoint.?sync",
            r"(?i)long.?range.?attack",
        ],
        "strong_patterns": [
            r"(?i)weak.?subjectiv.*(checkpoint|period|bound|sync)",
            r"(?i)checkpoint.*(sync|subjectiv)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    # =========================================================================
    # ADDITIONAL CONCEPTUAL — protocol-level design questions
    # =========================================================================
    {
        "id": "preconfirmations",
        "query": "preconfirmations based preconfs",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)preconfirm",
            r"(?i)preconf",
            r"(?i)pre.?confirm",
            r"(?i)based.*preconf",
            r"(?i)commit.?boost",
        ],
        "strong_patterns": [
            r"(?i)preconfirm.*(design|mechanism|protocol|based|proposer|BFT)",
            r"(?i)based.*preconf",
            r"(?i)leaderless.*preconf",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "execution-tickets",
        "query": "execution tickets proposer market",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)execution.?ticket",
            r"(?i)ticket.*propos",
            r"(?i)propos.*ticket",
            r"(?i)execution.*auction",
            r"(?i)sealed.*execution",
        ],
        "strong_patterns": [
            r"(?i)execution.?ticket.*(market|design|mechanism|auction|proposer)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "light-client",
        "query": "light client sync committee protocol",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)light.?client",
            r"(?i)sync.?committee",
            r"(?i)light.*protocol",
            r"(?i)beacon.*light",
        ],
        "strong_patterns": [
            r"(?i)light.?client.*(sync|committee|protocol|proof|bridge)",
            r"(?i)sync.?committee.*(light|client|protocol|slashing)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "state-expiry",
        "query": "state expiry mechanism",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)state.?expir",
            r"(?i)state.*rent",
            r"(?i)stateless",
            r"(?i)address.*space.*extension",
            r"(?i)state.*growth",
        ],
        "strong_patterns": [
            r"(?i)state.?expir.*(mechanism|design|proposal|in.?protocol|out.?of.?protocol)",
            r"(?i)state.*rent.*(mechanism|design)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "staking-issuance",
        "query": "staking issuance curve",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)issuance.*(curve|rate|policy|reward)",
            r"(?i)staking.*(reward|yield|return|issuance|emission)",
            r"(?i)validator.*reward",
            r"(?i)monetary.*policy",
            r"(?i)endgame.*staking",
        ],
        "strong_patterns": [
            r"(?i)issuance.*(curve|adjustment|proposal|targeting|endgame)",
            r"(?i)staking.*(issuance|economics|incentive)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "rollup-da",
        "query": "rollup data availability requirements",
        "category": "conceptual",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)rollup.*data.?availab",
            r"(?i)data.?availab.*rollup",
            r"(?i)rollup.*blob",
            r"(?i)L2.*data.*availab",
            r"(?i)taxonomy.*data.*availab",
            r"(?i)calldata.*rollup",
        ],
        "strong_patterns": [
            r"(?i)rollup.*data.?availab.*(requirement|policy|assumption|cost)",
            r"(?i)taxonomy.*data.*availab.*rollup",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    # =========================================================================
    # ADDITIONAL NATURAL LANGUAGE — conversational queries
    # =========================================================================
    {
        "id": "committee-natural",
        "query": "how are validator committees selected each slot",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)committee.*(select|assign|shuffle|random)",
            r"(?i)validator.*(committee|assign|shuffle)",
            r"(?i)beacon.*committee",
            r"(?i)RANDAO.*committee",
            r"(?i)slot.*committee",
        ],
        "strong_patterns": [
            r"(?i)committee.*(selection|assignment|shuffle|algorithm)",
            r"(?i)validator.*(committee|assignment).*(slot|epoch|random)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "da-rollup-natural",
        "query": "why do we need data availability for rollups",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)data.?availab",
            r"(?i)rollup",
            r"(?i)blob.*rollup",
            r"(?i)fraud.?proof.*data",
            r"(?i)validity.?proof.*data",
        ],
        "strong_patterns": [
            r"(?i)data.?availab.*(rollup|L2|fraud|validity)",
            r"(?i)rollup.*(data.?availab|blob|calldata)",
            r"(?i)why.*(data.?availab|blob)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "inactivity-natural",
        "query": "how does the inactivity leak punish offline validators",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)inactivity.?leak",
            r"(?i)offline.*validator",
            r"(?i)validator.*offline",
            r"(?i)inactivity.*penalty",
            r"(?i)penalty.*inactive",
            r"(?i)leak.*score",
        ],
        "strong_patterns": [
            r"(?i)inactivity.?leak.*(punish|penalty|mechanism|offline)",
            r"(?i)offline.*validator.*(penalty|punish|leak)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "nothing-at-stake-natural",
        "query": "how does proof of stake prevent nothing at stake attacks",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)nothing.?at.?stake",
            r"(?i)proof.?of.?stake.*(attack|security|assumption)",
            r"(?i)stake.*(attack|security|nothing)",
            r"(?i)long.?range.?attack",
            r"(?i)slashing.*double",
            r"(?i)fork.*penalty",
        ],
        "strong_patterns": [
            r"(?i)nothing.?at.?stake.*(attack|problem|prevent)",
            r"(?i)proof.?of.?stake.*(security|assumption|risk)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    {
        "id": "validator-deposit-natural",
        "query": "how much ETH do you need to run a validator",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)32\s*ETH",
            r"(?i)deposit.*validator",
            r"(?i)validator.*deposit",
            r"(?i)minimum.*stak",
            r"(?i)staking.*requirement",
            r"(?i)solo.*stak",
            r"(?i)no.*minimum.*stak",
            r"(?i)join.*validator",
            r"(?i)validator.*requirement",
            r"(?i)run.*validator",
            r"(?i)become.*validator",
        ],
        "strong_patterns": [
            r"(?i)32\s*ETH.*(deposit|stake|validator|minimum)",
            r"(?i)validator.*deposit.*(amount|minimum|32)",
            r"(?i)minimum.*ETH.*stak",
            r"(?i)requirement.*(run|join|become).*validator",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "light-client-natural",
        "query": "how do light clients verify the beacon chain without downloading everything",
        "category": "natural",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)light.?client",
            r"(?i)sync.?committee",
            r"(?i)stateless.*verif",
            r"(?i)light.*verif",
            r"(?i)merkle.*proof.*light",
        ],
        "strong_patterns": [
            r"(?i)light.?client.*(verif|proof|sync|protocol|trust)",
            r"(?i)sync.?committee.*(light|verif|proof)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    # =========================================================================
    # ADDITIONAL IDENTIFIERS — specific EIPs and function names
    # =========================================================================
    {
        "id": "eip-7732",
        "query": "EIP-7732 enshrined PBS",
        "category": "identifier",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)EIP.?7732",
            r"(?i)enshrined.*PBS",
            r"(?i)\bePBS\b",
            r"(?i)enshrined.*proposer.?builder",
        ],
        "strong_patterns": [
            r"(?i)EIP.?7732",
            r"(?i)\bePBS\b.*(enshrined|design|spec|mechanism)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "eip-7702",
        "query": "EIP-7702 set EOA account code",
        "category": "identifier",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)EIP.?7702",
            r"(?i)set.*EOA.*code",
            r"(?i)account.?abstraction.*7702",
            r"(?i)authorization.*delegate",
        ],
        "strong_patterns": [
            r"(?i)EIP.?7702",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    {
        "id": "eip-7251",
        "query": "EIP-7251 max effective balance",
        "category": "identifier",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)EIP.?7251",
            r"(?i)MAX_EFFECTIVE_BALANCE",
            r"(?i)max.*effective.*balance",
            r"(?i)increase.*effective.*balance",
            r"(?i)effective.?balance.*(design|neutral|increase|change|proposal)",
            r"(?i)consolidat.*validator",
        ],
        "strong_patterns": [
            r"(?i)EIP.?7251",
            r"(?i)MAX_EFFECTIVE_BALANCE.*(increase|raise|change)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum", "eip"],
    },
    # =========================================================================
    # ADDITIONAL EDGE CASES — more bare abbreviations and stress tests
    # =========================================================================
    {
        "id": "bare-randao",
        "query": "RANDAO",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bRANDAO\b",
            r"(?i)random.*number.*dao",
            r"(?i)beacon.*random",
            r"(?i)randomness.*beacon",
        ],
        "strong_patterns": [
            r"(?i)\bRANDAO\b.*(bias|exploit|random|beacon|analysis)",
            r"(?i)random.*number.*generation.*dao",
        ],
        "anti_patterns": [
            r"(?i)Mining attacks on PoRA",
            r"(?i)TestPush",
        ],
        "expected_source_kinds": ["forum"],
        "modes_to_test": ["keyword", "hybrid_0.5", "hybrid_0.7", "semantic_1.0"],
    },
    {
        "id": "bare-bls",
        "query": "BLS",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bBLS\b",
            r"(?i)boneh.?lynn.?shacham",
            r"(?i)BLS12.?381",
            r"(?i)signature.*aggregat",
        ],
        "strong_patterns": [
            r"(?i)\bBLS\b.*(signature|aggregat|key|pairing|12.?381)",
            r"(?i)boneh.?lynn.?shacham",
        ],
        "anti_patterns": [
            r"(?i)Mining attacks on PoRA",
            r"(?i)TestPush",
        ],
        "expected_source_kinds": ["forum", "eip"],
        "modes_to_test": ["keyword", "hybrid_0.5", "hybrid_0.7", "semantic_1.0"],
    },
    {
        "id": "bare-mev",
        "query": "MEV",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bMEV\b",
            r"(?i)maximal.?extractable.?value",
            r"(?i)miner.?extractable.?value",
            r"(?i)flashbot",
        ],
        "strong_patterns": [
            r"(?i)\bMEV\b.*(extract|auction|mitigation|relay|boost|block)",
            r"(?i)maximal.?extractable",
        ],
        "anti_patterns": [
            r"(?i)Mining attacks on PoRA",
            r"(?i)TestPush",
        ],
        "expected_source_kinds": ["forum"],
        "modes_to_test": ["keyword", "hybrid_0.5", "hybrid_0.7", "semantic_1.0"],
    },
    {
        "id": "bare-das",
        "query": "DAS",
        "category": "edge",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)\bDAS\b",
            r"(?i)data.?availability.?sampl",
            r"(?i)PeerDAS",
            r"(?i)erasure.?cod",
        ],
        "strong_patterns": [
            r"(?i)\bDAS\b.*(sampl|availability|polynomial|erasure|column)",
            r"(?i)data.?availability.?sampl",
        ],
        "anti_patterns": [
            r"(?i)Mining attacks on PoRA",
            r"(?i)TestPush",
        ],
        "expected_source_kinds": ["forum"],
        "modes_to_test": ["keyword", "hybrid_0.5", "hybrid_0.7", "semantic_1.0"],
    },
    {
        "id": "long-ssf-natural",
        "query": "what are the security tradeoffs of single slot finality compared to multi-epoch finality",
        "category": "edge",
        "expand_for_hybrid": False,
        "relevance_patterns": [
            r"(?i)single.?slot.?finality",
            r"(?i)\bSSF\b",
            r"(?i)finality.*(tradeoff|security|latency|overhead)",
            r"(?i)epoch.*finality",
            r"(?i)fast.*finality",
        ],
        "strong_patterns": [
            r"(?i)single.?slot.?finality.*(security|tradeoff|compar)",
            r"(?i)finality.*(security|tradeoff).*(single|slot|epoch)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
    # =========================================================================
    # CROSS-DOMAIN — test when query spans multiple concepts
    # =========================================================================
    {
        "id": "casper-ffg-finality",
        "query": "Casper FFG finality gadget",
        "category": "conceptual",
        "expand_for_hybrid": True,
        "relevance_patterns": [
            r"(?i)Casper",
            r"(?i)\bFFG\b",
            r"(?i)finality.*gadget",
            r"(?i)justif.*finaliz",
            r"(?i)checkpoint.*finality",
        ],
        "strong_patterns": [
            r"(?i)Casper.*FFG",
            r"(?i)FFG.*Casper",
            r"(?i)friendly.?finality.?gadget",
            r"(?i)Casper.*finality.*(gadget|mechanism|proof)",
        ],
        "anti_patterns": [
            r"(?i)TestPush",
            r"(?i)Mining attacks on PoRA",
        ],
        "expected_source_kinds": ["forum"],
    },
]

# Default modes to test when not overridden per-query
DEFAULT_MODES = ["keyword", "hybrid_0.5", "hybrid_0.7", "semantic_1.0"]

# Category descriptions for reporting
CATEGORY_DESCRIPTIONS: dict[str, str] = {
    "jargon": "Ethereum-specific technical terms (tests embedding model domain knowledge)",
    "conceptual": "Abstract protocol design questions (should work well across all modes)",
    "natural": "Natural language / conversational queries (semantic should help)",
    "identifier": "Exact EIP numbers, function names (keyword should dominate)",
    "edge": "Known hard cases and failure modes (establishes quality ceiling)",
}
