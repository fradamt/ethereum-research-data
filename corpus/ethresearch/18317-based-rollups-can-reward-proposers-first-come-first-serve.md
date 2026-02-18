---
source: ethresearch
topic_id: 18317
title: Based Rollups can reward Proposers First Come First Serve
author: mteam88
date: "2024-01-14"
category: Layer 2
tags: [mev, rollup]
url: https://ethresear.ch/t/based-rollups-can-reward-proposers-first-come-first-serve/18317
views: 1980
likes: 9
posts_count: 3
---

# Based Rollups can reward Proposers First Come First Serve

# Based Rollups can reward Proposers first come first serve

**tl;dr**: *Based rollups don’t need a complicated auctioning system to reward proposers if they are willing to sacrifice L2 MEV rewards*

## Introduction

Before reading it is vital to understand [Based Rollups](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016), the [mev-boost](https://docs.flashbots.net/flashbots-mev-boost/introduction) block [supply chain](https://flashbots.mirror.xyz/bqCakwfQZkMsq63b50vib-nibo5eKai0QuK7m-Dsxpo), and sequencing

The inspiration for this article was a section of the [Taiko](https://taiko.xyz/) docs that mentions their system for choosing which provider to reward:

> The first proposeBlock tx in the enclosing L1 block will earn the [block] reward.
> – Proposing Taiko blocks

That sentence is followed up by this note:

> This is a temporary solution which may change soon, as we see an issue that can arise where the proposer will submit empty blocks to earn the reward.
> – Proposing Taiko blocks

**NOTE: these docs no longer exist.**

The rest of this article argues why it is unnecessary to change the first-come-first-serve (FCFS) system that is currently implemented in the Taiko testnet.

## Explanation

### Assumptions

#### L1 searchers = L2 builders = L2 proposers

All will be referred to as “L2 builders” for the remainder of this article.

This assumption is reasonable because L2 proposers will bid for inclusion in the L1 through the mev-boost system, acting as L1 searchers. L2 builders and proposers look the same to the block reward system.

#### L1 builders choose to include only the highest-paying L2 builder’s bundle

Every proposer implements a check in their contract that only pays the builder if they are the first to call proposeBlock (and therefore winning the l2 block reward.) L1 builders are then incentivized to only include the highest bidding L2 builder’s block.

#### An FCFS system rewards only the first block proposal in the L1 block.

Only the first L2 block proposed in a single enclosing L1 block wins the block reward. All subsequent block proposals are either ignored or simply not rewarded.

### Reasoning

If these assumptions are true, the proposer with the most valuable L2 block will win the L2 proposer reward.

L2 builders will compete to build the most valuable L2 block, which they will submit to L1 builders as mev-boost bundles. Whichever L2 builder outcompetes its peers will be included at the top of block by the L1 builder.

## Tradeoffs

### MEV

As in most rollup designs, a based rollup using this design will sacrifice ALL MEV rewards to its L1. Researcher [Justin Drake](https://twitter.com/drakefjustin) has stated that [this problem is not specific to based rollups.](https://twitter.com/i/spaces/1ZkKzjzlAkNKv?s=20)

Additionally, MEV rewards are expected to trend towards 0 over time as MEV-aware applications leak less and less MEV to block builders.

### Spam resistance

This is the concern of the Taiko team.

The idea is that L2 builders will propose empty (or nearly empty) blocks to earn the block reward without generating valuable blocks.

An FCFS system will resist spam because spamming L2 builders will only bid up to the value of the block reward. L2 blocks will be worth more than this because of the MEV opportunities that exist inside these L2 blocks. Legitimate (non-spamming) L2 builders will be able to outbid spamming L2 builders based on the MEV rewards that they can extract.

The Taiko team published an article on MEV in based rollups that begins to address this issue:

> L1 builders will include L2 blocks into their L1 blocks as long as there is at least a tiny of piece of MEV in this block (and the gas limit is not reached). And as long as there are any DEXs deployed on L2, there always will be some MEV additionally to transaction fees;
> – MEV for “Based Rollup”

Changing the reward that L2 builders receive based on other aspects of their blocks (transaction count, execution layer information, etc.) may also allow legitimate L2 builders to outbid spamming L2 builders if MEV rewards are negligible. Further research is required to determine these metrics. These variable block rewards only help legitimate L2 builders outbid spamming L2 builders, **they can be set up within an FCFS system.**

## Conclusion

As far as I can see, a simple FCFS system should be sufficient for Based Rollups, and no further development is required. Research into variable block rewards should be conducted to determine if MEV rewards will be enough to completely avoid spamming L2 builders earning the L2 block reward.

This article should be common sense, but I want to start a discussion on this (because I’m probably wrong lol)

## Replies

**Brecht** (2024-01-14):

Thanks for starting some discussion about this! Next to the concerns in your post, I want to highlight some other ones as well.

For an L1, putting transactions in a block is basically free. So that means that as long as a transaction pays a `fee > 0` (or can make money in another way), it can be included and be profitable. For an L2 however, this is not the case anymore because including a transaction in a block has a cost: The tx data cost, and for a zk rollup the cost to prove the execution of that transaction. So that creates a lower bound for which a proposer would ever include a tx inside an L2 block, because if the tx cannot at least pay for that, not including it will be more profitable. That means that a block reward is only helpful in getting transactions included between this `tx_data_cost + tx_proving_cost` and `tx_total_cost`, where the tx total cost also includes all the general overhead costs (transaction costs without the data part, proof verification) mostly shared between all the transactions.

So for example if there are only transactions that pay a fee below this lower bound in the mempool, an empty block will be the most profitable block to create. In which case the block reward isn’t helpful to get people’s transactions included, or keep actual proposers/provers in the game because creating and proving empty blocks is not representative to the actual work that needs to be done with blocks containing real transactions.

On the other hand, in the cases where the block reward isn’t necessary, it’s extremely likely almost the complete block reward will just be sent to the L1 validator, because only the L2 proposer/builder that pays the most to the L1 validator gets his block included, and so any “free money” to be made will have to be used to bribe the L1 validator.

So then the question arises what the point is of the block reward. The reward could help transactions get included that pay a fee  `tx_data_cost + tx_proving_cost < tx_fee_paid < tx_total_cost`, essentially subsidizing user transactions in a small range. This could be useful, for example to mitigate variations in the L1 costs (unpredictable when the user signs the L2 tx), but it seems unlikely to me that block rewards given in a based rolup would be able to play a bigger role than that.

---

**mteam88** (2024-01-15):

I see what you mean. From the proposer’s piont of view the block reward doesn’t matter because the value will always end up with the L1 validator.

I think we need to continue to explore the possibility of dynamic block rewards (maybe rewarded retroactively instead of inside the proposeBlock transaction) to encourage L2 block builders. I think it would be possible to explicitly reward block builders who include unprofitable L2 transactions, effectively subsidizing these transactions.

Let me know what you think.

