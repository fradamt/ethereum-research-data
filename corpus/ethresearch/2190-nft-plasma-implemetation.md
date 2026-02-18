---
source: ethresearch
topic_id: 2190
title: NFT Plasma implemetation
author: fubuloubu
date: "2018-06-10"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/nft-plasma-implemetation/2190
views: 3158
likes: 1
posts_count: 5
---

# NFT Plasma implemetation

Wondering if there are successful NFT-related Plasma implemetations in the works I can review.

I have a construction where NFT is tokenizing a physical asset and the Plasma chain operators are permissioned and require no fees due to external incentivization to facilitate transactions. Why the validators are sufficiently incentivizes against DoS to network participants is more for me to figure out, the point is no fees are required so no splits need to happen. Because my token is a NFT, it doesn’t make sense to split the token, I just care that each transfer is legally conducted according to the transaction rules I have (basically owner gives UID X to new owner).

My questions are about how much I can optimize the plasma construction with the constraint that transactions are feeless and Single Input-Single Output. My initial thought is that it requires: block number, transaction index, new owner, and signature. I might also add an ID field for the NFT token’s ID.

I have less experience with UTXO-based chains than with Ethereum’s account based structure, so I know I am probably missing something here. I also figured with all the NFT fever happening, someone has to be working on this, and may even want to colloborate with us on our use case.

## Replies

**kfichter** (2018-06-10):

I would highly recommend implementing [Plasma Cash](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298) for this. It’s exactly what you’re looking for.

I don’t know if there are any complete Plasma Cash implementations (yet).

---

**fubuloubu** (2018-06-10):

Thanks! I hadn’t read that one as closely, it definitely seems like a more perfect fit.

---

**chfast** (2019-06-26):

After one year, is there any update in the subject?

---

**fubuloubu** (2019-06-26):

I am working on this still. Trying to adapt what the current state of the art is to a Rust implementation.

There seems to be a lot more being done on more general-purpose plasmas, but this has had work done on it, mostly from [@gakonst](/u/gakonst)

