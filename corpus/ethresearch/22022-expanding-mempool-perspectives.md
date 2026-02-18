---
source: ethresearch
topic_id: 22022
title: Expanding Mempool Perspectives
author: Nero_eth
date: "2025-03-27"
category: Uncategorized
tags: [protocol-research-call]
url: https://ethresear.ch/t/expanding-mempool-perspectives/22022
views: 893
likes: 14
posts_count: 3
---

# Expanding Mempool Perspectives

# Expanding Mempool Perspectives

> Many thanks to dataalways,  soispoke, ralexstokes and julianma for feedback on this post and EthPandaOps and Flashbots for the mempool data archives.

**TL;DR**: Ethereum might have been overindexing on “local builders” for censorship resistance.

Local building is required as a **fallback mechanism** to allow proposers (incl. *home stakers*) to **build their own blocks when needed** (e.g. when there’s a liveness issue caused by builders/relays). These fallbacks must be **permissionless and trustless**, which can be achieved through local building as it works today, or through open and permissionless gateways (**e.g. ePBS, or decentralized relays**). With permissionless participation in the MEV-Boost market, local building becomes unnecessary while **(weak) censorship resistance and liveness remain intact**.

## The Role of Local Builders, Private Orderflow and the Public Mempool

Ethereum has evolved from a **monolithic, gossip-driven public mempool** into a **dynamic ecosystem** of specialized block builders, private orderflow deals, user-operation bundlers, and L2 sequencers. This transition has resulted in several shifts:

- Enhanced Specialization – Introduction of services like pre-confirmations, based sequencing, front-running protection (MEV Blocker, Flashbots Protect), and improved mempool privacy, all contributing to better UX.
- Diminished Public Mempool Role – While its economic significance has declined, the public mempool remains critical for censorship resistance.
- Rise of Private Transactions – Currently, around 35% of transactions are submitted privately, predominantly via Beaverbuild and Titan Builder—a trend that has remained stable since June 2024.
- Centralization Concerns – Exclusive orderflow deals create economies of scale, leading to greater centralization among builders. However, PBS protects validators from centralization pressure, and e.g. Flashbots’ buildernet is tackling the risks on the builder side.

**A crucial question arises:**

 → *Do we need local builders?*

> For the following, let’s not confuse the role of home stakers with local builders. Those roles are different (even though often carried out by the same entity) and should be treated differently. Home stakers unquestionably are highly important to Ethereum, its decentralization and all the properties that result from it.

## Mempool != Mempool

There was never a comprehensive mempool. However, over time, increased sophistication has reduced the economic importance of the public mempool.

[![dgdfgdfgdf (5)](https://ethresear.ch/uploads/default/optimized/3X/0/4/04cbd8e3a6e562c00c1f0cdf3488d259ba9e6a3e_2_690x286.png)dgdfgdfgdf (5)923×383 37.8 KB](https://ethresear.ch/uploads/default/04cbd8e3a6e562c00c1f0cdf3488d259ba9e6a3e)

### Understanding Builders

- Local Builders
… are proposers who don’t use or fallback from MEV-Boost (min-bid flag) and access only the public mempool. Typically, these are home stakers who prefer not to rely on MEV-Boost relays, even if it means missing out on 3x the execution layer profits per block.
- MEV-Boost Builders
… see everything local builders do, plus additional private orderflow. This includes transactions sent to the builder via RPC services, searcher bundles, or builders directly doing based sequencing for L2s. The builders’ own transactions (e.g. MEV-Boost payment) are private orderflow too.

### How Much Private Orderflow Exists?

[![xof-over-time (2)](https://ethresear.ch/uploads/default/optimized/3X/8/0/807fb7eb47d847675645ddedaf842394e5b6d290_2_690x394.png)xof-over-time (2)700×400 22.5 KB](https://ethresear.ch/uploads/default/807fb7eb47d847675645ddedaf842394e5b6d290)

Approximately **35% of all transactions** in a block are private, meaning they never appeared in the mempool databases of **both Flashbots and Xatu**.

> Even with the combined efforts of Flashbots (incl. Alchemy, Bloxroute, Chainbound, and Eden) and Xatu nodes consistently logging observed transactions, some will inevitably go unseen. However, I’m confident that the dataset captures over 99.9% of all public mempool transactions.

The trend observed around summer 2024 didn’t continue, and we now see **30-40% of transactions being private**, which aligns with expectations, as many transactions have no clear incentive to be submitted privately.

> For DEX transactions, check out this query by dataalways, showing 80% private orderflow for those transactions.

While around 30-40% of all transactions are from private orderflow (*green line*), almost 70% (*violet line*) of the total fee paid originates from private orderflow.

[![share-over-time (2)](https://ethresear.ch/uploads/default/optimized/3X/7/a/7a91de831582ca102a52d7bb2354b67c7d83dd43_2_690x276.png)share-over-time (2)1000×400 49 KB](https://ethresear.ch/uploads/default/7a91de831582ca102a52d7bb2354b67c7d83dd43)

Focusing on builders, we see **Beaverbuild** and **Titan Builder** as the two big contenders for private orderflow:

[![xof-over-builder (3)](https://ethresear.ch/uploads/default/optimized/3X/d/b/dbb9f2844379a8dd25b177f86c01376d46ac3a42_2_690x413.png)xof-over-builder (3)1000×600 66.1 KB](https://ethresear.ch/uploads/default/dbb9f2844379a8dd25b177f86c01376d46ac3a42)

### Is the Public Mempool Dying?

Today, **locally built blocks** are significantly **less full** than **MEV-Boost blocks**:

- The median MEV-Boost block typically uses 15 million gas (18 million since the recent gas limit increase to 36 million), aligning closely with the EIP-1559 target.
- In contrast, the median locally built block consumes only 5-10 million gas.

> This suggests that blocks from local builders may temporarily reduce throughput. However this short-term effect is compensated over time with the basefee adjusting.

[![gas-used-over-time](https://ethresear.ch/uploads/default/original/3X/5/0/502dec3f976bd4ddc40dabfc712a1078bcf34f22.png)gas-used-over-time700×500 31.6 KB](https://ethresear.ch/uploads/default/502dec3f976bd4ddc40dabfc712a1078bcf34f22)

> This is not a new observation—it has already been documented by dataalways earlier this year.

Looking at **gas usage across consecutive block-building combinations** provides insight:

- Local builders following another local builder’s block get close to the 14.55 million gas target.
- Local builders following an MEV-Boost builder’s block fill only 7.11 million gas on average.
- MEV-Boost builders following a local builder use significantly more gas.

[![gas-over-block-combos (1)](https://ethresear.ch/uploads/default/optimized/3X/c/2/c2d6d0de41479e5f88a13e81b418290737237e1f_2_690x276.png)gas-over-block-combos (1)1000×400 23.2 KB](https://ethresear.ch/uploads/default/c2d6d0de41479e5f88a13e81b418290737237e1f)

### Timing Games and Block Propagation

MEV-Boost builders, with relay support, frequently engage in timing games ([as detailed here](https://timing.pics/)), potentially delaying block propagation by up to **3 seconds** (~25% of the slot). This delay can impact the next proposer’s ability to include transactions, reducing their gas utilization.

The chart below illustrates **gas usage in block n + 1** based on the **block seen time of the previous block n**. Once again, we observe that **local builders following MEV-Boost builder** blocks come with **around 7 million gas**.

[![gas-used-over-time-prev-slot (3)](https://ethresear.ch/uploads/default/optimized/3X/1/6/160fd85ef8c781b3b2fe3066b0c38ed27dd40b8b_2_690x276.png)gas-used-over-time-prev-slot (3)1000×400 41.1 KB](https://ethresear.ch/uploads/default/160fd85ef8c781b3b2fe3066b0c38ed27dd40b8b)

- As the block seen time of the previous block increases, gas usage in the next block decreases.
- Local builders following a MEV-Boost block typically fill only ~7 million gas.

At 1 second into the slot, gas usage is around 7 million; by 3.5 seconds, it drops to ~5 million.

### Economic Perspective

Priority fees contribute **only ~3% of a local builder’s revenue** annually ([see this analysis](https://ethresear.ch/t/is-it-worth-using-mev-boost/19753)), a figure that declines as the **public mempool shrinks**.

Yet, certain transactions remain **non-extractable**, including:

- Simple ETH or token transfers
- Smart contract deployments
- Transactions from privacy apps like Railway or Tornado Cash
- etc.

> From both UX and CR perspectives, the public mempool remains essential.
> Local builders are already sacrificing a significant amount of additional revenue on the EL side and might be happy with the CL side of rewards, so handling fewer transactions might not place much additional burden on them.

## The Future of Local Builders

### Are Local Builders Essential for Censorship Resistance?

The assumption that **local builders are critical for CR** is worth questioning.

> Local builders naturally order transactions by priority fees and are unlikely to modify their client software for censorship.

However, the **MEV-Boost market already incentivizes anti-censorship behaviors**:

- If a widely used app becomes a censorship target, compliant builders would have to sacrifice the MEV profits extractable from that app’s transactions. To stay competitive with non-censoring builders, they have a strong incentive to avoid censorship and find ways to bypass restrictions.
- If a less frequently used app faces censorship, smaller builders can accumulate a queue of transactions that censoring builders refuse to include. Once the queued transactions offer sufficient priority fees, non-censoring builders can outbid censoring ones, ensuring eventual inclusion.

### Case Study: Tornado Cash

Tornado Cash transactions, subject to censorship, [saw increased inclusion delays](https://x.com/nero_eth/status/1889748822735175978). However, small builders, despite their lower market share, **accumulated and batched these transactions to secure inclusion**.

The following chart distinguishes between Local Builders and MEV-Boost Builders. Local builders account for approximately 8–10% of the network. Over the past year, they included the second-most Tornado Cash transactions, yet the lower chart shows local builders had a relatively low inclusion rate per block. Small builders with a relatively low market share appear to have picked up TC transactions to batch-include them, helping them win the block auction.

[![tc-inclusion-rates](https://ethresear.ch/uploads/default/optimized/3X/c/f/cf9fee167ae30dadbf2da76d69659318b0545d55_2_583x500.png)tc-inclusion-rates700×600 31.2 KB](https://ethresear.ch/uploads/default/cf9fee167ae30dadbf2da76d69659318b0545d55)

Even without local builders, sanctioned transactions would still reach the chain, suggesting that some weak form of **a censorship-resistant mechanism can persist without them**. We might see increased inclusion times, but the final impact depends on the user/app being censored.

### What about Liveness?

Liveness is a different matter. Without a permissionless way for local builders to submit bids directly to themselves, bypassing relays that could censor them, Ethereum can’t guarantee liveness.

If local builders can transition in a **trustless and permissionless** manner **without relying on relays**, then **their role as local block builders diminishes**.

## Replies

**Julian** (2025-03-27):

Hey! Thanks for the analysis.

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Even without local builders, sanctioned transactions would still reach the chain, suggesting that some weak form of a censorship-resistant mechanism can persist without them. We might see increased inclusion times, but the final impact depends on the user/app being censored.

Just pointing out that with FOCIL, local block building takes a very different role,which might mean that censored applications that are not economically meaningful may still see short inclusion times.

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> This discrepancy suggests that whenever a local builder produces a block, Ethereum may be sacrificing potential throughput.

By EIP-1559, the throughput is decided as a system-level property, so Ethereum will have the 18M gas that is the current target as throughput. In that sense, Ethereum does not sacrifice throughput by using local builders. It can mean that the throughput is less efficiently allocated, as the base fee does not resemble the actual network congestion, as it is supposed to do.

---

**Nero_eth** (2025-03-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Just pointing out that with FOCIL, local block building takes a very different role,which might mean that censored applications that are not economically meaningful may still see short inclusion times.

Yeah, I agree — the whole topic is just more complex than it seems, with many factors at play. For example:

- The application: Are there many or few transactions? Are users willing to pay high priority fees?
- The CR mechanism: This can range from weaker setups, like MEV-Boost auctions, to stronger approaches, like unconditional inclusion lists (ILs) with severe missed-slot penalties and ILs carrying over to the next slot. FOCIL sits somewhere in between, leaning more toward the strong side.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> It can mean that the throughput is less efficiently allocated

Yeah agree, this is a better way to describe it. And as shown in the bar chart above, we do see that blocks built on top of blocks of local builders tend to be *fuller*. This could be at least partially due to a decreasing base fee, which allows more transactions to be included.

