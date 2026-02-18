---
source: ethresearch
topic_id: 5904
title: Cheap EC Operations on Unsupported Curves
author: m1cm1c
date: "2019-07-31"
category: Cryptography
tags: []
url: https://ethresear.ch/t/cheap-ec-operations-on-unsupported-curves/5904
views: 1865
likes: 1
posts_count: 5
---

# Cheap EC Operations on Unsupported Curves

I want to be able to verify signatures created by smart meters. Unfortunately, their signature algorithm doesn’t use curve ALT_BN_128 but BrainpoolP256r1. I wrote [this verification algorithm](https://github.com/BlockInfinity/SmartMeterSignatureVerification/blob/e6e4d85d84ed7239bb269376e5fb65ab616ce196/Verify.sol) that requires an inversion, an addition of two curve points, and two scalar multiplications of curve points. The problem is especially the gas cost of the latter.

I wrote [a contract for these operations](https://github.com/BlockInfinity/EccOperations/blob/bf47c220c5ba1876c565c4bf1559300dd38c4613/EccOperations.sol) where the scalar multiplication is implemented via a simple double-and-add algorithm. Unfortunately, a scalar multiplication using this method costs between 84’000 and 19’000’000 gas. Originally, I didn’t want to write my own contract for that but the only Solidity implementation I was able to find was `ECops.sol` by `orbs-network` on Github. Scalar multiplication using this contract is much cheaper (about 623’000 gas), but then there’s the minor disadvantage that the results are wrong.

Is there a better solidity implementation out there where I can just plug the right curve parameters in?

I have now posted this question on Ethereum SE too. I can’t post a link to it because I’m only allowed two use two per post. But I used the same title, so if you google “stackexchange Cheap EC Operations on Unsupported Curves”, it should pop up.

## Replies

**kladkogex** (2019-08-13):

SKALE network when released will support a large variety of curves.

---

**cdetrio** (2019-08-14):

Take a look at [Weierstrudel](https://medium.com/aztec-protocol/huffing-for-crypto-with-weierstrudel-9c9568c06901), it’s an optimized EVM implementation of bn128 scalar multiplication. You might be able to adapt it to another curve, but it would take some work.

---

**mariocao** (2019-09-09):

You can take a look to our [elliptic-curve-solidity](https://github.com/witnet/elliptic-curve-solidity) library. Our library was  generalized in order to support any elliptic curve based on prime numbers up to 256 bits, so it should fit your needs. ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=14)

Additionally, we recently implemented a wNAF simultaneous multiplication for curves with valid endomorphisms such as `Secp256k1`.

---

**kladkogex** (2019-10-18):

In most cases you need pairing too … So it has to be precompiled in order to be viable …

