---
source: magicians
topic_id: 27395
title: All Core Devs - Testing (ACDT) #65, January 12, 2026
author: system
date: "2026-01-07"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-65-january-12-2026/27395
views: 84
likes: 2
posts_count: 5
---

# All Core Devs - Testing (ACDT) #65, January 12, 2026

### Agenda

#### Fusaka:

- Mainnet BPO 2 Outcome
- Mainnet BPO 3

#### Glamsterdam:

- bal-devnet-0/1 updates
- epbs-devnet-0 update
- EL EIP prioritization: GitHub · Where software is built

#### XXM gas topic:

- Wen 80M gas?

#### Debug RPC Endpoint

- Add RPC endpoint testing_buildBlockV1 by marcindsobczak · Pull Request #710 · ethereum/execution-apis · GitHub

#### RPC

- JSON RPC Error codes standardization using open-rpc extension specs by simsonraj · Pull Request #650 · ethereum/execution-apis · GitHub

**Meeting Time:** Monday, January 12, 2026 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1865)

## Replies

**poojaranjan** (2026-01-12):

Quick recap: [Tweet Thread](https://x.com/poojaranjan19/status/2010736991550206171)

---

**system** (2026-01-12):

### Meeting Summary:

The team reviewed progress on the mainnet VPO 2 and discussed plans for implementing BPO 3, including client updates and testing preparations. They addressed concerns about spam and fee structures in the network, while also reviewing the status of various clients and testing efforts across different implementations. The team concluded by discussing specific PRs and future releases, including plans for implementing CFI EIPs and standardizing JSON RPC error codes.

**Click to expand detailed summary**

The team discussed the successful mainnet VPO 2 and the upcoming BPO 3, which requires implementing GetBlobV3 and partial cell messages on the CL side. Barnabas reported that Lighthouse and Prysm clients have already implemented the necessary changes, and the team is planning to launch a devnet for testing. The group decided to proceed with BPO 3 implementation when ready, rather than waiting for increased demand, as it would improve efficiency. They also discussed concerns about spam and fee structures, with Justin raising questions about L2s potentially overwhelming L1 validators. The conversation ended with a brief mention of BlockLab access lists, which were expected to be released for testing that week.

The team discussed the status of various clients and testing efforts. Stefan reported that the Defnet client was running well over the holidays, with some syncing issues that have been mostly resolved. Felipe mentioned progress on testing, including a PR to increase self-destruct test cases for BALs and plans for a new test release with expanded Ethereum tests. The team also discussed the status of ePBS implementations, with Justin sharing information about recent releases and open PRs that need review. Barnabas suggested aiming for the Alpha 1 release for the devnet to avoid implementing broken Phase 0 changes.

The team discussed two PRs: a bid forwarding threshold proposal and a bug fix for builder deposits at fork. For the first PR, Barnabas suggested a floor and cap system for bid value increases, but the team agreed to kick this can down the road as it’s not enforceable and could lead to different client behaviors. For the second PR, Potuz explained a solution to allow builders to be active at the fork, which would prevent applications like Gnosis Swap from failing. The team agreed this PR was necessary but could be included in a future devnet release.

The team discussed several topics related to Ethereum development and testing. They agreed to implement the first four CFI EIPs (7778, 7708, 7843, 8024) for the next release, targeting January 21st for DevNet 2. The group decided to focus on reprice implementations rather than increasing the gas limit to 75 million. Marcin presented a PR for standardizing JSON RPC error codes, which Simsonraj explained in detail. The team agreed to review the PR and provide feedback before merging. They also discussed the need for more testing of the double RPC endpoint implementation.

### Next Steps:

- CL client teams : Implement partial messages on the CL side for BPO 3
- CL client teams: Add volume metrics listed in the beacon metrics report PR for BPO 3
- CL client teams needing help with BPO 3: Reach out to Barnabas or Raul from P2P team
- Reth team: Look into syncing issues on devnet one
- Erigon team: Resume BAL  progress now that primary developer is back from holiday
- Mario: Reach out async to Reth team to check status on block-level access lists
- Felipe: Release next test version for BAL after self-destruct PR is merged, including all old Ethereum tests for Glamsterdam
- Justin Traglia: Respond to Barnabas’ comment on the bid forwarding threshold PR
- Client teams: Review open ePBS PRs and provide feedback
- Bharath: Take PR about validator broadcasting blobs offline to clarify and provide context
- Justin Traglia and team: Discuss complicated PR  offline
- Consensus spec team: Freeze structures for ePBS to allow client implementations to proceed
- EL client teams: Implement first four CFI EIPs  for next release
- EL client teams: Provide update on CFI EIP implementation status at next ACDT
- Felipe/testing team: Start implementing the four priority EIPs in specs and tests this week
- Martin : Share analysis results on gas limit testing with client teams, targeting tomorrow
- Martin: Reach out to teams with client-specific bottleneck findings on Telegram gas-limit testing channel
- Marcin: Test Nethermind’s double RPC endpoint implementation
- Mario/testing team: Help with testing and validation of double RPC endpoint using execute for EELS
- EL client teams: Review and provide feedback on JSON RPC error codes standardization PR

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: LYp=xhP7)
- Download Chat (Passcode: LYp=xhP7)
- Download Audio (Passcode: LYp=xhP7)

---

**system** (2026-01-12):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=b70x8N8xG2A

---

**poojaranjan** (2026-01-19):

Summary: https://x.com/poojaranjan19/status/2013342579102765230

