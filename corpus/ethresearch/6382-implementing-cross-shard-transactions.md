---
source: ethresearch
topic_id: 6382
title: Implementing cross-shard transactions
author: vbuterin
date: "2019-10-28"
category: Sharded Execution
tags: [cross-shard]
url: https://ethresear.ch/t/implementing-cross-shard-transactions/6382
views: 8192
likes: 4
posts_count: 8
---

# Implementing cross-shard transactions

One of the requirements of phase 2 is the ability to move ETH quickly from one shard into another shard. Though *cross-shard transactions in general* are possible through application of [the usual receipt mechanism](https://github.com/ethereum/wiki/wiki/Sharding-FAQ#how-can-we-facilitate-cross-shard-communication), with the protocol itself needing only to provide access to each shard’s state roots to each other shard, cross-shard ETH requires a little more enshrined in-protocol activity. The reason for this is that we need to keep track of how much ETH there is in each shard, and we need an enshrined mechanism for preventing replay of cross-shard transfers.

The usual receipt-based mechanism does solve this, but it does so by having a state tree of “already consumed receipt IDs”, which would be considerable complexity to add to a currently nominally stateless system. The reason this receipt ID tree is required is that we allow receipts to be consumed out of order. That is, if Alice sends a transaction from shard A → B and then Applebaum sends a transaction from shard A → B, it’s possible that Appelbaum’s transaction gets received in shard B first. This is necessary because with the gas-market-based approach for handling receipt-consuming transactions, it’s possible that Alice may decide to just not pay for the transaction to finish the transfer on shard B.

So a question arises: **can we replace the mechanism for handling receipts with one where receipts are processed sequentially**, so we only need one state variable for “the ID of the receipt shard B last received from shard A” that can just be incremented?

That is, every shard A maintains in its state, for every other shard B, two values: (i) the nonce of the next receipt that will be *sent* from A to B, and (ii) the nonce of the next receipt that will be *received* from B to A.

The answer to “who pays for it” is easy: the second half of processing a cross-shard transaction free (block producers would be required to process a certain number of receipts from other shards per block), with the rate-limiting done by charging fees on the source shard of the receipt. However, this has a major problem: what if one does a (possibly accidental, possibly intentional) DoS attack on a specific shard by sending receipts to it from all shards?

[![ReceiptDoS](https://ethresear.ch/uploads/default/original/2X/f/fc476176d0bdaff22ed20a716cc9b7d01aaeb8be.png)ReceiptDoS461×461 9.89 KB](https://ethresear.ch/uploads/default/fc476176d0bdaff22ed20a716cc9b7d01aaeb8be)

N shards sending N receipts each would impose O(N^2) load on the destination shard.

To solve this, we could impose the following mechanism. Every shard is required to process up to N receipts (eg. N = 64) in a block; if there are fewer than N receipts from other shards to process, it can use Merkle proofs from other shards to prove this. Each shard continually relays to the beacon chain the total number of receipts it has processed, and this is used to provide an updated “gas price” for sending receipts *to* that shard. For example, the gas price could be increased by 10% for each block that a shard’s receipt processing queue is full, up to a maximum of N. This ensures that at the extreme a DoS attack eventually fails to increase the length of a receiving shard’s queue, so each message gets processed, but it’s always *possible* to send a transaction that does some minimal amount of cross-shard activity. Alternatively, shards will already need to publish their EIP 1559 gasprices to the beacon chain to process block fees; this fee can be dual-purposed for this function as well.

If we have this mechanism for sending ETH cross-shard, we could also dual-purpose it for general-purpose receipt-sending functionality, creating an enshrined guaranteed cross-shard transaction system. The main challenge is that to compute the *effect* of receipts, we need someone to voluntarily provide Merkle witnesses of state. If full state is not enshrined, one cannot force this at protocol level; but what one *can* do is add a requirement of the form “in order to include one of your own transactions, you must also provide witnesses for a cross-shard receipt that is in the queue”.

## Replies

**dankrad** (2019-10-28):

One disadvantage of rate-limiting is that then, there are no guarantees that receipts will be received in any finite amount of time, which makes potential locking mechanisms more difficult to design. The effect of that could be reduced if the sending shard had a way to check consumption of a receipt. I guess that could be done by keeping receipt counters on the beacon chain.

---

**adlerjohn** (2019-10-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> One disadvantage of rate-limiting is that then, there are no guarantees that receipts will be received in any finite amount of time

How so? For any n \in \mathbb{Z}, I can find an m \in \mathbb{Z} such that m > n, where n is the position of a receipt in the queue (total ordering provided by the blockchain) and m is the total receipts that could have been processed at some block height.

---

**vbuterin** (2019-10-29):

I think [@dankrad](/u/dankrad) means a known-ahead-of-time synchrony bound. And I think ultimately such things are not possible, because it’s always possible that N+1 proposers skip in a row or N+1 committees fail to get 2/3 or whatever.

---

**villanuevawill** (2019-11-08):

Why not just make receipt bitfields stateful? I’m definitely cautious of automating the fee market. It requires DoS protection (as stated in your writeup) and other complexities (voluntary Merkle witnesses of state). Also, it appears to make the system more opinionated vs. a generally minimal approach. You also have less control of prioritizing your transaction in a bloated market (thereby reducing some predictability).

*Running numbers on a stateful system:*

To get the same effect of N = 64 (assuming the block always has 64 cross shard calls), would require 64 bits of storage for each block. Over a year, that equates to:

31536000 (seconds in a year) / 6 (seconds per block) * 64 (N) / 8 / 1000000 = 42.048 MB.

I/O would not be a significant blocker since it would be loaded in a buffer. To decrease storage further, we could likely assume receipts on average will be used within a day. This means we can limit the amount of state to ~115kb. After a day, receipts could be pruned into a separate root and witnesses would need to be submitted akin to what we assumed before (waking mechanism - [Cross-shard receipt and hibernation/waking anti-double-spending](https://ethresear.ch/t/cross-shard-receipt-and-hibernation-waking-anti-double-spending/4748)). We can also significantly reduce the size (thereby increasing the stateful period) by utilizing interval trees or run-length encoding appropriately.

Maybe this is a crazy idea, but receipts seem like a fairly core piece of the protocol and seems reasonable to keep receipt bitfields stateful at least for a certain period of time.

---

**vbuterin** (2019-11-09):

The challenge is that it significantly complicates the model for how the base layer works, as in the long run (really, after ~1 month) the bitlists would become too big to download in real-time, so nodes would need to either store updated bitlists for every shard or have a version of protocol-level stateless clients.

I have my own idea for a different simplification; will write it up soon.

---

**villanuevawill** (2019-11-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> so nodes would need to either store updated bitlists for every shard or have a version of protocol-level stateless clients.

Yep - this is why I suggested run-length encoding and having two roots. One for the stateful bitfields and the other for stateless. Assuming most receipts are claimed within a day, we can keep the statefulness to **under 100kb** (the rest just operate with witnesses as considered before).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I have my own idea for a different simplification; will write it up soon.

Interested to read this.

---

**kashishkhullar** (2020-02-22):

Given that the execution of a transaction on shard A will cost gas and generate a receipt. Will the consumption of receipt also cost gas?

