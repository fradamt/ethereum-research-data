---
source: ethresearch
topic_id: 7912
title: Seigniorage Share Implementation
author: satoshinate
date: "2020-08-28"
category: Economics
tags: []
url: https://ethresear.ch/t/seigniorage-share-implementation/7912
views: 1159
likes: 1
posts_count: 2
---

# Seigniorage Share Implementation

Hi all,

I’ve taken the liberty to implement a modern version of Robert Sam’s 2015 proposal of a Seigniorage Shares model.

Specifically, there are two tokens, where one is an object of stabilization and the other is the investment token.

The investment token pays out dividends from the delta in proposed positive coin supply (see https://medium.com/@dejanradic.me/pay-dividend-in-ether-using-token-contract-104499de116a) for O(1) mechanics.

During negative coin supply deltas, the stablecoin is burned on chain for discounted investment tokens.

To wrap things nicely, the coin will be bootstrapped via liquidity mining on uniswap (add liquidity to receive new investment tokens), and the price oracle will be based on UniswapV2’s oracle functionality.

Would love to discuss economics of this design and see what works and what could be better.

## Replies

**satoshinate** (2020-09-03):

launched protocol: https://dollarprotocol.com/

