---
source: magicians
topic_id: 25950
title: All Core Devs - Execution (ACDE) #224, November 6, 2025
author: system
date: "2025-10-24"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-224-november-6-2025/25950
views: 136
likes: 1
posts_count: 4
---

# All Core Devs - Execution (ACDE) #224, November 6, 2025

### Agenda

- Fusaka

reminder: please add the relevant coordinators from your client team to this doc for the Fusaka upgrade
- testnet updates
- mainnet rollout

Glamsterdam

- H* naming
- process update, see comment by @ralexstokes

FOCIL discussions on ACDC
- STEEL testing complexity assessment prioritization

brief summary of initial client positions

- Nethermind
- Geth
- Erigon
- Reth (updated)
- Nimbus (Pureth)

repricing breakout results

- case for repricings by @casparschwa and @adietrichs
- bundle options by @misilva73
- recommendations by @mariusvanderwijden

DFI / CFI candidate selections

[WELDing the STEEL](https://github.com/ethereum/pm/issues/1781#issuecomment-3465992763)

**Meeting Time:** Thursday, November 06, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1781)

## Replies

**abcoathup** (2025-10-27):

### Summary

*[link to [@adietrichs](/u/adietrichs) summary]*

### Recordings/Stream

- https://forkcast.org/calls/acde/224
- Live stream on X: [x.com/ECHInstitute]

### Writeups

- ACDE #224: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDE #224 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade (December 3):

EF mainnet announcement: mainnet December 3, BPO1 December 9, BPO2 January 7 2026
- Testnet upgrades;  Holešky Oct 1,  Sepolia Oct 14,   Hoodi Oct 28;
- Current devnet: fusaka-devnet-3 [specs]
- mainnet upgrade & incident response team plan
- For retrospective: week or two needed between testnet upgrade & mainnet releases to fix any bugs

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam) (2026):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners scoping discussions:

Proposed for Inclusion EIPs
- ACDE 2025-11-06 - Google Präsentationen
- Team perspectives: Erigon, Geth, Nethermind,  Nimbus/Pureth, Reth
- STEEL: testing complexity assessments for EIPs
- Repricing:

Caspar & @adietrichs Case for repricing
- @misilva73 repricing bundle options
- @MariusVanDerWijden’s repricing recommendations
- @CarlBeek’s repricing EIP tracker

[Mascot needed for Glamsterdam upgrade](https://ethereum-magicians.org/t/mascot-needed-for-glamsterdam-upgrade/26008)

Heka + Bogotá

- Suggest a portmanteau for Heka + Bogotá

https://steel.ethereum.foundation/blog/blog_posts/2025-11-04_weld_final/

---

**system** (2025-11-06):

### Meeting Summary:

The meeting covered the status and timeline of the Fusaka upgrade, including BPO activation and ongoing investigation of reported issues. The team conducted a comprehensive review of 40 EIPs for the Glamsterdam fork, discussing client positions and potential bundling approaches while focusing on temperature checks rather than immediate decisions. The conversation ended with plans to continue EIP discussions at the next All Core Developers’ Meeting in two weeks, with emphasis on making individual EIP decisions rather than addressing them during DevConnect.

**Click to expand detailed summary**

The meeting focused on two main topics: the Fusaka upgrade and the initial scoping discussion for the Glamsterdam fork. For Fusaka, the team confirmed that BPO1 was activated on Hoodi, with BPO2 scheduled for the following week. While there were no major bugs reported during the fork transition, some issues were discovered later, with Nethermind and Prism teams investigating. The team agreed to proceed with the current timeline for the Fusaka rollout. Regarding Glamsterdam, Ansgar proposed a process for reviewing the 40 EIPs, focusing on temperature checks rather than making decisions today. The team discussed client positions on various EIPs, with Geth, Erigon, and Nimbus sharing their stances. The core repricing effort was highlighted as a potential bundle for consideration, though its exact scope remains in flux. The conversation ended with a reminder that final decisions on EIPs would not be made today, but rather used to guide discussions in two weeks.

The team discussed repricing EIPs and their potential impact on Ethereum’s scalability. They debated whether to bundle multiple EIPs together or address them separately, with concerns raised about the complexity of testing and the potential for unintended consequences. The group agreed to have a separate conversation about state growth approaches. They also reviewed individual EIPs, with some clients expressing preferences for certain proposals. The team decided to further discuss adjustments to EIP 8032 offline, as it could help with both state growth and access costs.

The team discussed several EIPs related to Ethereum improvements, focusing on memory costing and EVM changes. They agreed to oppose EIP-47923 and EIP-8057 due to complexity concerns, while supporting EIP-8024 and EIP-7843. The group also considered the implementation of various EVM improvements, with some clients already having implemented EIP-7610. They decided to postpone further discussion on EIP-7979 and EIP-7791, with Felix expressing concerns about the latter’s potential unforeseen consequences. The team agreed to bundle EIP-7843 with slot length changes if motivated use cases could be provided.

The meeting focused on reviewing and discussing various Ethereum Improvement Proposals (EIPs) related to testing, Peer ETH, and contract deployment. The team agreed to move forward with EIP 8024, which was supported by client teams and deemed straightforward to test. They decided to exclude EIP 7610 from further discussion as it had already been implemented. The group also discussed the potential inclusion of certain SSZ-related EIPs in the DFI candidate list, with Dustin suggesting a subset scope approach for Peer ETH implementation. The conversation ended with a brief mention of contract deployment-related EIPs, including removing the init code size limit and deterministic factory pre-deploy.

The meeting focused on reviewing and discussing various EIPs (Ethereum Improvement Proposals) for potential inclusion in the Glamsterdam fork. Key topics included contract size increases, cryptography-related precompiles, and transaction/block features. Clients expressed concerns about the redundancy of certain EIPs, particularly 7907 in relation to 2926, and the timing of implementing post-quantum cryptographic features. The group agreed to take some discussions offline, including the strategy for handling contract size increases and the merits of FOCIL (Friendly OpenCensus for Internet Lighting). It was decided that the next ACDE (All Core Developers’ Meeting) in two weeks would focus on making individual decisions about EIPs, rather than having a full discussion during the upcoming DevConnect event.

### Next Steps:

- Barnabas: Publish blog post for Fusaka mainnet releases today with TBD for Nethermind and Prism versions
- Nethermind team: Continue investigating the main bug discovered related to Fusaka and re-org
- Prism: Release mainnet version by Monday
- All client teams: Add relevant coordinators from your client team to the Fusaka upgrade doc
- Besu: Publish their stance on EIPs by next week
- Ansgar: Synthesize all comments from the call and create CFI candidate list and DFI candidate list before the next call in two weeks
- Champions of DFI candidate EIPs: Try to convince people asynchronously over the next two weeks why their EIP is important
- Charles : Address compatibility concerns with account abstraction approaches offline
- Marius: Request that Charles and AA teams provide more information about transient storage hard limits  and its interference with AA before next call
- Guillaume and others: Take contract size strategy discussion offline
- Zsolt: Present clean implementation and material for Trustless Log Index  in coming weeks
- All participants: Voice any strong objections to continuing the scoping discussion in two weeks  on Discord
- FOCIL discussion participants: Join ACDC calls for FOCIL discussions and decisions
- All participants: Review the STEL team blog post on welding execution spec test code into execution specs
- Testing developers: Review changes in the STEL weld blog post and reach out with questions

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: E78A#nF+)
- Download Chat (Passcode: E78A#nF+)

---

**system** (2025-11-06):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=QWkAtpeIa4o

