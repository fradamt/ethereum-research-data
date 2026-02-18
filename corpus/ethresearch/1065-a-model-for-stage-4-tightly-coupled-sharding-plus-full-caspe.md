---
source: ethresearch
topic_id: 1065
title: A model for stage 4 "tightly coupled" sharding plus full Casper
author: vbuterin
date: "2018-02-13"
category: Sharding
tags: [tight-coupling]
url: https://ethresear.ch/t/a-model-for-stage-4-tightly-coupled-sharding-plus-full-casper/1065
views: 4789
likes: 13
posts_count: 9
---

# A model for stage 4 "tightly coupled" sharding plus full Casper

UPDATE: see correction here [A model for stage 4 "tightly coupled" sharding plus full Casper](https://ethresear.ch/t/a-model-for-stage-4-tightly-coupled-sharding-plus-full-casper/1065/6) ; in short, some kind of limited forkful sharding (eg. with a short revert limit) may be unavoidable, though we can have finality come more quickly if desired by reducing the period length to 1 block.

The following describes how “tightly coupled” sharding might work, in a way that simultaneously provides full Casper, along with fast semi-confirmations.

We assume:

- Either data availability proofs, or that nodes simply directly check availability of collations a few blocks back
- A cryptoeconomically secure mechanism for randomly sampling validators
- A chain-based PoS scheme

Consider a chain-based PoS scheme where every block has a proposer, which is randomly sampled from the validator set, and `SLOT_COUNT` (eg. 12) collation slots. For each slot, a validator index is sampled, and a shard ID is randomly chosen; this random sampling happens `LOOKAHEAD` (eg. 5) blocks in the past (ie. the validator indices and shard IDs for block `N` are chosen during block `N - LOOKAHEAD`.

Each collation slot can be either empty, or taken up by a collation header, created by the specified validator. A collation header simultaneously serves **three** functions:

1. Representing a collation in the specified shard.
2. “Soft-confirming” the parent block.
3. Carrying a Casper FFG vote for the most recent checkpoint.

(1) is the same as collations in the current sharding proposal, except it is **tightly coupled**; that is, a block cannot be valid unless all collations it contains are available, and the same is true for all ancestors of that block. Additionally, the sharding is now *internally fork-free*: the collation must be built on top of the previous collation for the same shard mentioned in the chain.

Regarding (2), we have two properties. First, each collation that confirms the parent block adds 1 point to the score of the parent block; hence, these collations are the dominant factor that determines which chain is the longest. Second, a single validator creating two collations with the same index at the same height is a slashable offense; hence, if you see a collation with `N > SLOT_COUNT/2` slots full, then you know that any competing chain will either require `2N - SLOT_COUNT` slashed validators, or it would have to revert an entire `LOOKAHEAD` blocks to get different validators; either condition is hard, so this gives a kind of “soft finality” that can be reached within a single block. This can essentially be Ethereum’s answer to the market desire for blockchains that offer confirmations within a few seconds.

And (3) is self-explanatory. Note that the numbers match up quite conveniently; for example, if there are 100 shards, and we have an implied “period length” of 5, then this implies `SLOT_COUNT = 20`; with 20 votes per block, which with 2000 validators gives an equivalent “epoch length” of 100 blocks.

## Replies

**kladkogex** (2018-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The following describes how “tightly coupled” sharding might work, in a way that simultaneously provides full Casper, along with fast semi-confirmations.

How are users going to submit pending messages to validators? If validators are going to be chosen randomly from a global pool one probably does not want to store all pending messages on all validators …

If a user submits a pending message to validator X, and the message is not included into a collation before this validator becomes inactive for the particular shard the message is destined to, then the user will need to resubmit the message to another validator, unless there is some kind of a gossiping scheme which passes pending messages from validator to validator …

---

**vbuterin** (2018-02-14):

There would be a separate gossip network per shard, which would be between clients of that shard and proposers on that shard. Proposers and validators are separate, see [Separating proposing and confirmation of collations](https://ethresear.ch/t/separating-proposing-and-confirmation-of-collations/1000) ; proposers and executors are shard-specific and validators are chosen from a global pool.

---

**JustinDrake** (2018-02-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> We assume:
>
>
> Either data availability proofs, or that nodes simply directly check availability of collations a few blocks back

Let’s assume we do *not* have data availability proofs. By “directly check availability of collations” do you mean download the full collation bodies of the corresponding collation headers?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> a block cannot be valid unless all collations it contains are available

This means that for checking the validity of a block it is necessary for a fully validating node of the main shard to download the full collation bodies for `SLOT_COUNT` (in the worst case) collation headers. Is that right?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> if there are 100 shards, and we have an implied “period length” of 5, then this implies SLOT_COUNT = 20

If the period length is 5, and the child shards process roughly as much as the main shard, then we can expect collation bodies to be about 5 times the size (in bytes) of a block. So with `SLOT_COUNT = 20`, verifying the validity of a block will involve downloading the equivalent of about `SLOT_COUNT` * 5 = 100 blocks. It seems fully validating nodes of the main shard would need to have the downstream bandwidth for the collation bodies of all shards combined.

---

**vbuterin** (2018-02-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Let’s assume we do not have data availability proofs. By “directly check availability of collations” do you mean download the full collation bodies of the corresponding collation headers?

Basically, if a node is considering whether or not to create a block, then it fully downloads and verifies the data availability of (i) all collations it wants to include, (ii) all collations in ancestors going back up to `WINDBACK / SLOT_COUNT` blocks. If a node is considering whether or not to build a collation on top of block B, then it performs the same availability check for block B.

So if `SLOT_COUNT = 20`, then it might make sense to check three blocks back. The key insight here is that because collations are now serving the double duty of also being claims on the availability of prior collations in all shards, regardless of the degree of parallelization between collations (ie. `SLOT_COUNT`), the number of collations you need to look back should not change (likely except in the extreme case where `SLOT_COUNT >= WINDBACK`).

> It seems fully validating nodes of the main shard would need to have the downstream bandwidth for the collation bodies of all shards combined.

Yes, but being a fully validating node of the main shard in this model is equivalent to being an super-full node in the old model; the system doesn’t require any such nodes to actually exist. I expect the preferred configuration to be not verifying collation availability in the normal case, and only verifying it `WINDBACK` periods back when you get called to create a block or a collation.

---

**vbuterin** (2018-02-19):

Eek! I just realized something, which is that the scheme does require O(C^2) bandwidth after all. The scheme *does* require validators creating collations or blocks to verify the work of the entire chain, even if only for a short “burst” period of time once in a while. Particularly, this means that it can’t work if the only acceptable values for WINDBACK are less than SLOT_COUNT (which is likely; remember that if SLOT_COUNT = 20 with 100 shards, that means that each collation contains 5 blocks’ worth of data, so with WINDBACK = SLOT_COUNT, a validator is asked to process the equivalent of a block for each shard within the timespan of one block). Also, note that increasing LOOKAHEAD doesn’t help, as the data doesn’t become available to verify until one block length before the validator needs to make their own block/collation.

The goal should be for block creators to be able to use an existing random-sampled vote among collation validators to determine that some collation is available and finalize its membership in the main chain. One simple option is forkful sharding with a revert limit. In fact, I’m not sure if it’s possible to improve on that without completely leaning on a scalable data availability proof solution.

We *can* have a scheme where once a shard is suggested it needs to be voted on by a committee, but that has more complicated incentives as you have to figure out the right rewards for the committee members, whereas it’s much more clear for the forkful model where each collation creator is implicitly voting on the availability of every collation before them.

---

**kladkogex** (2018-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Consider a chain-based PoS scheme where every block has a proposer, which is randomly sampled from the validator set,

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Proposers and validators are separate, see Separating proposing and confirmation of collations ;

I think these two statements contradict each other, do they? Did you mean that “a proposer is randomly sampled from the global set of proposers”

---

**vbuterin** (2018-02-20):

> Did you mean that “a proposer is randomly sampled from the global set of proposers”

**Block** proposers are randomly sampled from the global set. **Collation** proposers are a role that anyone can participate in.

---

**turb0kat** (2018-02-22):

Is there a total architecture document somewhere?  Stuff is evolving very fast and it is hard to keep the full picture in my head as the thinking / design evolves.

