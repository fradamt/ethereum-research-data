---
source: ethresearch
topic_id: 6445
title: A mathematical analysis of Uniswap markets
author: g
date: "2019-11-12"
category: Economics
tags: []
url: https://ethresear.ch/t/a-mathematical-analysis-of-uniswap-markets/6445
views: 3218
likes: 11
posts_count: 2
---

# A mathematical analysis of Uniswap markets

Hey all!

We just put out a new paper showing some interesting properties of Uniswap and its generalizations. The paper can be found [on arXiv](https://arxiv.org/abs/1911.03380).

Essentially, we show a few things:

1. The instantaneous Uniswap arbitrage problem (along with the Balancer arbitrage problem) is convex, even when adding in most reasonable (read: convex, monotonic) models of the market. This implies that the arbitrage conditions are often easy to compute and are extremely likely to hold in practice.
2. There doesn’t seem to be a way of depleting Uniswap markets of their reserves by only trading the pair of coins found in the market (i.e., the only possible way to truly deplete a market is by burning UNI coins).
3. As one might expect, the larger the fees, the larger the no-arbitrage bounds are, which means that the Uniswap price may stray further from the true market price.
4. The paper also gives an explicit formula for Uniswap returns in the no-fee case by constructing an equivalent portfolio.

We also leave some questions which may be of interest to the Eth research group:

1. What is the right view of convexity for AMMs? We mention that both Balancer and Uniswap are also log-log convex (as is any AMM which uses concave, nonincreasing functions for their bonding curves), but don’t explore this topic further.
2. Under what conditions can we guarantee that liquidity providers have positive expected value relative to a portfolio with equivalent weights to the UNI coins minted?
3. Are there even more natural generalizations (or classes) of AMMs which have better properties than Uniswap/Balancer? Can we characterize what conditions are necessary/sufficient for a “good” AMM? What does this even mean in practice?

Anyways, please feel free to ask us any questions (or pose any problems that come to mind!) about/from this paper ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

## Replies

**g** (2020-03-24):

[@tchitra](/u/tchitra)  and I were recently able to answer questions 1 and 3 in a fairly natural way in a [new paper on arXiv](https://t.co/X2cG2RQq8G) we just released, and question 2 in the path independent case (though the general case remains somewhat open). In particular, we give a very general class of AMMs (which we call the Constant Function Market Makers or CFMMs) that includes Balancer, Curve, Uniswap, etc as specific instances.

It also has some (hopefully) neat results!

1. There is general method for deriving liquidity provider returns, which turns out to just be convex duality theory. It can be used to give a few-line-proof of the LP returns for Uniswap and Balancer.
2. We show that a CFMM is path independent if, and only if, it can be written only as a function of the reserves (and the proof gives a way of constructing this function).
3. The definitions of path independence are relaxed a little bit to a new (and still-as-useful version) called a path surplus. This general case is harder to analyze, as one might expect, but includes many CFMMs with fees, which are often not path independent.
4. We give sufficient conditions for which functions might serve as good price oracles.
5. This class allows one to optimize over good CFMMs with respect to some desired objective. In other words, if anyone would like to come up with a good CFMM for a specific task, it is likely possible to find a function which is “good” in whatever sense they might want.

Some future questions:

1. Can we give the general returns for path deficient LPs?
2. Is convexity a necessary condition? It is easily sufficient since it implies all of the resulting theorems, but perhaps there is something weaker that will also work?
3. Is there a class of fees and fee structures which can be easily analyzed and/or optimized over?
4. Is there a framework in which we can compare the traditional AMMs (e.g. Hanson’s LMSR) and CFMMs? We give a proof as to why this question makes no sense under our conditions, but perhaps there is a useful framework where these things can be compared.
5. Is there a subclass of CFMMs that is “easy to optimize over,” i.e., under some useful conditions and models, we can give either an analytic solution or a poly-time algorithm to compute it or approximate it. The problem is easily seen to be NP-hard in general for many objective functions so only approximations will do for general CFMMs.

As always, please feel free to ask any questions or conjectures! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

