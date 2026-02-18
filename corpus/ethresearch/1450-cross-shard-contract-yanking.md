---
source: ethresearch
topic_id: 1450
title: Cross-shard contract yanking
author: vbuterin
date: "2018-03-21"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/cross-shard-contract-yanking/1450
views: 13330
likes: 6
posts_count: 5
---

# Cross-shard contract yanking

*Special thanks to Piper Merriam for helping to come up with this idea*

This is a generalization of [cross-shard locking schemes](https://ethresear.ch/t/cross-shard-locking-scheme-1/1269) and similar techniques to enabling cross-shard activity to solve train-and-hotel problems. Philosophically speaking, “locking” a contract that exists on shard A effectively means freezing its state on shard A, saving the state into a receipt, importing the contract to shard B, performing some operation between that contract and some other object on shard B, then using another receipt to send the contract back to shard A where it then continues its existence.

We can simplify and generalize this by changing the mechanism from “locking” to “yanking”. We add an opcode to the EVM, YANK (one stack argument: `target_shard`), which deletes the contract from the state and issues a receipt that contains the state of the contract and the `target_shard`; this receipt can then be processed in the `target_shard` to instantiate the same contract in that shard. Contracts are free to specify their own conditions for when they get yanked.

As an example, a hotel booking contract might work by having a function, `reserve()`, that reserves a hotel room, instantiates a contract that represents the hotel room, and that contract then contains a `move_to_shard(uint256 shard_id)` function which allows anyone to yank the contract to another shard. One can then solve the train-and-hotel problem by reserving the hotel room, yanking the contract to the same shard as the train booking contract, then atomically booking the hotel room and the train ticket on that shard. If desired, the hotel room contract’s `book()` function could self-destruct the hotel room contract, and issue a receipt that can then be used to save a booking record in the main hotel booking contract. If a user disappears after yanking but before atomically booking, then anyone else who wants to reserve the hotel room can just use the same hotel room contract to do so, possibly yanking the hotel room contract back to the original shard if they wish to.

For yanking to be efficient, the yankee’s internal state must be small so that it can be encoded in a receipt, and the gas cost of yanking would need to be proportional to the yankee’s total size. In general, it’s a bad idea from a usability perspective for a contract that could be of interest to many users to be yankable, as yanking makes the contract unusable until it gets reinstantiated in the `target_shard`. For these two reasons, the most likely workflow will be for contracts to have behavior similar to the hotel room above, where the contract separates out the state related to individual interactions so that it can be moved between shards separately.

Note that there is a nice parallel between cross-shard messages and yanking, and existing CALLs and CREATEs: CALL = synchronous intra-shard message passing, CREATE = synchronous intra-shard contract creation, CROSS_SHARD_CALL = asynchronous cross-shard message passing, YANK = asynchronous cross-shard contract creation. The YANK opcode does not necessarily need to both delete the existing contract and create a receipt to generate a copy on the new shard. Doing that could require calling both CROSS_SHARD_CREATE and self-destruct; that would make the symmetry complete, though a feature would be needed to allow creation of a contract in another shard with the same address as the original contract.

## Replies

**skilesare** (2018-03-23):

I like this idea a good bit.

In fact…this seems like it might be an interesting thing to try now.  Maybe zip up an ERC on mainnet, ship it to a test net, run a transaction, and then send it back.

Re: internal state must be small - Any crossover to stateless transactions here?  Witnesses from a YANK point should be deterministic such that clients can produce them and send them along with transactions to the yanked contract.

Re: address creation -> could the contracts live inside of some kind of Contract Managment Contract that passes all calls through a LookUp? Processing of this receipt could have updating this entry as part of its process.

At what point does it become easier to fuzz the borders of a shard than to yank contacts back and forth across hard bordered shards.

I guess merge blocks are a kind of fuzzing of borders.  What is the desire to reduce merge blocks to a patter instead of letting them free flow?  A DoS attack where some yahoo writes a contract that hits all 10 shards in such a way that all blocks have to be merge blocks?  Is there a gas cost solution to something like that?  Push the burden to the architects to reduce X-shard functionality?

---

**musalbas** (2018-07-17):

How do you prevent a user from using the same yank receipt twice, potentially yanking a contract (with the same state) back and forth between shards without any new YANK calls?

Do shards have to remember every yank receipt ever claimed, so that it can’t be claimed twice? (If so, does that not create unpruneable ever-growing state that has to be stored by shards?)

Or is there something smart that can be done?

---

**vbuterin** (2018-07-18):

There’s three natural extreme options:

1. Shards have to remember every yank receipt ever claimed
2. Yanking requires a Merkle proof of every previous block in that shard proving that the same contract was not yanked in during that block
3. A receipt specifies one specific block height during which it can be claimed, and if the contract does not get included at that specific height it’s simply dead forever.

But these three options are all clearly ridiculous, so there are natural intermediate options:

1. A receipt must be claimed within one year. Shards have to remember receipts for one year.
2. Shards have to remember receipts for one week. If a receipt is not claimed within one week, then the claimer must provide one Merkle proof per week proving that the receipt was not part of the claimed receipts list in the state during each previous week.

This is actually the same problem as the problem with [rent and hibernation](https://ethresear.ch/t/improving-the-ux-of-rent-with-a-sleeping-waking-mechanism/1480), and it seems likely ideal to have one mechanism to handle both cases.

---

**lookfwd** (2019-11-24):

What are the performance expectations of `YANK`? More specifically it seems to me that a modifying use of the receipt would require finality on the source chain. The whole idea resembles cache coherence ([1](https://en.wikipedia.org/wiki/MESI_protocol), [2](https://en.wikipedia.org/wiki/Bus_snooping)), which, at this stage is user-initiated by a protocol built around `YANK`, but could/should eventually be automated by it to network & incentives layer i.e. let market forces decide where it’s optimal for a contract to live in order to maximize throughput.

