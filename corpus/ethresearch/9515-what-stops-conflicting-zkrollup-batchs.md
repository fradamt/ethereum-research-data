---
source: ethresearch
topic_id: 9515
title: What stops conflicting zkrollup batchs?
author: zes
date: "2021-05-15"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/what-stops-conflicting-zkrollup-batchs/9515
views: 1186
likes: 1
posts_count: 2
---

# What stops conflicting zkrollup batchs?

For zkroolups, there’s someone who submits the batches to the mainnet. What prevents it from submitting conflicting information?

For example, A has 10 eth in the zkrollup smart contract. A signs two transactions A → B 10 eth, A → C 10 eth, what if two zkrollup batches with these conflicting transactions separately are sent out simultaneously?

## Replies

**stri8ed** (2021-05-17):

Only one of the batches will be accepted. After that, the other batch will fail, since the state root has changed, thereby invalidating the proof.

