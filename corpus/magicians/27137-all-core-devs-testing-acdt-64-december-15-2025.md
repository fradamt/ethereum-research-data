---
source: magicians
topic_id: 27137
title: All Core Devs - Testing (ACDT) #64, December 15, 2025
author: system
date: "2025-12-12"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-64-december-15-2025/27137
views: 69
likes: 0
posts_count: 3
---

# All Core Devs - Testing (ACDT) #64, December 15, 2025

### Agenda

Fusaka:

- mainnet BPO 1 success

Glamsterdam:

- bal-devnet-0/1 updates
- epbs-devnet-0 update

XXM gas topic:

- Wen 80M gas?

BPO3 preparations:

Partial responses interop:

- prysm branch
- lighthouse branch
- geth open pr
- nethermind open pr
- others?

Max blobs flag:

- nethermind
- reth
- others ?

H* discussion topics:

- Rename Heka → Heze (see eth magician discussion
- Decide on final name by next ACD?

Holiday schedule:

- No ACDT during holidays
- Last ACDT today/22nd of Dec - do we need another call?
- ACDE instead of ACDT on 5th of Jan @adietrichs
- Next ACDT 12th of Jan

**Meeting Time:** Monday, December 15, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1842)

## Replies

**system** (2025-12-15):

### Meeting Summary:

The team reviewed the successful launch of BPO 1 and planned for BPO 2’s launch while discussing various technical proposals including new validator types and proposer preferences. They examined the Prysm post-mortem report on the Fusaka mainnet incident and reviewed progress on execution-spec-tests release 2.0, which included changes to storage keys and values. The team also discussed bootstrapping options for builders at the fork boundary, gas limit adjustments for BPOs, and implementation of GetBlobs V3, while Tullio presented on RPC testing efforts at Erigon and the group agreed to finalize the H-star naming convention decision.

**Click to expand detailed summary**

The team discussed the successful launch of BPO 1 on Fusaka and planned for BPO 2’s launch on January 7th. Barnabas and Justin agreed to discuss a new validator type and proposer preferences gossip topic. The team reviewed the Prysm post-mortem report on the Fusaka mainnet incident. Stefan was asked to provide updates on DevNet 1 or DevNet Zero, but the transcript ended before he could respond.

The team discussed progress on the execution-spec-tests release 2.0, which includes changes to use Uint 256 for storage keys and values. Clients were encouraged to test against the zero branch and switch to the Valid one branch. Felipe mentioned adding gas boundary tests for call-off codes. Karim reported on business features, including state root conclusion and parallelization with Blobact. Marc and Dragana discussed progress on parallel transaction execution and state root computation. Milen updated on Erigon’s progress with the Valid branch and Hive tests. Justin presented proposals for ePBS, including changes to builders and withdrawal structures, and sought feedback from the client teams.

The team discussed bootstrapping options for builders at the fork boundary, with Justin explaining two potential approaches: converting existing validators or requiring builders to wait one epoch before submitting bids. Barnabas emphasized the need for a final decision before the upcoming breakout meeting, noting that Lighthouse requires more time for review. Enrico raised concerns about normal validators being cut off from validating if they want to submit bids, which Justin confirmed would be the case. The team also discussed a new Gossip topic proposal for conveying fee recipient, gas limit, and trusted payments preferences to builders.

The team discussed the placement of a trusted payment field in the gossip topic, with Bharath suggesting it might be more appropriate in validator registrations due to the need for per-builder preferences. Justin mentioned he had added a boolean field for trusted payments but received feedback to remove it, as proposers don’t have to adhere to these preferences. Bharath provided an update on working with builder specs, particularly for staked and unstaked builders, and mentioned he would review Justin’s PR for potential impacts. Justin requested reviews for two PRs related to process_withdrawals and get_expected_withdrawals.

The team discussed gas limit adjustments for BPOs, with Barnabas noting that BPO2 would require additional work on the CL side for MaxPobs and partial responses. Kamil reported improvements in test generation and Nethermind’s work on StateB, while Raúl requested a concrete definition for the gas limit to focus analysis. The team agreed to change defaults for the next BPO, and Ameziane inquired about handling the next gas limit increase before Glamsterdam. Kamil also mentioned ongoing work on opcode tests and precompile analysis, with the goal of suggesting better numbers by the end of December.

The team discussed the implementation of GetBlobs V3 and the need for ELs to push out branches supporting the change, with Nethermind’s PR expected the next day. Raúl emphasized the importance of ELs including this change in their next releases to facilitate better integration in DevNets, and mentioned that some open points in the spec would be resolved by the end of the week. Barnabas proposed including the Max blobs flag in the next releases of every EL to limit local blob-builders and prevent orphan blocks, noting that Nethermind and RISC had already implemented it. Ben raised a related topic about gas limit interpretation in shorter slots, suggesting that client-side values might resolve the ambiguity, though Barnabas proposed discussing this further in the new year.

Tullio presented on RPC testing efforts at Erigon, highlighting their development of an RPC integration testing suite that complements the existing IVRPC compat test suite. The discussion included plans to present this work at the upcoming RPC standardization call on Monday at 3pm UTC. The team also discussed the H-star naming convention, with Barnabas reporting that “Heze” had received more votes than the original name, and the group agreed to finalize this decision on Thursday’s call. The conversation ended with the announcement of an updated holiday schedule for AllCoreDevs testing calls, with several calls being cancelled during the holiday period and the next regular meeting scheduled for January 12th.

### Next Steps:

- All EL client teams: Test against execution-specs release 2.0 and switch to Valid one branch
- All EL client teams: Review and investigate the out-of-gas self-destruct test failures
- All EL client teams: Run Kurtosis test with EVM first and leave it running for a while to ensure interop works well
- All client teams: Review Justin’s builder change PR  and provide feedback by Friday’s breakout call
- Lighthouse team: Review the builder change proposal before the breakout call
- Justin Traglia: Make final decision on builder change by this week’s breakout call
- Bharath: Review Justin’s PR 4788  and make changes if needed, raise questions if not happy
- Bharath: Continue working on builder specs for staked and unstaked builders
- Justin Traglia and Bharath: Discuss proposer preferences gossip topic offline regarding per-builder preferences
- Kamil : Complete test generation improvements and retest everything this week with latest stack
- Kamil and Maria’s team: Gather data for precompile tests and suggest better repricing numbers by end of December
- All EL teams: Implement and include GetBlobs V3 support in next releases
- All CL teams: Implement partial responses support for BPO 3
- All EL teams: Implement the Max blobs flag in next releases within the next month or two
- Raul: Send link to networking spec working group and add interested participants
- Tullio: Present RPC testing suite at the RPC standardization call next Monday at 3pm UTC
- Tullio: Contact Chase  on Discord to collaborate on RPC documentation
- All participants: Provide feedback on Heze/Hizi star name pronunciation and finalization by Thursday call
- Barnabas: Post holiday schedule in chat and cancel ACDT call for December 22nd

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: .7%47DP2)
- Download Chat (Passcode: .7%47DP2)
- Download Audio (Passcode: .7%47DP2)

---

**system** (2025-12-15):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=JbHnZnkl2Mc

