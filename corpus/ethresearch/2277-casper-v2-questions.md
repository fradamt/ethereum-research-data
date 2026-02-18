---
source: ethresearch
topic_id: 2277
title: Casper V2 Questions
author: kladkogex
date: "2018-06-18"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/casper-v2-questions/2277
views: 1905
likes: 1
posts_count: 2
---

# Casper V2 Questions

Looking at the new draft of the  [Casper V2 spec](https://notes.ethereum.org/SCIg8AH5SA-O4C1G1LYZHQ?view)

One question I have is related to selection of block proposers.

My understanding is that for a given block several (M) block proposers are selected.

Are all block proposers equal for a given block or they have priorities (score) which is taken in account by the fork choice rule ?

If all block proposers are equal, then  the bad guys could win by proposing faster than good guys (lets say you have 16 block proposers each time, and one of them is always bad but way faster than other 15 good guys).

## Replies

**vbuterin** (2018-06-18):

All block proposers are equal. That said, clients will wait a longer time before accepting (and attesters will wait a longer time before attesting) proposals with higher skip numbers, so if everyone is online the 0-skip proposal should always “win”.

