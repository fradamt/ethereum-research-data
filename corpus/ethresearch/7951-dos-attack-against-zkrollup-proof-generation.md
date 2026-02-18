---
source: ethresearch
topic_id: 7951
title: DoS attack against zkRollup proof generation?
author: siburu
date: "2020-09-09"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/dos-attack-against-zkrollup-proof-generation/7951
views: 2828
likes: 3
posts_count: 3
---

# DoS attack against zkRollup proof generation?

I finally realized it when I made a prototype … the bottleneck of zkRollup isn’t in L1 but in L2, to say, in proof generation.

On my laptop (Dell XPS13 9370), it takes ≈1 second to generate zkRollup proof per transaction.

So zkRollup seems not to be suitable to improve “throughputs” unless you use a very expensive EC2 instance or use many instances or invent something smarter…

However, it’s still useful for “gas savings”, to say, batch operations.

You can aggregate 10,000 L2 txs into a single L1 tx after ≈3 hours-long proof generation.

I have a question about this here.

In zkRollup, anyone can be an aggregator.

In other words, anyone can invalidate other aggregators’ ongoing proof generation by executing valid submission to L1, even if other aggregators already spend a long time and much money to aggregate many transactions.

Is there already a workaround for this issue?

## Replies

**adlerjohn** (2020-09-09):

This isn’t really a DoS attack against ZK rollups in general. You don’t need to have an anything-goes-first-come-first-serve leader selection algorithm. I wrote about this further here, under the section “Merged Consensus”:

https://medium.com/@adlerjohn/the-why-s-of-optimistic-rollup-7c6a22cbb61a

A commonly suggested scheme is something like a round-robin with stake. However, your attack is indeed a problem for two desirable features (and because of this attack, these features cannot be safely implemented with a ZK rollup):

1. Force exit and continue. In this feature, a user can request an exit, and the rollup block producer(s) must service it in the next block, after which the rollup chain can continue as normal. This is a DoS vector, as you described the attack, any state transition will invalidate the proof you’re working on. The way force exits must be done is that the ZK rollup chain must be halted if an exit request isn’t processed within some timeout. Obviously not as good as continuing.
2. Pipelining proof generation off-chain with more than one block producer. Having more than one block producer (not at one time, but in general) means that a system can be permissionless. However, since the next rollup block depends on the previous rollup block, the previous block producer can just…not share the block they’re proving with the next block producer, stalling the pipeline. The solution is to do a two-step process, whereby the block is first submitted on-chain, then the proof after a timeout. However, introducing a timeout now means you have a synchrony assumption, which means L1 miners can mess with things, and if you’re not careful your ZK rollup degrades to an optimistic rollup, making all this ZK stuff a waste of time. ZK rollups have a huge number of edge cases you need to be careful with if you don’t want to end up with an optimistic rollup.

These are some of the many downside of ZK rollups compared to [optimistic rollups](https://ethresear.ch/t/minimal-viable-merged-consensus/5617), which don’t have these issues.

---

**siburu** (2020-09-09):

Thank you for pointing them out!

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> A commonly suggested scheme is something like a round-robin with stake.

In such a scheme, a single block producer is elected in a round-robin manner, it gets an exclusive right to submit blocks, but it loses the right if it neglects its task for a certain period of time, right?

If so, the scheme is vulnerable to censorship. The force exit feature can be a gospel but it has a side effect leading to DoS. Hmm…

