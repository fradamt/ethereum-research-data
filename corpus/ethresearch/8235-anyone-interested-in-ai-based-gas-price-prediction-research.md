---
source: ethresearch
topic_id: 8235
title: Anyone interested in AI-based gas price prediction research?
author: kladkogex
date: "2020-11-19"
category: Economics
tags: []
url: https://ethresear.ch/t/anyone-interested-in-ai-based-gas-price-prediction-research/8235
views: 1384
likes: 0
posts_count: 3
---

# Anyone interested in AI-based gas price prediction research?

At SKALE we have been recently facing pretty bad transaction submission problems to the main net, where transactions get stuck unpredictably even if the gas price is high.

It looks like miners routinely misbehave,  in a sense that they censor out transactions with a high gas price because of whatever optimizations their proprietary software does.  The problem is pretty bad because there are only a handful of mining pools.

We are trying to understand how to deal with it. One possibility is to get hold of the actual software that mining pools are using (I am not sure it is possible since it may be proprietary)

Another way to build an AI model that evaluates a transaction, pre-executes it in the EVM and, based on the data tries to predict whether it will get stuck or not.

I wonder if anyone else is interested in research like this, or have faced similar problems.

## Replies

**HAOYUatHZ** (2020-11-21):

Hi [@kladkogex](/u/kladkogex)

You may wanna take a look at https://www.gasnow.org/ by SparkPool, one of the largest Ethereum mining pools in China.

Most existing solutions calculate gas fees based on historical gas fee data. However, **GasNow** calculates gas fees based on pending transaction mempool.

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/7393a2a4971039f913f9ac99a784a7c558835686_2_690x272.png)image1114×440 41.9 KB](https://ethresear.ch/uploads/default/7393a2a4971039f913f9ac99a784a7c558835686)

You can find more details on their page.

---

**HAOYUatHZ** (2020-11-21):

Basically

“Rapid” is the median of (tx1, tx2, … , tx_n)

“Fast” is the max(**tx2**, … , tx_n)

Usually using “Fast” can get a tx included into the next block. (Though Strictly speaking it’s neither 100% the case if the block reaches GasLimit)

