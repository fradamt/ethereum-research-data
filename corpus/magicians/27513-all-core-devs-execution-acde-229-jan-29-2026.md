---
source: magicians
topic_id: 27513
title: All Core Devs - Execution (ACDE) #229, Jan 29, 2026
author: system
date: "2026-01-19"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-229-jan-29-2026/27513
views: 62
likes: 1
posts_count: 4
---

# All Core Devs - Execution (ACDE) #229, Jan 29, 2026

### Agenda

- Housekeeping

Breakout Calls

Post Quantum transaction signature (PQTS)
- L1-zkEVM
- Glamsterdam Repricings

Glamsterdam

- devnet-2 updates
- BAL client optimizations (parallel execution, batch reads, parallel state root calculation, sync)

update by @nerolation
- repricings context by @misilva73

CFI EIP priorities for future devnets
scoping: PFI EIPs without protocol changes

- EIP-7610: Revert creation in case of non-empty storage
- EIP-7872: Max blob flag for local builders
- EIP-7949: Genesis File Format

New EIPs

- EIP-8077: eth/XX - announce transactions with nonce
- EIP-8094: eth/vhash - Blob-Aware Mempool

Hegota

- Headliner Proposal Presentations

Universal Enshrined Encrypted Mempool (EEM) by @jannikluhn
- Frame Transactions by @lightclient and @fjl

context

[SSZ execution blocks](https://ethereum-magicians.org/t/hegota-headliner-proposal-ssz-execution-blocks/27619) by [@etan-status](/u/etan-status)
see [next ACDC](https://github.com/ethereum/pm/issues/1907) for [FOCIL](https://ethereum-magicians.org/t/hegota-headliner-proposal-focil-eip-7805/27604)

**Meeting Time:** Thursday, January 29, 2026 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1883)

## Replies

**abcoathup** (2026-01-28):

## Call details

### Video, transcript & chatlog

- All Core Devs Execution #229 - Forkcast - [Forkcast] by EF Protocol Support

### News coverage

- weekly #9 | Ethereal news - [Ethereal news] edited by @abcoathup
- ACD After Hours: ACDE #229 - [ACD After Hours] by @Christine_dkim
- Highlights from ACDE #229 - [Etherworld] by @yashkamalchaturvedi

### Resources

- Glamsterdam Upgrade - Forkcast
- Hegotá Upgrade - Forkcast

---

**system** (2026-01-29):

### Meeting Summary:

The AllCoreDevs 229 meeting focused on discussing the implementation of mandatory optimizations for DevNet 2 launch and fork readiness requirements, with particular emphasis on parallel execution, batch reading, and state root calculation optimizations. The team reviewed various EIP proposals including post-quantum transaction signatures, encrypted transactions, and account abstraction features, while discussing concerns about storage collisions and client behavior divergence. The conversation ended with discussions about EIP prioritization and standardization needs, including client flags and Genesis file format, along with presentations of new proposals for improving transaction security and mempool efficiency.

**Click to expand detailed summary**

The meeting began with Ansgar welcoming attendees to AllCoreDevs 229, noting that the first meeting post-main scoping decisions focused on a packed agenda. Three breakout calls were announced, with Antonio presenting a post-quantum transaction signature breakout call starting February 4th, and Kevaundray confirming a call on February 11th at 3pm UTC. Maria was expected to announce a breakout course related to Glamsterdam repricings, but the transcript ended before she could make the announcement.

The team discussed the launch of DevNet 2 on February 4th, with Maria emphasizing the importance of having all optimizations in place by the end of February to allow for proper benchmarking before interop events in April. Toni reported that Geth, Besu, and Nethermind have implemented the three mandatory optimizations (parallel execution, batch reading, and parallel post-state route calculation), while the sync optimization remains optional. The team agreed to formalize the expectation that these optimizations are part of the official fork readiness requirements, with the batch read optimization being prioritized.

The team discussed sync optimization strategies, focusing on batch reads and parallel state root calculation for different clients. Toni explained that optimizations like BlockLab Access lists could be used for benchmarking, but Maria emphasized the importance of having agreed-upon optimizations in place by the end of February to avoid creating bottlenecks in state reads and writes. The group agreed that all clients should have the necessary optimizations implemented by the fork, with Toni noting that Geth and Besu were ready with their batch I/O implementations. Andrew expressed comfort with this approach for Erigon, though Csaba pointed out that resource requirements might still be a concern.

The team discussed the scope of Fork optimizations, clarifying that three main optimizations are expected to be part of the Fork scope, while sync optimizations for specific clients are up to individual implementation. They agreed that BALs must be served over DevP2P until the WSP, with performance optimizations being optional. The group also considered future devnet priorities, with a consensus to prioritize BAL optimizations and EIP 8037 for state growth before adding new EIPs to future devnets.

The team discussed prioritization and progress on block-level access lists, with Daniel suggesting to consider smart contract size increase for the next devnet to test worst-case scenarios. They also talked about potentially increasing the devnet gas limit to 150 million and the need to check for any limits, such as the 10 megabyte RLP size limit. Justin explained the implementation side of gas pricing and UX considerations, while Maria suggested discussing compatibility issues related to repricings in breakout calls. The team also touched on the need to formalize the devnet scoping process and make decisions on non-protocol-changing EIPs, with EIP 7610 being one of them.

The team discussed whether to include a specific EIP in the upcoming hard fork, focusing on its implications for storage interfaces and performance. Dragan explained that the EIP addresses an extremely unlikely scenario involving hash collisions or quantum computing, and suggested removing the affected accounts through a hard fork as a simpler solution. The group agreed that including this EIP in the fork scope would not be necessary, as the potential issues it addresses are highly improbable and could be handled by removing the relevant accounts.

The team discussed storage collision issues and client behavior divergence, with Daniel noting that 198 clients have implemented the current storage collision test while Reth has not. Dragan explained that Reth would continue skipping the tests as they consider passing all 200% tests unnecessary for security. Ansgar suggested keeping the EIP in CFI rather than the fork due to the behavioral divergence, while Vitalik proposed a future-proof solution involving account object creation during creation operations. The team agreed to resolve this issue asynchronously rather than during future ACDE meetings.

The team discussed the scope of EIPs, particularly regarding client flags and the Genesis file format. They agreed to DFI (Designated For Implementation) two EIPs related to client flags and Genesis file format, as these were considered out of scope for the Fork meta EIP. However, they emphasized the importance of standardizing these behaviors across clients, even if the standardization doesn’t go through the hard-fork process. Justin Florentine highlighted a gap in standardization for ChainGenesis, which could impact future features. The team also noted that while Nevermind was the only client not supporting the requested layout, progress was being made with a PR for Alexei FLCL.

Csaba presented two Ethereum Improvement Proposals (EIPs): EIP-8077, which adds metadata to mempool announcements to enable better fetching choices and selective filtering, and EIP-8094, which addresses inefficiencies in replacing blob transactions by avoiding unnecessary redistribution of blob content. The team discussed the potential impact of adding more metadata to announcements, with Łukasz and Fabio expressing concerns about increased bandwidth usage and the need to balance metadata richness with scalability. Ansgar clarified that the deadline for submitting headliner proposals for H-star is February 4th, and presentations can follow on the next AllCoreDevs call.

Jannik presented EIP 8105, which aims to add encrypted transactions to the protocol to prevent front-running and sandwich attacks. The proposal introduces a new role for key providers and a new transaction type, with encrypted transactions being included at the end of blocks. The system is designed to be flexible and neutral, allowing for various cryptographic mechanisms. The discussion touched on key systems, metadata leakage, and the timing of key revelation and transaction execution. Potuz raised concerns about pipeline benefits being lost if transactions are only executed at the very end of a slot. The proposal was presented as a co-headliner for Hecate, alongside FOCIL, to improve credibility, neutrality, and censorship resistance of Ethereum.

The meeting focused on discussing EIP 8141, a proposal for account abstraction that abstracts transaction signatures and verifies transaction validity. Felix presented the EIP, highlighting its features like frame lists for multiple calls at different permission levels and fee sponsorship. The team debated whether this EIP should be prioritized as a headliner due to its post-quantum readiness, with concerns raised about adoption and mempool compatibility. Ansgar suggested it should be a headliner to promote security and UX. The conversation ended with a brief discussion on SSC execution blocks, proposed by Etan, focusing on reducing scope to address urgent issues like latency in the Engine API and transaction data format conversion.

### Next Steps:

- Antonio: Host post-quantum transaction signature breakout call on February 4th at 3pm UTC
- Kevaundray: Host breakout call on February 11th at 3pm UTC
- Maria: Host biweekly Glamsterdam repricings breakout call on Wednesdays at 2PM UTC, starting February 4th
- All clients: Review and be aware of clarifications to EIPs 7708 and 7708 summarized in the devnet 2 document by Stefan
- All clients: Be ready for devnet 2 launch on February 4th
- All clients : Communicate feature flags for enabling/disabling BAL optimizations to Stefan for benchmarking purposes
- All clients: Implement the three core BAL optimizations  by end of February, with batch reads prioritized first
- Andrew : Prioritize batch reads optimization implementation
- All clients: Check if everything would be fine with increasing gas limit to 150 million for devnet 2
- Ansgar: Look into formalizing the devnet scoping process between ACDE and ACDT
- Ansgar: Investigate if there’s a need and good way to document BAL optimizations as part of Fork scope in official documentation
- Csaba: Share slide link in chat for networking EIPs presentation
- All clients: Review EIP 8105  proposal and provide feedback
- Felix and Matt: Expand mempool validation section in EIP 8141  documentation
- Felix and Matt: Communicate with wallet builders and infrastructure providers about upgrade path for frame transactions
- Etan: Coordinate with transaction EIP authors to build new transaction types on top of SSC rather than RLP if SSC execution blocks moves forward

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: T0PEzG##)
- Download Chat (Passcode: T0PEzG##)
- Download Audio (Passcode: T0PEzG##)

---

**system** (2026-01-29):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=4t_YTAbrH4o

