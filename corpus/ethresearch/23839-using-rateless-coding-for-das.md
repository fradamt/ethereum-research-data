---
source: ethresearch
topic_id: 23839
title: Using Rateless Coding for DAS
author: MoritzGrundei
date: "2026-01-12"
category: Sharding
tags: [data-availability]
url: https://ethresear.ch/t/using-rateless-coding-for-das/23839
views: 185
likes: 8
posts_count: 4
---

# Using Rateless Coding for DAS

# Abstract

We want to motivate the usage of rateless codes, particularly Random Linear Network Coding (RLNC) through an on demand sampling approach instead of sampling from a fixed coded set as done in prevailing DAS methods like Celestia, SPAR, or Peer/Full DAS from the perspective of sampling efficiency.

# Why Fixed Rate Codes?

The original motivation for the usage of coding for DAS was that, under anonymity, sampling from uncoded data only decreases false negative probability (a verifier concluding that data is available even though it is not) linearly with the number of samples taken as 1 - s/k for s samples taken from k uncoded chunks. Now, if we apply a (n,k) RS code for example, the false negative probability for s samplings (without replacement) decreases faster than ((k-1)/n)^s.

# Increased Sampling Efficiency Through Rateless Coding

By employing fixed rate coding, the verifier (light client) inherently restricts itself to sampling from a pre-coded set of n symbols. Looking at the false negative probability above for sampling from fixed rate coded data, the question that naturally arises is: why not make the n as large as possible so that the false negative probability is sufficiently low even for a small number of samples? There are several downsides to this including:

- The codes used here are usually codes like RS codes that have inherent limits on the magnitude of n as well as the possible combinations of (n,k).
- storage and computational cost at the data producer would inadvertently increase alongside bandwidth costs for dispersal of sampling data to custody nodes like for example in PeerDAS.

A natural solution to this problem would be to create samples on demand to prevent the storage and dispersal bottlenecks, which naturally leads us to consider rateless codes as those can be viewed as maximum distance separable (MDS) codes in the limit for large n. RLNC is one example of such a rateless code that builds coded packages by forming random linear combinations of the original data.

On demand sampling from a code like RLNC provides a false negative probability of q^{-s} where q denotes the cardinality of the field for the coding coefficients. The full description of one such protocol is given in this paper: From Indexing to Coding: [A New Paradigm for Data Availability Samping](https://www.arxiv.org/abs/2509.21586#:~:text=From%20Indexing%20to%20Coding%3A%20A%20New%20Paradigm%20for%20Data%20Availability%20Sampling,-Moritz%20Grundei%2C%20Aayush&text=The%20data%20availability%20problem%20is,by%20platforms%20such%20as%20Ethereum.)

[![Screenshot 2026-01-09 at 15.09.13](https://ethresear.ch/uploads/default/optimized/3X/2/4/24c408a65497797b078b652f6ba089bc66d976ee_2_690x457.png)Screenshot 2026-01-09 at 15.09.132334×1546 271 KB](https://ethresear.ch/uploads/default/24c408a65497797b078b652f6ba089bc66d976ee)

Probability of a false negative (Undecodability of the underlying payload is not detected) for sampling from coded data (see [1],[2]).

# Potential for true Decentralisation

Another downside with fixed rate coded data is that samples are individualized which gives room for expensive repairability procedures. For 1D RS codes, as used in PeerDAS for example, losing a single Cell of an RS coded blob requires downloading the equivalent of an entire blob to reconstruct the data due to the bad locality properties of RS codes. Once tensor codes are introduced this will get better but an unstructured code like RLNC can also provide a more decentralized version of distributed custody,

A [protocol for decentralized custody](https://ethresear.ch/t/alternative-das-concept-based-on-rlnc/22651) using RLNC has been proposed by [@Nashatyrev](/u/nashatyrev) showing favorable properties in repair bandwidth as well as dissemination and storage overhead.

# References

[1] Al-Bassam, Mustafa, et al. “Fraud and data availability proofs: Detecting invalid blocks in light clients.” *International Conference on Financial Cryptography and Data Security*. Berlin, Heidelberg: Springer Berlin Heidelberg, 2021.

[2] Yu, Mingchao, et al. “Coded merkle tree: Solving data availability attacks in blockchains.” *International Conference on Financial Cryptography and Data Security*. Cham: Springer International Publishing, 2020.

## Replies

**Nashatyrev** (2026-01-13):

Great paper! Thank you for sharing.

Just a quick question: in your approach you make Pedersen commitments for rows while linearly combine columns. In this post [Faster block/blob propagation in Ethereum](https://ethresear.ch/t/faster-block-blob-propagation-in-ethereum/21370#p-52013-the-proposer-5) the commitments are made for columns which makes proof for `w` simpler from my perspective and don’t require extra interaction (sending projection vectors `p`). What are the pros of row commitments then?

---

**MoritzGrundei** (2026-01-13):

Thank you for the question!

You are right, the Pedersen commitments can be simply applied over the columns as you suggested in your post which is a possible way to do it.

The downside would be that the commitment size grows linearly with the number of packages / columns. Considering the inner product argument in the verification process, download cost only grows with log(N) while incurring some more computational complexity during the verification process.

---

**Nashatyrev** (2026-01-14):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/m/f17d59/48.png) MoritzGrundei:

> the commitment size grows linearly with the number of packages / columns

Oh yeah, it is actually great to have as many columns as you want ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) Thanks for explanation!

So a light client needs only a supernode (node with the whole data at hands) to do sampling in this scheme. But I believe it shouldn’t be a problem to sample a partial node as well which has only several original columns. Thus a light client may select a number of partial nodes to do the full sampling if they have the full set of columns in total.

