---
source: magicians
topic_id: 24343
title: "EIP-7928: Block-level Access Lists: The Case for Glamsterdam"
author: Nerolation
date: "2025-05-26"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/eip-7928-block-level-access-lists-the-case-for-glamsterdam/24343
views: 1059
likes: 10
posts_count: 6
---

# EIP-7928: Block-level Access Lists: The Case for Glamsterdam

# Block-Level Access Lists: The Case for Glamsterdam

By [Toni](https://x.com/nero_eth), [Francesco](https://x.com/fradamt), [Jochem](https://x.com/JochemBrouwer96) and [Ignacio](https://x.com/ignaciohagopian).

> This short note follows a template designed by @timbeiko to propose a headline feature for fork inclusion.

In this document, we propose **Block-Level Access Lists (BALs)** for inclusion in the Glamsterdam hard fork.

## Summary

[EIP-7928](https://eips.ethereum.org/EIPS/eip-7928) introduces Block-Level Access Lists (BALs), a mechanism to enable parallel execution of transactions. By enforcing an explicit mapping of each transaction to the state it touches or modifies (storage keys, balances, nonces), clients can parallelize both disk I/O and EVM execution (incl. state root calculation). This accelerates block processing and increases throughput. The main beneficiaries are node operators (due to reduced validation latency) and everyone profiting from scaling Ethereum L1 (apps, users, and infrastructure providers).

## Detailed Justification

Clients execute transactions sequentially due to unknown access patterns, limiting parallelism and increasing block processing latency. While optimistic parallel execution exists, it relies on speculative assumptions and incurs overhead, especially ineffective for worst-case blocks with many dependencies.

BALs resolve this by making transaction access and state changes explicit. With this information, clients can deterministically parallelize both EVM execution and disk I/O without speculation. This reduces worst-case block processing time and enables more predictable performance.

Beyond parallelism, explicit state diffs enable execution-less validation (e.g., for zk clients), pre-execution analysis (e.g., inclusion lists, warming) and improved data indexing and sync methods. These benefits justify the modest size overhead BALs introduce.

## Primary Benefits

**Parallelization**: Reduces maximum block processing time.

By including storage locations and transaction-level state diffs in blocks, transactions can be parallelized. Most clients already support optimistic parallelization (block-wide pre-loading), which works well for average blocks but struggles with blocks that have long dependency chains. BALs enable *perfectly parallel* validation, untangling dependencies and allowing transactions to be processed in arbitrary order—independent of each other.

## Secondary Benefits

**State transition without execution**: BALs are full state diffs. This allows clients to derive the post-state from the pre-state and the BAL (`apply_bal(pre_state, bal) -> post_state`). This has several implications:

- In zkEVM contexts, nodes can verify a proof and skip execution while still maintaining full state.
- Can be used to update state during sync or reorgs.
- Partial statelessness benefits, as BALs help partially stateless nodes maintain only the subset of state they care about.
- Assists proposals like FOCIL (inclusion lists) that require post-execution validity checks. By applying the BAL to the pre-state, checks that could usually only be done after transaction execution can be performed pre transaction execution.

The same applies to block-level warming with fair cost distribution. Today, this could only be done after executing every transaction but, having BALs, can be done earlier, before execution.

**Simpler alternative to RPC methods**:

- Account balance indexing has long been a pain point for many application developers. BALs help solve this by allowing developers to track balances without relying on numerous RPC calls. Users and applications can access and maintain balance information directly from the block—making the process much more efficient and straightforward.

## Why Now?

The community has expressed a clear desire: Ethereum L1 must scale to meet the needs of users and developers. BALs unlock performance gains critical for higher throughput and/or shorter slot times. They also pave the way for zkEVM-based light nodes (executionless + stateless), full nodes (executionless + stateful) and partially stateless execution.

In Fusaka, [EIP-7825](https://eips.ethereum.org/EIPS/eip-7825) takes the first step by capping the gas limit of individual transactions, which enforces a baseline level of parallel execution.

## Compared to Alternatives

Optimistic parallel execution is already implemented in most clients. It performs well for average blocks, where many transactions are independent (see [dependency.pics](https://dependency.pics)), but it fails to parallelize worst-case blocks where each transaction depends on the previous one’s writes. BALs improve performance not only in the average case but especially in the worst case, which is key to predictable and scalable execution.

## Stakeholder Impact

**Positive:**

- Users benefit from cheaper L1 transactions.
- Validators and node operators experience lower computational overhead (removes the need for optimistic parallelization mechanisms that effectively execute blocks twice).
- Execution clients gain a more predictable model of transaction independence, enabling deeper optimizations.
- Users and apps benefit from easier data indexing.

**Negative or Trade-Offs:**

- Block builders are responsible for generating accurate BALs. This task is straightforward, and discussions with builders have shown that the added complexity is negligible. It’s a small extra effort for builders that greatly simplifies the job of validators.
- Block size overhead: At 36m gas limit, BALs add an average of ~45 KiB per block. This is due to the inclusion of (1) storage locations and (2) state diffs (~50:50 in size). While this is modest compared to worst-case calldata blocks, it is a persistent cost that must be benchmarked across different workloads and gas limits. Importantly, large-BAL blocks and large-calldata blocks are mutually exclusive, thus the worst-case block size remains the same as today.

## Technical Readiness

The specification is included in [EIP-7928](https://eips.ethereum.org/EIPS/eip-7928), and the SSZ data structures are well-defined. Implementation discussions are ongoing with multiple execution client teams, and preliminary prototypes are in the making. There are [initial specs](https://github.com/ethereum/execution-specs/compare/forks/osaka...nerolation:execution-specs:BALs) implemented using the  ethereum/execution-specs. No changes are required to the consensus layer.

With targeting a 2026 hard fork, researchers and client teams have ample time for further analysis, implementation, testing, and simulation.

## Security & Open Questions

**Open Questions:**

**What exactly should go in the BAL?**

 →  The design space is discussed [here](https://ethresear.ch/t/block-level-access-lists-bals/22331).

Two key insights from the ongoing discussion:

1. Transaction-level state diffs are valuable beyond just parallelization, with benefits outlined above.
2. The primary contributor to BAL size is reads. Reads are cheaper than writes, thus can be done more often within a single block, leading to larger BALs. Removing storage locations from BALs (only keeping tx-level state diffs for writes) significantly reduces their average and worst-case size.

Removing storage locations from the BAL would halve its size but would also eliminate the ability to perform batch I/O at the beginning of block processing. So the key question is:

**Should we preserve storage locations in BALs for increased utility, or drop them for smaller size?**

## Replies

**gballet** (2025-05-28):

I am a proponent of BALs, I do think they can serve as a first step for statelessness. There are however many important open questions to be resolved before this should be considered:

1. This is lacking a proper analysis of how often the worst case really happens. Looking at dependency.pics, it doesn’t seem it’s happening that often (at all, really). Is it really worth the bandwidth costs, so that a few  block, from time to time, are not super optimal? I would like to see this addressed.
2. There are 5 different designs, and some of the touted properties of BALs are only available in some of these designs.
3. To my knowledge, no measurements of mainnet have been published. I suggest also running a perfnet and a bloatnet, in order to find out how they really perform on a network.

Proposing this for Glamsterdam at this stage is, in my opinion, a recipe for disaster. We need to schedule EIPs that are clearly designed and with no open questions, otherwise the same thing will happen as with EOF: delayed fork, and then simply dropped.

---

**gballet** (2025-05-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> Partial statelessness benefits, as BALs help partially stateless nodes maintain only the subset of state they care about.

This would have to be trusted, though: You would need some kind of extra mechanism to validate that the BAL is correct, which partial stateless designs can’t. Verkle can do this, binary trees can do this, zkvms can do this, each with many trade-offs. I don’t see how that would be true with BALs.

---

**Nerolation** (2025-05-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> This is lacking a proper analysis of how often the worst case really happens. Looking at dependency.pics, it doesn’t seem it’s happening that often (at all, really). Is it really worth the bandwidth costs, so that a few block, from time to time, are not super optimal? I would like to see this addressed.

I did some initial analysis on [Execution Dependencies](https://ethresear.ch/t/execution-dependencies/22150) and the main findings were that “*most blocks are highly parallelizable. On average, 60–80% of transactions are completely independent, and dependency chains are shallow. However, a small number of blocks have heavy entanglement and long critical paths, limiting parallelism — especially near the top-of-block (ToB), where MEV searchers compete for order*.”

This was the [design exploration](https://ethresear.ch/t/block-level-access-lists-bals/22331) with some concrete numbers:

I agree with your point and further analysis are needed (which are in the pipeline).

I agree that bandwidth is a key constraint in here. Currently, the size of a BAL is around 40–50 KiB, and this does not scale linearly with the gas limit. Eliminating the storage location fields could reduce their size by roughly half, but it’s unclear whether that trade-off is desirable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> There are 5 different designs, and some of the touted properties of BALs are only available in some of these designs.

Right now, the discussions settled on storage locations + post-tx state diffs, with the storage locations TBD. Removing them saves space but also removes some functionality.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> I suggest also running a perfnet and a bloatnet, in order to find out how they really perform on a network.

Agreed. I also think we’ll need state diffs regardless of any performance gains, since zk nodes that want to maintain state will require them anyway. The real question is whether to go with post-transaction diffs or post-block diffs. Their worst-case sizes are basically the same, and while post-block diffs are slightly smaller on average, most transactions are independent,  so the difference in size is very small on average. If the parallelization benefits don’t play out in prototypes, we can switch to post-block diffs. But I expect the gains from fully parallelizable blocks to make post-tx diffs clearly worth it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> This would have to be trusted, though: You would need some kind of extra mechanism to validate that the BAL is correct, which partial stateless designs can’t. Verkle can do this, binary trees can do this, zkvms can do this, each with many trade-offs. I don’t see how that would be true with BALs.

Yeah, you’re right, in order to trustlessly stay at the tip of the chain you’d need witnesses coming alongside the state diff and thus you wouldn’t be able to use it for validating but there are other use cases for it. Every full node user that just cares about having access to an RPC could run a partial statelessness node. Every node that wants to quickly sync and accepts the “risk” to not have merkle proofs alongside with state diffs since it finds out about the correctness of the syncing process if arriving at the correct head.

The problem I see with witnesses are just their size.

---

**ihagopian** (2025-05-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> This is lacking a proper analysis of how often the worst case really happens. Looking at dependency.pics, it doesn’t seem it’s happening that often (at all, really). Is it really worth the bandwidth costs, so that a few block, from time to time, are not super optimal? I would like to see this addressed.

Note that worst-case scenario relevance can’t only be weighted by historical frequency since they can also be used for attacks. If the gas limit is raised and there’s no control over the worst-case scenario, you would have a new DoS vector.

---

**Nerolation** (2025-05-29):

This is true but applies to everything. Increasing the gas limit should always only be considered after evaluating limits such as the maximum block size the network can support and the number of storage ops nodes can handle.

In terms of worst-case block sizes, even after EIP-7623, blocks filled with calldata can still be larger than those filled with max-size BALs. However, these two types of data are **exclusive**: a block cannot reach the maximum for both simultaneously. Therefore, if the goal is to DoS attack, calldata remains the more effective approach. That said, **sustained** use of either at maximum capacity **is not feasible**, as the base fee would increase exponentially. While it’s important that the network can handle worst-case peaks, it’s the average case that reflects long-term sustainability.

