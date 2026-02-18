---
source: magicians
topic_id: 4790
title: "EIP-3026: BW6-761 curve operations"
author: yelhousni
date: "2020-10-06"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-3026-bw6-761-curve-operations/4790
views: 2705
likes: 2
posts_count: 3
---

# EIP-3026: BW6-761 curve operations

One-layer recursive proof composition can be achieved for pairing-based zkSNARKs (e.g. Groth16) using chains of pairing-friendly elliptic curves. Such curves were introduced in [ZEXE](https://github.com/scipr-lab/zexe), namely: BLS12-377 and CP6-782. Later a new curve was constructed in [[HG20](https://eprint.iacr.org/2020/351.pdf)] to replace CP6-782 with very efficient implementation, namely BW6-761. There are many implementations of this new curve in different languages (Rust, C++, Go, Go/Assembly). This thread is to discuss the EIP-3026 related to it.

We want to get community feedback and assess public interest in this curve getting into Ethereum. Note that for gas schedule, we followed EIP-2537 for estimation but haven’t proposed constants yet because there are many implementations and Ethereum clients and we’re looking for comparing them, so *help is wanted*.

## Replies

**yelhousni** (2020-10-15):

Thanks to [@kobigurk](/u/kobigurk), Jon Chuang and Celo folks, we have the fastest implementation of BW6-761 (https://github.com/celo-org/zexe). This implementation is based on the Rust reference implementation available in zexe (https://github.com/scipr-lab/zexe) but implements Intel assembly instructions, GLV multiplication and batched inversion. The timings on a i7-8700k machine are:

```auto
- test curves::bw6_761::bench_g1_add_assign                ... bench:       1,901 ns/iter (+/- 114)
test curves::bw6_761::bench_g1_add_assign_mixed          ... bench:       1,342 ns/iter (+/- 87)

- test curves::bw6_761::bench_g2_add_assign                ... bench:       1,915 ns/iter (+/- 159)
test curves::bw6_761::bench_g2_add_assign_mixed          ... bench:       1,366 ns/iter (+/- 112)

- test curves::bw6_761::bench_g1_mul_assign                ... bench:     310,110 ns/iter (+/- 14,826)

- test curves::bw6_761::bench_g2_mul_assign                ... bench:     314,360 ns/iter (+/- 21,913)

- test curves::bw6_761::bench_pairing_final_exponentiation ... bench:   1,653,075 ns/iter (+/- 131,364)
test curves::bw6_761::bench_pairing_full                 ... bench:   3,364,130 ns/iter (+/- 255,925)
test curves::bw6_761::bench_pairing_miller_loop          ... bench:   1,266,690 ns/iter (+/- 76,955)
```

---

**mratsim** (2020-10-31):

I’m curious of the performance benchmark of https://github.com/kilic/bw6 as well as it also uses assembly.

