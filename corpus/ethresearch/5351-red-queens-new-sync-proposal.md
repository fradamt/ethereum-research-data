---
source: ethresearch
topic_id: 5351
title: "Red Queen's: New Sync Proposal"
author: yperbasis
date: "2019-04-23"
category: Execution Layer Research
tags: [chain-sync]
url: https://ethresear.ch/t/red-queens-new-sync-proposal/5351
views: 2719
likes: 6
posts_count: 3
---

# Red Queen's: New Sync Proposal

As part of Ethereum 1x efforts, we want to tackle the issue of the growing blockchain state. Large state size leads to long sync times. On top of that, geth’s fast sync is not that fast and takes a few hours. Parity’s warp sync is faster, but is not supported in geth. We propose a new sync protocol and an algorithm, which we believe can perform snapshot sync in less than an hour. The idea is somewhat similar to Warp Sync and especially to Leaf Sync (under development in geth). Moreover, the new protocol caters for clients with a different storage structure than the canonical Patricia trie (e.g. turbo-geth).

The new protocol and algorithm are described in a [paper](https://github.com/yperbasis/silkworm/blob/master/doc/sync_protocol_v1.pdf). See also my [presentation](https://youtu.be/Au1Qll-86v0?t=24843) at Ethereum Core Devs Eth1x/Istanbul Planning Meeting in Berlin.

This is the first version; comments, suggestions, critique are most welcome.

## Replies

**timbeiko** (2019-12-09):

[@yperbasis](/u/yperbasis) thanks for sharing! I assume this is not compatible with the Beam Sync proposal that Trinity has been working on?

---

**lithp** (2019-12-11):

They’re compatible ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

“Beam Sync” is a slight misnomer, it’s not a sync protocol, and instead it’s more of a sync strategy. Currently, Beam Sync works by using the `GetNodeData` requests that eth already supports, but Beam Sync could just as easily use Red Queen’s `GetStateNodes` request. In fact, it would run much faster if it could use `GetStateNodes`, because a single call of `GetStateNodes` is enough to fetch an account, something which takes around 7 round-trips using `GetNodeData`.

Though, this is just my impression of the situation, [@carver](/u/carver) might not agree with all of it.

