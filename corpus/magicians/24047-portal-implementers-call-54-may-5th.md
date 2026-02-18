---
source: magicians
topic_id: 24047
title: Portal Implementers Call #54 - May 5th
author: system
date: "2025-05-05"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-54-may-5th/24047
views: 50
likes: 0
posts_count: 2
---

# Portal Implementers Call #54 - May 5th

## Meeting Info

- May 5, 16:30 UTC
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates
- History Network Update
- Devops team running portal on Kurtosis

 **🤖 config**

- Duration in minutes : 30
- Recurring meeting : true
- Call series : Portal Implementers
- Occurrence rate : weekly
- Already a Zoom meeting ID : true # Set to true if this meeting is already on the auto recording Ethereum zoom (will not create a zoom ID if true)
- Already on Ethereum Calendar : true # Set to true if this meeting is already on the Ethereum public calendar (will not create calendar event)
- Need YouTube stream links : false # Set to false if you don’t want YouTube stream links created
- display zoom link in invite : false # Set to true to add the Zoom link to the Google Calendar invite description

[GitHub Issue](https://github.com/ethereum/pm/issues/1524)

## Replies

**Chloe** (2025-05-05):

This week’s notes:

### 1. Team update

- Update on Trin & Glados by Kolby

Bug fixes & improvements

Fixed a bug related to gossiping content to nodes outside their radius
- Replaced hardcoded fork activations with dynamic network config
- Integrated Trin as a library, removing slow HTTP JSON-RPC and redundant tests to improve performance and dev experience

Enabled HistoricalSummaries for the Beacon Bridge
Added Deneb header proof type, generation code, and Deneb header validation
Added Electra types and created header proof using BeaconBlockElectra
In progress

- PR to add HistoricalSummariesWithProof for Electra
- PR to generate e2hs files

Glados：Added internal transfer failure chart

Update on [Fluffy](https://github.com/status-im/nimbus-eth1/tree/master/fluffy) by [Kim](https://github.com/kdeme)

- Bug fixes & improvements

Improved eth_createAccessList to return access lists even when the EVM execution reverts
- Ensured only a single instance of AsyncEvm created and shared across API handlers
- Added architecture docs to the Fluffy guide

Tested & activiated block proof tests
Implemented & tested the adjustment of historical_summaries proof for Electra

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- Continued implementing discv5 and awaiting upstream changes from Besu in the discv5 library
- Continued implementing history endpoints, eg. historyTraceGetContent, historyRecursiveFindNodes
- Nearly done with accumulator integration
- Working toward release a Samba lib to be integrated into Besu client
- Commit to complete the History network checklist soon

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [acolytec3](https://github.com/acolytec3)

- Focused on implementing ephemeral headers, with progress on validation and purging old offers
- Will work on historical summaries updates after current ephemeral headers implementation

Update on [Shisui](https://github.com/zen-eth/shisui) by [Grapebaba](https://github.com/GrapeBaBa)

- Converted ExecutionBlockProof from list to vectors
- Added recursiveFindNodes in putContent logic
- Fixed bug in ping extension upgrades
- Working on ephemeral headers implementation

### 2. Discussion topics

#### 2.1 History Network Update

- Most client teams progressing well on implementation; No major blockers
- Link of History Network meta tracking issue: History Network Fully Operational Meta Tracking Issue · Issue #398 · ethereum/portal-network-specs · GitHub

#### 2.2 Running Portal in Kurtosis

- Goal

Enable Portal Network clients to run inside Kurtosis, for better devnet/ testnet support and integration testing

Initial target

- Run local, small-scale devnets to experiment with setup, discover limitations, and determine necessary client-side changes

Topics discussed

- Networking design consideration

Need for large super-nodes vs many small nodes in testing
- Use of ephemeral devnets with isolated protocol IDs to avoid collisions
- Flagged potential issues with ephemeral headers as client teams are still finalizing their implementation

Bridgework: Need mechanisms to insert historical data into the devnets for testing purposes
Protocol ID/ Chain ID: Discussed potentially using chain IDs for Kurtosis devnets, and how to map them to protocol IDs in Portal clients
Config consideration

- Reuse existing EL/CL configs
- Add Portal-specific settings via standardized spec file (shared across clients) and optional client-specific extensions

Collaboration

- Kolby (Trin) - Will act as the point of contact from Portal devs
- Kim (Fluffy) - Expressed interest to support Fluffy within Kurtosis
- Barnabas (ethPandaOps) - Will provide Kurtosis integration support
- Other teams/ clients are welcome and encouraged to contribute

Action items

- Coordinate PRs and communication in ethpandaops repo
- Create a tracking issue for Kurtosis integration blockers and client-side requirements to support Kurtosis devnet
- Explore minimal devnet setups for initial testing

