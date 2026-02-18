---
source: magicians
topic_id: 26739
title: All Core Devs - Testing (ACDT) #62, December 1, 2025
author: system
date: "2025-11-27"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-62-december-1-2025/26739
views: 75
likes: 1
posts_count: 4
---

# All Core Devs - Testing (ACDT) #62, December 1, 2025

### Agenda

**Happy 5th birthday beaconchain!**  ![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=15)

Fusaka:

- msf-1
- mainnet fork on wednesday

Glamsterdam:

- bal-devnet-0 updates
- epbs-devnet-0 update

XXM gas topic:

- Mainnet has reached 60M gas
- Wen 80M gas?

Engine API changes:

- ssz vs protobuff vs grpc

Max blobs flag discussion

**Meeting Time:** Monday, December 01, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1820)

## Replies

**system** (2025-12-01):

### Meeting Summary:

The team celebrated the Beacon Chain’s fifth anniversary and reviewed progress on client implementations, with most clients passing execution tests and plans for a DevNet launch. The team discussed gas limit increases and associated challenges, agreeing to target 75 million gas units before reaching 80 million, while also reviewing various EIPs related to receipt sizes and block building. The group explored transitioning from RLP to SSZ encoding and decided to conduct benchmarking tests, with plans to postpone the transition to ACDT calls until January.

**Click to expand detailed summary**

The team celebrated the fifth anniversary of the Beacon Chain launch and discussed progress on various clients. Most clients are passing execution spec tests, with some issues being addressed. The team plans to start a DevNet soon and will have a breakout call on Friday to discuss ePBS updates. The decision on trustless payments will be made at the next ACDC call in about a week and a half. The mainnet has reached 60 million gas units, and the team is targeting 80 million gas units, with discussions on achieving this goal to follow.

The team discussed the challenges with increasing the gas limit to 80 million, particularly regarding receipt sizes and the 10MB message limit in the DevP2P network. They agreed to target a gas limit increase to 75 million first, leaving a buffer before reaching 80 million, with implementation planned for around the end of January. The team also reviewed an EIP (7975) that would allow receipts to exceed the current limit, though this would require a protocol update. Additionally, they discussed a new testing capability for block building and a proposed EIP (7872) to limit the number of blobs included in a block, which most clients appeared to support.

The team discussed transitioning from RLP to SSZ encoding, with Alexey proposing to start work on SSZ implementation once a few endpoints support the format. Barnabas suggested EngineAPI as a potential first application, while Łukasz emphasized the need to consider this in the Glamsterdam scope planning due to the effort required. The group agreed to conduct benchmarking tests comparing SSZ, JSON, and other formats, particularly for GetBlobs and GetPayload functions, to determine the optimal approach. They also decided to postpone the transition to ACDT calls until January 1st, with the first ACDT meeting scheduled for January 5th.

### Next Steps:

- Justin: Post the agenda for the ePBS breakout call on Friday
- Barnabas: Reach out to different EL teams to check on their EIP-7975 implementation progress and schedule a meeting for late January or beginning of February
- Kamil and EF team: Rework all gas benchmarks to Fusaka this week and next week
- Kamil: Summarize and send a note on what needs to be done to bump gas limit further
- EL teams: Review and provide feedback on the new RPC namespace PR for testing capabilities  within a week
- Barnabas: Push for benchmarks on SSZ vs JSON encoding for Engine API
- Barnabas: Merge BAL and PBS breakout calls into ACDC starting from January 1st

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: d!DF3k12)
- Download Chat (Passcode: d!DF3k12)
- Download Audio (Passcode: d!DF3k12)

---

**system** (2025-12-01):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=J4tWSYe_nWQ

---

**poojaranjan** (2025-12-01):

# All Core Devs - Testing (ACDT) #62, December 1, 2025 (Quick notes)

Barnabas Busa facilitated the call

## Happy 5th Birthday, Beacon Chain!

Barnabas congratulated everyone on the 5th anniv of beacon chain launch. A big milestone for Ethereum’s consensus journey.

## Fusaka

- msf-1 concluded last week, was a success. No obvious bugs were found.
- Mainnet fork on Wednesday: Feeling safe to be moving on the fork.

## Glamsterdam Devnet Updates

### BAL devnet 0 update

Stefan

- Strong progress on consensus and execution testing
- Clients successfully passing execution spec tests
- Devnet launch expected soon
- Kurtosis framework testing in active development

#### Clients update

**Nethermind**(Marc)

- Overall progress going well
- Client is passing key spec tests

**Nimbus** (Dustin)

- Passing 5 or 7 checks consistently

**Besu** (Felipe) shared in chat

- 100% passing tests

**Reth** (Dragan Rakita)

- Review needed on withdrawal flow tests

Spencer

- Running static, niche-case tests may be valuable
- Use Ethereum test suite for edge-case coverage on BALs

### ePBS devnet 0 update

Justin Traglia:

- ePBS progress is steady, and changes are being merged into trunk
- Breakout call scheduled this Friday
- Justin will review refactoring
- Decision on trustless payments expected this Friday or next All Core Dev meeting

**Lodestar** (in chat)

- Steady progress on state transition
- Now passing v1.6.1 spec

## Gas & Network Capacity

Barnabas

- Ethereum mainnet reached 60M gas per block last week; the next milestone target is 80M gas.
- Jochem Brouwer raised a concern related to 80M gas receipts size.
- Also shared the EIP PFId for Glamsterdam addressing receipts size concerns: EIP‑7975.
- Kamil Chodoła suggested: move first to 75M gas, then ship the EIP implementation to unlock 100M gas later.
- Barnabas asked from the goup on async adoption of the EIP.
- Ben Adams noted that partial adoption of EIP is not a disaster if done safely.
- Łukasz Rozmej shared that increases are possible once client implementations align and are ready.
- Lukasz updated that Carlos from EF is working on state tests.
- Kamil: Some state/receipt tests remain challenging but are expected to be edge cases, not blockers. The plan is to roll out Fusaka first, then continue gas expansion work toward 80M–100M.
- Testing teams expressed support and interest in spinning up a performance test network.

#### Next Steps Agreed

- Barnabas will reach out to client teams to check readiness.
- Performance network (“perfnet”) to test 75M gas and receipts: proposed by Kamil → agreed by Jochem.
- Will be discussed around the end of January.

## Block building

- Marcin Sobczak is building a common interface to trigger Execution Layer client (Nethermind) block creation here.
- It would be great for other client teams to review this early version — it still needs small updates, but it will significantly improve the testability of Ethereum block building and enable better test generation.
- Suggesting the Ethereum DevOps Team could review implementation needs.
- EIP‑7951 interactions can be part of broader testing coverage.
- Kamil also suggested following up next week so teams can measure progress and align releases.

## ssz vs protobuff vs grpc

Teams want to discuss improving Ethereum’s data format and serialization in future network upgrades, especially for the Glamsterdam upgrade.

- Barnabas: Proposed these API changes after multiple discussions and wants feedback from the Execution Layer (EL) teams.
- Alexey: Says this will help the EL move to the more efficient SSZ format faster and that serialization needs to be optimized for performance.
- Lukasz: Notes that changes should be considered during Glamsterdam but warns that in Nethermind, current libraries are missing and it requires heavy effort.
- EL teams generally see SSZ support as an important future goal, but right now, it’s still on the wishlist, not finalized.

#### Next Steps

- The BAL and ePBS breakout calls will transition to ACDT on Jan 5 onward.
- The finalized decisions on API changes will be reviewed again in early 2025.

