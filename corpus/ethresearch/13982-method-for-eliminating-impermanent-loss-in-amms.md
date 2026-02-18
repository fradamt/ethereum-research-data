---
source: ethresearch
topic_id: 13982
title: Method for Eliminating Impermanent Loss in AMMs
author: efalken
date: "2022-10-20"
category: Economics
tags: []
url: https://ethresear.ch/t/method-for-eliminating-impermanent-loss-in-amms/13982
views: 2090
likes: 1
posts_count: 3
---

# Method for Eliminating Impermanent Loss in AMMs

I created a constant product AMM that virtually eliminates impermanent loss on the Goerli network [here](https://sam-ruddy.vercel.app/) (the verified contract on the testnet is here). I explain it more fully in a substack post [here](https://efalken.substack.com/p/how-to-eliminate-impermanent-loss), but in brief, it works as follows.

The AMM allows leverage, so traders and LPs can generate short positions as well as leveraged long positions. This allows LPs to net trades against their pool positions. If there is only one LP, and she is also the only trader, her net position is constant as the price changes. By definition, this implies she would have a zero impermanent loss.

With several LPs, the objective is to incent the LP’s to monopolize arbitrage trading. To do that, the first key is giving the LP’s a cheaper trading fee. If the trading fee is 0.2% for non-LPs, the LPs will find it attractive to arb a 0.2% price difference between the AMM and the ‘true’ price, while non-LPs will not.

A second key is a mechanism for making sure LPs trade in proportion to their pool liquidity. We do not want one minor LP making all of the arbitrage trades, because that would leave the other LPs subject to the standard IL. If you give the LPs the cheap fees on buy orders only if their net ETH position is below their initial ETH position (and similar for sells), this would prevent a minority of LPs from dominating the zero-fee trading.

There is a downloadable spreadsheet there to see how this works, as well as discussion of other conditions (eg, LPs cannot add or withdraw while their LP position is open).

Comments or questions appreciated.

## Replies

**vivien98** (2022-10-24):

> With several LPs, the objective is to incent the LP’s to monopolize arbitrage trading

Even if we manage to incentivize LPs to do arbitrage in a fair way like you said, impermanent loss still remains, right? Because LPs arbitraging themselves would only eliminate LVR and not IL.

---

**efalken** (2022-10-24):

Impermanent loss is eliminated. See link for detail. I define LVR as impermanent loss, that is, I use the standard option theoretic measure of the convexity cost for the hedger (ie, [p^2*variance/2]*[liq/p^1.5/2]). Some define IL using specific starting and ending prices, but that’s an inefficient metric because it is very case dependent, and assumes the LP is not hedging. While LP’s might not hedge, that just means they are exposed to more risk, but the expected loss to them is the same.

