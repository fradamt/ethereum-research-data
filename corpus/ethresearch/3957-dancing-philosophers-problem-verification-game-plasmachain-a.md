---
source: ethresearch
topic_id: 3957
title: Dancing philosophers problem, verification game, Plasmachain and data availability
author: philosopher
date: "2018-10-26"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/dancing-philosophers-problem-verification-game-plasmachain-and-data-availability/3957
views: 1099
likes: 6
posts_count: 4
---

# Dancing philosophers problem, verification game, Plasmachain and data availability

Hi, everyone! (It’s Philosopher from Onther Inc.)

The **dancing philosophers problem** is a delightful analogy designed to present simple explanations for the data verification game. (Check out our mini-seminar “Plasma for Dummies(KR)” more about the data verification game.) We believe this easy analogy can help you gain a better understanding of the perplexing problem of data availability, which has been propelled into the forefront of much debate in the recent Ethereum community.

> [Medium Post Link]

## Replies

**technocrypto** (2018-10-28):

Hmmmm.  This article seems to be a good effort, but it is not entirely accurate.  For example, the terms “sidechain” and “Plasma” are not used to refer to the same thing.  A “sidechain” means that there is another chain with its own independent consensus mechanism, but that you can move tokens across in some fashion where failure of the sidechain limits the damage to only the tokens which were actually on the sidechain.  On Plasma, by comparison, the failure of the additional “Plasma chain” does not lose *any* tokens, provided that the main chain is still secure.  This is because the consensus rules of the Plasma chain depend on the main chain rather than being independent.  They are not “side to side” and connected.  They are more like “parent and child” where one has the ultimate authority no matter what the other one does.  To make it more clear:  the users of a Plasma chain must watch both the Plasma chain they are using as well as the main chain it depends upon to remain safe.  But the users of the main chain can ignore the Plasma chain.  On a sidechain users from both chains can ignore the other chain for most purposes, so it truly is a “side to side” relationship.  Does my description make sense?

---

**Danny** (2018-10-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/technocrypto/48/2549_2.png) technocrypto:

> On Plasma, by comparison, the failure of the additional “Plasma chain” does not lose any tokens, provided that the main chain is still secure.

Although the main chain is secure, what if the operator who mines each block of *plasma chain* withhold the block of plasma chain ? IMHO in this situation, the user of plasma chain could lose their tokens too . Even if the whole user of the plasma monitor the operator, they cannot prove the data unavailability of the operator. How do you think on this side ?

---

**technocrypto** (2018-10-28):

The entire purpose of a secure Plasma design is to keep users safe even when the Plasma operator disappears, signs invalid or conflicting blocks, or withholds data.  When users see the Plasma block published to the main chain, ask for a copy from the operator, and do not receive it, they immediately have an action they can take to remain safe.  The specific action differs between different Plasma designs, but there is always an action, or the design would not be considered a secure Plasma design.

