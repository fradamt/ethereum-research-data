---
source: magicians
topic_id: 25328
title: EIP-7732 Breakout Room Call #23, September 12, 2025
author: system
date: "2025-09-02"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-7732-breakout-room-call-23-september-12-2025/25328
views: 100
likes: 1
posts_count: 3
---

# EIP-7732 Breakout Room Call #23, September 12, 2025

### Agenda

### Specifications & testing

#### Open

- eip7732: add tests for process_withdrawals block processing

Converted to draft, what’s the status?

[eip7732: add fork choice tests (part1)](https://github.com/ethereum/consensus-specs/pull/4489)

- Need to pull in updates & rebase to gloas.

[eip7732: rename execution payload header to execution payload bid](https://github.com/ethereum/consensus-specs/pull/4525)

- Need to resolve conflicts & request another review from potuz.
- Should be able to merge this a few hours after the breakout.

[eip7732: add attestation processing tests](https://github.com/ethereum/consensus-specs/pull/4564)

- Need potuz to re-review & then we can merge.

[eip7732: add tests for execution payload availability reset](https://github.com/ethereum/consensus-specs/pull/4570)

- Need potuz to re-review & then we can merge.

#### Merged

- eip7732: do not add zero value withdrawals
- eip7732: consider builder pending payments for pending balance to withdraw
- eip7732: remove header and inclusion proof from data column sidecar
- eip7732: enforce self build header signature to point of infinity
- eip7732: abort payment on proposer equivocation
- eip7732: add note about fee recipient

### Beacon API standardization



      [github.com/ethereum/pm](https://github.com/ethereum/pm/issues/1714#issuecomment-3277268595)












####



        opened 10:56PM - 02 Sep 25 UTC



          closed 02:01PM - 15 Sep 25 UTC



        [![](https://avatars.githubusercontent.com/u/94402722?v=4)
          will-corcoran](https://github.com/will-corcoran)





          Breakout


          ePBS


          protocol-call







### UTC Date & Time

[September 12, 2025, 14:00 UTC](https://savvytime.com/conve[…]()rter/utc/sep-12-2025/2pm)

### Agenda

### Specifications & testing

#### Open

* [eip7732: add tests for process_withdrawals block processing](https://github.com/ethereum/consensus-specs/pull/4468)
    * Converted to draft, what's the status?
* [eip7732: add fork choice tests (part1)](https://github.com/ethereum/consensus-specs/pull/4489)
    * Need to pull in updates & rebase to gloas.
* [eip7732: rename execution payload header to execution payload bid](https://github.com/ethereum/consensus-specs/pull/4525)
    * Need to resolve conflicts & request another review from potuz.
    * Should be able to merge this a few hours after the breakout.
* [eip7732: add attestation processing tests](https://github.com/ethereum/consensus-specs/pull/4564)
    * Need potuz to re-review & then we can merge.
* [eip7732: add tests for execution payload availability reset](https://github.com/ethereum/consensus-specs/pull/4570)
    * Need potuz to re-review & then we can merge.

#### Merged

* [eip7732: do not add zero value withdrawals](https://github.com/ethereum/consensus-specs/pull/4509)
* [eip7732: consider builder pending payments for pending balance to withdraw](https://github.com/ethereum/consensus-specs/pull/4513)
* [eip7732: remove header and inclusion proof from data column sidecar](https://github.com/ethereum/consensus-specs/pull/4527)
* [eip7732: enforce self build header signature to point of infinity](https://github.com/ethereum/consensus-specs/pull/4552)
* [eip7732: abort payment on proposer equivocation](https://github.com/ethereum/consensus-specs/pull/4562)
* [eip7732: add note about fee recipient](https://github.com/ethereum/consensus-specs/pull/4565)

### Beacon API standardization

https://github.com/ethereum/pm/issues/1714#issuecomment-3277268595

### Impact to relays & mev-boost

* Will clients allow validators use third-party software like mev-boost & commit-boost?
    * If the answer is "no" what are the implications?
* Will builders operate builder (0x03) validators?
    * Alternatively, relays could operate validators where builders continue to submit payloads to relays, who then verify/publish the bid to the network on their behalf. For builders, this wouldn't require large changes on their part. At the very least, this would give builders more time to convert to the new system. It might continue to be useful for smaller builders who do not have sufficient capital.

### Call Series

EIP-7732 Breakout Room

<details>
<summary>🔧 Meeting Configuration</summary>

### Duration

60 minutes

### Occurrence Rate

bi-weekly

### Use Custom Meeting Link (Optional)

- [ ] I will provide my own meeting link

### Facilitator Emails (Optional)

_No response_

### Display Zoom Link in Calendar Invite (Optional)

- [x] Display Zoom link in invite

### YouTube Livestream Link (Optional)

- [x] Create YouTube livestream link
</details>












### Impact to relays & mev-boost

- Will clients allow validators use third-party software like mev-boost & commit-boost?

If the answer is “no” what are the implications?

Will builders operate builder (0x03) validators?

- Alternatively, relays could operate validators where builders continue to submit payloads to relays, who then verify/publish the bid to the network on their behalf. For builders, this wouldn’t require large changes on their part. At the very least, this would give builders more time to convert to the new system. It might continue to be useful for smaller builders who do not have sufficient capital.

**Meeting Time:** Friday, September 12, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1714)

## Replies

**system** (2025-09-12):

### Meeting Summary:

The team discussed open specification PRs and consensus specifications, focusing on header naming conventions and merging related PRs for Ethereum. They reviewed testing PRs and discussed the transition to Devnet 0, emphasizing the need to freeze the spec for header changes while leaving withdrawals as they are. The group also addressed beacon API standardization, explored builder API design, and discussed the implications of supporting off-chain relays and builders in the protocol.

**Click to expand detailed summary**

Justin led the meeting in Will’s absence, discussing open specification PRs for EIPs, primarily focusing on Terence’s contributions. The main topic was the header naming convention, where Francesco and others requested keeping the existing header structure, though Terence had renamed it to “Execution Payload Bid.” The team also noted that one PR related to “get proposer head” was not yet opened, and Justin confirmed he had merged a related PR about abort payment on proposer. The meeting experienced some technical difficulties with streaming, which were eventually resolved.

The team discussed merging several PRs related to Ethereum consensus specifications. Terence explained that while his PR to rename the execution payload header had been approved, there were conflicts that needed to be resolved. They agreed to merge Terence’s PR today, with Potuz planning to open a subsequent PR to update the header during payload processing and remove the latest block hash. The team also reviewed testing PRs, with Terence noting that while withdrawal testing was challenging, it was not currently a priority. Potuz mentioned that while the target for Devnet 0 was the end of October, there were still some decisions needed regarding the header structure and placement.

The team discussed the transition to Devnet 0, focusing on the header changes and withdrawal processes. Potuz emphasized the need to freeze the spec for Devnet 0, including the header changes, while leaving withdrawals as they are to meet the October deadline. The group agreed to prioritize the header PR and start coding on mainnet branches. Shane presented a PR for the Beacon API standardization, which received initial reviews from Erdek and others. The team identified key stakeholders for API reviews, including Jacek, Etan, Dustin, and Paul Harris, with a focus on feedback from client teams. Shane also highlighted new APIs for bids, envelopes, and payload attestation, as well as modifications to existing APIs like get block.

The team discussed the choice between creating a V4 endpoint or modifying the V3 endpoint for beacon block responses, with a consensus forming in favor of V4 for cleaner code. They also explored the use of the consensus block value field, which was confirmed to be used by Vouch and potentially other clients, with Chris Berry now handling these responsibilities. The team agreed to maintain the current process of triggering data column sidecar creation when releasing execution envelopes, eliminating the need for a new API endpoint.

The team discussed the implications of supporting off-chain relays and builders in the protocol. Potus and Justin expressed that they would prefer everything to be within the protocol, with builders potentially staking a relay to support non-staked builders. Lorenzo added that builders often have negative expected value due to rebates to apps and originators. The team agreed that the protocol spec should not specify off-protocol behavior, and Stefan raised questions about how proposers would connect to builders in this scenario.

The team discussed the flow for blind signing in the protocol, with potuz explaining the process of requesting and submitting bids, as well as signing payload envelopes. Francesco and others expressed concerns about the complexity of the proposed method compared to simply accepting signed 0-value bids with real values specified outside the protocol. The group agreed that the current mevboost-like approach might be simpler and sufficient for their needs. Shane raised questions about the builder API and direct HTTP connections to builders, which potuz addressed by explaining the potential for decentralized bid requests and fallback mechanisms. The team decided to defer further discussion on the builder API for later, as Devnet 0 would focus on self-building support.

The team discussed the design of the builder API, with Lorenzo clarifying that either signing or not signing is acceptable for the protocol evolution. They addressed questions about validator creation and compound validators, with Potuz explaining that new validators with 0x03 credentials could be created but existing validators cannot be converted to builders before the fork. The team also discussed concerns about builder endpoints and the readiness of Titan relay or builder for the fork, though specific implementation details were not finalized.

### Next Steps:

- Potuz to open a PR to keep the header with the same functionality as today, remove the latest block hash, and add a new field for the bid.
- Terence to fix conflicts and merge the PR for renaming execution payload header to execution payload bid.
- Potuz to review Terence’s attestation processing test PR.
- Potuz to review Terence’s execution payload if reset PR.
- Terence to share the link to the test cases for fork choice tests.
- Shane to reach out to Chris Berry regarding the consensus block value field in the Beacon API.
- Client teams to implement the builder API for Devnet 0 with local building support.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 3#hBX*KT)
- Download Chat (Passcode: 3#hBX*KT)

---

**system** (2025-09-12):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=bgFRXNZrbMQ

