---
source: ethresearch
topic_id: 973
title: Cartel formation incentive in full PoS - interest rates must rise with the total deposit size
author: nootropicat
date: "2018-02-01"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/cartel-formation-incentive-in-full-pos-interest-rates-must-rise-with-the-total-deposit-size/973
views: 2530
likes: 7
posts_count: 6
---

# Cartel formation incentive in full PoS - interest rates must rise with the total deposit size

In the Casper testnet interest rate is proportional to inverse square root of total deposits. That would be very bad for full PoS.

Changes in validator sets are transactions.

Bob is a selfish profit-optimizing validator. If Bob’s expected future return on staked eth is expected to drop due to new validators joining he’s not going to include their join transactions. Fee loss is infinitesimal under any significant adoption scenario, as he only loses the difference to the next highest gas priced transaction.

The simplest case is:

Bob is the last block generator in a period (anything from a block to epoch) that’s used to count total deposits and interest rates.

If it’s per epoch and Bob is making the last block he has a 100% chance to block new validator for at least one epoch.

If it’s per block then for at least one block.

In general Bob should censor when

> lostFeeDifference  annualRate = rateScaling * sigmoid(k * fractionOfStakedEth)

With k = 3 and rateScaling = 2.1% it goes from 1.05% rate at 0 eth staked to 1.7% rate at 50% staked; ~2% rate at 100% eth staked.

## Replies

**vbuterin** (2018-02-01):

That imposes a huge amount of risk on the network - if we measure the constants wrong, then it would be easy to accidentally hit an equilibrium where the interest rate is very low and no one participates. Also, in the long term, when transaction fees dominate there’s a de-facto return component that’s a simple inverse of total deposits, so we can’t count on the reward schedule too much.

I think it’s better to just have explicit censorship detection, a la [Censorship rejection through "suspicion scores"](https://ethresear.ch/t/censorship-rejection-through-suspicion-scores/305)

---

**clesaege** (2018-02-01):

Someone who wants to stake can put higher fees such that fee loss is not infinitesimal.

The block creator still has incentive in accepting the join TX, as if he does not, another block creator will.

This works as long as we don’t have cartels.

---

**vbuterin** (2018-02-01):

Ultimately it’s up to the users to simply reject chains that censor for too long.

---

**nootropicat** (2018-02-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> That imposes a huge amount of risk on the network - if we measure the constants wrong

Which applies to the current proposed schedule as well; all that remains is a relative comparison in which decreasing rates are likely ‘more wrong’ (is wronger a word?).

> then it would be easy to accidentally hit an equilibrium where the interest rate is very low and no one participates

**Note that if there are nearly no validators cartel formation risk (and incentive!) is at the highest.**

> Also, in the long term, when transaction fees dominate there’s a de-facto return component that’s a simple inverse of total deposits, so we can’t count on the reward schedule too much.

1. Just push the issue (inflation ending) far into the future, hope it’s solved by zk cryptography and don’t worry about it. It’s nothing compared to the fact that PoW self-destructs in an orgy of selfish mining without block rewards; at least PoS has the weak ‘I own lots of coins and don’t want their value to go down’ + the fact that as long as even a minority of active validators aren’t censoring it sort-of works.
2. Put on a reward schedule term on top of this schedule to ensure smooth transition to the inverse relationship

> I think it’s better to just have explicit censorship detection, a la Censorship rejection through “suspicion scores”

This in practice boils down to people rebelling and coordinating externally to switch to a fork; pretty much a disaster that would destroy trust in the network, as there would be zero guarantee that the situation wouldn’t repeat. Especially because the mere existence of a cartel doesn’t mean that the network stops working.

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> Someone who wants to stake can put higher fees such that fee loss is not infinitesimal.

With public amounts fees would have to be enormous, some percentage of deposit. However, this is a good argument for making confidential amounts first-class, as that would force the profit calculation to use averages.

---

**nootropicat** (2018-02-01):

What about both incentives at the same time? That would eliminate the cartel incentive completely while allowing for a decreasing rate of interest even without any inflation, just pure fees.

Accrued income (including fees) is locked proportionally to x = sigmoid(k*totalDepositFraction); locking is once per epoch.

> Epoch 1:
> earn 10 ETH, balance 10 ETH
> Epoch 2:
> earn 5 ETH, balance 5 ETH

Now you want to withdraw:

> Epoch 3:
> x = 0.6
> You can withdraw 6 ETH from epoch 1 and 3 ETH from epoch 2
> Total 9 ETH

Remaining locking periods per epoch remain. This provides a monotonically increasing incentive for existing

validators to let more validators join, preventing formation of long-term cartels.

k = 5 gives 50% at 0% staked and 92% at 50% staked.

