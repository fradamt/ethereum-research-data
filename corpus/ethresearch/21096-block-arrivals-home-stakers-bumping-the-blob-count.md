---
source: ethresearch
topic_id: 21096
title: Block Arrivals, Home Stakers & Bumping the blob count
author: samcm
date: "2024-11-27"
category: Sharding
tags: [data-availability, scaling]
url: https://ethresear.ch/t/block-arrivals-home-stakers-bumping-the-blob-count/21096
views: 1182
likes: 34
posts_count: 6
---

# Block Arrivals, Home Stakers & Bumping the blob count

# Block Arrivals, Home Stakers & Bumping the blob count

> Thanks to all the community members that are selflessly sharing their data that allowed this analysis to be possible, to MigaLabs for their validator entity data and to ProbeLab for an early version of their Mainnet bandwidth report.
>
>
> Special thanks to Parithosh, Toni, Mikel, Andrew, and Matty for their feedback and help throughout this analysis.

## TL;DR

### Summary

- Timing games have historically made it hard to predict a safe blob count bump
- ethPandaOps recently started receiving block arrival timing data from the community
- Analysis of the most bandwidth sensitive scenario shows a healthy block & blobs arrival time

### Outcomes

- When naively extrapolating this data and combining with EIP7623, this analysis supports increasing the blob count in EIP7691 to either 4/8 or 6/9.

This is only one data point, but it leads to a more optimistic outlook on a potential blob count bump than previous analysis.

## Intro

The [ethPandaOps team has recently started receiving data from members of the community](https://ethpandaops.io/posts/contribute-to-xatu-data/). Home stakers are one of the Ethereum network’s most valuable assets, and this scheme is starting to shine a light on how they see the network. A [sidecar binary](https://ethpandaops.io/data/xatu/#get-started) is run alongside a beacon node, and records the events happening on the node via the beacon API event stream. These events are sent to the ethPandaOps team, who then publishes the data (with a small delay & some data scrubbing).

For more info:

- Data collection
- Accessing the data

The team has been collecting community data for around 6 weeks, and we now have enough data to make some interesting observations that were previously not possible.

## Background

With the arrival of [EIP4844](https://eips.ethereum.org/EIPS/eip-4844), a block is only considered valid once the block & the blobs referenced in the block are received by a node. This block/blob bundle has until 4s in the slot to be received by the majority of the network otherwise it runs the risk of being re-orged.

[Sophisticated operators (and now MEV-Relays) play block proposal timing games](https://timing.pics/). These operators submit their blocks as late as possible to maximise their profit while minimizing their risk of being re-orged. These timing games have historically obfuscated block arrival timing data.

[Unreleased, upcoming research from ProbeLab](https://probelab.io/) indicates that the 50th percentile of non-cloud nodes on the network have 20Mbps of upload bandwidth.

[Blob usage on Mainnet continues to grow.](https://dune.com/queries/3757544/6319515)

## Problem statement

Ethereum’s decentralization is paramount to it’s success. [EIP7691](https://eips.ethereum.org/EIPS/eip-7691) aims to increase the blob count, and runs the risk of unintentionally excluding some node operators from it’s set if the parameters are too high.

We need to:

- Ensure that a blob count increase is safe for home stakers, as this group of actors is the “worst case” for a blob count increase as they have the lowest available bandwidth.
- Ensure that the network has enough data throughput to support Layer 2 growth.

Given the existing landscape, we can make some assumptions with regards to a potential blob count increase:

**Least at risk:**

Counterintuitively, if you looked at block arrival data, operators playing timing games would appear to be the most at risk of being impacted by a blob count increase. Being reorged out for proposing late is bad for business, and we can assume they’ll adjust their block proposal timings accordingly. **A blob count increase is unlikely to be problematic here.**

**Most at risk:**

A solo staker building a block locally (no mev-relay) and being attested to by other home stakers. In this scenario:

- The proposer:

needs to publish their block and all blobs to the network. This node needs to publish the block (~100KB), and then all of the blobs (128KB each) to all of its mesh peers as fast as possible.

when building blocks locally, the proposer does not have the help of the MEV Relay gossiping the block/blobs bundle to its own peers.

The attesters:

- need to download the block/blobs bundle from the p2p network before 4s in to the slot.

**This analysis will ask the following questions:**

- Question 1: How is 3/6 performing on Mainnet?
- Question 2: Does arrival time scale with block/blob bundle size?
- Question 3: How much more can we support on Mainnet today?

**We’ll answer these questions from the perspective of a home staker as this is our most at-risk group of operators.**

## Analysis

```auto
Start: 2024-10-04T22:00:00Z
End: 2024-11-25T02:00:00Z
Blocks: 366,384
Arrival events: 75,945,392
Countries: 9 (Australia, Bulgaria, Czechia, Germany, Italy, Spain, The Netherlands, United Kingdom, United States)
```

Check out the juypter notebook [here](https://github.com/ethpandaops/xatu-data/blob/6ff49435d3e2bd078155ad06040d584e89ea3289/analysis/mainnet/blob-bump-prediction/prediction.ipynb).

The timing data was captured by Xatu Sentry, a sidecar binary that runs alongside a beacon node and records many events via the beacon API event stream. These events can be considered *worst case* for block arrival times as there is additional processing time and network overhead for the event to be recorded. From analysis, this overhead ranges between 50-300ms but we have kept the timing data as-is in the interest of safety.

Each beacon node implementation emits `block`, `head`, and `blob_sidecar` events in different orders. To address this, we define a block/blob bundle as “arrived” only after all associated events for the slot have been recorded from each beacon node. This is once again a *worst case* scenario.

### Question 1

**How is 3/6 performing on Mainnet?**

> TL;DR: Pretty well!

[![](https://ethresear.ch/uploads/default/optimized/3X/3/2/3221f9f6e15311cbe773da0ffec6cd9df34fe899_2_690x475.png)1166×804 115 KB](https://ethresear.ch/uploads/default/3221f9f6e15311cbe773da0ffec6cd9df34fe899)

This chart shows block/blob bundle seen arrival times against the combined size of the bundle. When looking at locally built blocks proposed by solo stakers and seen by home users, a lot of block/blob bundles are seen before 4s.

[![](https://ethresear.ch/uploads/default/optimized/3X/5/0/503985d3e43892b27f5b8b85bdb4282958eb96a4_2_690x475.png)1166×804 118 KB](https://ethresear.ch/uploads/default/503985d3e43892b27f5b8b85bdb4282958eb96a4)

We should also look at blocks provided by MEV Relay as the reality is that a lot of blocks are proposed via this route. We can see an increase in the `min`, as there are additional round trips involved in this process, but things still look healthy!

**Outcome:** Block/blob bundles are arriving well within the 4s deadline for our home users.

### Question 2

**Does arrival time scale with block/blob bundle size?**

> TL;DR: Yes

[![](https://ethresear.ch/uploads/default/optimized/3X/9/5/95b81d2dec4ec6041818b4b717f5961957a0f90e_2_690x471.jpeg)3530×2411 650 KB](https://ethresear.ch/uploads/default/95b81d2dec4ec6041818b4b717f5961957a0f90e)

The trend lines show the 99th, 95th, and 50th percentiles of arrival times - meaning what percentage of blocks arrive were seen faster than that line.

These percentile trend lines answer our question: as bundle sizes increase, arrival times also increase. This suggests bandwidth is the primary bottleneck for these actors.

[![](https://ethresear.ch/uploads/default/optimized/3X/5/7/576cfaad3fa0db3276a657322f7180f6a4edf1b8_2_690x471.jpeg)3530×2411 651 KB](https://ethresear.ch/uploads/default/576cfaad3fa0db3276a657322f7180f6a4edf1b8)

Again looking at blocks provided via MEV Relay, we see a similar story.

**Outcome:** Yes, arrival times scale with block/blob bundles size

### Question 3:

**How much more can we support on Mainnet today?**

> TLDR: 4/8 and 6/9 are both achievable

To answer this question we need to check how big the block is. The 99th percentile of compressed beacon block size through our time period is `101KB`. Our blobs are fixed at a size of `128KB`.

Using these parameters, we can overlay the block/blob count:

[![](https://ethresear.ch/uploads/default/optimized/3X/3/c/3c3dbd09011f7924bf7c6eb43536b51fcb659c66_2_690x471.jpeg)3530×2411 918 KB](https://ethresear.ch/uploads/default/3c3dbd09011f7924bf7c6eb43536b51fcb659c66)

We can **very naively** plot a trend line to see when would cross the 4s attestation deadline.

[![](https://ethresear.ch/uploads/default/optimized/3X/5/5/55e090af2d5dcc7100554dc6d544be282c54d989_2_690x471.jpeg)3530×2411 1 MB](https://ethresear.ch/uploads/default/55e090af2d5dcc7100554dc6d544be282c54d989)

This trend line assumes a linear relationship between blob count and arrival time. Under this assumption, we can support up to 14 blobs per block while maintaining 95% of block/blob bundles arriving within the deadline. The 95% target provides margin for the 50-300ms processing overhead in our measurements, while also accounting for outliers.

[![](https://ethresear.ch/uploads/default/optimized/3X/9/e/9ea71149e7ec70d2fb3c96f23538dbc1c85a79fb_2_690x471.jpeg)3530×2411 1020 KB](https://ethresear.ch/uploads/default/9ea71149e7ec70d2fb3c96f23538dbc1c85a79fb)

When looking at MEV Relay blocks specifically, the data shows an even more optimistic picture - the 95th percentile trend line indicates support for up to 20 blobs per block. This improved performance can be attributed to MEV Relays being high-bandwidth nodes that help distribute blocks and blobs across the network in parallel with the proposer.

##### EIP7623

[EIP7623](https://eips.ethereum.org/EIPS/eip-7623) improves the worst case compressed block size to ~720KB - about 7x larger than our average historical block. Let’s analyze if we can still support more blobs with this increased block size.

[![](https://ethresear.ch/uploads/default/optimized/3X/f/d/fd1ab2e34d37c616c3f6a59bd19cab1e5daf7cbe_2_690x471.jpeg)3530×2411 967 KB](https://ethresear.ch/uploads/default/fd1ab2e34d37c616c3f6a59bd19cab1e5daf7cbe)

Even with an absolute *worst case* block size with [EIP7623](https://eips.ethereum.org/EIPS/eip-7623) we still support a blob increase. Note that the current maximum compressed block size on Mainnet is 1.79MB (and we’re seemingly going ok!), so take this data point with a grain of salt.

[![](https://ethresear.ch/uploads/default/optimized/3X/f/d/fdcce8fa1e9401070d2d913db490fac1667c47a0_2_690x472.jpeg)1175×804 208 KB](https://ethresear.ch/uploads/default/fdcce8fa1e9401070d2d913db490fac1667c47a0)

The trend for MEV Relay blocks again supports a much higher blob count compared to locally built blocks.

**Outcome:** The data supports a blob count increase, especially if [EIP7623](https://eips.ethereum.org/EIPS/eip-7623) is included at the same time. 4/8 or 6/9 are both safe to apply. There is potential for a higher blob count, but we’ll need to see how the network performs with an initial bump first.

### Conclusion

Ethereum’s decentralization is fundamental, and home stakers play a crucial role in this picture. The network is a delicate and intricate system that demands thoughtful and deliberate consideration.

Our analysis indicates that block arrival performance surpasses initial expectations for nodes with limited bandwidth. The community-contributed data offers valuable real-world insights into the network’s capabilities, and we would like to once again thank those who are contributing their data.

While we naively assumed a linear relationship between blob count and arrival time, this is a simplified view of a highly complex distributed system. Additionally, there are ongoing work streams that could either improve or worsen bandwidth requirements over time. Our analysis is focused on the data available to us now, based on observations from the past six weeks of network performance.

Based on block/blob arrival metrics alone, increasing the blob count from (target 3/max 6) to (target 4/max 8) or (target 6/max 9) appears to be viable. **However, this is just one of many factors to evaluate when deciding on blob count adjustments.**

## Replies

**potuz** (2024-11-27):

A deadline of 4s gives zero time for validation. Nodes can in principle optimize and precompute head optimistically and then discard the node if it’s not available but that’s not done in practice so at the very least any forkchoice accounting should be included (and presumably database access on some clients). Another end is the VC BN interaction and the signing by a potentially remote signer. I expect accounting for these should not change much your thesis, but anyway felt it should be included

---

**rolfyone** (2024-11-27):

Thanks for noting ‘arrival’ as when it’s been processed by the node and the events distributed, helps understand the graphs.

This looks like more than 1% of proposals don’t meet the 4 second benchmark, meaning they’d be missed when looked at for attestations, which isn’t great…

If you follow the trail to 9 it kind of looks like that number is approaching 5%… admittedly 5% of a small percentage of overall blocks being late but still definitely relevant.

This was a good set of data to look into, really appreciate all the work it must have taken to gather!

---

**yiannisbot** (2024-12-03):

Thanks for these very insightful results!

[ProbeLab’s](https://probelab.io) study that [@samcm](/u/samcm) referred to is this one that came out yesterday: [Bandwidth Availability in Ethereum: Regional Differences and Network Impacts](https://ethresear.ch/t/bandwidth-availability-in-ethereum-regional-differences-and-network-impacts/21138).

I think a relevant point to this study is the number of blobs per block carried over the network currently: [Bandwidth Availability in Ethereum: Regional Differences and Network Impacts](https://ethresear.ch/t/bandwidth-availability-in-ethereum-regional-differences-and-network-impacts/21138#p-51501-current-blob-count-per-block-14). We see that in 42% of the cases (slots), there are 5-6 blobs anyway.

Although it’s not straightforward, or accurate to make a direct correlation, the network is currently carrying what the future target would be (6) in 40+% of slots and there doesn’t seem to be any disruption at all.

---

**pop** (2024-12-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/samcm/48/19108_2.png) samcm:

> 1166×804 118 KB

What I see from this chart is mev builders tend to propose blocks with no blobs more often than local builders.

My hypothesis is that some mev builders prefer to send zero blobs to make the block propagation faster to have more time to play timing games while some mev builders who have higher bandwidth can afford to both play timing games and send 6 blobs.

I think it’s very valuable if we can plot this chart per mev builder so that we can know if mev builders behave differently.

---

**famouswizard** (2024-12-17):

[samcm](https://ethresear.ch/u/samcm), thanks for sharing! It’s great to see that the block and blob arrival times are performing well, even with increasing sizes.

How do you think changes in the network’s bandwidth, especially among solo stakers, could impact the feasibility of increasing the blob count further, especially in scenarios where solo stakers may not have access to high-bandwidth connections?

