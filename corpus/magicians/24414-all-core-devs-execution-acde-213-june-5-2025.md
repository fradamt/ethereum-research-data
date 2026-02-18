---
source: magicians
topic_id: 24414
title: All Core Devs - Execution (ACDE) #213 (June 5, 2025)
author: system
date: "2025-06-02"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-213-june-5-2025/24414
views: 557
likes: 6
posts_count: 5
---

# All Core Devs - Execution (ACDE) #213 (June 5, 2025)

- June 5, 2025, 14:00-15:30 UTC
- Stream: https://www.youtube.com/watch?v=FI5n90Vg-hQ
- Ethereum Protocol Calls Calendar subscription

# Agenda

- Fusaka

Gas limit ACDT#39 follow up
- Update EIP-7883: Assume minimal base/mod length of 32 by chfast · Pull Request #9855 · ethereum/EIPs · GitHub
- RIP-7212 updates: https://github.com/ethereum/EIPs/pull/9833/
- devnet-2 EIPs

Glamsterdam

- Headliner candidates:

FOCIL
- EVM64
- Available Attestations

Other EIPs

- [EIP-7577: Versioning Scheme for EIPs](https://eips.ethereum.org/EIPS/eip-7577)

- [EIP-7928: Block-level Access Lists: The Case for Glamsterdam](https://ethereum-magicians.org/t/eip-7928-block-level-access-lists-the-case-for-glamsterdam/24343)

- [Update EIP-7773: PFI Amsterdam EIP-7793 & EIP-7843 by Marchhill · Pull Request #9858 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9858)

Logistics

- June 9 ACDT & June 12 ACDC cancelled
- @adietrichs filling in for next ACDE

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : ACDE
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : false #
- Already on Ethereum Calendar : false #
- Need YouTube stream links : true #
- Facilitator email: tim@ethereum.org
Note: The zoom link will be sent to the facilitator via email



[GitHub Issue](https://github.com/ethereum/pm/issues/1565)

## Replies

**abcoathup** (2025-06-03):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #213 (June 5, 2025)](https://ethereum-magicians.org/t/all-core-devs-execution-acde-213-june-5-2025/24414/5) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE #213 Summary – 5 June 2025
> Action Items
>
> 60 M Gas-Limit Increase
>
> Benchmark at Berlinterop and share results in #gas-limit-testing Discord channel before next ACDE call .
>
>
> Fusaka Devnet-2 – CFI list
>
> EIP-7934 RLP Execution-Block Size Cap
> EIP-7951 secp256r1 precompile (RIP-7212 rewrite – PR 9833).
> EIP-7907 Meter Contract Code Size (256 kB cap)
>
>
> EIP-5920 DFI’d from Fusaka
> ModExp Parameter Tuning – review Pawel’s PR 9855.
> EIP Versioning Process
>
> Revive EIP-7577 discussion: hash-anchored vers…

### Recordings

- https://www.youtube.com/live/FI5n90Vg-hQ?t=240s
- Eth Cat Herders:

Podcast (audio): Spotify – Web Player
- Live stream on X: https://x.com/i/broadcasts/1lDxLzXNNroGm

### Writeups

- ACDE #213: Call Minutes by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDE #213 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

fusaka-devnet-1 targeting June 9
- fusaka-devnet-2 targeting June 23

---

**system** (2025-06-05):

### Meeting Summary:

The meeting focused on discussing potential gas limit increases for Ethereum and their impact on different node operators, as well as reviewing and deciding on various Ethereum Improvement Proposals (EIPs) for upcoming network upgrades. The team explored potential headliner proposals for the Amsterdam fork, including EVM64, Fossil, and Block Access Lists, and debated their implementation and interactions. Additionally, the group discussed versioning schemes for EIPs and agreed to continue exploring options for better tracking and management of proposals.

**Click to expand detailed summary**

The meeting focused on discussing gas limit increases for Ethereum, with Parithosh explaining that while client teams were asked about potential blockers for raising the gas limit to 60 million on Mainnet, the decision was deferred until after Berlin interop testing is complete. The team acknowledged that while intermediate steps could be taken, the main concern was coordination overhead rather than technical feasibility. Micah noted the testing team’s thorough investigation into potential issues with high gas limits for stakers.

The discussion focused on the impact of increasing gas limits on different types of Ethereum node operators, particularly those running nodes at home. Micah raised concerns about the lack of research into how gas limit changes affect home RPC clients and end users, contrasting with the focus on stakers and block builders. The group discussed the feasibility of running Ethereum nodes on consumer hardware, with some arguing that 60M gas limit is still manageable for home users, while others suggested that higher gas limits would require more expensive hardware. The conversation touched on the need to distinguish between different types of nodes in future discussions and decisions.

The team discussed increasing the mainnet gas limit to 60 million, with Tim suggesting a review of requirements for a potential one-time bump or gradual increase. Marcin highlighted the need to be aware of worst-case scenarios, such as blocks taking 3 seconds to process at high gas limits. The team also reviewed updates to EIP-7883, with Marcin explaining that one proposed change would be withdrawn, and they agreed to add a fourth tender to the code. Tim encouraged everyone to review the updated EIP asynchronously and make a decision within the next week.

The team discussed replacing EIP-7212 with EIP-7951, which has a simpler cryptographic interface and extensive tests, though gas cost benchmarking is still needed. They reviewed potential EIPs for Devnet 2, with general agreement on including EIP-7212 and EIP-7934, while EIP-7907 was conditionally supported pending further discussion. The team decided to postpone the pay opcode and meter contract size EIPs for later hardforks, with Ben suggesting a 50% contract size increase as an interim solution.

The team discussed implementing EIPs for the Fusaka devnet and Glamsterdam fork. They decided to tentatively include EIP-7907 in Devnet 2, despite potential database complexity issues, while keeping EIPs 7212, 7934, and 5920 in scope. They agreed to experiment with EIP-7907 implementation and test its performance, with the understanding that if issues arise, they may need to remove it from the fork. The team also decided to move EIP-5920 to DFI and potentially include the pay opcode in Glamsterdam, though final decisions on scope for Devnet 2 and the fork were left pending successful implementation of EIP-7907.

The meeting focused on discussing potential headliner proposals for the upcoming Ethereum fork in Amsterdam, including Fossil (FOCIL), EVM64, and Delayed Execution. Wei presented EVM64, which defines new opcodes for 64-bit operations, and discussed two implementation options: one built on legacy EVM and another on top of EOA. Thomas provided an overview of Fossil, highlighting its importance in improving censorship resistance by enabling multiple validators to enforce transaction inclusion. The group discussed the urgency of implementing Fossil, with some participants expressing concern about builder centralization and the need for censorship resistance. The conversation ended with a brief discussion of the interaction between Fossil, Delayed Execution, and Block Access Lists.

Tim led a discussion on two proposed headliners for the Amsterdam event. Mingfei presented a proposal (EIP-479) aimed at enhancing Ethereum’s proof-of-stake protocol’s resilience against reorganization attacks. Tim suggested that further discussion on Mingfei’s proposal be held on the CL call, as it seemed more relevant to that audience. The conversation ended with a reminder that additional proposals could be submitted via the Ethereum Magicians thread.

The discussion focuses on block-level access lists (BAL) as a potential feature for Ethereum. Toni explains that BAL aims to introduce parallelization for batch I/O and transaction execution, which could improve L1 scaling. The feature also has secondary benefits for state updates and syncing. There is debate about whether BAL should be considered a headline feature and how it might interact with other proposed changes like FOCIL and delayed execution. Ansgar suggests separating the read and write aspects of BAL for governance decisions. Guillaume expresses support for BAL but emphasizes the need to finalize the design before scheduling implementation. The group discusses the historical context of similar proposals and the current focus on L1 scaling. Client teams have shown interest in post-transaction state diffs as part of the BAL implementation.

The team discussed two main topics: block access lists (BALs) and the “pay” opcode. Regarding BALs, Toni explained they would add approximately 40 kB on average to block size, which while non-negligible, was deemed worthwhile after considering pros and cons. The team agreed to remove the “pay” opcode from Fusaka and reconsider it for Amsterdam, with concerns raised about potential implementation implications and testing challenges. Ahmad briefly mentioned a versioning scheme for EIPs (EIP-7577) but did not elaborate.

The team discussed implementing versioning schemes for Ethereum Improvement Proposals (EIPs), with Ahmad proposing a system to track changes and versions, while Tim expressed concerns about adding unnecessary friction to the process. The group debated using commit hashes versus semantic versioning, with Tim suggesting a more comprehensive approach that would include EIP state and hard fork status. Andrew proposed stricter enforcement of freezing EIP commits on the Devnet spec, and danceratopz suggested coupling EIPs more tightly with implementations in EELS. The team agreed to continue the discussion and trial something for the Amsterdam fork.

### Next Steps:

- All: Review the slides on Available Attestation presented by Mingfei
- Client teams: Experiment with implementing block level access lists
- All: Review and provide feedback on EIP-7951
- All: Review the implications of including the PAY opcode in Fusaka
- All: Review EIP-7577 on EIP versioning and provide feedback
- Testing team: Work on a more comprehensive EIP versioning proposal that integrates with the overall EIP process
- All: Review the issue raised about blog count max per transaction
- All: Continue discussions on block level access lists in the Discord channel

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: ?JsEQK2F)
- Download Chat (Passcode: ?JsEQK2F)

---

**system** (2025-06-05):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=FI5n90Vg-hQ

---

**timbeiko** (2025-06-05):

## ACDE #213 Summary – 5 June 2025

### Action Items

1. 60 M Gas-Limit Increase

Benchmark at Berlinterop and share results in #gas-limit-testing Discord channel before next ACDE call .
2. Fusaka Devnet-2 – CFI list

EIP-7934 RLP Execution-Block Size Cap
3. EIP-7951 secp256r1 precompile (RIP-7212 rewrite – PR 9833).
4. EIP-7907 Meter Contract Code Size (256 kB cap)
5. EIP-5920 DFI’d from Fusaka
6. ModExp Parameter Tuning – review Pawel’s PR 9855.
7. EIP Versioning Process

Revive EIP-7577 discussion: hash-anchored version tags, Devnet freeze-points, and automatic EIP-bot / EELS syncing to cut test-implementation drift .
8. Glamsterdam “Headliners” – keep discussing on EthMagicians

FOCIL (tx inclusion-lists) – 7805
9. EVM64 (64-bit opcode subset) – thread
10. Available Attestations – thread
11. Block-level Access-Lists – EIP-7928

---

### Key Discussions

#### Gas-Limit Increase to 60 M

- Signalling deferred until Berlinterop results provide concrete throughput / latency data.
- Concerns: effect on home-node operators (Micah) vs. median-user UX (Dankrad); reference hardware guidance in EIP-7870.
- Marcin (Erigon) warned worst-case 60 M blocks execute in ~3 s at 20 Mgas/s .

#### Fusaka EIP Updates

- EIP-7951 – interface-identical replacement for RIP-7212; ~780 test vectors ready.
- EIP-7934 – debate over enforcement layer & runtime overhead; decision next call.
- EIP-7907 – broad community demand; database-footprint analysis underway.
- EIP-5920 – DFI’d from Fusaka, as we need to evaluate impact more thoroughly.

#### Glamsterdam Brain-Storm

- FOCIL implemented in five clients; targets mempool censorship-resistance.
- EVM64 promises faster execution via 64-bit arithmetic; benchmarks pending.
- Available Attestations aims at stronger fork-choice safety (discussion to shift to CL calls).
- Block-level Access-Lists enable deterministic parallelisation and dovetail with delayed execution, but design space still wide and must co-exist cleanly with FOCIL .

#### EIP Versioning

- Testing team urges formal version tags tied to EELS reference implementations; Tim proposes starting with commit-hash IDs then expanding to full process automation .

---

### Logistics

- ACDT #40 (9 Jun) & ACDC (12 Jun) cancelled (in-person Berlin meetings).
- ACDE #214 – 19 Jun will be chaired by @adietrichs .
- Agenda & recordings: ACDT #39 gas-limit thread.

