---
source: ethresearch
topic_id: 1989
title: Extending minimal sharding with cross-links
author: vbuterin
date: "2018-05-12"
category: Sharding
tags: []
url: https://ethresear.ch/t/extending-minimal-sharding-with-cross-links/1989
views: 3762
likes: 6
posts_count: 8
---

# Extending minimal sharding with cross-links

Required reading: [A minimal sharding protocol that may be worthwhile as a development target now](https://ethresear.ch/t/a-minimal-sharding-protocol-that-may-be-worthwhile-as-a-development-target-now/1650)

We can extend the minimal sharding spec to reduce in-shard block times, and particularly make in-shard block times not dependent on a majority being online, as follows. Instead of the `chunks_root` in the committee vote being the root hash of a single chunk, it now is a hash of the header of a block in the chain of that particular shard. A proof-of-custody mechanism is added to ensure that:

1. The linked header, and all headers between that header and the header previously linked for that shard, must be available.
2. As a corollary of (1), the linked header must be a descendant of the header previously committed to for that shard (note: this follows from the cross-link fork choice rule described earlier)
3. For every header in that shard between the current and previous header (including the current, not including the previous), the collation body must be available.

The committee that can create a cross-link is chosen based on main-chain randomness based on exponential backoff: suppose that the last main-chain block when a collation for that shard was linked is T. Let R[i] be randomness from block i. For any block S > T, find the most recent block B such that `B.number - T` is an exact power of 2 (possibly with some minimum, eg. 128). Use R[B] as the source for a valid committee.

This accomplishes two goals:

- It ensures that a committee does not have infinite time to find each other and collude to make an invalid block, as eventually any committee will get replaced by another one.
- It gives a newly assigned committee ample time to download and verify the linearly growing amount of data that they are assigned to attest to (specifically, the committee need only be able to verify data twice as fast as the chain is growing).

If more than 33% of nodes are offline, then cross-links will not happen, but the chain on each shard will be able to keep growing.

One possible addendum may be to not allow making a cross-link for a shard until the previous cross-link is finalized; this would allow the notarization committees to not have to worry about complicated dependent fork choice rules, as the “root” of the shard chains from which shard fork choice is evaluated from would be clear since the previous cross-link would already have been finalized.

## Replies

**jamesray1** (2018-05-14):

Remember to put the category as sharding, that’s how I see sharding posts with notifications for posts with that category, unless someone gives a link to the post that doesn’t have a sharding category, as happened here.

PoC:

- Enforcing windback (validity and availability), and a proof of custody,
- Finality and Windback - Proof of Custody Revisited
- Extending skin-in-the-game of notarization with proofs of custody

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It ensures that a collation does not have infinite time to find each other and collude to make an invalid block… It gives a newly assigned collation ample time to download and verify

This doesn’t make sense, a collation is not an entity. Do you mean a proposer collator (maybe we should call them prollators as a contraction) and an attestor (formerly a notary, now the role of notary is done by notarization committees), respectively?

---

**vbuterin** (2018-05-15):

Sorry! Fixed the mistakes. s/collation/committee/g in that sentence.

---

**NicLin** (2018-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Use R[B] as the source for a valid collation.

Seems this one should be ‘committee’ too?

---

**NicLin** (2018-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It ensures that a committee does not have infinite time to find each other and collude to make an invalid block, as eventually any collation will get replaced by another one.

Can you elaborate more on how this goal is achieved? and what does it mean by ‘any collation will get replaced by another one’?

---

**vbuterin** (2018-05-19):

> Can you elaborate more on how this goal is achieved? and what does it mean by ‘any collation will get replaced by another one’?

Every slot [T+2^k, T+2^{k+1}] is mapped to a distinct committee. Compare this to two possible alternate policies:

1. Every slot [T + k, T + k + 1] is mapped to a distinct committee
2. Once a cross-link is made, the committee for the next cross-link is selected, and does not change until that committee does come together to make the cross-link.

(2) has the weakness that the members of a committee have as much time as they want to discover each other and collude to possibly sign something false. (1) has the weakness that if, for example due to some long-lasting network failure or attack, many committees fail to sign in time, then the shard chain history will keep growing, and so the network could permanently reach a state where the amount of historical backlog a newly selected committee has to verify is larger than the amount that it could conceivably verify within a k-length period.

The proposal given resolves both issues, because (i) every committee is eventually replaced, and outside of exceptional scenarios it’s replaced fairly quickly, so they don’t have excessively long time to collude, and (ii) the amount of time that a committee has to verify history is half the amount of time that it took to create that history in the first place, so as long as regular history processing consumes less than 50% of CPU power it will always be possible to verify history in time.

---

**NicLin** (2018-05-20):

Thanks! It’s much more clear to me now.

Also this one:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This accomplishes two goals:
>
>
> It ensures that a committee does not have infinite time to find each other and collude to make an invalid block, as eventually any collation will get replaced by another one.

---

**tim** (2018-05-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> suppose that the last main-chain block when a collation for that shard was linked is T. Let R[i] be randomness from block i. For any block S > T, find the most recent block B such that B.number - T is an exact power of 2 (possibly with some minimum, eg. 128).

ahh, this is my kind of sentence. so concise ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

