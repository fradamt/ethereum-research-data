---
source: ethresearch
topic_id: 1152
title: Exponential epoch backoff
author: vbuterin
date: "2018-02-19"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/exponential-epoch-backoff/1152
views: 2125
likes: 1
posts_count: 4
---

# Exponential epoch backoff

Edit 2018.03.03: figured out the best way to do slashing conditions.

I propose a rule change to the Casper FFG contract: instead of an epoch’s length being a fixed 50 blocks, 50 is merely the *base* epoch length, and an epoch’s actual length is calculated at epoch start time according to the following rule:

- If the last epoch finalized a checkpoint, the epoch length is 50 blocks.
- Otherwise, the epoch length is double the length of the previous epoch.

This has the advantage that it allows Casper to keep finalizing checkpoints even under highly adverse conditions, where latency is extremely high, as eventually the epoch length will catch up to the latency, allowing a checkpoint to be finalized.

Instead of the leak penalty being based on LFE ^ 2, the penalty will now be 4 ^ LFE, ensuring that it continues to be quadratic in the important variable, *time* since finality.

We change slashing conditions as follows. We continue to define epoch number as `floor(epoch_start_block_number / 50)`; when the epoch length is longer than 50, we simply skip epoch numbers. Every vote specifies not just the current epoch, but also the next epoch minus one (eg. if the current epoch is 108 and the next is expected to be 112, then the vote specifies (108, 111)). We refer to these two values as *target start* (ts) and *target end* (te).

We leave the NO_SURROUND condition unmodified, but we replace the NO_DBL_VOTE condition with NO_INTERSECT:

*A validator cannot sign two votes whose target ranges intersect; that is, a validator cannot sign V1 and V2 where `V1.te >= V2.te >= V1.ts >= V2.ts`*.

The proof of safety is the same: if there are two finalized checkpoints on separate chains A and B, with chain B having a higher target end, then we can keep walking back through that chain and it is not possible to avoid either intersecting or surrounding at least one of the target ranges of A.

## Replies

**tim** (2018-02-21):

A little out of the loop but here we go!

With regards to the epoc’s length variable, what are you optimizing the system for: {latency, decreased network congestion, security}?

Also how did you arrive at 50 blocks? Did you reverse calculate a desired tps upper bound and then deduce the 50 block size on a variety of factors like network size now/future and arrive at a lower bound?

Some other thoughts that came through the brain:

How will a parallel evm or simd play into this mechanic of the system.

Maybe modeling the epoch’s length on successful wireless ad hoc networking consensus protocols with reguard to the monotonicity attribute.

![:face_with_monocle:](https://ethresear.ch/images/emoji/facebook_messenger/face_with_monocle.png?v=9)

---

**vbuterin** (2018-02-22):

> what are you optimizing the system for: {latency, decreased network congestion, security}?

Overhead of 1-2 tx/sec seems like the maximum reasonably acceptable. 1000-2000 nodes seems like the minimum reasonably acceptable for decentralization. From here, the basic finality inequality (see [Parametrizing Casper: the decentralization/finality time/overhead tradeoff | by Vitalik Buterin | Medium](https://medium.com/@VitalikButerin/parametrizing-casper-the-decentralization-finality-time-overhead-tradeoff-3f2011672735)) says that epoch time has to be ~1000 seconds.

---

**kladkogex** (2018-02-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This has the advantage that it allows Casper to keep finalizing checkpoints even under highly adverse conditions, where latency is extremely high, as eventually the epoch length will catch up to the latency, allowing a checkpoint to be finalized.

An alternative would be to keep the epoch length fixed as it is now, but start subsidizing (co-paying)  validator gas costs under adverse conditions - making sure that validator transactions have higher priority than all other transactions.

If network conditions a really bad (say you have a split of Europe and US) then arguably you do not want to finalize any checkpoints until the split is resolved.  So not finalizing may actually be a good thing under some conditions.  You can subsidize transactions if  the network conditions are getting bad, and if they are really bad, you can accept the fact that things are not finalized until the conditions improve …

