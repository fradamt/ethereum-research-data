---
source: magicians
topic_id: 22572
title: "EIP-7863: Block-level Warming"
author: Nerolation
date: "2025-01-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7863-block-level-warming/22572
views: 448
likes: 11
posts_count: 25
---

# EIP-7863: Block-level Warming

Discussion topic for [EIP-7863](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7863.md)

Find an initial analysis of the EIP in the following:


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 17 Jan 25](https://ethresear.ch/t/block-level-warming/21452/7)



    ![image](https://ethereum-magicians.org/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_500x500.png)



###





          Execution Layer Research






When I first considered this problem, my initial reaction was to add the access list to the block header. It would then be the proposer’s additional duty to provide the block’s access list, and the state transition function would check its...










#### Update Log

> 2025-01-16 Initial Commit

#### External Reviews

None as of 2025-01-18.

#### Outstanding Issues

2025-01-18: Clarify if block-level warming or directly move to multi-block warming

2025-01-18: Clarity warm-warm-for-all vs. one-warms-and-gets-refunded (costs distributed among transactions or accesses)

## Replies

**wjmelements** (2025-01-21):

It appears your mechanism would strongly penalize the use of transaction-level access lists. Is this intentional?

---

**Nerolation** (2025-01-22):

I disagree that its penalizing anyone.

Access list would still make sense for ToB transactions and one can also think of mechanisms as proposed in [EIP-3584: Block Access List](https://eips.ethereum.org/EIPS/eip-3584) that allow everyone from benefit from access lists.

One could also think of building probabilistic access list, putting rarely used storage slots into the access list and “hoping” that some others are already warm (e.g. because they are warm in 99% of the cases - WETH as an example).

With block-level warming there are no losers when compared to the status-quo, so “strongly penalizing” is clearly wrong.

---

**wjmelements** (2025-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> I disagree that its penalizing anyone.

Then you are wrong, and did this unintentionally, likely because you don’t understand the current mechanism. The cost for warming a slot that is already warm (or one that won’t be touched in the transaction) far exceeds the benefit of warming it for first-use, by a factor of 24 for accounts and 19 for storage.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> One could also think of building probabilistic access list, putting rarely used storage slots into the access list and “hoping” that some others are already warm

This would be the only remaining use for access lists. The probabilities here are 4.17% for accounts and 5.26% for storage. These probabilities are so low and for most users it is impossible to identify which slots will be unique to your transaction. The result is that regular users won’t use them anymore, and block builders will have an even larger advantage in MEV than they already have. It would further encourage their collusion with searchers and thereby end private orderflow.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> With block-level warming there are no losers when compared to the status-quo, so “strongly penalizing” is clearly wrong.

The mistake your are making is that you are comparing the absolute cost before and after when you should be comparing the marginal benefit before (100) and after (-2100). The losers are anyone still using access lists. Kindly admit this is a fault in your current design and find a way to fix it. I suggest making the the first instance of each block-warm entry in an access list free. This will prevent access lists from going extinct.

---

**wjmelements** (2025-01-22):

My main objection to block-level warming is that it prevents parallel execution due to the `GAS` opcode. Block transactions should be able to be executed in parallel.

---

**Nerolation** (2025-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> The probabilities here are 4.17% for accounts and 5.26% for storage.

Where do you take these probabilities from?

The EIP is still at the very beginning and access lists are being discussed. I love to see them being applied to the whole block and sharing the costs, but I think this comes with significant increased complexity compared to this rather simple change.

Access lists didn’t really take of and block level warming might just be tackling the problem, efficiency we leave on the table, from a different angle, and further iterations might come with handling them in some smarter way.

Parallelization, true, yeah. Though, I wouldn’t say it’s preventing. At most, adding some complexity. You say “should”, we both see how well those efforts are going. So the best time to do block warming was probably a few years ago.

---

**wjmelements** (2025-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> Where do you take these probabilities from?

It’s the collision probability where the expected value of including an entry in an access list is zero. If the probability is less than this, you should include it in the access list. Otherwise you should not include it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> Access lists didn’t really take of [sic]

I use them in every transaction. There are a few ways to make them better but their current design is opt-in. Theoretically block execution can warm the state earlier using these lists. Security would be a bit better if access lists were strict, because there would be restrictions on unexpected execution. Strict access lists can also make light client execution possible in combination with state proofs. I don’t want to destroy them therefore.

---

**Nerolation** (2025-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> I don’t want to destroy them therefore.

No one is saying to destroy them. There seems to be broad agreement that they are useful. However, we could explore ways to apply them at the block level and offer refunds to those who had to pay for creating the access list. This approach is more complex compared to block-level warming, which has its own challenges. But these difficulties shouldn’t stop us from making improvements in other areas.

We could also consider repricing access lists to further strengthen the incentives.

I don’t agree with the idea that this would completely ruin them. There will always be storage slots where you can be fairly certain they aren’t warmed yet—for example, checking my balance in an ERC20 token.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> wjmelements:
>
>
> The probabilities here are 4.17% for accounts and 5.26% for storage.

It’s the collision probability where the expected value of including an entry in an access list is zero. If the probability is less than this, you should include it in the access list. Otherwise you should not include it.

Do you have more details on this? What is the time frame analyzed, what data, where’s the code?

---

**wjmelements** (2025-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> Do you have more details on this? What is the time frame analyzed, what data, where’s the code?

There is no need to collect data to calculate this probability. Here is an article on how to compute the [expected value](https://simple.wikipedia.org/wiki/Expected_value).

The first step is to set up the equation I described.

> the collision probability where the expected value of including an entry in an access list is zero.

```auto
P(alreadyIncluded) * V(alreadyIncluded) + P(!alreadyIncluded) * V(!alreadyIncluded) = 0
```

The next step after setting up the algebraic equation is to plug in the marginal benefit numbers aforementioned. I will do that here using the account gas numbers, 2600 and 100.

```auto
P(alreadyIncluded) * (-2600) + P(!alreadyIncluded) * (100) = 0
```

Because these probabilities sum to one, you can solve for the probabilities that yield zero for the expected value.

```auto
P(alreadyIncluded) * (-2400) + (1 - P(alreadyIncluded)) * (100) = 0
(-2500) * P(alreadyIncluded) + 100 = 0
P(alreadyIncluded) = 1/25
```

So the probability is 1/25 (aka 1:24). I previously miscalculated it as 1/24 in haste.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> There will always be storage slots where you can be fairly certain they aren’t warmed yet—for example, checking my balance in an ERC20 token.

You would have to check hash preimages for substrings containing the sender address. It doesn’t work in the general case either; there are plenty of possible future designs because ethereum is Turing complete. I don’t think the implementers of `eth_createAccessList` are going to appreciate your change therefore. It is much simpler to implement the change I previously suggested, so that each transaction still references all of its own accesses. Users, wallets, and nodes shouldn’t have to reason about the probability of collision with earlier transactions in the block.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> However, we could explore ways to apply them at the block level and offer refunds to those who had to pay for creating the access list.

My suggestion achieves that, but I am open to other ideas.

I’d also be interested in ways for the first user touching each thing to pay the same as everyone else. Perhaps the warming gas cost could be shared somehow.

---

**Nerolation** (2025-01-23):

Ah gotcha, “so if the probability that your address is already warm >5%, you’'d not put it in there”.

One thing I was thinking of is separating access lists from transactions, and then validate them before starting execution. Invalid access lists are still included+paid for. This would allow us to handle them before execution and allow all txs to profit from warmed storage slots. Eventually, one could refund some of the costs.

---

**Nerolation** (2025-01-28):

I was thinking a bunch about this and, imo, the best thing we could do is approach the cold/warm inconsistency overy transactions from a block-level perspective.

One could think of combining all access lists at the beginning of a transaction and then splitting the costs for access list creation among the accesses.

This comes with problems like “quality of access list” vs. “quantity”, meaning, we would want to avoid having WETH in every second access list when it’s best to have it only in a single one.

Duplicates in a block are waistful.

With block-level warming, block builders might have an incentive to warm the storage slots (accounts + storage keys) for the transactions in their block using access lists. This would give them another 100 gas per first access.

Regular users might still use access lists for storage slots that they are certain that the already-warm propability is <5%.

In the end, no matter if you today use access lists or not, with block level warming you’ll never be worse off compared to today. I think it’s reasonable to compare absolute values here and let and efficient market play out the dynamics for access lists. In times of PBS, efficient block packing is outsourced in >90% of block anyway.

---

**wjmelements** (2025-01-29):

> efficient market play out the dynamics for access lists

The most efficient market is a single centralized builder-searcher determining the order of all transactions, maximizing extraction. This is not desirable, and we should not make changes that promote this behavior. Currently, searchers have a fair gas auction with builder-searchers and can occasionally win. After this change they would all be integrated.

Marginal costs do matter because they determine who wins the gas auction. You don’t care if block builders have this huge advantage over independent searchers, but eradicating independent searchers would be a huge step toward centralization. As aforementioned, the gas savings of knowing prior block accesses is 25x and 20x larger than the gas savings of the access list itself. We should not give that advantage to builders.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> Regular users might still use access lists for storage slots that they are certain that the already-warm propability is  Duplicates in a block are waistful.

Agree. But it’s likely less wasteful than having no access lists at all. And the transaction should not be penalized for what they do not know. The best way to encourage them to include it is to ensure they’re always incentivized to include it. Another reason for each transaction to have their own list is that it is beneficial for the simulation of that individual transaction.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png) Nerolation:

> In the end, no matter if you today use access lists or not, with block level warming you’ll never be worse off compared to today

Use of access lists is not a constant. You may not think inclusion is penalized in terms of the absolute change in but they are penalized in marginal terms in reference to the decision to include or not. A poor understanding of marginalism is a recurring theme of your EIPs. Marginalism explains how microeconomic decisions are made and can be used to predict the outcomes of changes in incentives. I challenge you to study marginalism before thinking of ways to fix this.

Consider the decision matrix for whether to include an account item or not.

| Decision Before | Prior Access | First Access |
| --- | --- | --- |
| Include | 100 | 100 |
| Exclude | 0 | 0 |

| Decision After | Prior Access | First Access |
| --- | --- | --- |
| Include | -2400 | 100 |
| Exclude | 0 | 0 |

It is clear that this change does penalize access lists for every user except the omniscient builder, and that the builder’s advantage is substantial. I am also concerned that a builder can manipulate the gas of a transaction by changing a first access into a prior access or vice versa, causing a transaction to fail or succeed, or to cost more or less than expected (which can matter for priority fees).

---

**shemnon** (2025-02-03):

How is this better than simply raising the gas limit 10-15%?

As a node implementor I only see more bookkeeping and accounting to do so that gas golfers can reduce their gas burnt numbers.  The amount of computational work done in a node actually goes up on a per-gas basis.  So based on that I view this as strictly worse than simply raising the gas limit.

Second, this will critically damage parallel execution efforts.  By making the gas cost dependent on the state access of all prior transactions you are making the current transaction dependent on the side effects of the entire preceeding block.  Parallel efforts depend greatly on slots having effective read locks (which can be shared) and effective write locks (which are exclusive).  Having to consider the warm state removes the effective read locks and changes everything into an effective write lock, reducing the scope across which these effective locks can be shared across the block. It also increases the mandatory bookkeeping of this data.  Prior to this we only needed to re-evaluate transactions if a prior transaction changed the value of a slot, now simply reading it causes changes to the execution semantics across transactional boundaries. USDC would be an example, where the paused field must be read but is (almost) never written to. The effective read lock now becomes effective write locks.

If there is still the desire to reduce the per-gas cost of warming a slot or account across the transaction, consider tracking who warms a block and if there are multiple warmers, at the end of the block refunding all users of the field pro-rata for the warming costs of the slot or account and updating the balances at the end of the transactional block.  Realize though, that while the effective ether cost goes down the actual computational cost goes up.  I do not think this is a net win against the alternative of just raising the block gas limit by 20%.

---

**Nerolation** (2025-02-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> How is this better than simply raising the gas limit 10-15%?

Raising the gas limit comes with more load on all dimensions while the purpose of block-level warming is more to get the storage pricing closer to realities in clients, that can cache over multiple transactions.

I agree that it’s bad for parallel execution, and maybe some form of block-level access lists (described [here](https://hackmd.io/q-d9jMeeTZa-GptrBuPmSw)) might be better than simple cumulative block-level warming, allowing clients to parallelized I/O and execution.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> If there is still the desire to reduce the per-gas cost of warming a slot or account across the transaction, consider tracking who warms a block and if there are multiple warmers, at the end of the block refunding all users of the field pro-rata for the warming costs of the slot or account and updating the balances at the end of the transactional block.

I see why such an approach sounds fairer but I fear this comes with significantly more complexity. I do agree with your concerns and think it’s a trade-off that we may want to consider carefully.

---

**petertdavies** (2025-02-04):

I agree with the scepticism above about “First Access Warms For All”. I see 4 problems with it:

1. It’s unfair to users.
2. It creates a minor form of MEV.
3. It reduces the extent to which transactions are isolated from one another. In general, the design has been to treat two transactions in the same block and two transactions in different blocks the same.
4. It creates execution dependencies between transactions with common reads. Currently, in principle, two transactions can be executed in parallel as long as neither of them reads an item that the other writes to.

I’d like to propose a different approach, where gas refunds are issued at the block level allowing the builder to include more transactions and lowering the future base fee. I think this mostly fixes those problems and should be simple to implement. Here is a formal spec:

1. At the start of each block:

Initialize two empty sets block_level_accessed_addresses and block_level_accessed_storage_keys and one counter block_gas_refund
2. Add any pre-warmed items to the sets (e.g. coinbase, precompiles)
3. For each transaction in the block:

Execution is entirely unchanged from current behaviour
4. At the end of the transaction:

Add each address in accessed_addresses (excluding pre-warmed) to block_level_accessed_addresses, if the address already present add COLD_ACCOUNT_ACCESS_COST - WARM_STORAGE_READ_COST to block_gas_refund
5. Add each storage key in accessed_storage_keys to block_level_accessed_storage_keys, it the key is already present add COLD_SLOAD_COST - WARM_STORAGE_READ_COST to block_gas_refund
6. At the end of the block:

net_gas_used = gas_used - block_gas_refund
7. Check net_gas_used <= block_gas_limit, rather than gas_used <= block_gas_limit
8. Calculate the base fee for the next block based on net_gas_used rather than gas_used

By dealing with block level access lists at the end of the transaction we avoid having to deal with interaction between them and reverts.

---

**wminshew** (2025-02-04):

I’d like to propose what I think is a simple solution: tweak gas costs for `accessLists`.

Specifically, every txn is executed as-is today. But at the `accessList` level, rather than charging X for a given address/slot, X/n is charged (where n is the number of `accessLists` with that address/slot). Afaict, this has the following properties:

1. leaves txn execution de-coupled
2. encourages accessList usage (by creating potential for more gas savings from usage)
3. end-users receive gas benefits directly
4. no weird minor MEV

Also pretty simple to code / execute from a block producer perspective (I think). Any big drawbacks I’ve missed?

---

**wjmelements** (2025-02-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wminshew/48/4658_2.png) wminshew:

> Also pretty simple to code / execute from a block producer perspective (I think). Any big drawbacks I’ve missed?

The gas and its opcode should be computable without knowing prior block accesses. So you want to structure this as a refund applied at the end of the block, to enable parallel execution.

---

**wminshew** (2025-02-11):

> The gas and its opcode should be computable without knowing prior block accesses.

I believe this is true in my proposal. Only thing that affects the gas cost in execution is whether the txn included the address / slot in its `accessList` (and not at all related to prior block access), which is already the case today and simply how `accessLists` work

---

**lu-pinto** (2025-02-12):

I would like to see some comparative measurements of MGas/s before we make any decision, between the following cases:

- Parallel transactions with block level warming,
- Parallel transactions without block level warming and
- Sequential transactions with block level warming

I agree that incentivizing access lists is a better approach than this one, it helps parallel execution rather than harming it.

---

**alex-forshtat-tbk** (2025-02-28):

Hello [@Nerolation](/u/nerolation)

We at the ERC-4337 team have proposed an EIP-7557 that aims to solve the same issue some time ago.

It didn’t go anywhere back then but there may be some value in the discussions around it, and we would be glad to collaborate on this problem.

The original topic is here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alex-forshtat-tbk/48/1453_2.png)
    [EIP-7557: Block-level Warming](https://ethereum-magicians.org/t/eip-7557-block-level-warming/16642) [EIPs](/c/eips/5)



> A mechanism for a fair distribution of the gas costs associated with access to addresses and storage slots among multiple transactions with shared items in their accessList.
>
>
> Old PR link:

A little back story, our main concern when designing this mechanism was to ensure the resulting cost savings are actually distributed fairly and not turned into another channel for MEV extraction.

The resulting design attempts to use a simplified version of Shapley values in order to redistribute the collected fees.

We also had to move the gas cost redistribution to the end of the block to simplify the block execution, instead of affecting the cost in place.

At that point we have decided to wait for the Verkle before pushing EIP-7557 any further, but it appears that this topic has become relevant again.

---

**shemnon** (2025-02-28):

The new update is a lower number, this is confusing.  I will drop my comments in the other thread.


*(4 more replies not shown)*
