---
source: ethresearch
topic_id: 2023
title: Proving UTXO Sum Validity for Mass Exits
author: kfichter
date: "2018-05-17"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/proving-utxo-sum-validity-for-mass-exits/2023
views: 2457
likes: 1
posts_count: 10
---

# Proving UTXO Sum Validity for Mass Exits

This is an edited copy/paste from [omisego/research](https://github.com/omisego/research/issues/35).

It seems like it’ll be necessary for the user that submits a mass exit to attach a summation of the value of all referenced UTXOs. For example, if exiting UTXOs worth (10 ETH, 20 ETH, 15 ETH), then the user will also attach the value “45 ETH” in some way. When the mass exit processes, this sum will be “reserved” for mass exit to be processed on a per-UTXO basis later. This is necessary so that invalid exits that process after 2 weeks can’t steal money while the mass exit is still being processed.

Unfortunately, it isn’t easy to prove that this summation is valid. The above user might attach “50 ETH”, which would obviously be invalid. We don’t want users to be able to steal money in this manner.

One possible solution to this problem is a sum Merkle tree of sorts. Each leaf node in the tree would contain the tuple (`utxo_value`, `total_sum`), where `total_sum` represents the sum of all leaf nodes to the left of this node, inclusive of the node itself. For example, if the UTXO values are 10 ETH, 20 ETH, 15 ETH, then the leaf nodes would be (10, 10), (20, 30), (15, 45).

These leaves would be Merklized and the final sum + tree root would be published along with the mass exit. The tree could be challenged in a TrueBit-esque game where two users iterate down the tree until they find the first leaf node at which they disagree. They reveal this node as well as the leaf node to the left of this node. The root chain makes a calculation to determine which party is correct (`left_total_sum` + `right_utxo_value` = `right_total_sum`).

Note that this requires log(n) transactions to the root-chain in the worst case, which is not ideal. This may be way too many back-and-forth responses for the average user, although we might not consider mass-exit submitters to be average users (?). We could trivially prove fraud in 1 O(n)-sized transaction by revealing the entire UTXO set, but this is almost definitely too big. It may be possible to construct more concise proofs, but I haven’t figured out anything better (yet).

I’d love to know if research on this topic has been done before.

## Replies

**MaxC** (2018-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> These leaves would be Merklized and the final sum + tree root would be published along with the mass exit. The tree could be challenged in a TrueBit-esque game where two users iterate down the tree until they find the first leaf node at which they disagree. They reveal this node as well as the leaf node to the left of this node. The root chain makes a calculation to determine which party is correct ( left_total_sum + right_utxo_value = right_total_sum ).

I don’t think this will work  in vanilla plasma because if the last unavailable block is challenged, no one has any way of knowing whether the UTXO sum corresponds to the UTXOs from the bitfield. However, it would be possible to do this if UTXOs were indivisible, i.e. each UTXO has one input and one output.

I had a similar idea for sum trees a while back for mass withdrawals in plasma cash, where this ought to be possible because each bit in the bit-field is linked to a single coin.

---

**kfichter** (2018-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> I don’t think this will work in vanilla plasma because if the last unavailable block is challenged, no one has any way of knowing whether the UTXO sum corresponds to the UTXOs from the bitfield.

To clarify, we would also add a “UTXO tree” to each block, so it should be clear if the sum is correct. Each mass exit would point to a specific UTXO tree, the bitfield would be over this tree instead of over all outputs. The UTXO tree is consensus crtical, so a withheld tree forces all users to exit.

This UTXO tree construction makes the bitfield more efficient, but we can also request the operator perform more interesting aggregations (like an aggregations of UTXOs for a specific address). This should be scriptable.

The bitfield/sum is deterministic from the UTXO tree, so either the tree is available and the sum can be challenged, or the tree is unavailable and everyone must exit (fine b/c time-wise priority).

---

**MaxC** (2018-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> This UTXO tree construction makes the bitfield more efficient, but we can also request the operator perform more interesting aggregations (like an aggregations of UTXOs for a specific address). This should be scriptable.

Do the withdrawals also contain the entire UTXO tree? If yes, it should work, if not it seems unworkable.

---

**kfichter** (2018-05-17):

Withdrawals only contain the reference to the tree (block #), a bitfield, and a sum/sum tree root. The root of the UTXO tree is stored with each block.

---

**MaxC** (2018-05-17):

Then an operator can grief?

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> The bitfield/sum is deterministic from the UTXO tree, so either the tree is available and the sum can be challenged, or the tree is unavailable and everyone must exit (fine b/c time-wise priority).

How do you deal with the  withdrawals from the latest block which is unavailable? No challenger  can tell whether the amount withdrawn is or is not equal to the sum of the UTXO amounts as specified by the bitfield.

I suppose one way could be to use a randomly drawn committee to attest to the data-availability of mass withdrawals.

---

**kfichter** (2018-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> No challenger can tell whether the amount withdrawn is or is not equal to the sum of the UTXO amounts as specified by the bitfield.

This is fine in Plasma MVP, right? The sum can’t be challenged, but every well-behaved user will exit and be processed before the mass exit is processed. Note that the mass exit can be given a priority equal to something like the last possible transaction in the specified block #.

---

**MaxC** (2018-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> block

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> This is fine in Plasma MVP, right? The sum can’t be challenged, but every well-behaved user will exit and be processed before the mass exit is processed. Note that the mass exit can be given a priority equal to something like the last possible transaction in the specified block #.

Good question. I think it’s ok in Plasma because  according to [this](https://www.reddit.com/r/ethereum/comments/7pkuab/how_does_plasma_compress_state_using_utxo/), for every UTXO you try to exit with, you provide a Merkle proof that proves the UTXO referenced was included in some Plasma block.

---

**MaxC** (2018-05-17):

I think using data availability solutions is definitely the way to go for mass exits.

---

**kfichter** (2018-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> I think using data availability solutions is definitely the way to go for mass exits.

I’m inclined to agree, although I think it reduces the security to the security of the mechanism that determines availability. Maybe we just have one well-secured (delphi-like) mechansim to attest to data availability and allow it as a plug-in for Plasma chains comfortable with it.

