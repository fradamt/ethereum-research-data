---
source: ethresearch
topic_id: 21929
title: Economic Censorship Games in Fraud Proofs
author: kakia89
date: "2025-03-10"
category: Layer 2 > Optimisitic Rollup
tags: []
url: https://ethresear.ch/t/economic-censorship-games-in-fraud-proofs/21929
views: 164
likes: 2
posts_count: 1
---

# Economic Censorship Games in Fraud Proofs

By [Ben Berger](https://sites.google.com/view/ben-berger/home), [Ed Felten](https://github.com/edfelten), [Akaki Mamageishvili](https://mamageishvili.info/) and [Benny Sudakov](https://people.math.ethz.ch/~sudakovb/). This is a repost from here: [Economic Censorship Games in Fraud Proofs - Arbitrum Research](https://research.arbitrum.io/t/economic-censorship-games-in-fraud-proofs/9722), by [Ben Berger](https://ethresear.ch/u/bnberger/summary).

Optimistic rollups grant a 7-day challenge period in their fraud proof systems to mitigate against a strong censorship attack, where the potential adversary controls so much of Ethereum’s stake to allow for complete jurisdiction over which blocks get accepted as part of the canonical chain.

However, other forms of censorship are possible and it is important to understand their implications for rollup security — in particular how the length of the challenge period is related to that security.

In a recent [paper](https://arxiv.org/abs/2502.20334) we study economic censorship attacks in which an adversary bribes Ethereum’s block builders/proposers to exclude the honest party’s moves in the challenge protocol, by offering them a payment higher than the honest party’s inclusion tip. This is particularly relevant today, as the grand majority of Ethereum blocks are built through the MEV-Boost auction.

In the fraud proof context, whenever it is the honest party’s turn to submit the next protocol move (which is an Ethereum transaction), the adversary can choose whether to censor that move at the cost of the bribe, or let that move through while conserving funds for future censorship.

The honest party, on the other hand, can offer higher or lower inclusion tips as a response to the adversary’s choices.

Our goal in the paper was to understand the dynamics introduced by this type of attack, the strategies we expect the different actors to use, and the implications of these for optimistic rollup security and design.

To this end, we study a stylized model of the interaction between an attacker, a defender and the block proposers, in the form of a multi-round strategic game. Each round corresponds to a block where the defender wants to submit its next move of the underlying challenge protocol.

We study three variants of this game, which differ according the number of proposers responsible for deciding the current block’s contents, and the proposers’ assumed behavior.

The three variants are parameterized at least by the total number of rounds T (corresponding to the length of the challenge period), the number of those rounds N that the defender needs to win (corresponding to the number of honest moves required to win the fraud proof challenge), and the budgets of the attacker and the defender, denoted D and A, respectively.

The main question we ask is:

> How large does the attacker’s (defender’s) budget have to be with respect to the defender’s (attacker’s) budget, as a function of the game’s parameters, such that it can guarantee victory in the game?

We provide answers to this question for each of the variants. En route, we identify optimal and approximately optimal (but simpler) strategies for both players.

In what follows we provide more details on each of the variants and our results, and we refer the interested reader to our paper for the full picture.

**\mathcal{G}^1 Game**

First, we look into the most basic version of this interaction where there is a single proposer in each round, and the round is won by the party that has placed a higher bid. The round winner gets her budget deducted by an amount equal to her bid, and the defender wins the entire game if and only if it has won the required number of rounds.

We identify the players’ optimal strategies, and we prove that the attacker can guarantee victory iff

\frac{T-N+1}{N}D \leq A

**\mathcal{G}^1_k Game**

Next, we investigate an extension of \mathcal{G}^1 where a round can be either regular or special. In a special round the attacker is required to outbid the defender by a factor k>1 in order to win it.

These special rounds are motivated by the existence of Ethereum proposers that are not rational, but rather follow the default transaction inclusion policy offered by Ethereum’s execution clients. Under this default policy, transactions are included in the block by decreasing order of priority fee per gas, and it estimated that around 2% of Ethereum’s propsers use it to build their blocks.

To illustrate the implication of this for censorship, let us assume that the honest party’s transaction consumes g gas units and is specified with a priority fee per gas f which happens to be the highest one among the current pending transactions. An adversary who wishes to censor that transaction would need to spend at least (G-g)f in priority fees, where G is the block gas limit, by submitting at least G-g gas units worth of transactions with priority fee at least f.  This is k = (G-g)/g times as much as the honest party would have paid for inclusion.

As opposed to \mathcal{G}^1, the optimal strategies in this variant and the borderline ratio between the players’ budgets that determines which of them can guarantee victory are complex and we suspect that there are no closed-form formulas to capture them. We do however provide an efficient algorithm to calculate these, and we also identify simple strategies for both players whose performance converges to that of the optimal ones in some asymptotic regime of the game’s parameters which fits the parameters we find in practice.

**\mathcal{G}^m Game**

Finally, we consider a setting where a block’s content is determined by multiple proposers, and the defender and attacker can interact with any of them. The defender wins a round if at least one of the proposers includes the defender’s transaction in its suggested ``inclusion list’'.

We analyze how the competition among proposers and its resulting equilibrium behavior affects the outcome of the game. We obtain almost matching conditions for both players to have a winning strategy. In particular, for the attacker, we obtain a lower bound on its budget that is almost the number of proposers times higher than the value from the game \mathcal{G}^1, for her to win with high probability.

**Translation of Results into Practice**

We now discuss the quantitative results we obtain when we plug-in the relevant parameters we find in practice that define the games \mathcal{G}^1, \mathcal{G}^1_k and \mathcal{G}^m.  We focus on the case of BoLD, which has been deployed on Ethereum mainnet on February 12th, 2025.

The one week challenge period in BoLD corresponds to about T =50000 blocks/rounds, since a new block on Ethereum is created every 12  seconds. It is estimated that around 2% of Ethereum proposers use default software to decide which transactions get included in their blocks. In other words, around s = 1000 rounds are special.

The block gas limit is 30M gas units at the time of writing, but [there is a strong willingness to raise it to 36M](https://pumpthegas.org/). A single BoLD transaction by the defender takes up about 0.5M gas units. Thus, in order to censor a defender’s transaction in a special round, the adversary would need to submit at least 29.5M gas units worth of transactions, each of which is specified with a priority fee per gas unit that is higher than the priority fee per gas unit specified by the defender.

Therefore, we estimate the parameter k for the special rounds in \mathcal{G}^1_k to be about 60, and soon to be increased to about 72. The maximum number of transactions that an honest party needs to post in a BoLD challenge is around N=60. Let us assume that the attacker can steal all the bridged assets from the optimistic rollup, if she manages to confirm the wrong claim about the rollup state. In the case of Arbitrum, that would amount to around $10B.

To guarantee security against economic censorship assuming that this is the attacker’s budget,

our results suggest that the defender’s budget D should be at least $12$M, in the absence of special rounds.

For the special round variant, the corresponding borderline budget ratio we find is approximately equal to 1786. Therefore, our result for  \mathcal{G}^1_k implies that D should be at least $5.6M in order to be secure against economic censorship.

With m block builders and no special rounds, the required value for D is simply lowered by a factor of m. A reasonable value for multiple proposers or FOCIL committee members is around 20, hence the required defender’s budget is in the order of sub million.
