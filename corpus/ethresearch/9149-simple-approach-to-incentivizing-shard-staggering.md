---
source: ethresearch
topic_id: 9149
title: Simple approach to incentivizing shard staggering
author: vbuterin
date: "2021-04-11"
category: Sharding
tags: []
url: https://ethresear.ch/t/simple-approach-to-incentivizing-shard-staggering/9149
views: 5629
likes: 6
posts_count: 11
---

# Simple approach to incentivizing shard staggering

One of the ideas that becomes possible with sharding is the concept of *staggering*: having shards produce blocks at different times, allowing the system as a whole to have blocks at a regular frequency of more than one per second. Layer-2 projects (eg. rollups) built on top of this system could then have latencies on the order of a second or lower, despite the system as a whole having 12-second latencies.

[![shards1](https://ethresear.ch/uploads/default/original/2X/3/3de5d8fd3bda30619c24fbe8fd94889d2a0a808f.png)shards1721×201 3.55 KB](https://ethresear.ch/uploads/default/3de5d8fd3bda30619c24fbe8fd94889d2a0a808f)

*The four colors represent four shards; each shard and the beacon chain have a latency of k seconds, but the system as a whole has a block appearing once every \frac{k}{4} seconds.*

A significant challenge in implementing this, however, is incentives. Even if we add a protocol rule that shard proposers are “supposed to” publish their shard blocks at asymmetric times (eg. shard 0 publishes 1/8 after the start of a slot, shard 1 publishes 3/8 after the start of a slot, etc), the “supposed to” matters little if there are no actual protocol rules that ensures that this actually happens.

**There are incentives that govern when block producers publish blocks: if you publish too early, you miss out on transactions, if you publish too late, you risk the block not getting included, and somewhere in the middle is the optimum. If we want shard blocks to be staggered, we need incentives that differ between shards so that the optimal publishing time is staggered too.**

Let N = 64 be the number of shards. Let D = [8, 16, 24, 32] be a list of distances. Define an “optional ancestry link” as a link from the (k - D[i])'th header to the k'th header (the z'th header here means the header of shard k\ mod\ N in slot \lfloor \frac{z}{N} \rfloor).

[![shards2](https://ethresear.ch/uploads/default/original/2X/0/08161c41753ef992ea12cc5bb016c0c74bede0a1.png)shards2721×201 7.44 KB](https://ethresear.ch/uploads/default/08161c41753ef992ea12cc5bb016c0c74bede0a1)

*Dotted lines represent optional ancestry links for N = 4 and D = [2, 3].*

### Idea 1: one byte per optional ancestry link in the header

We add to the shard header an “ancestry checksum” with |D| bytes: byte i of the k'th header is expected to be the same as the first byte of the hash of the (k - D[i])'th header. So for each optional ancestry link, there is a one-byte slot to include the first byte of the hash of the ancestor block.

These ancestry checksums being correct is not necessary for validity; it’s okay for shard headers to provide an ancestry checksum with some or all bytes being invalid. Rather, we add incentives to *encourage* them to be correct, without mandating it.

Note also that instead of requiring a shard block at slot N to reference the beacon block at slot N and be eligible for inclusion in slot N+1, we move the inclusion slot up to N+2. This allows shard blocks to be published around the same time as the beacon blocks themselves, so there is no “hole” in shard block progression around the time when beacon blocks get proposed.

### Idea 2: one hash per optional ancestry link in the body

The first D chunks of a shard header body are reserved for ancestry links. Specifically, the i'th chunk of the k'th shard block is expected to be the same as the hash of the (k - D[i])'th header.

These hashes being correct is not necessary for validity; rather, we add incentives to *encourage* them to be correct, without mandating it.

### Idea 3: checksum based on contents instead of header

*Notation note: “[W]” means “a Kate commitment to the polynomial W”, e(a, b) is a pairing.*

Let P be the polynomial committed to by the (k - D[i])'th header, and let z be the proposer’s private key. The first chunk of the shard block body is expected to equal P(z). Note that this is a linear function of the entire shard block body, and it requires the entire body to calculate.

It can easily be proven with a Kate proof: let Q(X) = P(X) // (X - z), where [Q] can be verified by checking e([X - z], [Q]) = e([P - c], [1]) where c is the claimed value. [X-z] can be computed as [X] - Z where Z is the proposer’s public key (so verification can be done publicly).

Using a function of the shard block body and the proposer’s private key ensures that the proposer needs to download and check the entire shard block body, and encourages the proposer of the older block to actually publish the data quickly. This mechanism does require the proposer to get on a few extra shards when they get assigned to propose, but it only affects the proposer so total impact on validator node complexity is low.

## Ancestry checksum incentives

The core incentive in all three cases is simple. If a shard block correctly includes an optional ancestry link to another shard block, then we add a probabilistic lottery: based on some future RANDAO value, there is a \frac{1}{X} chance that a reward of size proportional to X is applied to *both* the producer of the shard block that included the link *and* the producer of the shard block that was included.

## Replies

**imkharn** (2021-04-12):

Under the ‘only publish the header’ method, what is the penalty for withholding the contents for byzantine or MEV reasons and how long does that penalty take to occur?

---

**vbuterin** (2021-04-13):

The penalty would be that shard block not getting accepted, and you would have to withhold it for at least a full slot for that penalty to come into play.

---

**dankrad** (2021-04-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Note also that instead of requiring a shard block at slot NN to reference the beacon block at slot NN and be eligible for inclusion in slot N+1N+1 , we move the inclusion slot up to N+2

In the case of shard execution, this would increase the cross-shard delay from 1 to 2 slots?

But we probably aren’t optimizing for that anymore/might use a different scheme for execution shards.

---

**vbuterin** (2021-04-13):

> In the case of shard execution, this would increase the cross-shard delay from 1 to 2 slots?

I suppose we could make the 2-slot delay *only* for those shards that have either very low or very high shard numbers and so are intended to be published in parallel with a shard block.

---

**barnabe** (2021-04-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Using a function of the shard block body and the proposer’s private key ensures that the proposer needs to download and check the entire shard block body, and encourages the proposer of the older block to actually publish the data quickly.

If A is the ancestor block and B is the new block, is it that P is a commitment of A’s body, z is B’s proposer’s private key and B’s body includes P(z), so that B’s proposer must download A to evaluate P(z)?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> based on some future RANDAO value, there is a 1/X chance that a reward of size proportional to X is applied to both the producer of the shard block that included the link and the producer of the shard block that was included.

Why should that be probabilistic vs a fixed reward? I don’t understand what X refers to here, is the intent to have varying rewards based on k \mod N?

---

**vbuterin** (2021-04-14):

> If A is the ancestor block and B is the new block, is it that P is a commitment of A’s body, z is B’s proposer’s private key and B’s body includes P(z) , so that B’s proposer must download A to evaluate P(z) ?

Yep!

> Why should that be probabilistic vs a fixed reward?

A probabilistic reward reduces the costs of implementing the reward; you only need an occasional beacon chain transaction.

X can be any sufficiently big number, eg. perhaps 2^{13} if we want to target a reward being processed once per epoch under optimal conditions.

---

**djrtwo** (2021-04-14):

For idea-3, the idea is for the proposer to see the header and then do a req/resp to get the body?

(or is it that the proposer needs to be listening to gossip channels of the full shard contents)

Being able to make such a request requires being connected peers that are listening to that shard subnet, and also induces a round trip request *after* having received the header on the global channel. This makes the ability to get this correct much more difficult than just listening to the global header subnet (idea 1 and 2 only have that requirement).

Whereas, being on the subnet pre-supposes that proposer lookahead is sufficient to get onto the subnet (i.e. at least an epoch and not the way beacon proposers are selected today). I think this method with sufficient lookahead is preferable to the req/resp described above.

---

**vbuterin** (2021-04-15):

The proposer should just join the subnets of the other shards they will be linking to. This isn’t a large overhead because each validator is only proposing a small percentage of the time.

---

**djrtwo** (2021-04-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The proposer should just join the subnets of the other shards they will be linking to

But you do need better lookahead that beacon proposers get today. So `>= 1 epoch` like beacon committees get

---

**vbuterin** (2021-04-15):

Got it. One hybrid option would be to have a subset of probable block proposers be discoverable 1 epoch in advance, so that entire subset can join a few extra subnets. This could be done very easily by just always choosing the proposer from the first committee.

