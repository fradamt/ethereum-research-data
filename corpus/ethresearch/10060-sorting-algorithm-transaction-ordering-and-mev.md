---
source: ethresearch
topic_id: 10060
title: Sorting Algorithm, Transaction ordering and MEV
author: PatrickDehkordi
date: "2021-07-10"
category: Economics
tags: []
url: https://ethresear.ch/t/sorting-algorithm-transaction-ordering-and-mev/10060
views: 1585
likes: 4
posts_count: 6
---

# Sorting Algorithm, Transaction ordering and MEV

Is it possible to implement a well defined sorting mechanism into the protocol to eliminate MEV? Or is this impossible because there is no consensus in the mempool?

## Replies

**pmcgoohan** (2021-07-10):

The latter- it’s impossible because there is no consensus in the mempool. But there could be.

  [![image](https://ethresear.ch/uploads/default/original/2X/7/78d6ae3c959923eadbcf60b3197f7ea6aeacaaac.jpeg)](https://www.youtube.com/watch?v=zf2l3veT9EI)

---

**aelowsson** (2021-07-11):

Would you mind explaining why it is not possible to require nodes to add the time (e.g., X.X ms after block X) that they first saw a transaction, and then median filter (or using any other appropriate order statistics) across say the first 30 recorded time stamps. I understand there are nuances on how to reconcile time stamps etc. but it seems it could be sorted out…so I wonder what would be the attack vector? Would love to read up more before I ask these sort of questions hehe but I am quite busy. This just seemed like the obvious “naive solution”.

---

**pmcgoohan** (2021-07-11):

Every node relaying their own and everyone else’s timestamp for every tx bloats the network.

Plus an attacking node just censors them all and only forwards their own made up one.

In short, it’s trusted.

---

**pmcgoohan** (2021-07-11):

More easily you have no mechanism to enforce miners to respect the timestamps. They can just add their own 30 timestamps from their own made up nodes when they write the block

---

**aelowsson** (2021-07-11):

Thanks. I was trying to understand if there is a way for nodes to show that a miner is rearranging the transactions without thinking about a way to enforce miners not to do that. Perhaps some chain of timestamps leading back to the sender of the transaction, thresholded at 30 timestamps to not make too much bloat. Anyway hope you can find and implement a solution, it is an important problem!

