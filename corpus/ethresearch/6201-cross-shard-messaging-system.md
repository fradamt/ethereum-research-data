---
source: ethresearch
topic_id: 6201
title: Cross-Shard Messaging System
author: adiasg
date: "2019-09-26"
category: Sharding
tags: []
url: https://ethresear.ch/t/cross-shard-messaging-system/6201
views: 5610
likes: 1
posts_count: 7
---

# Cross-Shard Messaging System

This post outlines an ***in-protocol*** cross-shard messaging system by proposing changes to the block validity and fork choice rules. This is a part of the CBC Casper sharding proposal, but can be easily applied to later phases of Eth2.0. A description of this can be found in the [CBC Casper draft paper](https://github.com/cbc-casper/cbc-casper-paper/blob/acc66e2ba4461a005262e2d5f434fd2e30ef0ff3/cbc-casper-paper-draft.pdf) in Section 4.6

# 1. Objective

Eth2.0 supports cross-shard messaging on an out-of-protocol basis, meaning that users have to manually perform some operations to deliver a cross-shard message. The protocol handles the delivery of the receipt of the transaction from a shard chain to the beacon chain, and the user has to create a transaction on the recipient shard that refers to this receipt.

[![image](https://ethresear.ch/uploads/default/optimized/2X/e/e77798d734620817e32e26701c7b8976bedd269b_2_517x238.png)image952×440 21.3 KB](https://ethresear.ch/uploads/default/e77798d734620817e32e26701c7b8976bedd269b)

The goal is to have a protocol which handles the end-to-end delivery of the cross-shard message, in which the user only has to generate a transaction on the first shard chain.

[![image](https://ethresear.ch/uploads/default/optimized/2X/8/87058648f17ec3d961b51c9d8b4833499943bb4c_2_517x244.png)image959×454 27.8 KB](https://ethresear.ch/uploads/default/87058648f17ec3d961b51c9d8b4833499943bb4c)

# 2. Proposal

## 2.1. Block Structure

Blocks now contain 2 new logs, one for sent messages (in this block) and received messages (in this block) each.

## 2.2. Messages

Messages are objects that contain:

- sender_shard_ID
- recipient_shard_ID
- final_destination_shard_ID
- target_block on the recipient shard
- blocks_to_live parameter
- payload_tx

Any cross-shard message is going to have to make 2 hops - Shard A to Beacon Chain, and Beacon Chain to Shard B. `sender_shard_ID` and `recipient_shard_ID` are for the specific hop, and `final_destination_shard_ID` identifies Shard B.

The message can be received in blocks on the recipient shard between heights `height(target_block)+1` and `height(target_block)+blocks_to_live`.

[![image](https://ethresear.ch/uploads/default/optimized/2X/1/16f8ef8713adaea98a3fccda746e99e57a58cf30_2_690x202.png)image980×287 12.5 KB](https://ethresear.ch/uploads/default/16f8ef8713adaea98a3fccda746e99e57a58cf30)

In the above figure, the `target_block` is `b2` and `blocks_to_live` is 2. This message can be received only in blocks `b3` & `b4`.

## 2.3. Block Validity & Fork Choice

The atomicity of sends and receives needs to be maintained; either a message is sent in the sender shard and received in the recipient shard (eventually), or it does not appear anywhere.

I’ll skip the obvious ones like: each message can only be received once, chains can only receive messages destined for themselves, etc.

### 2.3.1. Shard Chains

The shard chain fork choice follows the beacon chain fork choice, and these modifications enforce the send-receive atomicity:

- If the beacon chain sends a shard some message, then the target_block is in the fork choice on the shard chain.
- If the beacon chain receives some message from a shard, the sender block is in the fork choice on the shard.
- If the beacon chain does not receive a shard chain message by it’s expiry, then the sender block is orphaned in the shard.
- Any shard chain block that doesn’t receive a yet-unreceived message by it’s blocks_to_live expiry is orphaned.

The below figure illustrates the first rule:

[![image](https://ethresear.ch/uploads/default/optimized/2X/2/257d1443ed4b7d918629fec8d220d3af569a820d_2_517x235.png)image1118×510 18.5 KB](https://ethresear.ch/uploads/default/257d1443ed4b7d918629fec8d220d3af569a820d)

The below figure illustrates the second rule:

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/317a5ce5d533d649c88ea23ef30365a7052700d9_2_517x227.png)image1095×482 18.4 KB](https://ethresear.ch/uploads/default/317a5ce5d533d649c88ea23ef30365a7052700d9)

### 2.3.2. Beacon Chain

The beacon chain block validity rule enforces that messages received in a block are immediately redirected and sent to the final destination. If a message is in the receive log of a block, it must also appear on the sent log of the block with:

- sender_shard_ID identifying the beacon chain
- recipient_shard_ID as the final_destination_shard_ID of the received message
- appropriate target_block and blocks_to_live on the recipient shard

Since the shard chain fork choices are dependent on the beacon chain fork choice, the beacon chain fork choice must follow this rule to avoid chaos in the shards:

- The beacon chain cannot send to/receive from one fork of a shard and later send to/receive from a conflicting fork of the shard. (“send to a fork” refers to the fork containing the target_block)

The purpose of this fork choice rule is to avoid the below situation:

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/3d03781b3b392d5b6c68e9863a4d4716b84b4325_2_517x182.png)image1077×380 19.4 KB](https://ethresear.ch/uploads/default/3d03781b3b392d5b6c68e9863a4d4716b84b4325)

# 3. How Are Messages Traveling Between Shards?

Messages can get from the beacon chain to the shards/from shards to the beacon chain naturally because of the way validators are distributed:

- Messages from the beacon chain to a shard chain are seen by all validators on the shard, since they are also validators on the beacon chain. Validators on the shard chain also have all necessary information for executing the fork choice.
- Messages sent from a shard to the beacon chain are collected by the respective crosslink committee and included in the crosslink information on the beacon chain. It is important to note that not all beacon chain validators have access to necessary information for executing the beacon chain fork choice and block validity rules. The requirement is that atleast one of the validators on the shard chain provides fraud proofs in case the stated rules are broken.

## Replies

**adlerjohn** (2019-09-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/adiasg/48/1635_2.png) adiasg:

> It is important to note that not all beacon chain validators have access to necessary information for executing the beacon chain fork choice and block validity rules.

I’m admittedly still not familiar with the nomenclature used for Casper, but is that supposed to be worded like that? I would assume that all beacon chain validators have enough information to execute the beacon chain fork choice rule—if not, how would they be able to stay in consensus? I would also assume that all beacon chain validators can execute a beacon chain block validity function—if not, how would they be able to stay in consensus? A fraud proof for an invalid crosslink shouldn’t invalidate any beacon chain block, otherwise economic finality isn’t possible.

---

**adiasg** (2019-09-26):

Let’s consider the below situation:

[![image](https://ethresear.ch/uploads/default/optimized/2X/e/e7c0339de4ee00a3c52113aa6024c483e5b77601_2_690x224.png)image1050×342 19 KB](https://ethresear.ch/uploads/default/e7c0339de4ee00a3c52113aa6024c483e5b77601)

Note that the beacon chain fork choice rule is broken in this case:

![](https://ethresear.ch/user_avatar/ethresear.ch/adiasg/48/1635_2.png) adiasg:

> The beacon chain cannot send to/receive from one fork of a shard and later send to/receive from a conflicting fork of the shard. (“send to a fork” refers to the fork containing the target_block )

The beacon chain validators who are’t in the shard committee or crosslink committee will not be able to detect the above situation on their own. The assumption is that at least one validator from the shard committee or the crosslink committee will provide a fraud proof for this to the beacon chain. Up til here, this is similar to the situation where an invalid state of a shard gets into the crosslink on the beacon chain.

The purpose of invalidating that beacon chain block is to maintain the send-receive atomicity:

![](https://ethresear.ch/user_avatar/ethresear.ch/adiasg/48/1635_2.png) adiasg:

> either a message is sent in the sender shard and received in the recipient shard (eventually), or it does not appear anywhere

You’re right that this isn’t the best way to go about it, since a colluded crosslink committee can have the power to invalidate a part of the beacon chain at their will sometime in the future.

Perhaps we can have a rule which allows the beacon chain to invalidate specific previously sent/received messages, which has the effect of invalidating the corresponding shard block which received/sent the message?

---

**vbuterin** (2019-09-27):

This seems like it requires the beacon chain to do work for every cross-shard message that takes place (at the very least, it must contain it in the receive and send log). How does this avoid causing the beacon chain to incur O(C^2) overhead, causing it to quickly get overloaded?

In general, it seems like any scheme where the beacon chain explicitly processes messages, rather than processing roots of large sets messages, has this property.

---

**adiasg** (2019-09-27):

Ah, that’s right. This puts an O(C^2) load on the beacon chain.

This starts making more sense in the CBC sharding proposal, which is a multi-level hierachical sharding scheme.

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/76b14dba3ba07b83f4205d3c47ff61ad01c7af80_2_690x372.png)image1044×563 30.8 KB](https://ethresear.ch/uploads/default/76b14dba3ba07b83f4205d3c47ff61ad01c7af80)

The root shard only processes messages which are routed between the depth 1 siblings. Through proper load balancing and message routing costs, we can avoid the O(C^2) overloading. E.g., we can charge higher fees to process message routed through shards at lower depth. The goal is to encourage (or force through in-protocol load balancing) the clustering of frequently communicating entities in lower shard subtrees.

---

**vbuterin** (2019-09-27):

Right, I see; so this assumes the CBC-sharding hierarchical shard system.

I’m personally not a proponent of that system; I think it would put too much load on the root shard. For example assuming uniform activity across shards, fully 50% of all activity would have to go through the root chain. I’m sure in reality most activity is not uniform, but if even 5% of activity is uniform then that’s already a maximum cap of 40x on scalability.

---

**adiasg** (2019-09-28):

About above calculation: If 5% of cross-shard activity is uniform, then 2.5% of all cross-shard messages are passing through the root shard, and there is a 40x scalability limit.

However, the load from 2.5% of all cross-shard messages is not the same as 2.5% of the *total load of the system*. If we assume that cross-shard messaging consumes 10% of the system load, then the root shard bears 0.25% of total system load, leading to a 400x scalability limit.

