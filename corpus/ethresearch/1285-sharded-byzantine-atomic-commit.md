---
source: ethresearch
topic_id: 1285
title: Sharded Byzantine Atomic Commit
author: musalbas
date: "2018-03-02"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/sharded-byzantine-atomic-commit/1285
views: 5316
likes: 4
posts_count: 8
---

# Sharded Byzantine Atomic Commit

I’ve just read up on Ethereum’s sharding documents (and am currently reading all the threads here), and hope to contribute some ideas. Given the recent threads on [cross-shard locking schemes](https://ethresear.ch/t/cross-shard-locking-scheme-1/1269), I thought it would be a good time to jump in.

I’d like to introduce Sharded Byzantine Atomic Commit (S-BAC), a correct inter-shard consensus algorithm for atomic commitment. Unlike previously proposed algorithms, S-BAC does not rely on the client being honest to guarantee liveness, and thus no lock time-out period for clients is required to prevent deadlocks. The liveness property depends on shards being honest.

For the full details and security proofs, see page 7 of our [Chainspace paper](https://arxiv.org/abs/1708.03778).

Here is an overview of the protocol:

[![image](https://ethresear.ch/uploads/default/optimized/1X/10b114b093c3313c564a00c8103d289941435f5a_2_690x283.png)image744×306 35.6 KB](https://ethresear.ch/uploads/default/10b114b093c3313c564a00c8103d289941435f5a)

The protocol is agnostic to the actual BFT protocol algorithm used - that is, it doesn’t matter if you use PBFT or a blockchain + proof-of-work/proof-of-stake. For the evaluation of the protocol in the paper, we used PBFT.

There are some optimisations that can be made when using a blockchain + proof-of-work/proof-of-stake, however. For example, if a shard includes a prepared(accept, T) message on the blockchain for a transaction T, but T eventually gets aborted, then that can be considered to be a waste of space on the blockchain. In another post, I will propose a way to safely and permanently prune such messages from the blockchain, even from archival nodes, so that they are not needed to bootstrap a full node.

## Replies

**MaxC** (2018-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> I’d like to introduce Sharded Byzantine Atomic Commit (S-BAC), a correct asynchronous intra-shard consensus algorithm for atomic commitment. Unlike previously proposed algorithms, S-BAC does not rely on the client being honest to guarantee liveness, and thus no lock time-out period for clients is required to prevent deadlocks. The liveness property depends on shards being honest.

Hey, nice work Musalbas! Can you please say a few words to give the intuition of  how your system works? Seems from the diagram that you are using pBFT to agree on cross shard transactions, but for transactions that take place within a single shard I guess the pBFT mechanism is not necessary.   How will this system scale if many transactions are cross shard and thereby must be shared with all other shard members?

---

**kladkogex** (2018-03-02):

Mustafa -  so judging from the picture this would require n^2  messages where n is the number of shards, since each shard sends messages to each other shard.

Why would not you use one shard as  a leader if all shards are good anyway :-))  Then it would be n

---

**musalbas** (2018-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> Hey, nice work Musalbas! Can you please say a few words to give the intuition of  how your system works? Seems from the diagram that you are using pBFT to agree on cross shard transactions, but for transactions that take place within a single shard I guess the pBFT mechanism is not necessary.   How will this system scale if many transactions are cross shard and thereby must be shared with all other shard members?

See page 7 of [the paper](https://arxiv.org/abs/1708.03778). It works similarly to a two-phase commit. We’re not using PBFT in the diagram; any BFT protocol works (e.g. blockchain + proof-of-work). The prototype uses PBFT. For single-shard transactions technically you don’t need the two-phase commit, you can just commit the transaction in one phase.

The more shards each transaction touches, the lower the throughput, as once you have a situation where all transactions touch all shards, that’s effectively equivalent to having a non-sharded blockchain. Here’s a graph:

[![image](https://ethresear.ch/uploads/default/original/1X/3c41c4163a7c9d6537c12f004763c3e6a8f3f520.png)image360×316 17 KB](https://ethresear.ch/uploads/default/3c41c4163a7c9d6537c12f004763c3e6a8f3f520)

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Mustafa -  so judging from the picture this would require n2n^2  messages where nn is the number of shards, since each shard sends messages to each other shard.
>
>
> Why would not you use one shard as  a leader if all shards are good anyway :-))  Then it would be nn

I think you could as if any shard that a transaction touches is dishonest, then liveness is compromised. However, if the leader shard is dishonest, then that further allows them to potentially frame other shards as being byzantine, by not relaying their messages, to block transactions from progressing.

---

**MaxC** (2018-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

>

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> The protocol is agnostic to the actual BFT protocol algorithm used - that is, it doesn’t matter if you use PBFT or a blockchain + proof-of-work/proof-of-stake. For the evaluation of the protocol in the paper, we used PBFT.

I think we could combine your work and mine so shards request locks, ensuring liveness, but not all locks need be acquired in a given round.

---

**xianfeng92** (2018-07-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> The more shards each transaction touches, the lower the throughput, as once you have a situation where all transactions touch all shards, that’s effectively equivalent to having a non-sharded blockchain.

so，is there a related solution to optimize it?

---

**musalbas** (2018-07-18):

It’s not really a problem, but a natural property of sharding. If you want to make a transaction that modifies state in multiple shards, all of those shards have to be involved in some way, you physically can’t do better than that.

---

**xianfeng92** (2018-07-18):

a good allegory, thank you ~

