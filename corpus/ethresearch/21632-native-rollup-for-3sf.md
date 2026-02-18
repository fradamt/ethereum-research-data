---
source: ethresearch
topic_id: 21632
title: Native Rollup for 3SF
author: adust09
date: "2025-01-30"
category: Uncategorized
tags: [layer-2, single-slot-finality]
url: https://ethresear.ch/t/native-rollup-for-3sf/21632
views: 397
likes: 5
posts_count: 1
---

# Native Rollup for 3SF

Author: [@adust09](/u/adust09), [@banr1](/u/banr1) from [Titania Research](https://titaniaresear.ch/), [@keccak255](/u/keccak255) from [Titania Research](https://titaniaresear.ch/)

Special Thanks: @grandchildrice

## 1. Introduction

In this proposal, we introduce a new architecture that aims to further improve user experience(UX) by combining [Native Rollup](https://ethresear.ch/t/native-rollups-superpowers-from-l1-execution/) with [3-Slot Finality (3SF)](https://ethresear.ch/t/3-slot-finality-ssf-is-not-about-single-slot/). Specifically, we demonstrate the possibility of merging the advantage of Native Rollup where rollup EVM execution can be directly verified on L1 with 3SF, which finalizes blocks in stages. We also provide an estimate of how much time can be allocated for proof processing to the developers of the zkEL (zk execution layer). This estimate serves as useful information for teams developing a zkEL.

### 1.1. Native Rollup

Native Rollup is a mechanism that achieves high security by leveraging and verifying the L1 EVM directly. Concretely, it utilizes a newly proposed `EXECUTE` precompile contract, enabling L1 validators to directly verify rollup EVM transactions.

[![スクリーンショット 2025-01-29 18.38.43](https://ethresear.ch/uploads/default/optimized/3X/4/7/47b8c6653eee0f5c14be0475d30901107e5db0eb_2_690x431.png)スクリーンショット 2025-01-29 18.38.432160×1350 159 KB](https://ethresear.ch/uploads/default/47b8c6653eee0f5c14be0475d30901107e5db0eb)

A key feature of this approach is that it achieves exactly the same level of security and upgrade compatibility as Ethereum L1, without the need for external security councils or complex fraud proof games.

Since it is no longer strictly necessary to verify zkRollup on-chain, there is the advantage of flexible off-chain verification while controlling gas costs. Moreover, real-time settlement can be achieved, significantly simplifying synchronous composability.

### 1.2. 3-Slot Finality

[3-Slot Finality (3SF)](https://ethresear.ch/t/3-slot-finality-ssf-is-not-about-single-slot/) is a protocol design aimed at finalizing proposer-submitted blocks within three slots. In previously proposed [Single Slot Finality (SSF)](https://ethresear.ch/t/a-simple-single-slot-finality-protocol/), it was necessary to conduct about three voting rounds within one slot. In contrast, 3SF unifies these voting rounds into a single round per slot. This reduces the number of signature aggregations and P2P network propagations needed for each vote.

3SF assumes that network delay remains within a known constant Δ and that at least two-thirds of the validators behave honestly. The process within each slot of 3SF is as follows:

- Block proposal (Δ)
- head-vote + FFG-vote (2Δ)
- Freezing (2Δ)

fast-confirmation (Δ)

- view-merging (Δ)

In step 1, the proposer proposes a block.

In step 2, both the head-vote (to select the chain head) and the FFG-votes (for source and target) are executed in the same round. The current Ethereum L1 aggregation scheme is taken as a basis. First, votes are broadcast, then an aggregator collects them and broadcasts again, making the total time 2Δ.

In step 3, based on the results of steps 1 and 2, if the proposed block receives more than two-thirds of the head-votes, fast-confirmation is achieved, and the block is considered nearly irreversible. Furthermore, when the block that achieved fast-confirmation is shared among all validators as the chain head at the start of the next slot, the view is merged.

After that, the block proposed in slot 1 is justified in slot 2 and finalized in slot 3. In other words, 3SF is an approach that lengthens the finality time while shortening the confirmation time. At the same time, by combining the head vote and the FFG vote, the slot duration becomes shorter compared to SSF. Consequently, this balance is considered sufficient for most users. The slot structure of 3SF is very similar to that of the current Ethereum L1.

## 2. Native Rollup for 3SF

### 2.1. Native Rollup for existing Ethereum

zk provers in Native Rollup are anticipated to take longer to process compared to proposers or attesters. If we want the proof to be completed within one slot, we will likely have to wait for further advancements in ZKP and cryptographic technology. Hence, storing the `stateRoot` of the previous block rather than the current block has already been proposed in [EIP-7862](https://github.com/charlie-paradigm/EIPs/blob/4a3ee2ad4a0917d6b915e829c0c7fa540f72539b/EIPS/eip-7862.md). This allows the proposer to delay EVM execution. Native Rollup is premised on this approach.

Below is an illustration of slot transitions when Native Rollup is applied to the existing Ethereum.

[![スクリーンショット 2025-01-29 22.59.59](https://ethresear.ch/uploads/default/optimized/3X/a/3/a393e1d72b503270ca16ecf2cc66c28e0afbb5d6_2_690x431.png)スクリーンショット 2025-01-29 22.59.592160×1350 241 KB](https://ethresear.ch/uploads/default/a393e1d72b503270ca16ecf2cc66c28e0afbb5d6)

Here, the number after each role name means assigned to that slot. For example, attesters2 is the attesters assigned to slot 2. Also, the shaded area means that the following tasks are performed in the corresponding slot.

- Green shaded: proposer in EL execution
- Red shaded: proposer in zkEL for proof generation
- Yellow shaded: attesters in EL, execution by zkEL, verification of proof

The proposer has been idle for 4 to 12 seconds, but EIP-7862 enables delayed execution for proposer in EL. This is shown in green in the figure.

In Native Rollup, the proposer must run not only the EL and CL but also the zkEL locally. Thanks to EIP-7862, proof generation can be delayed as well. The role of the zkEL on the proposer is to generate proofs for L2 state transitions, shown in red. Unlike the EL, this can be postponed until just before the proposer step in the next slot.

Note that the `stateRoot` verified by attesters2 is from slot 1. Due to EIP-7862, this offset occurs, but it provides the benefit of delayed execution. Each `stateRoot` has an L1 and an L2 version. The L1 side confirms correctness by actually executing the computation, while the L2 side confirms correctness by verifying the zero-knowledge proof.

### 2.2. Native Rollup for 3SF

Adapting 3SF to this architecture would result in the following.

[![スクリーンショット 2025-01-29 22.57.28](https://ethresear.ch/uploads/default/optimized/3X/c/e/ce8a7e8a7ab0ff84c34486ec23a7716670d565aa_2_690x431.png)スクリーンショット 2025-01-29 22.57.282160×1350 238 KB](https://ethresear.ch/uploads/default/ce8a7e8a7ab0ff84c34486ec23a7716670d565aa)

For convenience, attesters1 and attesters2 are shown separately, but the specifications are not firmly decided, so they could be the same entities.

Whereas the existing ethereum slot processing comprises propose, vote, and aggregate, 3SF adds a freeze step. This is common processing for all validators, providing fast-confirmation and view merge.

As before, the following apply:

- Green shaded: execution by EL in proposer
- Red shaded: proof generation by zkEL in proposer
- Yellow shaded: verification of execution and proof by EL, zkEL in attesters

Even under 3SF, the situation is largely the same as with Native Rollup for the existing Ethereum. By delaying execution and verification respectively for the proposer and attester, there is some flexibility in execution time, and this does not conflict with the 3SF steps. We believe Native Rollup can be applied under 3SF as well.

**In the zkEL, the proof generation task begins when the EL requests proof generation at the start of the slot. There is then leeway up to just before the vote & aggregation phase of the next slot. In other words, if the proof can be completed within Δ + 2Δ + 2Δ + Δ = 6Δ, this scheme can be realized.** The attesters need the proof for their verification, so as long as it is generated by their verification phase, it will be in time.

However, given the current performance of zkVM, proof generation in the zkEL might takes several minutes to tens of minutes, which is not realistic. Relying on high-spec servers might be the only option for fitting it within 6Δ. If we rely on high-spec servers, there is a possibility that specialized parties will become centralized.

## 3. Discussion & Improvement

The following discussion and improvements can be made.

### 3.1 zkEL Proof Market

One potential solution to the computational cost of proof generation in the zkEL is to delegate it to an external market. If such a market can be established, even solo-stakers could easily generate proofs by outsourcing them. This is somewhat analogous to MEV-Boost. However, the following concerns arise:

- Centralization Risk

Reduced redundancy and censorship resistance
- Loss of diversity in zkVM proof methods

Distortions in incentive design

### 3.2 Additional research on 3SF

3SF still faces a tradeoff between security and usability; additional research on how to support a large number of validators may be beneficial from a security perspective when reducing finality time as 3SF does.

- Are there more efficient ways to aggregate and propagate messages? What bottlenecks exist in the current aggregation scheme in the first place?
- Is security really sufficient when discussing reducing the number of messages, such as Orbit SSF?
- How do we set issuance rewards and how much do we allocate to validators?
- Can we estimate the length of Δ and provide more specific specifications that the prover should meet?
- Is the direction of this proposal useful in the first place?

## 4. Summry

This proposal presents a new architecture that integrates Native Rollup with 3SF to enhance user experience by leveraging the security and efficiency of both systems. By enabling direct verification of rollup EVM transactions on L1 and finalizing blocks in three stages, the combined approach offers real-time settlement and flexible off-chain verification while maintaining high security standards. Overall, this integration aims to optimize scalability and security for Ethereum-based applications.
