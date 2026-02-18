---
source: ethresearch
topic_id: 19024
title: Public Projects with Preferences and Predictions
author: bowaggoner
date: "2024-03-17"
category: Economics
tags: [governance]
url: https://ethresear.ch/t/public-projects-with-preferences-and-predictions/19024
views: 1598
likes: 11
posts_count: 2
---

# Public Projects with Preferences and Predictions

A few years ago, I posted [Governance mixing auctions and futarchy](https://ethresear.ch/t/governance-mixing-auctions-and-futarchy/10772) here. Also relevant are [Practical Futarchy Setup](https://ethresear.ch/t/practical-futarchy-setup/10339) and [Votes as Buy Orders](https://ethresear.ch/t/votes-as-buy-orders-a-new-type-of-hybrid-coin-voting-futarchy/10305). My post/question eventually led to research funding from the Ethereum Foundation and now my collaborator and I have a paper proposing a new governance mechanism: [Public Projects with Preferences and Predictions](https://arxiv.org/abs/2403.01042). I hope you find it interesting and I would love to hear your feedback and thoughts! Here is a summary.

---

**Problem:** A group, such as members of a DAO, need to decide between one of several alternatives, such as which project to pursue (they must pick exactly one). I want to focus on two aspects of this problem:

- They want to base the decision on an aggregation of both preferences and information. For example, one way is to first hold discussions and conduct research in order to aggregate information. Then, if consensus is not reached, hold a vote to aggregate preferences into a final decision.
- A primary problem of any organization is to avoid capture. In particular, the individual preferences of the members are generally not perfectly aligned with the mission of the organization. The above “discuss-then-vote” approach doesn’t solve this. A decisionmaking mechanism should somehow be biased by a credible estimate of the impact on the organization’s mission.

---

**Formalizing it:** A group of agents must pick one of m alternatives. The group’s mission is quantified by what we call an “external welfare impact” of the decision. The goal is to maximize total welfare: the sum of the external welfare impact, plus the utilities of all the agents in the group. The group first wants to aggregate information, in particular about the external welfare impacts of each alternative choice it could make. We model information as predictions about the future, i.e. the group first wants to estimate the external welfare impact B_k of each alternative k=1,\dots,m. After obtaining the estimates, the group will hold a vote. We suppose that each agent i has a preference over the alternatives, modeled as a value v_k^i for each alternative k. The group will use some sort of voting mechanism to combine the preferences as well as the external welfare impacts into a final decision.

For example, consider a DAO whose charter requires consideration of climate impacts of its decisions. The external welfare impact B_k of an alternative k could be measured by the amount of extra tons of CO2 produced if that alternative is chosen. The DAO may still choose an alternative that produces more CO2 if the members as a whole strongly prefer that alternative.

---

**Proposal:** We propose it the **Synthetic players QUAdratic transfers mechanism with Predictions (SQUAP)**, and it works like this:

1. We use an information-aggregation oracle to obtain an estimate of the external welfare impact B_i of each alternative. The oracle can be implemented in many possible ways, but in particular we consider using “decision markets” (i.e. sets of conditional prediction markets, as in futarchy).
2. We use Quadratic Voting, specifically the Quadratic Transfers Mechanism studied by Eguia et al. However, the mechanism casts “extra” votes based on B_1,\dots,B_m.

The extra votes are not simply the numbers B_1,\dots,B_m for each alternative. Instead, they are the votes that “synthetic players” would cast in equilibrium of Quadratic Voting, if their total values for each alternative were B_1,\dots,B_m. This is based on an analysis of the equilibrium, extending results of Eguia et al.

---

**About the prediction markets:** We need to suppose that the external welfare impact can be predicted before the fact and measured afterward. You can think of lots of ways to use proxies and estimates for quantities that are hard to measure or have long time horizons. For simplicity, in the paper we assume that if we take any decision k, then B_k will be directly observable and measurable. So we will set up m prediction markets, predicting for each alternative k the eventual impact B_k conditioned on making decision k. When we eventually make some decision k, we cancel all the trades in every market except the market for k. But we do eventually observe B_k for that chosen alternative and we resolve the market payoffs accordingly.

The Quadratic Transfer Mechanism picks an alternative from a probability distribution, where the probability of taking decision k is e^{A_k} / \sum_{\ell} e^{A_{\ell}} and A_k is total the number of votes cast for decision k. There is a nonzero probability of picking each alternative. That may sound odd, but it actually helps address a well-known problem with futarchy and decision markets – bad incentives around predictions about decisions that won’t actually be taken.

---

**Formal results:** Unfortunately, we can’t quite prove (yet) good results about SQUAP itself. However, we can analyze an “Impractical Variant” that is not practical because it requires some extra knowledge by the mechanism designer. Essentially, instead of calculating our synthetic votes based on what the real players vote for, we have to first commit to our synthetic votes based just on knowing B_1,\dots,B_m, before we see what the players do. This is impractical to calculate without good estimates of what the players will do, but it’s not totally ridiculous. In any case, we can prove something:

> Main Theorem. In the 2-alternative case, in Nash equilibrium, the Impractical Variant of SQUAP satisfies Social Welfare \to Optimal as the “size” of the group grows large relative to the preferences of any one individual.

The interesting and non-obvious part of all this is that the mechanism “works” in theory even though there are apparently bad incentives across the two stages. Someone with really strong preferences about the decision could try to manipulate the prediction market prices in order to manipulate the synthetic votes. And someone who bet a lot of money in the prediction market could try to cast really outsized votes in the Quadratic Voting stage in order to make their prediction-market payoffs come good. So the interesting part is in proving that these things don’t happen, or rather, they can happen a little but not enough to influence the outcome significantly … as long as each individual’s preferences are small compared to the group total.

Our theorem quantifies the rate at which the social welfare approaches the optimal, and it’s reasonably fast as the size of the group grows large. But this post is too long already. I’ll just clarify that Social Welfare is formalized by the sum of the values of the participants in the group, plus the external welfare impact, of whatever the mechanism chooses.

The paper is here: [[2403.01042] Public Projects with Preferences and Predictions](https://arxiv.org/abs/2403.01042)

## Replies

**Jmiller4** (2024-03-29):

Cool stuff! Excited to check out the full paper.

