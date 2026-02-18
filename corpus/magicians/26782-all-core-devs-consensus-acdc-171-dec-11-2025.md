---
source: magicians
topic_id: 26782
title: All Core Devs - Consensus (ACDC) #171, Dec 11, 2025
author: system
date: "2025-11-30"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-171-dec-11-2025/26782
views: 118
likes: 0
posts_count: 3
---

# All Core Devs - Consensus (ACDC) #171, Dec 11, 2025

### Agenda

- Fusaka

Mainnet
- BPO1
- 2025 upgrade process retrospective

Glamsterdam

- Trustless payments in 7732
- Non-headliner EIP scoping

FOCIL
- 7688
- 8061
- 8080

Heka / Bogotá

- scoping process: EIP-8081: Hegotá Network Upgrade Meta Thread
- portmanteau: Hekotá is leading candidate

**Meeting Time:** Thursday, December 11, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1825)

## Replies

**system** (2025-12-11):

### Meeting Summary:

The team reviewed recent successful events and technical developments across various client implementations, including discussions about performance issues and storage solutions. They evaluated multiple Ethereum Improvement Proposals (EIPs) for upcoming forks, particularly focusing on trustless payments and FOCIL implementation, while debating the timing and process for headliner selection. The conversation ended with decisions about EIP inclusion for Amsterdam and Heka forks, along with discussions about maintaining transparency and credibility in their decision-making process.

**Click to expand detailed summary**

The team discussed recent successful events including mainnet and BPO1, with Barnabas reporting successful blob-spamming tests. James mentioned new releases for Prysm including a hotfix and semi super node feature. Potuz raised concerns about attestation performance degradation on nodes with slower disks, leading to a technical discussion about async storage and custody duties. The team agreed to continue the detailed technical discussion offline, particularly regarding the handling of blocks and columns in async storage scenarios.

The team discussed improvements to Teku clients and the retrospective process for the Fusaka upgrade, with Nixo inviting feedback on an EthMagicians post. They also debated the inclusion of trustless payments in ePBS, with Fredrik proposing to include them and Stokes presenting arguments for keeping them as is, noting potential benefits and minimal disruption to the MEV ecosystem. The team agreed to continue discussions on finding a compromise that supports the status quo of the MEV ecosystem while implementing trustless payments.

The team discussed the EIP process and decision-making, with Alex noting the need for slowing down and supporting each other. They decided to keep the current EIP specifications as is, with some questions remaining about how different components should fit together. Potuz explained potential changes to trustless payments, which could allow builders to deposit faster without being validators, but this would remove their ability to submit bids. The team agreed to further discuss these changes in the next breakout call, aiming for a more forward-compatible solution. They also touched on the FOCIL EIP, considering its inclusion in a future fork, but decided to follow the established process for headliner selection for HECA.

The group discussed the process of including FOCIL, with concerns raised about repeatedly moving goalposts and focusing on technical merits rather than process. Donnoh emphasized the importance of timely inclusion for safety, citing examples like optimistic roll-ups and intent protocols with challenge periods. The conversation touched on economic attacks and the benefits of FOCIL, though Trent noted they were primarily discussing the process rather than specific EIP benefits.

The team discussed whether to include FOCIL in the Glamsterdam fork and debated the timing of the headliner process for the H-star fork. They ultimately decided to proceed with SFI for Glamsterdam today while postponing the headliner decision for H-star until January. The group agreed that FOCIL is a strong candidate for the headliner process, but they should follow the established process rather than making exceptions. There was some concern about the potential impact of FOCIL on other features and the need to balance different priorities. The team emphasized the importance of maintaining credibility and transparency in their decision-making process.

The meeting focused on decisions regarding EIPs (Ethereum Improvement Proposals) for the upcoming fork, particularly for Amsterdam and Heka. The team decided to proceed with DFI (Determine Final Inclusion) for FOCIL in Amsterdam and CFI (Considered for Inclusion) for several EIPs, including 7688, 8061, and 8080, in Heka. They also discussed the process for selecting a headliner feature and the need for further community input on EIPs. Additionally, there was a proposal to change the name of the Heka fork due to concerns about its astronomical accuracy, with a decision to be made at the next ACD (Annual Consensus Discussion) meeting.

### Next Steps:

- Prysm: Complete and publish post-mortem for mainnet issue
- Raúl and Potuz: Continue discussion on disk storage optimization and custody signaling in Discord thread
- Teku : Release improvements related to Fusaka custody and syncing by end of this week or early next week
- Community: Provide feedback on Fusaka retrospective process via EthMagicians post before ACD starts in the new year
- ePBS authors and community: Continue working on design to ensure current MEV ecosystem  can operate with minimal disruption, particularly around staking requirements
- ePBS team: Make trustless payments modifications  the topic of next breakout call
- ePBS team: Assess feasibility and implications of non-validating stakeholder approach by next breakout
- stokes: Update Meta EIP to reflect FOCIL as CFI  for Heka
- All teams: Start Heka headliner selection process in January
- Client teams: Implement 7688  on a branch that can be discarded if needed
- stokes: CFI 7688, 8061, and 8080 for Glamsterdam in Meta EIP
- Francesco and team: Continue tuning parameters for 8061  during R&D process
- Leo: Start second vote for Heka name change and mobilize core devs to participate by next week
- Leo: Bring name change proposal with community support to next ACD
- stokes: Propose portmanteau for Heka/Bogota fork by next ACD
- All: Finalize Heka name and portmanteau by next ACD at the latest

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: v+j7YMdI)
- Download Chat (Passcode: v+j7YMdI)
- Download Audio (Passcode: v+j7YMdI)

---

**system** (2025-12-11):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=LcDW43G82bA

