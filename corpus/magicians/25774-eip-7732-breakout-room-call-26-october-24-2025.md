---
source: magicians
topic_id: 25774
title: EIP-7732 Breakout Room Call #26, October 24, 2025
author: system
date: "2025-10-13"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-7732-breakout-room-call-26-october-24-2025/25774
views: 48
likes: 0
posts_count: 3
---

# EIP-7732 Breakout Room Call #26, October 24, 2025

### Agenda

#### Specifications & testing

New consensus specifications: [v1.6.0-beta.1](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0-beta.1)

- eip7732: add tests for process_withdrawals block processing
- eip7732: add fork choice tests (part1)
- Add payload_status field to AttestationData
- eip7732: add slot field to DataColumnSidecar
- eip7732: fix zero-amount builder withdrawals
- eip7732: swap beacon_block_root and slot in places in DataColumnSidecar
- eip7732: set default value of BuilderPendingPayment.withdrawable_epoch to FAR_FUTURE_EPOCH
- eip7732: deal with zero value bids correctly
- eip7732: use bid in block parent validation
- eip7732: fix signed envelope yields for execution payload tests
- Clean up Gloas specs (part 1)
- Clean up Gloas specs (part 2)
- Clean up Gloas specs (part 3)
- TODO: Remove merkle proof tests in Gloas (reference)
- TODO: Add pending payment withdrawal epoch asserts (reference)

#### Implementation updates from client teams

- Prysm
- Lighthouse
- Teku
- Nimbus
- Lodestar
- Grandine

#### Proposed changes to AttestationData

There is a proposal to add a “payload status” field to `AttestationData`:

- https://github.com/ethereum/consensus-specs/pull/4655

Overview from previous breakout call:

- EIP-7732 Breakout Room Call #25, October 10, 2025 · Issue #1744 · ethereum/pm · GitHub

Discord thread:

- Discord

**Meeting Time:** Friday, October 24, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1759)

## Replies

**system** (2025-10-24):

### Meeting Summary:

The meeting began with updates on the new consensus specifications beta release and ongoing pull request reviews for EPBS DevNet Zero. Client teams provided progress reports on various Ethereum clients, including block processing, master branch merges, and state transition implementations. The team discussed potential changes to the consensus specification, including renaming fields and modifying attestation data, while also addressing validation processes and payload gossip conditions.

**Click to expand detailed summary**

The meeting began with a brief pre-stream discussion before transitioning into the main session. Justin announced the release of a new consensus specifications beta version for EPBS DevNet Zero and mentioned that several pull requests were closed, while others remained open for testing and review. He encouraged participants to review the specifications and noted that two tasks still required attention. The meeting then moved to updates from client teams, with a request for an update from the Present team, though no response was recorded in the transcript.

The team discussed progress across different Ethereum clients, with Terence noting that merging to the develop branch is blocked by the Fusaka release and waiting for a new spec due to DataColum sidecar changes. Several clients reported ongoing work, including Lighthouse’s block processing efforts, Teku’s master branch merges, and Lodestar’s implementation of state transition processing. Caleb, who is joining the Nimbus team, mentioned completing some PRs to the unstable branch and noted that networking work is about 70% complete. The conversation ended with Saulius reporting progress on ePBS implementation for Grandine, though completion is estimated to be a few weeks away.

The team discussed renaming the “Index” field to “Payload Status” in the consensus specification, with Mehdi proposing this change to simplify implementation and reduce complexity. Justin raised concerns about the difficulty of renaming fields in consensus specs, while Enrico supported the change as it would improve the specification and prevent future bugs. Potuz and ethDreamer expressed strong opposition, citing the additional complexity and boilerplate code it would require, particularly for their teams. Despite the opposition, the team agreed to consider the change if other teams supported it.

The team discussed changes to attestation data, with Saulius and Justin agreeing that implementing such changes would be too complex given the current codebase. Mark suggested postponing any attestation data changes until necessary. The group also reviewed Gossip conditions for payloads, with potuz and ethDreamer agreeing to add a condition preventing the gossiping of payloads for blocks with a root later than the latest finalized block. Shane raised questions about interop and ePBS for DevConnect, but potuz and others mentioned they would not be attending.

The team discussed the validation process for blocks and payloads, with ethDreamer raising a question about the timing constraints for blocks versus payloads. Potuz clarified that payload timeliness is independent of propagation and explained that the “older than finalized” rule is necessary to prevent advancing on a competing branch. Justin announced that he would work with Potuz and CHAIN to organize the next steps, and the conversation ended with a reminder that the next meeting would be held in two weeks.

### Next Steps:

- Mehdi: Close the PR for renaming attestation index to payload status
- Mark : Open a PR to add a condition that payloads should not be gossiped if the block root is older than the latest finalized checkpoint
- Justin: Work with Potuz and Shane to organize a group discussion for DevConnect regarding ePBS interop, dual PTC deadlines, and related topics

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: h+Bqp6sM)
- Download Chat (Passcode: h+Bqp6sM)

---

**system** (2025-10-24):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=MCnBoHlN-jU

