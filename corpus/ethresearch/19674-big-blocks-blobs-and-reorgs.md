---
source: ethresearch
topic_id: 19674
title: Big blocks, blobs, and reorgs
author: Nero_eth
date: "2024-05-29"
category: Sharding
tags: [data-availability, scaling]
url: https://ethresear.ch/t/big-blocks-blobs-and-reorgs/19674
views: 5975
likes: 16
posts_count: 7
---

# Big blocks, blobs, and reorgs

# Big blocks, blobs, and reorgs

With [EIP-4844](https://www.eip4844.com/) going live, Ethereum effectively increased its transaction throughput by providing dedicated space for rollups to post their data down to L1.

Blobs are now the main contributor to the block size, while the average beacon block size (excluding blobs) went down from ~125 KB to ~90 KB.

**In the chart below, one can see the impact of blobs on the data throughput of Ethereum:**

[![block_content_over_time](https://ethresear.ch/uploads/default/original/3X/9/9/992968f3269c56752a8fc1ce4805ff35f91c1f03.png)block_content_over_time700×400 16.7 KB](https://ethresear.ch/uploads/default/992968f3269c56752a8fc1ce4805ff35f91c1f03)

Such an increase in throughput is expected to push certain “weaker” validators to their limits. Thus, we want to answer the question “*Do blobs contribute to reorgs and if so, by how much?*”

For the following analysis, I’m relying on a node to parse data in real-time (head of chain) and check the contents of blocks that were eventually reorged.

**The earliest data point considered for the following analysis is slot 8,992,385 (May 3, 2024), which gives us around 4 weeks of data.**

**In total, we observe 487 reorgs and a total of ~184,000 slots in this time span.**

### Snappy compressed blocks

First, let’s compare the **snappy compressed block size of blocks** that were reorged vs those that made it into the canonical chain.

In particular, we’re interested in whether reorged blocks were on average larger than those that weren’t reorged.

*In this context, we’re referring to reorgs as valid blocks that the respective proposer proposed but that were eventually orphaned by consecutive proposers.*

[![boxplot2](https://ethresear.ch/uploads/default/optimized/3X/6/5/65e2f3539a7b27774ccc3e9027f94040b7a393ac_2_690x229.png)boxplot21200×400 18.7 KB](https://ethresear.ch/uploads/default/65e2f3539a7b27774ccc3e9027f94040b7a393ac)

Based on the above graph, we **cannot** see a significant difference in the median block size of reorged and not-reorged blocks. Focusing on the 75\% quantile and the upper whiskers which are defined as Q_{75} \times 1.5\ IQR, we do see reorged blocks being larger than not reorged ones. This was expected (bigger blocks lead to bigger struggles), however, as visible in this [earlier analysis](https://ethresear.ch/t/on-increasing-the-block-gas-limit/18567) on block sizes, the effects were reduced with 4844 going live.

### Blobs

Next, let’s look into blobs. With the go-live of EIP-4844, most rollups switched from using calldata to blobs, shifting the majority of posted data from the EL payload to blobs.

[![boxplot3](https://ethresear.ch/uploads/default/optimized/3X/d/c/dcb946af5f97726ad19040528abaff69748f11e8_2_690x229.png)boxplot31200×400 13.5 KB](https://ethresear.ch/uploads/default/dcb946af5f97726ad19040528abaff69748f11e8)

Based on the above boxplots, we can see that most **reorged** blocks contained 6 blobs. Seeing more reorgs for blocks with 6 blobs is kind of expected as those blocks were approximately **7 times larger than the average block pre-4844**.

**The same pattern is evident when visualizing the percentage of reorged blocks over the number of blobs per block.**

[![reorgrate_over_blobs](https://ethresear.ch/uploads/default/optimized/3X/3/2/32857ee973ca2a11247e2f25384b6b45b2b6be2e_2_690x301.png)reorgrate_over_blobs800×350 11.9 KB](https://ethresear.ch/uploads/default/32857ee973ca2a11247e2f25384b6b45b2b6be2e)

Comparing the percentage of reorged blocks with 0 and 6 blobs, we can see that the probability of a reorg is more than **3 times larger.**

In this context, it’s important to check what the distribution of blobs per block looks like. The “extreme” cases of 0 or 6 blobs per block might heavily impact the perceived impact of blobs on reorgs.

[![blobs_per_block_ist](https://ethresear.ch/uploads/default/optimized/3X/7/8/78cfeeac384e4d699dd3776ba954dd95dffbda24_2_690x265.png)blobs_per_block_ist1300×500 15.4 KB](https://ethresear.ch/uploads/default/78cfeeac384e4d699dd3776ba954dd95dffbda24)

As visible in the above histogram, which shows the distribution of blobs per block in May 2024, most blocks contained either 0 or 6 blobs.

### Regression Analysis

To quantify the impact of blobs on reorgs, we can apply a simple logistic regression.

In addition to the (1) uncompressed block size, (2) snappy compressed block size, (3) gas used per block and (4) number of transactions and (5) blobs per block, we also put different CL clients as dummy variables into the regression model.

All dependent variables are z-score scaled and the Lighthouse client is part of the intercept.

[![logit](https://ethresear.ch/uploads/default/original/3X/5/2/5270b626e19b685b050d293245984a8e0700ba11.png)logit745×398 21 KB](https://ethresear.ch/uploads/default/5270b626e19b685b050d293245984a8e0700ba11)

Looking at the intercept (const), the baseline log-odds of a reorg when all other predictors are at their mean indicates a very low baseline probability of a reorg happening.

To put that in numbers, empirically around 0.27\% of all blocks in May 2024 were reorged.

Next, let’s focus on the dependent variables, considering p \le 0.01 as a significant result.

**Blobs**, **size_compressed**, and **nr_txs** have significant impacts on the probability of a reorg.

- Each additional blob and each additional byte in size_compressed increases the probability of a reorg.
- size, gas_used and other client variables (Nimbus, Prysm) do not have significant impacts (compared to the Lighthouse client).

For each increase in blobs by the standard deviation of blobs (=2.33), the log-odds of a block being reorged increase by 1.2582.

The baseline probability of a reorg, with all dependent variables at their mean, is approximately 0.27\%. This would mean that an increase in blobs by one standard deviation (=2.33) results in the probability of a reorg increasing from approximately 0.27\% to 0.93\%, representing an increase of about 0.67 percentage points.

### Clients

**Notably, the number of reorgs is in general very low and even lower for “minority” clients such as Lodestar and Teku. Thus a few Lodestar or Teku users that are playing timing games could already impact this result.**

**Thus, the following result must be taken with a grain of salt.**

**For the Lodestar client:**

- The log-odds of a reorg increase by 0.9814 when using the Lodestar client.
- This corresponds to an odds ratio of approximately 2.667, indicating that the odds of a reorg are about 166.7\% higher when using the Lodestar client.
- The baseline probability of a reorg is approximately 0.27\%. When using the Lodestar client, this probability increases to approximately 0.45\%, an increase of about 0.178 percentage points.

**For the Teku client:**

- The log-odds of a reorg increase by 0.5629 when using the Teku client.
- This corresponds to an odds ratio of approximately 1.756, indicating that the odds of a reorg are about 75.6\% higher when using the Teku client.
- The baseline probability of a reorg is approximately 0.27\%. When using the Teku client, this probability increases to approximately 0.3\%, an increase of about 0.027 percentage points.

For the **Nimbus** and **Prysm** clients, we do not see a significant impact on reorgs compared to **Lighthouse**.

## Next Steps

- Call for reproduction: Please reproduce my analysis. Working with a lot of data can be dirty. Working with data that disappears from the chain after a block was reorged is even dirtier. Thus, view this as an initial attempt to dive into the “blobs vs reorgs” topic.
- More data: 4844 is still very young and I plan to reproduce this analysis in a few months to verify the results using more data.
- Filter for client bugs: A small bug in a client can significantly impact the result. Same applies to validators playing timing games, honest reorg strategies, and EL clients.
- What about relays and builders: Check why we see either 0 or 6 blobs, the extreme cases, so often, and what the builder and relay behavior is in those scenarios.
- Check how efficiently blobs are used and if sharing blob space among multiple entities could increase efficiency.

## Replies

**jonastheis** (2024-06-12):

That’s a great analysis, thanks!

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> In total, we observe 487487487 reorgs and a total of ~184,000184,000184,000 slots in this time span.

What is the depth of the observed reorgs?

Following up on this thought, it would be very interesting to analyze the severity of reorgs  depending on the block size/contained blobs.

---

**dankrad** (2024-06-15):

Great analysis! I think what would be the most interesting to understand when the blocks that are reorged were sent. For a rational player, 0.6% does not sound like an excessive rate of loss for blocks if playing MEV timing games. However, if it’s mainly home stackers and/or self builders, then it could potentially be more problematic.

---

**dapplion** (2024-06-17):

> Such an increase in throughput is expected to push certain “weaker” validators to their limits

Re-org rates are not a good proxy for that measure. Weaker validators (say some solo stakers) represent a minority of stake. Blocks won’t be re-orged but those weaker validators will cast incorrect head votes, reducing their attestating rewards.

It would be a great follow-up to correlate block+blob size with head participation, or more granularly correlate solo staker head vote correctness with block+blob size

---

**wanify** (2024-06-23):

Thank you for the insightful post! I tried to reproduce your analysis using my local node and obtained almost the same results, except that my results showed a lower reorg rate for blocks containing 5 blobs compared to your results.

(From slot 8,800,000~ 9,238,231, # of forked blocks = 1,040)

[![Screenshot 2024-06-23 at 9.40.25 PM](https://ethresear.ch/uploads/default/optimized/3X/4/d/4d61d38025193d7464faacb2bbfcf73ffb65e2bc_2_517x246.png)Screenshot 2024-06-23 at 9.40.25 PM2008×956 61.1 KB](https://ethresear.ch/uploads/default/4d61d38025193d7464faacb2bbfcf73ffb65e2bc)

[![Screenshot 2024-06-23 at 9.46.17 PM](https://ethresear.ch/uploads/default/optimized/3X/7/b/7b59dab995776d765b6aa2d24a937da24e7b7c68_2_345x217.png)Screenshot 2024-06-23 at 9.46.17 PM1732×1090 63.5 KB](https://ethresear.ch/uploads/default/7b59dab995776d765b6aa2d24a937da24e7b7c68)

---

**pop** (2024-10-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> boxplot31200×400 13.5 KB

From this plot, do you think the current blob count target and limit are the highest we can go now, or we can go further, or no opinion on this?

---

**Nero_eth** (2024-10-29):

Always difficult to pinpoint down the reasons for a reorg to only one factor.

There are many influences like timing games, the el payload size, the slot index in the epoch, etc. that significantly impact the likelihood of reorgs.

Furthermore, the situation improved by a lot since then and today, months after shipping 4844, we got reorgs down to a level not seen for years.

So, yeah, with making sure that we also limit the EL payload size (EIP-7623), I think we are ready for more blobs, assuming other network-level optimizations in place.

