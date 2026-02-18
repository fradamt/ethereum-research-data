---
source: ethresearch
topic_id: 9852
title: "Data Availability Question: Why would a node accept blocks with invalid bodies?"
author: chrixp
date: "2021-06-15"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/data-availability-question-why-would-a-node-accept-blocks-with-invalid-bodies/9852
views: 1262
likes: 0
posts_count: 2
---

# Data Availability Question: Why would a node accept blocks with invalid bodies?

From multiple sources that I’ve read, the data availability problem is when a malicious node publishes a block with an invalid body and therefore node can not verify if a block is valid or not. I’m a bit confused because why would a node accept blocks with invalid bodies in the first place?

## Replies

**MicahZoltu** (2021-06-17):

Not an invalid body, but a block *without* a body.  Ethereum clients currently do not accept any such block, which is why Ethereum doesn’t have a data availability problem.  The data availability problem comes up when people design systems that *don* require every node have all of the data.

