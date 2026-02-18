---
source: ethresearch
topic_id: 20361
title: PeerDas Documentation
author: arantxazapico
date: "2024-08-30"
category: Sharding
tags: [data-availability]
url: https://ethresear.ch/t/peerdas-documentation/20361
views: 676
likes: 6
posts_count: 2
---

# PeerDas Documentation

Joint work with [@b-wagn](/u/b-wagn), [A Documentation of Ethereum’s PeerDAS](https://eprint.iacr.org/2024/1362.pdf)

The long-term vision of the Ethereum community includes a comprehensive data availability protocol using polynomial commitments and tensor codes. As the next step towards this vision, an intermediate solution called PeerDAS is about to integrated, to bridge the way to the full protocol. With PeerDAS soon becoming an integral part of Ethereum’s consensus layer, understanding its security guarantees is essential.

The linked document aims to describe the cryptography used in PeerDAS in a manner accessible to the cryptographic community, encouraging innovation and improvements, and to explicitly state the security guarantees of PeerDAS. We focus on PeerDAS as described in Ethereum’s consensus specifications [[Eth24a](https://github.com/ethereum/consensus-specs/commit/54093964c95fbd2e48be5de672e3baae8531a964), [Eth24b](https://github.com/ethereum/consensus-specs/tree/dev/specs/_features/eip7594)].

Our intention is two-fold: first, we aim to provide a description of the cryptography used in PeerDAS that is accessible to the cryptographic community, potentially leading to new ideas and

improvements that can be incorporated in the future. Second, we want to explicitly state the security and efficiency guarantees of PeerDAS. In terms of security, this document justifies the following claim:

**Theorem 1** (Main Theorem, Informal): *Assuming plausible cryptographic hardness assumptions, PeerDAS is a secure data availability sampling scheme in the algebraic group model, according to the definition in [[HASW23](https://eprint.iacr.org/2023/1079)].*

We hope to receive feedback from the community to make further improvements to this document

## Replies

**b-wagn** (2025-09-18):

As an update, we have just released an improved security analysis [here](https://eprint.iacr.org/2025/1683).

In particular, we can prove security now from a standard model assumption instead of relying on the algebraic group model.

