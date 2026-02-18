---
source: ethresearch
topic_id: 1631
title: Easy sharding with merged blocks
author: yhirai
date: "2018-04-06"
category: Sharding
tags: []
url: https://ethresear.ch/t/easy-sharding-with-merged-blocks/1631
views: 1658
likes: 0
posts_count: 14
---

# Easy sharding with merged blocks

I think I came up with an easy way to scale Ethereum.  This kind of thing is usually wrong, so let me try here.  For sharing security among shards, I think merged blocks are enough.

## Data Structure

### Changes to Block Header and Transaction

I start from the Byzantium version of Ethereum.  I add a 256-bit value `shardID` to the blockheader.  I also add a 256-bit `shardID` to the transaction.

A valid block can only contain transactions of the same `shardID` as shown in the block header.

An **unsealed block** is very similar to a block, but without nonce and mix hash components in the block header.

### Merged Block

A merged block between two shards contain

- a mix hash
- a nonce
- an unsealed block of shard ID A
- an unsealed block of shard ID B

A merged block is valid if

- the unsealed block A is valid
- the unsealed block B is valid,
- The nonce and the two unsealed headers yield the mix hash, and a number smaller enough to pass both shard’s current difficulty, and
- it’s ancestors don’t contain any fork of any shard

The blockhash of a merged block is the same for both shards.  A block’s parentHash can point to a merged block. That’s why blockheader needs a shardID.

After a merged block, the difficulty of shards A and B are still independent.

## Fork choice rule

### (a) heaviest path (doesn’t work)

First, we choose the heaviest path.  A path can go along the parentHash of any shards.  Its weight is the sum of difficulties.  We choose the tip of the heaviest path. Its ancestors don’t contain any fork of any shard, so a chain is automatically chosen for each shard.

But, then, mining on a non-heaviest-path is quite unsecured.

### (b) heaviest tip

Instead of choosing a best path, we can choose the heaviest tip (considering all ancestors of the (merged) block).  Then, the ancestors of the tip do not contain forks on any shards, and we get a sequential history on all shards.

## Q & A

- Is a merged block atomically contained in both shards or neither?

Yes.

why would miners merge-mine?

- because they can get rewards on both shards.

## Replies

**fubuloubu** (2018-04-06):

So the client has to choose which shard they submit their transaction to? How would they make that choice? How does the protocol ensure the even weighting of that choice over time?

Why does the transaction need `shardID` at all? Can’t the miner calculate valid shards to stick it in based on examining the transaction’s `to` field? This would allow the miner more flexibility to choose a shard to put it in (or conversely, if a miner only mines one shard they can selectively listen for transactions that work in their shard but have not been included in a prior block on any other shard)

Neat idea “merge mining”

---

**vbuterin** (2018-04-06):

So every shard has a separate proof of work chain? What happens if a miner tries to 51% attack some specific chain?

---

**fubuloubu** (2018-04-06):

You could design a system that only opens up new shards if there is an overabundance of miners (by some metric) for a prolonged period of time. Then they would be attracted to the new shard, moving some of that hash power around to prevent any one shard from having too little miners on it. Something of that nature?

---

**vbuterin** (2018-04-06):

The problem is that you can’t tell one miner from another, so it would just look like existing miners on one shard are all increasing their hashpower.

---

**fubuloubu** (2018-04-06):

So basically you just see overall network hashpower? And you know the number of shards. So per-shard hash power is overall power divided by number of shards, loosely?

---

**yhirai** (2018-04-06):

1. usually a user is only interested in one shard, so they submit their transaction there.  There is no attempt at even weighting. Different shards have totally separate world states (maybe something like ‘moving contracts across shards’ can be done using merged blocks).
2. the signer has control over on which shard their signatures are valid.  It’s similar to replay protection.

---

**yhirai** (2018-04-06):

The attacking miner needs the hashing power stronger than all other miners on all shards combined.  The fork choice rule is global.  The fork choice rule chooses the single best block from all shards.

---

**yhirai** (2018-04-06):

The total difficulty of a [edit: first] merged block is the sum of the weights of the two shards so far.  In order to orphan this merged block, it’s not enough to overweigh the miners on one shard, but to over weigh the miners on both shards.  The history contains more and more merged blocks, making the best block as heavy as all shards combined.

---

**yhirai** (2018-04-06):

I just need to see the overall network hashpower, and I don’t see per-shard hash power relevant.  The fork choice rule just chooses the best single block among all shards (the two parents of merged blocks can be confused, and the best block does not change).  So the competition is across all shards at the same time.

---

**vbuterin** (2018-04-06):

Ah I see. So merge blocks inherit the hashpower of both of the shard chains that they merge. One problem with this is is that if a miner wants to make a block, they would want to verify not just that specific shard, but also the other shard of the most recent merge block that is in that shard, and then any shards merged to that shard, and so forth; the entire DAG becomes a dependency. Are you proposing that miners only light-verify past a particular confirmation depth threshold? If so, that is feasible, though I would still really worry about targeted 51% attacks on subtrees. There’s an unavoidable tradeoff here: if a miner fully verifies portion p of shards, then the scalability factor is limited to 1/p, and an attacker could attack with portion p of hashpower. So basically it’s the same bottleneck as merged mining.

---

**yhirai** (2018-04-06):

I see.  Let’s say there are 100 shards.  Each miner only verifies 2 shards, and light-verifies blockheaders of the rest 98 shards.  If there are 500.0 miners, one shard has around 10.0 miners.  So it’s enough to defeat these 10.0 miners to censor this shard.

---

**yhirai** (2018-04-06):

In the end you’re right.  It’s easy to censor one or two shards, so users should be able to submit their transactions to whichever shard they want to.  Then the world state transition is not sequential anymore, so the scheme cannot be called “easy sharding” anymore.

---

**yhirai** (2018-04-06):

Perhaps, we can send users around to random shards, instead of choosing several collators randomly from a collator pool.

