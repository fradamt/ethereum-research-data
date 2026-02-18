---
source: ethresearch
topic_id: 10521
title: Are Rollups not worth implementing as ETH 2.0 will soon be released?
author: zhew2013
date: "2021-09-07"
category: Sharding
tags: []
url: https://ethresear.ch/t/are-rollups-not-worth-implementing-as-eth-2-0-will-soon-be-released/10521
views: 2207
likes: 9
posts_count: 3
---

# Are Rollups not worth implementing as ETH 2.0 will soon be released?

It is great to see there are some projects migrating to rollups for lower gas fee and faster transaction time. I am pondering on starting a service for new NTF projects to issue and trade NFTs on my rollup (inspired by [@vbuterin](/u/vbuterin) ’s post yesterday). But would the launch of ETH 2.0 pretty much make my project worthless? If the volume of transactions aren’t much on rollups, users might just be trade on ETH 2.0 with low fee.

Would really appreciate your guys’ input!

## Replies

**MicahZoltu** (2021-09-07):

There is no ETH2.  There is the upcoming switch to Proof of Stake (The Merge), which will change the consensus engine but won’t likely have any effect on blockchain throughput.  Sometime after that there is State Expiry, The Portal Network, Sharding, and Regenesis which each may allow for some amount of increase in gas throughput but the exact amounts are unknown.

Layer 2 is definitely the right way to scale, I don’t recommend waiting for layer 1 solutions to drive gas prices down.  My suspicion is that long term Ethereum will be used as a global settlement layer for layer 2 solutions (probably zkRollup type solutions) and very little day-to-day stuff will happen on L1.

---

**zhew2013** (2021-09-07):

Thanks for the reply. If blockchain is really going to impact this world (like if we have decentralized Twitter, etc.), then yeah I think even in the long run L2 is needed. L1 might just serve as a proof of something happened.

Minimum data will be store on L1. Computation will also happen mostly off L1. Correct?

