---
source: magicians
topic_id: 25594
title: FOCIL Breakout #21, October 7, 2025
author: system
date: "2025-09-26"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/focil-breakout-21-october-7-2025/25594
views: 29
likes: 0
posts_count: 6
---

# FOCIL Breakout #21, October 7, 2025

### Agenda

- FOCIL on native rollups
- Development updates

**Meeting Time:** Tuesday, October 07, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1743)

## Replies

**system** (2025-09-26):

YouTube recording available: https://youtu.be/7Jy3QttPHoc

---

**system** (2025-10-07):

### Meeting Summary:

The meeting focused on discussing the implementation of forced transactions in roll-ups and the challenges faced by native roll-ups in using the Engine API. Donnoh and Potuz debated the limitations and assumptions involved in reusing existing checks for forced transactions, emphasizing the need for a centralized sequencer and the potential restrictions on design space. Development updates included unit tests for inclusion lists, fixes for fork-choice and beacon block timeout errors, and progress on metrics for Reth and Lodestar clients, while Katya raised questions about counting invalid transactions and proposed combining metrics for CL and EL parts in a dashboard for easier comparison.

**Click to expand detailed summary**

Luca from L2Bit presented on native rollups, explaining their concept and the challenges of implementing forced transactions. He discussed how native rollups can leverage the execute precompile to minimize risks and maintain feature parity with L1. Luca highlighted the difficulties of implementing forced transactions in rollups with centralized sequencers, suggesting the use of inclusion lists to address this issue. He also explored how Fossil’s implementation could be adapted to support forced transactions in native rollups. The discussion touched on potential challenges with transaction resubmission and validation in the context of inclusion lists.

Donnoh and Jihoon discussed the challenges of implementing forced transactions in L2s, particularly for native roll-ups. They explored the potential benefits of having FOCIL in L1, which could simplify the work for L2s and improve censorship resistance. Potuz clarified that FOCIL on L2 would involve reusing the execution layer’s transaction check function, which is not a mechanism design or part of the consensus. The discussion concluded with an agreement that while having FOCIL in L1 could benefit L2s, it should not be the primary reason for its inclusion in the L1 protocol.

The meeting focused on discussing the implementation of forced transactions in roll-ups and the challenges faced by native roll-ups in using the Engine API. Donnoh and Potuz debated the limitations and assumptions involved in reusing existing checks for forced transactions, emphasizing the need for a centralized sequencer and the potential restrictions on design space. Jihoon highlighted the importance of delays for reverse transactions and suggested using an empty inclusion list for external mechanisms. Development updates included unit tests for inclusion lists, fixes for fork-choice and beacon block timeout errors, and progress on metrics for Reth and Lodestar clients. Katya raised questions about counting invalid transactions and proposed combining metrics for CL and EL parts in a dashboard for easier comparison.

### Next Steps:

- Jihoon to share a document that lays out test cases for inclusion list store.
- Jihoon to follow up with Justin about where to place the test cases document .
- Jihoon to look into the “beaconBlock Timeout” error with the Geth prototype after completing testing work.
- Katya to continue building a dashboard combining relevant CL and EL metrics for easier comparison.
- Katya to share the complete dashboard design for further discussion when finished.
- Pelle and Katya to continue work on getting metrics working in Reth.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 8gBE?gwX)
- Download Chat (Passcode: 8gBE?gwX)

---

**system** (2025-10-07):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=Ga8Hpx1tHb8

---

**jihoonsong** (2025-10-09):

FOCIL opens the door for rollups to easily implement forced transactions.

### Research

**FOCIL and Native Rollups**

- In a world where L1 full nodes can perform the state transition function statelessly, this capability can be used to verify rollup states. With the EXECUTE precompile exposing this functionality, a native rollup could leverage Ethereum’s execution client code as-is for its own state transitions, without the complexity coming from custom proof systems and governance.
- Rollups implement forced transactions so users can withdraw even when a centralized sequencer crashes or censors them. Forced transactions are hard to implement though; they are usually implemented either by defining new transaction types or by operating as a based rollup for a certain time window, which may degrade UX.
- Once we have FOCIL in L1, native rollups can use it to implement forced transactions. FOCIL introduces inclusion_list_transactions parameter to state_transition in the execution spec. Native rollups can pass forced transactions to this parameter during its state transitions. In other words, rollup users can submit their forced transactions to a rollup smart contract in L1 and those queued forced transactions are passed as IL transactions during state transitions of native rollups.
- A non-native rollup can also adopt this approach if they want, which eases the burden of implementing forced transactions.

Q: FOCIL allows omitting IL transactions, if it’s invalid or there is not enough gas left. What happens when a forced transaction via FOCIL mechanism is validly omitted?

A: The user would need to resubmit a forced transaction. It’s an open problem but we’re quite optimistic that a good solution can be found.

### Implementation Updates

- Reth has fixed a bug that caused unsatisfied IL blocks due to an encoding misconfiguration and has been implementing on execution metrics.
- Lodestar has adopted basis points configs so now it can run on 6s slots for faster testing, and has fixed a bug that passed empty ILs to forkchoiceUpdated calls.

### Testing

- Jihoon has been working on adding unit tests for InclusionListStore.

### FOCIL Metrics

- Katya has shared FOCIL execution metrics PR.
- Pelle has been implementing the FOCIL execution metrics in Reth.

### Links

- The Native Rollups Book
- FOCIL on Native Rollups
- FOCIL execution metrics PR

---

**jihoonsong** (2025-10-09):

### Recording

- YouTube
- X Stream

### Summary

- X Thread
- Full Summary

