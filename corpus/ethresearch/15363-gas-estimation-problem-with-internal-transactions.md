---
source: ethresearch
topic_id: 15363
title: Gas Estimation problem with internal transactions
author: nebojsa
date: "2023-04-20"
category: EVM
tags: []
url: https://ethresear.ch/t/gas-estimation-problem-with-internal-transactions/15363
views: 1404
likes: 0
posts_count: 2
---

# Gas Estimation problem with internal transactions

## Motivation

Gas estimation is a key piece of infrastructure that ensures transaction will have enough gas in the runtime. Currently, the community relies on the `eth_estimateGas` RPC endpoint to determine the minimum amount of gas needed for transactions to succeed. However, this poses a challenge when computing gas for contracts that catch *unsuccessful external calls* in their logic.

## Current Solution

The `eth_estimateGas` endpoint currently employs a binary search algorithm to find the optimal amount of gas required for transaction execution. It lowers the amount of gas if the simulation is successful and raises it if the simulation fails with an `out of gas` error.

## Proposal

To improve gas estimation, we propose tracking internal transaction failures caused by `out of gas` errors and changing the condition for lowering the amount of gas. Instead of lowering the gas only if the simulation is successful, the gas will only be lowered if the simulation is successful and doesn’t encounter `out of gas` errors in any internal transaction.

In [go-ethereum](https://github.com/ethereum/go-ethereum), this can be implemented by introducing a new [logger](https://github.com/ethereum/go-ethereum/blob/99f81d27248f13a8e43731a0a1294044ced5d675/core/vm/logger.go) that only listens to `CaputeFault` and records an error if it occurred due to insufficient gas.

## Replies

**wallawalla** (2023-06-15):

How does this allow for gas estimation in O(1) time? Does this approach handle tricky cases like `delegatecall(sub(gas, 10000), ...)`? It’d be great if you could share a bit more!

