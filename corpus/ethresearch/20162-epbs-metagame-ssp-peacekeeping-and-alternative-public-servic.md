---
source: ethresearch
topic_id: 20162
title: "ePBS Metagame: SSP peacekeeping and alternative public service"
author: maxkoeg
date: "2024-07-27"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/epbs-metagame-ssp-peacekeeping-and-alternative-public-service/20162
views: 2706
likes: 1
posts_count: 5
---

# ePBS Metagame: SSP peacekeeping and alternative public service

### Introduction

Alongside Enshrined Proposer-Builder Separation, MEV-Burn is expected to produce a major shift in many on-chain economic and social dynamics. From reducing rugpool incentives to making ReOrg’s even less profitable, this rollout is sure to provide some tangible improvements to the Ethereum protocol, but what seems to get all too frequently overlooked is the on-chain behavioral impact.

If you haven’t already, I would *strongly* recommend taking a peek at both [how i learned to stop worrying and love mev-burn](https://ethresear.ch/t/dr-changestuff-or-how-i-learned-to-stop-worrying-and-love-mev-burn/17384) by [Mike Neuder](https://ethresear.ch/u/mikeneuder), and [Burn incentives in MEV pricing auctions](https://ethresear.ch/t/burn-incentives-in-mev-pricing-auctions/19856) by [aelowsson](https://ethresear.ch/u/aelowsson) as they both inspired me to write this piece and may help decipher some of the more technical details.

As stated in [aelowsson](https://ethresear.ch/u/aelowsson)’s [Burn incentives in MEV pricing auctions](https://ethresear.ch/t/burn-incentives-in-mev-pricing-auctions/19856) there are five types of potential MEV-Burners within pricing auctions:

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png)[Burn incentives in MEV pricing auctions](https://ethresear.ch/t/burn-incentives-in-mev-pricing-auctions/19856/1)

> (A) Public good builder, (B) For-profit public good builder, (C) Extortion racket, (D) Staker-initiated griefing, (E) Staker-initiated griefing cartel.

### PGB Overview

Narrowing in on the Public Goods division, there are several ways to be considered a Public Goods Builder; one being burn rates. Simply put, the more profits a builder dedicates to burning, the more ‘ultrasound’ Ethereum gets, the more deflationary Ether is, and ultimately, the more service is done to the public. This could be a strategy chosen over a For-Profit Builder if the operator determines that the potential social credit outweighs the mere profit a For-Profit Builder would contribute. Once again this motivation would apply to another type of Public Good Builder, an ‘Organic’ Builder. Instead of contributing high burn rates, this builder would rather exclude toxic MEV such as Sandwitching or even swear off censorship, creating a stronger Ethereum protocol rather than just making Ether more economically plausible. Both would be critical to maintaining the integrity and utility of Ethereum, and both can be used in harmony or to different degrees.

In order for a PGB to be nominated to build a block, both a validator would need to value its reputation/social credit over its slot profit and a builder would go through the trouble to construct a public service block. Due to the random nature of POS, even if a validator were to choose a PGB for its block construction it would *not* experience a epoch-over-epoch profit increase, but a builder may. This is touched on later, but the social credit a PGB acquires could bring in more *business* while the randomness of validation ensures that a validator would not.

Some of these public service examples have already been theorized, and many tend to restrict public good opportunities to *just* these examples. If you take anything away from this article, know that this ePBS social layer may be more dynamic than many predict it to be.

### Case Study

When choosing a block builder, validators have a choice; a choice of image; a choice of profit; and ultimately a choice that will contribute to the ePBS social layer. Once again, public service can be attractive to many builders still establishing their image. Potential for this public service can be found even in the ePBS vulnerability of Staker-initiated griefing. (theorized by [aelowsson](https://ethresear.ch/u/aelowsson)) Simply put, SSPs will do anything to remain the most profitable staking model, even if they need to sabotage or grief competing validators. By outbidding other builders, SSP-sponsored builders can achieve the slot held by an opposing validator and tank opposing SSP rewards. This then reduces the average user rewards for competing SSPs and drives users (and fees) to their own platform. One example of alternative public service resides within SSP peacekeeping. By reducing burn rates and including all MEV (including toxic) a for-profit model can be derived. Using liquidity developed via this method can then be used to outbid suspected SSP griefers or even direct bidding aggression at any SSP-sponsored builder, further enforcing ePBS and preventing large validators and builders from being run together again. However, looking past technical difficulties such as identifying SSP builders, this method also proves to be inefficient, as it offers minimal public credit, due to the fact it leverages harmful building practices to enforce SSP unity.

### PGB Efficiency

The efficiency of a public goods builder or PGB is multidimensional, to say the least. Two sections I’ll touch on are popularity efficiency and network improvement-based efficiency.

PBE or Population-Based Efficiency is the simpler of the two and can be represented by the following equation:

E = \frac{pq}{ra}

This equation combines a popularity index (\frac{q}{a}) and a profit margin (\frac{p}{r}); where E is relative efficiency, p is average slot profits, q is average builder pick rate after profit expenditure, r is average slot revenue and a is average builder pick rate before profit expendature.

This equation represents the efficiency of a PGB’s ‘social marketing’. By sacrificing some slot profit a PGB can increase its pick rates and potentially increase its epoch-over-epoch profit or even just control more of the builder market. *Of course, all the while serving the Ethereum public.*

Another form of efficiency modeling is NIBE or Network Improvement Based Efficiency. This model bases the efficiency of a PGB on its actual public service. However, the idea is harder to put an equation behind, as each public service action contributes varying improvements to the network and each have their own relative values.

### The Social Layer

As ePBS rolls out and additional features like MEV burn hit the network, it’s clear that countless social impacts will arise. From SSP sabotage to even the PGB social dynamic, there are many opportunities for cliques, groups, and cartels to form. However, no matter what social problems may arise, any reputable builder will find a way to negate any nefarious builder patterns, and any reputable validators will find a way to support any honest builders. Ultimately, the idea of social credibility and the value of PGB’s may balance the many Immiscible groups that are predicted to form after the introduction of ePBS and MEV burn.

Concluding this paper I would like to, once again, thank both [aelowsson](https://ethresear.ch/u/aelowsson) and [Mike Neuder](https://ethresear.ch/u/mikeneuder) for their wonderful research on MEV burn and pricing auctions respectively. Between PGB dynamics and ePBS metagame, there’s so much more to uncover in this field, so I would like to end by wrapping up this research on PGB dynamics and the resulting social layer by reminding everyone that there is still a world of research to be done.

## Replies

**r4f4ss** (2024-07-28):

Can you elaborate more on the benefit of having a high PGB Efficiency? As far as I understood the builder will leave some profit to have a high E, which seems to be just a point system. Gamification works, but real money, or ETH is more valuable than simple points. I am afraid that only altruistic builders would adhere to this system unless the PGB Efficiency can be converted into something more valuable.

---

**r4f4ss** (2024-07-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxkoeg/48/20268_2.png) maxkoeg:

> This equation combines a popularity index (\frac{q}{a}) and a profit margin (\frac{p}{r}); where EEE is relative efficiency, p is average slot profits, q is average builder pick rate, r is average slot revenue and a is average builder pick rate.

q and a are really the same? Seems a mistake.

---

**maxkoeg** (2024-07-28):

Thanks for the correction, q would be personal pick rate after profit expenditure while a would simply be the chance the builder would’ve been picked before its profit expenditure.

---

**maxkoeg** (2024-07-28):

The idea of the ePBS social layer is as such: if a ‘good’ builder contributes to the network, its peers are generally more likely to choose it again, and if a ‘bad’ builder builds a toxic block, the validator that chose it is now deemed responsible for its toxic acts and may be inclined to avoid that builder in the future. Now, if we consider the economic incentives that may back a builder, we get a system in which both the social credibility of and a builder’s historical profit are taken into consideration. The equation I posted earlier merely identifies if a builders financial sacrifices are providing adequate rewards, in this case a higher chance of being chosen in later slots.

