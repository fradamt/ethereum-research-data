---
source: magicians
topic_id: 2314
title: Fund Lock - A Different Approach to Limit State Size
author: avihu28
date: "2019-01-02"
category: Working Groups > Ethereum 1.x Ring
tags: []
url: https://ethereum-magicians.org/t/fund-lock-a-different-approach-to-limit-state-size/2314
views: 981
likes: 6
posts_count: 4
---

# Fund Lock - A Different Approach to Limit State Size

Following a talk with [@AlexeyAkhunov](/u/alexeyakhunov)

Consider this model:

For every word stored in storage the caller must lock a fixed amount of ETH, say 0.001 ETH. When the storage being released, the caller gets this amount back, perhaps minus a small fee that get burned.

In this model, state size is limited by the total ETH supply. Moreover, as state grows it becomes more and more expensive to consume more storage. This is because consuming so much ETH to be locked in storage will become more and more expensive.

It is also easy to imagine transition from the current state to this model. There will be a grace period in which after storage that didn’t lock funds will be removed.

IMO it might be a simpler model of State Rent, supposedly still getting the goal of limiting the state size.

## Replies

**AlexeyAkhunov** (2019-01-02):

Thank you, now i have had a chance to think about it a bit more. This model is similar to what we have now with gas refunds for clearing the storage and self-destructing, with two crucial differences:

1. Locked up funds are expressed in ETH, rather than in gas, as currently, which makes the state expansion limiting effect much stronger (amount of gas that can be created is much much larger than amount of ETH that exist and can be created)
2. Current clearing refunds only work as refunds (and can only refund 1/2 of the gas expenditure of the transaction). That forces dApps combine refunds with other operation, which is not straightforward and ugly most of the time (therefore GasToken is a nice abstraction around it, but still ugly). Because it is hard to use, higher lock-ups cannot be justified. More straightforward withdrawal of locked up funds may justify higher lock up amounts.

I like this scheme, but two things needs to be worked out sufficiently:

1. Withdrawal of locked up funds - how should this work and where should the released funds go? For contracts, it can go to the contract’s balance, and then contract’s code would decide where it goes next (for example, if it is a token contract, and people have to lock up ETH in order to transfer to a fresh token holder (which will require modification of token standards), then consolidation of token holders would release some ETH, and the address that sends transaction gets that ETH. The side effect is that effectively ETH transfer is required every time when tokens are given to new addresses. In the case of self-destruction, the released ETH can simply go to the target address specified with the SELFDESTRUCT opcode.
2. What is the mechanism for locking up funds for the existing storage/accounts? Here we stumble to the similar problems as with rent - pre-existing state needs to be taxed (otherwise there will be hoarding before the change), but how? You propose to remove state after grace period, which unfortunately introduce removal of accounts and storage. If lock ups were here from the start, we would not even need to worry about it. But because we are applying this on the existing state, we will have to remove parts of it, unless someone locks up ETH for it, with all the complications inherent to the State rent. As a result, this scheme might actually become as complex (or even more complex) as the State rent.

---

**gcolvin** (2019-01-05):

I still think we worry too much about things like hoarding.  Our state is increasing exponentially; whatever the behavioral effects of the transition they will be drowned out soon enough.

---

**AlexeyAkhunov** (2019-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I still think we worry too much about things like hoarding. Our state is increasing exponentially; whatever the behavioral effects of the transition they will be drowned out soon enough.

I hear you. Hoarding is a potential problem, but there is no guarantee that it will occur on a large scale. I know that some kind of hoarding is already occurring on the current Ethereum (people running bots deploying contracts and reserving storage at a very low gas price to repackage them using transparent proxies and sell + GasTokens). If there is a way to make sure that profitable hoarding would not occur a lot, i would like to explore mitigations. We do not have many attempts to get things right, unfortunately.

There is a solution to hoarding which is to introduce “debt” for the pre-existing account and storage, and this debt needs to be payed off by subsequent modifications. A tweak in that is to introduce the debt not from the block 0, but from some DEBT_BLOCK < HARDFORK_BLOCK, where DEBT_BLOCK is a point in time where we begin time-stamping the state items, but before the state expansion becomes more expensive. That means that all the state expansion that occurred for the last 3,5 years gets a waiver.

