---
source: ethresearch
topic_id: 20044
title: Searcher Competition in Block Building
author: kakia89
date: "2024-07-11"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/searcher-competition-in-block-building/20044
views: 2106
likes: 5
posts_count: 1
---

# Searcher Competition in Block Building

In a new paper with Christoph Schlegel ([@jcschlegel](/u/jcschlegel)), Benny Sudakov and Danning Sui([@sui414](/u/sui414)), we look at the distribution of MEV rewards between the validator and searchers. We model the interaction between all players using tools from cooperative game theory. Namely, for any coalition of players, we define a (maximum achievable) value the coalition can derive by creating the best block together. The validator is a special player, that is needed to create any value. In other words, it has a veto power. However, searchers are the ones that find (arbitrage) opportunities which derive a value. Searchers can be substitutes or complements of each other into finding opportunities. The outcome of this interaction is payoff vector, specifying how much each player gets. In the core of the game payoffs are such that any coalition gets paid at least as much as the value they produce themselves.

First, we study a structure of the core, which is always non-empty set of payoff vectors. Then, we focus on the searcher-optimum allocation and show that each searcher obtains its marginal contribution. In a stochastic model, where each opportunity is independently found with the same probability by each searcher, we show that if this probability is mildly high in the number of searchers, validator gets all rewards. In other words, core is just a single payoff vector. While if this probability is low, with a constant probability the validator can get zero payment, as the searchers are complements of each other. We extend some results to the blocks with bounded size.

On the empirical side, we observe that if there is a high competition of searchers, validator rewards are increasing (in absolute terms), which aligns with our theoretical predictions.

For more details check out the paper: [[2407.07474] Searcher Competition in Block Building](https://arxiv.org/abs/2407.07474). Any feedback is welcome.
