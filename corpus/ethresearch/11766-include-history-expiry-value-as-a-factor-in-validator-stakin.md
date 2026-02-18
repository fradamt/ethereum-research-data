---
source: ethresearch
topic_id: 11766
title: Include history expiry value as a factor in validator staking rewards?
author: basememara
date: "2022-01-13"
category: Economics
tags: []
url: https://ethresear.ch/t/include-history-expiry-value-as-a-factor-in-validator-staking-rewards/11766
views: 1283
likes: 0
posts_count: 2
---

# Include history expiry value as a factor in validator staking rewards?

I’ve been setting up my node validator on testnet and while waiting for a week for the entire blockchain to download on this machine I thought about maybe there’s a better way.

To me, if a validator even has one day of transaction data then it should have enough safe data to securely validate blocks. Is this a valid assumption or make sense?

What if we include the amount of historical data that your validator holds as a factor that increases your staking rewards. So if my validator only has a week of history, my staking rewards would be less but also less opportunity for my validator to fulfill requests that are older than one week so it will be less busy.

However, if I choose to download the whole blockchain then I can fulfill requests for transactions that involve any date range. And therefore will be more be more busy but also incentivize to store large amounts of historical data with increased staking rewards.

The most important thing this does though in my eyes is that it lets anyone participate to secure the network from day 1 and also space is not a concern to participate anymore.

I’m sure I’m missing many things and context but sharing in case this makes sense. Any thoughts or feedback would be greatly appreciated!

## Replies

**MicahZoltu** (2022-01-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/basememara/48/8507_2.png) basememara:

> What if we include the amount of historical data that your validator holds as a factor that increases your staking rewards.

Proving this is a *really hard* problem.

![](https://ethresear.ch/user_avatar/ethresear.ch/basememara/48/8507_2.png) basememara:

> To me, if a validator even has one day of transaction data then it should have enough safe data to securely validate blocks. Is this a valid assumption or make sense?

You are correct, history is not strictly needed by any individual in the network, it just avoids us needing a schelling point for what “latest” is.  Look into the discussion on history expiry (sometimes called regenesis) or EIP-4444 where we are talking about removing ancient history from the core protocol.

