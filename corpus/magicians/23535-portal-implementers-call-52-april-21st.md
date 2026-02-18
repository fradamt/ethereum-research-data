---
source: magicians
topic_id: 23535
title: Portal Implementers Call #52 - April 21st
author: system
date: "2025-04-14"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-52-april-21st/23535
views: 46
likes: 1
posts_count: 2
---

# Portal Implementers Call #52 - April 21st

## Meeting Info

- Apr 21, 16:30 UTC
- Duration: 30 minutes
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates

[GitHub Issue](https://github.com/ethereum/pm/issues/1471)

## Replies

**Chloe** (2025-04-22):

This week’s call notes:

### 1. Team update

- Update on Trin & Glados by Milos

Improved bridge functionality

Supported e2hs files for gossiping history
- Updated all bridges to use census / offer, enabling direct offer instead of gossip logic

Added ephemeral header content type definition (not active yet)
Ongoing PRs on Deneb proof generation & validation, and Electra consensus types
Glados: Implemented protocol version tracking for peers

- Trin, Fluffy, and Shisui now all officially supports v1

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [ScottyPoi](https://github.com/ScottyPoi)

- v1 is implemented but not publicly updated yet
- Continued working with DevOps to revamp boot node setup
- Awaiting ChainSafe to release an update that includes the bug fix discussed last week

Update on [Shisui](https://github.com/zen-eth/shisui) by [Qi Zhou](https://github.com/qizhou)

- Profiling ongoing to resolve performance issues (especially in comparison to Trin)
- Implemented new RPC endpoints to support missing JSON-RPC APIs
- Added caching for the highest compatible version to speed up lookups

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- Focused on integration with Besu

Currently managed to run Samba inside Besu locally, but still need further polishing & adjustments
- Aim to support Samba both within Besu and as a standalone solution
- Working toward deployment / testing of Samba in Besu across versions to evaluate performance and behavior

### 2. Discussion: Head-MPT State Network Spec

- Key problem

How to update slices of state for nodes whose section had no updates in a given block

Proposed Solution: Introduce block-level MPT diffs as a formalized content type

- Each block contains a diff from the previous block’s state
- Allow nodes to update and re-anchor their data to the latest MPT root, even if their slice didn’t change
- Enable a lightweight initial rollout - nodes can sync & operate without full account state storage initally

Sync Mechanism

- New nodes can sync from the current trie and fast-forward using accumulated diffs
- Trie diffs will be the main data gossiped on the network
- While the protocol supports querying individual trie nodes, gossiping individual nodes isn’t the focus

Implementation Roadmap for client teams

- 1st priority: Finalize ephemeral header support in the History Network
- 2nd priority: Push the State Network as close to the chain head as possible
- Afterwards: Define block-level diff data type, and implement diff generation & propagation

Relevant PR/ issue: [Add first version of the spec for the Head-MPT State network by morph-dev · Pull Request #389 · ethereum/portal-network-specs · GitHub](https://github.com/ethereum/portal-network-specs/pull/389)

