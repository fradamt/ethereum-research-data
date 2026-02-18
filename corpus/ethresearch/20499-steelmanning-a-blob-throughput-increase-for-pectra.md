---
source: ethresearch
topic_id: 20499
title: Steelmanning a blob throughput increase for Pectra
author: Nero_eth
date: "2024-09-26"
category: Sharding
tags: []
url: https://ethresear.ch/t/steelmanning-a-blob-throughput-increase-for-pectra/20499
views: 809
likes: 15
posts_count: 3
---

# Steelmanning a blob throughput increase for Pectra

# Steelmanning a blob throughput increase for Pectra

With the discussions about the Pectra hardfork scope continuing, I want to provide some empirical input on the current state of the network.

I’ll try to do so by answering some commonly raised questions that arise in discussions on the proposed blob target/limit increase for Pectra.

**The arguments for shipping [EIP-7691](https://eips.ethereum.org/EIPS/eip-7691) in Pectra are:**

- Continue scaling DA - with EIP-4844, we have only set the foundation.

Provide existing L2s and their apps enough blob space for further scaling.
- Avoid creating a precedent of “blob fees can explode and are unpredictable” (h/t Ansgar); this harms future adoption if rollups have to account for rare fee spikes over extended periods.

**The number of reorgs has been trending down since Dencun.**
**The impact of blobs on reorgs has decreased as well.**

## How did the number of reorgs evolve over time?

> reorged = “nodes saw a block by the proposer of the respective slot”
> missed = “no sign that the proposer was online”

- Within the last 365 days, 5,900 blocks were reorged.
- This equates to 0.225% of the blocks in that time interval.
- At the same time, 14,426 slots were missed, representing 0.549%.
- On average, we observe 492 reorgs and 1,202 missed slots per month.

The number of reorgs has been decreasing, which is a positive development, though not surprising, as core devs continuously improve client software. Interestingly, contrary to expectations that the most recent hard fork (= Dencun) would lead to a significant rise in reorgs, we actually observed the opposite trend.

**Since the Dencun upgrade, the number of reorgs halved.**

[![combined_reorgs_missed](https://ethresear.ch/uploads/default/optimized/3X/4/b/4b1dde8030fe4c0167480cd65d800b986c292802_2_571x500.png)combined_reorgs_missed800×700 39.6 KB](https://ethresear.ch/uploads/default/4b1dde8030fe4c0167480cd65d800b986c292802)

It’s challenging to identify the exact reason for the change in trend, but it may be attributed to the ongoing improvements made by core devs to their client software.

## What’s the impact of blobs on reorgs?

[Initial analysis](https://ethresear.ch/t/big-blocks-blobs-and-reorgs/19674) conducted a few months after the Dencun hardfork showed that blocks with 6 blobs were reorged 3 times more frequently than 0-blob blocks. In general, we observed that the reorg rate has increased steadily with a growing number of blobs.

Updating this analysis presents a different picture today. Even though we still see that 6-blob blocks are reorged more frequently than 0-blob or 1-blob blocks, the numbers have decreased significantly, showing no substantial difference between blocks with one blob and those with six blobs.

We still observe a small difference in the reorg rate for 0-blob blocks and x-blob blocks (where x > 0).

![reorgrate_animation](https://ethresear.ch/uploads/default/original/3X/0/6/0609208e43c3fb8f94ebcc46b3b99a4fc79eda27.gif)

## How well are blobs distributed over blocks?

Plotting the distribution, we can see that most blobs contain either 0 or 6 blobs, with blocks containing 1 to 5 blobs representing the minority. However, the situation has improved since the [last study](https://ethresear.ch/t/big-blocks-blobs-and-reorgs/19674), with fewer slots at the extremes of 0 blobs and 6 blobs.

![all_blobs_day](https://ethresear.ch/uploads/default/original/3X/c/c/ccf6c5d3f8fad8bbd1330b98c1bb8e804fc19014.gif)

## Related work

| Title | Url |
| --- | --- |
| On Attestations, Block Propagation, and Timing Games | ethresearch |
| Blobs, Reorgs, and the Role of MEV-Boost | ethresearch |
| Big blocks, blobs, and reorgs | ethresearch |
| On Block Sizes, Gas Limits and Scalability | ethresearch |
| The Second-Slot Itch - Statistical Analysis of Reorgs | ethresearch |

## Replies

**Evan-Kim2028** (2024-09-27):

Thanks for putting together a comprehensive overview of blob reorg rates since Dencun. One additional datapoint to consider is that during the June 20th blob congestion event resulting from the Layer Zero airdrop, blob reorg rates shot up to ~7% (20132500 to 20135500).

36 observed reorgs during this 3000 block period out of a 492 monthly average is ~7% of  average monthly reorgs in less than half a day!

[![image](https://ethresear.ch/uploads/default/original/3X/3/7/37c9c19e0d54b0f8a3d03035d89339204b5ca792.png)image536×451 12.7 KB](https://ethresear.ch/uploads/default/37c9c19e0d54b0f8a3d03035d89339204b5ca792)

It’s quite certain that we will see more black swan events like this in the future and this will spike reorg rates. The open question is what the worst case scenario might be to the network and if that is acceptable under an increased blob target/limit.

For example, in another black swan event with an increased blob target, could reorg rates be significantly higher than 7%, excacerbated by the increased number of blobs in the blob market?

---

**TimDaub** (2025-03-25):

The title of this post is “Steelmanning a blob throughput increase for Pectra” but the post mostly talks about reorgs, which seem to be about basically keeping the system working as expected. To me talking about reorgs isn’t an argument for economically motivating for Ethereum stakers why the blob target should be raised.

The two arguments that seem to me the strongest for increasing the blob throughput are:

(1)

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Avoid creating a precedent of “blob fees can explode and are unpredictable” (h/t Ansgar); this harms future adoption if rollups have to account for rare fee spikes over extended periods.

and (2)

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Provide existing L2s and their apps enough blob space for further scaling.

Now, for (1), the narrative over the last 6 months has been that L2s are extractive to Ethereum because Ethereum isn’t capturing value from, for example, Base’s insane fee accrual. It’s true, isn’t it? Why are we ETH holders giving all of this cashflow voluntarily to a random American CEX that has its own stake holders etc.?

Meanwhile Ethereum’s fee accrual is down an order of magnitude. Which mechanically means that ETH price will eventually follow it, unless something happens.

Let’s be honest, if blob fees were to explode for a few days and Ethereum stakers would get their fair share of the pie, today I’d consider that a fair thing to happen. And the hypothetical follow-up accusation, probably coming from cheap L2 operators, that “blob fees are unpredictable!!!” would be considered clownish, in particular because Ethereum has enabled these L2s to make so much money in the last year without being unpredictable at all. I honestly think that after having blobs online for more than a year without any major crisis in the pricing model, whatever happens now, by virtue of lindiness, blobs are predictable and non-explosive. And if that changes, I agree that there should be a quick path to fixing that.

As for (2): It’s insanely cheap right now to transact on L1 and it has basically always been insanely cheap to transact on L2s for the last year. So I don’t think there’s any urgency in raising the blob target for that reason.

Generally speaking, in my view the blob throughput increase steelman today has to provide a motivation for why we are increasing the blob target even though Ethereum’s fee accrual is at record lows. We’re not beating the “L2s are parasitic to Ethereum” accusation because we are too careful. If these mercantile L2 operators are moving to alt DA immediately after seeing higher prices on Ethereum, let them move, because it gives you more moral rights then to really scale Ethereum to undercut alt DAs.

Why is it a valid argument that we can increase the blob base fee and increase the blob target, but an invalid argument is that we can leave everything as is and only upgrade when the situation mandates it? Is this because the release process is bad and hard to coordinate? My understanding is that raising the blob target is just changing a few constants…

