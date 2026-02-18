---
source: magicians
topic_id: 23324
title: Portal Implementers Call #49 - March 31st
author: system
date: "2025-03-31"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-49-march-31st/23324
views: 37
likes: 0
posts_count: 2
---

# Portal Implementers Call #49 - March 31st

## Meeting Info

- Mar 31, 16:30 UTC
- Duration: 30 minutes
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates
- Updates to the Ephemeral Headers specification

[GitHub Issue](https://github.com/ethereum/pm/issues/1406)

## Replies

**Chloe** (2025-03-31):

This week’s call notes:

### 1. Team update

- Update on Trin & Glados by Kolby

Formalize the new e2hs file format to handle all EL blocks, which simplifies bridging process
- Implemented e2hs, incl. adding reader & writer in e2store crate
- Published e2store crates available for external projects to use
- Fixed a utp packet handling bug, where 1st part of transfer is ignored by recipient if the STATE response to SYN is dropped
- Cleaned up redundant test vectors
- Glados: Now display header by numbers on the latest block status graph

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [ScottyPoi](https://github.com/ScottyPoi)

- Added protocol versioning to ENRs and preparing for the PR on accept/decline code change
- Updating EthereumJS to support EIP-4444 and drop day by integrating Ultralight as a dependency
- Progressed on ephemeral headers implementation

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- Implemented new endpoints but facing delays with UTP library (putContent issue) and accumulator integration
- Restructuring code for better modularity to integrate with Besu client

Need further exploration on the primary use case of Samba by the Besu client (eg. JSON-RPC serviing vs full block sync)

Update on [Shisui](https://github.com/zen-eth/shisui) by [Qi Zhou](https://github.com/qizhou)

- Added support for protocol versioning and decline/ accept code implementation
- Fixed race condition bug, and merged ping extension PR
- Investigating the whoareyou challenge response issue and performance bottlenecks in Go implementation

### 2. Discussion topics

#### 2.1 Protocol Versioning Implementation

- Most of the client teams have started implementing the protocol versioning
- Teams are encouraged to implement miniimal versioning to enable incremental updates and compatibility testing

#### 2.2 Ephemeral Headers Spec Update

- The problem

The initial assumption that all EL headers could be sourced from LightClientUpdates was invalidated as the CL derives tx/ withdrawal data via SSZ instead of RLP/ MPT

The spec is being updated to

- Clarify limitation: EL headers can’t be fully sourced from the Beacon Network
- Define handling

Headers should be organized chronologically in payloads
- Clients should retain headers during reorgs until chain validity is re-verified
- Avoid unnecessary network requests that could case DDOS issue
- Allow headers to propagate naturally across the network

Edge cases: Notes added for scenarios like reorgs and data propagation

Next step

- Team working on the implementation is encouraged to read the PR link for details

Relevant github issue/ PR

- https://github.com/ethereum/portal-network-specs/pull/387

#### 2.3 Shisui & Ultralight Connectivity Issue

- The problem

Milos obversed intermittent failures when sending Find_Nodes request to Shisui and Ultralight nodes

Pattern of failure

- Find_Nodes requests fail at non-zero distance
- Requests with zero distance or simple ping work fine
- The issue isn’t consistently reproducible but happens frequently

Investigation

- Initial debugging attempts suggest the session or message keys might be incorrect
- Equivalent Hive tests are passing, ruling out protocol-level bugs
- Shisui identified a potential race condition in node assignment logic and a fix has been proposed & under review

Next step

- Team agree to collaborate via a live debug session, with Shisui deploying a test node for targeted troubleshooting

Relevant link

- Discord

#### 2.4 EIP-4444 Coordination Updates

- Sepolia testnet: The initial May 1st drop date is now Sepolia testnet drop date, with efforts underway to align an EL client version ready for Sepolia so CL clients can test against
- Mainnet drop date: The mainnet drop date is postponed to sync with Pectra upgrade, due to CL’s dependency on pre-merge logs

#### 2.5 State Network Progress

- State network rollout has stalled due to

Gossip performance issue: Bottlenecks in propagating new state data across the network
- Dependencies: Protocol versioning, accept codes must be finalized first to unblock state sync features

Action plan

- Short-term goal: Focus on shipping a client version that can sync state even if it’s slighly behind the head of the chain
- Priority:

History network will take precedence over the State network due to higher urgency
- Ephemeral state work and performance optimizations may follow later, depending on team availability

Team bandwidth constraints

- There will be reduced manpower on Trin side during summer due to vacation/ parental leave
- Potentially exploring collaboration with Fluffy team on the State network development

#### 2.6 Hive test status

- Two key failures remain unsolved

JSON-RPC extension: Some clients still need to expose required extensions via JSON-RPC
- Post-merge proof validation: Minor bug persist in validating post-merge proof formats

Next step

- Teams are urged to prioritize these fixes within the next two weeks to get Hive tests fully green, as prolonged failures risk being overlooked

