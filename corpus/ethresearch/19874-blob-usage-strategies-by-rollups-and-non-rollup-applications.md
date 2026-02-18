---
source: ethresearch
topic_id: 19874
title: Blob Usage Strategies by Rollups and Non-rollup Applications
author: doublespending
date: "2024-06-20"
category: Data Science
tags: [data-availability, rollup]
url: https://ethresear.ch/t/blob-usage-strategies-by-rollups-and-non-rollup-applications/19874
views: 3647
likes: 5
posts_count: 3
---

# Blob Usage Strategies by Rollups and Non-rollup Applications

[Full Report](https://0xpantarhei.substack.com/p/blob-usage-strategies)

## TDLR

1. The main applications using blobs are rollups, accounting for approximately 87%. Non-rollup applications mainly include Blobscriptions and customized type 3 transactions.
2. Rollup applications choose different blob usage strategies according to their own situations. The strategies will consider the number of blobs carried by type 3 transactions, blob utilization, and blob submission frequency to balance the costs of availability data fees and delay costs.
3. Non-rollup applications can be characterized and distinguished from rollup applications by the number of blobs carried by type 3 transactions, blob utilization, and blob submission frequency. These features help identify scenarios of blob abuse, allowing for the design of corresponding anti-abuse mechanisms.
4. In most cases, using blobs as a data availability solution is more cost-effective than calldata. However, there are a few scenarios where calldata is cheaper: blob gas price spikes and blob utilization is extremely low.
5. Short-term fluctuations in blob gas price is mainly influenced by the demand from non-rollup applications. Rollup applications have a relatively inelastic demand for blobs, so they do not significantly impact short-term fluctuations in blob gas prices.
6. Currently, rollup applications do not seem to consider blob gas price as a reference factor in their blob usage strategies.
7. The probability of blocks containing type 3 transactions being reorganized is extremely low. Additionally, carrying more blobs does not increase the probability of block reorganization. However, there is a clustering phenomenon in block height for blocks containing type 3 transactions.

## Introduction

This report provides an in-depth analysis of type 3 transactions used for carrying blobs from the time of the Ethereum Decun upgrade until May 22, 2024. It focuses on blob usage strategies of rollup and non-rollup applications. The dataset, data processing programs, and visualization code for this report are [open source](https://github.com/doublespending/EIP-4844-Data-Analysis), detailed in the following “Dataset” section.

## Type 3 Transactions & Blobs Share by Applications

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/1/9101b16c984217aa1e5a51a59e7c0024aa6e8e18_2_690x363.jpeg)image1462×770 137 KB](https://ethresear.ch/uploads/default/9101b16c984217aa1e5a51a59e7c0024aa6e8e18)

### Rollup Applications

Observations from Figure 1 on the proportion of type 3 transactions:

- Base, Scroll, Linea, and Starknet are in the same tier, having the highest transaction proportions.
- Arbitrum, Optimism, and Zksync are in the next tier, having the second-highest transaction proportions.

This phenomenon seems counterintuitive as Arbitrum and Optimism have higher TPS than Scroll, Linea, and Starknet and should have a higher proportion of type 3 transactions.

Figure 2 shows that counterintuitive phenomenon is caused by different rollup strategies in the number of blobs carried by type 3 transactions.

Observations from Figure 2 on the proportion of blobs:

- Base stands alone, having the highest proportion of blobs.
- Arbitrum and Optimism are in the same tier, having the second-highest proportion of blobs.
- Scroll, Linea, Starknet, and Zksync are in the same tier, having a medium proportion of blobs.

This phenomenon aligns more with intuition: blob proportions are directly related to the scale of rollup’s availability data, thus showing a positive correlation with rollup TPS.

The difference between the proportion of type 3 transactions (31%) and blobs (14%) for non-rollup applications indicates that non-rollup applications and rollup applications have different needs.

### Non-Rollup Applications

- Rollup applications are B2B businesses aiming to fill fine-grained Layer 2 transaction availability data, so their type 3 transactions are not limited to carrying only 1 blob.
- Non-rollup applications are B2C businesses aiming to upload complete text, images, etc., so their type 3 transactions usually carry only 1 blob to meet their needs.

## Rollup Blob Usage Strategies

### Rollup Strategy Model

This section models the rollup blob usage strategies with

1. blobNumber, i.e. the number of blobs carried by type 3 transactions
2. blobUtilization, i.e. blob space utilization
3. blobInterval, i.e. the blob submission interval

#### Fee Cost

The fee cost per transaction for rollups is expressed as:

\begin{equation}
feeCost = \frac{1}{k}(\frac{blobCost}{blobUtilization}+\frac{fixedCost}{blobNumber*blobUtilization})
\end{equation}

- fixedCost: the fixed cost of a type 3 transaction
- blobCost: the cost of a single blob
- The larger the blobUtilization, the lower the amortized cost of the blob fee \frac{blobCost}{blobUtilization} and the fixed cost \frac{fixedCost}{blobNumber*blobUtilization}, resulting in a lower fee cost feeCost.
- The larger the blobNumber, the lower the amortized cost of the fixed cost \frac{fixedCost}{blobNumber*blobUtilization}, resulting in a lower fee cost feeCost.

#### Delay Cost

**The delay cost per transaction for rollups is expressed as:**

\begin{equation}
delayCost = F(\frac{blobNumber*blobUtilization*k}{tps})
\end{equation}

- The larger the blobUtilization, the larger the delay cost delayCost.
- The larger the blobNumber, the larger the delay cost delayCost.
- The larger the tps, the smaller the delay cost delayCost.

> The derivation of the formula can be found in the full version.

### Rollup Strategy Analysis

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/c/cc978c93e42157bd63c06de9c0637fc887dccced_2_690x260.png)image2366×894 374 KB](https://ethresear.ch/uploads/default/cc978c93e42157bd63c06de9c0637fc887dccced)

[![image](https://ethresear.ch/uploads/default/optimized/3X/3/2/32521830fd7aab2cbd7f19d504720344afb2eff7_2_574x499.jpeg)image1272×1108 138 KB](https://ethresear.ch/uploads/default/32521830fd7aab2cbd7f19d504720344afb2eff7)

### Non-Rollup Blob Strategies

Rollup applications are B2B, while non-rollup applications are B2C. Therefore, non-rollup applications differ from the rollup strategy model. For non-rollup applications:

- The number of blobs carried by type 3 transactions depends on the size of the content (texts/images) stored in the blobs.
- Blob utilization depends on the size of the content (texts/images) stored in the blobs.
- Blob submission intervals depend on the immediate needs of C-end users, with no delay costs involved.

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/c/cc978c93e42157bd63c06de9c0637fc887dccced_2_690x260.png)image2366×894 374 KB](https://ethresear.ch/uploads/default/cc978c93e42157bd63c06de9c0637fc887dccced)

- According to Figure 5 (Others ), 1 blob can meet the needs of most non-rollup applications.
- According to Figure 6 (Others ), the blob utilization is concentrated between 20% and 40%, indicating that non-rollup applications generally cannot fill the blob, with the data size mainly between 25.6 kB and 51.2 kB.
- According to Figure 7 (Others ), about 83% of blobs have a submission interval of less than 1 minute, indicating a relative high frequency of user demand for non-rollup applications.

In summary, the type 3 transactions for non-rollup applications can be characterized as: **high-frequency transactions carrying 1 low-utilization blob** .

The essence of this characterization is that non-rollup applications are driven by immediate needs and are less concerned about the fee cost per data byte compared to rollup applications.

This characterization allows for the identification of non-rollup applications, which in turn helps design mechanisms to limit blob abuse by non-rollup applications.

## Is Using Blobs Always More Cost-effective than Calldata?

Introducing `feeRatio` to measure the relative advantages of the two solutions:

\begin{equation}
feeRatio = \frac{calldataFeeCost }{blobFeeCost}
\end{equation}

- When feeRatio ≥ 1, it indicates that using blobs as a data availability solution is not worse than calldata.
- When feeRatio
A few in Metal rollup:

- Rollup application Metal seems not to have considered switching between blobs and calldata in its strategy, leading to suboptimal choices in some extreme cases.
- Extreme cases are mainly due to Metal’s low blob utilization (see Figure 6) coinciding with a spike in blob gas prices.
- However, given that extreme scenarios are rare and maintaining two data availability solutions is costly, Metal’s suboptimal strategy in extreme cases seems acceptable.

> The analysis of blob and calldata solutions in this section only considers fee costs and not delay costs. Considering delay costs, calldata has an actual advantage.

## Blob Gas Price and Blob Usage Strategies

### Analysis of Blob Gas Price Fluctuations

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/8/58dd45e0e206936eb5eb2b32fc343a70322254c1_2_690x363.jpeg)image1456×768 160 KB](https://ethresear.ch/uploads/default/58dd45e0e206936eb5eb2b32fc343a70322254c1)

Figures 9 and 10 show that in scenarios of high blob gas prices (> 10), the proportion of non-rollup applications (**Others**) is significantly higher than in scenarios of low blob gas prices (< 10).

Therefore, it can be concluded that the surge in blob gas prices is mainly driven by the demand from non-rollup applications, rather than rollup applications. Otherwise, the proportion of rollup and non-rollup applications should remain stable.

### How Rollups Respond to Blob Gas Price Fluctuations

*Hypothesis 1: The higher the blob gas price, to reduce fee costs, applications should carry more blobs in type 3 transactions, i.e., the number of blobs should be positively correlated with blob gas prices.*

[![image](https://ethresear.ch/uploads/default/optimized/3X/f/b/fb34ad1ab0fcf6250662d82b007a763309889ef7_2_505x500.jpeg)image1520×1502 168 KB](https://ethresear.ch/uploads/default/fb34ad1ab0fcf6250662d82b007a763309889ef7)

Figure 14 shows that the hypothesis does not hold.

*Hypothesis 2: The higher the blob gas price, to reduce fee costs, applications should increase blob utilization, i.e., blob utilization should be positively correlated with blob gas prices.*

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/2/521bb465406b224d50b0117150169a5991c5029c_2_498x500.jpeg)image1432×1436 133 KB](https://ethresear.ch/uploads/default/521bb465406b224d50b0117150169a5991c5029c)

Figure 15 shows that the hypothesis does not hold.

*Hypothesis 3: The higher the blob gas price, to reduce fee costs, applications should delay blob submissions, i.e., blob submission intervals should be positively correlated with blob gas prices.*

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/e/9e1dd1bbb0bad1163b9eaf7f8d61f340279bb0fd_2_514x500.jpeg)image1538×1494 211 KB](https://ethresear.ch/uploads/default/9e1dd1bbb0bad1163b9eaf7f8d61f340279bb0fd)

Figure 16 shows that the hypothesis does not hold.

> In Figures 9 and 10, readers might notice that some rollup applications seem to respond to high blob gas prices. Scroll seems to suspend blob submissions under high blob gas prices. However, this conclusion is incorrect. The reason is that not all rollups immediately used blobs after the EIP-4844 upgrade.

## Blobs and Block Reorg

From the Decun upgrade to May 22, there were 171 type 3 transactions included in the forked blocks and 348,121 included in the canonical blocks. Therefore, the proportion of type 3 transactions being forked is approximately 0.049%. This section explores the relationship between block reorg and blob.

### Blob Number Distribution in the Canonical and Forked Blocks with Blobs

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/e/bef1c025b4ae7c6990e2c7968acf12a6eccba1a2_2_690x403.jpeg)image1462×854 105 KB](https://ethresear.ch/uploads/default/bef1c025b4ae7c6990e2c7968acf12a6eccba1a2)

*Hypothesis: More blobs increase the probability of block reorganizations.*

If the hypothesis holds, the following inequality should be satisfied:

\begin{equation}
P(reorg|blob=n)  > P(reorg|blob=n-1)
\end{equation}

According to [Bayes’ theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem), inequality above is equivalent to:

\begin{equation}
\frac{P(blob=n|reorg)}{P(blob=n)}  > \frac{P(blob=n-1|reorg)}{P(blob=n-1)}
\end{equation}

We check whether the actual data satisfies inequality and obtain the following table:

[![image](https://ethresear.ch/uploads/default/optimized/3X/e/c/ec253f7881bbf00cf3b5a37a8635dfb0181309ee_2_690x201.png)image1280×374 68.8 KB](https://ethresear.ch/uploads/default/ec253f7881bbf00cf3b5a37a8635dfb0181309ee)

The table above shows that equation (10) does not hold for all `n`. Therefore, the hypothesis does not hold, indicating that more blobs are not significantly related to block reorganizations.

### Distribution of Type 3 Transactions and Blobs by Applications in the Canonical and Forked Blocks with Blobs

[![image](https://ethresear.ch/uploads/default/optimized/3X/d/d/ddfc7f0d5d5b2a90aaf6efff87b6d7a3733c2aff_2_425x500.jpeg)image1512×1776 113 KB](https://ethresear.ch/uploads/default/ddfc7f0d5d5b2a90aaf6efff87b6d7a3733c2aff)

Figures 18 and 19 show that the proportion of type 3 transactions/blobs for Zksync and Scroll in forked blocks is significantly higher than in the canonical blocks.

Applications seem to have some connection with block reorganizations, possibly related to differences in blob usage strategies by applications:

- Zksync and Scroll are less strategic in selecting the timing of submitting type 3 transactions, targeting block heights prone to reorganization.
- The unique characteristics of Zksync and Scroll’s type 3 transactions make the blocks containing them more likely to be reorganized.

### Clustering Phenomenon of Forked Blocks with Blobs

[![image](https://ethresear.ch/uploads/default/optimized/3X/2/8/281e3d3c49f900b77406ef467f2c32a1b08331eb_2_690x286.jpeg)image1488×618 135 KB](https://ethresear.ch/uploads/default/281e3d3c49f900b77406ef467f2c32a1b08331eb)

If each block has the same probability of being reorganized, the forked blocks should be evenly distributed across the block height range. However, Figure 20 shows a clustering phenomenon in block heights for forked blocks, possibly related to network conditions.

In addition, the clustering phenomenon that occurs in block reorganization seems to be somewhat related to the applications that submit blobs. For example, type 3 transactions for non rollup applications are only included in forked blocks between 19500000 and 19600000.


      ![](https://ethresear.ch/uploads/default/original/3X/1/2/1205235ab66f774c2b06018c9a6e0a2ac1a43476.jpeg)

      [0xpantarhei.substack.com](https://0xpantarhei.substack.com/p/blob-usage-strategies)



    ![](https://ethresear.ch/uploads/default/optimized/3X/c/8/c8fddab9d0816ee9808a23d99c555dd37d094af1_2_690x345.jpeg)

###



This report provides an in-depth analysis of type 3 transactions used for carrying blobs.

## Replies

**Evan-Kim2028** (2024-06-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/doublespending/48/9960_2.png) doublespending:

> Figures 9 and 10 show that in scenarios of high blob gas prices (> 10), the proportion of non-rollup applications (Others) is significantly higher than in scenarios of low blob gas prices (< 10).

is this in gwei?

One particular outlier in high reorgs was around the last week of March - like March 27,28ish that caused a spike in missed slots/reorgs. Perhaps your clustering phenomenon could be related to that incident?



      [gist.github.com](https://gist.github.com/benhenryhunter/687299bcfe064674537dc9348d771e83)





####



##### gistfile1.md



```
On March 27-28 the Ethereum network suffered from extremely high rate of miss slots. Most of these slots were first relayed from the bloXroute relays. We identified that the bloXroute relays worked properly throughout the incident, publishing blocks and blobs correctly, however they propagated the blocks fast thru the BDN while the blobs sidecar propagated through the p2p more slowly (the sidecar is expected to propagate slower, and is allowed to be accepted until t=8 sec) this uncovered a specific CL behavior which caused clients to reject these blocks and cause missed slots. In the current Lighthouse version, the node is expecting the peer that first provided the block to also provide the blobs.  The BDN does not propagate blobs and that caused the BDN connected consensus nodes to ignore blocks that were first received from the BDN.   A recent release of the BDN improved the speed of gossiped blocks without blobs, relying on the rest of the p2p network to propagate blobs as needed which caused the significant increase of the missed slots. The BDN relies heavily on Lighthouse, which makes up the majority of our beacon nodes at bloXroute, due to its performance and speed.  Post release we witnessed successful block propagation through our BDN and made the assumption this release was valid.  This also showcased itself mainly on the bloXroute relays due to their tight coupling with the BDN.  The BDNs speed of providing the beacon nodes with the block caused this behavior even in scenarios where other relays were publishing blocks that bloXroute did not have.

Throughout this time the bloXroute relays were providing blocks with blobs back to validators and also publishing blocks with blobs to our BDN and to our network of beacon nodes.  These publish requests would return a 202 response due to the beacon nodes already seeing that block from the BDN.

This issue was able to be resolved after a series of tests were done isolating this issue to lighthouse’s behavior after seeing a block first through the BDN and then slowly migrating our relay away from using the BDN for block publishing and then disabling the BDN’s block propagation of any blocks containing blobs.
```










https://twitter.com/sproulM_/status/1773853486373130708

---

**doublespending** (2024-06-21):

> is this in gwei?

This is `wei` and blob base fee has been stay at 1 wei for a long time.

> Perhaps your clustering phenomenon could be related to that incident?

I think so. This also implies that reorg may not have much to do with blob, mainly related to some incident.

