---
source: ethresearch
topic_id: 4219
title: Increasing decentralization of nodes by reducing power of bigger nodes
author: dremlinit
date: "2018-11-12"
category: Economics
tags: []
url: https://ethresear.ch/t/increasing-decentralization-of-nodes-by-reducing-power-of-bigger-nodes/4219
views: 1017
likes: 1
posts_count: 4
---

# Increasing decentralization of nodes by reducing power of bigger nodes

I’d like to greet you all and inform that i’m a dude who doesn’t have enough knowledge to correctly understand how the casper cbc algorith comes to a conclusion of state, and i dont hang around in ethereum research to understand the correct format of writing these “topics”.

However, i like thinking about game theory and trying to figure out ways to accomplish a certain equilibrium point of node distribution.Reason i am here, posting, is; i think i came up with a probably not an implementable idea, that would help reduce the chances of %51 attack happening and increasing the number of “small eth staked nodes”.

To my understanding, staking works in a way giving power to stake holders, proportionally to the number of eth one has staked. As in someone staking 32 eth has 32Power, someone staking 100 eth has 100Power.

Having a power function somewhat like this(below) might make it harder to accomplish a %51 attack, and incentivize the small eth staker(which probably are the guys who’ll act honest).

Power = numberOfEthStaked + (1/numberOfEthStaked)

This function is pretty close to a flat line, so must be adjusted, but i’m not good at math to calculate a proper function takes all eth at existance into account.

## Replies

**erikryb** (2018-11-12):

The problem with this scheme is that it is susceptible of sybil attacks. What stops a big actor from running many nodes with 32 ETH each?

---

**dremlinit** (2018-11-12):

Well to be honest, i was thinking of the difficulty of managing (total eth staked/2*32) accounts, but propably a way to automate those accounts can be created.

Might reducing the power a total ip can have help prevent sybil attacks?

in such a way that;

Power = numberOfEthStaked + (1/numberOfEthStaked) - (number_of_accounts_per_ip / some_number)

tho since i lack an incredible amount of knowledge in technical details i dont know if this can be implemented

---

**nullchinchilla** (2018-11-17):

IP addresses aren’t measurable or verifiable on the blockchain. Fundamentally a secure, decentralized way of defining “identity” that’s Sybil-proof yet doesn’t allow people with more resources more identities is probably impossible.

