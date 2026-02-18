---
source: ethresearch
topic_id: 1814
title: PoSW random beacon
author: JustinDrake
date: "2018-04-24"
category: Sharding
tags: []
url: https://ethresear.ch/t/posw-random-beacon/1814
views: 2758
likes: 0
posts_count: 6
---

# PoSW random beacon

**TLDR**: We build upon the idea of using proofs of sequential work (PoSW) for a [clocked proposer sampling mechanism](https://ethresear.ch/t/as-fast-as-possible-shard-chains-with-notarization/1806). By making a number of adjustments we construct a clocked random beacon that can be used as common infrastructure across all shards.

**Construction**

We use notaries as the global set of participants for the random beacon (as opposed to per-shard proposers). The random beacon is used recursively to select ranked notaries at every 5-second period. (Bootstrapping of the recursion is done with nothing-up-my-sleeve randomness near the genesis, specifically to fill the “seeder lookahead” defined below.)

At a given period we label the ranked notaries N_i for i = 0, 1, .... Enforcement of ranking is done via PoSW to give better-ranked notaries an artificial latency edge over lower-ranked notaries. Specifically notary N_i must produce a PoSW with difficulty factor D * i where D is adjusted to target 5-second periods. (Notice the first notary N_0 does not need to produce this PoSW, although there is another PoSW defined below for anti-grinding.)

To participate in the random beacon a notary must reveal a previously-committed hash preimage. (Commitment can be done for example with a hash onion H(H(H(...))).) This reveal process is a way to “reseed” the random beacon. (This is especially important because an ASICed attacker may produce PoSW faster than others.) Specifically the RNG could be the XOR of the fastest-revealed preimage at every period.

The above construction however has a grinding attack. Specifically a top-ranked notary may decide to not participate by not broadcasting the preimage after knowing before everyone else the next RNG output. To address this grinding attack we apply additional sequential work on the fastest-revealed preimage before XORing.

Specifically we apply 5*l-seconds worth of additional sequential work, where l is the seeder lookahead. That is, we use the RNG output that is l periods old as the seed to select the ranked-notaries for the next period. This lookahead allows for the top-ranked notaries to start working on these l-period-old preimages and provide a corresponding timely PoSW at the time of participation.

Setting l=1 or l=2 is possibly good enough in practice. (Formal modelling “à la Cardano” of the beacon and its attacks to choose good parameters can be done after the intuitive idea has been confirmed.) Notice the seeder lookahead does not have to equal the proposer lookahead.

**Discussion**

To abstract the clocked proposer sampling mechanism into a random beacon we’ve made the following changes:

1. Use notaries instead of proposers.
2. Use a recursive strategy instead of bootstrapping from blockhashes. This simplifies the need for synchronisation between period lengths and block times, allowing for shard-native periods “unchained” from the main chain.
3. Mitigate a grinding attack by applying a second round of sequential work.

The random beacon can be used as common infrastructure for all shards, and can be used for things other than proposer sampling. Note also that the proofs of work (see [page 15](https://eprint.iacr.org/2018/183.pdf)) are ~200KB large so reuse across shards is a significant efficiency boost.

To harden the beacon we can also do timestamp comparisons in the context of an assumed global clock and honest majority. We can also apply penalties to notaries that do not participate.

## Replies

**vbuterin** (2018-04-24):

I believe Bram’s PoSW protocol has the property that it doesn’t necessarily produce one unique answer, because you can make a graph that has one error in construction and it will pass the verification check most of the time (this doesn’t break the sequential work property because making a graph with one error still takes almost as much sequential work as a graph without errors). Doesn’t this preclude its use for random beacons at least directly?

---

**JustinDrake** (2018-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Doesn’t this preclude its use for random beacons at least directly?

If by “directly” you mean the equivalent of a nonce/blockhash for PoW, then yes. In the scheme presented however there’s extra structure, namely the hash commitment which has a unique preimage for the corresponding period.

---

**vbuterin** (2018-04-24):

In that case, I’m confused as to how this addresses the grinding vector. The proposer knows ahead of time what the random value is, and has the ability to publish or not publish; if they don’t publish, then someone else will do a PoSW to publish, but the output that they give will be different from yours.

---

**JustinDrake** (2018-04-26):

You’re right! Grinding is not addressed ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) 🤦

---

**vbuterin** (2018-04-26):

And I think in general, making a random beacon out of a PoSW that doesn’t have an additional unique-answer property is super-hard. The reason is that you’re asking for a mechanism that unlocks a random number as soon as and only when *any* value that satisfies a particular predicate (in this case, PoSW verification) is available, which is equivalent to [witness encryption](https://eprint.iacr.org/2013/258.pdf) (which is known to be super-hard). In fact, I think a solution would require not just witness encryption, but also trusted setup.

