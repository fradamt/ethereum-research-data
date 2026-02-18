---
source: ethresearch
topic_id: 1340
title: 30% sharding attack
author: JustinDrake
date: "2018-03-09"
category: Sharding
tags: [random-number-generator, security]
url: https://ethresear.ch/t/30-sharding-attack/1340
views: 2557
likes: 6
posts_count: 4
---

# 30% sharding attack

**Attack**

Let’s assume that an attacker controls some proportion a of validator deposits in the VMC, and some proportion b of mining power in the main chain. Because the current [getEligibleProposer method](https://github.com/ethereum/sharding/blob/develop/docs/doc.md#details-of-geteligibleproposer) is subject to blockhash grinding the attacker can make himself the eligible proposer on a shard (actually, several shards, depending on how fast the attacker can grind) with proportion a + (1 - a)*b.

If we set a = b (i.e. the attacker controls the same proportion of validator deposits and mining power) and solve for a + (1 - a)*a = 0.5 (i.e. solve for the attacker having controlling power) we get a = 0.292. That is, an attacker controlling just 30% of the network can do 51% attacks on shards.

**Defenses**

One defense strategy is to use a “perfectly fair” validator sampling mechanism with no repetitions, e.g. [see here](https://ethresear.ch/t/fork-choice-rule-for-collation-proposal-mechanisms/922). Another strategy is to improve the random number generator to something like RANDAO or Dfinity-style BLS random beacons.

## Replies

**JustinDrake** (2018-03-09):

I think I was being stupid 🤦. The blockhash wraps the over the nonce so blockhash grinding is limited by PoW. Maybe there’s a 30% sharding attack with full PoS, but the situation is not nearly as bad with PoW.

---

**mhchia** (2018-03-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> but the situation is not nearly as bad with PoW

And it seems harder to simultaneously control so many stakes and hashing powers. Don’t know how to measure this kind of hybrid condition. ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

---

**vbuterin** (2018-03-10):

I am inclined to say don’t bother initially for this exact reason. In the longer term, there are better random beacons that we can introduce, and will have to introduce anyway for full PoS.

