---
source: ethresearch
topic_id: 20540
title: On solo staking, local block building and blobs
author: Nero_eth
date: "2024-10-02"
category: Sharding
tags: [mev, data-availability]
url: https://ethresear.ch/t/on-solo-staking-local-block-building-and-blobs/20540
views: 1264
likes: 17
posts_count: 12
---

# On solo staking, local block building and blobs

# On solo staking, local block building and blobs

[![](https://ethresear.ch/uploads/default/optimized/3X/6/7/679782c02f64eba56e5061a305e16a7815b77bc5_2_377x375.jpeg)791×785 121 KB](https://ethresear.ch/uploads/default/679782c02f64eba56e5061a305e16a7815b77bc5)

In recent weeks, discussions about a potential increase in blob throughput in Pectra have intensified, with two distinct groups emerging. One advocates for the increase, while the other is hesitant, preferring to wait for clear data supporting such a change.

From my perspective, one sentiment is overwhelmingly clear within the community:

\textbf{Solo stakers are at the heart of Ethereum.}

While there hasn’t been a consensus on the minimum requirements for validators (see [sassal.eth’s tweet](https://x.com/sassal0x/status/1839684947864322320) on that), the Ethereum community has made one thing clear:

\textbf{We do not want to sacrifice solo/home stakers for additional linear scaling.}

In my view, this reflects a healthy direction for Ethereum and underscores the community’s view on the importance of viable solo staking.

However, it raises an important question: “***Where is the line?***”

***Specifically, at what point does the contribution of a weaker, lower-bandwidth staker to decentralization no longer justify the limitations it imposes on Ethereum’s ability to scale?***

In this piece, I aim to provide additional data points to help the community make an informed decision on whether we want to pursue a blob throughput increase in Pectra.

> As Potuz, a core developer from Prysm, aptly stated, the real question is not “Do we want to scale, and how?” but rather, “Are we ready to do so now?”

## Who is being reorged today?  (Oct 2023 - Oct 2024)

[![](https://ethresear.ch/uploads/default/optimized/3X/f/7/f76b082ee7f082c61d5c9d69136f1151f702f5d3_2_690x345.png)1000×500 33.8 KB](https://ethresear.ch/uploads/default/f76b082ee7f082c61d5c9d69136f1151f702f5d3)

- On average ~0.2% of blocks are reorged (=reorged ⊆ missed).
- Professional node operators (NOs) such as Lido, Kiln, Figment, and EtherFi are reorged less often than the average.
- Less professional NOs such as solo stakers, Rocketpool operators, or the unidentified category which likely includes many solo stakers that couldn’t be identified, are more frequently reorged.

As shown in [an earlier analysis](https://ethresear.ch/t/steelmanning-a-blob-throughput-increase-for-pectra/20499), the reorg rate has been trending down since the Dencun hardfork.

In the following chart, we can see that this effect was different for different entities:

[![reorgs_entites_over_time (3)](https://ethresear.ch/uploads/default/optimized/3X/6/0/60009e3ddd9404a75f92b335b6acfa5fc7dfc4d2_2_690x345.png)reorgs_entites_over_time (3)1000×500 53.4 KB](https://ethresear.ch/uploads/default/60009e3ddd9404a75f92b335b6acfa5fc7dfc4d2)

- The reorg rate decreased for solo stakers and unidentified since Dencun.
- The same applies to Rocketpool operators, as well as larger operators such as Lido, Coinbase, Figment, and OKX.

## What about local block building? (Oct 2023 - Oct 2024)

[![](https://ethresear.ch/uploads/default/optimized/3X/8/3/8395fc7a154b30a8dc6cfabd6e3f5ca242a37c1d_2_690x345.png)1000×500 17 KB](https://ethresear.ch/uploads/default/8395fc7a154b30a8dc6cfabd6e3f5ca242a37c1d)

- Local builders have a reorg rate of approximately 1.02%.
- MEV-Boost builders have a reorg rate of approximately 0.20%.
- Local builders are approximately 5 times more likely to be reorged than MEV-Boost builders.

[![](https://ethresear.ch/uploads/default/optimized/3X/9/c/9cb8adb2f9f76b5c455c8d2857d15ae29686ef03_2_690x345.png)1000×500 32.9 KB](https://ethresear.ch/uploads/default/9cb8adb2f9f76b5c455c8d2857d15ae29686ef03)

- The reorg share for local block builders seems to have remained constant or even increased after the Dencun hardfork.
- For MEV-Boost users, reorgs have been trending down since Dencun.
- Notably, previous analysis showed that local builders included on average more blobs into their blocks. Furthermore we have seen that right after the Dencun hardfork blocks with 6 blobs struggled a bit, but this eventually stabilized again. This might explain why the reorg rate didn’t decrease for local builders.

## Who are the local builders? (Oct 2023 - Oct 2024)

[![](https://ethresear.ch/uploads/default/optimized/3X/c/6/c69dfe7af38af8f4d0f4da5172d1b415c82c1ddd_2_690x172.png)1200×300 13.7 KB](https://ethresear.ch/uploads/default/c69dfe7af38af8f4d0f4da5172d1b415c82c1ddd)

- Solo stakers (here labeled as “solo staker” but with many solo stakers in the unidentified category) are the largest entity within the “local builder” category.
- Furthermore there are Lido NOs that are not using MEV-Boost at all or use the min-bid flag.

# Key Insights

- Solo stakers tend to miss more slots compared to professional validators.
- Solo stakers often build their blocks locally rather than using MEV-Boost.
- Local block builders don’t benefit from the fast propagation offered by MEV-Boost relays.
- Relays engage in timing strategies (e.g., relay delays, allowing time to wait for even more profitable blocks).
- Epoch boundaries contribute to an increase in reorgs.

Multiple factors can lead to reorgs, making it challenging to pinpoint exactly why certain validators, like solo stakers, experience them more frequently than others.

## Replies

**Julian** (2024-10-02):

Thanks for the analysis! Do you know what the impact is on APR or absolute revenue? I thought it may be relevant since the percentage of reorgs is so small

---

**ivanmetrikin** (2024-10-02):

Great analysis, thanks!

> Solo stakers tend to miss more slots compared to professional validators

It’s not very surprising as solo stakers have slower machines and worse internet connections on avg compared to pros. Same goes for block reorgs: takes you longer to propose a block → more likely it’s gonna get reorged

> Furthermore there are Lido NOs that are not using MEV-Boost at all

All NOs from the “Curated Module” are supposed to use MEV-boost. But they do build vanilla blocks if relays are not available or not responding quick enough. See Block Space Distribution on rated.network

---

**roberto-bayardo** (2024-10-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/ivanmetrikin/48/17776_2.png) ivanmetrikin:

> All NOs from the “Curated Module” are supposed to use MEV-boost. But they do build vanilla blocks if relays are not available or not responding quick enough. See Block Space Distribution on rated.network

We might be seeing local building result in more reorgs simply because local building is being used mostly as a “fallback” later in the slot, not because it tends to include more blobs.

---

**potuz** (2024-10-02):

Is it possible to have the curve of local block building reorg rate at the same time as average blobs per hour during that time?

---

**Nero_eth** (2024-10-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/ivanmetrikin/48/17776_2.png) ivanmetrikin:

> All NOs from the “Curated Module” are supposed to use MEV-boost. But they do build vanilla blocks if relays are not available or not responding quick enough. See Block Space Distribution on rated.network

I can tell with with high certainty that there are many Lido validators who are either not using MEV-Boost or have a high.enough `min-bid` flag set which lets them fall-back to local building everytime it’s their turn to propose a block.

---

**Nero_eth** (2024-10-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/roberto-bayardo/48/11591_2.png) roberto-bayardo:

> We might be seeing local building result in more reorgs simply because local building is being used mostly as a “fallback” later in the slot, not because it tends to include more blobs.

I agree with the first part, though, local builder DO include more blobs than mevboost. I linked to [this ealier analysis](https://ethresear.ch/t/blobs-reorgs-and-the-role-of-mev-boost/19783) that had this chart:

[![blobs_over_time_builder (4)](https://ethresear.ch/uploads/default/optimized/3X/4/b/4bf0a4fe8bc95e88d122c479fe88cf4f32883fbf_2_690x258.png)blobs_over_time_builder (4)1200×450 69.4 KB](https://ethresear.ch/uploads/default/4bf0a4fe8bc95e88d122c479fe88cf4f32883fbf)

---

**roberto-bayardo** (2024-10-03):

Blob txs don’t provide much revenue so I can see why MEV builders would ignre them unless they have very high priority fees.  What I’m not seeing though is that there is a (strong) causal relationship between including blobs and higher reorgs.  There must be *some* relationship of course (bigger blocks/blobs will always have higher reorg rate) but is it the first-order factor behind higher reorgs for local builders?

---

**Evan-Kim2028** (2024-10-04):

I’m skeptical that it’s possible to see any meaningful relationship between higher blobs equals higher reorgs. There simply aren’t enough data points for all blob sizes - rollips tend to favor either 1 blob or 5-6 blobs per block.

---

**hzysvilla** (2024-10-17):

Thanks for sharing.

How do you identify the solo staker in the first diagram?  The data might be inaccurate if you use the graffiti field.

---

**Nero_eth** (2024-10-18):

Very conservatively by looking at their deposit address. Basically, checking if the deposit address behaved like a solo staker (e.g. having an ens name that doesn’t point to a company).

No graffiti data needed.

---

**armagg** (2024-12-16):

I think the number you provided is too low to conclude that we shouldn’t increase throughput. Even a slight linear scaling of the Ethereum network can have a significant impact on gas prices and the number of transactions, leading to greater adoption of the Ethereum network. This, in turn, could enhance decentralization. A 1% chance of reorganization doesn’t seem that concerning.

