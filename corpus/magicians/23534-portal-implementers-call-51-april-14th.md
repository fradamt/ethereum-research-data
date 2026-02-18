---
source: magicians
topic_id: 23534
title: Portal Implementers Call #51 - April 14th
author: system
date: "2025-04-14"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-51-april-14th/23534
views: 44
likes: 1
posts_count: 2
---

# Portal Implementers Call #51 - April 14th

## Meeting Info

- Apr 14, 16:30 UTC
- Duration: 30 minutes
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates

[GitHub Issue](https://github.com/ethereum/pm/issues/1470)

## Replies

**Chloe** (2025-04-14):

This week’s notes:

### 1. Team update

- Update on Trin & Glados by Kolby and Mike

Implemented Protocol versioning & v1
- Fixed bug in JSON-RPC result for the offer method
- Performance improvements of e2hs writer

44× speedup for converting era1 to e2hs files
- 6× speedup for converting era to e2hs files
- Now pre-merge e2hs files can be generated in ~10s and post-merge e2hs files in ~5 minutes

Plan to run Bridges fully on e2hs files with public endpoints soon
Discussion on adopting e2hs format as a standard post-merge history format

- Nearly ready for broader feedback & adoption once the full repo is generated and publicly available

Glados update

- Finished schema change last week, allowing UTP health visibility
- Deploy sync auditing this week
- Plan to work on protocol versioning visibility next week

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [ScottyPoi](https://github.com/ScottyPoi)

- v1 protocol version merged and unit tested
- Fixed bugs in discv5 test suite

3 PRs submitted to ChainSafe’s discv5 implementation to fix ID encoding, challenge re-sending, and byte/int conversion bugs

Continued revamping public node setup with devops team for better reliability

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- First call with Besu team to align on plugin use and integration

Need to change certain discv5 endpoints from Besu side to integrate with Samba

Working in parallel on

- Endpoint completion
- Design shift from standalone to plugin-compatible mode

Update on [Shisui](https://github.com/zen-eth/shisui) by [Qi Zhou](https://github.com/qizhou)

- Implemented protocol versioning v1 and updated offer interface
- Fixed a panic issue related to closing connections on errors
- Addressing performance issue

Working on utp rate limiting to optimize gossip
- Benchmarking ongoing to resolve performance gaps vs Trin

### 2. Discussion topics

#### 2.1 Head-MPT State Network Spec

- Design overview

The Head-MPT State Network will initially be a separate sub-network (not merged with the existing state network) for faster iteration, with potential future integration

Scope

- Focused on the last 256 blocks, with nodes anchoring content via state roots or block hashes

Content Types

- Gossiped data includes account trie nodes, bytecodes, and storage trie nodes
- Each node anchors content to the state root

Gossip mechanism

- Bridges split the trie diff into 256 subtries and gossip each as a key-value pair
- Nodes store and update assigned subtrie based on their node ID
- Nodes retain their subtrie for the last 256 blocks, discarding older ones

Querying & sync

- Direct leaf queries are supported with proofs
- Nodes can fetch missing individual trie nodes when bootstrapping or syncing

Implementation Phasing

- Start with account trie only
- Contract trie support will follow after validation

Next step

- Client teams are encourated to review the PR and provide feedback
- Deeper discussion scheduled for next week’s call (or the week after if there is light attendance next week due to Easter)

Relevant PR/ issue: [Add first version of the spec for the Head-MPT State network by morph-dev · Pull Request #389 · ethereum/portal-network-specs · GitHub](https://github.com/ethereum/portal-network-specs/pull/389)

