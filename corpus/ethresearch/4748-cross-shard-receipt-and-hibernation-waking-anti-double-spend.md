---
source: ethresearch
topic_id: 4748
title: Cross-shard receipt and hibernation/waking anti-double-spending
author: vbuterin
date: "2019-01-04"
category: Sharding
tags: [cross-shard, hibernation]
url: https://ethresear.ch/t/cross-shard-receipt-and-hibernation-waking-anti-double-spending/4748
views: 4705
likes: 2
posts_count: 5
---

# Cross-shard receipt and hibernation/waking anti-double-spending

*Special thanks to [@jvluso](/u/jvluso) for inspiration*.

Prerequisites:

- Improving the UX of rent with a sleeping+waking mechanism
- A minimal state execution proposal

The general process for a cross-shard transaction (for an example, we’ll use transferring 5 ETH) is:

- On shard A, destroy 5 ETH, creating a receipt (ie. a Merkle branch with a root committed into the state root of that block) containing (i) the destination shard, (ii) the destination address, (iii) the value (5 ETH), (iv) a unique ID.
- Once shard B becomes aware of the state roots of shard A up until that point, submit a Merkle branch proving that receipt into shard B. If the Merkle branch verifies and that receipt has not already been spent, generate the 5 ETH and give it to the recipient.

To prevent double-spends, we need to keep track in storage which receipts have already been claimed. To make this efficient, receipts need to be assigned sequential IDs. Specifically, inside each source shard, we store a next-sequence-number for each destination shard, and when a new receipt is created with source shard A and destination shard B, its sequence number is the next-sequence-number for shard B in shard A (this next-sequence-number gets incremented so it does not get reused). This means that in each destination shard we only need to keep track of SHARD_COUNT bitfields, one for each source shard, to prevent double spends, which means a cost of only one bit of storage per cross-shard tx.

**Notice that there is an opportunity for protocol simplification here by unifying two mechanics**: we can make a contract hibernation/waking process simply be a compulsory cross-shard transaction, except with the source and destination being the same. The second half of the cross-shard transaction (the receipt publication) would simply happen whenever anyone wishes to wake the contract.

Now, we still need to deal with one problem with this scheme: it creates permanent storage for each cross-shard transaction (and for each hibernation/waking). It is only one bit of permanent storage, but still permanent storage nonetheless. Assuming 10 cross-shard transactions plus hibernations per second coming into each shard, that’s 315M bits ~= **39 MB per year of storage**.

We *could* simply grin and bear it, but there is another alternative. We break up time into N-block periods (eg. N blocks = 1 year). If the current period is `k`, we store in the state a list of sequence IDs that have been consumed during periods `k-1` and `k`. When the period increments to `k+1`, we remove the list for period `k-1` from the state, and store the Merkle root of this list as a receipt (eg. in a [DBMA](https://ethresear.ch/t/double-batched-merkle-log-accumulator/571)).

If someone wishes to claim in period `k` a receipt that was produced in period `j < k-1`, then for every period in `j.....k-2` they would need to provide a Merkle proof showing that that receipt has not yet been consumed.

This scheme has the following properties:

- Max storage requirements: a few hundred MB per shard (39 MB in the best case if everyone is consuming receipts within one period, but it could become larger if consuming very old receipts happens frequently, as the total entropy  of the ~400 million ID numbers being consumed within some period would be higher)
- Max length of a Merkle proof: ~1 kb per year

There is a natural linear tradeoff here: we can have 10x less storage in exchange for 10x longer Merkle proofs for resurrecting old contracts by simply shortening the length of a period.

## Replies

**dlubarov** (2019-01-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This means that in each destination shard we only need to keep track of SHARD_COUNT bitfields, one for each source shard, to prevent double spends, which means a cost of only one bit of storage per cross-shard tx.

What do you think of requiring that cross-shard receipts be consumed in order? Then shards would store just the sequence number of the last consumed receipt (per source shard). That’s the approach we’re planning to take for our project.

Granted, the order requirement means that we can’t rely on an individual user to forward their receipt to the receiving shard, otherwise cross-shard channels could get stuck. But (at least in our model) receipt forwarding doesn’t necessarily have to be performed by the transaction author. We could allow anyone to forward cross-shard receipts to the receiving shard, perhaps with a small reward.

---

**vbuterin** (2019-01-05):

> What do you think of requiring that cross-shard receipts be consumed in order?

The problem with that is that it means that it requires a gas model where receipts on the start shard consume gas of the destination shard. Totally doable, but I think it’s likely out of scope for Serenity at this point.

---

**jvluso** (2019-01-08):

I’m glad to see that suggestion was helpful.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> We could simply grin and bear it, but there is another alternative. We break up time into N-block periods (eg. N blocks = 1 year). If the current period is k , we store in the state a list of sequence IDs that have been consumed during periods k-1 and k . When the period increments to k+1 , we remove the list for period k-1 from the state, and store the Merkle root of this list as a receipt (eg. in a DBMA ).

I hadn’t heard of MMRs before, but they seem great for this. Do you think it would be helpful to use merklized  bloom filter trees in the mountains to make proving that the ids aren’t in the tree faster?

---

**vbuterin** (2019-01-15):

I don’t expect bloom filters to be useful here. Bloom filters are useful for ethereum 1.0 receipts because the values you’re checking against are 256-bit hashes, so checking non-membership “the dumb way” would require downloading a lot of data. Here though, indices are assigned sequentially, and we already have a fairly optimized bitfield for checking inclusion, so I don’t think they would help more on top of that.

