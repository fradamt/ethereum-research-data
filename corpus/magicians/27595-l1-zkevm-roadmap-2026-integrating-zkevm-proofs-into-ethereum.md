---
source: magicians
topic_id: 27595
title: "L1-zkEVM Roadmap 2026: Integrating zkEVM Proofs into Ethereum's Core Protocol"
author: kevaundray
date: "2026-01-26"
category: Magicians
tags: [zkp, stateless, zk, execution]
url: https://ethereum-magicians.org/t/l1-zkevm-roadmap-2026-integrating-zkevm-proofs-into-ethereums-core-protocol/27595
views: 852
likes: 11
posts_count: 1
---

# L1-zkEVM Roadmap 2026: Integrating zkEVM Proofs into Ethereum's Core Protocol

**Published by the EF’s zkEVM team**

In [July 2025](https://blog.ethereum.org/2025/07/10/realtime-proving), we outlined the initial vision for snarkifying the execution layer. That update focused on the theoretical feasibility of a zkEVM on L1 and the early research into zkEVM proofs. Following the update on zkEVM [security foundations](https://blog.ethereum.org/2025/12/18/zkevm-security-foundations) late last year we are now sharing a concrete **[L1-zkEVM roadmap for 2026](https://github.com/eth-act/planning/blob/8189a4714dd719ff7dc1ad2a947909bf1810041c/projects.md#zkevm-on-l1)**.

The following post describes the set of milestones and sub-themes required for Ethereum L1 to support zkEVM proofs as a viable alternative to re-execution in the attesting workflow. This marks a fundamental shift that integrates zkEVMs back into L1 governance and infrastructure, moving from research to implementation.

### The High-Level Plan

To understand the scope of the work ahead, we must look at the pipeline required to get a proof to an attester. The 2026 roadmap focuses mainly on enabling the following end-to-end workflow:

1. EL client (stateful): produces an ExecutionWitness (stateless input)
2. zkEVM Guest Program: consumes the block and witness to perform stateless validation
3. zkVM: executes the guest program (targeting RISC-V or similar)
4. Prover: produces zkEVM Proof(s) of Execution
5. CL client: consumes and verifies the proof(s)

To make this workflow possible, the roadmap is divided into six core sub-themes:

### Execution Witness & Guest Program Standardization

**1. Execution Witness & Guest Program** One of the building blocks of this roadmap is the ability for Execution Layer (EL) clients to produce an *ExecutionWitness* — a data structure containing all required data to validate a block statelessly. Work is underway to define this format in the execution-specs, create RPC endpoints (building on debug_executionWitness), and optimize the witness for guest programs.

Concurrently, we will be defining the *Guest Programs* themselves: the stateless validation logic that consumes an EL block and witness to determine the validity of a state transition. This logic must compile to a standardized target and be reproducible.

**2. zkVM-Guest API Standardization** A resilient ecosystem requires diversity, not reliance on a single implementation. We therefore need to standardize the interface between zkVMs and guest programs, allowing various implementations of each to work together interchangeably. This standardization effort involves defining a list of minimal hardware targets, creating common C headers for precompiles and I/O, and explicitly specifying assumptions regarding memory layouts, program panic semantics and unaligned accesses to name a few.

### CL Integration and Prover Infrastructure

**3. Consensus Layer Integration** The ultimate consumer of these proofs is the Consensus Layer (CL) client. We are developing modifications to the consensus-specs to allow CL clients to verify zkEVM proofs during beacon block validation (i.e. zkAttester clients). This involves rigorous testing and potential updates to EIP-7870 to accommodate attesters, full nodes and potentially introduce new node types.

**4. Prover Infrastructure** We are building the necessary infrastructure to generate and verify proofs. This includes integrating zkVMs into Ethproofs and [Ere](https://github.com/eth-act/ere), ensuring GPU implementations are fully open source, and establishing metrics to track prover reliability. The goal is to allow attesters and provers to seamlessly use this infrastructure to verify and generate proofs.

### Security and Performance

**5. Benchmarking & Metrics** A perpetual goal of this roadmap is robust benchmarking. We need to understand the relationship between opcode usage, native cycle counts, and proving times. We will also be establishing metrics for guest programs, zkVMs, and GPU usage. This data will inform future gas repricing efforts for ZK-friendliness and help define prover hardware requirements with respect to specific gas limits.

**6. Security & Formal Verification** L1-zkEVM security remains paramount. The roadmap includes plans for formal verification of critical components — specifically the guest program, standardized targets, SNARK provers, and SNARK verifiers. We also plan to introduce dashboards to monitor testing coverage, fuzzing, and audit status.

**The impact of ePBS:** While not a direct sub-project of the L1-zkEVM roadmap in 2026, Enshrined Proposer-Builder Separation (ePBS) is a critical dependency for zkEVMs. Without ePBS, the time window for creating a proof is constrained to 1-2 seconds. With the deployment of ePBS — targeted for the upcoming “Glamsterdam” hardfork — this window expands to 6-9 seconds, significantly improving the feasibility of real-time proving.

### Join the Discussion

This roadmap represents a collaborative effort across EL teams, CL teams, zkVM developers, *EF Protocol* teams, and community contributors. To dive deeper into these technical specifications and coordinate on the milestones for the coming year, we are planning a dedicated break-out room and invite the Ethereum community to follow along and contribute to bringing an L1-zkEVM to mainnet.

To stay involved, don’t hesitate to [reach out to us](https://zkevm.ethereum.foundation/#team) and join the ongoing technical discussions in the #l1-zkevm and #l1-zkevm-protocol channels on the [EthR&D Discord server](https://discord.gg/CzYbYV3a).
