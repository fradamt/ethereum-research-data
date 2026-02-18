---
source: ethresearch
topic_id: 9933
title: Point compression in pairing-based cryptography
author: dishport
date: "2021-06-25"
category: Cryptography
tags: []
url: https://ethresear.ch/t/point-compression-in-pairing-based-cryptography/9933
views: 1617
likes: 0
posts_count: 3
---

# Point compression in pairing-based cryptography

It is well known that in pairing-based cryptography we mainly use two groups G_1 and G_2 without an efficiently computable isomorphism between them (so-called type 3 pairings). Do you know protocols in which one party simultaneously sends to another party points P_1 \in G_1 and P_2 \in G_2 ? I am also interested in the situation when three points of only one group G_1 (or G_2) are transmitted.

Maybe for these cases I know a batch compression method such that its decompression phase is much faster than finding y-coordinates from given x-coordinates. I want to understand, is my result useful or not in practice ?

Thanks in advance for any comments.

## Replies

**Pratyush** (2021-06-25):

Yes, in zkSNARK proofs you often send multiple elements together. For example, a Groth16 proof is 2G1 and 1G2.

---

**dishport** (2021-06-26):

For 2G1 + 1G2 we can use [my earlier method](https://eprint.iacr.org/2020/010/20200724:162533) with the cost of two exponentiations in the basic field \mathbb{F}_p (i.e., independently compress-decompress 2G1 and 1G2). In other words, in this situation we do not need to independently compress-decompress 2G1 + 1G2 and 1G1, because the complexity is the same (two exponentiations). I know how to compress-decompress 3G1 or 1G1 + 1G2 (if the embedding degree k=12 as for curves BLS12 or BN) with the cost of one exponentiation in \mathbb{F}_p.

