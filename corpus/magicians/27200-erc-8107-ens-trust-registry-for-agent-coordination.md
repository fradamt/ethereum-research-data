---
source: magicians
topic_id: 27200
title: "ERC-8107: ENS Trust Registry for Agent Coordination"
author: KBryan
date: "2025-12-17"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8107-ens-trust-registry-for-agent-coordination/27200
views: 60
likes: 0
posts_count: 1
---

# ERC-8107: ENS Trust Registry for Agent Coordination

## Summary

Web of trust validation using ENS names for ERC-8001 multi-party coordination.

## Abstract

This ERC defines a Trust Registry where agents establish and query transitive trust relationships using ENS names as identifiers. Trust propagates through signature chains following the GnuPG web of trust model, enabling coordinators to gate participation based on trust graph proximity.

## Motivation

[ERC-8001](https://eips.ethereum.org/EIPS/eip-8001) defines minimal primitives for multi-party agent coordination but explicitly defers reputation to modules:

> “Privacy, thresholds, bonding, and cross-chain are left to modules.”

This ERC provides that reputation module.

## Key Design Decisions

**Why ENS?**

- Final standard (ERC-137)
- Battle-tested identity layer
- Built-in ownership semantics
- No dependency on draft standards

**Why Web of Trust?**

- Proven model (25+ years in GnuPG)
- Decentralized — no central registrar
- Agents can automate trust propagation

**Trust Levels**

| Level | Meaning |
| --- | --- |
| Unknown | No relationship |
| None | Explicitly distrusted |
| Marginal | Partial trust — multiple required |
| Full | Complete trust — single attestation sufficient |

## Links

- PR: Add ERC: ENS Trust Registry for Agent Coordination by KBryan · Pull Request #1412 · ethereum/ERCs · GitHub
- ERC-8001: ERC-8001: Agent Coordination Framework

Feedback welcome on the trust validation algorithm and ERC-8001 integration approach.
