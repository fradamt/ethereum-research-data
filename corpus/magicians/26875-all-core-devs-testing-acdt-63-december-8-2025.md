---
source: magicians
topic_id: 26875
title: All Core Devs - Testing (ACDT) #63, December 8, 2025
author: system
date: "2025-12-03"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-63-december-8-2025/26875
views: 57
likes: 0
posts_count: 4
---

# All Core Devs - Testing (ACDT) #63, December 8, 2025

### Agenda

#### Fusaka:

- Fusaka fork last Wednesday
- BPO 1 Fork: Epoch 412672, December 9, 2025, 02:21:11pm UTC

#### Glamsterdam:

- bal-devnet-0 updates
- epbs-devnet-0 updates

#### XXM gas topic:

- Updates

**Meeting Time:** Monday, December 08, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1834)

## Replies

**system** (2025-12-08):

### Meeting Summary:

The meeting covered updates on recent technical developments, including the successful completion of the Fusaka Fork and discussions about bug fixes and network stability. The team reviewed data collection efforts for BPO1 and proposed optimizations for dispatching quantums to the network, while also addressing patterns in blob inclusion and column propagation. The conversation ended with updates on testnets, ePBS developments, and testing approaches for new EIPs, with decisions about trustless payments and builder API design to be made at the upcoming ACDC meeting.

**Click to expand detailed summary**

Mario welcomed everyone to ACDT 63 on December 8th, 2025, and highlighted that the recent Fusaka Fork was completed successfully. He encouraged teams to share any significant events or outcomes from the fork, particularly inviting input from the Prysm team. Barnabas was asked to provide details on any meaningful events that occurred during the fork.

The team discussed a late Psmith decision that caused a cascading effect, with a flag fix included in their 7.0.0 release and a promised proper fix expected by the end of the day. Bharath shared that a bug fix for GetPayload V2 in Fushaka, which did not add it to their API routes, was mitigated by fallbacks in CommitBoost and MEV boost, resulting in no impact on network stability. Raúl mentioned an update on mainnet and Fushaka in preparation for BPO1, but the details were not provided in the transcript.

Raúl presented an overview of data collected from the mainnet to prepare for BPO1, focusing on patterns in blob inclusion and column propagation. He highlighted interesting findings, such as the high frequency of blocks with 9 blobs and the rapid propagation of columns once the first copy is seen. Raúl proposed an optimization for dispatching quantums to the network, suggesting a breadth-first policy for sending columns to GossipSub. He also mentioned that this change is already implemented in Go GossipSub and would be easy for the Prysm team to adopt. The team discussed the potential reasons behind the patterns observed in blob counts and column propagation, with Pawan asking about the effectiveness of GetBlobs.

The meeting covered updates on several topics, including the effectiveness of Get blobs, the Fusaka event, and the upcoming BPO Fork. Raúl mentioned the need to correlate data with the presence of blobs in the mempool, and James from Prysm provided an update on their efforts to release a more permanent fix for the Fusaka event, with a technical post-mortem in progress. Mario confirmed that the BPO Fork would occur the following day and encouraged monitoring to ensure a smooth process. The conversation ended with a brief mention of the block-live access list for the next topic of discussion.

The team discussed progress on testnets, with Stefan reporting 13 epochs running with 4 clients and encouraging clients to add debug endpoints. Felipe mentioned ongoing work on gas boundary issues and tests, which will be released early in the week. The team also discussed plans for a devnet, with Stefan setting a benchmark of 24 hours with 3 clients before starting. Mario provided an update on ePBS, including a breakout call discussion on dynamic penalties and trustless payments, with a decision on trustless payments to be made at ACDC on Thursday. The next ePBS breakout call is scheduled for December 19th, after which dev updates will be discussed at ACDC.

The team discussed ePBS (Eth2 Phase 0) and its upcoming changes, focusing on two main topics: trustless payments and builder API design. Bharath presented a design for the Builder API that would support both staked and unstaked builders, though he noted this might simplify some aspects like builder specs and MevBoost. The team agreed to make decisions about trustless payments and builder types at the upcoming ACDC meeting on Thursday, with a final breakout call scheduled for December 19th. The discussion also touched on the need to define PBS metrics across clients during devnet, though this was deemed too early to decide.

The team discussed progress on repricings and gas testing. Kamil reported improvements to stateful scenarios performance on Nethermind and work on a new process for 100-meg block testing. Mario shared updates on a new workflow for generating 100-meg gas test artifacts, which will be available for download on GitHub. Kamil also mentioned ongoing work on a Nethermind plugin for faster block tracing, which is currently being tested on Sepolia.

The team discussed testing approaches for new EIPs and BlockTime access lists. They decided to bundle similar type EIPs together with BlockTime access list tests for faster devnet testing, rather than testing them separately. The testing team will explore this approach, with updates to be provided asynchronously if any issues arise. The group also noted that BlockTime access list testing would be simpler, but no strong preferences were expressed against this method.

### Next Steps:

- Prysm team: Push out a proper fix release for the Fusaka issue, ideally by end of today , or early this week
- Potuz : Write up a technical post-mortem for the Fusaka issue
- Prysm team: Include backfill functionality in the new release
- CL client teams: Add the debug endpoint to update the debug add blocks endpoint to add the generated bug accesses
- All client teams: Run with the EVM fuzzer to find any inconsistencies with block-level access list implementation
- Felipe: Get gas boundary issue tests reviewed, merged, and released early this week
- Stefan: Start devnet 1 once Kurtosis is running for at least 24 hours with at least 3 clients
- All participants: Review arguments from both sides on trustless payments before ACDC this week to make a decision
- All participants: Join ACDC on Thursday to make decision on trustless payments in ePBS
- All participants: Join ePBS breakout call on December 19th
- Kamil : Publish PR link for the Nethermind plugin for tracing historical blocks once testing is complete
- EL client teams: Review and provide feedback on the spec for the new RPC endpoint for testing VU block
- Testing team : Proceed with testing new CFI EIPs together with block-level access list

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: %ioWH66U)
- Download Chat (Passcode: %ioWH66U)
- Download Audio (Passcode: %ioWH66U)

---

**system** (2025-12-08):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=tcANELFmOjU

---

**abcoathup** (2025-12-09):

![image](https://forkcast.org/ethereum-icon.svg)

      [Forkcast](https://forkcast.org/calls/acdt/063/)



    ![image](https://forkcast.org/forkcast-metacard.png)

###



Watch All Core Devs Testing call #063 from 2025-12-08.

