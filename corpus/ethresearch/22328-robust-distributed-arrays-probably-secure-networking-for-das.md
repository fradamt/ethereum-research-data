---
source: ethresearch
topic_id: 22328
title: Robust Distributed Arrays -- Probably Secure Networking for DAS
author: b-wagn
date: "2025-05-13"
category: Networking
tags: [data-availability]
url: https://ethresear.ch/t/robust-distributed-arrays-probably-secure-networking-for-das/22328
views: 246
likes: 4
posts_count: 1
---

# Robust Distributed Arrays -- Probably Secure Networking for DAS

# Robust Distributed Arrays – Probably Secure Networking for DAS

*Authors:* Dankrad Feist, Gottfried Herold, Mark Simkin, Benedikt Wagner

Data Availability Sampling (DAS) is a central component of Ethereum’s roadmap. It enables clients to verify data availability without requiring any single client to download the entire dataset. DAS operates by having clients randomly retrieve parts of redundantly encoded data from a peer-to-peer network. While the cryptographic and encoding aspects of DAS have recently undergone [formal analysis](https://eprint.iacr.org/2023/1079.pdf), the peer-to-peer networking layer remains underexplored, with a lack of security definitions and efficient, provably secure constructions.

In [our work](https://arxiv.org/pdf/2504.13757), we address this gap by introducing a novel distributed data structure that can serve as the networking layer for DAS, which we call *robust distributed arrays*.

Our work consists of two parts:

1. we give a formal model, rigorously defining what the networking solution for DAS should achieve in terms of security. We call the resulting distributed data structure robust distributed arrays.
2. we present a simple and efficient construction and formally prove that it satisfies our definition. Our construction operates in a permissionless network and remains secure even if a majority of participants are malicious. Concretely, we only assume that a sufficiently large absolute number of honest parties is online in sufficiently large time intervals, irrespective of how many malicious parties there are in the network. In particular, we avoid any honest majority assumption. The reason why tolerating a dishonest majority is important is that DAS is a crucial component for Ethereum‘s safety, which should hold even under dishonest majority. We explain this in more detail in the introduction of our paper.

[The paper](https://arxiv.org/pdf/2504.13757) contains the formal definition (Section 3) as well as the construction and its analysis (Section 4).

Intuitively, our security notion (Definition 4) states that for most indices i, if a party stores data x at position i at some time and after some minimum delay another party tries to retrieve the data stored at position i, this indeed gives back x.

This security notion means that the corresponding non-distributed data structure is simply an array, hence the name. Our construction achieves this without requiring every participant to store all data.

For all details, including informal overviews, we refer to [the paper](https://arxiv.org/pdf/2504.13757).
