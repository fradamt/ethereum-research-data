---
source: ethresearch
topic_id: 22665
title: "Behind the Scenes of Ethereum's Pectra Upgrade: A Data-Driven Analysis"
author: dennis-tra
date: "2025-06-25"
category: Networking
tags: [p2p]
url: https://ethresear.ch/t/behind-the-scenes-of-ethereums-pectra-upgrade-a-data-driven-analysis/22665
views: 469
likes: 9
posts_count: 1
---

# Behind the Scenes of Ethereum's Pectra Upgrade: A Data-Driven Analysis

# Introduction

Hard-forks are pivotal moments that redefine the capabilities and efficiency of the network. On May 7th, Ethereum Mainnet upgraded from the Deneb to the Electra fork which included a few critical changes and improvements to the consensus and networking layers of the protocol. This post specifically looks into how the network has prepared for the fork by analysing the network topology in the weeks leading up to the event, how message arrival times have changed, and if the upgrade enabled some relaxed bandwidth requirements.

For this, the [ProbeLab](https://probelab.network) team has conducted a dedicated analysis of the data that some of our measurement tools like [Nebula](https://github.com/dennis-tra/nebula) and [Hermes](https://github.com/probe-lab/hermes) have gathered before, during and after the hard fork event. This analysis complements our weekly updates on the [network topology](https://probelab.io/ethereum/discv5/2025-22/), [block arrival times](https://probelab.io/ethereum/block_arrival/2025-22/), [bandwidth usage](https://probelab.io/ethereum/gossipsub/bandwidth/2025-23-01/), and [more](https://probelab.io/ethereum). We have done [A Deep Dive into the P2P Layer of the Dencun Hardfork](https://probelab.io/blog/deep-dive-dencun/) a year ago which informed some of our focus areas for this study.

## tl;dr

These are our main takeaways

- Two days before the hard fork 53% of the network was ready for the upgrade
- 70% of the network upgraded immediately and an additional ~18% upgraded within the following five days after the fork
- The block broadcasting latency has not been affected overall:

Overall, we saw a slight decrease in the block arrival latency of close to 200ms at the median.
- However, some of the nodes located in Africa, Australia and South America, which are geographically more disadvantaged due to the higher latency to the EU and US (where most nodes are deployed) experienced slower block arrival times than before the upgrade.

Generally, around 5% of the blocks don’t arrive on time in the 4-second slot deadline implying potentially fewer rewards for validators due to missed attestation heads.

# Table of Contents

- Introduction

tl;dr

[Methodology](#p-55116-methodology-4)

- Tools used
- Dataset

[Network Topology Changes](#p-55116-network-topology-changes-7)

- Fork Digests
- Client Upgrades
- Takeaways

[Hardfork impact on block arrival times](#p-55116-hardfork-impact-on-block-arrival-times-11)

- Differences across continents
- Differences across clients
- Arrivals over the epoch duration
- Takeaways

[Network bandwidth throughput](#p-55116-network-bandwidth-throughput-16)

- Bandwidth per continent
- Bandwidth per hosting type
- Takeaways

[Conclusion](#p-55116-conclusion-20)

# Methodology

## Tools used

For the work presented in this post, the ProbeLab team made use of the following tools

- Nebula - a libp2p and discv5-compatible network crawler.
- Hermes - a lightweight GossipSub listener and tracer that subscribes to all relevant pubsub topics and traces all protocol interactions.
- Xatu - EF EthPandaOps’ network monitoring platform.

## Dataset

The results presented in this study span a period of two weeks: one week before the Pectra upgrade (i.e., dates: `2025-04-28` to `2025-05-07`), and one week after (i.e., dates `2025-05-07` to `2025-05-14`).

In the later “Hardfork impact on block arrival times” section of the report, we reference Xatu’s public database, which aggregates data samples from a diverse set of agents and nodes participating in the [Community Data Collection Effort](https://ethpandaops.io/posts/contribute-to-xatu-data/). This includes:

- Ethereum Foundation (EF) control nodes, also known as sentry nodes, which are deployed across various clients and geographic locations.
- Community-run nodes, which altruistically contribute data to the public database.

Data for the rest of the sections came from our continuous Nebula crawler deployment, plus custom scripts wherever it was needed.

# Network Topology Changes

## Fork Digests

[![Advertised Fork Digests over Time](https://ethresear.ch/uploads/default/optimized/3X/d/8/d85b8083d3f0ed5d23c9a328082d6f9c5c90c096_2_690x345.png)Advertised Fork Digests over Time2000×1000 164 KB](https://ethresear.ch/uploads/default/d85b8083d3f0ed5d23c9a328082d6f9c5c90c096)

The above graph shows the advertised fork digests in the discv5 DHT around the time of the hard fork. One can clearly see a sharp drop of advertised Deneb digests at the hard fork time: 2h after the hard fork, 70% of nodes followed the new fork. In the days following the hard fork there is a long tail of nodes updating to the new fork. However, five days after the fork there are still around 12% of nodes following the outdated fork. We can safely assume that these nodes don’t run validators, as otherwise, they couldn’t follow up with the head of the chain, which ultimately makes the validator unable to perform its duties.

One could assume that the nodes which didn’t upgrade on time are home/hobby deployments. However, if we split the online nodes five days after the fork in two categories 1) follows electra 2) does not follow electra, we can see that nodes who don’t follow electra predominantly run in cloud infrastructure - cancelling the hypothesis of home deployments.

[![Electra Cloud Share](https://ethresear.ch/uploads/default/optimized/3X/4/8/480e729885d6e5c0924af349ccc9b82fec3d9987_2_690x345.png)Electra Cloud Share2000×1000 117 KB](https://ethresear.ch/uploads/default/480e729885d6e5c0924af349ccc9b82fec3d9987)

Looking at the **next** fork versions that nodes announce, we can see that some clients already advertise the next Fulu fork.

[![Advertised Next Fork Version over Time](https://ethresear.ch/uploads/default/optimized/3X/d/3/d3aa9411716c841c57e38d17d3aa3f289620b277_2_690x345.png)Advertised Next Fork Version over Time2000×1000 168 KB](https://ethresear.ch/uploads/default/d3aa9411716c841c57e38d17d3aa3f289620b277)

Interestingly, this is almost exclusively Prysm that already announces Fulu here. The other client implementations still only publish Electra.

## Client Upgrades

Looking at the days leading up to the hard fork, we focus on how users of the Prysm, Lighthouse and Teku implementations adapted compatible client versions.

The following graphs show the number of nodes running a certain version of one of the mentioned client implementations over time until a few days after the hard fork. All three graphs denote the time at which the hard fork happened as well as when the first compatible version for the new fork was released on GitHub.

[![Prysm Electra-compatible Versions over Time](https://ethresear.ch/uploads/default/optimized/3X/0/b/0b38d1f635206d3a91ecbfe1eff17a932356d3c2_2_690x345.png)Prysm Electra-compatible Versions over Time2000×1000 180 KB](https://ethresear.ch/uploads/default/0b38d1f635206d3a91ecbfe1eff17a932356d3c2)

[![Lighthouse Electra-compatible Versions over Time](https://ethresear.ch/uploads/default/optimized/3X/6/d/6df5ecb6c627280d7444845f6fb40b3b14671ed2_2_690x345.png)Lighthouse Electra-compatible Versions over Time2000×1000 183 KB](https://ethresear.ch/uploads/default/6df5ecb6c627280d7444845f6fb40b3b14671ed2)

[![Teku Electra-compatible Versions over Time](https://ethresear.ch/uploads/default/optimized/3X/8/e/8e7a9e68c5e8bb405ab0f42a97c512fbf7c4d5ed_2_690x345.png)Teku Electra-compatible Versions over Time2000×1000 223 KB](https://ethresear.ch/uploads/default/8e7a9e68c5e8bb405ab0f42a97c512fbf7c4d5ed)

As expected, in all three cases, we can see that shortly after an official release of the respective client, node operators started to upgrade. Two days before the hard fork around 53% of the nodes in the network were running an Electra-compatible client implementation - 60% one day before, 67% one hour before. The numbers don’t consider Nimbus clients as they don’t advertise version information. Nimbus is the fourth implementation with a significant share in network deployments, so the number of Electra-ready nodes is likely a few single-digit percentage points higher.

We can also safely say, that node operators don’t use the hard fork as an opportunity to switch client implementations as the following graph shows. The distribution of client implementations hardly changed during the fork.

[![Client Types over Time](https://ethresear.ch/uploads/default/optimized/3X/7/3/736459a475bd00fff1cd1b95aa6ebb1ceed4e463_2_653x500.png)Client Types over Time1568×1200 68.1 KB](https://ethresear.ch/uploads/default/736459a475bd00fff1cd1b95aa6ebb1ceed4e463)

## Takeaways

- Around 70% of online nodes followed the new fork immediately.
- A long tail of another ~20% followed the new fork one week after the event
- It’s difficult to say whether the remaining nodes are home/hobby deployments, as we’ve found that they run on cloud infra, i.e., less likely to have a node spun up without running a validator.
- Compatible client releases were picked up gradually the days leading up to the fork.

# Hardfork impact on block arrival times

One of the core additions of the Pectra upgrade is the increase of the blob target and max values by three extra blobs per block (see [EthPandaOps post](https://ethresear.ch/t/block-arrivals-home-stakers-bumping-the-blob-count/21096), [ProbeLab post](https://ethresear.ch/t/bandwidth-availability-in-ethereum-regional-differences-and-network-impacts/21138)). Despite the fact that the network benefits by that extra 50% of ephemeral space, this blob count increase also means that the network needs to transfer up to 348KBs extra data in every slot. This ultimately could have an impact on the overall message broadcasting capabilities of the network, if nodes can’t allocate more bandwidth at the early stages of the slot, when the block gets propagated.

The following graphs were aggregated by fetching all the block arrival times submitted to the EthPandaOps public Xatu instance. Note that the first chart belongs to the measurements before the Pectra upgrade, and the second one after the upgrade. This data includes not only data points from the Ethereum Foundation’s sentry nodes, but also from some external collaborators that participate in [the community data collection program](https://ethpandaops.io/posts/contribute-to-xatu-data/). For more clarity, the graphs describing the pre-Pectra state span the dates `2025-04-28` to `2025-05-07`, while the ones post-Pectra span the dates `2025-05-07` to `2025-05-14`. Furthermore, for the sake of a cleaner distribution, we’ve dropped all those block arrivals that exceeded 12 seconds since the beginning of the slot where they were proposed. We consider that a block arrival that exceeds the 12-second mark is likely to be related to a reorg rather than to the gossipsub message broadcast that we are trying to visualise.

## Differences across continents

The following graphs show the block arrival time using the start of the slot, or `t=0,` as reference. The first graph focuses on data before the Pectra upgrade. The graph shows similar distributions across the different countries, with the total mean of block arriving at the 2.386 seconds mark before Pectra. It is worth mentioning, though, that we do measure a spread of 500ms between the fastest receiving continent’s mean (Europe with 2.278 seconds) and the slowest one (Southern America with 2.725). Furthermore, the figure also shows that 95% of the data points were received within the 3.84 seconds of the slot, respecting the spec window of 4 seconds for the block propagation. However, this is not the case for all countries; nodes placed in Africa and South America had their 95th percentile of block arrivals exceeding the 4-second mark: at 4.327 and 4238 seconds marks, respectively.

Before Pectra Upgrade:

[![Before Pectra](https://ethresear.ch/uploads/default/optimized/3X/0/c/0c3d423ab2bb8edce21f06bf79c5a8166805f101_2_690x492.png)Before Pectra700×500 24.6 KB](https://ethresear.ch/uploads/default/0c3d423ab2bb8edce21f06bf79c5a8166805f101)

After Pectra Upgrade:

[![After Pectra](https://ethresear.ch/uploads/default/optimized/3X/e/2/e289589e5fedddede8077d8ddbbf7a3202b1de43_2_690x492.png)After Pectra700×500 24.4 KB](https://ethresear.ch/uploads/default/e289589e5fedddede8077d8ddbbf7a3202b1de43)

The second graph shows distribution of block arrivals after the Pectra upgrade. We observe that the aggregated mean distribution (not the division by continent) improved by 56ms at the 2.33 mark. Interestingly, we can also see how the tail of the distribution has increased by 22ms at the 95th percentile with an arrival mark of 3.917 seconds since the start of the slot. The increase in the block propagation times can be attributed to the data points coming from South America, whose tail distribution got delayed by almost 220ms. In line with our initial expectations, countries with more restricted access to hardware resources or internet bandwidth (South America and Africa) seem to be the ones taking the biggest hit in terms of block arrival awareness.

## Differences across clients

The following graphs show the CDF of the block arrivals aggregated by the client type that submitted the data points. The graphs barely show any differences between the pre- and post- Pectra upgrade. The only client that presents minimal differences is Prysm, which reported a mean block arrival time 120ms sooner than before the upgrade, and which, together with Teku, seems to be aware of blocks before the rest of the clients. Although we need to take this with a grain of salt, we should take these graphs as a performance comparison between CL clients (check out the disclaimer note below the charts).

Before Pectra Upgrade:

[![Before Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/d/b/db8e54ba51a26e30372e3d0ced0e26947215668a_2_690x492.png)Before Pectra Upgrade700×500 24.5 KB](https://ethresear.ch/uploads/default/db8e54ba51a26e30372e3d0ced0e26947215668a)

After Pectra Upgrade:

[![After Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/2/6/2687eae5e2cfa7fecae01ea70c9e385afa149417_2_690x492.png)After Pectra Upgrade700×500 25 KB](https://ethresear.ch/uploads/default/2687eae5e2cfa7fecae01ea70c9e385afa149417)

> Disclaimer
> The are a few reasons that should prevent us from taking these CL clients numbers as a performance comparison:
>
>
> Xatu received the data points from the Beacon API event stream endpoint, which despite being a standard, each client decides how to implement internally. This means that each developer team decides at which step of the internals it is time-stamping the block arrival. Some might timestamp it as soon as the message passes the gossipsub validations, others might timestamp it after the application layer has validated it.
> The distribution of these nodes is not even or homogeneous across the different geographical locations. Which means that the submitted datapoints for these clients are highly subjected to the resources where they are running. Hypothetical example: if a single node is reporting from South America and that happens to be a nimbus node (which has lower representation in the network), nimbus isolated metrics are likely going to look worse than others.

## Arrivals over the epoch duration

The figures above give us a wide overall view of the pre- and post-hardfork network status. However, they could be hiding sudden spikes or performance drops during specific epochs, i.e., the hardfork transition. To address this, the following charts display the same aggregated block arrival times and aggregations, but in a time series format.

The following graph shows what we think are the four most relevant data points over time: the minimum, the mean, the median, and the 95th percentile of the reported block arrival times. The figure shows stable block propagation over the network, with just a sudden spike of the 95th percentile line reaching the 4.6 seconds mark 12 hours before the hard fork on May 7th at 00 AM UTC (the hardfork took place at 10am UTC on May 7th). The spike lasted for a few hours before recovering and eventually lowering the mean and median arrival times to ~2.2 seconds from a former average of 2.38 seconds.

We attribute the spike of block arrivals around the hardfork time to some of the late-updating nodes that could indeed interfere with the mesh stability.

[![Message Arrival Times Percentiles](https://ethresear.ch/uploads/default/optimized/3X/b/e/be40ae0bb67efe8446f76ada6cb981203c7c0910_2_690x492.png)Message Arrival Times Percentiles700×500 43.3 KB](https://ethresear.ch/uploads/default/be40ae0bb67efe8446f76ada6cb981203c7c0910)

Once again, we observe that there are still 5% of block arrivals close to or even exceeding the 4-second mark, which should be alarming for MEV builders, but also individual builders with regard to the bids they accept.

The next graph aggregates the mean block arrival time *by continent*, where we can see quite a few different spikes:

- The first noticeable spike appears on the 28th of April at 11 AM in the region of Africa, which presented a mean block arrival of 3.6 seconds, before dropping to normal levels (~2.6 seconds after 10 hours).
- The second spike corresponds to the 30th of April at 3 AM, when the data points from nodes in Asia reported a mean arrival time up to 3.36 seconds for approximately 8 hours.
- The last visible spike is the biggest one, with a total duration of 19 hours that started on May 6th at 3 PM and finished right at the hardfork. The spike comes from nodes in South America, which reported a mean arrival time of close to 3.8 seconds.

[![Message Arrival Times by Continent](https://ethresear.ch/uploads/default/optimized/3X/3/3/334e65e6bf1e3b083a188c8955666a7752a656ce_2_690x492.png)Message Arrival Times by Continent700×500 63.2 KB](https://ethresear.ch/uploads/default/334e65e6bf1e3b083a188c8955666a7752a656ce)

The next graph shows the same time distribution but aggregating the block arrivals by the mean *per client*. The graph shows similar block arrivals to the pre-Pectra era, although most of them show performance improvement:

- We still see that all clients experience the spikes discussed above, during and after the hard fork.
- Prysm and Teku are still the first ones to receive the messages by a margin of approximately 300ms.

[![Message Arrival Times by Client](https://ethresear.ch/uploads/default/optimized/3X/c/2/c22833ed31c6862318113950e0a0b53e5f4df5a9_2_690x492.png)Message Arrival Times by Client700×500 69.1 KB](https://ethresear.ch/uploads/default/c22833ed31c6862318113950e0a0b53e5f4df5a9)

> Disclaimer:
> Check the previous disclaimer around the aggregated distributions for the different CL clients here.

## Takeaways

- According to the Xatu database, 5% of the blocks don’t arrive on time at the controlled nodes where we collect data from.
- The increase of blobs, as anticipated, hasn’t affected the core of the network. Not at least with regard to its capacity to broadcast and receive beacon blocks at the expected time windows.

Our measurements show that, at the median, the overall performance of the network, in terms of block arrival time, has marginally increased (i.e., blocks arrive ~200ms earlier).
- Only the tail, which can be more limited in terms of resources, showed lower performance.

# Network bandwidth throughput

One of the main concerns of the Pectra upgrade was how the network would react to a 50% increase in the blob target and max values. More precisely, whether it would resist that increase in bandwidth throughput, and if it would still be ready to keep pushing the limits ([EthPandaOps post](https://ethresear.ch/t/block-arrivals-home-stakers-bumping-the-blob-count/21096), [ProbeLab post](https://ethresear.ch/t/bandwidth-availability-in-ethereum-regional-differences-and-network-impacts/21138)). This last chapter of the study presents the results from the upload bandwidth throughput measurements that ProbeLab carried out during the hardfork.

The following graphs show the CDF of the measured upload throughput for nodes in the Ethereum mainnet network when requested for a list of the latest 20 blocks from four different geographic locations. The first graph shows the measured distribution before the Pectra upgrade, and the one below the measurements after the Pectra upgrade.

Interestingly, when comparing both graphs, what we see is that the network didn’t experience any alarming changes in the bandwidth throughput distributions. However, we do see a small reduction in the available throughput for the lower half of the distribution (1st to 50th percentiles).

On a general note, we’ve observed a reduction of 1 Mbps for both the 10th and the 50th percentiles, which shifted from averages of 9.94 and 24.78 Mbps to 8.84 and 23.53 Mbps for home and cloud deployments, respectively. This reduction seems to be more present in the US West and Southeast Asia regions.

There is still some good news, though. The upper percentiles of the distribution showed bigger throughput beyond the mean, increasing the 75th and 90th percentiles from 37.22 and 61.46 Mbps to 40.26 and 82.12 Mbps, for home and cloud deployments r espectively.

Before Pectra Upgrade:

[![Before Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/8/7/87e9c1eccc587f2c64bd988a5141a07209d765c8_2_690x492.png)Before Pectra Upgrade700×500 32.7 KB](https://ethresear.ch/uploads/default/87e9c1eccc587f2c64bd988a5141a07209d765c8)

After Pectra Upgrade:

[![After Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/d/d/dd4a950c64fe59c6100cbbc885a6815a27b0dab0_2_690x492.png)After Pectra Upgrade700×500 32.5 KB](https://ethresear.ch/uploads/default/dd4a950c64fe59c6100cbbc885a6815a27b0dab0)

### Bandwidth per continent

If we display the distribution based on the location of the remote node, we get the following graphs.

- Our measurements from nodes located in Africa show that the 20 Mbps mark has shifted from 20% of the measured peers to only 12% of them. However, the tail of the distribution reported higher bandwidth limits than before the hard fork.
- The trend of having larger throughput on the higher percentiles is also applicable to the distributions aggregated by continents. Nodes in the US and Europe are, in this case, the ones reporting the highest throughput. Our measurements show that over 20% of the nodes in those regions exceed throughput of 40Mbps.

Before Pectra Upgrade:

[![Before Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/e/e/ee24705d82b43f17e33ebca3e857794619534ec7_2_690x492.png)Before Pectra Upgrade700×500 35.8 KB](https://ethresear.ch/uploads/default/ee24705d82b43f17e33ebca3e857794619534ec7)

After Pectra Upgrade:

[![After Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/d/0/d089a4cee54809d47f5706eae8359f9070ffa4f9_2_690x492.png)After Pectra Upgrade700×500 35.8 KB](https://ethresear.ch/uploads/default/d089a4cee54809d47f5706eae8359f9070ffa4f9)

### Bandwidth per hosting type

Thanks to the data we gather from Nebula, we can identify the host type of the probed nodes, aggregating the measurements by those nodes hosted in cloud servers and those that we couldn’t correlate to any major data centre.

The following graphs show that the distributions didn’t change much in either case. The only perceived change corresponds to a variation of the steepness of the 30th percentile of the nodes hosted at cloud services, which has been slightly degraded by 1 Mbps. Either way, in both cases, the tail of the distribution shows the increment in throughput beyond the median, indicating that nodes were able to reply sooner with the whole set of requested blocks.

Before Pectra Upgrade:

[![Before Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/c/2/c2677393d39702f40fac738fdc7befc52c37afef_2_690x492.png)Before Pectra Upgrade700×500 18.5 KB](https://ethresear.ch/uploads/default/c2677393d39702f40fac738fdc7befc52c37afef)

After Pectra Upgrade:

[![After Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/7/e/7e503f87f83ad2eef7d67cf6c876b7b601d7d112_2_690x492.png)After Pectra Upgrade700×500 18.5 KB](https://ethresear.ch/uploads/default/7e503f87f83ad2eef7d67cf6c876b7b601d7d112)

Plain throughput is not the only thing that we are looking for; at least in Ethereum, the timings are relevant. Since the network has specific time windows, it is important to see when that throughput is available within the slot. The following graphs show the mean measured throughput aggregated by host type and the slot time at which the beacon blocks were requested.

The pattern is clear, there is a drop in both cloud and non-cloud hosted nodes between the first and the fourth second of the slot. This is the window when the network broadcasts the beacon blocks and the blob sidecars over gossipsub.

When it comes to comparing the pre- and the the post-Pectra upgrade distributions, what we see is that both follow the exact same pattern over the slot. The only difference, in this case, is that the mean has increased by 5-6Mbps for cloud nodes and 2Mbps for non-cloud nodes.

Before Pectra Upgrade:

[![Before Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/e/5/e5e02b0a711da6efcbb4c701dcec6983ddf30320_2_690x492.png)Before Pectra Upgrade700×500 20.9 KB](https://ethresear.ch/uploads/default/e5e02b0a711da6efcbb4c701dcec6983ddf30320)

After Pectra Upgrade:

[![After Pectra Upgrade](https://ethresear.ch/uploads/default/optimized/3X/2/8/2886ebf2957d257b6b78e280a79b49f2fecced36_2_690x492.png)After Pectra Upgrade700×500 20.4 KB](https://ethresear.ch/uploads/default/2886ebf2957d257b6b78e280a79b49f2fecced36)

### Takeaways

- The network is generally in a healthy state despite the addition of 3 extra blobs.
- Nodes at the top-end of the resource availability distribution seem to have more bandwidth available than before the upgrade.
- On the other end of the spectrum, the more restricted peers in the network have perceived a small drop in upload throughput, which, however, is considered neither significant, nor critical.
- As reported in this ethresear.ch post [link], there is a clear reduction in the number of duplicate messages due to the addition of the IDONTWANT message primitive, but its influence in terms of bandwidth availability is not clear across the spectrum of node resource availability.

# Conclusion

The fork event highlighted a tendency among node operators to wait until the last minute to upgrade. While the majority of nodes followed the new fork on time, a significant portion lagged by up to a week. Compatible client releases were being adopted only gradually ahead of the fork, indicating that upgrade urgency is still lacking across parts of the network.

On the propagation side, timely block delivery still isn’t guaranteed. Around 5% of blocks arrive late at control nodes, and while median timings improved, the tail continues to struggle—pointing to persistent gaps in resource availability or network performance.

Still, the network overall remains in a stable and healthy state post-fork. The addition of extra blobs has not caused major disruption and the introduction of `IDONTWANTs` has improved the situation, but not significantly. Some nodes appear to have more bandwidth availability, possibly due to the `IDONTWANT` addition, or provision of extra bandwidth resources, while less powerful nodes (likely home stakers) present a slight reduction in terms of upload throughput.
