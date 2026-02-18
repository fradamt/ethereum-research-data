---
source: ethresearch
topic_id: 5459
title: Is a Tree of Pyramid schemes our best bet for a scaling solution?
author: Econymous
date: "2019-05-16"
category: Layer 2
tags: []
url: https://ethresear.ch/t/is-a-tree-of-pyramid-schemes-our-best-bet-for-a-scaling-solution/5459
views: 1838
likes: 0
posts_count: 5
---

# Is a Tree of Pyramid schemes our best bet for a scaling solution?

Is that clickbaity?

Here’s what I need to know. Once an atomic swap is complete, there’s no need to interact with the asset’s original chain until someone wants to redeem that asset.

I’ve assumed it to always be like this. Once an atomic swap has been completed, you basically have a voucher for the asset that you can redeem at anytime.

Is **the only reason** we haven’t made nested Proof of stake side/child chains because we lose security against 51% attacks at every deeper level?

If the above is true, then I believe I have a scaling solution.

If it’s not, then I am crazy, and I need to be checked into a mental health facility.

---

What is the scaling solution? Well. it’s nested sidechains. How can we ensure their security? inverting pyramid scheme smart contracts so that losers get more tokens the more they lose in the pyramid.

## Replies

**adlerjohn** (2019-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/econymous/48/11192_2.png) Econymous:

> Is the only reason we haven’t made nested Proof of stake side/child chains because we lose security against 51% attacks at every deeper level?

Yes, but not exactly for *nested PoS* side chains. Just side chains in general. Increasing throughput by diluting security (i.e., by having each side chain run its own consensus protocol and trusting it hasn’t been attacked) is a non-starter.

![](https://ethresear.ch/user_avatar/ethresear.ch/econymous/48/11192_2.png) Econymous:

> inverting pyramid scheme smart contracts so that losers get more tokens the more they lose in the pyramid.

Can you provide some more details on how this works, precisely? Lose where? I would argue that proving you lost money due to an insecure side chain is isomorphic to proving you haven’t lost money.

---

**Econymous** (2019-05-16):

It blows my mind. You’re telling me everything I need to hear.


      [docs.google.com](https://docs.google.com/document/d/1U2WAPDdsgVq4SsFaWhHTjkkn_P-R6ZusDIKyhS5NWhY/edit)


    https://docs.google.com/document/d/1U2WAPDdsgVq4SsFaWhHTjkkn_P-R6ZusDIKyhS5NWhY/edit

###

Resolve Token Distribution Rough Draft by Econymous | Review and Edited by: Maxie the Crypto Writer  Fair distribution can be accomplished through a smart contract that functions as a pyramid scheme which inverts a centralizing force as an incentive...








tldr: you can create a pyramid scheme smart contract. You calculate the loss & use it as a multiplier when rewarding tokens after someone “sells” out of the contraccs. Those tokens are used to stake the childchain. These token’s can’t be whaled out (no matter how bad the supply inflates) because people are incentivized  to create them, by take greater and greater losses in the pyramid smart contract.

---

Fortunately this isn’t all just words. I’m currently debugging the smart contract & intend to launch a demo so everyone can see the pie chart.

i’m not keen on communication, so i just gotta push this out asap

---

**Econymous** (2019-05-19):

Here’s what the code looks like.

Hopefully this makes a bit more sense

---

**Econymous** (2019-05-22):

It’s on ropsten testnet.

The website’s a bit broken. it requires metamask to work, I’ll fix that shortly.

http://terrible-music.surge.sh/#/market

the website can now load without metamask, but the exchange can not be seen without metamask. working on that. now

