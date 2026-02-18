---
source: ethresearch
topic_id: 287
title: History, state, and asynchronous accumulators in the stateless model
author: JustinDrake
date: "2017-12-03"
category: Sharding
tags: [stateless, accumulators]
url: https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287
views: 10017
likes: 8
posts_count: 10
---

# History, state, and asynchronous accumulators in the stateless model

**TLDR:** Ethereum currently uses an accumulator (the Patricia-Merkle trie) which is designed for state. There’s an alternative accumulator design which is a great match with the [stateless client model](https://ethresear.ch/t/the-stateless-client-concept/172), but it works for history only. By separating history and state, and encouraging use of history versus state, we can make the stateless client model more practical and scalable than initially thought.

**History in Ethereum 1.0**

In this post “history” refers to any append-only data structure relevant to Ethereum. We have transaction history, block history, receipt history. Contract code is also a form of history because [contract code is immutable](https://ethereum.stackexchange.com/a/2162/136). Finally applications can exhibit history (e.g. think of a contract that maintains historical tick data in storage).

In Ethereum 1.0 history is a second-class citizen because transactions, blocks and receipts are not natively readable from transactions (with the exception of the block hash, but only for the [256 most recent blocks](https://ethereum.stackexchange.com/questions/418/why-are-contracts-limited-to-only-the-previous-256-block-hashes)). Vitalik wrote [2.5 years ago](https://www.reddit.com/r/ethereum/comments/3iwon4/developer_psa_blockhashes_are_only_good_for_256/cukmzun/) that making history inaccessible “improves efficiency and code simplicity for many kinds of nodes” and that “state is all that matters”. I imagine the rationale was that we cannot have nodes fetch potentially very old historical data to process transactions. Even today the folklore is that “ever growing blockchain history doesn’t scale”.

**History in the stateless model**

In the stateless model nodes never need to go digging for data (regardless of whether that data is history, state or something else). Indeed the responsibility of providing data is borne offchain (e.g. by the transaction sender). In that sense, history is no harder than state to process in the stateless model. Not only that, it turns out that handling history may be *significantly easier* than handling state in the stateless model.

The key here is a recent innovation called [asynchronous accumulators](https://eprint.iacr.org/2015/718.pdf) from Leonid Reyzin and Sophia Yakoubov. The specific construction in their paper is a clever and simple twist over the beloved Merkle tree; no magic. Their asynchronous accumulator has a property they call “low update frequency”, which allows for history (without dynamism inherent to state) to be accumulated such that the witnesses for the individual events need only be updated logarithmically in the number of events (as opposed to linearly). And the cherry on top is that updates do not require knowledge of the accumulated set, perfectly matching the stateless model.

An asynchronous accumulator is useful for at least two reasons. First, it dramatically reduces the costs of witness maintenance for witness holders. Second and maybe more importantly, it greatly increases the probability that a transaction in the stateless model will be executable with the same witness data it was sent with (c.f. [account lists](https://ethresear.ch/t/account-read-write-lists/285)). In other words, low update frequency might be the ingredient that makes the stateless client model practical.

**Ethereum 2.0 idea: dual accumulators**

So for Ethereum 2.0 we may want to try to flip around the philosophy of “state first, history second”, instead aiming for “history first, state second” to leverage low frequency accumulator witness updates. Every contract would be endowed with a dedicated accumulator for its history, in addition to the existing read/write storage accumulator. Consider the following hybrid “dual accumulator” VM:

1. One accumulator for the history (keeping track of the “immutable past”). Append-only (non-dynamic); high bandwidth; low frequency witness updates; cheap; super large tracking set (think trillions of elements); implemented using an asynchronous accumulator
2. One accumulator for the state (keeping track of the “changing present”). Dynamic; medium bandwidth; high frequency witness updates; expensive; relatively small tracking set (think millions of elements); implemented similarly to the current Patricia-Merkle trie

My gut feel is that many (if not all) Ethereum applications can be tweaked to push almost all (80% to 99%+) of their storage load to the history (see below for a strategy to push all-but-256bits of the storage load to the history). Pushing data through the history accumulator would exhibit a greatly discounted gas price relative to pushing data through the storage accumulator, encouraging application developers to use storage only if absolutely necessary.

**Writing “history-driven” applications**

It turns out there are generic ways to write applications that maximise history and minimise storage. Below are two strategies:

1. Using SNARKs (or STARKs), it’s possible for any application to use just 256 bits of storage, pushing everything else to history. The 256 bits of storage would hold the hash of the (implicit) state derived from the “transactions” pushed to the history, themselves proved valid with a SNARK. Each transaction would update the 256 bits of storage. The state is implicit because it is derived offchain from the “transactions” (a bit like Bitcoin balances are implicitly derived offchain from UTXOs). Notice that data availability for the implicit state is handled by the gossiping of historical transactions at the time of execution.
2. As an alternative to SNARKs/STARKs above, we can use a TrueBit/fraud proof model with potentially-invalid-but-collaterised transactions (pushed to the history) that “confirm” after a given period of time during which no successful challenge was made. The application would use storage as a buffer for temporarily unconfirmed transitions state of the implicit state.

## Replies

**vbuterin** (2017-12-04):

The paper https://eprint.iacr.org/2015/718.pdf looks very similar to merkle mountain ranges (see [here](https://github.com/opentimestamps/opentimestamps-server/blob/master/doc/merkle-mountain-range.md)). So that category of thing is definitely not a new idea, and there are other ways to do this as well, for example by adding a [patricia tree of previous state roots into each state root](http://github.com/ethereum/EIPs/issues/96).

There **definitely** are going to be many history-focused use cases inside sharding. Particularly, asynchronous cross-shard calls pretty much have to be done with this paradigm of “create a receipt on shard A, then later prove that the receipt exists to shard B”, and if you then use a model where users delay sending receipts as long as possible and only use receipts to create new receipts then you’ve basically reinvented the UTXO model.

The idea of having explicit data structures in the system to make low-witness-update-frequency  history objects easily usable is definitely an interesting one. That said, there are limits: in general, any application that allows you to reference objects from the history is very often also going to require some kind of stateful mechanism for efficiently proving whether or not those objects have already been consumed.

---

**JustinDrake** (2017-12-04):

Yes very similar to (actually, looks the same as) Merkle Mountain Ranges (MMR). Wow, several people (including Peter Todd, Greg Maxwell, Mike Hearn, Oleg Andreev, Andrew Miller) were basically discussing stateless clients and this asynchronous accumulator for Bitcoin in 2013 (see [here](https://bitcointalk.org/index.php?topic=314467.msg3371194#msg3371194) and [here](https://s3.amazonaws.com/peter.todd/bitcoin-wizards-13-10-17.log))! Back then they called it “storageless”.

> The idea of having explicit data structures in the system to make low-witness-update-frequency history objects easily usable is definitely an interesting one.

Given how cheap, user-friendly and low-complexity an MMR is, it does feel natural to consider including one at the consensus layer to dump every piece of history to it, including transactions, blocks, receipts, and application-specific history. Every piece of history can be wrapped in a thin layer of metadata, e.g. to classify the event type.

For example blockhashes can be dumped as `[TYPE_BLOCKHASH, {block number goes here}, {block hash goes here}]`. Compared to the [blockhash refactoring proposal](https://github.com/ethereum/EIPs/blob/2f8d0f5e6192a0fb236ffb3c1b95f5fea871270e/EIPS/blockhash_refactoring.md) it wouldn’t impose storage, it would allow for efficient checking of arbitrary blockhashes, and wouldn’t require ad-hoc opcodes and/or contracts at the consensus layer.

> any application that allows you to reference objects from the history is very often also going to require some kind of stateful mechanism for efficiently proving whether or not those objects have already been consumed

Yes, and this would a design space that’s left open for application developers. The extreme approach I alluded to above with the SNARKs/STARKs is for contracts to define their own application-level accumulator for efficient proofs of object consumption or non-consumption. (For anyone reading, there are universal accumulators with efficient proofs of both set ownership and set non-ownership.)

This approach suffers from a practical issue around transaction synchronisation. Indeed, updating the application-level accumulator is a serial bottleneck that will cause contention when many users want to interact with the contract at the same time. One could do “accumulator sharding” with several accumulators to allow for parallelism. And applications can setup a queuing mechanism for participants to reserve “interaction slots” to avoid wasted work from contention and give everyone a chance to participate.

**EDIT:** The practical issue around transaction synchronisation goes away with [miner-updated witnesses implemented using miner data](https://ethresear.ch/t/account-abstraction-miner-data-and-auto-updating-witnesses/332).

---

**kladkogex** (2018-01-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The paper https://eprint.iacr.org/2015/718.pdf looks very similar to merkle mountain ranges (see here).

The paper talks about low frequency updates if elements are added.   What about cases where elements are updated or removed?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Particularly, asynchronous cross-shard calls pretty much have to be done with this paradigm of “create a receipt on shard A, then later prove that the receipt exists to shard B”,

Another problem to solve for asynchronous cross-shard calls will be transaction rollback.  If contract X calls contract Y  on another shard,  then contract X should be able to roll back its state if a call to contract Y fails

---

**JustinDrake** (2018-01-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The paper talks about low frequency updates if elements are added.   What about cases where elements are updated or removed?

The accumulator only supports additions. That’s the whole tradeoff ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) So the engineering question becomes: How can we design dapps that mostly make use of additions, so as to maximise the value of MMRs? See [this post](https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385) for one possible direction.

---

**kladkogex** (2018-01-04):

I see - now all of this becomes clear …

By taking a physics analogy one can represent destruction of a particle (electron) by addition of an anti-particle (positron).  So for the Merkle Mountain range, instead of removing an item I can add an anti-item.   And for an update I can add an anti-item and then a new item.

Is this similar to what you are proposing?

Applications could theoretically maintain pairs of maps for items and anti-items.  And then there could be some logic to “garbage collect” these pairs (say every day).  Then witnesses would only need to be updated every day.

---

**vbuterin** (2018-01-04):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> So for the Merkle Mountain range, instead of removing an item I can add an anti-item.   And for an update I can add an anti-item and then a new item.

Yes, exactly. Though you need cryptoeconomic witnesses to prove that the anti-item does not exist.

---

**tawarien** (2018-02-20):

I have some trouble understanding the correct reasons behind why this is a benefit. I do understand the part with the high and low-frequency update, but I think I miss something and their is more that makes the history cheaper. What I do not understand is if I can access the state and the history from my smart contracts, why would it be cheaper to lookup an element from a set of trillions of elements (respectively checking a witness for that set in the stateless model) vs doing the same for a set containing millions of elements. My intuition would tell me that the smaller set is cheaper to access or check witnesses. What do I miss? Or do I miss nothing and its all just about the frequency of the witness update

---

**JustinDrake** (2018-02-20):

The research has progressed somewhat since this post. The best accumulator design for logs we know of is the [double-batched Merkle log accumulator](https://ethresear.ch/t/double-batched-merkle-log-accumulator/571). Below are reasons why using this particular log accumulator (for history) is cheaper than using a Patricia trie (for state):

1. Log witnesses do not have to be updated (only extended, once). Compare this to state witnesses which need to be updated for every insertion and deletion to the trie. A significant simplification is that, unlike state witnesses, there is no need for validators to auto-update log witnesses. Logs are also the natural basis for receipt-based asynchronous cross-shard communication, so having a protocol-level log accumulator helps communicating receipts across shards.
2. Notice that the size of the log witnesses is log(#objects in a single collation), whereas the size of state trie is log(#total state objects). For concreteness, let’s assume the bottom buffer of the double-batched accumulator has 1024 hashes. In a single collation we can expect on the order of 16,000 logs, so the size of a single log witness will be about (14 + 10) * 32 = 768 bytes. We can expect the state trie to quickly grow to a billion objects, so a single state witness will quickly reach 30 * 32 = 960 bytes.
3. With log shards and custom execution models (e.g. this one) you don’t have to execute transactions onchain. My guess is that the cost of onchain execution in the EVM is about 10x-100x greater than the cost of a state-minimised log-based equivalent.

Point 1) is an important practical simplification in the context of stateless clients. Point 3) is a significant opportunity for scalable apps (either stateless or stateful) that benefit from onchain data availability without bearing the costs of onchain execution.

---

**tawarien** (2018-02-21):

Thanks, points 2 and 3 where the one I missed.

A more concrete question and probably to soon to answer.

How high do you estimate the cost reduction per byte if it stored in the history vs in the state.

