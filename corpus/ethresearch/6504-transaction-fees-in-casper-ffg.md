---
source: ethresearch
topic_id: 6504
title: Transaction fees in Casper FFG
author: khabanh1337
date: "2019-11-26"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/transaction-fees-in-casper-ffg/6504
views: 1550
likes: 1
posts_count: 2
---

# Transaction fees in Casper FFG

Hello everyone!

I have a question about transaction fees when Ethereum switches to Casper FFG.

Will the transaction fees stay the same in terms of gas limit and gas price?

How will transaction fees be calculated in Casper FFG?

How much will miners and validators be rewarded?

Thank you very much.

## Replies

**econoar** (2019-11-27):

Each shard will still have a gas (block) limit.

Transaction fees (at least early on) should go down dramatically. We are adding 1024x the throughout but demand won’t go up that much. Therefore, there will likely be an abundance of block space in the early days of eth2

In PoW there’s a minimum fee of sorts where below that, it’s not worth it for a miner to include a tx due to uncle risk. In PoS this risk doesn’t exist and therefore fees could get very close to 0. At least that’s what I’m expecting.

Most validator profit will come from staking rewards. You can find expectations for that [here](https://docs.ethhub.io/ethereum-roadmap/ethereum-2.0/eth-2.0-economics/)

