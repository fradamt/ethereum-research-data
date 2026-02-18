---
source: magicians
topic_id: 24150
title: Portal Implementers Call #56 - May 19th
author: system
date: "2025-05-12"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/portal-implementers-call-56-may-19th/24150
views: 149
likes: 0
posts_count: 2
---

# Portal Implementers Call #56 - May 19th

## Meeting Info

- May 19, 2025, 16:30 UTC
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

[GitHub Issue](https://github.com/ethereum/pm/issues/1539)

## Replies

**Chloe** (2025-05-19):

This week’s notes:

### 1. Team update

- Update by Piper

Preparing a co-authored document with Jason that outlines Portal’s role in the L1 scaling roadmap
- Inviting teams to review and provide feedback prior to the public release

Update on [Trin](https://github.com/ethereum/trin) & [Glados](https://github.com/ethereum/glados) by [Michael](https://github.com/mrferris)

- Internal refactoring
- Added new docker image for trin-execution
- Moved consensus-related constants into ethportal-api
- Added trace offer endpoint which support multiple content keys
- Deployed e2hs bridges for data bridging
- Glados: UTP transfer failures are now visible, aiding network health tracking

Update on [Ultralight](https://github.com/ethereumjs/ultralight/tree/master) by [ScottyPoi](https://github.com/ScottyPoi)

- Boot nodes redeployed with some issues to be fixed
- Merged updated SSZ container for HistoricalSummariesStateProof, resolving Hive test failures

Update on [Nimbus Portal Client](https://github.com/status-im/nimbus-eth1/tree/master/portal) (formerly Fluffy) by [Kim](https://github.com/kdeme)

- Added access from History network to historical summaries
- Updated state bridge for more efficient gossiping
- Fixed a bug in FindContent responses
- Working on rate-limiting to better monitor gossip success rates
- Renaming from “Fluffy” to “Nimbus Portal Client” underway across code and infrastructure

Dual support (“f” as Fluffy and “n” as Nimbus Portal) for transition phase in ENRs

Update on [Shisui](https://github.com/zen-eth/shisui) by [Qi Zhou](https://github.com/qizhou)

- Performance improvements via refactoring discv5 to pipeline the reloop and dispatch loop asynchronously
- Fixed memory leak issues and block boundary check error
- Refactored validation logic to reduce redundancy
- Implemented support for retrieving ephemeral header from storage (code currently under review)

Update on [Samba](https://github.com/meldsun0/samba) by [Derek](https://github.com/Dsorken)

- Implemented the protocol versioning incl. accept codes and utp size prefix
- Fixed an issue in history offer logic with large transfers
- Integration with Besu

Improved logs and added parameter options for running Samba inside Besu
- Made all Portal History JSON-RPC calls available as method calls for Java projects
- Basic Besu node now operational with Samba integration

Plan to implement the beaconStore endpoint and Capella validation this week

### 2. Discussion topics

#### 2.1 Beacon Spec Update

- PR was submitted based on last week’s discussion
- Open for team review before merging

#### 2.2 Ephemeral Header Gossiping Mechanism Discussion

- The problem: Current doc suggests neighborhood gossip for ephemeral headers, but this may

Restrict propagation to nodes near the content ID
- Risk incomplete network coverage

Team consensus: Random gossip preferred over neighborhood gossip

- Neighborhood gossip filters peers based on radius related to content ID, which is irrelevant for ephemeral headers
- Random gossip can be adjusted to prioritize peers closer to the sender, but should spread widely to ensure all nodes receive the headers

Action item

- Submit PR to update the spec to clarify random gossip as the mechanism for ephemeral headers

