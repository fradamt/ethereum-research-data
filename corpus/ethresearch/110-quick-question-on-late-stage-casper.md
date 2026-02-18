---
source: ethresearch
topic_id: 110
title: Quick Question on late-stage Casper
author: drcode
date: "2017-10-01"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/quick-question-on-late-stage-casper/110
views: 1388
likes: 1
posts_count: 5
---

# Quick Question on late-stage Casper

Hi, I’m trying to find some documentation on who gets to create the blocks/checkpoints in late-stage Casper: In early-stage Casper, blocks/checkpoints are simply determined via the underlying POW system.

Can someone point me to documentation that describes where blocks originate from in late-stage Casper? The obvious mechanism would be to simply select a random validator for the task to create new blocks (and then use the Casper voting mechanism to work around situations where this validator performs their task incorrectly) but is there a document that confirms this?

Hopefully these sorts of questions are appropriate for this forum- Thanks!

## Replies

**vbuterin_old** (2017-10-02):

This is not yet decided. There are two alternatives that I’m aware of:

1. Use Iddo Bentov’s “everyone can create blocks” proof of stake
2. Turn votes themseves into blocks, so there would be some mechanism for deciding who can create a block on top of a given head at a given time, and every block is simultaneously a block and a vote to try to justify/finalize a checkpoint.

---

**drcode** (2017-10-02):

Thanks- That offers helpful context.

---

**Lars** (2017-10-03):

Do you have a reference to Iddo Bentov’s “Everyone can create blocks” algorithm? It would be interesting to study.

---

**vbuterin_old** (2017-10-03):

I was thinking of this: https://arxiv.org/abs/1406.5694

