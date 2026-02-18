---
source: ethresearch
topic_id: 8377
title: Optimal gas fee transaction algorithm
author: kladkogex
date: "2020-12-16"
category: Economics
tags: []
url: https://ethresear.ch/t/optimal-gas-fee-transaction-algorithm/8377
views: 1226
likes: 0
posts_count: 3
---

# Optimal gas fee transaction algorithm

We recently have been having lots of problems reliably submitting transactions to the main net.

Some of them hang for a long time even if the gas price is high.

So I have come up with an algorithm to fix this. It works as follows:

- a client submits a transaction, initially with a low gas fee
- 30 seconds later if the transaction is not mined, it is resubmitted with the same nonce a little larger gas price
- and so on

The idea is that instead of initially starting with high gas price, or bumping the price by a lot, you keep resubmitting it with a slightly larger gas price, until it gets mined. By doing this you naturally find the optimal gas price.

Potentially this saves LOTS of money, if, say, implemented in Metamask.

Note that the entire sequence of transactions (say a hundred) can be signed at once, so only one human confirmation is neded.

## Replies

**OisinKyne** (2020-12-16):

You should checkout any.sender, https://www.anydot.dev/

Recently acquired by Infura, it works by gradually escalating fees in a manner similar to what you have described.

---

**kladkogex** (2020-12-16):

Vow! Thanks! Will check out!

