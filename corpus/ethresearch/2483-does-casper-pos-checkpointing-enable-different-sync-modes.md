---
source: ethresearch
topic_id: 2483
title: Does Casper/PoS checkpointing enable different sync modes?
author: fubuloubu
date: "2018-07-07"
category: Meta-innovation
tags: []
url: https://ethresear.ch/t/does-casper-pos-checkpointing-enable-different-sync-modes/2483
views: 1616
likes: 6
posts_count: 6
---

# Does Casper/PoS checkpointing enable different sync modes?

Not that I have any real experience with client internals, but my basic understanding leads me sometimes to fantasize about the client layer.

Anyways, my random thought is that if checkpoints were a thing, you could start at some recently agreed upon checkpoint (validator stake >2/3 pool), ask to download the state from others at that checkpoint (there is a proof of correctness), and then start downloading blocks matching in reverse order until either 1) you reach the genesis block or 2) you are up to date on what you care about (new accounts don’t care about much except the contracts they want to interact with eventually).

You could announce a syncing state and disable transactions to contract accounts you haven’t fully back-validated yet (i.e. validated the creation transaction) if you wanted to be extra cautious.

I think checkpoints enable some cool assumptions and in my inexperience with client implemetations I wanted to ask this question to see if anyone thought of the pros and cons with this approach.

## Replies

**vbuterin** (2018-07-08):

The holy grail is an ultrafast syncing process, that works like this:

- Start from the current validator set you already know about
- Ask the network for what is the highest-epoch block that that validator set finalized
- Ask the network for the signatures proving that it was finalized. Verify them
- Download the new validator set from that state root. Repeat the above steps until you’re at the truly most recent finalized checkpoint
- Apply the fork choice from there

This would require one round of network interaction per validator set change, and if you adopt slowly changing validator sets as we do in the latest Casper spec then individual nodes can trade off between security and syncing speed (eg. if the default settings let you sync with 100 rounds with 30% fault tolerance, you can do it in 50 rounds with 27% FT, or in 20 rounds with 18% FT).

You could even batch the rounds together, basically asking a client for a single proof of “dynasty A finalized dynasty B, B finalized C, C finalized … finalized Z” and then verifying it all at once, and then after that download the latest state.

After you do that, I would recommend listening in the network for fraud or data unavailability claims about any of the historical data you skipped through and checking as much of the claims as you can.

---

**fubuloubu** (2018-07-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> After you do that, I would recommend listening in the network for fraud or data unavailability claims about any of the historical data you skipped through and checking as much of the claims as you can.

Hmm, maybe another setting could be applied here for randomly auditing history e.g. “check 2% of historical data”

---

**PARKSWAP** (2018-07-08):

[@vbuterin](/u/vbuterin): I like a lot of what you have been pondering…

As they say there are a 1000 ways of skinning a cat.

You may find it of interest to discuss around the O-zone project… (see emails to noreply@b****[in.com](http://in.com))

J.

---

**MaxC** (2018-07-08):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/p/3d9bf3/48.png) PARKSWAP:

> O-zone

There is also Coda from O(1) labs who are developing recursive snarks, although I had been thinking about something similar to Vitalik’s solution.

---

**fubuloubu** (2018-07-08):

Literally just reading about this now! Truly groundbreaking concept. Big if true.

