---
source: ethresearch
topic_id: 9216
title: What is gas cost for update operation in Ethereum?
author: ChenZhongPu
date: "2021-04-18"
category: Mining
tags: []
url: https://ethresear.ch/t/what-is-gas-cost-for-update-operation-in-ethereum/9216
views: 991
likes: 0
posts_count: 1
---

# What is gas cost for update operation in Ethereum?

Recently, I have read a [ICDE paper](https://dblp.uni-trier.de/rec/conf/icde/Zhang0XTC19.html) about `Ethereum`, it states that:

> the gas cost to update a word to storage is 5,000.

But according to [Ethereum: A secure decentralised generalised transactionledger](https://gavwood.com/Paper.pdf), the gas cost of reset operation is 5,000.

> Paid for an SSTORE operation when the storage value’s zeroness remains unchanged or is set to zero.

Based on common sense, `update` is at least as hard as `store` itself. So, I think the statement of that ICDE paper is wrong. Can anyone help to figure this out?
