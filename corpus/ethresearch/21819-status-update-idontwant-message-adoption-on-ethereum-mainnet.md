---
source: ethresearch
topic_id: 21819
title: "Status Update: `IDONTWANT` Message Adoption on Ethereum Mainnet"
author: yiannisbot
date: "2025-02-24"
category: Networking
tags: [p2p, scaling]
url: https://ethresear.ch/t/status-update-idontwant-message-adoption-on-ethereum-mainnet/21819
views: 365
likes: 7
posts_count: 2
---

# Status Update: `IDONTWANT` Message Adoption on Ethereum Mainnet

## Context

The `IDONTWANT` control message was adopted as part of libp2p’s Gossipsub protocol spec in May 2024 [[GH Pull Request](https://github.com/libp2p/specs/pull/548)]. The purpose of the control message is to notify mesh neighbours of a peer that it has already received a particular message and doesn’t want to have it delivered again.

The goal of having such a message primitive has been to reduce the number of duplicate messages that a node receives. Reducing the number of duplicate messages is important because, consequently, more bandwidth will become available and will, in turn, allow for more blobs to be included in a block. It has been observed through measurement studies [see [ProbeLab’s previous post](https://ethresear.ch/t/bandwidth-availability-in-ethereum-regional-differences-and-network-impacts/21138)], but also intuitively, that peers might receive a message up to `D` times. Although redundancy (in terms of message duplicates) in a decentralised P2P network is partly a feature and not a bug, it has been argued that the number of duplicates can be reduced.

This post serves as a brief update on the number of Ethereum nodes that support the `IDONTWANT` control message on the Ethereum mainnet.

## Methodology & Results

At ProbeLab, we crawl the discv5 network every 2hrs (total of 84 times per week) and produce a variety of results in the form of weekly reports. You can find the latest report at: [Week 2025-07 | ProbeLab](https://probelab.io/ethereum/discv5/2025-07/)

As part of that, we scraped the nodes we have “seen” over a random crawl and found the following:

- All client implementations have added support for the IDONTWANT control message.
- Despite that, there’s still 1879 nodes (approximately 20%-25% of the network) that doesn’t support IDONTWANT in practice.
- This percentage comes from nodes that run older versions of their respective client implementation. In particular, the following versions of each client are still present in the network (as can also be seen in this plot) and are older than the version that supports IDONTWANT.

```auto
Lighthouse: v5.0.0 to v5.2.1
Grandine: 0.4.1
Prysm: v4.1.1 to v5.1.0
erigon: caplin
lodestar: v1.16.0 to v1.27.0
teku: v24.2.0 to v24.8.0
rust-libp2p: 0.44.1
nimbus: no version given
```

- Here’s the breakdown of the number of nodes per client implementation that runs one of the above versions and hence, DO NOT support IDONTWANT:

Prysm: 1477 (50% of Prysm’s  ~3000 nodes)
- Lodestar: 176 (100% of Lodestar’s ~176 nodes)
- Lighthouse: 162 (4,3% of Lighthouse’s ~3700 nodes)
- Teku: 33 (2.9% of Teku’s ~1135 nodes)
- Erigon: 16
- rust-libp2p: 4 (4.5% of rust-libp2p’s 85 nodes)
- nimbus: 9 (1.9% of Nimbus’s 460 nodes)
- Grandine: 2

## Next Steps

ProbeLab is monitoring closely the adoption of `IDONTWANT` control messages and will re-run the Bandwidth Availability study [[link](https://ethresear.ch/t/bandwidth-availability-in-ethereum-regional-differences-and-network-impacts/21138)] it has run in Dec 2024 to quantify the performance improvement, in terms of bandwidth requirement reduction, when a larger part of the network has upgraded and supports this new control message. This study will most likely be carried just after the Pectra update, when all nodes will have been updated and will be published as a separate [ethresear.ch](http://ethresear.ch) post.

## Replies

**yiannisbot** (2025-04-09):

Here’s an update to the number of nodes that **DO NOT** support `IDONTWANT` messages on the Ethereum mainnet as of 2025-04-02. The previous study above was carried out on 2025-02-24.

- Prysm: 952

~32% of Prysm’s ~3000 nodes remaining
- ~18% improvement compared to 2025-02-24, i.e., 18% of Prysm’s nodes have upgraded since end of Feb.

Lodestar: `145`

- 82% of Lodestar’s ~176 nodes remaining
- 82% improvement compared to 2025-02-24, when no Lodestar nodes were upgraded to a release with support for IDONTWANT.

Lighthouse: `84`

- 3.1% of Lighthouse’s ~3700 nodes remaining
- 1.3% improvement compared to 2025-02-24

Teku: `29`

- 2.5% of Teku’s 1135 nodes remaining
- 0.4% improvement compared to 2025-02-24

Erigon: `40`

- Weirdly, there is an increase in the number of Erigon nodes that do not support IDONTWANT

rust-libp2p: `4`

- No change compared to 2025-02-24

nimbus: `5`

- 1% of Nimbus’s 460 nodes
- 0.9% improvement compared to 2025-02-24

Grandine: -

- No Grandine nodes found to not support IDONTWANT messages

## TL;DR

- There hasn’t been a massive shift to newer releases and hence only 620 new nodes have added support for the IDONTWANT message between late Feb 2025 and early April 2025.
- Out of the most popular client implementations, Lighthouse and Teku are the leading forces with more than 95% of their nodes on Ethereum mainnet having support for IDONTWANT messages.
- Prysm is the biggest contributor to the remaining 1259 nodes that don’t have support for IDONTWANT with 952 nodes not on the latest release.

---

---

You can find latest metrics on Ethereum mainnet at: https://probelab.io

- Weekly Network Health report for Week 14, 2025 at: Week 2025-14 | ProbeLab
- Block Arrival Times for Week 14, 2025 at: Week 2025-14 | ProbeLab
- Daily metrics for:

Node Bandwidth Usage at: Week 2025-15 day 02 | ProbeLab
- Number of control RPCs: Week 2025-15 day 02 | ProbeLab
- Number of Duplicates at: Week 2025-15 day 02 | ProbeLab

