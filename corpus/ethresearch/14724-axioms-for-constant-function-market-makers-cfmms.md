---
source: ethresearch
topic_id: 14724
title: Axioms for Constant Function Market Makers (CFMMs)
author: kakia89
date: "2023-01-31"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/axioms-for-constant-function-market-makers-cfmms/14724
views: 1064
likes: 3
posts_count: 1
---

# Axioms for Constant Function Market Makers (CFMMs)

While CFMMs proved to be very popular and reliable, the construction of invariants to define them seems in many ways ad-hoc and not based in much theory. We fill this gap and propose an axiomatic approach to constructing CFMMs. The approach is, as in any axiomatic theory, to formalize simple principles that are implicitly or explicitly used when constructing trading functions and to check which classes of functions satisfy these principles, beyond those functions already used.

The constant product rule (CPMM) has been particularly focal in DeFi. Our main results characterize a natural superclass of the CPMM  resp. of its multi-dimensional analog, the (weighted) geometric mean by three natural axioms. The CPMM rule is characterized by being trader optimal within this class. This gives a possible normative justification for the use of this rule. Our axioms formulate broad and natural design principles for the construction of CFMMs for DeFi.

The first is homogeneity which guarantees that liquidity positions are fungible. Practically, the fungibility of liquidity positions allows tokenizing them in order to use them in other applications, for example as collateral or to combine them with other assets to new financial products.

The second is independence which requires that the terms of trade for trading a subset of token types should not depend on the inventory level of not-traded token types. In the case of smooth liquidity curves, this is equivalent to requiring that the exchange rate for a token pair does not depend on the inventory levels of tokens not involved in the trade. Independence can be interpreted as a robustness property that helps to secure the AMM against certain kinds of price manipulation attacks (e.g. for the purpose of front- or back-running) where an exchange rate for a token pair is manipulated by adding or removing liquidity for a token not involved in the trading pair or by trading a different token pair. Independence can also naturally occur when different token pairs are traded in independently run AMMs.

The combination of homogeneity and independence leads to constant inventory elasticity: the terms of trade are fully determined by the inventory ratio of the pair traded, and, at the margin, percentage changes in exchange rates are proportional to percentage changes in inventory ratio. Combining the axioms we obtain the class of constant inventory elasticity. Alternatively, if we require un-concentrated liquidity then the elasticity in the above characterization is positive but smaller or equal to 1.

If we further add symmetry in market making – an AMM is symmetric if the names of the token types can be changed without changing how the market is made – the AMMs in the class of homogeneous, independent AMMs with un-concentrated liquidity can be ranked by the curvature of their liquidity curves which determines how favorably the terms of trade are from the point of view of traders; the constant product rule is characterized by being trader optimal within this class.

The above characterizations are obtained for the case of more than two tokens traded in the AMM. For the case of exactly two tokens, the independence axiom is trivially satisfied and we generally obtain a much larger class of trading functions satisfying the above axioms of homogeneity, aversion to (im)permanent loss, un-concentrated liquidity, and symmetry. The class can no longer be completely ranked by the convexity of the induced liquidity curves. However, if we focus on separable CFMMs we obtain the same kind of characterizations as in the multi-dimensional case, as well as the same kind of optimality result for the CPMM. In the two-dimensional case, separability of the trading function is a consequence of an additivity property for liquidity provision that we call LP additivity.

For more technical information, please check [[2210.00048] Axioms for Constant Function Market Makers](https://arxiv.org/abs/2210.00048).

Any feedback is welcome. Are there other properties that pin down AMMs?
