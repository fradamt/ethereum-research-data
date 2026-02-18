---
source: ethresearch
topic_id: 1679
title: Offchain collation headers
author: JustinDrake
date: "2018-04-09"
category: Sharding
tags: []
url: https://ethresear.ch/t/offchain-collation-headers/1679
views: 5624
likes: 5
posts_count: 7
---

# Offchain collation headers

**TLDR**: We propose a sharding strategy where collation headers are kept offchain, i.e. off the main chain. Potential benefits include:

1. No censorship of collation headers by main chain miners or validators
2. No gas fees for inclusion of collation headers, avoiding stalled shards if main chain gas prices skyrocket
3. Faster periods (e.g. 5-second periods) compared to the currently proposed 75-second periods
4. Lower variance periods compared to the main chain’s high-variance block times
5. No collation header processing bottleneck, allowing for more shards
6. Shard upgradability without main chain forking
7. Cheaper protocol-layer signature abstraction
8. Faster finality (~7.5 seconds on average) compared to ~2 weeks pre-Casper and ~20 minutes post-Casper
9. Competing sharding implementations running off the main chain

For simplicity of exposition we use Dfinity chains as described in their [consensus whitepaper](https://dfinity.org/pdf-viewer/pdfs/viewer?file=../library/dfinity-consensus.pdf), although other constructions may be more suited. Special thanks to [@karl](/u/karl) for collaborating on this.

**Construction**

The SMC in the main chain allows for notaries to post fixed-size ETH deposits. We assume 2/3 of the notaries are honest, and that the main chain reaches finality in `MAIN_CHAIN_FINALITY := 40320` block times (~2 weeks).

We now instantiate a Dfinity chain called the “beacon chain” that sits below the main chain. The beacon chain provides a high-grade random beacon with a low-variance period length of 5 seconds. The beacon chain processes all transactions necessary for the random beacon, in particular the BLS Distributed Key Generation (DKG) transactions. The beacon chain processes no user transactions.

The beacon chain and the main chain are synchronised via beacon checkpoints posted on the main chain. A beacon checkpoint is a beacon output that occurs every ~10 minutes, i.e. for which the period number is a multiple of `BEACON_CHECKPOINT_GRANULARITY := 120`. Not all checkpoints have to be included in the main chain. We want chronological ordering of the beacon checkpoints which can be enforced by the SMC or via client-side filtering. Notice the beacon output chain is forkfree so beacon checkpoints don’t roll back.

Synchronisation allows for unambiguous two-way light-clienting:

- Main chain light-client for the beacon chain: At period p the beacon chain finds the most recent beacon checkpoint in the main chain with period at most p - MAIN_CHAIN_FINALITY * 3 and uses the post-state root of the block containing that checkpoint for light-clienting. In particular, the beacon chain uses the set of deposits as specified by the main chain light-client, which is final and well-defined at every period of the beacon chain.
- Beacon chain (and shards) light-client for the main chain: At block b the main chain finds the second most recent beacon checkpoint included in the main chain. This checkpoint is at least 10 minutes old which is enough for finality of the beacon chain (and the shards). Indeed, assuming the worst case where an attacker has 1/3 of the deposits and he always successfully causes the committees to sign off on equivocated proposals at every height then the attacker can cause competing forks to last 10 minutes with probability 1/3^{120} < 10^{-57}.

We now instantiate the shards below the beacon chain. Those are Dfinity chains which use the random beacon from the beacon chain. In other words, a committee of size 423 (honest majority with high probability) is randomly sampled for every collation at every period and for every shard, along with ranked proposers. The collations are notarised for availability via quorums of size 212.

![image](https://yuml.me/diagram/scruffy/class/%5BMain%20chain%20(for%20deposits)%5D%20-%3E%20%5BBeacon%20chain%20(for%20RNG)%5D%2C%5BBeacon%20chain%20(for%20RNG)%5D%20-%3E%20%5BShard%201000%5D%2C%5BBeacon%20chain%20(for%20RNG)%5D%20-%3E%20%5B...%5D%2C%5BBeacon%20chain%20(for%20RNG)%5D%20-%3E%20%5BShard%201%5D)

**Discussion**

The beacon chain acts as a “synchronised sidechain” to the main chain. Separation of concerns (deposits management vs beacon management) reduces load on the main chain and allows for upgradability of the sharding infrastructure (beacon chain and shards) without forking the main chain. More importantly, the beacon chain and the shards operate “unchained” (pun unintended ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)) from the limitations of the main chain, especially with regards to censorship, gas price, period length and period variance. This is somewhat reminiscent of plasma chains, but without the exit mechanism.

Interestingly in this construction the shards have better finality than the main chain despite shard security deriving from that of the main chain. One reason is that the shards only care about deposit snapshots from the main chain’s finalised past. This is somewhat reminiscent of state channels being able to provide instant game theoretic finality via deposits.

An important consideration is the bottlenecks of the [sharding phase 1 draft spec likely to be retired](https://ethresear.ch/t/sharding-phase-1-spec/1407), of which there are three:

1. Collation header processing: Processing of collation headers is now distributed across shards instead of being centralised in a single chain. This bottleneck goes away here, allowing for 1000 shards instead of 100.
2. Light-client access: Every shard has (delayed) light-client access to every other shard. With 200 bytes headers, 1000 shards and 5-second periods the bandwidth overhead is 200*1000/5 = 40kB/s. The double-batched Merkle accumulator imposes a storage overhead of ~1MB for light-client access across all shards. This bottleneck is not too constraining.
3. Notary bandwidth: Assuming 10,000 notaries, 1000 shards, 50kB collation bodies, and 5-second periods we get a notary bandwidth of 423kB/s. This is the only significant bottleneck for going above 1000 shards, and it is potentially addressable with erasure codes.

As a final remark, notice the main chain can provide basic infrastructure for different sharding implementations running in parallel. This basic infrastructure could be deposits, a RNG scheme, a commitment scheme, a challenge-response game, checkpoints, etc. This makes the main chain a uniquely well suited platform for the bootstrapping, experimentation and competition of sharding designs.

## Replies

**vbuterin** (2018-04-09):

> This bottleneck goes away here, allowing for 1000 shards instead of 100.

I really don’t think it does. Notaries that are running the finality loop will still need to verify all of the committees to make sure that they’re finalizing data that has actually been approved by the committees, so they will still have to process all signatures from all committees themselves.

And the overhead to do that is 212 * 1000 / 5 = 40000 messages per second, which is… quite a lot.

Additionally, how are you making Casper FFG rounds complete in 7.5 seconds? What is the global hash that everyone is signing on? Part of the reason why it’s important for shard headers to get rooted in the main chain is so that they do get incorporated into a global data root that represents the history of all shards, which the Casper FFG cycle can then easily finalize over.

---

**MaxC** (2018-04-09):

Hey nice work!  I have one worry about the Dfinity scheme and please correct me if I’m wrong.

Isn’t the issue with Dfinity that the random beacon groups are only selected dynamically but generated well in advance?

This  means you’ve got a relatively stable group who can be bribed and corrupted to not produce the next random number.

So to ensure liveness, I think this scheme (and Dfinity) would require another check to ensure that if a beacon group stalls, a new threshold group could be selected.

---

**JustinDrake** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Notaries that are running the finality loop will still need to verify all of the committees to make sure that they’re finalizing data that has actually been approved by the committees, so they will still have to process all signatures from all committees themselves.

With Dfinity chains there are two optimisations. The first is that full notarisation of a collation implies full notarisation of all previous collations on that shard. The reason is that committees only notarise previously notarised collations. So a notary summoned to notarise a collation at some height `h` only has to check the signatures for the collations of that shard at height `h - 1` (usually a single collation, unless there is equivocation of the top-ranked proposer and multiple notorisations). The second optimisation is that BLS signatures aggregate, so only a single signature has to be checked instead of 212 per collation.

With 10,000 notaries and 1000 shards, a notary will be summoned to notarise 42.3 shards per period, which corresponds to checking 42.3 signatures per 5 seconds, i.e. less than 10 messages per second.

Other signature tricks may be applicable to non-Dfinity designs, such as [“diagonal” staggering and “horizontal” bursts](https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638) or [cryptoeconomic signature aggregation](https://ethresear.ch/t/cryptoeconomic-signature-aggregation/1659).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> how are you making Casper FFG rounds complete in 7.5 seconds?

I’m not. I’m not even assuming any form of Casper in the design. I guess the point is that the time to finality of the shards is independent from the time to finality of the main chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What is the global hash that everyone is signing on? Part of the reason why it’s important for shard headers to get rooted in the main chain is so that they do get incorporated into a global data root that represents the history of all shards, which the Casper FFG cycle can then easily finalize over.

What gets explicitly included in the main chain via transactions are the (unique deterministic) beacon checkpoints, at most one per 120 periods. The second-most recent beacon checkpoint is the “global hash” that Casper FFG can finalise over. Beacon checkpoints are separated by 10 minutes which is enough for shard finality, so the second-most recent beacon checkpoint will have corresponding finalised data roots, one for each shard. The data roots are not made explicit with a transaction, instead they come from light-clienting (similar to every shard light-clienting every other shard). A global data root can be computed by Merklelising the individual shard data roots corresponding to beacon checkpoints.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> Isn’t the issue with Dfinity that the random beacon groups are only selected dynamically but generated well in advance?

Right, committees are selected in advance, which opens the door for adaptive attacks. It is possible that Dfinity’s 2/3 honesty assumption (which subsumes adaptive attacks) is unrealistic; time will tell. The good news is that the honesty assumption can easily be put to test without tight-coupling the shards to the main chain.

---

**vbuterin** (2018-04-09):

> What gets explicitly included in the main chain via transactions are the (unique deterministic) beacon checkpoints, at most one per 120 periods. The second-most recent beacon checkpoint is the “global hash” that Casper FFG can finalise over.

Ah, I see. Missed that part. That actually aligns well with the general approach I just finished writing up today ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) [Off-chain intermediate blocks](https://ethresear.ch/t/off-chain-intermediate-blocks/1680)

I’m not convinced that a separate random number chain is worth the complexity, but aside from that the paths seem similar.

---

**JustinDrake** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> That actually aligns well with the general approach I just finished writing up today

Right, both approaches are part of a spectrum in regards to what gets included in the main:

- The original design includes a root per period and per shard
- Your design includes a root per epoch and per shard
- My design includes a root per epoch

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I’m not convinced that a separate random number chain is worth the complexity

The separate beacon chain buys you two things:

1. There is a notion of “global root” for all shards simultaneously, providing sublinear (actually, constant) main chain overhead. This removes the main chain as a bottleneck.
2. Like the shard execution layer, the global root is not a consensus game, so has no forking and rollbacks. So even if a shard rollbacks for whatever reason, the main chain doesn’t need to rollback itself. This is relevant pre-Casper and pre-tight-coupling. Even after tight-coupling, having shard light-clienting in the main chain have a more conservative delay than the Casper time to finality provides extra robustness to the main chain, something consensus-driven data roots doesn’t readily provide.

---

**jamesray1** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Potential benefits include:

It would be good if you could list potential cons too, e.g. it is no longer possible to check logs of collation headers (which could be emitted if they were created on-chain) e.g. as per [Per period committee snapshot - #9 by hwwhww](https://ethresear.ch/t/per-period-committee-snapshot/1703/9). If there are no logs on chain then you can’t use them for fast syncing or light syncing, so you’d need to either get them from off-chain (which doesn’t seem secure) or find another way for these syncing methods.

