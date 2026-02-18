---
source: magicians
topic_id: 25694
title: "EIP-8037: State Creation Gas Cost Increase"
author: misilva73
date: "2025-10-07"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8037-state-creation-gas-cost-increase/25694
views: 453
likes: 7
posts_count: 21
---

# EIP-8037: State Creation Gas Cost Increase

Discussion topic for [EIP-8037](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8037.md); [Web](https://eips.ethereum.org/EIPS/eip-8037);

#### Abstract

This proposal increases the cost of state creation operations, thus avoiding excessive state growth under increased block gas limits. It sets a unit cost per new state byte that targets an average state growth of 60 GiB per year at a block gas limit of 300M gas units and an average gas utilization for state growth of 30%. Contract deployments get a 10x cost increase while new accounts get a 8.5x increase. Deployments of duplicated do not pay deposit costs. To avoid limiting the maximum contract size that can be deployed, it also introduces an independent metering for code deposit costs.

## Replies

**weiihann** (2025-10-10):

The “code exists” check is just the EL clients checking in their data store—there’s no global Merkle proof for “this code hash exists somewhere.” Therefore, we need another mechanism of storing all unique code hashes, which in itself is a separate EIP.

Regarding the duplicate bytecode discount in the same block, it’s unfair for the first deployment (see the full [pros and cons](https://ethereum-magicians.org/t/not-all-state-is-equal/25508#p-62266-cheaper-deployment-for-bytecodes-that-already-exist-13)) so I’d prefer the system contracts method.

---

**misilva73** (2025-10-10):

> we need another mechanism of storing all unique code hashes

Good point. If we need to add a new structure to provide this discount, then the overhead is much higher than I originally thought. Curious what [@CPerezz](/u/cperezz) thinks of this? I am thinking that maybe we should have the discount on a EIP of its own. That way we connect the new structure with introducing the discount.

> I’d prefer the system contracts method.

To clarify, do you mean the `LIBCREATE` opcode you suggested in your analysis?

---

**weiihann** (2025-10-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/misilva73/48/15295_2.png) misilva73:

> I am thinking that maybe we should have the discount on a EIP of its own.

Agree.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/misilva73/48/15295_2.png) misilva73:

> To clarify, do you mean the LIBCREATE opcode you suggested in your analysis?

I meant the “global codehash registry”. Basically a system contract that stores all code hashes in its storage.

---

**CPerezz** (2025-10-14):

Short update.

We discussed with [@gballet](/u/gballet) and [@weiihann](/u/weiihann) and the core issue identified is:

- Full-sync clients do have code that doesn’t pertain to any account. (SELFDESTRUCTed or reorg-ed after deployment)
- Snap-sync clients don’t serve these legacy codes as they aren’t part of any account. So new snap-sync nodes don’t have this code in their DBs.

We could track down all bytecodes that aren’t tight to an account and re-deploy them. On this way, all clients would agree on whether code exists or not.

The problem as noted by [@gballet](/u/gballet) is that if we deploy and then hit a reorg, we fall into this issue again even without SELFDESTRUCT. The issue is that once we revert, we undo all state changes. **But since contract bytecodes aren’t part of the state, clients aren’t rolling them back and removing them from the DB**. Thus, new snap-synced clients and old ones would diverge on what code exists/doesn’t.

Therefore, if we can’t find a good solution for this later point, we might find ourselves forced to go system-contract or to have a root for codes (both solutions being quite undesirable).

If we can’t find a better approach, we will need to revisit this.

EDIT:

We could use Access Lists. And if you provide the address which holds the codehash of the bytecode you want to deploy, you get the discount. Nevertheless, even these services are provided: [Ethereum Smart Contract Search](https://etherscan.io/searchcontract) and while you aren’t prevented to deploy bytecode (you just pay more), this solution might be undesirable.

---

**wjmelements** (2025-10-23):

`GAS_SELF_DESTRUCT_NEW_ACCOUNT` is not really a distinct parameter from `GAS_NEW_ACCOUNT` in the current spec. They might be different parameters in node implementations only because they were different previously, but that was a bug and now it is fixed.

---

**misilva73** (2025-10-24):

Good point. Will update the EIP

---

**aelowsson** (2025-11-02):

Consider incorporating the idea of a dynamic state price proposed by Łukasz Rozmej [here](https://github.com/ethereum/EIPs/pull/10667), after reaching out to him. It can be folded into the existing EIP by setting a `BASE_GAS_LIMIT` and a corresponding `COST_PER_STATE_BYTE_BASE` at that limit. In this example, I set `BASE_GAS_LIMIT = 60_000_000` as a likely gas limit in an important phase of implementing this EIP.

```python
# Baselines
BASE_GAS_LIMIT           = 60_000_000
COST_PER_STATE_BYTE_BASE = 380          # Gas per state byte at BASE_GAS_LIMIT

# Per-block state byte price (could be computed in a dedicated function)
state_byte_price = COST_PER_STATE_BYTE_BASE * block.gas_limit // BASE_GAS_LIMIT

# Per-block "constants" used by this EIP (only fixed within the block)
GAS_CREATE             = 112 * state_byte_price
GAS_CODE_DEPOSIT       =       state_byte_price
GAS_NEW_ACCOUNT        = 112 * state_byte_price
GAS_STORAGE_SET        =  32 * state_byte_price
PER_EMPTY_ACCOUNT_COST = 112 * state_byte_price
PER_AUTH_BASE_COST     =  23 * state_byte_price
```

This will ensure a smoother transition for developers and users, allowing them to adapt patterns over time to the relative increase in the price of state.

---

**aelowsson** (2025-11-02):

After going back and forth and realizing how easy it is to get lost, this is what I think are the core principles to consider:

We cannot guarantee some specific state expansion just by altering gas costs. For one, we do not know the price-elasticity of demand for state creation. We can easily imagine users not being particularly sensitive to the increased state gas costs, continuing to purchase state relative to other resources similar to present usage patterns. That means two things:

1. State growth is not guaranteed to be contained by the increase in its gas cost, but it will help. We should not be surprised by an increase in state growth, even if we scale gas costs linearly with the increase in the gas limit. It is also not impossible that state growth falls.
2. We may under equilibrium see well over 50% of all consumed gas being spent on state, which obviously is an impediment to scaling under the current one-dimensional fee market.

To address this in a fully satisfying manner, we need a multidimensional fee market, expanding on something like EIP-7999. However, EIP-8011 would also be very useful in the short-term.

---

**aelowsson** (2025-11-03):

I wrote an [EIP](https://github.com/ethereum/EIPs/pull/10689) now to address these concerns, please have a look.

1. To confidently target some specific state growth, the protocol tracks state_bytes_used each block (applying the EIP-8037 harmonization) and keeps a running counter of excess_state_bytes. When state_bytes_used exceeds the target, excess_state_bytes increases, and an EIP-4844 mechanism is applied to increase the gas charged per state byte. This allows us to precisely target a specific state growth.
2. To not impede scaling when a higher gas is charged per state byte, it is necessary to exempt state gas from the block gas limit. This is achieved by tracking the regular_gas_used and state_gas_used separately, counting only regular_gas_used against the limit.

---

**misilva73** (2025-11-03):

I have been thinking about the question of controlling state growth and its price elasticity, and I am not sure that dynamic pricing will have a greater impact than direct repricing.

The relative use of state-creation operations vs. burst operations (i.e., pure compute, data, etc.) can only meaningfully change by two mechanisms:

1. Users choose to use different DApps with different breakdowns of gas usage.
2. Developers build new DApps or upgrade their already popular DApps to a new gas usage breakdown.

Without any of these changes, an increase in state creation costs will not serve as a virtual limit on the other resources - i.e., we will see less of the same transactions, without more gas being used for burst resources relative to state creation.

On point 1, we can observe this empirically, as users’ reaction times should be faster. I did a quick empirical analysis [here](https://github.com/misilva73/evm-gas-repricings/blob/main/notebooks/0.4-state_price_elasticity.ipynb) to measure price elasticity and measure a small but positive relationship:

- When the base fee in USD increases by 1%, we experience a ~0.09% drop in the net state created per total gas used.
- And a 1% increase in the base fee in USD is associated with a total 0.6% decrease in the new state created by the total gas used accumulated over the following days.

Spam contracts are also part of this first mechanism, with users using them only when it is economically feasible. So, it is not surprising to observe such elasticity empirically.

Both a dynamic price and a one-time reprice should affect this mechanism. In both cases, state creation becomes more expensive as throughput increases, so we should see users switching the types of DApps they use. The main differences between the fixed and the dynamic price changes are:

- The fixed price is a one-time shock and thus is more likely to induce immediate behavioral changes. However, it needs to be carefully tuned to hit the right price. So, it is harder to do it correctly.
- The dynamic price adjusts based on users’ behavior, making it much simpler to get right. The risk of under- or overshooting is lower. However, it is also less likely to prompt immediate change among users, and prices are dynamic (sometimes they are cheaper).

Now, point 2 is trickier. Having developer change their DApps takes time, and the shock needs to be significant enough. However, if we exclude spam contracts, this mechanism has the largest long-term impact. Here, it is even harder to estimate empirically as the effects take longer to materialise. I haven’t done the analysis yet, but we could observe the effects of EIP-2929. Still, on this mechanism, I expect that a significant one-time price change will have a bigger impact than a dynamic price. Developers will be much more aware of such a big one-time change and more likely to do something about it.

So, the TL;DR is that the dynamic price seems less risky, as we don’t need to pick a price increase. The natural use of state-creation operations will make the controller increase the price accordingly. However, by not doing a significant price change, and thus not “shocking” the system, it will likely have a softer impact on state growth.

I would like to know your view on this, Anders. Am I missing something in my rationale?

---

**misilva73** (2025-11-03):

I read your design and I agree that if we want to implement a dynamic price, then this design looks great! We would need more analysis on the parameters, but I like the mechanism. I also like that we get a separate block limit for state creation gas vs. the other resources.

The question is whether we want to do a dynamic price or a fixed price. Curious on your thoughts here.

---

**aelowsson** (2025-11-03):

Thanks, yes I think we can frame it as there being two fundamental models. The gas cost can be (A) set by developers or it can (B) adapt with usage to achieve some specific state growth.

A. The fixed EIP-8037 change and the “dynamic” version that adapts with the block gas limit are fairly similar, with the gas cost set by developers. Adapting the cost with the gas limit offers a smoother transition and scales relative to how much gas is available, but still incorporates some specific gas cost regardless of actual state creation.  The outcome can be an increase or decrease in state growth, depending on the price-elasticity of demand and how much the gas limit is scaled. As you mention, the fixed adjustment will have a stronger initial effect in reducing state creation. We could also simply tune the initial effect and the smooth increase to our liking, with whatever curve is preferred.

B. The version that adapts with state creation will see the price adjust until state creation converges at the set desired target. State creation can become very expensive at first relative to the cost of other operations until usage patterns change. A simple pattern is opting to use an existing ETH address instead of creating a new one for each CEX withdrawal, etc. The effect on the gas cost will thus be “as strong as it needs to be”.

We can examine the limits of EIP-8037 by considering the outcome if usage patterns do not change. Of course, as you also illustrate, we can suspect some change in usage. But say for example that the increase in the gas limit is associated with a general drop in the base fee, such that although state creation becomes relatively more expensive than other operations, users do not take notice to the extent that we desire.

Assume we have 30% spent on state gas at 60M gas limit, producing 124 GiB in state growth per year (350 Mib/day). We then scale the L1 by `5x` up to a 300M gas limit and increase the gas cost for state creation by `8.5x`, while usage patterns do not change. The equilibrium outcome is then that `100 * 0.3 * 8.5 / (0.3 * 8.5 + 0.7) = 78.5%` of all gas is spent on state. Even though we scaled the gas limit by `5x`, the real achieved scaling is only `5 * (1 - 0.785) / 0.7 = 1.54x`, and we would be producing 191 GiB in state growth per year (538 Mib/day).

This was an extreme example that I just wanted to highlight in order to illustrate a general effect that we might see but to a lesser extent. If we end up with a realistic 50% spent on state gas we would see a real scaling of `5 * (1 - 0.5) / 0.7 = 3.57x` (focusing here only on non-state operations), producing 122 GiB in state growth per year (343 MiB/day). Note there is a slight discrepancy relative to the state growth specified in EIP-8037 at 300M gas due to the assumption here that 30% spent on state gas at 60M gas limit produces 124 GiB in state growth per year.

Exempting state from the gas limit would produce a guaranteed `7.14x` in scaling (for non-state operations). This seems important for a scaling fork. Adapting the price with state creation would produce a guaranteed fixed state growth (at whatever level we specify).

---

**misilva73** (2025-11-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> Exempting state from the gas limit would produce a guaranteed 7.14x in scaling (for non-state operations). This seems important for a scaling fork. Adapting the price with state creation would produce a guaranteed fixed state growth (at whatever level we specify).

This is a good argument. And I agree that we can set the initial cost per byte higher than the current value in order to garantee a faster convergence to the target state growth level.

---

**ryley-o** (2025-11-05):

Hello! I’m here mostly to learn. For transparency, I’m an Ethereum app developer working on high-quality NFT projects that store metadata directly on-chain to ensure provenance and long-term availability.

I absolutely support what’s best for the network, and I understand that managing state growth is essential. However, the proposed increases in storage costs — roughly 10x for SSTORE-style immutable blob storage and 3x for general slot storage — seem likely to push many applications off of L1. That feels somewhat counter to Ethereum’s broader goal of remaining a decentralized and viable platform for EVM applications.

Looking at the longer-term roadmap, there are already promising solutions (like Verkle trees and state expiry) aimed at addressing state growth more sustainably and potentially improving UX along the way.

My questions are:

- How important is it to this team to minimize large fluctuations in gas costs and protocol complexity in the short term, versus focusing on the roadmap items that address state growth more directly?
- Does the team consider immutable, blob-style data (e.g., contract bytecode) fundamentally different from mutable slot storage — both under current conditions and in a post-Verkle, state-expiry world?
- Should those differences influence current pricing proposals, especially to avoid discouraging legitimate on-chain use cases during this transition period?

I’m mostly here to learn and understand the reasoning, but I wanted to share this perspective from an app developer’s point of view. Thanks for the thoughtful work you’re doing on this!

---

**misilva73** (2025-11-19):

Here is an analysis on possible state growth scenarios under higher throughput regimes and the impact of repricings: [State growth scenarios and the impact of repricings - Economics - Ethereum Research](https://ethresear.ch/t/state-growth-scenarios-and-the-impact-of-repricings/23476)

---

**Helkomine** (2025-12-21):

Does increasing the price per byte of contract code affect the deployment of some large contracts such as Uniswap Pool v2 and v3? Such a contract would cost at least 2M gas; if this proposal is approved, it would be 19M, while eip-7825 limits it to approximately 16.8M, which would cause implementation to fail.

---

**duncancmt** (2026-01-05):

Echoing [@Helkomine](/u/helkomine) regarding the poor interaction between this EIP and 7825: under this EIP, it’s not anywhere *close* to possible to deploy a max-size (24KiB) contract under the 7825/7987 limit. The EIP-170 contract size limit already significantly constrains what dApp developers can build on-chain (see the discussion around EIP-7907), so further reducing that limit via this EIP would be a net negative for the ecosystem.

---

**Helkomine** (2026-01-05):

Actually, I’m not against raising fees, but it should also come with an expansion of the gas limit per transaction. At the very least, we should allow for the designation of transactions with larger gas limits, as suggested here : [EIP-TBA: Increasing Transaction Gas Limit with a New Fee Calculation Rule](https://ethereum-magicians.org/t/eip-tba-increasing-transaction-gas-limit-with-a-new-fee-calculation-rule/27249)

---

**DanielVF** (2026-01-08):

EIP-8037 currently attempts to target a **linear** per year increase in storage state. However, for all of computing’s history, we’ve seen an **exponential** decrease in the cost of storage.

I think over just five years, this could get a bit out of step with the actual underlying cost structure, and then exponentially get worse from there.

---

**Helkomine** (2026-01-09):

The fee structure will be redesigned to reflect actual storage costs over time.

