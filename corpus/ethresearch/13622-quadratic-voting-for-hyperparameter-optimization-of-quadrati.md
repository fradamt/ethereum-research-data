---
source: ethresearch
topic_id: 13622
title: Quadratic Voting for "hyperparameter optimization" of Quadratic Funding
author: llllvvuu
date: "2022-09-10"
category: Economics
tags: [quadratic-funding]
url: https://ethresear.ch/t/quadratic-voting-for-hyperparameter-optimization-of-quadratic-funding/13622
views: 2039
likes: 1
posts_count: 2
---

# Quadratic Voting for "hyperparameter optimization" of Quadratic Funding

## Motivation

In the [original quadratic funding (QF) paper](https://arxiv.org/abs/1809.06421), it’s pointed out that quadratic voting (QV) may be good for selecting from a fixed set of candidates, but does not itself generate any candidates.

In contrast, QF attempts to generate an “optimal” allocation from scratch. This flexibility also makes it more vulnerable to pockets of corruption: in QF, every tight-knit group regardless of size takes up resources, whereas in QV this only happens if a group manages to secure a plurality.

Due to the fragility of the base QF system, in practice a [number of parameters are continuously optimized](https://gov.gitcoin.co/t/the-grants-2-0-funding-stack-choose-your-own-algorithm/10770?u=llllvvuu), and there are more that could potentially be experimented with, such as how changing the search/recommendation algos, [deliberation](https://compdemocracy.org/) processes, and experimenting with [AI sales agents assisting people with contributions](https://twitter.com/glenweyl/status/1549832178476978178?s=20&t=IPR3c28q53CQmWayZCagmA) might affect the outcome.

This naturally suggests a hybrid approach which chooses from multiple instantiations of the more “flexible” QF, using the more “error-correcting” QV.

(there is some aesthetic similarity to putting a finality gadget on top of probabilistic consensus)

### Pre-Round vs Post-Round Voting

It’s useful to wait for the data from the round before voting on the fund matching rule. But is it also important to lock in the rule, for certainty? I would argue this latter concern is potentially negligible, since

1. There is more significant uncertainty about:
a. What match my contribution will get
b. How much funding the project will get
c. How much funding other projects will get
2. This uncertainty is unlikely to be resolved by predictive models (outcomes are highly path-dependent, and the purpose of QF in the first place is to reveal information that we couldn’t have predicted before)
3. Uncertainty may be good, if it disproportionally discourages would-be colluders

A preferable way to mitigate uncertainty might be to make available “match protection” features, such as a “stop-loss” order to pull my contribution, or put in a contribution, if some basic condition is met (e.g. match drops below some amount, funding reaches some amount, etc). This would leave us free to pursue post-round voting/ratification of the funds matching rule.

### Permissionless generation of alternatives

It could be permissionless for anyone to nominate a QF matching adjustment and/or manual disqualifications. The ballot could be searchable/sortable based on some collaborative filtering or prediction market scheme.

People could even make nominations that give some small fee to themselves if selected. The idea of incentivized teams competing to “fix it in post” could be very powerful for decentralizing any round postprocessing.

Such teams may “campaign”, e.g. provide explanations and graphics for why they made certain parameters and disqualification decisions.

### Further gains

It’s possible that multiple rounds of selection could create a “genetic algorithm” over QF “hyperparameters”. Information could also be shared between different orgs who are running QF. Hence, not only could QV provide a “last look” where high-collusion results could be forked out or even confiscated, it could evolve durable learnings regarding QF in the long-run.

## Replies

**dazzsherly** (2022-09-13):

Great Stuff, thanks for sharing the valuable information

