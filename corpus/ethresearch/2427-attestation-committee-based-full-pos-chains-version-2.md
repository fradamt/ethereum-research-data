---
source: ethresearch
topic_id: 2427
title: Attestation committee based full PoS chains, version 2
author: vbuterin
date: "2018-07-03"
category: Proof-of-Stake
tags: [attestation]
url: https://ethresear.ch/t/attestation-committee-based-full-pos-chains-version-2/2427
views: 6711
likes: 4
posts_count: 9
---

# Attestation committee based full PoS chains, version 2

Suppose that you have a PoS chain, where there is some validator set V, and where blocks are subdivided into epochs of length EpochLength; you want every validator to vote once in every epoch as this is important for the consensus cycle and to minimize any gains from RNG manipulation. There is a source of random entropy in the chain; suppose that the random entropy updates once per epoch. At the start of every epoch, we randomly shuffle V and partition it into slices S_1 ... S_{EpochLength}, each of size SSize = \frac{V}{EpochLength}, and we split up activity into consecutive time slots T_1 ... T_{EpochLength}.

There are two types of messages: blocks and attestations. A block is a data structure that contains a pointer to a parent block, as well as a set of messages, and a set of signatures (“attestations”) of the parent block or another earlier block. The block must include at least \frac{SSize}{2} attestations of its parent, though it can contain more. A block must specify what slot number it is produced in; if a block is in slot i, immediate attesters of that block must come from the set S_i, and its signer must be the first member of S_i.

![image](https://ethresear.ch/uploads/default/original/3X/0/5/05e6478c738f9ec53b0a6007ee4788ed088a8f1c.svg)

Notice that a block at step i+2 can include not just attestations of the parent block created at step i+1, but also attestations of blocks earlier in history, as well as attestations of blocks outside of the same chain.

If a block is produced by the first member of S_i during timeslot i that is on the head, the other attesters are expected to co-sign this block. If a block does not get produced on the head, then the other attesters can sign a message asserting to what they consider the current head to be. Hence, there can actually be *two* ways that an attestation of a block with height i gets included in a block with height j > i+1:

1. The creator(s) of the block(s) with heights i < h < j fail to include it
2. The creator(s) of the block(s) with heights i < h < j fail to produce blocks, or produce blocks that are not on the head, in which case attesters can create attestations at height h of blocks of height i < h

Attestations of a block’s parent that come in slots later in the first slot when such an attestation could appear (ie. case (2)) can count toward the \frac{SSize}{2} attestation minimum (which is what allows the chain to progress even when <\frac{1}{2} of validators are online), but attestations of blocks other than a block’s parent do not.

Note that a signer and an attester are in symmetric positions in the block structure but not at network layer: because the signer is the sole *mandatory* attester, in general the signer signs a block immediately after making it and broadcasts it with the signature, and other attesters then sign after them. This allows the total aggregate signature of a block to be only one signature in size and require only one pairing to compute, at least in the best case where everyone agrees what they are signing.

#### Fork choice rule

The simplest fork choice rule to use is simple height counting. The ideal fork choice rule to use is [GHOST](https://pdfs.semanticscholar.org/4016/80ef12c04c247c50737b9114c169c660aab9.pdf), which works as follows:

1. Start at the genesis (or most recent finalized block)
2. Let the “current block” be the block the algorithm is looking at at the moment (ie. the genesis or most recent finalized block initially)

If the current block has zero children, then exit.
3. If the current block has only one child, set the current block to that child, and go
4. If the current block has more than one child, set the current block to the child that has more valid most-recent signatures from a validator signing on either that block or some descendant of that block
5. Repeat (2) until exit, and return the current block as the head.

For example, consider the following diagram, where A, B… M are the most recent signatures, and the blocks they are located in are the blocks those signatures are attesting to:

![image](https://ethresear.ch/uploads/default/original/3X/a/1/a1eaff9a90a13c27a6ade2d1ed30df61956e0faa.svg)

The head is the green block, because:

- A is the only child of the last finalized block
- B and C are the children of A. B has far more signatures backing it or its descendants than C.
- (D E) is the only child of B.
- F and (G H) are the children of (D E). (G H) has 5 signatures backing it or its descendants, F has 3, so (G H) wins.
- (I J) and M are the children of (G H). (I J) has 2 signatures backing it or its descendants, M has one, so (I J) wins.

GHOST preserves the property that the chain that has the most signatures supporting it is the winning chain, which is an important criterion to make reversion, censorship and other attacks maximally difficult.

## Replies

**naterush** (2018-07-06):

> The block must include at least \frac{SSize}{2} attestations of its parent, though it can contain more.

If there are less than  \frac{V}{EpochLength * 2} validators online, then the chain will be unable to make progress.

> then the other attesters can sign a message asserting to what they consider the current head to be.

Is an attester slashed for signing two different attestations during the same slot?

Also, consider the weird edge case where an attestor signs a message attesting to a current head, and then in a later epoch signs a message attesting to a “necessarily conflicting” head. Aka: in epoch i, attest to block B as head, and then in i+1 attest to the parent of B as head. GHOST makes it impossible to change one’s mind about the head like this, and so it might be worth considering punishing the attestor here also.

> Attestations of a block’s parent that come in slots later in the first slot when such an attestation could appear (ie. case (2)) can count toward the \frac{SSize}{2} attestation minimum (which is what allows the chain to progress even when  If the current block has more than one child, set the current block to the child that has more valid most-recent signatures from a validator signing on either that block or some descendant of that block

How do we know what signatures from validators are the most-recent ones, especially if signatures are aggregated (seemingly disallowing sequence numbers)?

---

**vbuterin** (2018-07-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> If there are less than \frac{V}{EpochLength * 2} validators online, then the chain will be unable to make progress.

False. The chain would just have to wait for two or more slots to gather up enough signatures.

> Is an attester slashed for signing two different attestations during the same slot?

Yes.

> Who is required to build/attest to the EpochLength−n blocks that remain in this epoch?

The initial slots in the next epoch.

So the “accounting” for epoch h would only be done at the end of epoch h + 1.

> How do we know what signatures from validators are the most-recent ones, especially if signatures are aggregated (seemingly disallowing sequence numbers)?

Use slot number as a proxy for recency.

---

**naterush** (2018-07-07):

> False. The chain would just have to wait for two or more slots to gather up enough signatures.

I was considering a case where less than \frac{V}{EpochLength * 2} validators are online total (not just for one slot) - for example, the minimum size of the attestation committee is 10 and there are 9 validators online out of the whole validator set.

> The initial slots in the next epoch. So the “accounting” for epoch h would only be done at the end of epoch h+1.

I’m a bit confused about how this works. How are the validator set slices from the next epoch known if the next epoch hasn’t started yet?

Thanks for the info ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

---

**vbuterin** (2018-07-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/naterush/48/4241_2.png) naterush:

> I was considering a case where less than \frac{V}{EpochLength * 2} validators are online total (not just for one slot) - for example, the minimum size of the attestation committee is 10 and there are 9 validators online out of the whole validator set.

Aaah, I see what you mean. Yeah, in that case the system would not be able to make progress, unless you extend the scheme so that it allows for attestation committees to add up across epochs. But I’m not too worried; ~99% of validators would need to be offline for this to become an issue.

> I’m a bit confused about how this works. How are the validator set slices from the next epoch known if the next epoch hasn’t started yet?

By “accounting” I mean “checking who voted, adding rewards, and evaluating finality”. So you would calculate the shuffling for epoch n+1 at the start of epoch n+1, but you would not do any computations related to tallying what took place in epoch n until the end of epoch n+1.

---

**naterush** (2018-07-12):

> So you would calculate the shuffling for epoch n+1 at the start of epoch n+1

This is the final thing I don’t understand. What happens if the number of blocks built by all the slices of attestors is less than the number of blocks in an epoch?

As there are only EpochLength slices generated at the start of an epoch, do the same attestor slices need to continue building blocks (in the same order) until the end of the epoch?

---

**vbuterin** (2018-07-12):

> What happens if the number of blocks built by all the slices of attestors is less than the number of blocks in an epoch?

An epoch is counted as a set of *slots*, not a set of *blocks*. This is a change from the status quo.

---

**rcconyngham** (2018-08-02):

> as well as attestations of blocks outside of the same chain.

What exactly is this for? Do they still get rewarded? Or is this so that they can get punished for signing off-head blocks?

> If the current block has more than one child, set the current block to the child that has more valid most-recent signatures from a validator signing on either that block or some descendant of that block

A question here: Do we not only count signatures that are included in the chain, but also other signatures that are currently pending inclusion in a block and attestations in other chains?

---

**vbuterin** (2018-08-02):

> What exactly is this for? Do they still get rewarded? Or is this so that they can get punished for signing off-head blocks?

For two purposes:

1. So they can get some reward (or not be penalized)
2. So the chain can be aware of when it’s justified or finalized even if these justifications do not all come from on-canonical-chain blocks

