---
source: ethresearch
topic_id: 20190
title: Preconfirmation Bidding Increased Block Values on Holesky
author: Evan-Kim2028
date: "2024-08-01"
category: Data Science
tags: [preconfirmations]
url: https://ethresear.ch/t/preconfirmation-bidding-increased-block-values-on-holesky/20190
views: 2865
likes: 11
posts_count: 10
---

# Preconfirmation Bidding Increased Block Values on Holesky

# TLDR

- Since July 10, mev-commit 0.4.3 has enabled over 800 execution preconfirmations on Holesky, with increasing network participation.
- Providers issued 807 preconfirmations across 415 blocks. Bidders sent 4.24 ETH worth of bids.
- Average mev-commit block value was 0.0093 ETH compared to 0.0044 ETH for a vanilla block.
- Average total preconfirmation bids per mev-commit block was 0.0049 ETH, slightly higher than the average priority fees in the mev-commit block of 0.0045 ETH.
- Data shows that preconf bids contribute significantly to overall block value, despite limited participation for the nascent network.

# Overview

Since July 10, mev-commit 0.4.3 has been facilitating execution preconfirmations on Holesky tesnet. There has been an upwards trend of participation with currently 1 relay, 3 providers, 9 bidders, and [27,000 validators](https://validators.mev-commit.xyz/) participating. From July 10 to July 29 (Holesky block range 1902173 to 2027932), providers have issued 807 preconfirmations across 415 Holesky blocks. Some examples of preconfirmation blocks:

- 1943039 with 21 preconfs and .016 ETH worth of bids
- 1986732 with 7 preconfs and .04 ETH worth of bids
- 1986963 with 5 preconfs and .022 ETH worth of bids

There are two caveats to these initial results. The first is that network participation is still growing. As more actors onboard or opt in to the network, the flow of preconfs is likely to increase. The second caveat is that Holesky does not have the same competitive use cases for preconfs as mainnet, and does not mirror mainnet Ethereum transacting behavior as closely as desired.

The notebook used for analytics [can be found here](https://github.com/Evan-Kim2028/preconf_analytics/blob/e6fdb9886c600315d531b59cb13e6efccc7d56bd/notebooks/preconfs.ipynb). The data for these results can be replicated using the [mev-commit-sdk-py](https://github.com/primev/mev_commit_sdk_py) repository to collect mev-commit events powered by Hypersync indexer. There is also [an explorer](http://explorer.testnet.mev-commit.xyz/app/discover), which is currently in development.

# Bidding Behavior

We observe 815 preconfirmation transactions, indicating a niche but valuable market segment compared to 4 million regular transactions. This significant difference suggests preconfs are currently used by a smaller subset of users who are testing preconfirmations.

A total of 9 bidders participated, sending 4.24 ETH in bids compared to 0.13 ETH in priority fees, with an average preconfirmation bid of 0.005 ETH versus 0.00016 ETH for priority fees on the same transaction, indicating a heavier bidding preference for preconfirmations over priority fees.

[![image](https://ethresear.ch/uploads/default/optimized/3X/0/4/04d6296e99153e73f2e018b8c21b727582d0c89e_2_563x500.png)image589×523 38.2 KB](https://ethresear.ch/uploads/default/04d6296e99153e73f2e018b8c21b727582d0c89e)

Overall, priority fees totaled 544 ETH with the average preconfirmation bid being 0.0049 ETH, slightly higher than the average priority fee of 0.0045 ETH.

# Block Value

We hypothesized that preconfs would add an increase in block value, resulting in higher validator rewards per mev-commit block. On average, we observe 1.95 preconfirmation transactions per block compared to 42.3 total transactions. Average mev-commit block value was 0.0093 ETH compared to 0.0044 ETH for a vanilla block.

[![image](https://ethresear.ch/uploads/default/original/3X/d/9/d97a557eefe85c83cef80122c55b8695d60307b1.png)image542×474 14.5 KB](https://ethresear.ch/uploads/default/d97a557eefe85c83cef80122c55b8695d60307b1)

One limitation in comparing mev-commit blocks to vanilla Holesky blocks is that there are only ~400 mev-commit blocks compared to ~50,000 Holesky blocks. This is primarily due to the nascent mev-commit network participation rates. Additionally the average bid amount at 0.005 ETH seems on the higher side for Holesky blocks and may not accurately reflect mainnet amounts. However accurately pricing preconfirmations is a difficult task and has to be balanced with the presence of mev spikes on mainnet that can greatly skew results. We are actively researching how to price preconfirmations more effectively.

We illustrate the block revenue breakdown over several days in the chart below for mev-commit blocks, showing the breakdown between preconfirmation bids and priority fees:

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/0/c04ec97bff2be44d3e1f79915157487def6eb685_2_690x409.png)image941×559 38.3 KB](https://ethresear.ch/uploads/default/c04ec97bff2be44d3e1f79915157487def6eb685)

Preconfirmation bids significantly contributed to increasing block value. On days such as July 11th, 18th, and 24th, preconfirmation bids markedly boosted total block value, highlighting their substantial impact.

The charts below illustrate an outsized impact that preconfirmation bids on block value:

- Preconf Bids per Block: Despite a smaller number of transactions, preconfirmation bids are consistently higher, often reaching up to 0.02 ETH.
- Priority Fees per Block: While more frequent, priority fees are generally lower, seldom exceeding 0.01 ETH.

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/3/43fe06dfdd10788ec3344bc9e8592e3773cf34a6_2_690x312.png)image891×404 36.2 KB](https://ethresear.ch/uploads/default/43fe06dfdd10788ec3344bc9e8592e3773cf34a6)

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/0/1078d70fc113dfd6d3a0d5a291ef56a81a12f361_2_690x317.png)image890×409 34.7 KB](https://ethresear.ch/uploads/default/1078d70fc113dfd6d3a0d5a291ef56a81a12f361)

A notable example is block [1943039](https://holesky.etherscan.io/block/1943039), which had the highest number of preconfs with 21 out of 48 transactions. In this block, preconf bid revenue was 0.008 ETH, vastly outpacing the 0.0009 ETH from priority fees.

These observations demonstrate that even a few preconfirmation transactions can substantially enhance block value due to their higher bid amounts.

# Limitations

As mentioned earlier, the caveats to our initial findings is that Holesky is a testnet and does not have the same types of competitive opportunities as Mainnet. Users tend to have less urgency on Holesky and this is reflected in smaller block sizes and lower priority fees.

As a result, the preconf bids may not have the same relationship to priority fees on mainnet compared to testnet and may not accurately reflect the user’s true bidding preferences since testnet tokens are being used.

# Closing Remarks

This report initially touches on some preconfirmation bidding behavior observed through early mev-commit usage and offers insights into how preconf bids can increase validator rewards. We plan to follow up with a more detailed report on mev-commit protocol details such as the decay mechanism, rewards and slashing, settlement process, and revenue.

We plan to onboard more bidders, providers and validators into the mev-commit ecosystem and conduct more tests in an environment that mimics mainnet more closely. We invite you to participate starting at [Page Not Found](https://docs.primev.xyz/get-started/welcome-to-primev)

## Replies

**Julian** (2024-08-01):

Thanks for the write-up. It’s cool to see preconfs being implemented! I was wondering if you could touch upon the counterfactual of non-mev-commit blocks since the market looks uncompetitive. You mention that the average priority fee is 0.0045 ETH, and a block contains, on average, 42.3 transactions. This would imply an average block value of around 0.0045 ETH * 42.3, yet you see an average non-mev-commit block value of 0.0044 ETH. Could you explain how this is possible and how it affects your results?

---

**Evan-Kim2028** (2024-08-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> You mention that the average priority fee is 0.0045 ETH, and a block contains, on average, 42.3 transactions. This would imply an average block value of around 0.0045 ETH * 42.3, yet you see an average non-mev-commit block value of 0.0044 ETH. Could you explain how this is possible and how it affects your results?

the statement `Average preconfirmation bid was 0.0049 ETH, slightly higher than the average priority fee of 0.0045 ETH.` refers to average total block value breakdown. So  0.0049 ETH would refer to the average value of bids received in a block and 0.0045 ETH refers to the average value of priority fees received in a vanilla block.

The calculation would then be 0.0045 / 42.3 = ~0.000106 ETH priority fee per tx instead of a multiplication, similar to the average number in the Bidding Behavior section. To see the difference visually, you can look at the Preconf Bids vs Priority Fees box plot as well.

sorry the wording was ambiguous on my part. I will change it to make it more clear

---

**cwhcheng** (2024-08-02):

Thanks for the article! If i read it correctly from the doc, providers in the mev ecosystem include Block Builders, Relays and Proposers so I am curious to know why there are only 3 providers when there are 27,000 validators.

---

**Evan-Kim2028** (2024-08-02):

As noted in the post, we just started seeing preconfirmation activity on July 10th, which is less than a month ago. We are in the process of adding more providers, relayers, AND validators into the ecosystem.

---

**murat** (2024-08-04):

Providers are block builders in this case, no relays or validators have joined as providers making their own preconfirmation decisioning. The current version of the protocol is for execution preconfirmations which are difficult for those entities to provide, we may see them adopt other use cases in the future. We’ll update the wording on the documentation to reflect that providers *may be* those entities, thanks for pointing that out

---

**cwhcheng** (2024-08-05):

thanks for the clarification! But why only focus on execution preconf instead of inclusion preconf?

---

**r4f4ss** (2024-08-08):

Nice to see this idea evolving in testnet, thanks!

Can you please clarify why priority fees are being compared to preconf bids? As far as i know they are uncorrelated, priority fees are for searchers to have bundles included. Is it possible that one replace another?

---

**Evan-Kim2028** (2024-08-08):

execution preconfs already imply inclusion

---

**Evan-Kim2028** (2024-08-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/r4f4ss/48/17060_2.png) r4f4ss:

> Can you please clarify why priority fees are being compared to preconf bids? As far as i know they are uncorrelated, priority fees are for searchers to have bundles included. Is it possible that one replace another?

We expect that they will be interchangeable. Priority fees are used to bid for block inclusion rates. A preconfirmation is a type of guarantee for faster block inclusion as well. Note one major difference is that mev-commit preconfirmation bids have a linear decay function (think dutch auction) to incentivize faster inclusion acceptance.

