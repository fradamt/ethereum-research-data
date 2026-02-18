---
source: ethresearch
topic_id: 6594
title: Batch transactions settlement embedded in EVM
author: szhygulin
date: "2019-12-06"
category: EVM
tags: []
url: https://ethresear.ch/t/batch-transactions-settlement-embedded-in-evm/6594
views: 1237
likes: 0
posts_count: 1
---

# Batch transactions settlement embedded in EVM

Hello, community,

It is quite clear that the discrete nature of transaction processing in EVM makes it harder to design “fair” continuous-time paradigm DeFi tools, as thoroughly studied [here](https://arxiv.org/abs/1904.05234). Batch settlement market design sounds like a [solution](https://faculty.chicagobooth.edu/eric.budish/research/HFT-FrequentBatchAuctions-ImplementationDetails.pdf)

Is there any research/work on implementing batch smart contracts calls natively embedded in EVM?

By batch smart contract calls I mean the following: all SC calls within a block are considered to be the inputs to a single SC execution process, which treats all inputs as equal regardless of their position in the block.
