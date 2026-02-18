---
source: magicians
topic_id: 9717
title: A simple design for algorithmic quasistable currency
author: kladkogex
date: "2022-06-23"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/a-simple-design-for-algorithmic-quasistable-currency/9717
views: 552
likes: 0
posts_count: 3
---

# A simple design for algorithmic quasistable currency

Arguably the latest events have shown that algorithmic stable currencies are hardly possible, and the best is just to have 1:1 fiat in the bank.

For many transactional purposes, though, it would be OK to have a quasistable currency that has a slow varying exchange curve vs USD.

If I want to send money to a friend, I care that the exchange rate of this currency does not change much during the transfer.

The question, is then, what is the best design for an algorithmic quasi stable currency

A Uniswap like AMM with a large reserve does smooth out the curve, if the reserve is much larger than the daily exchange volume.

The question is how to stimulate people to put lots of money into AMM for a long time.

One possibility would be to pay staking rewards for depositing funds into AMM (in addition to AMM fees) and then require staking  for a long period of time (say 3 months)

Then the higher is the staking reward rate, the more money is in the AMM and arguably, the smoother is the exchange curve.

An added benefit of this design is that it creates an incentive to use AMM vs centralized exchanges

## Replies

**0xcacti** (2022-06-23):

This was the idea behind olympus no?  That did not work extremely well, although I am sure there is some contention over the way that it failed.

I think the problem with quasi/algo stables is that they all seem to require a constant inflow of cash/backing to be sustainable.  See bean, ohm, ust, etc.

---

**kladkogex** (2022-06-24):

Interesting

Thank you for the reference

> That did not work extremely well, although I am sure there is some contention over the way that it failed.

May be the time was wrong …

> I think the problem with quasi/algo stables is that they all seem to require a constant inflow of cash/backing to be sustainable. See bean, ohm, ust, etc.

Arguably one of the reasons fiat currencies are stable is central banks provide infinite liquidity to

national banks at low interest rates …

