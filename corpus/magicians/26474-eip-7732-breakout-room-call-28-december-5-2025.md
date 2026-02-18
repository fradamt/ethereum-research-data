---
source: magicians
topic_id: 26474
title: EIP-7732 Breakout Room Call #28, December 5, 2025
author: system
date: "2025-11-07"
category: Protocol Calls & happenings
tags: [breakout, epbs]
url: https://ethereum-magicians.org/t/eip-7732-breakout-room-call-28-december-5-2025/26474
views: 44
likes: 0
posts_count: 3
---

# EIP-7732 Breakout Room Call #28, December 5, 2025

### Agenda

#### Specifications & testing

New consensus specifications: [v1.6.1](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.1)

- Add tests for process_withdrawals block processing
- Add fork choice tests (part1)
- Fix randao mix processing in Gloas
- Suggest to queue DataColumnSidecars if they race the block
- Run process_builder_pending_payments before effective balance updates
- Set block_hash in the latest bid during Gloas state upgrade
- Clean up Gloas specs (part 6)
- Store full expected withdrawals in BeaconState while pending in ePBS
- Fix gloas execution_payload gossip rules typo
- Use non-placeholder value for DOMAIN_BEACON_BUILDER
- Add fork tests for Gloas
- Add test checklist for eip7732
- Refactor process_withdrawals
- Refactor get_expected_withdrawals
- Clarify setting blob_data_available in PayloadAttestation
- Add note for is_builder_payment_withdrawable
- Clarify blob sidecars broadcast section
- Fix is_builder_payment_withdrawable function

We can publish a new v1.7.0-alpha.0 release soon if clients want it.

#### Implementation updates from client teams

- Prysm
- Lighthouse
- Teku
- Nimbus
- Lodestar
- Grandine

#### Dynamic Penalty Proposal

- Speaker: @jcschlegel
- EIP-7732 Breakout Room Call #28, December 5, 2025 · Issue #1801 · ethereum/pm · GitHub

#### Builder-API with ePBS

- Speaker: @bharath-123
- EIP-7732 Breakout Room Call #28, December 5, 2025 · Issue #1801 · ethereum/pm · GitHub

#### Trustless Payments

- Speaker: @alextes
- EIP-7732 Breakout Room Call #28, December 5, 2025 · Issue #1801 · ethereum/pm · GitHub

**Meeting Time:** Friday, December 05, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1801)

## Replies

**system** (2025-12-05):

### Meeting Summary:

The team reviewed updates from various client implementations of ePBS and discussed a new consensus-spec release. A proposal for dynamic penalties in block building was presented to mitigate the free option problem, with the team publishing a specification and research post for feedback. The conversation ended with extensive discussions about the potential removal of trustless payments from the protocol, with concerns raised about market dynamics and relay operations, leading to an agreement to continue the debate at the upcoming ACDC meeting.

**Click to expand detailed summary**

The team discussed updates from various client implementations of ePBS. Justin announced a new consensus-spec release (version 1.6.1) and mentioned that the final breakout call would be on December 19th, after which discussions would move to ACDT. Client team updates were provided, with most teams reporting limited progress due to issues with Fusaka. Dustin and Caleb discussed ongoing ePBS support integration into Nimbus, while Lodestar reported progress on state transitions and work in progress for P2P and block building. Grandine shared updates on Sync Manager changes, envelope support, and fork-choice implementation.

Christoph presented a proposal for dynamic penalties to mitigate the free option problem in block building. The proposal involves adjusting penalties based on the correlation of payload failures, with penalties escalating for clusters of failures. The system would track penalties alongside pending payments, with penalties deducted from builder balances at the end of each epoch. The proposal includes theoretical guarantees and backtesting results, showing that penalties of 0.02-0.04 ETH could achieve a 0.5% acceptable failure rate. The team has published a specification and research post on ETH Research, seeking feedback on the proposal’s feasibility and potential issues.

The group discussed a proposal to remove trustless payments and staked builders, with Christoph explaining that proposers would be penalized for undelivered payloads. Potuz raised concerns about the viability of implementing this penalty mechanism, noting that builders could be off-protocol and difficult to penalize. The discussion also touched on the potential impact of liveness bugs on validators, with Potuz highlighting that this proposal could result in capital loss for validators in cases of client bugs. The conversation ended with a brief mention of moving on to discuss the builder API with ePBS.

Bharath presented a proposal for the builder API in the context of ePBS, discussing how it would function with both staked and off-protocol builders. The proposal includes a flow for communication between proposers and builders, as well as a mechanism for handling off-protocol builders through a blinded execution payload envelope. The discussion raised questions about the necessity and feasibility of supporting off-protocol builders, with some contention on the topic. Following Bharath’s presentation, Alex introduced a separate discussion on trustless payments, questioning whether it should be included in the Glamsterdam update, acknowledging the strong opinions on both sides of the debate.

The meeting focused on the debate over trustless payments in Ethereum’s protocol. Alex highlighted concerns about the potential centralization of the block-building market and the risk of reducing the number of builders if trustless payments are introduced. George and Barnabas argued that relays provide valuable services, such as OFAC compliance, that could be lost if trustless payments are implemented. The group discussed the possibility of fewer builders competing for proposer bids, which could lead to a more centralized market. Cayman suggested that the current design of trustless payments is not enforceable and proposed splitting the staked-builder and trustless payment flow for further research. The conversation ended with a debate over whether Ethereum should prioritize protocol improvements over the potential negative impacts on relays and proposers.

The team discussed the potential removal of trustless payments from the protocol, with concerns raised about the impact on builder market dynamics and relay operations. Max and Matthew expressed caution about rushing to remove trustless payments, citing potential technical complexities and the need for further analysis. Potuz emphasized the benefits of trustless payments, including resilience and liveness, and called for clear arguments for their removal. The group agreed to continue the discussion at the upcoming ACDC meeting, where a final decision will be made.

### Next Steps:

- Client teams: Review the list of unmerged PRs shared by Justin since the last breakout call
- Christoph and Bruno: Receive feedback on the dynamic penalty proposal ETH Research post and spec
- Bharath: Continue work on builder API specification for ePBS and incorporate feedback from discussions
- All participants: Review this call’s discussion on trustless payments before ACDC next week
- Justin: Publish a new consensus-spec release  if clients want it
- Community and clients: Come to a decision on trustless payments and be prepared to speak up at ACDC next week

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: 2jbW^%K8)
- Download Chat (Passcode: 2jbW^%K8)
- Download Audio (Passcode: 2jbW^%K8)

---

**system** (2025-12-05):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=LkfmeBuQeqU

