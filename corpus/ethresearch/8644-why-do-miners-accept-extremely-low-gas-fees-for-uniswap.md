---
source: ethresearch
topic_id: 8644
title: Why do miners accept extremely low gas fees for Uniswap?
author: kladkogex
date: "2021-02-08"
category: Economics
tags: []
url: https://ethresear.ch/t/why-do-miners-accept-extremely-low-gas-fees-for-uniswap/8644
views: 2633
likes: 0
posts_count: 3
---

# Why do miners accept extremely low gas fees for Uniswap?

We did some interesting experiments recently,  submitting Uniswap transactions with extremely low gas fees.

The funny thing is that transactions that were supposed to take hours if not days to accept, were accepted in a couple of minutes.

Did any one else see the same behavior and could it be related to front-running by miners?

## Replies

**nickgeoca** (2021-02-09):

That is interesting. It sounds related to one of the [dark forest blog posts](https://zengo.com/ethology-a-safari-tour-in-ethereums-dark-forest/). They said the miner buys before and sells after a large trade, where the large trade swings the price of the asset pair.

On that note, and curve finance having a different price slippage model, I wonder if the ethereum miners prefer uniswap transactions over curve finance transactions. Is it important for a swap’s success to cater to the miners?

---

**Mister-Meeseeks** (2021-02-09):

How low was the gas? Existing gas oracles don’t do a good job about predicting expected time. Was it significantly below the minimum inclusion fee on the block it was mined? (You can check by looking at the block on Etherscan and checking the next lowest priced transaction.)

If it clearly was below the minimum block inclusion fee, it’s possible the miner included it to front run. AFAIK only one major mining pool does this. UUPool, who make up about 3% of blocks mined. Check to see if front running happened. Find the block on Etherscan, then click all transactions. Check the transaction immediately before and after to see if your trade was “sandwiched”.

