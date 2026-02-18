---
source: ethresearch
topic_id: 2941
title: Channels Can Enforce Contracts Beyond Intermediary Lockup Time
author: ldct
date: "2018-08-15"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/channels-can-enforce-contracts-beyond-intermediary-lockup-time/2941
views: 2624
likes: 9
posts_count: 3
---

# Channels Can Enforce Contracts Beyond Intermediary Lockup Time

**Authors**: L4 Research Team. Special thanks to Armani Ferrante and Liam Horne for coming up with the on-chain transfer mechanism a few months ago.

## Background

In a state channel network, users can interact (enter contracts) with each other even if they don’t have a direct channel open with each other. A simple example of this is multi-hop payments in the lightning network, implemented via HTLCs.

There are a few constructions for this, including metachannels (section 5.9 of https://counterfactual.com/statechannels), Perun’s virtual channels, Sprites, Celer Network’s conditional payments and others, each with different properties.

In general, however, the intermediaries that mediate an interaction must lock up some collateral for an amount of time (e.g. in the lightning network, they are locked in a HTLC). Since users won’t consent to having their money locked up for an indefinite amount of time, there must be a time bound beyond which the intermediary must be able to recover their collateral. Furthermore, the intermediary is likely to charge an amount of fees proportional to the collateral lockup time (an interest rate).

## Introduction

This note describes how to build metachannels for which the users (i.e., non-intermediary parties) can enter contracts beyond the length of time for which collateral is locked up.

This only describes how to do it for 2 users (I don’t know how to extend this for more than two users!)

## Problem

We assume that Alice and Bob wish to enter a contract S. Alice locks an amount a_0 into the contract and Bob locks an amount b_0 into it, and intermediaries I_1, I_2, \ldots I_n offer to lock up an amount of collateral k = a_0 + b_0 until a deadline T.

In the old design (section 5.9 of the paper linked above), we create a proxy object for each channel, all of which observe the same counterfactually instantiated object S (observation is denoted by dashed arrows). Let an instance of proxy object be denoted P_{ij} where i, j are channel participants.

[![image](https://ethresear.ch/uploads/default/optimized/2X/0/0cf7f37cf9d3f5500a942f04605b2c0289b39fb7_2_690x221.jpg)image1408×452 24.9 KB](https://ethresear.ch/uploads/default/0cf7f37cf9d3f5500a942f04605b2c0289b39fb7)

When S is finalized to a value that assigns Alice an about a, then P_{ij} assigns a to i and k - a to j. (dashed arrows denote assignment of ownership)

[![image](https://ethresear.ch/uploads/default/optimized/2X/e/ec101e8e111f466965ba7e1b4bc3f56f34c6c342_2_690x219.jpg)image1452×462 32.9 KB](https://ethresear.ch/uploads/default/ec101e8e111f466965ba7e1b4bc3f56f34c6c342)

Observe that each P_{ij} has k assigned to it, each I_m recovers k, A recovers a and B recovers k-a.

More concretely, the proxy objects implement these rules: they are parameterized by an observed object S, a deadline T, a left party i, a right party j, and a collateral amount k.

1. If S is not finalized and the current block height is less than T, nothing is permitted.
2. If S is finalized at a, i may withdraw an amount a and j may withdraw an amount k-a

This design means that A and B cannot enter a contract that lasts beyond T, since after time T, each intermediary I_m needs to recover their collateral, hence S **must** finalize to some value (i.e., this forced finalization at T must be enforced either in S or in the proxy).

## Solution

In the new design, if S has not finished by the deadline (denoted by a question mark), the following happens instead (a solid arrow denotes on-chain transfer of funds):

[![image](https://ethresear.ch/uploads/default/optimized/2X/9/9deb2e3273fad9cc3ecf84e0cfcb9f98a013d44d_2_690x214.jpg)image1420×442 18.2 KB](https://ethresear.ch/uploads/default/9deb2e3273fad9cc3ecf84e0cfcb9f98a013d44d)

Once again that each P_{ij} has k assigned to it, each I_m recovers k, but now A and B collectively own an amount k, locked in S.

We see that S must record who sent it money, in order that the proxy objects “to the left” of the sender send to the right, and proxy objects “to the right” send to the left.

Additionally, note that it is safe to allow any party to send k at any time, not just when the deadline is over. This is desireable because parties might want to do this when gas prices are particularly low, but when the block height is not T yet.

Hence the proxy objects now implement these rules: they are parameterized by an observed object S, a deadline T, a left party i, a right party j, and a collateral amount k. The set of parties must be ordered, so that we can compare them; in this case, A < 1 < 2 < 3 < B, and we require i < j.

1. If S has balance 0 and S is not finalized, then either i or j may send an amount k to S.
2. If S is not finalized, the current block height is less than T, and S has balance k, nothing is permitted.
3. If S is finalized at a, i may withdraw an amount a and j may withdraw an amount k-a
4. If S is not finalized and the current block height is over T, and S has balance k, ask S who sent it the amount k; call that sender is P_{i_s j_s}. If i  i_s, then i may withdraw k.

These notes is also available in a version-controlled form at https://github.com/counterfactual/t-metachannel-notes

## Replies

**nginnever** (2018-08-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> Since users won’t consent to having their money locked up for an indefinite amount of time, there must be a time bound beyond which the intermediary must be able to recover their collateral.

*EDIT: The following assumes the intermediary set contains just one hop, a necessarily centralized hub. I have not thought about the implications on griefing a channel that is open through more than one intermediary as outlined in OP.*

While a hub won’t consent to keeping collateral locked forever, I could perceive it in a hubs best interest to keep the channel open as long as they can afford the capital lock if they are making transaction fees in the channel. Rather than require a “time bound”, could we not just let anyone in the channel exit when they want to?

I’ve created an altered “metachannel” or “virtual channel” based on my previous work and the Perun protocol. Rather than rely on a pre-agreed “validity timer” that requires that channels must be closed and reopened, or somehow altered as in your protocol here, I have elected to create exit rules on the state-channel contract that let any party in the set `virtualChannel.all-users {Alice, Bob, Ingrid}` signal to close by requesting of `vc.all-users` a consensus update to their “manager channel” for off-chain settlement. If off-chain consensus cannot be achieved, any party in `vc.all-users` may begin a challenge on-chain to force a virtual channel settlement.

This can lead to grief closing by the hub/operator but I am wondering if it is useful in a simple hub-and-spoke model with the same participant set here (2 parties in the virtual payment channel Alice/Bob over an intermediary).

Do you think there is still a need to create what I think you are suggesting here as a secondary fee to pay for time extensions? Or do you think a hub that is already collecting fees on transaction volume in a virtual channel hub-spoke model would simply elect to keep the channel open to collect these standard hub fees?

---

**ldct** (2018-08-20):

Thanks for the comments!

You are right that one can have more complicated lockup schemes than pay-X-to-lock-up-collateral-until-T. I think of them as trustless derivatives (in the finance sense) on the basic scheme, e.g., a one-sided scheme where the operator could allow the user to close at any time from 0 to T with a fixed interest rate, and collect a premium for the optionality.

One thing to note is that in the case that an intermediary stops intermediating, you lose the scalability benefit of channel networks over channels, so I think they should be incentivized to intermediate for as long as necessary.

Another thing is that the metachannel construction (as well as Perun’s virtual channels) is specifically designed to have the property that the intermediary doesn’t have to give permission (or even know about) every marginal “transaction” the channel is used for, so the “transaction fees” should be expressed as a function of locked time, instead of number of transactions, and we think this more closely matches the cost of capital.

