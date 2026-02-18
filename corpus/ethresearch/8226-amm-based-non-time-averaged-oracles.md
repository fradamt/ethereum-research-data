---
source: ethresearch
topic_id: 8226
title: AMM based non-time averaged oracles
author: snjax
date: "2020-11-17"
category: Applications
tags: []
url: https://ethresear.ch/t/amm-based-non-time-averaged-oracles/8226
views: 1252
likes: 3
posts_count: 1
---

# AMM based non-time averaged oracles

Some information about cryptocurrency rates could be obtained from AMM. The issue is that AMM could be manipulated and this may be the reason of hacks, like [2nd bZx hack](https://medium.com/@peckshield/bzx-hack-ii-full-disclosure-with-detailed-profit-analysis-8126eecc1360). Here I consider some manipulation costs computation for non-time averaged oracle models.

## 1. Uniswap v1 based oracle

Uniswap oracle manipulation is a composite of two opposite swaps.

(x,y) \rightarrow (x \sqrt{1+\alpha}, y\sqrt{1+\alpha}^{-1}) \rightarrow (x,y).

Price \pi_y/\pi_x at the middle will be \alpha times more than the initial.

The total fee for Uniswap v1 will be

\Phi = \phi (\sqrt{\alpha+1} - 1) x + \phi(1-\sqrt{\alpha+1}^{-1})y, neglecting O(\phi^2).

For the case of the same capitalization of x and y C/2, the total fee will be:

\Phi = \phi C \frac{\sqrt{\alpha+1} - \sqrt{\alpha+1}^{-1}}{2}, where C is total pair capitalization and \phi is fee rate.

## 2. Mooniswap based oracle

In Mooniswap there are two independent points, corresponding to opposite swaps. So, Mooniswap could offer upper and lower price bounds estimates. The difference between the points is corresponded to the accuracy of the oracle.

Attacker could shift any of two bounds to corresponding direction:

(x,y) \rightarrow (\sqrt{\alpha+1} x, \sqrt{\alpha+1}^{-1} y).

Rewards for opposite swap will be split by miners, arbitrage bots, and Mooniswap pool.

So, the cost for attack will be

\Phi = (\sqrt {\alpha+1} + \sqrt {\alpha+1} ^ {-1} -2) \frac{C}{2} = ((\alpha+1)^\frac{1}{4} - (\alpha+1)^{-\frac{1}{4}})^2 \frac{C}{2}

## Models comparison

Here is comparison of two models for \phi=0.003 and C=10000000(USD).

![oracle manipulation](https://ethresear.ch/uploads/default/original/2X/9/9ec056d6a79d1d441f34783cdd5310ecd57d5ce0.svg)

![oracle manipulation](https://ethresear.ch/uploads/default/original/2X/f/fbe253e25e3ec299983029c2f8ff352fe4dcd131.svg)

It is important to emphasize that manipulation(2) does not affect the whole value of the oracle, but only reduces the accuracy.

Manipulation cost is growing faster for the 2nd model, so, it could be used when the contract satisfies the following points:

- small manipulations are not important
- for big manipulations the attack is not cost-efficient
- more complex and time-averaged oracle constructions are vulnerable or too gas-inefficient for the current contract

## Links

[Uniswap whitepaper](https://uniswap.org/whitepaper.pdf)

[Mooniswap whitepaper](https://mooniswap.exchange/docs/MooniswapWhitePaper-v1.0.pdf)
