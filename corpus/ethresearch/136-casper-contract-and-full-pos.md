---
source: ethresearch
topic_id: 136
title: Casper contract and full POS
author: Lars
date: "2017-10-10"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/casper-contract-and-full-pos/136
views: 4179
likes: 9
posts_count: 2
---

# Casper contract and full POS

The hybrid POS implementation will be controlled by an on-chain contract. The drawback here is that messaging is expensive, but not a problem if the stake is big enough.

What is the plan for the full POS implementation, will it also be controlled by an on-chain contract?

The PREPARE  and COMMIT messages seem to be replaced by a VOTE message. Will this change the messaging cost for the hybrid POS, or will it still require approximately the same number of messages?

## Replies

**jonchoi** (2017-10-10):

Not sure about the plans for “full PoS implementation.” However, regarding:

![](https://ethresear.ch/user_avatar/ethresear.ch/lars/48/14_2.png) Lars:

> The PREPARE  and COMMIT messages seem to be replaced by a VOTE message. Will this change the messaging cost for the hybrid POS, or will it still require approximately the same number of messages?

The simplification from `PREPARE` & `COMMIT` to `VOTE` will also be accompanied by two tweaks: (1) epoch time goes from 100 blocks to 50 blocks, and (2) instead of taking one epoch of `PREPARE`s and `COMMIT`s, it takes two epochs of `VOTE`s for checkpoint finalization.

Then, here are the two notable implications: (a) the average time to finalization goes from 150 blocks to 125 blocks (1 + 1/2 100 block epochs vs. 2 + 1/2 50 block epochs), and (b) for a given validator set, **the average number of messages per 100 blocks in the network will remain the same** (because we doubled the # of epochs it takes to finalize a checkpoint but halved the epoch time to 50 blocks).

Hope that answers the second part of your post. This is based on my understanding from discussion with [@vbuterin](/u/vbuterin)  a few weeks back, so feel free to correct if I’m missing anything. Thanks! cc [@virgil](/u/virgil) [@karl](/u/karl)

p.s. Hi everyone! I’m new to this board and to Ethereum research. I will be working on economics of casper, sharding and gas pricing to start. Excited to work with you all  ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

