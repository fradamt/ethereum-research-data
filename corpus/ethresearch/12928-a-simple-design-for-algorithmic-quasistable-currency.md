---
source: ethresearch
topic_id: 12928
title: A simple design for algorithmic quasistable currency
author: kladkogex
date: "2022-06-23"
category: Economics
tags: []
url: https://ethresear.ch/t/a-simple-design-for-algorithmic-quasistable-currency/12928
views: 1445
likes: 0
posts_count: 2
---

# A simple design for algorithmic quasistable currency

For many transctional purposes it is OK to have a quasistable currency that has a slow varying exchange curve vs USD.

For example, If I want to send money to a friend, I care that the exchange rate of this currency does not change much during the transfer.  Therefore, I want a currency with suppressed fluctuations of the exchange rate.

The question, is then, what is the best design for an algorithmic quasistable currency

A Uniswap like AMM with a large reserve does smooth out the curve, if the reserve is much larger than the daily exchange volume.

The question is how to stimulate people to put lots of money into AMM for a long time.

One possibility would be to pay staking rewards for depositing funds into AMM (in addition to AMM fees) and then require staking for a long period of time (say 3 months)

Then the higher is the staking reward rate, the more money is in the AMM and arguably, the smoother is the exchange curve.

An added benefit of this design is that it creates an incentive to use the AMM vs centralized exchanges, so volume will arguably shift to  the AMM.

## Replies

**BnWng** (2022-06-24):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> it is OK to have a quasistable currency that has a slow varying exchange curve vs USD.

Totally agree, that, practically speaking, many usecases do not require the stability of USD. However, giving enough stability for all usecases creates a strong network effect. I.e. everyone will likely use the currency that has *greater than* the stability they require.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> A Uniswap like AMM with a large reserve does smooth out the curve, if the reserve is much larger than the daily exchange volume.

To clarify, you’re saying: a large uniswap pool of e.g. TOKEN:USDC would smooth out the price fluctuations of TOKEN because a lot of trading volume would be required to arbitrage the price on the current fair market price?

Unfortunately, the volume is also a function of the potential arb profit - so seem like any significant deviation from secondary market price would greatly increase volume.

So ultimately, this is another form of backing a token with collateral where the ‘backing’ gets worse and worse as users redeem.

