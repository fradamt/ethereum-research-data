---
source: ethresearch
topic_id: 4263
title: Any-order condition resolution in conditional prediction markets
author: cag
date: "2018-11-15"
category: Applications
tags: []
url: https://ethresear.ch/t/any-order-condition-resolution-in-conditional-prediction-markets/4263
views: 1699
likes: 4
posts_count: 1
---

# Any-order condition resolution in conditional prediction markets

So the [Gnosis PM contracts 2.x](https://gnosis-pm-contracts.readthedocs.io/en/latest/developer-guide.html) contains better support for conditional markets.

Some details are [here](https://gnosis-pm-contracts.readthedocs.io/en/latest/changes-from-v1.html#conditional-market-support) but to summarize, for two questions with outcomes [A, B, C] and [HI, LO], conditional markets can be made:

[![Conditional markets](https://ethresear.ch/uploads/default/original/2X/4/44efe38c092dd7641accabc1b869375e3006f9f3.png)Conditional markets460×405 30.3 KB](https://ethresear.ch/uploads/default/44efe38c092dd7641accabc1b869375e3006f9f3)

Wherein the predictive assets can be redeemed in any order of its constituent conditions:

[![Any order redemption](https://ethresear.ch/uploads/default/original/2X/e/e65998734d03cf4dbdc5c0b94594d9698a0a8b1f.png)Any order redemption460×405 32.6 KB](https://ethresear.ch/uploads/default/e65998734d03cf4dbdc5c0b94594d9698a0a8b1f)

This is done with a mapping from account => position id => balance, where a position id is a hash(collateralERC20Address . truncated32ByteSum({hash(condition id . index set) : outcome collection}).

I’m wondering how safe using a truncated32ByteSum of hashes to represent a set of objects as a key for a mapping is. In this case, this is further wrapped inside of another hash due to the use case. Maybe somebody can point me to similar uses of this idea?

Also, unions of outcomes are represented by bit arrays which are called *index sets*. I wanted to fully generalize Boolean formulas as keys in an mapping, but that doesn’t seem to be possible, meaning (A&HI)|(B&LO) can’t be represented as a single key whereas (A&HI)|(B&HI) = (A|B)&HI can.
