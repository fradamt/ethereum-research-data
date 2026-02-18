---
source: magicians
topic_id: 23186
title: Portal Implementers Call #48 - March 24th
author: system
date: "2025-03-18"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-48-march-24th/23186
views: 53
likes: 0
posts_count: 2
---

# Portal Implementers Call #48 - March 24th

## Meeting Info

- Mar 24, 16:30 UTC
- Duration: 30 minutes
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates
- Offer/Accept codes network upgrade

[GitHub Issue](https://github.com/ethereum/pm/issues/1392)

## Replies

**Chloe** (2025-03-24):

This week’s call notes below:

### 1. Team update

- Update on Trin by Ognyan

Cleaned up history storage by removing old content value types
- Refactored e2store header types for compatibility
- Implemented ping extensions for JSON RPC endpoints
- Added ephemeral store as a step toward ephemeral content for the History network

Update on [Fluffy](https://github.com/status-im/nimbus-eth1/tree/master/fluffy) by [Kim](https://github.com/kdeme)

- Tuned the PoC syncing Nimbus EL from Portal Netowrk: incl. adjust recursive finContent concurrency (reducing requests from 3 to 2 slightly improved performance)
- Observed that ~10% of recursive findContent requests timeout when sending 2-3 concurrent queries, potentially due to udp packet loss or async lib issue
- Improved ContentDB pruning mechanism for speed
- Integrated EVM and implemented eth_call, yielding a ~20% performance improvement
- Started investigating the issue of discv5 protocol handling multiple concurrent requests

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [ScottyPoi](https://github.com/ScottyPoi)

- Finalized ping extension for JSON RPC endpoints
- Improved pruning mechanism (now more deterministic behavior with reduced overlaps)
- Released major update with EthereumJS lib
- Progressed on ephemeral header implementation
- Preparing on Portal integration with EthereumJS client

Update on [Shisui](https://github.com/zen-eth/shisui) by [Qi Zhou](https://github.com/qizhou)

- Geth integration process update

PR re. repeat challenge in “who you are” handshake: Merged and currently being tested on Hive, have some issues with Fluffy nodes (need further investigation)
- PR re. ping extension for JSON RPC endpoints: In final review stasge, expected to be merged shortly

Collaborated with Geth to make Shisui run as an independent sub-process for Portal Network access

- Initial implementation planned by end of this month

Other work incl.

- Participated in protocol versioning discussion
- Start working on detailed offer decline code
- Fixed race condition issues

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- Close to passing all Hive tests, except a bug in putContent gossip handling
- Slightly behind on SSZ union removal and ephemeral headers implementation
- Working in parallel to integrate Samba as a plugin for Besu
- Nearest goal is to fix the putContent bug and make initial progress on Besu plugin integration

### 2. Roll out network changes using Protocol Versioning

- Deployment approach

Team agree to roll out offer/accept code changes using protocol versioning
- Clients will start supporting both old & new versions and signal protocol version through ENR

Glados Monitoring

- Need to add a tracking table on Glados to show the protocol versioning states

Issue discussed

- Versioning semantic: Whether to rename portal wire protocol version to a more general portal version for future clarity
- Lack of size prefix: FindContent/ Content request lacks a size prefix, making it difficult to distinguish between incomplete and invalid data, potentially leading to incorrect peer ban

Action items for protocol version 1

- Deploy offer/ accept codes
- Add length prefix to uTP streams

Related PR/ issue

- Deploy accept codes · Issue #375 · ethereum/portal-network-specs · GitHub
- FindContent results over uTP does not allow for discerning between incomplete and invalid data · Issue #380 · ethereum/portal-network-specs · GitHub
- Show protocol versioning statistics · Issue #382 · ethereum/glados · GitHub

### 3. Banning/ Peer handling

- Risk of peer banning

Could backfire in edge cases, eg. banning all peers during local network outage
- May accidentally isolate nodes from the network

Peer scoring is preferred over hard bans

- Prioritize good peers rather than punishing bad ones

### 4. Handling Ephemeral State Content

- Main issue

Current trie-based model struggles with ephemeral state management during chain reorgs, as state content can exist on both canonical and non-canoncial chain
- The issue arises when attempting to migrate state content to permanent storage or delete non-canonical chain related content after finality

Potential solutions

- Solution 1: Modify content keys to include block hashes, enabling proof tracking across forks (but risks redundant storage)
- Solution 2: Restrict trie-based model to finalized state only, using the flat model for ephemeral data near the chain head

Team consensus

- Favored Solution 2 for simplicity
- Open questions

Define the threshold of “finalized” (EL/ CL finality vs practical limits)
- Document verification rules for headers near the head of the chain

Action items

- Formalize flat model spec, led by Milos
- Clarify finality checks in the state network specs

Related PR/ issue

- Handling Ephemeral State content · Issue #382 · ethereum/portal-network-specs · GitHub

### 5. Storage of Ephemeral Block Bodies/ Receipts

- Main question

How clients choose to store the ephemeral block bodies/ receipts? Whether they should be store permanently?

Potential approach

- Pre-finalized data: Keep in-memory cache (auto-purged on finalization)
- Finalized data: Persist permanently (proofs are immutable post-finalization)

Client plans

- Trin: Testing in-memory storage for pre-finalized bodies/ receipts
- Fluffly: Exploring separate tables for headers/ bodies to enable efficient access & pruning, but still need further exploration

