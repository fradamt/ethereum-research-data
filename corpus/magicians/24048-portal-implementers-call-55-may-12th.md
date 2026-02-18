---
source: magicians
topic_id: 24048
title: Portal Implementers Call #55 - May 12th
author: system
date: "2025-05-05"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-55-may-12th/24048
views: 139
likes: 0
posts_count: 2
---

# Portal Implementers Call #55 - May 12th

## Meeting Info

- May 12, 2025, 16:30 UTC
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates

 **🤖 config**

- Duration in minutes : 30
- Recurring meeting : true
- Call series : Portal Implementers
- Occurrence rate : weekly
- Already a Zoom meeting ID : true # Set to true if this meeting is already on the auto recording Ethereum zoom (will not create a zoom ID if true)
- Already on Ethereum Calendar : true # Set to true if this meeting is already on the Ethereum public calendar (will not create calendar event)
- Need YouTube stream links : false # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

update mapping

[GitHub Issue](https://github.com/ethereum/pm/issues/1525)

## Replies

**Chloe** (2025-05-12):

This week’s notes:

### 1. Team update

- Update on Trin & Glados by Milos

Implemented support for Pectra types on the Beacon network
- Started adding initial support for Sepolia
- Ongoing work on implementing the bridge that will follow the chain head and generate e2hs files
- Glados: Updated areaGraph for cleaner visualization

Update on [Fluffy](https://github.com/status-im/nimbus-eth1/tree/master/fluffy) by [Kim](https://github.com/kdeme)

- Fixed a bug in HistoricalSummaries storage in beacon_db
- Explored experimental support for providing HistoricalSummaries as an Oracle to the History network (currently in testing, not merged yet)
- Implemented several performance improvements on State network for synchronous data processing
- Removed deprecated neighborhoodGossip logic
- Proposed PR to clarify that HistoricalSummaries must be from finalized beacon state

Nodes should only respond to HistoricalSummaries requests if they have data for the requested epoch or newer
- Otherwise, nodes should rely with an empty response (pending further clarification in the specs)

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [ScottyPoi](https://github.com/ScottyPoi)

- Progress on HistoricalSummaries and updating SSZ types
- Continued implementation of ephemeral headers
- Started implementing typing and distance functions of Head-MPT State Network
- Explored support for Sepolia recognized challenges in supporting multiple networks (mainnet & testnet) simultaneously

Update on [Shisui](https://github.com/zen-eth/shisui) by [Qi Zhou](https://github.com/qizhou)

- Fixed Hive test failures by addressing missing validation for historical network in findContent, especially for post-Shanghai data
- Addressed a lightclient error due to an JSON-RPC typo
- Split the ephemeral header PR into smaller parts for easier review

Implemented & merged the storage part
- Remaining features will be implemented in the coming weeks

Created a new benchmark to compare performance between Trin vs Shisui using the same payload

- Showed that discv5 from Geth implementation has significant overhead and slower compared raw uTP implementation
- The benchmark tests are currently ad hoc, but can potentially be modularized and reused across clients for performance debugging/ validation

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- Completed the accumulator functionality
- Ongoing work on protocol versioning and accept code
- Besu integration encountered some blockers (actively being addressed)

### 2. Discussion topics

#### 2.1 LightClientUpdatesByRange Behavior Change Proposal

- Current Spec: If a node is missing any update in a requested epoch range, it must not reply at all
- Proposed Change: Nodes should reply with available updates starting from the earliest in the range, even if incomplete

Rationale: Syncing nodes benefit from partial progress (getting closer to chain head)
- Impact: Able to avoids scenarios where nodes withhold all updates due to missing only the latest update

Team Consensus

- No objections; PR to be submitted to formalize the changes

#### 2.2 LightClientOptimisticUpdate Request/ Response Logic Optimization

- Current Spec: Nodes request optimistic updates based on local clock’s current slot
- Proposed Changes

Request Logic: Nodes should request the first missing slot (not just latest) if behind
- Response Logic: Peers should always reply with their latest optimistic update, even if it’s newer than the requested one

Example: If a peer stores only slot 100 but receives a request for slot 99, it should reply with slot 100

Key discussion points

- Some clients (eg. Fluffy, Ultralight) store only the latest optimistic update, so replying with older ones isn’t feasible
- There’s consensus to avoid introducing new content keys to existing data structure unless absolutely necessary to avoid complexity and redundancy

Team Consensus

- General agreement reached; PR to be submitted to formalize the changes

#### 2.3 Config Standardization for Testnets

- Unified Config Approach

Proposed a unified YAML config format combining CL, EL, and Portal-specific fields to simplify setup
- Can support presets or custom paths

Automation & Maintenance

- Generate configs from upstream (CL/EL repo) to minimize manual updates
- Tradeoff between simplified UX vs maintenance overhead

Possible to automate yaml generation to reduce maintenance burden

