---
source: ethresearch
topic_id: 5460
title: Can P.o.S. assist distributed computing?
author: Econymous
date: "2019-05-16"
category: Applications
tags: []
url: https://ethresear.ch/t/can-p-o-s-assist-distributed-computing/5460
views: 1382
likes: 1
posts_count: 5
---

# Can P.o.S. assist distributed computing?

I was wondering if P.o.S. could help secure distributed computing processes? Simulations or MMO’s

I’ve been working on a scaling solution where sidechains behave like multiple threads. So I wanted any feedback to keep that in mind.

I’ve got a hunch right now, but I just want to make sure so I can plan a research trajectory after my solution.

## Replies

**adlerjohn** (2019-05-16):

Proof-of-Stake on its own doesn’t provide meaningful scalability benefits (constant blocktimes only provide a small constant-factor improvement at best). Proof-of-Stake side chains aren’t a scaling solution—in fact any side chain with its own separate security pool (*i.e.*, a completely separate consensus protocol) on their own isn’t a scaling solution. A scaling solution needs to be, among other things, scalable *and secure*. The problem with side chains with their own consensus protocol is that they will be easier to attack than the main chain (*i.e.*, Ethereum).

The proposed solution for ETH 2.0 is to randomly sample from a single security pool—the beacon chain—to drive the consensus protocols of many side chains—the shard chains. You’re welcome to contribute to this effort, or re-invent the wheel with your hunch.

---

**Econymous** (2019-05-16):

I have a solution for the degrading security at each layer with nested sidechains.

So just for the sake of this discussion let’s assume that nested childchains are fully feasible. (yes, i know, hard to believe, but i’ve got a really good solution… i’m trying to finish up the website now, i’ve written the smart contract i just gotta do the data visualization for the pie chart)

So, if that’s a given. is there anyway that P.o.S. can be used in parallel with a distributed computing process?

---

**adlerjohn** (2019-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/econymous/48/11192_2.png) Econymous:

> is there anyway that P.o.S. can be used in parallel with a distributed computing process?

That’s literally what sharding is. If you’ve found a way to drive consensus on shard chains without random sampling from a single security pool then by all means publish your work so it can be reviewed.

---

**Econymous** (2019-05-16):

I mean general computational tasks. Like running an MMO or physics simulation.

I am trying to launch on ropsten. I’m not the best at writing. A whitepaper  (as you can see in my original thread)

All I know is the pie charts have to be fair every layer within nested sidechains.

Fair distribution at every layer like in this illustration https://youtu.be/zxToXSe3d6A

Here’s my amateur white paper.


      [docs.google.com](https://docs.google.com/document/d/1U2WAPDdsgVq4SsFaWhHTjkkn_P-R6ZusDIKyhS5NWhY/edit)


    https://docs.google.com/document/d/1U2WAPDdsgVq4SsFaWhHTjkkn_P-R6ZusDIKyhS5NWhY/edit

###

Resolve Token Distribution Rough Draft by Econymous | Review and Edited by: Maxie the Crypto Writer  Fair distribution can be accomplished through a smart contract that functions as a pyramid scheme which inverts a centralizing force as an incentive...








Is there a Proof of stake sidechain repo I can clone? I tried loomx but it’s proof of authority.

