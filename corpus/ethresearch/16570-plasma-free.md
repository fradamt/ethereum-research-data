---
source: ethresearch
topic_id: 16570
title: "**Plasma Free**"
author: barryWhiteHat
date: "2023-09-07"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-free/16570
views: 5965
likes: 16
posts_count: 9
---

# **Plasma Free**

Thanks [CC](https://github.com/ChihChengLiang) for review and feedback.

## Intro

Rollups are scaling ethereum. But the cost of rollups is still very high for many use cases. For example at the time of writing a cost of 0.02 USD was typical on l2. This is way too expensive for many use cases where users need to have transaction fees of ~0. For example OPCraft (another example is dark forest) a version of Minecraft where every operation is carried out on chain. Even after 4844 and all of data sharding has been completed its unlikely that data costs will be low enough to allow 0 cost transactions.

In this post we propose Plasma Free that supports EVM,  can run any evm contract, and has a gas fee (only prover cost ~0) that is independent of l1. The only cost is prover cost.

## Plasma

Plasma started as an attempt to solve two problems.

1. Data Availability
2. Execution Validity

After recent work that solves validity (zkevm’s) we revisit plasma and see what is possible if we have just one problem to solve.

## Plasma assumptions

Plasma assumes:

- Users watch online to see if data is unavailable
- If so they exit from an old state
- Users watch online to make sure each transaction is correct

Can we use the same assumptions and build a zkevm based system that allows us to not put data on chain ?

## Plasma Free

A block producer gets transactions from users and makes blocks. They publish each block header and a proof of validity on chain but not the data. They are supposed to share the data with all users.

If they share the data everything is fine. If they don’t share the data

- User places a forced transaction in the forced transaction que.
- If the forced transaction que is not cleared by the block producer during the forced transaction window the latest block is reverted.
- keep reverting until the forced tx que gets cleared.
- Continue from that point.

The fact that users need to make a forced transaction when data is unavailable means that they need to come on line once during the forced transaction window. This is the key difference between rollups. The users online assumption. With zk rollup users don’t need to be online, with optimistic rollup only a single honest user needs to be online. With plasma Free all users need to come online once per forced transaction window (E.g. 1 week) in the case of an attack so that they can exit.

The system depends on users being able to execute forced transactions. These transactions should only happen very rarely. The cost of such a transaction should be the same as a typical rollup transaction. So we have free transactions until data becomes unavailable and then we have the same costs as l2s.

## Forced transactions

A plasma free forced transaction is very similar to an l2 forced transaction. It is an ethereum transaction singed by the user who wants to exit. Forced transactions can be batched in the same way that l2 transactions are batched. This is how our forced transaction cost can have the same cost as l2 transactions.

## Conclusion

Here we introduced plasma free. This is not an l2 and not as good as an l2s. The users online assumption is a big pain point. But for some use cases this can be acceptable. An implementation of this using an already existing zkevm should be relatively easy to build with hopefully minimal zk components that need to be built.

## Replies

**adompeldorius** (2023-09-07):

How can users exit if the operator shuts down? Especially if they need to perform several transaction on the rollup in order to withdraw.

---

**barryWhiteHat** (2023-09-07):

If this happens they state keeps rolling back until another user has all the data and they are able to help the users exit.

---

**adompeldorius** (2023-09-07):

I see. This design seems similar to [Minimal fully generalized S*ARK-based plasma](https://ethresear.ch/t/minimal-fully-generalized-s-ark-based-plasma/5580).

---

**norswap** (2023-09-10):

Hey! Cool post, here are a few thoughts.

Mostly, I’m wondering if this compares favorably with existing or proposed DAC solutions. I’m thinking of what MetisDAO (data availability challenges) in particular.

It seems like a data availability challenge can be used to require the data to be posted on L1, at cost to the requester. This means, the sequencer can grief users by not posting the data, but can always be forced to release it (or the state roots will be invalidated). The opposite (sequencer eating the request costs) is worse, as this enables permissionless griefing.

Still, for this to be useful, it requires a mechanism to punish griefing sequencers. This could be up to some form of governance. Rollups today do require governance for upgrades anyway. An abuse of governance here only leads to the removal of an honest sequencer, so the negative consequences are pretty limited. cf. to Jon Charbonneau’s writing on “Proof of Governance” for more thoughts around this

Ultimately, social consensus is unavoidable. In enshrined rollups, the power of removing sequencers could be given to validators via some in-protocol mechanism (since they have the power to hardfork anyway to achieve the same thing).

To me that seems easier and more realistic than requiring every users to come online during a given window.

Socially speaking, the recent Starknet mainnet upgrade that deprecated some type of accounts (locking funds) caused a massive backlash despite Starkware communicating about it for months.

The requirement for users to come online can only lead to people entrusting a third-party to exit for them, and so the behaviour and incentives of this new actor should be mapped out in any such proposal.

---

**neozaru** (2023-09-10):

This reminds me of StarkEx Validium for some reason.

I think the forced transaction on Validium carries a gas burn loop to have it cost more gas, in order to avoid having users abusing it.

Not sure how it impacts your model if the forced tx costs a lot of gas. I guess it opens a bit more leverage for a malicious operator.

---

**qbig** (2023-10-09):

A problem for free transactions (also issues with cheap gas L1/L2), how to deal with spams?

---

**leohio** (2024-04-19):

To summarise the concept, it’s “Rollback instead of Rollup if a DA problem.”

The way to maximize the usage of forced tx queue is really interesting, since forced tx queue was just an idea to prevent a censorship in Rollups.

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> This is not an l2 and not as good as an l2s.

Basically, this can not be a strictly speaking L2 because the storage on L1 is limited, right?

If we can assume infinite storage resources to place all L2 transactions in Plasma on the L1 storage, people can confirm the subjective finality of their transactions (there is no rollback) after they check both the entire history of L2 and the forced transaction queue on L1. However, the storage resources on L1 are actually limited, so data availability for someone cannot be found just by checking the forced transaction queue.

Considering whether it is possible to relax the online requirement so that a user without a full node does not have to fully trust someone else. As you know, it is not possible to create a validity proof of not withholding with respect to DA, but it is possible to create a validity proof of having some of it. Would this help?

[![無題のプレゼンテーション (1)](https://ethresear.ch/uploads/default/optimized/3X/c/f/cff4cfc18ab5e64d7e2c345992b2f7bd708baf59_2_517x291.jpeg)無題のプレゼンテーション (1)960×540 10.9 KB](https://ethresear.ch/uploads/default/cff4cfc18ab5e64d7e2c345992b2f7bd708baf59)

I think that statelessness, offline safety, and capital efficiency are the trilemma in L2 architecture. This system is stateless (constant state growth ignoring user growth) and has full capital efficiency, but is also EVM compatible, so it seems very much on the trade-off.

---

**nuno** (2024-06-09):

Hi, thank you for the very exciting post!

I have a few questions.

> keep reverting until the forced tx queue gets cleared.

I understand that if all forced tx queues are not processed as L2 blocks within a certain period (let’s call it the revert window), the current state root will be reverted.

- I believe that the revert window does not necessarily need to match the forced transaction window. For rapid rollbacks, would it be acceptable to shorten this period to about one hour for the revert window?
- Is my understanding correct that, if no one processes the forced tx queue, it could potentially revert all the way back to the genesis block? However, since finality is necessary for withdrawals, we need to set an upper limit on reverts. If L2 reverts up to that limit, the revert window becomes infinite.

