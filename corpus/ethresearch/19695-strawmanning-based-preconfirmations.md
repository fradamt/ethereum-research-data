---
source: ethresearch
topic_id: 19695
title: Strawmanning Based Preconfirmations
author: linoscope
date: "2024-05-31"
category: Layer 2
tags: [mev, preconfirmations, based-sequencing, sequencing]
url: https://ethresear.ch/t/strawmanning-based-preconfirmations/19695
views: 5184
likes: 31
posts_count: 3
---

# Strawmanning Based Preconfirmations

By [Lin Oshitani](https://twitter.com/linoscope) (Nethermind Research). Thanks to [Conor](https://twitter.com/ConorMcMenamin9) and [Aikaterini](https://www.linkedin.com/in/aikaterini-panagiota-stouka/) for the detailed discussions and review. Thanks also to [Ahmad](https://twitter.com/smartprogrammer) and  [Brecht](https://twitter.com/Brechtpd) for their review and comments. This work was partly funded by Taiko. The views expressed are my own and do not necessarily reflect those of the reviewers or Taiko.

# Introduction

[Based sequencing](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016/) provides a credibly neutral shared sequencer layer that enables composability among rollups and between rollups and L1. Additionally, [based preconfirmations](https://ethresear.ch/t/based-preconfirmations/17353) provide fast preconfirmation services on top of based sequencing, significantly enhancing the user experience as a result. However, compared to non-preconfirming based sequencing, naive implementations of based preconfirmations introduce negative externalities that require thoughtful consideration. Although issues have been highlighted in works such as [this Bell Curve episode](https://www.youtube.com/watch?v=b3o2YP6sxpg) (mainly in the context of non-based sequencers) and [this write-up](https://research.chainbound.io/examining-the-based-sequencing-spectrum) from Chainbound, we believe the topic remains largely underexplored.

In this post, we will analyze a simple “strawman” preconfirmation setup, identify its shortcomings, and shed light on the challenges that future solutions must address.

# The Strawman

The strawman based preconfirmation setup is as follows:

- The L1 proposer may or may not delegate the preconf right to some external entity.

We use the term preconfer to describe the entity providing preconfirmations, which can either be the L1 proposer itself or an entity delegated from the L1 proposer.

The preconfer handles preconfirmations by providing two endpoints:

- Request endpoint: For users and searchers to request preconfirmations.
- Promise endpoint: For streaming the preconf results to the public. It enables the preconfirmation requester to promptly receive the result while allowing other users to stay updated on the latest preconfirmed state before initiating their own preconfirmations.

Users will include a “preconf tip” to the requests to incentivize preconfers to provide preconfirmations.
The preconfer preconfirms transactions primarily on a first-come-first-serve basis.

[![Based Preconf (2) (1)](https://ethresear.ch/uploads/default/original/3X/6/2/62f461e44a685f6ecf9401c8c6ad62689a826ec1.jpeg)Based Preconf (2) (1)649×282 5.73 KB](https://ethresear.ch/uploads/default/62f461e44a685f6ecf9401c8c6ad62689a826ec1)

Furthermore, because they are significantly more complex to design and implement, we focus solely on execution promises. Execution promises guarantee the exact sequence and state of a transaction. In contrast, inclusion promises only ensure that a transaction will be included without specifying the conditions of its inclusion.

# The Problems

We will cover six problems with the strawman based preconfirmation design:

- Problem 1: Latency races
- Problem 2: Congestion
- Problem 3: Tip pricing
- Problem 4: Fair exchange
- Problem 5: Liveness
- Problem 6: Early auctions

## Problem 1: Latency races

Whoever has the lowest latency to the preconfer gains all the MEV [back-running profit](https://docs.cow.fi/mevblocker/concepts/mev-concepts/what-is-backrunning). This is because they can:

1. Be the first to obtain the latest state of the chain through the promise endpoint and
2. be the first to insert their back-run transaction via the request endpoint.

This structure has historically [incentivized latency races](https://academic.oup.com/qje/article/130/4/1547/1916146), where network participants strive to minimize latency to the limit. Eventually, this would lead to searchers choosing to colocate or vertically integrate with preconfers, which significantly risks the network’s [geographical decentralization](https://collective.flashbots.net/t/decentralized-crypto-needs-you-to-be-a-geographical-decentralization-maxi/1385).

Such latency races have been a long-lasting concern for existing centralized sequencers. For example, the Arbitrum team has explored the idea of [implementing Proof of Work](https://github.com/OffchainLabs/nitro/pull/1504) (PoW) where they grant fast connections to participants who succeed in PoW while imposing artificial delays on participants who do not. However, this proposal encountered [backlash from the community](https://research.arbitrum.io/t/thoughts-on-arbitrums-proposal-to-score-connections-by-pow/8121) due to the substantial economic waste introduced.

## Problem 2: Congestion

Given that L2 transaction fees are typically low, searchers may choose to avoid latency races altogether and instead flood the rollup with probabilistic arbitrage attempts. This can be done by spamming an arbitrage contract that attempts an arbitrage and rollbacks if it fails. In Solana, where the fee is extremely low, it has been [reported](https://www.jito.network/blog/solving-the-mev-problem-on-solana-a-guide-for-stakers/#:~:text=Solana%20validators%20are%20wasting%20more%20than%2058%25%20of%20their%20time%20processing%20failed%20arbitrages) that validators waste ~58% of their time processing such failed arbitrage transactions.

This would result in a situation resembling pre-Flashbots [priority gas auctions](https://arxiv.org/abs/1904.05234), where the competition among searchers congests the block space with failed arbitrage transactions, ultimately driving up gas fees for regular users.

## Problem 3: Tip pricing

The preconfer must solve an [online MEV problem](https://hackmd.io/@EspressoSystems/bft-and-proposer-promised-preconfirmations#:~:text=online%20MEV%20maximization%20problem), where they decide whether to preconf a transaction with no/limited visibility to other transactions that compete for the same position. For example, suppose the preconfer receives a preconf request with 1 ETH tip. How would the preconfer know that the tip is appropriately priced? Should they accept the tip and preconf immediately or wait for a while in case there is another request with a higher tip?

## Problem 4: Fair exchange

The preconfer can withhold preconf promises and not return them to the user in a timely manner. Note that preconfers are incentivized to withhold preconf promises as much as possible to maximize their opportunity to reorder and insert transactions, thereby increasing their MEV.

As an extreme example, the preconfer could withhold all promises during its window (12 sec or more), reorder and inject txs as it wishes, and only publish the promises when the final tx batch is submitted to L1.

## Problem 5: Liveness

For the case when the proposer delegates the preconfirming rights to an external preconfer, the liveness and censorship resistance of the preconfirmations will rely solely on this single external entity for the duration of the preconfer’s slot(s).

## Problem 6: Early auctions

Any system with L1 composable preconfirmations (i.e., preconfirmation of L1 transactions) will likely result in *preconfer-builder integration,* where preconfer and builder become the same entity. This is for two reasons:

- With L1 preconfirmations, most cross-domain MEV, including CEX-DEX arbitrage, will be captured through preconfirmed transactions.

Considering the bulk of MEV revenue comes from CEX-DEX arbitrage, this means that most MEV revenue will be secured through preconfirmations. Consequently, the revenue from building the non-preconfirmed portion of the block will be greatly reduced.

Preconfed L1 transactions must be included at the top of the current block.

- Inserting any transactions before a preconfirmed transaction could alter the state anticipated by the preconfirmation, potentially invalidating the preconfirmation guarantee. This means builders must constantly incorporate the latest preconfed transactions into their blocks, which would be extremely difficult, if not unfeasible.

Combined with preconf delegation happening ahead of the proposer’s slot, preconfer-builder integration leads us to a world where L1 proposers delegate their preconfirmation rights *and block-building rights* to the same external entity *ahead of time* for their slot.

Selecting the block builder in advance, known as *early auctions*, contrasts sharply with the current MEV-Boost PBS pipeline, where block builders are dynamically chosen *just-in-time* (*JIT*) within the slot through block auctions. More details comparing JIT auctions and early auctions can be found [here](https://collective.flashbots.net/t/when-to-sell-your-blocks/2814).

The goal of based sequencing is to inherit the security of L1. However, with based preconfirmations, we risk altering the security landscape of the underlying L1 itself. Although early auctions might not be entirely detrimental (further research and experimentation are needed), they represent a fundamental shift from the current MEV-Boost builder market. Therefore, they should be introduced with great care, especially when introduced off-protocol, where control over centralization tendencies is limited.

# Conclusion

We observed that naive implementations of preconfirmations can lead to various negative externalities. As with all things in blockchains, trade-offs are inevitable. However, such negative effects should be mitigated as much as possible and, when needed, introduced as a deliberate choice, not an accident.

At Nethermind, along with our collaborators, we are actively researching solutions that address the issues outlined in this document. Stay tuned for more updates!

## Replies

**FabrizioRomanoGenove** (2024-06-12):

These are all valid points. IMO the tension stems from the fact that you cannot have ‘JIT preconfs’ and traditional JIT block building at the same time. That is, either:

- We choose a world where, as you point out, proposers can issue execution preconfs based on the most recent state, and as a consequence they’ll have to build an entire block, and everything you say happens, or
- We choose a world where traditional JIT blockbuilding is preserved, and preconfs will just serve as inclusion guarantees of sorts. In this latter scenario I think many of your conclusions would not hold.

Personally, I think that preconfs as in point 2 would be enough for a lot of use cases. I also find it way less invasive with respect to changing the current situation.

---

**lucasege** (2024-07-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/fabrizioromanogenove/48/16390_2.png) FabrizioRomanoGenove:

> We choose a world where traditional JIT blockbuilding is preserved, and preconfs will just serve as inclusion guarantees of sorts. In this latter scenario I think many of your conclusions would not hold.

Fair point, but the OP does mention focusing solely on execution preconfs because they can be viewed as a superset of inclusion guarantees.

If we only care about inclusion, then yeah a simple IL design can solve for the builder separation issue, but still does not solve for the proposer’s incentives/honest actions here which I think are a majority of the problems outlined here.

A simple solution to problem 4/3 would be a decaying price function based on time, but I struggle to see how this would be implemented in a “based” manner (i.e. not just adding another chain / trust assumption).

