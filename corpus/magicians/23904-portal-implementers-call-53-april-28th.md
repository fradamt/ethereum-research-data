---
source: magicians
topic_id: 23904
title: Portal Implementers Call #53 - April 28th
author: system
date: "2025-04-28"
category: Protocol Calls & happenings
tags: [portal]
url: https://ethereum-magicians.org/t/portal-implementers-call-53-april-28th/23904
views: 35
likes: 1
posts_count: 2
---

# Portal Implementers Call #53 - April 28th

## Meeting Info

- Apr 28, 16:30 UTC
- Duration: 30 minutes
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates

[GitHub Issue](https://github.com/ethereum/pm/issues/1508)

## Replies

**Chloe** (2025-04-28):

This week’s call notes:

### 1. Team update

- Update on Trin & Glados by Mike

Added AcceptCodes to census and bridge metrics for better tracking
- Beacon network is now required when History network is enabled
- Simplified header proof generation code to avoid duplication
- Changed ExecutionBlockProof from list to vector
- PR to enable HistoricalSummaries bridge and prepare for future testnet support
- Glados

Fixed a broken spec link
- Added protocol version support by client graph

Update on [Fluffy](https://github.com/status-im/nimbus-eth1/tree/master/fluffy) by [Kim](https://github.com/kdeme)

- Added protocol versioning support
- Implemented ephemeral header encoding/ decoding (disabled for now until database update work is complete)
- Implemented offer cache to hold content IDs of recent offers
- Added metrics to count offer accept codes (Grafana dashboard will be updated accordingly)
- Adjusted tests to support HeaderWithProof using SSZ vectors for Capella & Deneb

Adjust tests for supporting HeaderWithProof updated version with SSZ vector instead of list
- Adjusted generation of test vectors and enabled validation accordingly
- Updated portal-spec-tests test vectors

Revisited the PR of adding the HistoricalSummariesWithProof endpoint in Nimbus consensus client (expected to be merged soon)
PR to add HistoricalSummariesWithProof for Electra

Update on [Shisui](https://github.com/zen-eth/shisui) by [Qi Zhou](https://github.com/qizhou)

- Added ephemeral types support and test vectors
- Improved performance with multi-threading validation, reducing rejection rates from ~66% to

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- Continued internal adjustements to integrate Samba with Besu
- Working on completing all discv5 endpoints in the implementation
- Working towards deploying a Besu-Samba integrated instance
- Plan to differentiate client version string for tracking Besu-Samba integrated version and Samba standalone version

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [acolytec3](https://github.com/acolytec3)

- Merged discv5 fixes into ChainSafe implementation (not yet deployed to boot nodes)
- DevOps continued improving boot node stability through VM placement updates
- Plan to update History network container for Deneb headers
- Start to review ephemeral header gossip logic, and prepare to active the already-implemented basic types

### 2. Discussion topics

#### 2.1 History Network Deployment & Monitoring

- Goal

Finalize History network deployment to unblock State network development
- Primary focus is to get the ephemeral head fully live and deployed

Action items

- Create a meta-issue (led by Kolby) to track remaining tasks across client teams
- Glados monitoring

Separate infra needed for tracking ephemeral head data
- Minimal Beacon network monitoring to verify gossip availability

Next step

- Client teams to  contribute status updates via the meta-issue

#### 2.2 Pectra Upgrade & Testnet Integration

- Pectra Fork Readiness

Most Pectra-related updates are client-specific
- No major cross-team sync needed now
- Hive tests can be updated after the Pectra fork ships

Future Fork Testnet Integration

- Integrate Portal into testnets before future forks to avoid post-fork delays
- Prioritize Sepolia as the primary testnet for Portal-related work, as it contains pre-merge data

