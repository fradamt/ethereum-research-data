---
source: ethresearch
topic_id: 20679
title: Blob EIPs and Minimum Validator Requirements
author: MaxResnick
date: "2024-10-16"
category: Proof-of-Stake > Block proposer
tags: [data-availability]
url: https://ethresear.ch/t/blob-eips-and-minimum-validator-requirements/20679
views: 717
likes: 36
posts_count: 16
---

# Blob EIPs and Minimum Validator Requirements

[![](https://ethresear.ch/uploads/default/optimized/3X/4/7/477a44b70c262a922a22163da6ab2246f13fc6fa_2_690x376.png)1280×698 357 KB](https://ethresear.ch/uploads/default/477a44b70c262a922a22163da6ab2246f13fc6fa)

Author: Max Resnick

Acknowledgements: [@mikeneuder](/u/mikeneuder), [@timbeiko](/u/timbeiko), [@gakonst](/u/gakonst), [@mmp](/u/mmp), and Tivas Gupta for helpful comments.

# Blob EIPs and Minimum Validator Requirements

On the last execution ACD, a blob target increase as well as some other auxiliary proposals were moved to CFI status.

**Those proposals were:**

- EIP 7623 (Increase call data costs)

This EIP increases the gas cost of call data so that the maximum amount of call data possible in a block is lower, reducing the maximum size of a block. Before 4844 call data was how rollups posted their data to the blockchain so increasing the price of call data was not feasible but now that rollups are posting blobs instead we can raise the price of call data to control the max block size without causing problems for rollups.

EIP 7762 (Increase min_base_fee_per_blob_gas)

- This EIP sets a small reserve price for blobs (~1c) which is designed to increase the speed of price discovery. Each factor of 2 increase in the price of blobs takes almost 6 full blocks to achieve due to the controller implementation so setting this parameter to 2^25 wei rather than 1 wei saves a lot of time for the controller to ramp up.

EIP 7742 (Uncouple blob count between CL and EL)

- This is mostly a housekeeping change of putting blob count variables in the right place in keeping with the proper separation of concerns between the EL and CL.

EIP 7691 (increase blob target to 4 from 3, blob limit remains at 6)

- The EIP 4844 fee controller is an integral controller which would work just as well for 4 target, 6 limit as it does for 3 target, 6 limit.

## The Pushback

There was some pushback on the call and from solo stakers against these proposals. In particular, solo stakers were worried about the additional bandwidth required to solo propose a block. But if you look at the above proposals those fears may be misplaced. In fact if all the proposals were included together, it would lower the maximum size of the block. Increasing the blob target doesn’t mean increasing the blob limit and the addition of 7623 would lower the maximum size of the non-blob portion of the block payload.

In addition some solo-stakers posted about their poor upload bandwidth speeds which sparked a discussion of minimum validator requirements for solo-staking, especially if they are solo-proposing . Only a small fraction of nodes solo-propose blocks and doing so has a high opportunity cost. Still, let’s take these concerns at face value.

## Response to Pushback

First, how much bandwidth does it take to reliably propose a block of size x? The proposer needs their block to reach at least 40% of the network before 4 seconds into the slot. The block propagates through the P2P network but before this can happen, the proposer needs to seed it. It sends the full block to a subset of N of its peers. Sending to more and higher quality peers improves the probability that the block will reach a sufficient portion of the network before timeout.

But as I understand it, the default client implementations have very naive optimization for latency and reliability with peers. In other words, there may be ways that nodes can optimize their block propagation speed without using additional bandwidth.

Regardless, extremely poor connections from rural stakers are likely to present a bottleneck in the future so it is important to set internet connection requirements just as we set hardware requirements. I suggest 50Mb/s upload speed as a starting point for these discussions. While we don’t need nearly that much bandwidth today, the goal of the rollup roadmap is to get to 64 blobs per block so, even with optimizations coming with PeerDAS, we would have room for significant scaling in the future. Furthermore, 50MB upload speed on consumer internet is broadly available in North and South America, Asia and Europe. Africa also has substantial (albeit much less comprehensive) access at this speed range. This speed range will therefore give the network substantial headroom to grow, while still allowing for desirable levels of geographic decentralization.

## Proposals to Decrease The Minimum Stake

On Twitter, Vitalik proposed lowering the stake required to run a node. I think this would be a bad idea. There are two reasons we have stake, the first is accountability (slashing for bad behavior), and the second is sybil proofness (you need stake to participate). Lowering the minimum staking requirement would be bad on the margin because we already have far too many signatures to aggregate for finality. Each additional signature imposes a cost on the network by introducing another signature that must be aggregated each epoch. The current minimum stake seems about right to me and hopefully we see a large reduction in the node count after MAXEB in the next hardfork. Further, out-of-protocol solutions already allow solo-stakers to stake with substantially lower collateral.

## Replies

**aelowsson** (2024-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> On Twitter, Vitalik proposed lowering the stake required to run a node. I think this would be a bad idea. There are two reasons we have stake, the first is accountability (slashing for bad behavior), and the second is sybil proofness (you need stake to participate). Lowering the minimum staking requirement would be bad on the margin because we already have far too many signatures to aggregate for finality.

This proposal is envisioned as part of a transition to [Orbit SSF](https://ethresear.ch/t/orbit-ssf-solo-staking-friendly-validator-set-management-for-ssf/19928), or some other resolution outlined in Vitalik’s recent [guide](https://vitalik.eth.limo/general/2024/10/14/futures1.html) to this part of the roadmap. In Orbit SSF, small validators have a lower activity rate, alleviating issues of signatures aggregation. A further analysis of how finality can be designed to accrue in Orbit SSF can be found in a recent [research post](https://ethresear.ch/t/vorbit-ssf-with-circular-and-spiral-finality-validator-selection-and-distribution/20464).

As outlined in the linked post, I agree that there are some nuances to the issue of 1-ETH validators. It will make it more difficult to reach “full finality” (that is to say, finalized by the entire validator set) in a timely manner. Furthemore, it makes it possible to stake with very low risk for pools, likely necessitating stronger individual incentives.

---

**keyneom** (2024-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> I suggest 50MB/s upload speed as a starting point for these discussions.

Is this supposed to be megabytes or megabits?

---

**ab599597** (2024-10-16):

Appreciate the data, but worth mentioning that I live in Las Vegas, in a modern area of the city, and only have access to 100/5.

Your chart doesn’t show that reality.

---

**HawkBand** (2024-10-16):

I’m sorry but that’s a Las Vegas problem, not an Ethereum problem. It’s 2024, we can’t adapt to 5 mbps because certain zones of the US have infra comparable to the jungle of Cambodia.

That’s the speed my hometown in a non rich European country had 15 years ago.

I haven’t deeply research the bandwith we are targeting but there’s no need for 100% geographical diversification as the long tail of countries won’t add a meaninful amount of solo stakers.

I’m in favor of any bandwith that largely covers t1 and t2 cities in multiple continents, countries with different political systems and organizations such as EU, non EU countries in Europe, BRICS, NATO, G7, G20, MERCOSUR, ASEAN. It gives Ethereum all the geographical diversity it needs while remaining practical and being able to scale.

The proposed map seems to cover all of those. Although I would like to see a comparison of different upload speeds and compare the changes in terms of geographical diversity we lose/gain by increasing/decreasing the minimum bandwith.

---

**htimsk** (2024-10-16):

I’m very much in support of establishing some design minimum specification for bandwidth performance for an Ethereum validating full node. I was not certain from reading your post if you are proposing 50 MB/s (megabytes per second) or 50 Mbps (50 megabits per second). I think you meant to say the latter but can you please clarify.

Also it would be good to know if the minimum data transmission rate specification that you proposed is for symmetrical transmission meaning that both upload and download transmission speeds for the node should be 50 Mbps each way.

Two other points that I think is important to also establish in a minimum design specification is an expected total data transmitted over a month period for the node (e.g.,  Total Net I/O Tx 2.16 TiB (terabibibytes); Rx 2.38 TiB). This would help establish service requirements that establish a data cap in their monthly fees.

Last but not least also establishing some minimum latency specification for the Ethereum node design would be helpful. (e.g. < 15 ms (miliseconds) at idle or load)

---

**MaxResnick** (2024-10-16):

megabits, sorry edited for clarity

---

**MicahZoltu** (2024-10-17):

If we want to set a bandwidth requirement, I recommend setting it to StarLink upload speed because that is available almost everywhere in the world, is priced for consumers, and speed availability is uniform across the planet.

Of course, people can use whatever ISP they choose but I think StarLink gives a very nice baseline where few people can reasonably say “I don’t have access to internet that fast” and the ones who can say that can only do so because their government is oppressive and doesn’t allow it, not because infrastructure hasn’t reached them yet.

A quick search suggests that StarLink upload is around 10mbps at the moment, though it also does suggest it varies a bit by region (surprising, perhaps saturation of local satellites?).  Someone could do more thorough research and probably get some real numbers.

---

**chaudhary-amit** (2024-10-17):

‪The data on bandwidth (50 Mbps upload) sourced from Ookla shows significant issues when it comes to making population-wide conclusions. ‬

‪1. Selection Bias - Since Ookla relies on crowd-sourced data, it reflects the broadband speeds reported by a self-selected sample, making it unreliable for generalization.‬

‪   ‬

‪2. Spatial Accuracy: The accuracy of the location data is questionable, further complicating the assessment of internet access.‬

‪Access to internet speed is a critical issue, particularly concerning the digital divide. Even government statistics come under scrutiny—take, for example, the Federal Communications Commission (FCC), which has been found to misrepresent data.‬

‪[https://www.vice.com/en/article/study-us-broadband-gaps-three-times-worse-than-government-claims/‬](https://www.vice.com/en/article/study-us-broadband-gaps-three-times-worse-than-government-claims/%E2%80%AC)

‪[https://github.com/microsoft/USBroadbandUsagePercentages‬](https://github.com/microsoft/USBroadbandUsagePercentages%E2%80%AC)

‪This issue quite evident in the U.S., often touted as the leader in broadband speed globally. In other regions, the bias inherent in Ookla’s data is likely to be even more pronounced.‬

‪so the minimum bandwidth threshold of 50 Mbps is excessively high, effectively excluding many geographies and zip codes from consideration.‬

---

**siladu** (2024-10-17):

50 Mbps rules out Australia almost entirely ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

Certainly rules out the locations that are currently running nodes.

---

**bkellerman** (2024-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> EIP 7691 (increase blob target to 4 from 3, blob limit remains at 6)

This create asymmetric base fee response for full and empty blobspace, +8.1% and -14.6% respectively(w/o changing the update fraction). Have we thought about this fully?

If all of these are included, we would be making the fee response asymmetrical, reducing the upside response by 35%(12.5->8.1%), and putting in a minimum fee. This seems like a lot to do all at once.

---

**benaadams** (2024-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> I suggest 50Mb/s upload speed as a starting point for these discussions.

As the P2P network is TCP the theoretical link speed is largely irrelevant as it is capped by latency RTT and packet loss.

With the max throughput being:

`Max DATA throughput rate < (MSS/RTT)*(1 / sqrt(packetLoss))`

For ipv4 the Internet MSS minus framing is 1460 bytes; so if a connection between peers is 225ms (peers aren’t connected based on lowest latency/geographic nearness); and packet loss is 0.1% that gives a maximum throughput of:

`(1460 / 0.225) *  (1 / sqrt (0.001)) = 6489 * 31.6 = 205,052 bps`

So a rate of 205 Kbps; this is regardless of link speed; but the nature of TCP. It would be the same on 1Gbps up connections.

LibP2P does support QUIC as an alternative which the [Consensus Layer has accepted should be moved to](https://github.com/ethereum/consensus-specs/pull/3866); however this would need to happen before expecting a 50Mbps up speed to even be possible to anything other than geographically near peers (which the P2P doesn’t prioritise as it’s not very decentralizing)

---

**yiannisbot** (2024-10-17):

Your formula is close to what things used to be like, but not quite. Instead of `MSS` you would have to put TCP’s congestion window size (`CWND`), which was traditionally set to 64KBs. Also, packet loss is rarely a thing in the Internet and definitely not constant throughout a transfer.

So, the formula would be closer to `CWND/RTT`. Then modern TCP stacks allowed for window scaling to multiples of the 64KBs (see CUBIC and BBR and I don’t know what else is implemented these days), if there is enough bandwidth to exploit in the connection - basically the last mile, which is where the available bandwidth comes into the picture.

---

**HawkBand** (2024-10-17):

Map of the upload speed published by Starlink https:// www . starlink. com/map?view=upload

---

**MicahZoltu** (2024-10-18):

Thanks!  I’m extremely suspicious of this map given how the upload speed aligns perfectly with political borders, but it is certainly a better data-point than my random internet search.

---

**Evan-Kim2028** (2024-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> In addition some solo-stakers posted about their poor upload bandwidth speeds which sparked a discussion of minimum validator requirements for solo-staking, especially if they are solo-proposing

How do the solo staker anguishes about their “poor” upload bandwidth speeds compare to your proposed 50mbs minimum?

