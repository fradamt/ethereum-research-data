---
source: magicians
topic_id: 3175
title: "Red Queen's: New Sync Proposal"
author: yperbasis
date: "2019-04-23"
category: Working Groups > Ethereum 1.x Ring
tags: [fast-sync]
url: https://ethereum-magicians.org/t/red-queens-new-sync-proposal/3175
views: 1714
likes: 5
posts_count: 4
---

# Red Queen's: New Sync Proposal

As part of Ethereum 1x efforts, we want to tackle the issue of the growing blockchain state. Large state size leads to long sync times. On top of that, geth’s fast sync is not that fast and takes a few hours. Parity’s warp sync is faster, but is not supported in geth. We propose a new sync protocol and an algorithm, which we believe can perform snapshot sync in less than an hour. The idea is somewhat similar to Warp Sync and especially to Leaf Sync (under development in geth). Moreover, the new protocol caters for clients with a different storage structure than the canonical Patricia trie (e.g. turbo-geth).

The new protocol and algorithm are described in a [paper](https://github.com/yperbasis/silkworm/blob/master/doc/sync_protocol_v1.pdf). See also my [presentation](https://youtu.be/Au1Qll-86v0?t=24843) at Ethereum Core Devs Eth1x/Istanbul Planning Meeting in Berlin.

This is the first version; comments, suggestions, critique are most welcome.

## Replies

**yperbasis** (2019-04-23):

The new protocol is related to [Forming a Ring: ETH v64 Wire Protocol Ring](https://ethereum-magicians.org/t/forming-a-ring-eth-v64-wire-protocol-ring/2857).

---

**yperbasis** (2019-04-25):

See also a [gitter discussion](https://gitter.im/fast-warp-collaborator/community) about new sync protocols.

---

**yperbasis** (2019-06-10):

An update: we’re going to use “Red Queen” for a sync algorithm (one out of a few possible) and “Firehose” for the new sync protocol. A new version 0.3 of Firehose is available at https://github.com/ledgerwatch/turbo-geth/blob/red-queen/docs/firehose.MD.

