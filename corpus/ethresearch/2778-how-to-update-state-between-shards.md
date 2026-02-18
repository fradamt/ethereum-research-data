---
source: ethresearch
topic_id: 2778
title: How to update state between shards
author: spartucus
date: "2018-08-02"
category: Sharding
tags: [cross-shard, state-execution-separation]
url: https://ethresear.ch/t/how-to-update-state-between-shards/2778
views: 2784
likes: 0
posts_count: 8
---

# How to update state between shards

Hi, i’m new with ethereum sharding, I’m confused with state update during shards, please correct me if i’m wrong and any advice would be appreciated.

According to [Ethereum Sharding General Introduction](https://docs.google.com/presentation/d/1mdmmgQlRFUvznq1jdmRwkwEyQB0YON5yAg4ArxtanE4/edit#slide=id.g359cce9869_12_128):

> Validators submit collation header to the root chain

Does this mean root chain only has collation header? if so, what if A spend 1 eth (let’s say A only has 1 eth) on shard M and spend same 1 eth on shard N? (double spend). Does shard N knows A’s state?

## Replies

**vbuterin** (2018-08-02):

Each unit of ETH (and each object more generally) only exists on one shard at any particular time.

---

**spartucus** (2018-08-03):

Hi buterin, thanks for replying.

Does this mean this is more like a side-chain?

Object only exists on one chain, if he wants to switch to other chain, it must settlement account on current chain, and then register to other chain.

---

**vbuterin** (2018-08-03):

For an object to be transferred to another chain, you need a cross-shard transaction. This should take a few minutes to process.

---

**spartucus** (2018-08-03):

Any documents or resources about cross-shard transaction?

---

**spartucus** (2018-08-03):

I think i found related docs.

[Merge blocks and synchronous cross-shard state execution](https://ethresear.ch/t/merge-blocks-and-synchronous-cross-shard-state-execution/1240)

---

**hwwhww** (2018-08-03):

Also [Sharding FAQ](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#how-can-we-facilitate-cross-shard-communication) and [several approaches/discussions posts with “cross-shard” tag](https://ethresear.ch/tags/cross-shard).

---

**spartucus** (2018-08-03):

Thanks hwwang.![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=9)

