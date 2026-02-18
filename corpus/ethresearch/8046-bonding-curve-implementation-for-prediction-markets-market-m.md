---
source: ethresearch
topic_id: 8046
title: "Bonding curve implementation for prediction markets: market making without liquidity providers and impermanent losses"
author: kohshiba
date: "2020-09-29"
category: Economics
tags: []
url: https://ethresear.ch/t/bonding-curve-implementation-for-prediction-markets-market-making-without-liquidity-providers-and-impermanent-losses/8046
views: 2273
likes: 1
posts_count: 4
---

# Bonding curve implementation for prediction markets: market making without liquidity providers and impermanent losses

Hi Ethereans!

DEX using AMM seems very hot recently. In prediction markets, AMM can be implemented without liquidity providers or impermanent losses.

**Abstract.**

By applying dynamic pricing using a bonding curve to the parimutuel betting mechanism, it becomes possible to market-make prediction markets without liquidity providers and impermanent losses.

**Parimutuel betting mechanism**

While this method is not suitable for exchanges, it has the richest history compared to The pari-mutuel method’s advantage is that there is always liquidity, and there is no need for liquidity The problem with this method is that the price is usually always constant, making it difficult to incentivize early markets

**Dynamic pricing powered by bonding curve mechanism.**

The Bonding Curve mechanism (originally introduced by [@simondlr](/u/simondlr)) can eliminate the above problem by providing price movement; It gives more incentive to those who make the right predictions early on than to those who make them later on. The price movement is usually in response to the total token Also, the bonding curve mechanism creates price arbitrage opportunities for traders.

This mechanism combination is implemented in [Forecastory](https://www.forecastory.com/), a new forecasting market protocol I’ve been working on.

An introduction to the project can be found [here](https://medium.com/forecastory/introducing-forecastory-3d2d667e633e).

More details about the mechanism can be found [here](https://drive.google.com/file/d/1Ju20wl7ZvcFwy61WoeGHjoJoFVJixABC/view?usp=sharing).

You can try out the Rinkeby’s implementation from [here](https://www.forecastory.com/).

We’d love to hear your feedback!

## Replies

**kohshiba** (2020-09-30):

NOTE: The term AMM may be too broad.

This mechanism is not about AMMs like Uniswap. (Technically, Uniswap like AMM is called Constant Product Market Makers/CPMM)

https://medium.com/bollinger-investment-group/constant-function-market-makers-defis-zero-to-one-innovation-968f77022159

---

**lsaether** (2020-10-13):

Why are bonding curves better than orderbook or CPMM as implemented in catnip.exchange?

To me it seems like there would be a problem trading with this market. Let’s take for example a binary Yes-No market on some event. When the market is 50 - 50 odds why should anyone buy another share? Even if the outcome is how the market resolves that person would still lose money on their shares since they are essentially subsidizing the profits of the early participants in the market.

In comparison on Augur a person is incentivized to purchase shares up to 100% probability.

---

**kohshiba** (2020-10-14):

People would buy shares if their expectations of return > their subsidies for early participants.

Let’s say the probability of Trump win the presidential election 2020 of the U.S is 50% in a prediction market, but if one thinks that should be 80%, that person sees an opportunity in the market and would buy shares. (because that person sees more expectation on returns than their subsidy to early participants.) If one doesn’t see any opportunity in a market, one simply ignores the market. Even in that case, the market still shows the probability of the future event.

The market just aggregates information from many and reflects expectations of mass just like Uniswap does.

The advantages of this mechanism over order book or CPMM are;

1. more liquid (than order book)
2. no impermanent loss(advantageous to CPMM*)
*impermanent losses tend to be larger for volatile prediction markets and they become “permanent” losses

