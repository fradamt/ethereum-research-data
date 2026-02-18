---
source: ethresearch
topic_id: 2583
title: Atomix protocol in cross sharding
author: xianfeng92
date: "2018-07-17"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/atomix-protocol-in-cross-sharding/2583
views: 2671
likes: 0
posts_count: 5
---

# Atomix protocol in cross sharding

I saw a plan for cross-sharding, named Byzantine Shard Atomic Commit (Atomix) protocol

The program has the following steps：

1 Initialize. A client creates a cross-shard transaction (crossTX for short) whose inputs spend UTXOs of some input shards (ISs) and whose outputs create new UTXOs in some output shards (OSs). The client gossips the cross-TX and it eventually reaches all ISs.

2 Lock. All input shards associated with a given cross-TX proceed as follows. First, to decide whether the inputs can be spent, each IS leader validates the transaction within his shard. If the transaction is valid, the leader marks within the state that the input is spent, logs the transaction in the shard’s ledger and gossips a proof-of-acceptance, a signed Merkle proof against the block where the transaction is included. If the transaction is rejected, the leader creates an analogous proof-of-rejection, where a special bit indicates

an acceptance or rejection. The client can use each IS ledger to verify his proofs and that the transaction was indeed locked. After all ISs have processed the lock request, the client holds enough proofs to either commit the transaction or abort it and reclaim any locked funds, but not both.

3 Unlock. Depending on the outcome of the lock phase, the client is able to either commit or abort his transaction.

In this plan， If all transactions touch all the shards before committing, then the system is better off with only one shard.

What do you think of this plan or any suggestions? Let’s discuss it together. [More details](https://eprint.iacr.org/2017/406.pdf)

## Replies

**vbuterin** (2018-07-17):

This seems like it could be replicated with [cross shard yanking](https://ethresear.ch/t/cross-shard-contract-yanking/1450):

- Yank all input UTXOs into the same shard
- Perform a TX there
- Yank the output UTXOs back into their home shard

---

**xianfeng92** (2018-07-18):

A good plan, but i have a question.What is the improvement by changing the mechanism from “locking” to “yanking” ？ or just say  yanking mechanism will have a better efficiency？ Thank you ~

---

**vbuterin** (2018-07-18):

It’s a simplification. There’s no need to deal with separate “locked” states; the only state that we need to worry about is what shard a contract is in.

---

**xianfeng92** (2018-07-18):

Thank you，  we look forward to the arrival of the sharding

