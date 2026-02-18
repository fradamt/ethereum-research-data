---
source: magicians
topic_id: 27004
title: All Core Devs - Execution (ACDE) #226, Dec 18, 2025
author: system
date: "2025-12-08"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-226-dec-18-2025/27004
views: 128
likes: 0
posts_count: 3
---

# All Core Devs - Execution (ACDE) #226, Dec 18, 2025

### Agenda

- Announcements

ACD holiday schedule
- zkEVM roadmap updates doc by @kevaundray

H-star

- FOCIL decision summary
- Heka → Heze name change
- portmanteau decision

Glamsterdam

- repricing update
- scoping decisions

updated CFI / DFI candidate EIPs
- comment regarding EIP-8051 and related EIPs by @rdubois-crypto

Open Questions

Other

- EIP-8077 and EIP-8094 by @cskiraly

**Meeting Time:** Thursday, December 18, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1837)

## Replies

**system** (2025-12-18):

### Meeting Summary:

The meeting covered updates on the holiday schedule for AllCoreDevs calls and discussed the zkEVM roadmap document for 2026 projects. The team made decisions on various Ethereum fork proposals, including the H-star hard-fork and the renaming of the CL side to “Hegota,” and agreed on a timeline for Ethereum fork proposals. They also discussed and approved several EIPs related to gas pricing, compute operations, and code size limits, while deciding to delay decisions on certain proposals until January 5th to allow for further discussion and testing.

**Click to expand detailed summary**

The meeting covered several key updates and decisions. Ansgar announced the holiday schedule for the AllCoreDevs calls, with some changes to start the year with an out-of-schedule ACDE on January 5th to finalize Glam scope decisions. Kev highlighted the zkEVM roadmap document for 2026 projects. The team discussed and approved decisions on FOCIL for the H-star hard-fork and the renaming of the CL side to “Hegota,” pronounced “He-gota.” They also agreed to accept “Hegota” as the official name for the fork, despite its unpronounceable nature. Lastly, Nixo requested and received sign-off on the proposed timeline for the H-star EIP selection process.

The team discussed and agreed on a timeline for Ethereum fork proposals, with January 8-February 4 set for headliner proposal discussions and February 5-26 for headliner finalization. Marius presented repricing proposals targeting 60 megabits per second throughput, with the team agreeing to move several EIPs to “Candidate For Implementation” status including EIP-7904 for general repricings, EIP-7976 for calldata floor gas, and EIP-7981 for access list costs. The team decided to postpone decisions on state growth proposals to January 5th, while EIP-2780 for reducing intrinsic transaction gas was marked as a CFI candidate due to client support.

The team discussed several EIPs and gas-related proposals, with Ben Adams supporting them but highlighting the need for repricing details. Dragan Rakita suggested modifying EIP-2718 to dynamically check for new account creation and proposed integrating this check into the execution phase rather than the intersection pool. The group agreed to make a CFI decision on EIP-2718, while Ben Adams requested a delay in the decision for EIP-8038, which involves increasing state access gas costs. Ansgar proposed gathering client feedback on EIP-8038 before making a final decision.

The team discussed EIP-8038, which addresses state access pricing changes. Ansgar clarified that this EIP is separate from the state growth discussion and proposed including it in the fork for further testing and benchmarking. The group agreed to CFI (Community Funding Initiative) the EIP, with Ameziane from Besu and Guillaume supporting the decision. They acknowledged that the exact pricing numbers are still TBD, but agreed that making the decision now would help move the process forward, rather than delaying it for further benchmarking.

The team discussed and approved several EIPs related to gas pricing and compute operations. They decided to modify EIP 7904 to make certain operations more expensive rather than cheaper, aiming to achieve a target of 60 Ng gas per second. Marius explained that 18 operations would need to be repriced, with some increasing by 3x and others by 10%. The group agreed to CFI these changes, with Ansgar noting that the initial intent of EIP 7904 to increase compute for the same gas limit had evolved to maintaining the same compute except for a few bad cases while increasing the gas limit.

The meeting focused on the deprecation of certain EIPs, particularly CFI, and the decision to delay decisions on state creation, state growth, and pricing until January 5th. Marius provided an update on state benchmarks, explaining that they are running tests on 4x mainnet state and updating infrastructure to compare results across different networks. The group discussed two competing proposals for repricing on memory, ultimately deciding to mark them as DFI candidates due to lack of strong support. They also considered T-Store repricing EIP 7971, which was previously a CFI candidate but was marked as DFI due to production concerns.

The team discussed concerns about EIP 7971 regarding transient storage, with Ben Adams proposing to delay the decision until January 5th to allow more time to resolve outstanding issues. They agreed to remove the hard cap on transient storage access while keeping the storage limit high, with the understanding that the default would be DFI if the issues are not resolved by January 5th. The team also decided to classify EIP 7973 as a DFI candidate due to lack of strong support or opposition, while EIP 8032 on size-based storage gas pricing remained without a recommendation due to its controversial nature.

The meeting focused on discussing two EIPs related to increasing the code size limit in Ethereum. Guillaume presented EIP-2926, which introduces chunk-based code localization, while EIP-7907 was proposed as a simpler alternative. The group debated the merits of each EIP, with Guillaume advocating for 2926 due to its future-proof design and consistent access cost. However, three clients (Bisu, Erigon, and Reth) expressed concerns about the complexity of 2926 and signaled their preference for DFI (Delay For Implementation). Despite Guillaume’s arguments, the group decided to DFI 2926 due to lack of client consensus. The decision on EIP-7907 was delayed until January 5th, along with several other EIPs, to allow for further discussion and testing impact assessments.

### Next Steps:

- nixo: Make blog post announcing the H-star EIP selection timeline
- Repricing teams : Continue benchmarking work on state growth pricing options, including bloating to 4x mainnet state and updating infrastructure to run benchmarks on different state snapshots  by January 5th
- Repricing teams: Update EIP 7904 to reflect reduced scope
- Repricing teams: Finalize numbers for EIP 8038  based on ongoing benchmarks
- Repricing teams: Update EIP 2780 numbers based on AT38 and other repricing decisions
- Ben Adams and community: Resolve account abstraction concerns with EIP 7971  by January 5th, potentially by removing hard limits and keeping only gas-based pricing adjustments
- Guillaume: Publish or share more details on EIP 8032 transition mechanism for review before January 5th decision
- All participants: Review Guillaume’s Twitter thread on EIP 8032 transition before January 5th
- All participants: Make final decisions on state growth pricing options  on January 5th call
- All participants: Make final decision on EIP 7971  on January 5th call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: J$T8jLC1)
- Download Chat (Passcode: J$T8jLC1)
- Download Audio (Passcode: J$T8jLC1)

---

**system** (2025-12-18):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=_KGsKUeH77g

