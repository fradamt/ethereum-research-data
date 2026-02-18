---
source: magicians
topic_id: 23358
title: Portal Implementers Call #50 - April 7th
author: system
date: "2025-04-02"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-50-april-7th/23358
views: 101
likes: 1
posts_count: 2
---

# Portal Implementers Call #50 - April 7th

## Meeting Info

- Apr 7, 16:30 UTC
- Duration: 30 minutes
- Meet link: shared in EthR&D#portal-dev
- Recap: Portal Network Implementers Call Notes - HackMD (updated after each call)

## Agenda

- Team updates

[GitHub Issue](https://github.com/ethereum/pm/issues/1424)

## Replies

**Chloe** (2025-04-08):

This week’s call notes:

### 1. Team update

- Update by Piper

Working on history expiry coordination & organization
- In early onboarding phase for history state spec

Update on [Trin](https://github.com/ethereum/trin) & [Glados](https://github.com/ethereum/glados) by [Kolby](https://github.com/KolbyML)

- e2hs update

Fixed an invalid BlockIndex type in e2hs
- Pre-merge e2hs files generated & uploaded, except some minor bugs
- Once fixed, e2hs file will replace era1, with plan to sync up to the chain head minus ~27h

Fixed a bug where the discv5 ENR cache was to small to handle 500+ or more active peers by scaling the cache size to match the max number of sessions

- A cleaner upstream fix coming soon via the discv5 lib

Glados

- Updated Glados to support ethportal-api 0.6.0 which incl. ping extension
- Fixing the census issue, which now works even without online nodes

Update on [Fluffy](https://github.com/status-im/nimbus-eth1/tree/master/fluffy) by [Kim](https://github.com/kdeme)

- Updated ping endpoint to support ping extension
- Worked on async EVM improvement and investigating segfault/ bugs in CI tests
- Protocol versioning

Progressing on protocol versioning, but blocked by an unexpected compiler bug
- Need to update discv5 for protocol versioning to properly handle ENR access during request/ response

Plan to store ENR in session cache for reliable access

Implemented the changes of accept codes and add varient size prefix

- Investigating a clean solution to manage versioning info along with the encoding/ decoding process

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [ScottyPoi](https://github.com/ScottyPoi)

- Working on protocol versioning, added initial support but v1 features not yet active

Current priority: Finish the v1 changes implementation

Progressed on history expiry support within EthereumJS team
Plan to revamp boot node setup, shifting from 2 overloaded VMs to multiple smaller VMs, for better performance and reliability
Merged a Tauri-based web interface project built on Ultralight by Justin, currently allowing basic RPC lookups

Update on [Samba](https://github.com/meldsun0/samba) by [Meld](https://github.com/meldsun0)

- Implemented SSZ union removal
- Fixed a bug in the putContent JSON-RPC endpoint, which is related to the utp lib usage
- Passed local Hive tests against Trin, still debugging remaining test failures
- Plan to begin regular biweekly sync with Besu team for planning and coordination

Update on [Shisui](https://github.com/zen-eth/shisui) by [Grapebaba](https://github.com/GrapeBaBa)

- Merged PRs, incl. implementation on accept codes and protocol versioning
- Implemented add size prefix in FindContent
- Fixed the FindNodes response bug, due to packet too long
- Added rate limiting policy, where gossips are dropped when resource usage exceeds the limit
- Fixed discv5 whoareyou response issue in Geth, through in Hive tests still see issues when communicating with Fluffy nodes

The issue with Fluffy nodes

When two portal requests are sent simultaneously before a session is established, only the 1st succeeds and the 2nd fails
- eg. Fluffy’s background Ping (for node revalidation) races with test-triggered FindContent, would cause one to fail

Potential solution

- Queuing on Fluffy side: Queue the concurrent requests until the session is setup
- Retry logic: Clients could retry dropped requests automatically
- Test adjustment: Modify Hive test to better reflect real-world behavior

Ultralight related notes

- Identified 3+ encoding-related bugs when previously debugging Hive test failures related to discv5
- Not sure if these fixes would resolve the concurrent-request problem

### 2. Discussion topics

#### 2.1 Next step for Bridges

- Curent status

Bridges are mainly run by the Trin team currently

Technical updates

- Transition to generate e2hs file (much simplified without the accumulator) to replace era1 file for the entire range
- Plan to maintain two bridge types: ephemeral bridge (handle reorgs & complex edge cases) and e2hs bridge
- Dropping support for the older era1 bridge

Next step proposal

- Community-runned bridges

Consensus: Shift from team-operated to community-operated bridges
- Next steps: Document clear setup steps for external parties to get involved easily

#### 2.2 Hive test

- Achieved improved test coverage this week, with additional Portal Hive test now passing successfully
- Strong cross-team collaboration as client teams worked together on troubleshooting and debugging

#### 2.3 Team presence at Interop event

- Some members from Portal team will attend the event in Berlin in June

