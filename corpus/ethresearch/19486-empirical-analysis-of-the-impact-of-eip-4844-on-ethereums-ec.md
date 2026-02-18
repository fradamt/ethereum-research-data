---
source: ethresearch
topic_id: 19486
title: Empirical Analysis of the Impact of EIP-4844 on Ethereum's Ecosystem
author: wanify
date: "2024-05-07"
category: Economics
tags: []
url: https://ethresear.ch/t/empirical-analysis-of-the-impact-of-eip-4844-on-ethereums-ecosystem/19486
views: 4282
likes: 31
posts_count: 5
---

# Empirical Analysis of the Impact of EIP-4844 on Ethereum's Ecosystem

## Empirical Analysis of the EIP-4844’s Impact on Ethereum

*by [Seongwan Park](https://twitter.com/seongwan_eth), [Bosul Mun](https://twitter.com/1004YUKICHAN)*

Draft paper : [[2405.03183] Impact of EIP-4844 on Ethereum: Consensus Security, Ethereum Usage, Rollup Transaction Dynamics, and Blob Gas Fee Markets](https://arxiv.org/abs/2405.03183)

### Summary

On March 13, 2024, Ethereum implemented EIP-4844 to enhance its capabilities as a data availability layer. While this upgrade has successfully reduced [data posting costs](https://l2fees.info/) for rollups, it also introduces potential concerns regarding the consensus layer, particularly due to increased propagation sizes. Additionally, the broader impacts on the overall Ethereum ecosystem have not been thoroughly explored until now.

In our analysis, we’ve examined EIP-4844’s effects in terms of consensus security, Ethereum usage, rollup transaction dynamics, and the blob gas fee mechanism. Our study includes changes in synchronization times, detailed assessments of Ethereum usage, rollup activities, and insights into the blob gas fee mechanism. Our goal is to pinpoint both improvements and potential issues since the upgrade.

**Main Findings:**

1. Consensus Security

- Increase in fork rates, even excluding periods affected by client issues.
- Sync time has increased by approximately 140ms, from 2267.436ms to 2407.05ms.
- The most significant contributor to increased sync time is receive time, while blob propagation had minimal effects.

1. Ethereum Usage

- Marked increase in total data size posted by rollups (+116%).
- Significant reduction in total fees paid by rollups (-71%) and price per MiB for data availability (-82%).
- A substantial decrease in total gas used (-54%).

1. Rollup Transactions

- All six rollups studied (Arbitrum One, Optimism, Base, Starknet, zkSync Era, Linea) showed significant increases in transaction volume.
- User delay has notably increased in four of the rollups(except for Arbitrum One and zkSync Era), highlighting the need for blob sharing protocols.

1. Blob Gas Fee Market

- Small influence of the gas base fee on the blob gas base fee, with no reciprocal influence detected.
- Higher priority fees for blob transactions compared to non-blob transactions
- The blob gas fee market exhibits greater volatility than the gas fee market, yet it potentially reflects market demands more accurately.

**Figures**

[![Screenshot 2024-05-07 at 5.51.53 PM](https://ethresear.ch/uploads/default/optimized/3X/5/8/589586f7a2dd9e55913caf25215b3279929be1d3_2_345x204.png)Screenshot 2024-05-07 at 5.51.53 PM886×524 55.7 KB](https://ethresear.ch/uploads/default/589586f7a2dd9e55913caf25215b3279929be1d3)

[![Screenshot 2024-05-07 at 5.52.11 PM](https://ethresear.ch/uploads/default/optimized/3X/6/f/6fb1d284d34adcfa3b1b2f37dd60a1d882111787_2_345x226.png)Screenshot 2024-05-07 at 5.52.11 PM884×580 53.6 KB](https://ethresear.ch/uploads/default/6fb1d284d34adcfa3b1b2f37dd60a1d882111787)

[![Screenshot 2024-05-07 at 9.03.14 PM](https://ethresear.ch/uploads/default/optimized/3X/8/4/84bf36904da0af478a6813aee89ae47bd80b272d_2_393x374.jpeg)Screenshot 2024-05-07 at 9.03.14 PM1026×976 145 KB](https://ethresear.ch/uploads/default/84bf36904da0af478a6813aee89ae47bd80b272d)

[![스크린샷 2024-05-13 오후 7.47.01](https://ethresear.ch/uploads/default/optimized/3X/b/0/b0a06aed03cdbbe0c2df234e6a85e586326bcfb0_2_517x110.png)스크린샷 2024-05-13 오후 7.47.011644×352 38.9 KB](https://ethresear.ch/uploads/default/b0a06aed03cdbbe0c2df234e6a85e586326bcfb0)

We will also open our code&dataset soon.

We hope to offer a deeper understanding on the post-upgrade effects and encourage discussions that can help improve the Ethereum ecosystem. Your feedback and insights would be greatly appreciated.

## Replies

**SK0M0R0H** (2024-05-13):

It’s not clear from the plots, but it seems that for zkRollups, the increase in blob usage is more significant than the decrease in calldata compared to optimistic rollups.

Does this mean that after EIP-4844, zkRollups generally put more data on Ethereum? And the ‘marked increase in total data size posted by rollups (+116%)’ primarily attributed to zkRollups?

---

**wanify** (2024-05-13):

Hi, thank you for your comment!

The blue line in the figure represents the combined data of ‘calldata + blob’, not solely blob data size. We’ve added a new table to our post for clearer communication.

![](https://ethresear.ch/user_avatar/ethresear.ch/sk0m0r0h/48/2371_2.png) SK0M0R0H:

> Does this mean that after EIP-4844, zkRollups generally put more data on Ethereum? And the ‘marked increase in total data size posted by rollups (+116%)’ primarily attributed to zkRollups?

Indeed, the total data size posted by both optimistic rollups (+127.4%) and zk rollups (+102.22%) increased significantly. As for calldata, there was a more pronounced decrease in optimistic rollups (-80.98%) compared to zk rollups (-23.26%).

---

**SK0M0R0H** (2024-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/wanify/48/12083_2.png) wanify:

> As for calldata, there was a more pronounced decrease in optimistic rollups (-80.98%) compared to zk rollups (-23.26%).

Yeah, I think it makes sense for zkRollups because they still need to put proofs and public input into calldata.

![](https://ethresear.ch/user_avatar/ethresear.ch/wanify/48/12083_2.png) wanify:

> Indeed, the total data size posted by both optimistic rollups (+127.4%) and zk rollups (+102.22%) increased significantly.

But do you have any additional information or hypotheses on what rollups are posting now that they didn’t post before?

---

**wanify** (2024-05-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/sk0m0r0h/48/2371_2.png) SK0M0R0H:

> But do you have any additional information or hypotheses on what rollups are posting now that they didn’t post before?

While we didn’t detail this in our paper, the most notable changes were observed in Starknet, where data posting increased from 0.0001MB to 0.015MB—potentially related to the Starknet v0.13.1 update—and in Base, where posting increased from 0.01MB to 0.043MB.

