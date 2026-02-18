---
source: ethresearch
topic_id: 3097
title: Simple synchronous cross-shard transaction protocol
author: vbuterin
date: "2018-08-26"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/simple-synchronous-cross-shard-transaction-protocol/3097
views: 7986
likes: 2
posts_count: 12
---

# Simple synchronous cross-shard transaction protocol

Status: an idea I’ve already talked with some people before, but still deserves to be written up in one place and hasn’t yet.

We already know that it is relatively easy to support [asynchronous cross-shard communication](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#how-can-we-facilitate-cross-shard-communication), and we can extend that to solve train-and-hotel problems via [cross-shard yanking](https://ethresear.ch/t/cross-shard-contract-yanking/1450), but this is still highly imperfect, because of the high latency inherent in waiting for multiple rounds of cross-shard communication. Being able to perform cross-shard operations synchronously, in one transaction, would be ideal. But how do we do this?

First of all, a solution would inherently require data/state execution separation. To see why, suppose that there is a transaction between shard A and shard B, that depends on state and makes changes in both shards. For simplicity, suppose that the transaction is trying to book a train and hotel. Head of the chain is in green.

![image](https://ethresear.ch/uploads/default/original/3X/8/2/8213498c8cb9421ef780d2e8932d1528a47c443a.svg)

Now, suppose that shard A reorgs, but **not** shard B.

![image](https://ethresear.ch/uploads/default/original/3X/c/c/cc151d74f2a9618b3451bec6e81208c78aa7bfb0.svg)

Oh no! The hotel is now booked and not the train. To avoid this, we would have to add a fork choice rule where A2 no longer being part of the canonical chain would also kick B2 off the canonical chain, but this would mean one single reorg on one shard could potentially destabilize every shard.

The abstraction that we use instead is the state execution engine. We suppose that a node is aware of the state of one shard (without loss of generality, shard A) at height N-1, and the state roots of all other shards at height N-1, and the correct block hashes at height N (and the full block for shard A), and its job is to compute the state of shard A and learn the state roots of all other shards at height N. Notice that we assume that correct block hashes are pre-provided; if any shard reverts then the execution process will need to revert, but the ordering of data on all other shards would be preserved.

Green is known state, grey is unknown state, yellow are blocks, squares are roots, circles are full data.

![image](https://ethresear.ch/uploads/default/original/3X/9/f/9f498de881a4c7e6a22eec5464e67a03f1865511.svg)

We define a block as containing a sparse Merkle tree (or Patricia tree or any similar key-value structure) of transactions, mapping `address => tx`. Each transaction is itself a bundle `[shard[1], address[1], shard[2], address[2] ... shard[n], address[n], data]`. For a transaction `tx` in any shard to get executed, it must meet the following condition: for all (shard, address) pairs specified in the tx, accessing the key-value tree of block N of the given shard at the given address should return the transaction. That is, if the transaction specifies `[A, 123, A, 485, B, 769, data]`, then for `data` to get executed the transaction must appear at position 123 of block N in shard A, position 485 of block N in shard A and position 769 of block N in shard B.

Note that this requirement makes it impossible to have two transactions at the same height that affect the same account. This is by design. Otherwise, it would be possible to have towers of transactions that depend on each other, requiring clients to recursively download very large sets of transactions from other shards to verify a given transaction within their own shard. One possible compromise would be to allow unlimited transactions *within* a shard that do not even need to specify addresses, but that are always executed *after* the cross-shard transactions.

A client can implement this model as follows:

1. Download block N on shard A.
2. Collect all “foreign references” (that is, address references in transactions in shard A that come from other shards). For each foreign reference, ask the network for a Merkle branch for the state of the associated address from height N-1, and the block at the given position at height N.
3. For all transactions in shard A, verify that the references are consistent; that is, for every reference (s_id, addr) in a transaction T (foreign or local), verify that the value of the block of shard s_id at position addr is also T, using the data acquired in stage 2 for foreign references. If it is not, throw the transaction out.
4. For every transaction that passed step (3), execute it, using the state data acquired in stage 2.
5. Use cryptoeconomic claims, ZK-SNARKs, or any other mechanism to gather an opinion about the state roots of other shards at height N.

To keep heights perfectly synchronized, we can use slot number instead of height; if a given slot number on some shard is missing, we treat that as an empty block. Note that this algorithm requires two rounds of network communication per height: one to fetch foreign Merkle branches, and another to gather claims about state roots of other shards.

## Replies

**djrtwo** (2018-08-27):

How do you propose a client attempting to conduct a multi-shard tx coordinate their tx to be included at the same slot for each shard in question?

---

**vbuterin** (2018-08-27):

Here’s a simple but still imperfect take: switch the blockchain over to [self-targeting minfees](https://github.com/zcash/zcash/issues/3473) so that inclusion in the next block can be more easily guaranteed. Then, just trying to send a transaction into each shard at the same time should have a >90% success rate in any given shard, so would require trying ~1.11^N times for a cross-shard transaction affecting N shards.

This is probably most problematic against malicious proposers; to defend against this, we could have the execution be over a 2-block range instead of a 1-block range.

---

**cdetrio** (2018-08-29):

The way I imagine it, during the block proposal stage (as opposed to the state execution) the tx only needs to be included in the “originating” shard (the shard where the tx `from` address resides. or in a null_sender/account abstraction model, the `to` address).

All shard validators are light clients for all shards, right? Then during state execution (this is delayed state execution, so validators are making state root claims well after blocks have been proposed), validators look at the shard block headers for all shards, to see if there are any cross-shard transactions which touch that validator’s shard at that slot.

---

**vbuterin** (2018-08-29):

That would not work. Suppose a transaction in shard B1 affected (A.x, B1,y), and a transaction in shard B2 affected (A.x, B2.y) … up to B100. Suppose the B[i] is always the originator. Then, there would be 100 transactions touching A where the execution of any one transaction would depend on all of the previous transactions, and there would be no limit to how high the tower could go. Alternatively, one could imagine a chain of transactions (B1.x, B2.x), (B2.x, B3.x) …, each of which depended on the outcome of the previous, so calculating the result of (B99.x, B100.x) would require calculating the transactions on all other shards.

---

**cdetrio** (2018-08-29):

I don’t understand your notation (x/y/B2.y/etc), but what if each shard is constrained to only have one cross-shard transaction per block? Then if there are 100 shards, the tower is limited to 100 transactions.

---

**vbuterin** (2018-08-29):

Sorry, (A.x, B.y) means “a transaction that affects account x of shard A and account y of shard B”.

Sure, if you constrain each shard to have one cross-shard transaction per block, that would actually limit the tower to *one* transaction because it would force disjointness. But that’s a very low level of throughput to be targeting.

---

**cdetrio** (2018-08-29):

I’m thinking the constraint is that each shard can only have one originating transaction, so with 100 shards that’s 100 transactions, and to be extreme suppose each tx touches all 100 shards.

Once concern with synchronous cross-shard tx’s in a delayed state execution model is that the state execution gadget (which is not a consensus game) won’t be able to keep up with block proposals/finalization (the consensus game at the data layer). If the cross-shard throughput is constrained enough, then it should be able to keep up.

It will be progress to recognize that we have a protocol that works, even if it is low throughput. Currently few people accept that cross-shard synchronous transactions can work, so just adding to the phase II roadmap a bullet point that says we can have 1 cross-shard tx per block would be great progress. Once we can accept 1 (if not 100) cross-shard tx’s per block, then we can move on to discussing optimizations and relaxing the constraints to achieve higher throughput.

---

**vbuterin** (2018-08-29):

> Once concern with synchronous cross-shard tx’s in a delayed state execution model is that the state execution gadget (which is not a consensus game) won’t be able to keep up with block proposals/finalization (the consensus game at the data layer)

Why wouldn’t it? As long as you design it so that each level of state execution only takes at most 1-2 rounds of network latency plus the usual ~200ms of execution, then it should be well within bounds.

> It will be progress to recognize that we have a protocol that works, even if it is low throughput.

In that case, why not go with my protocol, that allows for one cross-shard transaction per block per account? Forcing participants to sometimes try sending the transaction several times before it succeeds would only increase de-facto fees by maybe a factor of ~2 due to the redundancy, much less than if there was only one transaction of cross-shard block space per shard.

---

**vbuterin** (2018-08-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> I’m thinking the constraint is that each shard can only have one originating transaction, so with 100 shards that’s 100 transactions, and to be extreme suppose each tx touches all 100 shards.

Actually, I think there might be a slightly different way of describing what you’re trying to do. Suppose that all 100 of these cross-shard transactions (could be less or more; no need for it to be the same as the shard count) all had to be stored *as part of the beacon chain*, and could synchronously affect shard state?

If we do that, then I think it actually might be possible to have (even if very expensive) cross-shard transactions win a way that allows us to *keep state roots inside of blocks*. This would lead to synchronous cross-shard transactions being very expensive but it would in some sense do the job.

---

**cdetrio** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Once concern with synchronous cross-shard tx’s in a delayed state execution model is that the state execution gadget (which is not a consensus game) won’t be able to keep up with block proposals/finalization (the consensus game at the data layer)

Why wouldn’t it? As long as you design it so that each level of state execution only takes at most 1-2 rounds of network latency plus the usual ~200ms of execution, then it should be well within bounds.

Right, so the concern is about designs where state execution might take more than 1-2 rounds of network latency (like with high towers of dependent tx’s).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It will be progress to recognize that we have a protocol that works, even if it is low throughput.

In that case, why not go with my protocol, that allows for one cross-shard transaction per block per account? Forcing participants to sometimes try sending the transaction several times before it succeeds would only increase de-facto fees by maybe a factor of ~2 due to the redundancy, much less than if there was only one transaction of cross-shard block space per shard.

A question about your protocol, is the purpose of the block structure containing the Merkle tree (mapping  `address => tx` with each tx bundle  `[shard[1], address[1], shard[2], address[2] ... shard[n], address[n], data]`) to make it easy for shards to verify that each account is only affected by one cross-shard tx in a slot (i.e. only affected by one cross-shard tx at some block height across all shards)?

This brings to mind the other major concern with synchronous cross-shard tx’s (particularly under delayed state execution): what prevents block proposers from stuffing the blocks with invalid tx’s (i.e. tx’s that don’t pay gas)? You say:

> if the transaction specifies  [A, 123, A, 485, B, 769, data] , then for  data  to get executed the transaction must appear at position 123 of block N in shard A, position 485 of block N in shard A and position 769 of block N in shard B.

But the validator on shard A is proposing shard-A-block-N without checking against shard-B-block-N, right? (perhaps shard-B-block-N has not even been proposed yet, as both shards are still on the same height N). If the tx doesn’t appear in shard-B-block-N position 769 (btw, not clear why its included twice at two different positions in shard A), then `data` is not executed. So the concern is what prevents validators from stuffing blocks with transactions where `data` is not executed, or is it not a problem if shard blocks are stuffed with invalid tx’s?

---

**vbuterin** (2018-10-22):

> A question about your protocol, is the purpose of the block structure containing the Merkle tree (mapping address => tx with each tx bundle [shard[1], address[1], shard[2], address[2] ... shard[n], address[n], data] ) to make it easy for shards to verify that each account is only affected by one cross-shard tx in a slot (i.e. only affected by one cross-shard tx at some block height across all shards)?

Yes.

> But the validator on shard A is proposing shard-A-block-N without checking against shard-B-block-N, right?

Correct.

> So the concern is what prevents validators from stuffing blocks with transactions where data is not executed, or is it not a problem if shard blocks are stuffed with invalid tx’s?

Invalid transactions are just treated as no-ops. And yes, it is possible for a malicious validator to prevent any cross-shard transactions that involve their shard from taking place for that one block.

