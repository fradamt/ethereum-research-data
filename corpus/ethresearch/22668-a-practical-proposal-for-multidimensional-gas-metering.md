---
source: ethresearch
topic_id: 22668
title: A practical proposal for Multidimensional Gas Metering
author: misilva73
date: "2025-06-25"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/a-practical-proposal-for-multidimensional-gas-metering/22668
views: 1267
likes: 9
posts_count: 22
---

# A practical proposal for Multidimensional Gas Metering

*This proposal is co-authored by myself and [@dcrapis](/u/dcrapis)*

[![fbce230bf72eb1324e03fa2e200e1cfb9044f4c38b748dadc305fd9a2c70c2f0](https://ethresear.ch/uploads/default/optimized/3X/7/9/79de9e8ed6a7bbd64c321f8400ca60b66feb3260_2_375x375.jpeg)fbce230bf72eb1324e03fa2e200e1cfb9044f4c38b748dadc305fd9a2c70c2f01024×1024 136 KB](https://ethresear.ch/uploads/default/79de9e8ed6a7bbd64c321f8400ca60b66feb3260)

We would like to thank [@soispoke](/u/soispoke), [@Julian](/u/julian), [@adietrichs](/u/adietrichs), and [@vbuterin](/u/vbuterin) for the discussion, comments, and review.

## Motivation

In Ethereum, we use gas as a measure of two important concepts for the EVM. On one hand, gas is used to measure the consumption of resources by transactions. The more a transaction uses, the more it pays in transaction fees. On the other hand, gas is also used to control resource limits and ensure that blocks are not overloading the network. Currently, validators enforce a limit of 36 million gas units per block. If a block needs more than this limit, it is considered invalid.

We can think of the first use of gas as “transaction pricing” and the second as “block metering”. Because the same metric has always represented both concepts, it is natural to think of them as interchangeable. However, we argue that we can consider them separately, and in fact, there are gains to be had by doing so. More concretely, **we can introduce a multidimensional metering scheme that accounts for the different EVM resources while maintaining the pricing model unchanged**.

But what is the benefit of doing this? First, using a multidimensional scheme to meter resources allows us to pack blocks more efficiently. In these schemes, even if a block has already reached the limit of one resource, we can still add more transactions to that block if they do not use the bottleneck resource. For example, a block that is already “full” from call data could still include computation-intensive transactions that do not spend gas on call data. This [blog post](https://vitalik.eth.limo/general/2024/05/09/multidim.html) from Vitalik explains well why the current one-dimensional scheme is not optimal.

Based on our [previous empirical analysis](https://ethresear.ch/t/going-multidimensional-an-empirical-analysis-on-gas-metering-in-the-evm/22621), a four-dimensional metering scheme that separates compute, state growth, state access, and all the other resources would allow an **increase of ~240% in transaction throughput**, assuming an infinite demand of historical transactions.

Second, even though [full multidimensional pricing](https://vitalik.eth.limo/general/2024/05/09/multidim.html) enables more flexible pricing, this flexibility comes at the cost of a worse UX experience for end-users and developers (as they now have to deal with multiple base fees and gas limits) and the risk of added incentives for bundling transactions to save on transaction fees. Moreover, EVM constraints such as in sub-calls, make the implementation of multidimensional pricing technically challenging. In other words, it is unclear whether the advantages of multidimensional pricing outweigh the potential issues. The tradeoff is much more obvious when changing the metering scheme alone.

## The New Metering Scheme

We propose **multidimensional metering** as a change to the way we account for gas used in a block. This allows us to fully utilize the gas limit for each individual resource, while still being in the safety limit, and yields significant throughput gains without changing the gas limit. Moreover, the transaction UX and the structure of the fees that are charged to users remain unchanged.

The new metering scheme introduces a new variable called `block.gas_metered`. During transaction execution we meter the gas used along each resource dimension (compute, state, access, memory, etc), say `(r_1, ... r_k)`. Then we compute

`block.gas_metered = max(r_1, ... r_k)`,

while the formula for the current definition of gas used is

`block.gas_used = sum(r_1, ... r_k).`

From the **user’s perspective everything stays the same**. A transaction still has a single `tx.gas_limit` and pays according to the actual `tx.gas_used`. The `tx.gas_used` and `tx.gas_limit` are still used to check the transaction’s “out-of-gas” condition (if during transaction execution `tx.gas_used` exceeds `tx.gas_limit` the transaction is reverted).

At the block level, **`block.gas_metered` replaces `block.gas_used`** in (1) **block validity condition** and (2) **EIP-1559 fee update calculation**.

```auto
LIMIT = 36_000_000
TARGET = LIMIT // 2

# sender is charged based on sum of resources
def compute_price_for_usage(tx_bundle):
   return basefee * sum(tx_bundle)

# block limit is enforced on the highest individual resource
def is_valid_consumption(block_bundle):
   return max(block_bundle) <= LIMIT

# basefee is updated using the highest individual resource
def compute_new_excess_gas(block_bundle):
   return max(0, excess_gas + max(block_bundle) - TARGET)
```

This proposal has the following properties:

- Increase resource utilization
- Maintain safety limit for each resource
- No changes to UX

This change is relatively simple compared to other multidimensional pricing approaches, and it yields significant improvements with a modest increase in complexity. In particular, optimal block building becomes more difficult, but simple heuristics can still be used to produce blocks. Protocol changes involve (i) introducing a gas cost schedule for resources other than compute and (ii) metering the gas used per resource. Note that since resources other than compute are used by a relatively small number of opcodes, this will only involve increasing the number of gas cost parameters from ~100 today to ~150 to account for all other resources.

Beyond yielding significant gains directly, this improvement is also an important **stepping stone to unlock future gains from multidimensional pricing**.

**Example**

The `block.gas_target` and `block.gas_limit` stay unchanged, 18m and 36m respectively. Suppose we get a block where the demand profile for each resource, measured in million gas units, is `(18, 9, 9, 6, 3)`, where each dimension in the vector is the gas attributed to a single resource. This block would be invalid under the current specification since `sum(18, 9, 9, 6, 3) = 45` exceeds the gas limit by 9 million gas units. With the new proposal the gas metered is `max(18, 9, 9, 6, 3) = 18` which makes the block valid and also right at target, so the gas fee will not change. Suppose we then get a block with high load on the second resource `(18, 30, 9, 6, 3)`, `block.gas_metered = 30` million gas units. While still being a valid block since it is bellow the limit, the base fee will increase as it is above the target.

## Next steps

Two key questions need to be answered to specify this proposal fully. First, we need to define the resources we want to track. The original gas model was designed to account for the following resources:

- Compute: the execution/CPU cost, representing the computational work performed during contract execution.
- Memory: A transient, expandable area used during execution for temporary data storage, cleared after the transaction completes.
- State: The current snapshot of all account balances, contract storage, and code maintained in a Merkle Patricia Trie.
- History: The complete record of transactions and state transitions stored on-chain, which enables nodes to reconstruct past states. History can be pruned, which is a key difference from state.
- Read / Write Access: The amount of data (proof components) required to verify a state read / write from the Merkle trie, impacting verification cost and efficiency.
- Bandwidth: The cost of sharing the block content, i.e. block size in Kb.
- Bloom Topic: A 32-byte hashed value from event topics incorporated into a 2048-bit bloom filter for efficient log filtering and query acceleration.

The question is whether the new metering system should track these same resources or not. Should any other resources be added (e.g. proving costs)? Should some resources be combined to simplify metering? Based on our previous analysis, there is a clear gain from separating at least compute, state, and access, as these are the bottleneck resources in our data. However, we may want to isolate more resources to future-proof this proposal.

The second question is how to properly split the total gas cost of each EVM operation into the various resources. Once we have defined the resources, we can perform a benchmark across the various EL clients to measure the resources used by each EVM operation (opcodes, precompiles, etc.). Of course, this requires defining how to measure the usage of the resource. For instance, for compute, we can use the execution time, while for bandwidth, we can track block size in Kb. Once we have the resource usage for each operation, we can set the safety limits for each resource and then convert them to gas units.

These benchmarks connect well with current efforts to [increase the gas limit](https://pumpthegas.org/). Here, client teams are already setting up benchmarks and tests to analyze network performance. A good example is the [Gas Cost Estimator Project](https://github.com/imapp-pl/gas-cost-estimator), which implements a comprehensive benchmark across different clients focused on computing costs. In addition, this work is closely tied to recent repricing efforts, such as [EIP-7904](https://eips.ethereum.org/EIPS/eip-7904) and [EIP-7883](https://eips.ethereum.org/EIPS/eip-7883).

## Replies

**71104** (2025-06-25):

If I understand correctly there will still be a single gas market price but four different block-level gas limits. Isn’t there a risk that the network will start preferring transactions with ~even resource usage and discarding transaction with imbalanced resource usage? That way the nodes can fill up the four gas limits more efficiently and get more rewards from gas fees.

Simplistic example: let

- L_A = 100 be the block-level gas limit for resource A,
- L_B = 150 the limit for resource B,
- U_A the amount of gas consumed by a transaction for resource A,
- U_B the amount of gas consumed by a transaction for resource B.

Won’t all nodes of the network be encouraged to prefer transactions that are as close as possible to U_B = U_A * 1.5 ? Or rather, why would a block proposer be okay with including many transactions with U_B = 0, for example? If it does that, there’s a risk it won’t be able to fill up the limit for resource B.

Unless I’m missing something, it looks to me like this scheme would encourage the network to prioritize transactions unfairly (there’s no reason why imbalanced transactions should be preferred over more balanced ones).

---

**niran** (2025-06-26):

OP Stack uses [a similar approach](https://docs.optimism.io/operators/chain-operators/configuration/batcher#batcher-sequencer-throttling) to meter demands on L1 data availability throughput. The biggest downside is that when the meter’s limit is reached, our blocks fall below the gas target.

These blocks don’t currently optimize for profit beyond ordering by priority fee, so it’s possible to get closer to the gas target with heuristics for metered resources. But even for profit-maximizing proposers, optimal blocks can fall below the gas target for extended periods.

When this happens, users must outbid each other’s priority fees in a first-price auction. Many applications do not expect to actively participate in priority fee auctions because EIP 1559 has been so successful at eliminating them, so they experience these periods as a denial of service. (The base fee also plummets to zero during these periods, so even when the meter is no longer binding, it takes time for the priority fee auction to end.)

It sounds like this proposal differs from OP Stack’s metering by including the meter in the 1559 calculation to avoid affecting the fee market. The most congested resource would determine whether gas usage is above or below target, which would prevent the priority fee auctions we see. Does that sound right?

---

**misilva73** (2025-06-27):

Even though you got the idea mostly right [@71104](/u/71104), I need to make a clarification. There is still a single-block gas limit in place. In other words, in your example, L_A=L_B. However, this does not change the effect you describe.

There are two types of blocks to consider here. First, there are the “normal-load” blocks, where block utilization is approximately 50%, and the “low-load” blocks, where block utilization is significantly less than 50%. This accounts for the majority of blocks (approximately 90%, based on our [historical analysis](https://hackmd.io/@nightingale/evm-gas-meter/%2F_yt9M7O1S4Of4WDf56ahrw#What-about-high-load-blocks)). In these blocks, there is no concern about transactions optimally balancing the various resources, as block builders can include all valid transactions.

Second, there are the “high-load” blocks, where utilization is close to 100%. From the same [empirical analysis](https://hackmd.io/@nightingale/evm-gas-meter/%2F_yt9M7O1S4Of4WDf56ahrw#What-about-high-load-blocks), these blocks occur ~10% of the time. Here, since block builders need to decide between certain transactions to include versus others, there may be an incentive to select transactions that better complement those already included. However, block packing may not be the primary criterion to make this decision. They also need to balance MEV profits and fees collected in this complex optimization problem.

So, even though we could see some incentives for more efficient block packing, these will not be prevalent enough to materially change the block composition. Interestingly, we also found that the resources used by high-load blocks are already different from the other blocks today. You can see this in the same [empirical analysis](https://hackmd.io/@nightingale/evm-gas-meter/%2F_yt9M7O1S4Of4WDf56ahrw#What-about-high-load-blocks).

---

**misilva73** (2025-06-27):

Correct, [@niran](/u/niran). In this proposal, we use the same formula for the block validity condition (i.e., how full a block is) and the EIP-1559 update rule. In both cases, we use the gas spent by the bottleneck resource. So, if the bottleneck resource exceeds the target, the base fee will increase in the next block. For the base fee to decrease, all resources need to be below the target.

---

**71104** (2025-06-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/misilva73/48/16215_2.png) misilva73:

> Second, there are the “high-load” blocks, where utilization is close to 100%. From the same empirical analysis, these blocks occur ~10% of the time. Here, since block builders need to decide between certain transactions to include versus others, there may be an incentive to select transactions that better complement those already included.

But nobody knows whether the current block will be a high-load one until it’s proposed, so it would be reasonable for all nodes to prioritize evenly balanced transactions regardless.

But even if the nodes can somehow predict whether or not the transaction rate will spike in the current slot I don’t think it’s okay to prioritize transactions unfairly ~10% of the time.

The fact that the optimization problem is further complicated by MEV is not a good excuser. If anything, this proposal creates a new MEV criterion to optimize for, making the problem worse.

---

**0x00101010** (2025-06-27):

Thank you for this proposal, I have 2 questions:

1. For performance, currently state access is most detrimental to block building, with this new design, we could potentially allow a block being built with 36 (block_limit) gas consumption state access, which is drastically higher than before (since we can still have other resource consumption as well). Curious if there’s any mitigations to this other than raising state access gas cost drastically
2. With the new design, somebody could potentially crowd out all the other actions by swarming the block with just 1 mispriced resource group, for example, if compute is priced really cheap, somebody could send all heavy compute transactions, that will cause base fee to increase, potentially pricing out other types of transactions. Is there any potential mitigations before having true multidimensional pricing?

---

**dcrapis** (2025-06-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/0x00101010/48/16183_2.png) 0x00101010:

> block being built with 36 (block_limit) gas consumption state access, which is drastically higher than before

the per resource block limit will be similar to today, not drastically higher

![](https://ethresear.ch/user_avatar/ethresear.ch/0x00101010/48/16183_2.png) 0x00101010:

> if compute is priced really cheap, somebody could send all heavy compute transactions, that will cause base fee to increase, potentially pricing out other types of transactions

the same problem is there today, and this proposal does not make it worse. full mitigation is the full multidim pricing as you say.

---

**71104** (2025-06-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/dcrapis/48/11293_2.png) dcrapis:

> the per resource block limit will be similar to today, not drastically higher

So the day this proposal goes live, all Ethereum users will suddenly be able to consume four times as much gas? Is that safe?

---

**Xiawpohr** (2025-07-05):

This proposal appears to change the block validity condition from  \sum_{i=1}^{k}r_i < L to  r_i < L \forall i \in \mathbb{Z}^{+}. Is it safe to apply the same 36M gas limit to all resources?

I’m curious about why `block.gas_metered` should be used in the EIP-1559 fee calculation. Doesn’t this reduce block proposers’ incentives to bundle more transactions? For example, consider two possible blocks with resource demands of (36, 0, 0, 0, 0) and (36, 36, 36, 36, 36) respectively. Both would increase the base fee by 12.5% under this proposal. Why would block proposers be motivated to do five times the work for the same price change?

If the goal of this proposal is to increase transaction throughput, why not simply increase `block.gas_target` when `block.gas_metered` is introduced?

---

**misilva73** (2025-07-16):

The safety concern is precisely why we are currently working on benchmarks to measure the resource consumptions of each EVM operation. The goal is to make sure that the cost per resource of each operation maps well to the block limit and that the nodes following EIP-7870 specs can still perform their duties on time.

Is there any other analysis that would make sense here in your view?

---

**misilva73** (2025-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/xiawpohr/48/19361_2.png) Xiawpohr:

> I’m curious about why block.gas_metered should be used in the EIP-1559 fee calculation.

We want to keep the EIP-1559 update rule consistent with the definition of how full a block is. To illustrate why this makes sense, let’s think about an example in a 2-resource design where the resource vector is (18M, 18M) and the limit is 36M. With multidim metering, the block utilization would be 50%, which means that we would be at target. In that case, we don’t really want to increase the base fee. If we were to increase the base fee and demand remained the same, we would see the block utilization drop below 50%. However, if we used the current formula for the base fee update, the block utilization would be 100% and the base fee would get the maximum increase.

![](https://ethresear.ch/user_avatar/ethresear.ch/xiawpohr/48/19361_2.png) Xiawpohr:

> Why would block proposers be motivated to do five times the work for the same price change?

Because they get more fees/MEV opportunities from them.

![](https://ethresear.ch/user_avatar/ethresear.ch/xiawpohr/48/19361_2.png) Xiawpohr:

> If the goal of this proposal is to increase transaction throughput, why not simply increase block.gas_target when block.gas_metered is introduced?

I don’t think they are comparable. With multidim metering, we can pack blocks more efficiently, which gives us a boost in available block space, independently of further increases in the gas limit. The idea is to align the block validity condition more accurately with the various resources’ safety limits.

---

**71104** (2025-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/misilva73/48/16215_2.png) misilva73:

> The safety concern is precisely why we are currently working on benchmarks to measure the resource consumptions of each EVM operation. The goal is to make sure that the cost per resource of each operation maps well to the block limit and that the nodes following EIP-7870 specs can still perform their duties on time.
>
>
> Is there any other analysis that would make sense here in your view?

Mapping gas costs to real-world resource costs totally makes sense to me and I’d be very interested in that kind of analysis, but I’m wondering how you’re going to deal with storage, which is a somewhat special one because it doesn’t just account for the I/O cost but also the cost of the storage itself, which in turn is unknown because you don’t know how long a smartcontract is going to keep some piece of data or if it will ever delete it. As far as I understand, that’s the main reason why storage is so expensive in Ethereum.

---

**71104** (2025-07-18):

Maybe a sensible way to deal with storage costs is to assume Moore’s law, i.e. something like “the cost of storing a word halves every 2 years”. That results in a geometric series with base \frac12, which converges to 2 when the number of iterations diverges to +\infty (see proof below).

Based on that, **the cost of storing a word forever is the cost of storing it for 2 years multiplied by 2**. That’s easy to estimate because you can take the cost of a disk with a certain capacity on GCP or AWS for a year, multiply it by 4, and divide it by the number of words that fit in that capacity.

Bonus point: double the cost further to account for Merkle hashes (see the rationale at the bottom).

---

Generic geometric series:

\begin{aligned}
S_n &= \sum_{i = 0}^n{\alpha^i} \\
S_{n + 1} &= S_n + \alpha^{n + 1} \\
S_{n + 1} &= 1 + \alpha \cdot S_n
\end{aligned}

\begin{aligned}
S_n + \alpha^{n + 1} &= 1 + \alpha \cdot S_n \\
S_n \cdot (1 - \alpha) &= 1 - \alpha^{n + 1} \\
S_n &= \frac{1 - \alpha^{n + 1}}{1 - \alpha}
\end{aligned}

When n diverges and \alpha \in (0, 1):

\lim_{n \to +\infty} \frac{1 - \alpha^{n + 1}}{1 - \alpha} = \frac{1}{1 - \alpha}

With \alpha = \frac12 that becomes 2.

---

In order to account for the Merkle hashes: in [this thread](https://ethresear.ch/t/were-mpts-ever-the-best-choice/22706) I explained why Ethereum’s MPTs tend to resemble a complete 16-ary tree when the number of leaves diverges.

The number of leaves of a complete 16-ary tree with height h is 16^h, while the total number of nodes is a geometric series with \alpha = 16 and n = h.

Let N be the number of leaves and M the total number of nodes:

\begin{aligned}
N &= 16^h \\
M &= \sum_{i = 0}^h{16^i} = \frac{16^{h + 1} - 1}{15}
\end{aligned}

Then each leaf (i.e. each stored value) contributes with \frac{M}{N} hashes:

\frac{M}{N} = \frac{16^{h + 1} - 1}{15} \cdot \frac{1}{16^h} = \frac{16^{h + 1} - 1}{16^h} \cdot \frac{1}{15}

When h \to +\infty:

\begin{aligned}
& \lim_{h \to +\infty} \frac{16^{h + 1} - 1}{16^h} \cdot \frac{1}{15} = \\
=& \frac{1}{15} \cdot \lim_{h \to +\infty} 16 \cdot \frac{16^h - \frac{1}{16}}{16^h} = \\
=& \frac{1}{15} \cdot 16 \cdot 1 = \frac{16}{15}
\end{aligned}

That is the average extra cost of the Merkle hashes of each leaf expressed in number of hashes, and it’s roughly equal to 1. Adding it to the cost of each stored word means roughly doubling the cost of the word itself.

---

**Xiawpohr** (2025-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/misilva73/48/16215_2.png) misilva73:

> We want to keep the EIP-1559 update rule consistent with the definition of how full a block is. To illustrate why this makes sense, let’s think about an example in a 2-resource design where the resource vector is (18M, 18M) and the limit is 36M. With multidim metering, the block utilization would be 50%, which means that we would be at target. In that case, we don’t really want to increase the base fee. If we were to increase the base fee and demand remained the same, we would see the block utilization drop below 50%. However, if we used the current formula for the base fee update, the block utilization would be 100% and the base fee would get the maximum increase.

I agree with keeping the EIP-1559 update rule consistent with how full a block is. However, replacing `block.gas_used` with `block.gas_metered` in the EIP-1559 fee update calculation introduces some risks.

Assuming under a 2-resource design with sufficient transactions in the mempool, validators can bundle transactions into blocks in any ways they want. How will the validators do to maximize the benefit? In the ideal scenario, they would use resources consistently at (18M, 18M) in every block, allowing the network to handle 2x the resources without any price changes. However, to maximize fees, validators might instead propose blocks with resources at (36M, 0), followed by blocks at (0, 36M), and so on. While both strategies process the same total amount of resources, the latter generates higher fees due to rising prices. This creates problematic incentives that we want to avoid, as they lead to higher gas prices, transaction delays, transaction censorship, and increased MEV activity.

![](https://ethresear.ch/user_avatar/ethresear.ch/misilva73/48/16215_2.png) misilva73:

> With multidim metering, we can pack blocks more efficiently, which gives us a boost in available block space, independently of further increases in the gas limit.

When you change the block validity condition to $r_i<L \forall i \in {1, 2, …, n}$​, the block size should become n*L, which allows us to correctly calculate how full a block is. It makes sense to me that under the same network node conditions, multidimensional metering allows us to pack blocks more efficiently, enabling the network to handle more gas per block. I think our divergence stems from the question of why available block space doesn’t equal the block gas limit in your perspective.

---

**misilva73** (2025-07-25):

This is a good question, and we are considering the best way to approach it. The simple approach is to put a hard limit on state growth per block (e.g., blocks cannot add more than 14 KB to the state trie).

Another approach can be to think of this as perpetual storage and calculating what is the cost of this perpetual commitment, discounted to today.

Open to more ideas, of course!

---

**misilva73** (2025-07-25):

Yes, this make sense! This is logic is treating it as a perpetual. I would simply add that state growth has an added cost on state I/O (i.e., larger states will take longer on average to query and update). So this is another cost that complicates matters. However, this aproach is already pretty reasonable to me.

---

**misilva73** (2025-07-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/xiawpohr/48/19361_2.png) Xiawpohr:

> I agree with keeping the EIP-1559 update rule consistent with how full a block is. However, replacing block.gas_used with block.gas_metered in the EIP-1559 fee update calculation introduces some risks.

This is a great point! When we were drafting the proposal, we also thought about how could multidim metering impact base fee manipulation attacks. However, from the perspective of the block builder/proposer, it would be more advantageous to reduce the base fee instead of increasing, no? That way they could collect more priority fees.

![](https://ethresear.ch/user_avatar/ethresear.ch/xiawpohr/48/19361_2.png) Xiawpohr:

> I think our divergence stems from the question of why available block space doesn’t equal the block gas limit in your perspective.

It think it helps to think of a specific example. Let’s assume we have a system with only two resources:

- Compute, which is measured as the time to execute a block
- Memory, which is measured as the the size of RAM occupied by the block execution

In addition, we have the following limits on the resources for a single block:

- Compute: 2s
- Memory: 1GB

Let’s also assume we have an EVM with only two operations:

- OP_C takes 0.1 s to execute and occupies no memory
- OP_M take 0.01GB of memory and takes no time to execute

We want to design a gas system that imposes our resource limits on the operations. We decide that a block will have a limit of 100 gas units. To set the costs for the operations, we map the cost of a worse-case block on each resource to the 100 gas units limit:

- For compute, the worse case block is a block full of OP_C’s. This results in a cost for a single OP_C of \frac{0.1\times 100}{2}=5 gas units.
- For memory, the worse case block is a block full of OP_M’s. This results in a cost for a single OP_M of \frac{0.01\times 100}{1}=1 gas units.

We can now see the difference between using the max rule versus the sum rule. If we had a block with 10 OP_C’s and and 50 OP_M’s, the gas cost by resource would be (50, 50). The gas used is 50+50=100, while the gas metered is \max(50,50)=50. So, with the sum, we are already at block limit. However, the block only takes 10 \times 0.1 = 1 seconds to execute and uses 0.01 \times 50 = 0.5 GB of memory. So, we are precisely using half of the available resources. We could argue that then the block limit could be doubled, so 200 units instead of 100. However, that is not possible because someone can craft a block with 200 OP_M’s that will lead to a memory usage of 2GB, thus going above the resource limit. This is the reason why the max is better - it aligns the block validity condition with the actual resource usage each each block.

---

**Xiawpohr** (2025-07-29):

Thanks for the clarification. I understand the concept much better. Let me continue with your example to compare the two block fullness definitions. Assuming we only price legitimate blocks with valid resource usage r_i < L \forall i \in \{1,2\}, validators cannot craft blocks that exceed resource limits.

- Definition A: Replace gas_usage with gas_metered in the gas fee update function
- Definition B: Double the block limit in the gas fee update function

| Gas cost by resource (r_1, r_2) | Def. A | Def. B |
| --- | --- | --- |
| (50, 50) | Half full | Half full |
| (0, 100) | Full | Half full |
| (100, 100) | Full | Full |

When the gas cost by resource is (50, 50), block utilization reaches 50% under both definitions. The key question is whether we can achieve 100% utilization using only one resource type.

I now understand your point, and both definitions seem acceptable to me. However, I’m still concerned that Definition A might create attack vectors for fee manipulation.

![](https://ethresear.ch/user_avatar/ethresear.ch/misilva73/48/16215_2.png) misilva73:

> from the perspective of the block builder/proposer, it would be more advantageous to reduce the base fee instead of increasing, no? That way they could collect more priority fees.

In my view, normal users typically don’t pay priority fees when the base fee is decreasing, since this indicates the block still has substantial available space. MEV users may pay higher priority fees for better transaction positioning when base fee reduces. I’d be interested to see any analysis or research that supports this argument.

---

**misilva73** (2025-07-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/xiawpohr/48/19361_2.png) Xiawpohr:

> In my view, normal users typically don’t pay priority fees when the base fee is decreasing, since this indicates the block still has substantial available space. MEV users may pay higher priority fees for better transaction positioning when base fee reduces. I’d be interested to see any analysis or research that supports this argument.

This is an interesting point. There could be three scenarios possible for the relationship between priority fees and the change in base fee: 1) they are positively correlated, 2) they are negatively correlated, and 3) they are not correlated.  In 1) the builder would have incentives to decrease the base fee. In 2) they would have an incentive to increase the base fee. And in 3), there are no incentives for the builder to manipulate the base fee.

We should be able to look at this relationship empirically. I haven’t seen data on this yet, but it should be quite simple to compute. Can you think of any other analysis that would make sense to do?

---

**Xiawpohr** (2025-08-01):

In theory, the priority fee market operates independently from the base fee market. However, in term of analyzing priority fees, several questions are worth exploring:

- What percentage of transactions in a block pay priority fees?
- What types of users pay priority fees? Are they normal users, MEV searchers, or other categories?
- Under what circumstances do users choose to pay priority fees?

We should also examine factors beyond priority fees. For instance, if we make it easier for blocks to reach the gas limit while still having available block space, would this incentivize builders to drive base fees up or become lazy about bundling additional transactions?


*(1 more replies not shown)*
