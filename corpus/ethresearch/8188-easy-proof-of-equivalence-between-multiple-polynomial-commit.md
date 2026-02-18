---
source: ethresearch
topic_id: 8188
title: Easy proof of equivalence between multiple polynomial commitment schemes to the same data
author: vbuterin
date: "2020-11-05"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/easy-proof-of-equivalence-between-multiple-polynomial-commitment-schemes-to-the-same-data/8188
views: 7662
likes: 19
posts_count: 5
---

# Easy proof of equivalence between multiple polynomial commitment schemes to the same data

Suppose you have multiple polynomial commitments C_1 … C_k, under k different commitment schemes (eg. Kate, FRI, something bulletproof-based, DARK…), and you want to prove that they all commit to the same polynomial P. We can prove this easily:

Let z = hash(C_1 .... C_k), where we interpret z as an evaluation point at which P can be evaluated.

Publish openings O_1 ... O_k, where O_i is a proof that C_i(z) = a under the i’th commitment scheme. Verify that a is the same number in all cases.

### Explanation

If any two commitments C_i and C_j point to different data, then they would almost certainly evaluate to different values at a randomly selected point (this is because if P_i - P_j is nonzero, then because P_i and P_j have some low degree < D (eg. D = 2^{15}), P_i - P_j can only be zero at \le D points, which is an insignificant fraction of all possible evaluation points). Hence, if there are successful openings at the same random coordinate that return the same value, this shows that all polynomials must be the same.

Choosing the point z as a hash of all the commitments ensures that there is no way to manipulate the data or the commitments after you learn z (this is standard Fiat-Shamir reasoning).

## Replies

**David** (2022-09-11):

This looks good to me but what usecase would this serve?

---

**vbuterin** (2022-09-12):

See the proto-danksharding FAQ, [here](https://notes.ethereum.org/@vbuterin/proto_danksharding_faq#How-exactly-do-ZK-rollups-work-with-the-KZG-commitment-efficiently) and the section before that.

---

**wanify** (2022-09-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> C_i(z) = a

I am not quite familiar with cryptography but… P_i(z)=a, isn’t it?

---

**CODER-6** (2024-02-27):

It should be added that C1…Ck are polynomial commitments over **the same field**.

