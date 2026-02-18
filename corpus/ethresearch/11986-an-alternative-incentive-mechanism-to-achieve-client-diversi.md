---
source: ethresearch
topic_id: 11986
title: An alternative incentive mechanism to achieve client diversity
author: ammarlakho
date: "2022-02-10"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/an-alternative-incentive-mechanism-to-achieve-client-diversity/11986
views: 2794
likes: 5
posts_count: 4
---

# An alternative incentive mechanism to achieve client diversity

Client diversity for the consensus layer is currently a major problem with Prysm having >[70%](https://www.slashed.info/) of all staked eth.

As described [here](https://blog.ethereum.org/2020/01/13/validated-staking-on-eth2-1-incentives/), slashing (when a staker goes down) is directly proportional to the number of stakers that go down alongside. So if there’s a bug in one client implementation, all the stakers using that client will go down and result in a greater amount being slashed.

Currently, the incentive to switch from Prysm and use a minority client is to avoid the possibility of losing a greater % of your stake when things don’t go to plan (a rare occurrence ideally). This might not be an important enough reason for stakers to switch since switching requires some effort. However, how about we flip the incentive mechanism and reward people for using a minority client. A staker’s reward can be inversely proportional to the number of stakers using that particular client. When stakers using a majority client see an easy way to increase their APY, they will be more motivated to switch clients and a market equilibrium can be reached much more quickly.

This mechanism would require the following 2 things:

1. A tamper-proof way to determine which client is being used by a staker.
2. A mathematical formula to determine how the reward will vary depending on the client you are using. This can be similar to the quadratic inactivity leak formula being used to calculate the amount to be slashed when a staker’s node goes down.

Interested to receive some feedback regarding the feasibility of such an approach and how we could come up with a tamper-proof way of determining a staker’s client.

## Replies

**MicahZoltu** (2022-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/ammarlakho/48/7081_2.png) ammarlakho:

> A tamper-proof way to determine which client is being used by a staker.

This is the very hard (maybe impossible) part of the problem, and it is necessary to implement something like this.

---

**caiosabarros** (2022-03-12):

Wouldn’t this be a huge incentive to the creation of many clients - which would decrease the quality of the network because of low-quality clients and possible errors? For example, I would then prefer to build my own client so that I can use it by myself without sharing it with anyone else - and then I would receive as many incentives as I could…

---

**jrausch12** (2024-01-25):

I would like to revive this thread given the recent bugs we have seen in nethermind and besu. The incentive math should have an upper and lower limit to it to stem the “I’ll fork a client and make it my own 1/1” issue. I think this is something that can be codified into the protocol so long as the emission of the client’s identity becomes non-fungible and a mechanism is placed in that allows for client info emission to be consumed by the protocol.

