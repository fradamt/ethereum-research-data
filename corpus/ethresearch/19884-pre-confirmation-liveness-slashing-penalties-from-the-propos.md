---
source: ethresearch
topic_id: 19884
title: Pre-confirmation Liveness Slashing Penalties from the Proposer's Perspective
author: aimxhaisse
date: "2024-06-21"
category: Economics
tags: [preconfirmations]
url: https://ethresear.ch/t/pre-confirmation-liveness-slashing-penalties-from-the-proposers-perspective/19884
views: 2319
likes: 3
posts_count: 1
---

# Pre-confirmation Liveness Slashing Penalties from the Proposer's Perspective

Current designs around pre-confirmations involve a slashing penalty on liveness, that is if a proposer who commited to pre-confirmations misses its proposal, part of its collateral is burned or redistributed to the user that sent the pre-confirmation as a payback.

This post explores the liveness penalty from the point of view of proposers from an economical perspective.

## Sources of Liveness Issues

Liveness issues are complex and can come from different actors or sources, part of them are the result of the proposer’s actions or choices, part of them don’t depend on the proposer. For example:

- proposing a block in time but being reorg by the next proposer,
- failure from the relayer to send the header in time,
- failure from the relayer to propagate the signed header in time and reveal the block to the proposer.

As a result, the decision on whether to opt-in or not from a proposer perspective has to take into account an **inherent** risk outside of its actions. Using a statistical approach on network history sounds like an easy starting point.

## Economical Minimal Viability

In the last 7 days on the network, about `0.54%` of slots were missed, to break-even economically (that is, for an operator to not lose or win anything in the long run), assuming the liveness fault is `1 ETH`, the minimal extra-tip of a pre-confirmation would be `0.0054 ETH`.

To put it in perspective, the median execution reward in the last 7 days is `~0.048 ETH`, so with `1 ETH` of collateral, the pre-confirmations would need to be about `10%` of the block’s value with the current network conditions. Using `P(miss)` as the probability to miss a block, the break-even formula is:

(1 - (P(miss))) * tip = P(miss) * penalty

And so the minimal tip:

tip = {(P(miss) * penalty) \over (1 - P(miss))}

With `1 ETH` as a collateral, here is the model for low probabilites of missed block with `P(miss) < 0.025`:

[![download](https://ethresear.ch/uploads/default/original/3X/e/a/ea574d8ff641f0e75064bfc788d672f031b6a3cb.png)download626×455 25.2 KB](https://ethresear.ch/uploads/default/ea574d8ff641f0e75064bfc788d672f031b6a3cb)

Zooming out up with `P(miss) < 0.5`:

[![download](https://ethresear.ch/uploads/default/original/3X/0/6/0638f8a59181327ccce1392f2bd48663d52562aa.png)download608×455 23.4 KB](https://ethresear.ch/uploads/default/0638f8a59181327ccce1392f2bd48663d52562aa)

## Opt-in if Economically Viable

One idea to make it viable at scale with little effort from proposers would be for the pre-confirmation sidecar on the proposer side to opt-in to pre-confirmations only it if the tip is above what’s economically sound given the current rate of misses on the network. For example, if in the last 24 hours the average missed block proposal is `0.5%`, only commit to pre-confirmations which tip is above `0.005 ETH`.

This approach requires the relayer to pass the pre-confirmation tip information to the proposer to decide whether or not to commit to pre-confirmations, or the proposer to send the minimal-tip to the builder so it can provide a block that match it.

The advantage of this approach is if the network is struggling at scale, the risk for a proposer to miss a slot increases, and so it makes sense for proposers to opt-out of pre-confirmations until the situation resolves. Increasing the pre-confirmer bid under such conditions makes sense as more risk is taken.

A disavantage is that the missed block proposal rate is an approximation: it doesn’t account for totally offline validators, or for the extra-cost involved in validating the pre-confirmation on the proposer side which can take time and increase the risks of missing the slot.

## Alternatives

#### Adjusted Liveness Penalty

Instead of using a minimal tip as a way to decide if it’s viable, the liveness penalty could be dynamically adjusted to what is the minimal viable condition. The tip could then be a fixed value.

#### User-Defined Liveness Penalty

The user sending the pre-confirmation could also decide both the liveness penalty and the tip as suggested in [User-Defined Penalties: Ensuring Honest Preconf Behavior](https://ethresear.ch/t/user-defined-penalties-ensuring-honest-preconf-behavior/19545), and adjust it to what the current state of the network is/what validators accept. The assumption here is maybe for some pre-confirmations the goal is to be as soon as possible on the L1, and so, reducing the liveness penalty would increase their probabilities of being pre-confirmed. On the other hand an arbitrage pre-confirmation could prefer to opt-in for a larger liveness penalty as its opportunity would be lost if the block is missed.

## Caveats

This simple break-even model on the proposer side has no incentive, it is unclear if it will motivate proposers to opt-in.
