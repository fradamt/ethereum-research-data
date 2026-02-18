---
source: ethresearch
topic_id: 20619
title: Potential impact of blob sharing for rollups
author: hyeonleee
date: "2024-10-12"
category: Layer 2
tags: []
url: https://ethresear.ch/t/potential-impact-of-blob-sharing-for-rollups/20619
views: 761
likes: 15
posts_count: 5
---

# Potential impact of blob sharing for rollups

By [Suhyeon](https://suhyeonlee.xyz/) - [Tokamak Network](https://www.tokamak.network/)

## TL;DR

> Small rollups encounter a dilemma because of their low L2 data throughput: blob use inefficiency or long blob delay.
> One solution to this problem is blob sharing, which is to put multiple rollups’ data into one blob.
> Our research simulated blob sharing of 26 rollups using nearly 6 months of data.
> The simulation results show all rollups (not only small ones) get at least 85% cost savings in DA.
> We found this is because active blob sharing reduces the number of blobs and smooths the blob base fee without spikes.

## Introduction

Rollups are a key scalability solution for Ethereum, processing transactions off-chain and submitting compressed data back to the main network. Before EIP-4844, rollups faced high data availability (DA) costs because all transaction data (calldata) had to be included on-chain, which was expensive.

EIP-4844 introduced blobs, a new type of transaction data that is cheaper to include on-chain compared to calldata. Blobs are fixed in size at 128 KB and are stored for about 18 days. This upgrade was intended to reduce DA costs significantly for rollups.

## The Small Rollup’s Dilemma

While blobs reduce costs, their fixed size poses a challenge for small rollups with low data throughput. These rollups often cannot fill the entire 128 KB blob, leading to inefficiencies. They are faced with two options:

- Use blob space inefficiently: Pay for the full blob even if they don’t need all that space.
- DA submissions with long delay: Wait until they accumulate enough data to fill a blob, which can reduce their DA service quality.

To illustrate this issue, we analyzed the blob utilization and performance of various rollups over a period from block number 19,426,589 to 20,611,514. The results are summarized in Table 1.

## Defining DA Service Quality

Here, to quantitatively measure the data availability service quality, we use a new indicator defined by the following formula:

\text{DA_Quality} = \frac{1}{\ln(\text{Average_Block_Gap}) + 1}

This formula assigns a higher DA quality score to rollups that submit blobs more frequently (i.e., smaller average block gaps between blob submissions). It’s a logarithmic function to handle large block intervals, ensuring meaningful comparisons across different rollups.

**Table 1: Rollup Blob Utilization and Performance (Blocks 19,426,589 to 20,611,514)**

| Rollup | Blob Count | Average Size (KB) | Total Size (GB) | DA Quality |
| --- | --- | --- | --- | --- |
| Base | 690,356 | 126.51 (98.84%) | 83.293 | 0.309 |
| Arbitrum | 375,014 | 127.52 (99.63%) | 45.607 | 0.288 |
| Taiko | 328,805 | 30.70 (23.99%) | 9.628 | 0.592 |
| OP Mainnet | 265,469 | 126.71 (98.99%) | 32.080 | 0.239 |
| Scroll | 139,199 | 105.35 (82.30%) | 13.985 | 0.332 |
| Blast | 106,033 | 115.03 (89.87%) | 11.632 | 0.255 |
| Linea | 93,604 | 117.64 (91.90%) | 10.501 | 0.237 |
| StarkNet | 62,361 | 127.98 (99.98%) | 7.611 | 0.242 |
| zkSync Era | 62,149 | 128.00 (99.99%) | 7.586 | 0.215 |
| Paradex | 44,300 | 127.99 (99.99%) | 5.407 | 0.234 |
| Metal | 31,382 | 0.18 (0.14%) | 0.005 | 0.220 |
| Zircuit | 27,821 | 6.04 (4.72%) | 0.160 | 0.275 |
| Kroma | 24,193 | 59.65 (46.60%) | 1.376 | 0.208 |
| Zora | 23,592 | 126.58 (98.89%) | 2.848 | 0.161 |
| Mode | 22,585 | 126.56 (98.88%) | 2.726 | 0.159 |
| Rari | 19,583 | 31.08 (24.28%) | 0.581 | 0.214 |
| Optopia | 7,851 | 16.19 (12.65%) | 0.121 | 0.179 |
| Boba Network | 6,236 | 3.29 (2.57%) | 0.020 | 0.166 |
| Debank Chain | 3,358 | 113.84 (88.94%) | 0.365 | 0.162 |
| Camp Network | 3,292 | 98.39 (76.87%) | 0.309 | 0.136 |
| Nal | 2,998 | 0.21 (0.17%) | 0.001 | 0.168 |
| Mint | 2,515 | 90.89 (71.01%) | 0.218 | 0.140 |
| Lambda | 2,336 | 103.80 (81.09%) | 0.231 | 0.143 |
| Lumio | 1,390 | 0.43 (0.33%) | 0.001 | 0.137 |
| Parallel | 1,348 | 119.29 (93.20%) | 0.153 | 0.113 |
| XGA | 1,031 | 98.20 (76.72%) | 0.097 | 0.142 |
| Lisk | 811 | 8.04 (6.28%) | 0.006 | 0.126 |
| Kinto | 204 | 13.20 (10.31%) | 0.003 | 0.124 |

As seen in Table 1, smaller rollups often have low blob utilization percentages, indicating they are not efficiently using the blob space. This leads to higher costs per unit of data or potential delays in DA submissions.

## Blob Sharing and Simulation

Blob sharing is a strategy that allows multiple rollups to combine their data into a single blob. This approach maximizes the utilization of the blob space and reduces costs for all participating rollups. We wondered how much of the DA costs can be saved if rollups collaborate.

To evaluate the effectiveness of blob sharing, we conducted a simulation using real-world data collected over nearly six months (block number 19,426,589 to 24,848,485) after the implementation of EIP-4844. Here are the key assumptions and the process we followed:

- Constant Data Rate: We assumed that each rollup produces data at a consistent rate between blob submissions.
- Blob Sharing Structure: In our simulation, blobs are shared by including multiple rollups’ data in a single blob, each preceded by a signature and data length for proper identification.
- Uniform Gas Consumption: We assumed a uniform gas cost for data availability transactions, focusing on the minimal gas required for a Type-3 transaction.
- No Impact on Ethereum Base Fee and Priority Fee: We assumed that the reduction in transactions due to blob sharing does not affect the Ethereum base fee or the priority fees paid by transactions.

The simulation involved the following steps:

1. Data Preprocessing: We calculated the amount of data each rollup produced in every block based on their actual blob sizes and submission intervals.
2. Blob Reconstruction: Rollup data was accumulated until it reached 128 KB, at which point it was packed into a shared blob for submission.
3. Handling Excess Data/Blob: If a rollup’s data exceeded 128 KB, the surplus was included in a new blob. Excess blobs were deferred to the next block.
4. Inclusion of Unlabeled Blobs: We accounted for existing unlabeled blobs in the data, ensuring they were included in the transactions appropriately.

## Findings

Our simulation results indicate that blob sharing can significantly reduce DA costs for all the rollups, with cost savings exceeding 85% for most rollups. Additionally, DA service quality improved due to more frequent data submissions enabled by blob sharing.

[![USD Cost Difference between Real and Simulated Blob Sharing](https://ethresear.ch/uploads/default/optimized/3X/5/4/54f1fb5a0f0cbd9c9346937e926ffcc95585dd1d_2_690x412.png)USD Cost Difference between Real and Simulated Blob Sharing1425×852 63.6 KB](https://ethresear.ch/uploads/default/54f1fb5a0f0cbd9c9346937e926ffcc95585dd1d)

As shown in Figure 1, the total costs for rollups decreased significantly in the simulation with blob sharing. The DA service quality, measured by our new indicator, also improved (you can see more data in our preprint).

## Understanding the Fee Mechanism

A key factor contributing to the substantial cost reductions is the Ethereum blob fee mechanism. The blob base fee increases exponentially when blocks include more than three blobs. By reducing the total number of blobs through sharing, we prevent sharp increases in the blob base fee, leading to significant cost savings.

The pricing of blobs follows an exponential function based on the number of blobs in a block, defined by the following equations:

\text{new_base_fee} = \max \left( B, B \times \exp \left( \frac{\text{excess_blob_gas}}{F} \right) \right)

\text{excess_blob_gas}_i = \max \left( 0, \text{excess_blob_gas}_{i-1} + \left( \text{blob_count}_i \times G - T \right) \right)

Here, *B* is the minimum base fee per unit of blob gas, *F* is the update fraction constant, and *excess_blob_gasi* represents the excess blob gas for block *i*. By minimizing the number of blobs per block through sharing, we can smooth out the blob base fee over time.

[![Blob Counts per 100,000 Blocks](https://ethresear.ch/uploads/default/optimized/3X/7/8/7835427ce6e7a408a58600de6a757c4cbaa31b3d_2_690x293.png)Blob Counts per 100,000 Blocks1665×709 81.1 KB](https://ethresear.ch/uploads/default/7835427ce6e7a408a58600de6a757c4cbaa31b3d)

Figure 2 shows the reduction in blob counts per block due to blob sharing. The total number of blobs changes by about 20%. However, the number of blocks with more than three blobs decreases dramatically. With fewer blobs per block, the blob base fee stays lower and more stable.

[![Blob Base Fee and Difference](https://ethresear.ch/uploads/default/optimized/3X/b/8/b828548d4c6946cf53adb652eb3350b0d0cf4c99_2_690x189.png)Blob Base Fee and Difference1723×473 95.5 KB](https://ethresear.ch/uploads/default/b828548d4c6946cf53adb652eb3350b0d0cf4c99)

In the result, Figure 3 shows how blob sharing leads to a smoother and lower blob base fee over time, compared to the sharp fluctuations observed without sharing. It removed over 99% of blob cost in many rollups in Figure 1.

## Conclusion

Blob sharing offers a practical solution to the inefficiencies faced by small rollups following the implementation of EIP-4844. By collaborating and sharing blobs, rollups can reduce costs, improve data availability service quality, and contribute to a more efficient Ethereum network.

Looking ahead, we cautiously predict that implementing blob sharing will require the introduction of a Proxy DA contract and the upgrade of each rollup’s DA contract to facilitate communication with this proxy. While direct access to blob data remains restricted, minimizing security concerns, establishing this interconnected and integrated data structure will necessitate active collaboration among rollups.

We believe that these findings have significant implications for the Ethereum community, especially for (smaller) rollups seeking sustainable operations. We welcome any feedback, comments, or questions about our research.

For more detailed information, please refer to our full paper available at https://arxiv.org/abs/2410.04111.

## Acknowledgements

Special thanks to Boo-Hyung Lee from [Tokamak Network](https://www.tokamak.network/) for discussions on the rollup structure and Akaki Mamageishvili from [Offchain Labs](https://www.offchainlabs.com/) for discussions on blob sharing and encouragement to post here.

## Replies

**famouswizard** (2024-10-12):

Thank you for the insightful research on blob sharing for rollups.

Have you considered any potential latency or security concerns that might arise from coordinating multiple rollups’ data submissions in shared blobs? Additionally, how do you envision the governance and incentives around the proposed Proxy DA contract to ensure smooth implementation?

Looking forward to your thoughts!

---

**hyeonleee** (2024-10-25):

[@famouswizard](/u/famouswizard) Thanks for reading my post

Firstly, I thought about security concerns for blob sharing. With the proxy DA contract structure I mentioned, the major concern will be the wrong data inclusion or DoS trials using such faults. Fortunately, the blob data is not directly accessible (only its commitment). It means this kind of threat can’t affect any rollups’ DA contracts. Therefore, I think that with the proper signature scheme for the shared blob data, security will not be a major concern.

Secondly, the incentive is an open problem I’m looking into. In [the related work](https://arxiv.org/abs/2212.10337) by Akaki and Felton, they showed that big roll-ups have greater bargaining power compared to small roll-ups, and such analysis has been shown in game theory. But as you see the data in my post, if rollups collaborate for a long term, big rollups result in even greater cost savings in dollar terms. Therefore, maybe big rollups have the motivation to treat small rollups fairly. Or, another possibility is that their partnership changes depending on the aspect of the blob base fee. For example, when the blob base fee remains high, big rollups need to make concessions, but if the blob base fee continues to be close to the minimum, big rollups may become more non-cooperative.

---

**pop** (2024-11-01):

Sharing blobs seems like a good idea! Do you have any plan to make it a real product? Like implementing and deploying a real proxy DA contract?

---

**hyeonleee** (2025-02-08):

[@pop](/u/pop)  I don’t have a plan to make a real product yet but our team is considering it seriously for a future project.

You can also check out a recent post proposing its design: [Blob Aggregation - Step Towards More Efficient Blobs - Layer 2 - Ethereum Research](https://ethresear.ch/t/blob-aggregation-step-towards-more-efficient-blobs/21624). I’ve shared my perspective on open problems in the comments there.

