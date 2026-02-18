---
source: ethresearch
topic_id: 6616
title: Proof of stake eth1 block proposal based on beacon chain leader selection
author: Pintail
date: "2019-12-11"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/proof-of-stake-eth1-block-proposal-based-on-beacon-chain-leader-selection/6616
views: 1626
likes: 2
posts_count: 8
---

# Proof of stake eth1 block proposal based on beacon chain leader selection

As a way of realising some benefit from the beacon chain even before phases 1 and 2 of eth2 are complete, the proposal for a finality gadget to provide PoS-derived finally to the eth1 PoW chain has been proposed. This idea rests on eth1 nodes including a beacon chain light client to allow their fork choice rule to incorporate finality information from the beacon chain.

However, if eth1 clients already need to include light clients on the beacon chain, why stop there? Couldn’t the random beacon be used to select a leader on the eth1 chain as a block proposer, and cut out PoW entirely? This could happen independently of the ongoing phase 1 and phase 2 research and allow eth1 to gain more of the eth2 benefits sooner (shorter and more evenly spaced block times, stronger security assumptions at lower issuance, greatly reduced energy requirements, lower barrier of entry to validators increasing node diversity).

It seems as though given the scale of ambition for eth2 and a number of significant unsolved problems such as state rent/stateless clients, it may still be years before a wholesale migration to eth2 is possible. Therefore in the mean time are there good reasons *not* to expand the scope of the ‘finality gadget’ aspect of the beacon chain to include eth1 block proposal and eliminate proof of work mining sooner?

## Replies

**lithp** (2019-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/pintail/48/5796_2.png) Pintail:

> Couldn’t the random beacon be used to select a leader on the eth1 chain as a block proposer

Who are the block proposers, and how do you manage updates to that set? The whole point of PoW is that anybody can join, if they can perform enough hashes! If you get rid of the hashes, you need another way of deciding which nodes are acting in the best interests of the network.

---

**Pintail** (2019-12-11):

Various possibilities - a subset of the beacon chain validators, or depositors into a separate eth1 validator contract.

---

**pipermerriam** (2019-12-11):

Interesting idea but I think there are some non-trivial things standing in the way.

1. Being a beacon chain validator has been intentionally designed such that it has low hardware requirements.
2. Eth1.x block creation has a much higher hardware requirement.

So we can’t just use the Eth2.0 beacon chain validators as block creators because that isn’t what they signed up for, nor is it something that they are guaranteed to be able to do.  This leaves us with having to effectively implement all of the same mechanisms that the beacon chain uses to manage the validator pool.

I’ll admit I haven’t thought much about this topic so there might be something obvious I’m missing, but I don’t believe there is a simple route to do what you propose.

---

**Pintail** (2019-12-11):

Thanks. I can see that many of those wishing to become beacon node validates will not have the computational resources to be eth1 block proposers. I guess I was imagining a subset of them would do however. Given the low requirements for the beacon chain, many of the current eth1 miners may well choose to become beacon node validators. They could signal their intention to be block proposers as well as beacon chain validators by depositing to an eth1 contract.

---

**josojo** (2019-12-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Being a beacon chain validator has been intentionally designed such that it has low hardware requirements.

Yes. However, to my understanding, the main reason for these low hardware requirements are  that **validators can easily switch to between the shards**. I think, if we would run the beacon chain with only one shard - the eth1.x shard - then the hardware requirements are not soo bad.

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Eth1.x block creation has a much higher hardware requirement.

Yes ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) But the choice between the wasteful POW and higher hardware requirements in a “1.x shard” system would be an easy decision for myself.

[@Pintail](/u/pintail). Thanks for opening this thread. Today, I had a quite similar idea, and I am happy that you already started the discussion. I would imagine a system, where we

- keeping eth2.0, as it is.
- migrating the current ETH 1.0 chain in a second redeployment of a beacon chain with one single shard and a little bit higher hardware requirements.

Of course, the long term plan would be to merge these two beacon chains with new technologies like stateless clients etc…

---

**lithp** (2019-12-12):

Linking in [this thread](https://ethereum-magicians.org/t/finality-gadget-for-ethereum1x-working-group/3177) from eth-magicians which seems related.

---

**siliconMan** (2019-12-15):

It seems worthy of putting some thought into this.  Switching 1.x to POS would give the current 5000+ node operators a way to make money from staking, and get rid of the massively wasteful GPU mining.    Anyone running an ETH 1.0 node now could easily spin up a 2.0 Beacon node on the same machine without increasing hardware requirements much if at all.

It’s basically going back to separating Casper from Sharding, and implementing Casper POS first.  Huge Benefits if it’s possible:

- Faster, consistent block times.  With 1559, almost all transactions go through in  Of course, the long term plan would be to merge these two beacon chains with new technologies like stateless clients etc…

I think that there could still just be a single production beacon chain.  The second one would be a testnet for 2.0 technologies.

