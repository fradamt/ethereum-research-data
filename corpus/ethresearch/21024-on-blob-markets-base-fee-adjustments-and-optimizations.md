---
source: ethresearch
topic_id: 21024
title: On Blob Markets, Base Fee Adjustments and Optimizations
author: Nero_eth
date: "2024-11-18"
category: Sharding
tags: [data-availability, rollup]
url: https://ethresear.ch/t/on-blob-markets-base-fee-adjustments-and-optimizations/21024
views: 1224
likes: 19
posts_count: 5
---

# On Blob Markets, Base Fee Adjustments and Optimizations

# On Blob Markets, Base Fee Adjustments and Optimizations

> Special thanks to Ansgar, Barnabé, Alex, Georgios, Roman and Dankrad for their input and discussions, as well as Bert, Gajinder and Max for their efforts on this topic!

**The tl;dr:**

All the suggested updates make sense in theory. Should we do them in Pectra - depends.

1. Raising the min blob fee allows faster price discovery.
2. Automating the blob gas update fraction makes it future-proof.
3. Normalizing the excess gas prevents an edge gas where the blob base fee drops after a fork that increases the target, though, nothing bad can happen if we don’t do it.
4. Making the base fee scaling symmetric ensures the mechanism stays as-is (scales \pm 12.5% at the extremes of 0 and 6 blobs)

---

**I would propose to summarize all those changes in [EIP-7762](https://github.com/ethereum/EIPs/blob/16a12dcf41251c592f74042b6aa5727097f60167/EIPS%2Feip-7762.md) and ship them together when we change the target/max from 3/6 to 4/6. If we’re afraid that Pectra might grow too big with adding yet more changes, I’d propose them in the following order with decreasing importance:**

1. Increase blob count.
a) Do 4/6, being conservative, or something like 6/9 if we feel more confident.
b) Ship EIP-7623 to ensure the EL payload size is significantly reduced to make room for more blobs.
2. Ship the outlined base fee changes.

---

### Recap of the Blob Fee Mechanism

With the launch of [EIP-4844](https://github.com/ethereum/EIPs/blob/16a12dcf41251c592f74042b6aa5727097f60167/EIPS%2Feip-4844.md), Ethereum added a new dimension to its fee market. Blobs, coming with their own base fee, provide dedicated space for data, allowing applications and rollups to post information on-chain without requiring EVM execution.

The blob fee structure is governed by a base fee update rule, which approximates the formula:

```python
base_fee_per_blob_gas = MIN_BASE_FEE_PER_BLOB_GAS * e**(excess_blob_gas / BLOB_BASE_FEE_UPDATE_FRACTION)
```

In this equation, `excess_blob_gas` represents the total surplus of blob gas usage compared to the target amount (`TARGET_BLOB_GAS_PER_BLOCK` per block). Like the [EIP-1559](https://github.com/ethereum/EIPs/blob/16a12dcf41251c592f74042b6aa5727097f60167/EIPS%2Feip-1559.md) fee mechanism, this formula is self-adjusting: as the excess blob gas increases, the `base_fee_per_blob_gas` rises exponentially, which discourages excessive usage and nudges the excess back toward a level at which rollups perceive the base fee as a “fair” price.

The process operates as follows: if block `N` consumes `X` blob gas, then in block `N+1`, the `excess_blob_gas` increases by `X - TARGET_BLOB_GAS_PER_BLOCK`. Consequently, the `base_fee_per_blob_gas` for block `N+1` adjusts by a factor of `e**((X - TARGET_BLOB_GAS_PER_BLOCK) / BLOB_BASE_FEE_UPDATE_FRACTION)`.

The parameter `BLOB_BASE_FEE_UPDATE_FRACTION` controls the maximum possible rate of change for the blob base fee. This rate is set to achieve a target maximum increase and decrease of approximately `1.125` per block, based on `e**(TARGET_BLOB_GAS_PER_BLOCK / BLOB_BASE_FEE_UPDATE_FRACTION)`.

In the initial rollout, blob prices were expected to be low, with gradual increases until the market finds an equilibrium or “fair” price (i.e., price discovery). The blob fee market introduced by EIP-[4844](https://github.com/ethereum/EIPs/blob/16a12dcf41251c592f74042b6aa5727097f60167/EIPS%2Feip-4844.md) follows a structure similar to [EIP-1559](https://github.com/ethereum/EIPs/blob/16a12dcf41251c592f74042b6aa5727097f60167/EIPS%2Feip-1559.md), with a base fee that adjusts dynamically based on demand.

#### Reaching the Point of “Price Discovery”

As of November 2024, Ethereum has reached a level of demand where rollups would stop posting blobs no matter what the base fee is, but instead post an amount of blobs that keeps the base fee quite stable. People like calling that a phase of “price discovery”, even though it just means that at that specific point in time a certain base fee X is regarded as a fair price. At the time of “price discovery”, rollups would no longer consistently post 6 blobs per block without considering the blob base fee, as it is no longer negligible. However, an increasing demand for blobs without an increasing supply (i.e. more blobs available) will lead to higher blob fees. For the following, forgive me when using this simplified concept of “price discovery,” even though prices are discovered every 12 seconds with every slot.

## Proposed Adjustments, and their Pros & Cons

Looking ahead to the upcoming Pectra fork, there is a clear demand for scaling blobs (from 3/6 to 4/6 or, more sophisticated, 6/9), which could necessitate adjustments to the blob fee market.

In the following sections, I will outline 4 potential changes to the blob fee market and discuss the associated benefits and challenges for each.

1. Adjusting the Minimum Base Fee: One of the simplest adjustments is to modify the MIN_BASE_FEE parameter, as suggested by Max Resnick.
2. Automating Blob Base Fee Update Fraction: A simple change to ensure the blob base fee update fraction scales with the target number of blobs.
3. Normalization of Excess Gas: Another proposal from Bert Kellerman and Gajinder suggests “normalizing” the calculation for excess gas usage.
4. Symmetrizing the Base Fee Updates: A proposal to adjust the base fee formula.

---

## 1. Increase MIN_BASE_FEE_PER_BLOB_GAS ()

The blob base fee starts at 0 and then slowly increases until the point of price discovery. Every ~6 blocks (with 6 blobs) the base fee doubles but it’s a long way to go from 1 wei to a price that is more reasonable, like, for example, 5 gwei. Until we’re at that level, the price may fluctuate a lot and rollups basically get “overly” cheap DA.

[![Screenshot from 2024-11-07 05-33-46](https://ethresear.ch/uploads/default/optimized/3X/0/e/0e1ac5c0a500f95aea3f6eca8114744eae97c7aa_2_690x324.png)Screenshot from 2024-11-07 05-33-46925×435 35.5 KB](https://ethresear.ch/uploads/default/0e1ac5c0a500f95aea3f6eca8114744eae97c7aa)

The mentioned EIP proposes to increase the minimum base fee from 1 wei to ~0.034 gwei. This would shorten the time until price discovery and thus quicker pushes rollups towards a more stable price range that is considered “fair”.

For the base fee to climb from 1 to 5 gwei, it takes…

\frac{\ln\left(\frac{\text{base_fee_target}}{\text{base_fee_start}}\right)}{\text{growth_rate}} = \frac{\ln(5 \times 10^9 / 1)}{0.117} \approx 190 \text{ blocks} and all of those blocks need to have 6 blobs. This equals to approx. 38 minutes.

With the new, increased `MIN_BASE_FEE_PER_BLOB_GAS`, we would lower this duration to…

\frac{\ln(5 \times 10^9 / 2^{25})}{0.117} \approx  \text{42 blocks}, equaling 8.4 minutes.

[![Screenshot from 2024-11-07 05-41-23](https://ethresear.ch/uploads/default/optimized/3X/4/1/417b2a602b0027c374bb9ba5aa1277a3e91fc684_2_690x324.png)Screenshot from 2024-11-07 05-41-23925×435 33.3 KB](https://ethresear.ch/uploads/default/417b2a602b0027c374bb9ba5aa1277a3e91fc684)

**One highly important caveat/implementation detail:**

**We MUST reset the excess gas when updating the `MIN_BASE_FEE_PER_BLOB_GAS`**.

The reason for that is that otherwise we would see an unpredictable, extreme spike in the blob base fee right after the fork. This is because the min base fee acts as a multiplier to the base fee and a small adjustment to it can greatly impact the base fee if the excess gas accumulated until that point is not reset.

Here’s an example of that: A apparently “meaningless” increase from 1 to 5 wei is enough to make the base fee skyrocketing and then, rollups would have to wait for a certain period of time until the price calms down again.

[![Screenshot from 2024-11-08 11-05-08](https://ethresear.ch/uploads/default/optimized/3X/8/8/8871037f542b273f175a81102502555816cc4f65_2_690x305.png)Screenshot from 2024-11-08 11-05-08970×429 27.5 KB](https://ethresear.ch/uploads/default/8871037f542b273f175a81102502555816cc4f65)

### Summarizing

#### Pros:

- Faster “price discovery”.
- Less volatility in times of supply

#### Cons

- Another potential “micro-optimization”.

---

### Symmetrizing Blob Base Fee Updates around the Target

With changing the target such that target=\frac{max}{2} doesn’t hold anymore, we change the distance from the target to the min/max. E.g., going to a blob target of 4 and a max of 6, there is room for 2 blobs up and 4 blobs down.

[![blob-target-max](https://ethresear.ch/uploads/default/original/3X/1/6/16bbe3da3a37a6134fe4878c7771e8aaff4dd555.png)blob-target-max380×216 5.59 KB](https://ethresear.ch/uploads/default/16bbe3da3a37a6134fe4878c7771e8aaff4dd555)

Now, with more room on the negative side than on the positive side, the base fee can move down faster than it can move up.

[![base_fee_symmetry](https://ethresear.ch/uploads/default/optimized/3X/4/c/4ced4a84d32f81d3705402822fa4e527fdda158b_2_404x500.png)base_fee_symmetry843×1043 36 KB](https://ethresear.ch/uploads/default/4ced4a84d32f81d3705402822fa4e527fdda158b)

A simple fix to this is the following:

We first determine the delta between the gas used and the target (same as we do now). Then we apply a scaling factor that is simply `target/(max-target)` to the side that has **less** “room” (e.g., the “up” side when doing 4/6 target/max).

The `calc_excess_blob_gas` function would look like the following:

```python
def calc_excess_blob_gas(parent_header: Header) -> int:
    scaling_factor = TARGET_BLOB_GAS_PER_BLOCK / (MAX_BLOB_GAS_PER_BLOCK - TARGET_BLOB_GAS_PER_BLOCK)
    blob_gas_delta = parent_header.blob_gas_used - TARGET_BLOB_GAS_PER_BLOCK
    if blob_gas_delta > 0:
        scaled_delta = blob_gas_delta * scaling_factor
    else:
        scaled_delta = blob_gas_delta
    excess_blob_gas = max(0, parent_header.excess_blob_gas + scaled_delta)
    return excess_blob_gas
```

Of course, this only works in cases where max-target<target and one could generalize it even more, but I’d guess it’s not worth it.

To better understand the effects of this symmetrizing process, let’s walk through a simple example:

1. Imagine we have three slots:

The first two slots contain 6 blobs each.
2. The last slot contains 0 blobs.
3. This results in a total of 12 blobs across the 3 slots.
4. The target is set to 4 blobs per block, with a maximum of 6 blobs.

#### Symmetric vs. Non-Symmetric Base Fee Adjustments:

- Symmetric Base Fee:

The base fee increases by approximately 12.5% twice (for the two 6-blob slots) and then decreases by 12.5% once (for the 0-blob slot).
- After these adjustments, the base fee ends up higher than its initial value.

**Non-Symmetric Base Fee**:

- The base fee remains unchanged after the 6-6-0 blob sequence.

This example highlights the benefits of a symmetric adjustment:

- The 6-6-0 blob sequence pushes us toward extremes (max utilization followed by none), which is undesirable.
- Ideally, the load should be more evenly distributed across the three slots (e.g., 4 blobs in each block).
- A symmetric base fee discourages extreme behavior by “penalizing” uneven usage (6 blobs instead of 4) more with a higher base fee, promoting a more balanced load.
- Of course, one could argue that blob users might not care about pushing the base fee up because they might only need to post blobs a few times in every epoch and therefore don’t care about the slot following their 6-blob posting. Though, this argument is short-sighted.

### Summarizing

#### Pros

- Ensure “price discovery” happens as fast as it does now.
- Ensure the “extremes” (0 and 6 blobs) cause the same percentage increases/decreases.

#### Cons

- Yet another “micro-optimization” and everything might be fine without doing it.
- Introducing some path dependency. E.g. jumping between gas\_used= target \pm 1\ blobs causes the base fee to increase steadily over time. This behavior can be counteracted by avoiding posting more blobs than the target, which may even incentivize a more balanced posting strategy.

## Replies

**joeykrug** (2025-03-15):

Whatever happened to this? These seem like good ideas, particularly the symmetric fee adjustment one. I think it’d be quite bad if it’s asymmetric in a way where it causes fees to drop significantly more than the market’s willingness to pay.

Also are there any thoughts at some point allowing stakers / validators to signal for a given blob target & blob maximum, similar to how they can for the general block gas limit?

Why not also cross post this to ethereum magicians? I checked there and there seem to be basically no post about the blob market issues. It seems like this should be an EIP

---

**Nero_eth** (2025-03-16):

These ideas were mainly shared to inform everyone about various topics discussed during ACD when the blob throughput increase was discussed to be included into Pectra.

The asymmetry with the 6/9 led us to update the final update fraction to **5,007,716**, getting a better balance between asymmetry and minimizing path dependency.

For more details, see:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/176a0ca418757e78a1ca9133bbe82b6d90b3546c/EIPS/eip-7691.md)





####

  [176a0ca41](https://github.com/ethereum/EIPs/blob/176a0ca418757e78a1ca9133bbe82b6d90b3546c/EIPS/eip-7691.md)



```md
---
eip: 7691
title: Blob throughput increase
description: Increase the number of blobs to reach a new target and max of 6 and 9 blobs per block respectively
author: Parithosh Jayanthi (@parithosh), Toni Wahrstätter (@nerolation), Sam Calder-Mason (@samcm), Andrew Davis (@savid), Ansgar Dietrichs (@adietrichs)
discussions-to: https://ethereum-magicians.org/t/eip-7691-blob-throughput-increase/19694
status: Last Call
last-call-deadline: 2025-04-01
type: Standards Track
category: Core
created: 2024-04-17
---

## Abstract

Increases the number of blobs in a block to provide more scale to Ethereum via L2 solution that rely on L1 data capacity.

## Motivation

Ethereum, with its rollup centric roadmap, scales by relying on L2. Since the Dencun fork, the blob gas target and maximum was set to 3/6 respectively. The blob gas limit was arrived at based on a series of big block tests performed on the Ethereum mainnet network as well as a series of testnets. The values were chosen cautiously, as it's extremely hard to predict the exact p2p behaviour of Ethereum mainnet.
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/176a0ca418757e78a1ca9133bbe82b6d90b3546c/EIPS/eip-7691.md)










Other proposals, such as the **minimum blob base fee**, were rejected due to a lack of demand from their primary users—L2s.

---

**joeykrug** (2025-03-16):

While it makes sense that the minimum blob base fee proposal was rejected due to lack of demand from L2s and that the fee market is pricing blobs above what that minimum fee would be, I believe we should reconsider including symmetric fee adjustments in a future hard fork.

The current asymmetric adjustment mechanism in the eip above allows fees to drop more rapidly than they rise, which could lead to inefficient market behavior over time. As demonstrated in the examples with the 6-6-0 blob distribution pattern, asymmetric adjustments can result in suboptimal resource allocation, more volatility in blob usage, possibly an underpricing of blob gas, and other issues outlined here https://ethresear.ch/t/the-target-demand-paradox-in-the-blob-fee-market-an-analysis-of-eip-4844-eip-7961/

It’s important to recognize that L2s aren’t the only relevant stakeholders here, and their incentives are naturally aligned with mechanisms that systematically result in lower fees. Of course they would favor asymmetric fee adjustments that allow fees to drop more quickly - they’re the primary fee payers! But we need to consider the entire ecosystem’s health, including validators, network security, and long-term sustainability beyond just the interest of L2s.

As outlined in your OP summarizing the discussion on it, symmetric fee adjustments would:

1. Create more predictable fee behavior for all participants
2. Discourage extreme utilization patterns
3. Promote more balanced blob usage across blocks
4. Prevent excessive fee oscillation that hurts the network’s economic stability

Even if L2s aren’t demanding this feature, implementing symmetric adjustments would create a more sustainable fee market that benefits the entire ecosystem long-term. Sometimes the most important protocol improvements aren’t the ones most loudly requested, but those that create foundational stability and address concerns from the broader ETH community.

What do people think about reviving the symmetric fee adjustment proposal in a future update?​​​​​​​​​​​​​​​​

---

**Nero_eth** (2025-03-17):

I agree. I was also a fan of making basefee updates symmetric around the target, but it seems the priorities have shifted. For Fusaka, the scope is nearly frozen, though this change is small enough to qualify as a negligible EIP and could still be included later on—especially since we need to adjust both the blob count and the basefee update fraction anyway. You can see the idea detailed in this PR, where I’ve already proposed it in an EIP:


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [GitHub](https://github.com/ethereum/EIPs/compare/master...nerolation:EIPs:blob-gas-mechanism-split)



    ![](https://ethresear.ch/uploads/default/optimized/3X/4/c/4c5ab6ffc20d0513b2288e9df9dce93bfb3c0f23_2_690x345.png)

###



The Ethereum Improvement Proposal repository. Contribute to ethereum/EIPs development by creating an account on GitHub.

