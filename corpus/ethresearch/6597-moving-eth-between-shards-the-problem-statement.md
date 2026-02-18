---
source: ethresearch
topic_id: 6597
title: "Moving ETH between shards: the problem statement"
author: vbuterin
date: "2019-12-07"
category: Sharding
tags: []
url: https://ethresear.ch/t/moving-eth-between-shards-the-problem-statement/6597
views: 7567
likes: 6
posts_count: 8
---

# Moving ETH between shards: the problem statement

In general, the way that tokens are handled on a sharded blockchain is through accounts and receipts that exist inside of execution environments. That is, a token is something that exists inside of an EE, in the form of account balances on different shards that have units of that token. On shard A, Alice might have 50 ExampleCoin (EXC) and Ashley 70 EXC, on shard B, Bob might have 40 EXC, etc, and these are all represented as leaves in the EE’s state tree.

[![Untitled%20Diagram](https://ethresear.ch/uploads/default/original/2X/c/c0433d3682ac934b088d20749fb5333058261815.png)Untitled%20Diagram502×181 4.28 KB](https://ethresear.ch/uploads/default/c0433d3682ac934b088d20749fb5333058261815)

Alice transferring EXC to Ashley is easy: it’s just a transaction within one shard that updates both balances. Alice transferring EXC to Bob is slightly more involved, but the method is established: Alice converts the EXC she wants to send into a receipt, waits for it to get included in the shard, and then Bob includes a Merkle proof of this receipt (plus a witness *from shard B* proving that receipt has not yet been spent) into shard B, at which point the balance in the receipt gets added to his account.

Now, let’s look at how ETH is different from EXC. EXC is an asset defined inside an EE, that exists only in that EE. Trust in the EE’s code is required to trust that EXC follows standard properties of an asset: if the EE’s code were bugged, Bob might be able to claim the EXC from the receipt multiple times, printing new EXC into existence (to give one possible example of a failure). ETH, on the other hand, is defined at protocol layer, and the protocol layer needs to be sure that ETH works securely.

Furthermore, there is a requirement that EEs must be able to hold ETH, and assign “ownership” to that ETH internally to accounts within that EE, and this ETH must be “spendable”. This is for paying transaction fees: if Alice wants to send a transaction, that transaction will need to spend Alice’s ETH to pay for gas, and the EE code must be able to take ETH that it holds and pay it to the block producer.

At EE internal state level:

![image](https://ethresear.ch/uploads/default/original/3X/9/1/91fd3e3865ef12a090aa30b7b9336f8e9c1d9018.svg)

In the top-level state:

![image](https://ethresear.ch/uploads/default/original/3X/2/1/21aa2974b14a04b948d2ec72db3ff2d44055a4df.svg)

For transfers within a shard, there are no challenges: transfers within a shard purely affect the internal accounting of an EE instance on some shard, they do not affect the total balance. But transfers *between* shards are tricky.

Suppose Alice (on shard A) wants to transfer 1 ETH to Bob (on shard B). There are actually *two* transfers that must take place:

1. Alice’s balance in the EE-internal state drops 1 ETH, Bob’s balance in the EE-internal state gains 1 ETH
2. The EE instance on shard A loses 1 ETH, the EE instance on shard B gains 1 ETH

(1) is purely an EE-internal matter so we do not need to care. But (2) must, somehow, be handled at protocol layer.

### Solutions

**1) Every shard crosslink publishes to the beacon chain all cross-shard transfers that it is making**.

Problem: this technically makes Ethereum sharding no longer quadratic, as for N shards there would be N shard blocks each containing N transfers in a high-usage scenario, so a total O(N^2) beacon chain load. These numbers are significant even in concrete terms: assuming 4 different EEs are popular, that’s 256 total transfers, and even if each transfer is compactly encoded into 10 bytes that’s 2560 bytes * 64 shards = 163 kB overhead.

**2) every shard crosslink publishes to the beacon chain a Merkle root of all transfers, every shard chain block is requires to contain Merkle branches from all most-recent transfer roots corresponding to the transfers to their shard**

That is, shard i would have a Merkle root detailing the transfers to shard (0, 1, 2 … N), and then shard j in the next block would be required to have the Merkle branch at position j from all shard blocks.

Problem: this feels like an awkward halfway-house between having protocol-guaranteed cross-shard transactions and not having such transactions. It has the complexity and mandatory data-passing requirements of a guaranteed cross-shard transaction scheme, without providing to users the benefits that such a scheme properly implemented would give them.

**3) Netting**

Shard blocks have the ability to record up to one transfer going to another EE on another shard. EEs would in general be expected to have small amounts of extra ETH locked up forever on each shard. When Alice sends ETH to Bob, Bob receiving the receipt gives him the right to use that ETH, dipping into this deposit if needed. The EE keeps track of its “debts” to copies of itself on other shard, and in every block sends a transaction that resolves its largest outstanding debt.

**4) Enshrine one EE for ETH / asset holdings that everyone is required to understand**

Problem: this creates an enshrined in-protocol state, and creates risks that this form of state because of its greater level of enshrinement will be abused for other application purposes.

**5) Create some form of “guaranteed cross-shard transaction” system and piggyback on that**

Basically, bring the entire infrastructure for cross-shard transactions into the base protocol, establishing some mechanism for guaranteeing arrival. If it is guaranteed in-protocol, then we can ensure that receipts are processed sequentially, removing the need for nontrivial amounts of state to store which receipts have been claimed and which have not; we just have a “next unclaimed receipt ID” ticker. However, this would require creating a sustainable gas mechanic, and handling cases where all shards send cross-shard transactions to the same destination shard simultaneously (this could be a DoS attack or an exceptional application activity, eg. an ICO).

## Replies

**mikedeshazer** (2019-12-07):

#5

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> infrastructure for cross-shard transactions into the base protocol

+1

From a user’s perspective, if receipts/transactions processed sequentially is the expected behaviour in-shard, might be convenient to have that expectation outer-shard, too.

---

**dankrad** (2019-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> 4) Enshrine one EE for ETH / asset holdings that everyone is required to understand
>
>
> Problem: this creates an enshrined in-protocol state, and creates risks that this form of state because of its greater level of enshrinement will be abused for other application purposes.

Wait, but as long as all transactions come with full Merkle proofs to the EE state root (as is the current plan), this state would still not be necessary to participate in consensus, right?

So I don’t really see where the problem is.

---

**vbuterin** (2019-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Wait, but as long as all transactions come with full Merkle proofs to the EE state root (as is the current plan), this state would still not be necessary to participate in consensus, right?

True, but we would have to decide on an enshrined account balance/code storage scheme, consider rent, have an enshrined model for what user-level ownership looks like, receipts, etc etc. It ends up bringing a lot of complexity that would otherwise be layer-2 up to a more privileged layer.

---

**ChengWang** (2019-12-07):

As far as I see, in the case Alice transfer ETH from A to B, there are 3 places Alice needs to pay gas fee: shard A, beacon chain, shard B.

Am I right here? If so, how would you implement these three phase fee payment in a simple way? The first phase of fee payment is just for creating the receipts, which should be natural. I am not sure about the other two phases.

---

**dankrad** (2019-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> True, but we would have to decide on an enshrined account balance/code storage scheme, consider rent, have an enshrined model for what user-level ownership looks like, receipts, etc etc. It ends up bringing a lot of complexity that would otherwise be layer-2 up to a more privileged layer.

All of these will have to be decided to have a functional Eth2 ecosystem. I think it is unlikely that a full node would not also be able to understand a VHEE, and based on that, it could easily make decisions on whether it is being paid valid ETH. So no enshrinement into the consensus layer would really be necessary, a new and better VHEE could even be built without a fork being necessary.

---

**villanuevawill** (2019-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> All of these will have to be decided to have a functional Eth2 ecosystem. I think it is unlikely that a full node would not also be able to understand a VHEE, and based on that, it could easily make decisions on whether it is being paid valid ETH. So no enshrinement into the consensus layer would really be necessary, a new and better VHEE could even be built without a fork being necessary.

![:100:](https://ethresear.ch/images/emoji/facebook_messenger/100.png?v=12) This complexity will have to be introduced regardless, and it seems natural to enshrine particular parts of it - I don’t mind expanding on this later but requires a longer writeup/rationale (although we don’t necessarily *need* to).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Problem: this creates an enshrined in-protocol state, and creates risks that this form of state because of its greater level of enshrinement will be abused for other application purposes.

Can you describe some of these abuses in particular?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> removing the need for nontrivial amounts of state to store which receipts have been claimed and which have not; we just have a “next unclaimed receipt ID” ticker.

I still don’t think you need a non-trivial amount of state - [Implementing cross-shard transactions - #7 by villanuevawill](https://ethresear.ch/t/implementing-cross-shard-transactions/6382/7) - I think this can be compressed to a fairly small value as mentioned in this response.

---

**qizhou** (2019-12-09):

Good summary!  I would like to share our thoughts on moving native token between shards, which are close to the solutions (2) and (5) with the following features:

- Guaranteed and ordered delivery via incentives: A cross-shard receipt will be incentivized to be eventually processed at destination shard.
- DoS attack prevention: Even the attacks may send lots of transactions to one shard from other shards, the system would continue to work.
- Happen-before guarantee: A cross-shard receipt will be always processed at the destination shard after the original token was spent from the source shard.

## Assumptions:

**A1.** A BP node of shard j is a light-client of shard i and full node of the root chain (similar to beacon chain in ETH2.0), and thus the node is able to obtain and verify the receipts of **all blocks** of shard i via a Merkle root hash (Note that “all blocks” constraint may be relaxed to “recent blocks”)

**A2.** The Merkle root hashes of cross-shard receipts from all shards are included in the root chain in a **deterministic** order.

**A3.** A shard block contains **a hash pointer to root block** and **a cursor**:

- The root block hash pointer tells which root block the BP of the shard block observed and included.  According to A1, the BP could fully recover all receipts from shards by the Merkle root hashes of the blocks of root chain since the genesis root block.  By ordering the receipts according to their position in the Merkle root and the position in the root chain, we can obtain a deterministic receipt queue, which will be processed by the shard in sequence.
- The cursor tells which receipt has been processed by the shard block in the queue, and thus the rest of the queue is called post-block unprocessed receipt queue, which can be very long due to DoS (however, the queue can be constructed by any BP of the shard on-demand and asynchronously according to A1 and A2, and thus all BP of the shard to be attacked won’t be overwhelmed by the DoS attack)

## Steps

The following are the steps for a cross-shard transaction:

1. A user generates a cross-shard transaction from shard i to shard j, and the tx is included in shard i block A.  The receipts of all txs of the block are generated and its Merkle root is included in a future root block.
2. At target shard j, upon observing a new root block and creating a new shard block, the BP of shard j create a pre-block unprocessed receipt queue by electing to include the root block or not in the shard block and :

- If a root block is not included, the pre-block unprocessed receipt queue of the new block equals to the post-block unprocessed receipt queue of the previous block
- If a root block is included, the pre-block unprocessed receipt queue of the block is constructed by appending all receipts included to the post-block unprocessed receipt queue of the previous block.  Again, the construction can be on-demand and asynchronously according to A1.

When creating a shard block, the **consensus** forces that a valid block must process the receipts in the pre-block unprocessed receipt queue until the queue is empty or a pre-set cross-shard transaction gas limit is exhausted.  The pseudo-code looks like:

```
def process_receipts(state, xshard_gas_limit, cursor):
  xshard_gas_remained = xshard_gas_limit
  while xshard_gas_remained > 0 and cursor.has_next() and cursor.peek().startgas > xshard_gas_remained:
      receipt = cursor.next()
      xshard_gas_remained = process_one_receipt(state, receipt)
return state, xshard_gas_remained, cursor
```

## Comments

### Guaranteed and ordered delivery via incentives

According to A2 and A3, as long as the receipt queue is deterministically ordered, the delivery is also ordered.  To ensure guaranteed delivery, i.e., to encourage a BP of a shard to include the latest root block (and thus forcibly process the receipt queue), we could have

- (Incentive from cross-shard receipt tx fee). If the BP doesn’t include the root block while the unprocessed receipt queue is empty, it will waste its cross-shard gas limit and the corresponding tx fee;
- (Incentive from block reward). In the case tx fee is small, we could further incentivize the BP as follows: if a BP includes a new root block, it will collect a full block reward rather than a partial block reward.

### DoS Attack

If an attacker sends overwhelming receipts from other shards to destination shard, the attack won’t prevent the BPs of the target shard from working:

- According to A3, the receipt queue can be constructed on-demand and asynchronously to the current block production of the shard.
- Each shard block will process the receipts with gas up to cross-shard gas limit

### Happen-before guarantee

The generating of the receipt at source shard and the processing of the receipt at target shard is a **partial order**.

## Other notes

- Gas limit for a receipt:  The gas limit of a receipt cannot greater than cross-shard gas limit.
- Mathematical description: An early mathematical description of the model can be found in [1, Section III.E]

