---
source: magicians
topic_id: 25145
title: EIP-7928 Breakout #1, August 27, 2025
author: system
date: "2025-08-18"
category: Protocol Calls & happenings
tags: [breakout, bal]
url: https://ethereum-magicians.org/t/eip-7928-breakout-1-august-27-2025/25145
views: 68
likes: 1
posts_count: 5
---

# EIP-7928 Breakout #1, August 27, 2025

### Agenda

## Block-Level Access List (EIP-7928) Breakout

**Date/Time:** [Wednesday, Aug 27, 2025 – 14:00 UTC](https://www.timeanddate.com/worldclock/fixedtime.html?iso=20250827T1400)

**Location:** Zoom, livestreamed on YouTube

**Agenda:**

- Recap of Block-Level Access List (BAL) design
- Inclusion of read-only accesses (SLOAD, BALANCE, STATICCALL)
- Encoding format decision: RLP vs SSZ
- Indexing rules for pre- vs post-execution changes
- Implementation/testing plan for initial devnet
- Implementation details and initial results by Jared (Geth)
- EELS and EEST Progress by Toni and Rahul
- Initial benchmarks by @dajuguan

**Goal:**

Finalize spec details and testing roadmap for EIP-7928

Zoom link will be posted on ACD before the breakout.

**Meeting Time:** Wednesday, August 27, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1691)

## Replies

**system** (2025-08-27):

### Meeting Summary:

The team discussed streaming arrangements for an upcoming meeting and confirmed they would stream on both X and YouTube platforms. The main focus was on the implementation progress of EIPs, particularly the Geth implementation where Jared presented benchmark results and discussed performance improvements in state processing. The team also reviewed testing efforts, client progress on implementing the BAL EIP, and agreed to maintain the current implementation while continuing to evaluate performance and benchmark results for future devnet deployment.

**Click to expand detailed summary**

Toni and Pooja discussed streaming arrangements for an upcoming meeting, agreeing to stream on both X and YouTube platforms. Pooja confirmed she would be ready to stream in about 2 minutes, and Toni decided to wait a few more minutes before starting the stream. Once ready, Toni gave the signal to Pooja, who confirmed they were live. The meeting then began with Toni welcoming everyone to the 1st EOP 7, 9, 28 Breakout call.

The team discussed the implementation progress of EIPs, focusing on the Geth implementation where Jared reported that block access list execution and building are complete, though storage and account reads are still pending. Jared presented benchmark results and mentioned that the code is ready for a devnet, pending verification of consensus and engine API changes. Toni noted that the inclusion of reads is still under discussion, with parallel I/O being considered valuable for larger blocks.

Jared presented an overview of the current serial and parallel transaction execution models, highlighting the performance differences between the master and bal branches. He explained that the bal branch processes blocks 2.6 times faster than the master branch, with state root calculation being the slowest step. Jared also mentioned ongoing work to optimize pre-processing steps and will continue to run longer benchmarks to gather more accurate performance data.

The team discussed the benefits and tradeoffs of different I/O strategies for block processing. Jared explained that while parallel I/O provides some speedup, state locations are not strictly necessary for execution, though they could be useful for accessing more detailed information about block changes. Po presented benchmark results showing that pre-fetching block states can improve state read rates through multi-layer reading and snapshot techniques, though Toni requested these results be shared with the group. The team agreed to conduct more detailed benchmarks to evaluate the performance impact of batch loading and state location usage, with Toni emphasizing the importance of understanding how larger block sizes would affect execution times versus I/O times.

The team discussed performance improvements in state processing, with Toni noting a 2x speedup in average cases and a 33x speedup in worst cases when using 32 cores. Jared suggested exploring the possibility of batch loading non-mutated storage slots and accounts after starting state route calculations, while Toni and Carl emphasized the need to balance I/O costs against performance gains. The group agreed that benchmarks against Mainnet would be necessary to determine the optimal approach, with Karim adding that mixing I/O and CPU operations during block processing might be beneficial.

Rahul and Felipe provided updates on testing efforts, focusing on a Python-based testing framework and integration with specs. Felipe explained the workflow, including how transactions are processed and tested, while Rahul highlighted the aggregation of test cases into a structured markdown file for better organization. They discussed the need for more complex and invalid tests, as well as the development of an adoption dashboard using an integration framework to track client progress.

The team discussed progress on implementing the BAL (Block Access List) EIP across different client projects. Toni requested client teams to provide updates on their progress, with Jared mentioning their first PR review scheduled for tomorrow. Mirgee from Beizu reported they had implemented the degree protocol for BLs but needed to update the engineering EIP and address potential edge cases. Mark from Aragon shared that they were working on the bound implementation and expected to provide an estimate by the end of the week, while Soubhik from Refuel reported progress on the engine API changes and reads/writes storage implementation. The team agreed to continue benchmarking to decide whether to include reads in the devnet, with Toni noting that Geff and Bezu might be the first clients ready for devnet deployment.

The team discussed keeping reads in the EIP for now to evaluate worst-case performance without them, with Toni agreeing to maintain the current implementation. Marc inquired about RLP versus SSZ, and Toni confirmed broad consensus to use RLP due to its simplicity and smaller size, noting some potential advantages of SSZ with compact proofs. The team agreed to meet again in two weeks for the next breakout call, with an unnamed participant suggesting a target of three weeks for the bal-devnet-0 release.

### Next Steps:

- Jared to implement and benchmark reads in Geth to evaluate performance impact of batch I/O vs. on-demand loading.
- Jared to continue running longer benchmarks on Geth implementation to verify the 2.2x speed-up holds.
- Po  to share detailed benchmark results on batch I/O performance with the group.
- Client developers to submit new edge case test cases as PRs to the markdown file shared by Rahul.
- Rahul and Felipe to finalize the basic test set and make a small release for client integration.
- Felipe to continue work on implementing more complex test structures and invalid tests.
- Client teams  to continue implementation of EIP-7928 and provide updates at the next call.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: &!20q46o)
- Download Chat (Passcode: &!20q46o)

---

**system** (2025-08-27):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=cEpkVjvK4kE

---

**system** (2025-08-28):

### Meeting Summary:

The team discussed streaming arrangements for an upcoming meeting and confirmed they would stream on both X and YouTube platforms. The main focus was on the implementation progress of EIPs, particularly the Geth implementation where Jared presented benchmark results and discussed performance improvements in state processing. The team also reviewed testing efforts, client progress on implementing the BAL EIP, and agreed to maintain the current implementation while continuing to evaluate performance and benchmark results for future devnet deployment.

**Click to expand detailed summary**

Toni and Pooja discussed streaming arrangements for an upcoming meeting, agreeing to stream on both X and YouTube platforms. Pooja confirmed she would be ready to stream in about 2 minutes, and Toni decided to wait a few more minutes before starting the stream. Once ready, Toni gave the signal to Pooja, who confirmed they were live. The meeting then began with Toni welcoming everyone to the 1st EOP 7, 9, 28 Breakout call.

The team discussed the implementation progress of EIPs, focusing on the Geth implementation where Jared reported that block access list execution and building are complete, though storage and account reads are still pending. Jared presented benchmark results and mentioned that the code is ready for a devnet, pending verification of consensus and engine API changes. Toni noted that the inclusion of reads is still under discussion, with parallel I/O being considered valuable for larger blocks.

Jared presented an overview of the current serial and parallel transaction execution models, highlighting the performance differences between the master and bal branches. He explained that the bal branch processes blocks 2.6 times faster than the master branch, with state root calculation being the slowest step. Jared also mentioned ongoing work to optimize pre-processing steps and will continue to run longer benchmarks to gather more accurate performance data.

The team discussed the benefits and tradeoffs of different I/O strategies for block processing. Jared explained that while parallel I/O provides some speedup, state locations are not strictly necessary for execution, though they could be useful for accessing more detailed information about block changes. Po presented benchmark results showing that pre-fetching block states can improve state read rates through multi-layer reading and snapshot techniques, though Toni requested these results be shared with the group. The team agreed to conduct more detailed benchmarks to evaluate the performance impact of batch loading and state location usage, with Toni emphasizing the importance of understanding how larger block sizes would affect execution times versus I/O times.

The team discussed performance improvements in state processing, with Toni noting a 2x speedup in average cases and a 33x speedup in worst cases when using 32 cores. Jared suggested exploring the possibility of batch loading non-mutated storage slots and accounts after starting state route calculations, while Toni and Carl emphasized the need to balance I/O costs against performance gains. The group agreed that benchmarks against Mainnet would be necessary to determine the optimal approach, with Karim adding that mixing I/O and CPU operations during block processing might be beneficial.

Rahul and Felipe provided updates on testing efforts, focusing on a Python-based testing framework and integration with specs. Felipe explained the workflow, including how transactions are processed and tested, while Rahul highlighted the aggregation of test cases into a structured markdown file for better organization. They discussed the need for more complex and invalid tests, as well as the development of an adoption dashboard using an integration framework to track client progress.

The team discussed progress on implementing the BAL (Block Access List) EIP across different client projects. Toni requested client teams to provide updates on their progress, with Jared mentioning their first PR review scheduled for tomorrow. Mirgee from Beizu reported they had implemented the degree protocol for BLs but needed to update the engineering EIP and address potential edge cases. Mark from Aragon shared that they were working on the bound implementation and expected to provide an estimate by the end of the week, while Soubhik from Refuel reported progress on the engine API changes and reads/writes storage implementation. The team agreed to continue benchmarking to decide whether to include reads in the devnet, with Toni noting that Geff and Bezu might be the first clients ready for devnet deployment.

The team discussed keeping reads in the EIP for now to evaluate worst-case performance without them, with Toni agreeing to maintain the current implementation. Marc inquired about RLP versus SSZ, and Toni confirmed broad consensus to use RLP due to its simplicity and smaller size, noting some potential advantages of SSZ with compact proofs. The team agreed to meet again in two weeks for the next breakout call, with an unnamed participant suggesting a target of three weeks for the bal-devnet-0 release.

### Next Steps:

- Jared to implement and benchmark reads in Geth to evaluate performance impact of batch I/O vs. on-demand loading.
- Jared to continue running longer benchmarks on Geth implementation to verify the 2.2x speed-up holds.
- Po  to share detailed benchmark results on batch I/O performance with the group.
- Client developers to submit new edge case test cases as PRs to the markdown file shared by Rahul.
- Rahul and Felipe to finalize the basic test set and make a small release for client integration.
- Felipe to continue work on implementing more complex test structures and invalid tests.
- Client teams  to continue implementation of EIP-7928 and provide updates at the next call.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: &!20q46o)
- Download Chat (Passcode: &!20q46o)

---

**system** (2025-08-28):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=cEpkVjvK4kE

