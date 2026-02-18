---
source: ethresearch
topic_id: 13563
title: Subgroup membership testing on elliptic curves via the Tate pairing
author: dishport
date: "2022-09-02"
category: Cryptography
tags: []
url: https://ethresear.ch/t/subgroup-membership-testing-on-elliptic-curves-via-the-tate-pairing/13563
views: 1877
likes: 3
posts_count: 2
---

# Subgroup membership testing on elliptic curves via the Tate pairing

[Subgroup membership testing on elliptic curves via the Tate pairing](https://link.springer.com/article/10.1007/s13389-022-00296-9)

[Journal of Cryptographic Engineering](https://link.springer.com/journal/13389) (2022)

> This note explains how to guarantee the membership of a point in the prime-order subgroup of an elliptic curve (over a finite field) satisfying some moderate conditions. For this purpose, we apply the Tate pairing on the curve; however, it is not required to be pairing-friendly. Whenever the cofactor is small, the new subgroup test is much more efficient than other known ones, because it needs to compute at most two n-th power residue symbols (with small n) in the basic field. More precisely, the running time of the test is (sub-)quadratic in the bit length of the field size, which is comparable with the Decaf-style technique. The test is relevant, e.g., for the zk-SNARK friendly curves Bandersnatch and Jubjub proposed by the Ethereum and Zcash research teams, respectively.

## Replies

**dishport** (2023-02-05):

I added an important appendix to my article. You will find attached

[Subgroup membership testing on elliptic curves via the Tate pairing.pdf](https://forum.zcashcommunity.com/uploads/short-url/r0S44ADAoSDO0vBnEjEkHlJx7rD.pdf) (307.5 KB)

the full version of the text (including appendix). Thereby, the new subgroup check is generalized to most elliptic curves. Do you have in Ethereum an elliptic curve for which such a subgroup membership test is necessary ? If so, I can adapt the new test for that curve.

