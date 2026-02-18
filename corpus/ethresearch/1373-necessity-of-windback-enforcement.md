---
source: ethresearch
topic_id: 1373
title: Necessity of windback enforcement
author: nate
date: "2018-03-12"
category: Sharding
tags: []
url: https://ethresear.ch/t/necessity-of-windback-enforcement/1373
views: 1838
likes: 3
posts_count: 4
---

# Necessity of windback enforcement

Prerequisites: [Enforcing windback (validity and availability), and a proof of custody](https://ethresear.ch/t/enforcing-windback-validity-and-availability-and-a-proof-of-custody/949),

[Proposer withholding and collation availability traps](https://ethresear.ch/t/proposer-withholding-and-collation-availability-traps/1294/15)

---

Currently, when a collator is given the ability to make a collation on a shard, they are supposed to download and verify the availability of the most recent collation bodies (called windback). Let’s say that `windback_periods = 25`.

Assume, for now, there are no schemes in use (like those linked above) to enforce windback. In this case, it does not seem like windback is a stable equilibrium.

Before a collator makes a new collation C, they have an incentive to windback as they risk having their collation orphaned otherwise. Essentially, future collators will choose to not build on C if they find collations in C’s history are unavailable while winding back themselves, causing the original collator to lose out on their collation subsidy.

However, collators also have an incentive to skip windback if they can, as it imposes some (small) cost on them.

Let’s say that`windback_periods = 25`. Each collator can reason: “the collator in front of me will check 25 collations back, but as this includes my new collation, this only overlaps with 24 of the collations I’ll check.” Thus, each collator can get away with `windback_periods = 24`, as they can be sure the next validators will not check as far back as the 25th. This logic can continue from 24 -> 23, 23 -> 22… all the way down to `windback_periods = 0`.

Essentially, it seems to be a rationalizable strategy for validators to never windback at all. (Obviously, this ignores the fact that the software will, by default, windback.)

For one, this points to the necessity of actually enforcing windback periods, like in the linked post or some other method.

Furthermore, I wonder if there’s some way to make the equilibrium-without-enforcement more stable by changing `windback_periods` to some mixed strategy, where validators windback some random-ish number of collations, instead of a constant. That being said, I don’t know enough GT to work through a) if this is possible, or b) what it would look like if so - so any/all thoughts appreciated ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=9)

## Replies

**vbuterin** (2018-03-12):

This is fundamentally very similar (identical?) to the validator’s dilemma issue: https://eprint.iacr.org/2015/702.pdf

> Furthermore, I wonder if there’s some way to make the equilibrium-without-enforcement more stable by changing windback_periods to some mixed strategy, where validators windback some random-ish number of collations, instead of a constant.

It’s worth noting that the existing software implementation already kinda does this; it does NOT try to wind back exactly 25 collations and then stops, rather it spends the entire 5 minutes allocated trying to wind back as far as it can, and this will naturally lead to wild variance in actual windback depths in practice.

Though I do think that having a specified minimum windback that gets enforced is useful as a second bulwark against collators checking too little.

---

**drstone** (2018-03-13):

What if at time t, there is some dynamically updated (maybe fixed) windback_period w_t. The proposer of the new block of height n+1 must windback w_t collation headers, computes f(x_{n-w_t},\dots,x_{n}), where each x_i is a header hash and f is some hash function, and embeds it into the new block. It would be required to recompute this value to ensure validity, basically windbacks are embedded over time.

---

**nate** (2018-03-14):

The issue with this approach is that validators only have to download collation headers, rather than full collations, to compute this. As collation headers are included in the root chain anyways, they don’t even have to download anything new.

A possible similar approach is that somehow making validators include a hash that relies on all the data in all of the most recent previous blocks, but the issue with this is that checking this in a smart contract is quite challenging.

