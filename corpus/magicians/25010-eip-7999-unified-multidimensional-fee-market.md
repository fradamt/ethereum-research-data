---
source: magicians
topic_id: 25010
title: "EIP-7999: Unified multidimensional fee market"
author: aelowsson
date: "2025-08-04"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7999-unified-multidimensional-fee-market/25010
views: 637
likes: 5
posts_count: 5
---

# EIP-7999: Unified multidimensional fee market

Discussion topic for [EIP-7999](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7999.md); [PR](https://github.com/ethereum/EIPs/pull/10100); [Web](https://eips.ethereum.org/EIPS/eip-7999).

#### Description

Let transactions specify one aggregate `max_fee` budget for all resources, unify fee markets, normalize gas, and generalize EIP-7918.

#### Relevant resources

- Vitalik Buterin’s research posts from 2022 and 2024. EIP-7706 which is a precursor to the proposed design.
- Multidimensional gas metering by Maria Inês Silva and Davide Crapis.
- Maria Inês Silva’s research post on gas repricing in multiple dimensions.
- A commit for EIP-7742 in an unmerged pull request, which uses a rather similar gas normalization as proposed in this EIP.

*Thanks for feedback to Maria Inês Silva, Toni Wahrstätter, Julian Ma, Davide Crapis, Barnabé Monnot, and Francesco D’amato.*

### Abstract

A unified multidimensional fee market is introduced, where each transaction specifies the maximum amount of ETH it is willing to pay for inclusion using a single `max_fee`. Upon inclusion, the protocol ensures that the transaction is able to pay the gas for all dimensions, treating the `max_fee` as fungible across resources. This enables a more efficient use of capital, and enshrines the same representation that users have when they interact with Ethereum. The fee market is further unified in terms of a single update fraction under a single fee update mechanism, generalized reserve pricing, and a gas normalization that retains current percentage ranges while keeping the price stable whenever a gas limit changes. Calldata is proposed as the first resource to be added, with avenues for facilitating gas fungibility for EVM resources considered for further expansion.

## Replies

**0xnagu** (2025-08-12):

Super interesting. Thank you.

I have several clarifying questions to understand this better (apologies for my ignorance). But let’s start with 2 or 3 clarifying questions:

1.

In the metering-only design, users still pay by the **sum** of resource usage $\sum_i r_i$, but block validity and the 1559 update key off **`max(r_i)`**. A rational builder seeking to maximize fees will optimize sum, not the max.

Suppose in two-resource land we alternate between blocks shaped as (A=18M,B=18M) vs (A=36M,B≈0), each with the same sum. The latter can raise basefee more than the former, or, conversely, a builder might bias packs to keep the measured max at/under target while still harvesting large sum priority fees.

How can you make sure (a proof or empirical evidence) that basefee burn stays aligned with total resource usage under adversarial packing, i.e., that proposers cannot keep basefee artificially low while extracting higher sum of priority fees?

What simulation results would convince us this isn’t a practical issue?

What mitigation strategies are practical here without increasing complexity of the implementation?

1.

With a single `max_fee`, the protocol only requires $F \ge \sum_i b_i \ell_i$, and the realized fee is $\sum_i b_i g_i + \text{priority}$, refunding the rest. This removes vector-cap failures (good), but it also concentrates a **single headroom pot** per tx equal to `max_fee – basefee_cost`.

Builders may have stronger incentives to order or bundle transactions to consume more of that headroom as **priority fee**, increasing tip volatility or MEV rent.

Is there an equilibrium or agent-based model quantifying the expected share of headroom that becomes tip vs refund under realistic builder policies? Any simple bounds you can derive from the historic data?

What mitigations are on the table if this is significant issue?

1. In the hybrid model for EVM gas, what are the security implications of having two different gas models operating simultaneously within the same block?

I think the disconnect between **how fees are priced (`sum`)** and **how congestion is measured (`max`)** is the central vulnerability here.

---

**aelowsson** (2025-08-12):

Thank you for your questions.

Question 1.

This question is best directed to the authors of [Multidimensional Gas Metering](https://ethresear.ch/t/a-practical-proposal-for-multidimensional-gas-metering/22668). Maria has an answer to a similar question [here](https://ethresear.ch/t/a-practical-proposal-for-multidimensional-gas-metering/22668/12), which provides clarity.

Question 2.

Builders cannot arbitrarily turn refunds into priority fees. The priority fee a builder can receive is capped by the user’s declared `max_priority_fee_per_gas` multiplied by the transaction’s actual gas used across tipped resources. It is also capped by whatever headroom remains under the user’s `max_fee`. Happy to take a look if there is a counter-example.

Question 3.

In the hybrid EVM gas approach, each transaction is processed according to the model applicable to the specified limit(s). Transactions are processed sequentially. The difference is a higher initial deduction from the sender, and a corresponding higher refund. EVM processing uses the applicable model as well (must track both aggregate and separate limits). Legacy gas-capped subcalls forward a proportional share of each remaining budget, as described in the subsection “EVM without gas observability”.  Two separate models can indeed lead to some additional complexity.

---

**0xnagu** (2025-08-16):

Thanks, Anders.

I agree on the absolute cap: builders can’t arbitrarily convert refunds into tips.

My worry is subtler: pooled headroom changes **when** the tip clamp binds. With vector budgets, per-dim misallocation often clamps tips; with pooled headroom, the same aggregate buffer can fund tips across tipped resources more often, shifting refunds → tips.

Do you have any data (or think of any) on **clamp-rate** and **realized tip share** (status quo vs 7999 with some wallet buffers)?

On the hybrid model, I’d love to learn more about a few crisp invariants: (1) behavior of legacy `gasleft()`/gas-capped patterns under proportional forwarding, (2) determinism/rounding rules so mixed-model blocks can’t diverge across clients, and (3) a bound on capacity lost due to the conservative pre-check expansion of single limits to all dimensions (plus mitigations, or Option-1 invalidation rates under PBS).

I agree this is workable but it has sharp edges.

---

**sbacha** (2025-08-17):

Implementation complexity grows with transaction types:

```auto
C(n) = O(n × t × m)
```

Complexity where:

• `n` = number of transactions

• `t` = number of transaction types (5 in Osaka)

• `m` = number of gas markets (2 post-Cancun)

A new fee market necessitates a new transaction type, any additional fee markets would thereby create new additional transaction types, shouldn’t this be a more abstract transaction type to envelope extensions down the line rather than having to make a new transaction type for additional improvements?

e.g.: Access Lists are already going to be made unviable for almost all use cases in the future, making that transaction type pretty much moribund.

