---
source: magicians
topic_id: 4628
title: EIP-2539 - Precompiles for BLS12-377 curve operations
author: prestwich
date: "2020-09-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2539-precompiles-for-bls12-377-curve-operations/4628
views: 926
likes: 2
posts_count: 2
---

# EIP-2539 - Precompiles for BLS12-377 curve operations

Celo is considering EIP-2539 for adoption in an upcoming hard fork, alongside EIP-2537. This work is complementary to the EIP-2537 precompiles. Conceptually, BLS12-377 is similar to BLS12-381, however, it has several interesting properties that BLS12-377 has that BLS12-381 does not. For example, 377 supports Halo-like proofs without trusted setups, and can provide many of the benefits of recursive proofs.

We have high-quality implementations of BLS12-377 in Rust and Golang (in-progress). I will be on the ACD call tomorrow to share some more of our plans, and talk about how we can contribute time and resources to geth and openethereum integration of both EIPs.

Resources:

- EIP-2539 Draft Spec
- EIP-2537

## Replies

**rdubois-crypto** (2022-11-07):

The ‘NTT friendly aspect’ of BLS12-377 is also compatible with Starks to speed up the FRI step. It would be of great interest to adopt it.

