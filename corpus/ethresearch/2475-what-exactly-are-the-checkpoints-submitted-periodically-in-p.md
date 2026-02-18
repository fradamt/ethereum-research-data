---
source: ethresearch
topic_id: 2475
title: What exactly are the "checkpoints" submitted periodically in Plasma?
author: dh1234
date: "2018-07-07"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/what-exactly-are-the-checkpoints-submitted-periodically-in-plasma/2475
views: 1252
likes: 1
posts_count: 3
---

# What exactly are the "checkpoints" submitted periodically in Plasma?

Is it blocks? block headers? merkle tree? merkle tree root?

are checkpoints synonymous with “commitments”?

## Replies

**vbuterin** (2018-07-07):

A Merkle tree root of the transactions in a block.

> are checkpoints synonymous with “commitments”?

Probably.

---

**kfichter** (2018-07-12):

Depends on what you mean by “checkpoint.”

I would differentiate block commitments and checkpoints. I define block commitments as periodic submissions of Plasma block roots (collections of transactions). However, I define checkpoints as periodic (but less frequent) submissions of Plasma state roots (collections of state). The key difference here is that block commitments attest to a set of transactions while checkpoints attest to the current state of the network. In that sense, users can use checkpoints to throw out the series of transactions that would be required to determine the current state of the network.

