---
source: ethresearch
topic_id: 1591
title: A simple temporary solution to the gas token abuse for the next HF
author: nootropicat
date: "2018-04-01"
category: Economics
tags: [gas-token]
url: https://ethresear.ch/t/a-simple-temporary-solution-to-the-gas-token-abuse-for-the-next-hf/1591
views: 1454
likes: 0
posts_count: 2
---

# A simple temporary solution to the gas token abuse for the next HF

Rent-based solutions are likely to be complex to implement and adopt, whatever the details. A simple temporary solution could be adopted in the next hard fork.

Gas token transports the refund part of the gas fee for storage/contract deletion from the past -> storing the gas price. The simplest possible solution is to implement it directly.

Empirically, the main gas price without congestion appears to be 1 gwei. Therefore the refund gas price should be frozen at 1 gwei.

Eg. sstore for a new location takes 20k GAS. 15k GAS can be later refunded. Therefore, the actual GAS cost during setting should be:

 gasCost = 5000*gasPrice+15000*1gwei/gasPrice

and the refund:

 refundGas = 15000*1gwei/gasPrice

(gasPrice can be a different variable for two different transactions)

Advantages: the incentive to spam the state storage during low gas prices disappears. Everything else remains at it is.

## Replies

**phil** (2018-04-02):

This works but then you’re talking about a capped refund of 1.5e-05ETH = .6 cents or so.  Might as well just set the refunds to 0 since nobody is using them as incentivized anyway, even at current rates.

