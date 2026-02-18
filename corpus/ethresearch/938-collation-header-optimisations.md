---
source: ethresearch
topic_id: 938
title: Collation header optimisations
author: JustinDrake
date: "2018-01-28"
category: Sharding
tags: []
url: https://ethresear.ch/t/collation-header-optimisations/938
views: 2102
likes: 3
posts_count: 6
---

# Collation header optimisations

To save gas in the main shard (and for the aesthetics of keeping things clean) we propose various collation header changes. For clarity of exposition we reduce the current header in two steps. The aim of this post is to brainstorm several changes to spark a discussion so that the best ideas eventually get cherry-picked to design an optimal collation header.

The currently specified [10-element collation header](https://github.com/ethereum/sharding/blob/develop/docs/doc.md#collation-header) is:

```auto
[
    shard_id: uint256,
    expected_period_number: uint256,
    period_start_prevhash: bytes32,
    parent_hash: bytes32,
    transactions_root: bytes32,
    coinbase: address,
    state_root: bytes32,
    receipts_root: bytes32,
    number: uint256,
    sig: bytes
]
```

with size 32+32+32+32+32+20+32+32+32+65 = 341 bytes. The first proposed reduced header is:

```auto
[
    collation_id: uint256
    expected_period_number: uint256
    log_root: bytes32
    state_root: bytes32
    parent_hash: bytes32
]
```

The changes are:

1. Rename number to collation_number and then merge shard_id and collation_number into collation_id := (shard_id << 128) + collation_number. The collation_id naturally identifies a collation within the 2-dim (shard_id, collation_number) collation vector space. Notice 128 bits suffice for the two coordinates. Even assuming a new shard is spawned every second or a new collation is added every second there’s enough bit space for 10^42 years.
2. Remove period_start_prevhash as it seems to be derivable from expected_period_number.
3. Merge transactions_root and receipts_root into log_root. Semantically transactions and receipts are both logs, just a different type. It is natural to merge them under the same accumulator. To distinguish types we suggest adding a corresponding prefix (such as TYPE_TX and TYPE_RECEIPT) to the log before hashing. Instead of using a Patria trie, we suggest using a Merkle tree with ordered leaves. By ordering the leaves we retain the power of tries (namely, non-membership proofs) and gain the following:

Exceptional/adversarial O(n) witnesses go away—more predictability, more fairness
4. We don’t have to suffer the 10% in trie witness overhead estimated by Vitalik
5. Possibly a slight performance improvement in Merklelisation
6. Assuming collation rewards are awarded in collations (as opposed to the main shard, c.f. this post) then I don’t think it is necessary to expose coinbase in the header.
7. As previously noticed by Vitalik the sig can be optimised away by reusing the signature from the transaction calling the VMC.

The second proposed reduced header is:

```auto
[
    collation_id: uint256
    collation_root: bytes32
    parent_root: bytes32
]
```

The changes are:

1. Put expected_period_number somewhere else. Either:

Fit expected_period_number % (2 ** 32) in collation_id. Assuming 14 second block times and 5 blocks per period, then 2 ** 32 blocks corresponds to about 10,000 years.
2. Grind expected_period_number % (2 ** 16) into collation_root. Assuming 14 second blocks times and 5 blocks per period, then 2 ** 16 blocks corresponds to 53 days which is enough to cover any kind of reasonable shard reorg, and 16 bits is small enough to grind into collation_root.
3. Merklelise log_root, state_root and the collation header hash into the collation_root. Merklelise all the things!
4. Replace parent_hash (a “dumb” hash) by parent_root (a “smart” root that nicely mirrors collation_root).

It seems we can make collation headers just 96 bytes (72% reduction). The `collation_id` describes “the where”, the `collation_root` describes “the what”, and the `parent_root` allows for a hash chain.

## Replies

**mhchia** (2018-01-29):

The idea is great and smart!

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Remove period_start_prevhash as it seems to be derivable from expected_period_number

Won’t there be issues If we remove `period_start_prevhash`?

Assume one made a `addHeader` transaction which was to be included in a specific chain, and it’s desiring `period_start_prevhash` is `hash_a`. However, one fork then occurred. Therefore the `period_start_prevhash` of the same period became `hash_b`. The `addHeader` transaction will still be accepted if we removed `period_start_prevhash` in the collation header. I’m not sure if there will be any problem in this situation.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Assuming collation rewards are awarded in collations (as opposed to the main shard, c.f. this post) then I don’t think it is necessary to expose coinbase in the header.

In this case we just award the rewards to collators(which are exactly the `addHeader` transaction senders)?

---

**jannikluhn** (2018-01-29):

With RLP encoding at least the numbers should already be quite compressed, shouldn’t they? Or are the values padded for simpler decoding in the contract?

---

**JustinDrake** (2018-01-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/mhchia/48/643_2.png) mhchia:

> Won’t there be issues If we remove period_start_prevhash?

That’s an interesting point. A collation header passes `addHeader` only if `parent_root` matches. So the main shard would need to reorg in such a way that `parent_root` stays the same given `expected_period_number`. In that case, from the point of view of the child shard, reality hasn’t changed. If anything, we probably want child shards to gracefully recover from main shard reorgs to avoid unnecessarily stalling the child shard and wasting gas on collation headers that are otherwise valid.

![](https://ethresear.ch/user_avatar/ethresear.ch/mhchia/48/643_2.png) mhchia:

> In this case we just award the rewards to collators(which are exactly the addHeader transaction sender)?

The idea is for the collation body (*not* the header) to be responsible for collation rewards. This can be be done for example by having the last transaction in a collation be a special coinbase transaction.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> With RLP encoding at least the numbers should already be quite compressed, shouldn’t they? Or are the values padded for simpler decoding in the contract?

My understanding is that any compression from RLP encoding does not reduce gas. As for padding values vs packing them, that’s a good pint, I’m not sure what would be most gas efficient for the VMC.

---

---

Third iteration on the collation header:

```auto
[
    locator: uint256
    root: bytes32
    parent_root: bytes32
]
```

The changes are:

1. Rename collation_id to locator. (The word “id” usually implies uniqueness, which we don’t have here. Removed “collation” as it’s redundant.)
2. The locator packs the location data (shard, number, period) where shard is given 128 bits and number and period are both given 64 bits. The reason for giving shard 128 bits is that shard identifiers do not need to be linearly ordered, whereas number and period are much more restricted starting at 0 and repeatedly incrementing by 1.
3. Maybe there’s an argument to include an extra field which is left unrestricted, or reserved for future use. The locator could then be (shard, number, period, extra) where each entry spans 64 bits.
4. Rename collation_root to just root. There’s no ambiguity here.
5. To be very explicit, root would be Merklelisation of transactions_root, receipts_root, parent_root and locator.

---

**vbuterin** (2018-01-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/mhchia/48/643_2.png) mhchia:

> Won’t there be issues If we remove period_start_prevhash?
>
>
> Assume one made a addHeader transaction which was to be included in a specific chain, and it’s desiring period_start_prevhash is hash_a. However, one fork then occurred. Therefore the period_start_prevhash of the same period became hash_b. The addHeader transaction will still be accepted if we removed period_start_prevhash in the collation header. I’m not sure if there will be any problem in this situation.

If we specify period number but not period prevhash, then a collation’s validity would depend not just on the collation itself but also the state of the blockchain; that is, a collation with the exact same data could flip from invalid to valid or back if the main chain has a reorg. This may be a real problem.

On the other hand, if client implementations don’t care about headers, and only care about logs, then we could just have the `addHeader` function “reconstruct” the header, adding in the prevhash start data and making the collation hash based on that, and it could be fine.

I currently lean in favor of requiring the full period prevhash to be in the collation header. In a philosophical sense, the parent of a collation and the collation header prevhash are both “parents” of the collation; they are both things that the collation execution depends on. Hence, it seems prudent to treat them similarly.

I also philosophically dislike “grinding” stuff into hashes; I’d rather just have them be separate data fields. Remember that from a gas perspective, zero bytes are changed at 4 gas/byte and nonzero bytes at 68 gas/byte, so the gains from shoving small numerical fields together are actually quite small.

Collapsing tx root, coinbase, state root, receipts root into collation_root seems very smart.

---

**JustinDrake** (2018-01-30):

I may have an optimal solution regarding `period_start_prevhash`: replace it by the hash of the receipt in the main shard for the transaction that adds the parent collation header. Reasons this is optimal:

1. It allows for the collation’s validity to only depend on the collation itself, while minimising unnecessary constraints for adding new collation headers. For example, main shard reorgs in the current expected period would no longer force validators to rebroadcast collation headers. Also, notice that including period_start_prevhash prevents two consecutive collation headers from being included in the same block which impedes optimisations such as loose periods.
2. It allows for the removal of parent_root as it would be Merklelised under the parent receipt hash. The duplication of hashes in the hash chain (once as root, once as parent_root) always felt a bit “wasteful” to me. We now simultaneously only have one “parent” hash, and the collation header hashchain is optimally granular.

The fourth iteration on the collation header is looking something like:

```auto
[
    shard: uint256
    number: uint256
    period: uint256
    root: bytes32
    parent_receipt: bytes32
]
```

with the optional packing of `(shard, number, period)` under a single uint256 called `locator`.

