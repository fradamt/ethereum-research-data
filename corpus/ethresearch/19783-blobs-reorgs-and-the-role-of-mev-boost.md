---
source: ethresearch
topic_id: 19783
title: Blobs, Reorgs, and the Role of MEV-Boost
author: Nero_eth
date: "2024-06-11"
category: Sharding
tags: [mev, data-availability]
url: https://ethresear.ch/t/blobs-reorgs-and-the-role-of-mev-boost/19783
views: 4737
likes: 15
posts_count: 4
---

# Blobs, Reorgs, and the Role of MEV-Boost

# Blobs, Reorgs, and the Role of MEV-Boost

**The TL;DR is:**

- Builders might have an incentive to not include blobs because of the higher latency they cause.
- Non-MEV-Boost users include, on average, more blobs in blocks than MEV-Boost builders.
- MEV-Boost users show a significantly lower probability of being reorged than Non-MEV-Boost users (see section MEV-Boost and Reorgs for details).
- Rsync-Builder and Flashbots have a lower average number of blobs per block than other builders.

---

In a [recent analysis on big blocks, blobs and reorgs](https://ethresear.ch/t/big-blocks-blobs-and-reorgs/19674), we could see the impact of blobs on the reorg probability.

**In the following, I want to expand on this by taking the MEV-Boost ecosystem into account.**

**The fundamental question is…**

-> **“*Does MEV-Boost impact reorgs, and if so, by how much?*”**

Blobs are “*big*” and big objects cause higher latency. Thus, one might expect builders to not include blobs into their blocks in scenarios in which:

- The builder is submitting its block late in the slot to minimize latency (see timing games).
- The builder wants to capture a high MEV opportunity and doesn’t want to risk unavailable blobs invalidating its block.
- The proposer is less well connected (because the gossiping starts later in the slot).

**Builders** might demand to be **compensated** through priority fees for including transactions which might cause blocks to be propagated with higher latency. Until 4844, such transactions have been those with a lot of calldata. As of 4844, blobs are the main drivers of latency.

[![tx_type_prio_fee_all (2)](https://ethresear.ch/uploads/default/optimized/3X/8/d/8db1993891d52c3c8be9d7c6adde8633810ad15b_2_690x345.png)tx_type_prio_fee_all (2)1200×600 61.8 KB](https://ethresear.ch/uploads/default/8db1993891d52c3c8be9d7c6adde8633810ad15b)

**As visible in the above chart, blob transactions don’t tip as much as regular Type-2 transactions.**

Based on that, blobs don’t give builders a significant edge over other builders competing for the same slot.

Another explanation could be private deals between builders and rollups to secure timely inclusion of blob transactions for a fee paid through side channels.

## MEV-Boost and Reorgs

The MEV-Boost ecosystem consists of sophisticated parties, **builders** and **relays**, that are well connected and specialized in having low-latency connections to peers.

Thus, it is expected that proposers using MEV-Boost should be reorged less often than ‘Vanilla Builders’ (i.e., users not using MEV-Boost).

[![reorgs_mevb_over_blobs (3)](https://ethresear.ch/uploads/default/optimized/3X/8/5/859fee3890096d24a955abd65642fee08ebd141c_2_690x258.png)reorgs_mevb_over_blobs (3)1200×450 21 KB](https://ethresear.ch/uploads/default/859fee3890096d24a955abd65642fee08ebd141c)

This expectation holds true when looking at the above chart.

**We can see that the reorg probability increases with the number of blobs. However, the reorg probability for MEV-Boost users is much lower than the one for Non-MEV-Boost users (Vanilla Builders).**

**In this context it’s important to not confuse correlation and causation:

-> *Non-MEV-Boost users are on average less sophisticated entities which also contributes to the effect we observe in the above chart.***

In this context it is interesting to compare the **average number of blobs per block** of MEV-Boost users vs. Non-MEV-Boost users.

[![blobs_over_time (3)](https://ethresear.ch/uploads/default/optimized/3X/3/c/3cbac65d110bbf6d535ba55d7dfb62f69206a271_2_690x373.png)blobs_over_time (3)1200×650 48.7 KB](https://ethresear.ch/uploads/default/3cbac65d110bbf6d535ba55d7dfb62f69206a271)

**As visible in the above chart, proposers not using MEV-Boost included on average more blobs into their blocks than MEV-Boost users.**

This might point towards MEV-Boost ecosystem participants (relays and builders) applying strategies that go beyond the “*include it if there’s space*” strategy.

**First, let’s look at the builders more closely.**

[![blobs_over_time_builder (4)](https://ethresear.ch/uploads/default/optimized/3X/4/b/4bf0a4fe8bc95e88d122c479fe88cf4f32883fbf_2_690x258.png)blobs_over_time_builder (4)1200×450 69.4 KB](https://ethresear.ch/uploads/default/4bf0a4fe8bc95e88d122c479fe88cf4f32883fbf)

Vanilla Builders (Non-MEV-Boost proposers) are the ones that have the highest blob inclusion rate, followed by Beaverbuild and Titan Builder.

Rsync-Builder seems to include way less blobs in their blocks.

The same applies to the Flashbots builder that seems to have changed its behavior in early May, with the average number of blobs per block approaching zero.

**“Is it fair to say 'Builder XY censors blobs!?”**

> **No**

> Different builders follow different strategies. For example a builder such as Rsync-Builder that is generally competitive in slots where low latency and speed matters might end up with winning those blocks where there are no blobs around (c.f. selection bias)

**Next, let’s shift the focus to the relays:**

[![blobs_over_time_relays (4)](https://ethresear.ch/uploads/default/optimized/3X/3/7/374ff432477462e6a307a3d83c7da899f3a5b541_2_690x258.png)blobs_over_time_relays (4)1200×450 72 KB](https://ethresear.ch/uploads/default/374ff432477462e6a307a3d83c7da899f3a5b541)

As visible above, Vanilla Builders have on average the highest blob inclusion rate.

The Ultrasound and Agnostic Gnosis relays are second and third, followed by the relays of BloXroute.

The Flashbots relay seems to include the lowest number of blobs.

**Importantly, relays are dependent on builders and ultimately it’s the builders that impact the above graph.**

## Next Steps

In the context of [PeerDAS](https://ethresear.ch/t/peerdas-a-simpler-das-approach-using-battle-tested-p2p-components/16541), the network will have to rely on nodes that are *stronger* than others and able to handle way more than 6 blobs per block. Therefore, it’d be super valuable to see more research on that topic happening.

- Call for reproduction: It’d be great if someone could verify my results by reproducing this analysis.
- Investigate the reasons why certain builders have a significantly lower blob inclusion rate than others.
- Reduce reorg rate for Non-MEV-Boost users: Relays could offer Non-MEV-Boost users their block propagation services to ensure that fewer of their blocks get reorged.

The blob market is still under development and a stable blob price is yet to be discovered. With increasing demand for blob space, tips from blob transaction will likely catch up to regular transactions.

## Replies

**meridian** (2024-06-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Rsync-Builder seems to include way less blobs in their blocks.
> The same applies to the Flashbots builder that seems to have changed its behavior in early May, with the average number of blobs per block approaching zero.

It would be interesting to see in the cases of builders including blob transactions if such inclusion paid a higher price than if they had not used blobs (i.e. calldata would have been cheaper).

Also to which extent are blobs being used and also paying higher than if they had used calldata.

---

**Evan-Kim2028** (2024-06-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> As visible in the above chart, blob transactions don’t tip as much as regular Type-2 transactions.
> Based on that, blobs don’t give builders a significant edge over other builders competing for the same slot.

We have to acknowledge outliers such as the Jared sandwich bot. They are such a large outlier that they can tip 1000x over the base gas price. In fact, sandwich bots in general account for over 95% of priority fees generated by [labeled libmev searchers](https://libmev.com/).

Monthly data snapshot for May

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/e/becd0ea940ac1c0b2d7d09703525339dd2c27de7_2_690x252.jpeg)image967×354 86.6 KB](https://ethresear.ch/uploads/default/becd0ea940ac1c0b2d7d09703525339dd2c27de7)

[![image](https://ethresear.ch/uploads/default/optimized/3X/6/2/62286d57bb4bbc76c374ce8315f78c436c9b7be4_2_690x300.png)image809×352 42.9 KB](https://ethresear.ch/uploads/default/62286d57bb4bbc76c374ce8315f78c436c9b7be4)

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Call for reproduction: It’d be great if someone could verify my results by reproducing this analysis.
> Investigate the reasons why certain builders have a significantly lower blob inclusion rate than others.

I think that [this flashbots dashboard](https://dune.com/flashbots/blob-block-builder-board)made by [@sui414](/u/sui414) mostly confirms your data on the same time frame. Note that Titan builder is at an average 3.8 blobs per block. I think the difference is that your data starts the first blob as 0 whereas the dune dashboard starts the first blob as 1.

I also have replicated results, albeit only on a 7 day timeframe that confirms that shows similar results to the end of your chart. Vanilla builders are at the top and confirm the most blobs per block. Note that my dataset only looks at the top 10 rollup producers, which accounts for the **majority** of blobs, but not **all** type 3 transactions.

[![image](https://ethresear.ch/uploads/default/original/3X/7/2/72639c375d580c30718b327be9ab1a64bb4f1389.png)image721×259 13.9 KB](https://ethresear.ch/uploads/default/72639c375d580c30718b327be9ab1a64bb4f1389)

---

**tripoli** (2024-06-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> We can see that the reorg probability increases with the number of blobs. However, the reorg probability for MEV-Boost users is much lower than the one for Non-MEV-Boost users (Vanilla Builders).

I feel like it’s worth explicitly mentioning that the relative increase in reorg rates for vanilla builders isn’t isolated to who builds the block, but is more of an effect from the interface between mev-boost and non mev-boost blocks. We can create the same plots (with an even stronger relationship in my reproduction) by filtering between whether the next proposer (the one doing the reorging) builds the block locally or via mev-boost.

MEV-Boost to MEV-Boost blocks are extremely rarely reorged, but as soon as either proposer builds one of the blocks locally the rates increase dramatically.

