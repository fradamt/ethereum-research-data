---
source: ethresearch
topic_id: 9077
title: Troubles with gas estimates in EVM
author: kladkogex
date: "2021-04-02"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/troubles-with-gas-estimates-in-evm/9077
views: 1567
likes: 0
posts_count: 3
---

# Troubles with gas estimates in EVM

At SKALE we need to charge the exact cost of a particular transaction to a particular user.

The fundamental problem we need to solve is that at the very end of a Solidity transaction we need to find out exactly how much gas this transaction uses.

It turns out that simply measuring gas used as the last line in a Solidity function does not work, because there is some gas used and freed AFTER the last line when the function returns.

We would be happy to issue a token grant to someone who knows how to solve it.

## Replies

**chfast** (2021-04-02):

Is this on-chain or off-chain?

---

**kladkogex** (2021-04-02):

On chain.

Otherwise it cant be trusted.

Basically Alice does a transaction for the benefit of Bob, and wants to reimburse exact gas costs from on-chain wallet of Bob

