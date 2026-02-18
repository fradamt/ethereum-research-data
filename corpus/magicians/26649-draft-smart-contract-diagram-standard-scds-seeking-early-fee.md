---
source: magicians
topic_id: 26649
title: "[Draft] Smart Contract Diagram Standard (SCDS): Seeking Early Feedback"
author: George
date: "2025-11-20"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/draft-smart-contract-diagram-standard-scds-seeking-early-feedback/26649
views: 73
likes: 0
posts_count: 1
---

# [Draft] Smart Contract Diagram Standard (SCDS): Seeking Early Feedback

Hey everyone - I’m working on a ERC for a Smart Contract Diagram Standard (SCDS), and I’d like early feedback before turning it into a formal ERC submission.

## Why?

Diagrams across the ecosystem (docs, audits, protocols) are inconsistent in semantics and structure.

Different teams use different shapes, vocabularies, and ad-hoc diagramming conventions, making it hard for humans and tools to reason about:

- governance and privilege flows
- callgraphs and dependencies
- fund/asset flows
- cross-chain or modular architectures

A shared, machine-readable semantic model would enable consistent docs, auto-generated diagrams, better audits, and easier integration for LLMs and analysis tools.

---

# What I’m Proposing

**SCDS** defines a minimal semantic model + JSON format for two diagram types:

### 1. Architecture diagrams

Describe *what the system is* (contracts, actors, systems, assets, privileges, dependencies).

No timing, no ordering.

### 2. Process diagrams

Describe *how actions occur* (transactions, internal calls, value flows, data submissions).

Includes ordered steps and process nodes.

The standard also supports:

- a minimal set of node kinds (contract, actor, system, asset, process…)
- a minimal set of relationship kinds (CALL / DELEGATECALL / TRANSFER / MINT / CAN_UPGRADE / RELAYS / etc.)
- hierarchical refinement (L0 → L1 → L2) via refinesDiagram and expands fields
- a single-file structure containing one full diagram plus all refinements (unique IDs across the file)
- key/value tags for extensibility and custom patterns

Visualization is intentionally out of scope. I would like to achieve shared semantics, not necessarily style or aesthetics (though I do propose some shapes for some object types).

---

# Overall JSON structure (very high-level)

Diagram JSON file:

```auto
{
  "id": "diagram-id",
  "label": "Name",
  "diagramType": "architecture | process",
  "level": 0,
  "refinesDiagram": null,
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

Node format:

```auto
{
  "id": "node-id",
  "label": "Node",
  "kind": "contract | library | ...",
  "tags": {
    "type": "upgradeable", ...
  },
  "contains": [],
  "expands": null
}
```

Edge format:

```auto
{
  "id": "e1",
  "from": "node-id",
  "to": "node-id",
  "kind": "TRANSACTION | CALL | TRANSFER |...",
  "tags": { "asset": "ETH",... },
  "step": 1
}
```

Nodes + edges include kinds, tags, ordering (for processes), and refinement hooks.

Full details in the draft below.

---

Naturally, I would love some feedback! The draft of the spec is below, and it may be useful to look over the node and edge section as it has the most opinionated parts, which is where I think the standard can be most useful.

1. Is the semantic model (node kinds / edge kinds) minimal but sufficient?
2. Does the architecture vs process split make sense? Should there be more types? Just keep to one?
3. Anything missing for complex systems (L2s, bridges, oracles, intent systems, vaults, etc.)? Should there be more kinds to nodes and edges?

---

# Full Draft (for those who want details)

https://docs.google.com/document/d/15PnEsKRqUgCXrD24eKuOYdykWHeda4pXut2Txk-sLr8/edit?usp=sharing
