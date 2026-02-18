---
source: ethresearch
topic_id: 1830
title: Algorand-style privately selected committees
author: vbuterin
date: "2018-04-25"
category: Sharding
tags: []
url: https://ethresear.ch/t/algorand-style-privately-selected-committees/1830
views: 2383
likes: 0
posts_count: 2
---

# Algorand-style privately selected committees

In contexts where commitee sizes are sufficiently large, it could make sense to use [Algorand](https://www.algorand.com/whitepapers/)-style privately selected committees, in order to improve lookahead privacy to improve DoS resistance and resistance against other kinds of adaptive adversary attacks.

Algorand-style private selection works as follows. Suppose that each validator V_i has a private preimage C_{V_i} (a la [RANDAO](https://ethresear.ch/t/rng-exploitability-analysis-assuming-pure-randao-based-main-chain/1825)), and there is a common randomness source R; for any given proposal P, we derive a randomness R_P (eg. R_P = H(R, C_P), where C_P is the *proposer’s* preimage). If there are in total N validators and we want a committee of size M, then anyone can make a signature by revealing C_{V_i} and showing that C_{V_i} \le 2^{256} * \frac{M}{N}. On average, M of the N validators will be able to do so for any given proposal, with standard deviation \sqrt{M} and so at least M - 3\sqrt{M} ~99.85% of the time (and at most M + 3\sqrt{M} 99.85% of the time).

Suppose an attacker has fraction p of proposers, and the committee threshold is \frac{2}{3} * M; we can try to estimate the probability that a fraudulent proposal will get through for various values of p and M with publicly selected committees (which are guaranteed to have size exactly M) and privately selected committees (using Poisson distributions, so assuming N approaching infinity, values for N = 20000 are very close to the limit at N \rightarrow \infty):

- M = 200, p = \frac{1}{4}: public selection safety failure 6.25 * 10^{-35}, private selection 1.89 * 10^{-22}
- M = 100, p = \frac{1}{4}, public selection safety failure 1.21 * 10^{-18}, private selection 2.75 * 10^{-12}
- M = 200, p = \frac{1}{3}: public selection safety failure 1.07 * 10^{-21}, private selection 5.64 * 10^{-13}
- M = 100, p = \frac{1}{3}, public selection safety failure 6.45 * 10^{-12}, private selection 1.90 * 10^{-7}
- M = 200, p = \frac{1}{2}: public selection safety failure 1.77 * 10^{-6}, private selection 9.35 * 10^{-4}
- M = 100, p = \frac{1}{2}: public selection safety failure 4.36 * 10^{-4}, private selection 1.24 * 10^{-2}

In summary, private selection unfortunately does have the weakness that it nearly doubles required safe committee sizes.

## Replies

**JustinDrake** (2018-04-25):

I wonder if this committee selection mechanism is one of Algorand’s patent applications (see [page 1 of their whitepaper](https://arxiv.org/pdf/1607.01341.pdf))

> Algorand’s technologies are the object of the following
> patent applications: US62/117,138 US62/120,916 US62/142,318 US62/218,817 US62/314,601 PCT/US2016/018300
> US62/326,865 62/331,654 US62/333,340 US62/343,369 US62/344,667 US62/346,775 US62/351,011 US62/653,482
> US62/352,195 US62/363,970 US62/369,447 US62/378,753 US62/383,299 US62/394,091 US62/400,361 US62/403,403
> US62/410,721 US62/416,959 US62/422,883 US62/455,444 US62/458,746 US62/459,652 US62/460,928 US62/465,931

