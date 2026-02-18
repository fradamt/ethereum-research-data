---
source: magicians
topic_id: 19197
title: Proposal for zk-rollups ensuring data availability and decentralization
author: HCP
date: "2024-03-14"
category: Magicians > Primordial Soup
tags: [sharding, eip-4844]
url: https://ethereum-magicians.org/t/proposal-for-zk-rollups-ensuring-data-availability-and-decentralization/19197
views: 718
likes: 0
posts_count: 1
---

# Proposal for zk-rollups ensuring data availability and decentralization

We propose new techniques for zk-Rollups in Layer 2 blockchain networks to ensure data availability and decentralization. Below, you will find the abstract of our paper.

The scalability limitations of public blockchains have hindered their widespread adoption in real-world applications. While the Ethereum community is pushing forward in zk-rollup (zero-knowledge rollup) solutions, such as introducing the "blob transaction’’ in EIP-4844, Layer 2 networks encounter a data availability problem: storing transactions completely off-chain poses a risk of data loss, particularly when Layer 2 nodes are untrusted. Additionally, building Layer 2 blocks requires significant computational power, compromising the decentralization aspect of Layer 2 networks.

We introduce new techniques to address the data availability and decentralization challenges in Layer 2 networks. To ensure data availability, we introduce the concept of "proof of download’‘, which ensures that Layer 2 nodes cannot aggregate transactions without downloading historical data. Additionally, we design a "proof of existence’’ scheme that punishes nodes who maliciously delete historical data. For decentralization, we introduce a new role separation for Layer 2, allowing nodes with limited hardware to participate. To avoid collusion among Layer 2 nodes, we design a ``proof of luck’’ scheme, which also provides robust protection against maximal extractable value (MEV) attacks.

The full version of our paper can be found at ([[2403.10828] Data Availability and Decentralization: New Techniques for zk-Rollups in Layer 2 Blockchain Networks](https://arxiv.org/abs/2403.10828?context=cs.CR)).

We are very keen to get feedback from the Ethereum community.

I’d welcome any questions or discussion here.
