---
source: ethresearch
topic_id: 19356
title: Reducing latency games by levelling the playing field on block size for PBS
author: antonydenyer
date: "2024-04-23"
category: Proof-of-Stake > Block proposer
tags: [mev]
url: https://ethresear.ch/t/reducing-latency-games-by-levelling-the-playing-field-on-block-size-for-pbs/19356
views: 4502
likes: 13
posts_count: 14
---

# Reducing latency games by levelling the playing field on block size for PBS

*Thanks to [@simbro](/u/simbro) for reviewing*

## Abstract

For this post, block size refers to the number of serialised bytes in a block. Currently, the average block size is over 100k [Ethereum Average Block Size Chart | Etherscan](https://etherscan.io/chart/blocksize). Note that we are talking about bytes, not gas limit.

Every block builder is motivated to submit a block to the PBS auction as late as possible. The more time a block builder has, the more time they have to accumulate transactions and, therefore, priority fees. For the purpose of this discussion, we assume no MEV is at play.

## Discrete Blocks and Latency Games

Apologies if this is old news, but it’s worth reiterating. The role of a block builder is multifaceted and requires proficiency in several infrastructure tasks.

1. Block builders must be able to access transactions; solo validators often miss out on priority fees because they are not well connected to the public mempool. A block builder with good connectivity to the mempool will likely win more blocks. They may even partner with wallets and other transaction originators to fast-track mempool transactions into their builder pipeline.
2. They must have good networking connectivity with the auctioneer, aka relay. The lower the latency between them and the auctioneer, the more time they have to build blocks.
3. Because the block builder is privileged, they can offer value-added features that no other entity can offer. Namely, revert protection through eth_sendBundle. The builder who can build a block the fastest whilst protecting private order flow from reverts will win more blocks (once again, we assume no mev).

Because blocks are discrete periods, pressure is applied to all parts of the stack towards the end of the block. Consequently, a block builder will do what it can to increase the amount of time it has to focus on its core activity, building the most profitable block.

## Observations

Block builders will likely submit multiple bids using multiple strategies. Sometimes, the bids for smaller blocks are received in time, while those for larger blocks are not. This is simply because larger blocks are slower. Consequently, transactions that could be included in a block are not being picked up.

## Hypothetical Scenario

A block builder has 100 transactions in their local mempool, totalling 0.5 eth in priority fees. The network is silent, and no other transactions are entering the mempool. The block builder submits the block (block a) to the auction. Near the very end of the block, another transaction enters the mempool with a whopping 1 eth in priority fees. The block builder now submits two more bids at the same time.

block b - containing our single juicy priority fee transaction for 1 eth.

block c - containing 101 transactions with all the transactions we have totalling 1.5 eth.

Both bids are now higher than the previous bid. One of three scenarios now stands:

1. The original bid wins as neither subsequent bid was reached in time by the auction before the deadline.
block_a_wins668×379 29.2 KB
2. The small block reaches the auction before the deadline, pushing out the previously submitted block of 100 transactions.
block_b_wins668×379 30.2 KB
3. The big block reaches in time, and all transactions are included.
block_c_wins668×379 30 KB

It is easy to imagine an interplay between latency, block size and priority fees that are entirely opaque to users and sophisticated actors.

## Real-world example

JetBuilder built [Ethereum Blocks #19598122 | Etherscan](https://etherscan.io/block/19598122) and only used 12% of the block space available, paying ~0.15 eth for the block. We observed them missing at least 40 transactions that could have been included in that block. The example transactions were in the mempool for at least five blocks (thanks to https://www.ethernow.xyz). They all landed on-chain in either the next block or the one after.

[block_19598122_missed.txt](/uploads/short-url/m28oil5kIiAPgjrYROY42OBPcYX.txt) (4.2 KB)

# Proposal

We should have some floor usage in gas terms to prevent transactions from bullying other transactions out of a block.

The gas floor target could be calculated in many ways, such as a predefined fixed target, half the gas limit, or a dynamic adjustment based on previous consumption (similar to 1559). It doesn’t need to be elegant or exact; it just needs to be something to incentivise block builders to utilise block space.

The penalty for not ‘filling’ the block would be something like `gas target missed * base fee`. This is the same price as putting a transaction in the block, except the block builder doesn’t get priority fees. Theoretically, a block builder could make a transaction with themselves, but the result is the same.

We are simply putting a price on what the network perceives as the underutilisation of block space.

## Replies

**tripoli** (2024-05-02):

This is a really interesting block and situation. I threw together some quick charts for anyone that doesn’t have the MEV auction data at their fingertips.

[![mev-bids-slot-8799985](https://ethresear.ch/uploads/default/optimized/3X/a/f/affedbc9ccf001dd75e2637aff0c3a736a74a537_2_690x373.png)mev-bids-slot-87999851800×975 76.8 KB](https://ethresear.ch/uploads/default/affedbc9ccf001dd75e2637aff0c3a736a74a537)

[![gas-used-slot-8799985](https://ethresear.ch/uploads/default/optimized/3X/f/9/f9610a288c2c7fc70bb99d3248069cae44bc0cc4_2_690x373.png)gas-used-slot-87999851800×975 73.8 KB](https://ethresear.ch/uploads/default/f9610a288c2c7fc70bb99d3248069cae44bc0cc4)

[![transactions-slot-8799985](https://ethresear.ch/uploads/default/optimized/3X/5/8/58003e9b53618ee8649afc3bfd05456f4664cc0e_2_690x373.png)transactions-slot-87999851800×975 72.2 KB](https://ethresear.ch/uploads/default/58003e9b53618ee8649afc3bfd05456f4664cc0e)

I like the idea of this proposal. It adds complexity, but it might be a more robust and efficient way of implementing missed slot penalties if we decide to go down that road.

Some questions off the top of my head:

- What are the incidence rates of blocks where the winning bid uses far less gas than the rest of MEV bids?
- Do non-boost blocks use less than 15 million gas on average? Does this further incentivize MEV-Boost usage?
- What’s the best way to measure this? Against MEV bids is a bad idea because of XOF, would we want a pseudo-oracle similar to the MEV-burn proposals?
- Who should pay the penalty? Right now the protocol can only charge the proposer, so would we need to change the MEV bid scoring spec or does it make sense to adopt a change like this with ePBS?

---

**umbnat92** (2024-05-03):

It’s an interesting topic. However, we previously studied this effect (full research [here](https://arxiv.org/pdf/2312.09654), ethresear.ch summary [here](https://ethresear.ch/t/the-cost-of-artificial-latency-in-the-pbs-context/17847)) and we found that is not that frequent a builder propose a bid with less than 10M gas. See figure below for reference.

[![bid_value_vs_gas_vs_eligibility](https://ethresear.ch/uploads/default/optimized/3X/4/b/4b28ecec33582d6fd6d868f33bf27d5761ad1f19_2_690x345.png)bid_value_vs_gas_vs_eligibility1600×800 123 KB](https://ethresear.ch/uploads/default/4b28ecec33582d6fd6d868f33bf27d5761ad1f19)

---

**antonydenyer** (2024-05-03):

I’m approaching this from a wallet perspective. We’ve been trying to understand why our transactions sometimes don’t get included. While I agree that, on average, it’s not that bad, from a single user experience, it can be greatly degraded. We’ve observed multiple occasions when valid transactions are not being included for multiple blocks in a row, in some cases more than ten blocks.

Here’s the data I have for the last month. It’s all the transactions we’ve seen in the public mempool with a view as to whether we think that transaction is valid or not for that block. The assumption here is that we’ve seen it for at least a full block. If we get a transaction anywhere in block 101, we ignore it - but we assume that everyone has got it by the end of block 102. So we’re probably underestimating the problem by quite a lot.

Here’s what we’ve observed in the last month:

Over 400 blocks have been built with less than 10M gas and have had at least 2 valid pending transactions (the count is not 100% accurate, but it’s enough to give an idea).

Of these, over 50 blocks have had more than 10 transactions ignored.

[block_transactions_raw.txt](/uploads/short-url/yRaA4cwBIF7kF10ZNKFXArtyD78.txt) (3.2 MB)

[block_transactions_summary.txt](/uploads/short-url/h0BAcAcdBgFVR1MfrVJRFBbHTRY.txt) (99.1 KB)

---

**umbnat92** (2024-05-03):

Would be interesting to see what was the gas used for previous slot (like a scatter plot where you have on x-axis the gas used for the 400 blocks you mentioned, and on y-axis the gas used in previous slot). Eventually extending this for base gas fee.

Further, it could be great if you can share these 2 valid pending txs

---

**antonydenyer** (2024-05-03):

Thanks for the stats; they’re fantastic. It’s really interesting to see that chasm in gas use and price! We don’t have easy access to this data ![:pray:](https://ethresear.ch/images/emoji/facebook_messenger/pray.png?v=14)

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> Do non-boost blocks use less than 15 million gas on average? Does this further incentivize MEV-Boost usage?

Or do solo validators miss more transactions than blockbuilders?

If some form of the gas floor was introduced, non-me boost validators may be impacted because they are not filling the block as much as they should. Clearly, these validators are not profit-maximising. Otherwise, they would use mev-boost, so we must assume they have motivations other than profit for participating.

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> Who should pay the penalty? Right now the protocol can only charge the proposer, so would we need to change the MEV bid scoring spec or does it make sense to adopt a change like this with ePBS?

It should come from the proposer. Given the following options:

Option A: 1eth priority fee 15M gas

Option B: 1.1eth priority fee 5M gas

I want option A to be chosen. I think the only way to do that is to change the priority fee rewards. But given we can not know things without trusted parties, oracles, etc etc, I think the best thing to use is the previous blocks gas used. Whilst it won’t be perfect I think it’s good enough.

---

**antonydenyer** (2024-05-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/umbnat92/48/9019_2.png) umbnat92:

> Would be interesting to see what was the gas used for previous slot (like a scatter plot where you have on x-axis the gas used for the 400 blocks you mentioned, and on y-axis the gas used in previous slot). Eventually extending this for base gas fee.

We’ve seen scenarios where a single block builder is dominant for multiple blocks in a row, with a slowly increasing gas usage. Take a look at it and walk forward!


      ![](https://ethresear.ch/uploads/default/original/3X/4/b/4b321b0cbf91834c9cc6f2f96362b232970fc1cd.png)

      [Ethereum (ETH) Blockchain Explorer](https://etherscan.io/block/19115589)



    ![](https://ethresear.ch/uploads/default/optimized/3X/3/1/313e33395bfe3ba3b18c0625e2d78ce6cc403989_2_690x345.jpeg)

###



Ethereum Block Height 19115589. The timestamp, block reward, difficulty, gas used and the number of transactions in the block are detailed on Etherscan.










![](https://ethresear.ch/user_avatar/ethresear.ch/umbnat92/48/9019_2.png) umbnat92:

> Further, it could be great if you can share these 2 valid pending txs

It’s in here:

![](https://ethresear.ch/user_avatar/ethresear.ch/antonydenyer/48/20160_2.png) antonydenyer:

> block_transactions_raw.txt (3.2 MB)

block_number - the block at which the transactions were valid

hash - the tx hash

Note the hash may appear multiple times across different blocks.

---

**umbnat92** (2024-05-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/antonydenyer/48/20160_2.png) antonydenyer:

> We’ve seen scenarios where a single block builder is dominant for multiple blocks in a row, with a slowly increasing gas usage. Take a look at it and walk forward!
>
>
> https://etherscan.io/block/19115589

But that could be that BF from pending txs was not enough to be included in the block. Indeed you see that the gas used increases up to the maximum possible value, after decreasing in block [19115599](https://etherscan.io/block/19115599), that should be a “standard” dynamic when there is network congestion. That is, builders saturate the block with txs with high BF+PF first, when activity goes down and there is scarcity of txs that can be included in the block with such high BF, they lower the gas used to decrease BF in the next slot and start to include txs again.

---

**umbnat92** (2024-05-03):

But that’s different from what happened in slot 19598122 (depicted by plots shared by [@tripoli](/u/tripoli)).

But this kind of scenarios (like the one described in your case 2) are really rare, especially since validators are playing timing games and as you can see from plots of the auction dynamic the bids proposed few hundred of ms later were higher

---

**tripoli** (2024-05-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/antonydenyer/48/20160_2.png) antonydenyer:

> block_transactions_raw.txt (3.2 MB)

I’ve only done a random sample, but these seem to overwhelmingly be blob transactions, so I think these stats significantly overstate the issue. Any chance you can add a transaction type column or filter blobs out?

![](https://ethresear.ch/user_avatar/ethresear.ch/antonydenyer/48/20160_2.png) antonydenyer:

> If some form of the gas floor was introduced, non-me boost validators may be impacted because they are not filling the block as much as they should. Clearly, these validators are not profit-maximising.

It turns out MEV-Boost blocks use significantly more gas than locally built blocks (especially since February of this year), so any gas floor would have second order effects on decentralization/censorship resistance etc.

[![dune-gas-by-type](https://ethresear.ch/uploads/default/optimized/3X/0/7/07fb5caad1586a133b72b256d97c7cf32090acd9_2_690x304.png)dune-gas-by-type2833×1251 230 KB](https://ethresear.ch/uploads/default/07fb5caad1586a133b72b256d97c7cf32090acd9)

---

**antonydenyer** (2024-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/umbnat92/48/9019_2.png) umbnat92:

> But this kind of scenarios (like the one described in your case 2) are really rare, especially since validators are playing timing games and as you can see from plots of the auction dynamic the bids proposed few hundred of ms later were higher

They are not rare. We regularly see transactions that are not included when they could be. In the first scenario, the spread of gas consumption is wide and obvious, which makes it easy to discuss.

In the second example, the same thing is happening, but it’s more subtle. Valid transactions (with a high enough base fee) are waiting in the mempool for multiple blocks. A block is ‘flushed’ when a tipping point occurs between mev, priority fee, and block size (kb). This also means that a user may experience an incredibly long inclusion latency.

---

**antonydenyer** (2024-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> I’ve only done a random sample, but these seem to overwhelmingly be blob transactions, so I think these stats significantly overstate the issue. Any chance you can add a transaction type column or filter blobs out?

Much of it has just been lost, but you’re right; the majority are type 3 transactions.

[transactions_with_type.txt](/uploads/short-url/3vCZF83nNsudV9sJhuBzCXj3XIb.txt) (3.2 MB)

I’ve updated the code I use to monitor the mempool to include it, so going forward, we should have complete data.

---

**antonydenyer** (2024-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> It turns out MEV-Boost blocks use significantly more gas than locally built blocks (especially since February of this year), so any gas floor would have second order effects on decentralization/censorship resistance etc.

I agree; they are already forfeiting not only mev rewards but also publicly available priority fee rewards (just because they do not have a fast internet connection). I could see a situation where ‘aligned’ solo validators may delegate block building to a non-censoring, non-mev relay, which doesn’t currently exist.

I think the second-order effects of censorship resistance could be positive. Currently, there is almost zero financial incentive for a block builder to take a stand on these matters.

---

**antonydenyer** (2024-05-16):

An alternative to monetary incentives could be to introduce some kind of VDF.

Emptier blocks should require some kind of VDF to make them valid, which would be proportional to their emptiness. There would be no monetary disincentive to send an empty block; however, you’d be making it slower to produce, putting it on a level playing field with the full block.

