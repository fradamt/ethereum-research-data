---
source: ethresearch
topic_id: 2429
title: Quadratic costs and collective payouts as anti-centralization gadget
author: vbuterin
date: "2018-07-03"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/quadratic-costs-and-collective-payouts-as-anti-centralization-gadget/2429
views: 3979
likes: 12
posts_count: 14
---

# Quadratic costs and collective payouts as anti-centralization gadget

The following is a proposal for a kind of gadget that could be added to Casper (or potentially other mechanisms) to explicitly discourage concentration and create a fairer environment for small validators.

Suppose that every validator v_i \in V (with weight w_i, weights summing to 1) can specify a value x_i that represents their “vote” in the gadget. At the end of every round, each validator v_i pays \frac{1}{2} * w_i * x_i^2, and gets back w_i * \sum_j{(w_j * x_j)}.

Suppose R = w_i * \sum_{j \ne i}{(w_j * x_j)} is the contribution to a validator’s payout from all other validators. A validator’s net payout is R + w_i * (w_i * x_i - \frac{1}{2} * x_i^2). The derivative equals zero (and hence the payout is maximal) at x_i = w_i. Hence, larger validators have an incentive to choose larger values of w_i, and as a result, their payouts will be lower.

For example, suppose other validators’ contribution, \sum_{j \ne i} (w_j * x_j), is 0.25, and some given validator has w_i = 0.15. Then this is their payout curve:

[![Screenshot_2018-07-04_00-19-39](https://ethresear.ch/uploads/default/original/2X/c/cc8438c27dfd317c0604072050cf6c575a1e03f2.png)Screenshot_2018-07-04_00-19-39324×215 4.75 KB](https://ethresear.ch/uploads/default/cc8438c27dfd317c0604072050cf6c575a1e03f2)

The optimum is at x=0.15, with a payout of R + w_i * (w_i * x_i - x_i^2) = 0.15 * (0.25 + 0.0225 - 0.01125) = 0.0391875 (0.26125 per unit weight). However, some smaller validator in this scenario, with w_k = 0.01 would have voted x_k = 0.01, and they would be getting a payout of 0.01 * (0.2725 - 0.0001) = 0.002724 (0.2724 per unit weight). The result is that smaller validators, and validators that are *less* capable of forming collusions, get higher payouts than validators that are *more* capable of forming collusions.

This has implications beyond the blockchain space: it shows how [quadratic voting](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2343956) in general, which works very similarly to this mechanism in terms of private costs and collective effects, has an even larger egalitarian effect than originally expected, and particularly how it can have pro-egalitarian consequences even without taking into account any explicitly built-in egalitarian properties (eg. distributing the revenue proportionately to all unique humans).

## Replies

**MPR** (2018-07-03):

The way you’ve stated how quadratic voting would work seems to be a major security risk, despite giving higher rewards to small skaters.

If it is possible to specify x_i then it would be possible for an attacker to increase x_i to a point that would not be economically optimal, but would increase their voting power in a shard. A wealthy attacker could then target a single shard and halt it’s function even if they don’t have a majority of the stake.

---

**danrobinson** (2018-07-03):

Couldn’t you drop the quadratic voting part of this mechanism (specifically the part where voters have the option to puff up their vote at quadratic cost), but still keep the concentration-resistant payout mechanism?

The simplest way would be to mandate  x_i = w_i  for all i, rather than allowing each validator to choose its own  x_i  (and separately assuming that economic incentives will push validators toward the  x_i = w_i  point).

I figure you were also looking for a way to do Sybil-resistant quadratic voting (which is extraordinarily cool), but I just want to understand if there’s an independent mechanism here for concentration-punishing payouts.

---

**vbuterin** (2018-07-04):

I dropped the “quadratic voting” part from the title; the participants are technically QV’ing on the collective payout factor but it’s not a governance system of any kind beyond that.

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> The simplest way would be to mandate x_i=w_i for all i, rather than allowing each validator to choose its own x_i (and separately assuming that economic incentives will push validators toward the x_i = w_i point).

Ah no, you don’t want to do that. The reason is that if you do that, then a coordinated group of participants or single participant with multiple accounts would have no way to coordinate to raise their x_i values together to their *mutual* optimum. The ability for groups of validators to collude to maximize their total gain (and maximize other validators’ gain even more in the process) is an important part of this mechanism.

Allowing arbitrary x_i values also ensures that payouts are invariant to splitting and merging; if you split or merge your accounts, your incentives to set x_i values are the same as they were before and so your total payout will be the same as it was before.

---

**danrobinson** (2018-07-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Ah no, you don’t want to do that. The reason is that if you do that, then a coordinated group of participants or single participant with multiple accounts would have no way to coordinate to raise their xix_i values together to their mutual optimum. The ability for groups of validators to collude to maximize their total gain (and maximize other validators’ gain even more in the process) is an important part of this mechanism.

Ahhh, I see that now, as well as the point that the votes don’t determine your weight in any other governance mechanism.

Pleasingly this already includes a “turnout reward” mechanism that should tend to disincentivize censorship, since every validator is rewarded for the participation of other validators in each vote.

---

**krzhang** (2018-07-04):

I’m confused. The validators in total pay \sum_i (1/2 w_i x_i^2). The overall payout is \sum_i w_i \sum_j (w_j x_j) = \sum_j (\sum_i w_i) w_j x_j = \sum_j w_j x_j. These are not equal (in particular, the second one can be larger than the first), so where is the money coming from?

---

**vbuterin** (2018-07-04):

It’s a subsidy coming from the protocol.

---

**krzhang** (2018-07-04):

Okay. In that case I’m assuming you’re in a context where you are not afraid of the protocol being drained by repeated application of such subsidies. (If everyone puts in a really small amount, say, then everyone gains). One such context would be every time we run this gadget, something else is being done, and that something else is providing enough value to the community as a whole.

If you do want to prevent draining, there must be edge cases (upper bounds on the money the protocol is willing to pay). On the edge cases, there can easily be attacks because the calculus no longer perfectly applies (well it does, but you must look beyond criticial points and also at boundary points now).

Typo: "larger validators have an incentive to choose larger values of x_i". I imagine the weight w_i is “more” fixed than x_i.

---

**vbuterin** (2018-07-05):

Think of the reward being added as an additional component of a proof of stake reward. If everyone participates in proof of stake validation as a result of this mechanism, then I would say that’s great.

---

**eva** (2018-07-23):

Interestingly, this quadratic costing (QC), concentration-resistance mechanism could be leveraged as a check and balance to discourage tyrannies in a *QV governance* itself (e.g., against collusive individual and/or majority). Where voters are incentivized with a vote-mined token and payout is *n* - QC, similarly *xᵢ* would be the QV and *wᵢ* the weight over total votes.

---

**nadavhollander** (2018-07-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Allowing arbitrary xix_i values also ensures that payouts are invariant to splitting and merging; if you split or merge your accounts, your incentives to set xix_i values are the same as they were before and so your total payout will be the same as it was before.

Forgive my naiveté, but I’m struggling to see the mathematical justification for this.  Are there some non-obvious mathematical derivations that yield this result?  Or am I missing something?

---

**vbuterin** (2018-07-25):

Suppose a user controls accounts v_1 ... v_k with weights w_1 ... w_k and votes x_i ... x_k. Then, the user’s marginal (ie. the derivative of the) cost to increasing x_i is w_i * x_i, and the user’s marginal gain is \sum_{j=1}^k w_j * w_i, as the user gains the benefit across all of their accounts. The two are equal when x_i = \sum_{j=1}^k w_j, exactly the same result as if all of that weight was concentrated within a single account.

---

**nadavhollander** (2018-07-25):

Got it, thanks.  Very elegant construction ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**sindarknave** (2018-09-30):

Would intertemporal changes benefit a collusive group of stakers?

Let’s say there are two validators. For one round validator A borrows capital and increases their stake, changing their  x_a  to fit  w_a , then immediately withdraws that stake after one epoch. Assuming that a validator’s best estimate of their weight is their weight in the previous epoch, validator B would underestimate and overestimate an optimal  x_b  for two epochs respectively. Not sure to what degree this attack can be conducted over time, but systemic uncertainty might benefit collusive groups of validators that can quickly borrow capital to vary their stake.

(A simple way to solve this could just be to commit your  x_b  to  w_b  before knowing w_b.)

