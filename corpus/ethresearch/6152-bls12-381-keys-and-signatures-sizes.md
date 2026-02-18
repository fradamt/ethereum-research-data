---
source: ethresearch
topic_id: 6152
title: "BLS12-381: Keys and Signatures Sizes"
author: hermanjunge
date: "2019-09-16"
category: Cryptography
tags: []
url: https://ethresear.ch/t/bls12-381-keys-and-signatures-sizes/6152
views: 4593
likes: 2
posts_count: 4
---

# BLS12-381: Keys and Signatures Sizes

Hello,

I’ve been struggling to find a justification for the **size of the private key in BLS12-381**. So far, my best hit is within this [chia network document](https://github.com/Chia-Network/bls-signatures/blob/bb96228e51aa0ffba917d8660989ce6f655d8db8/SPEC.md#serialization), who gives some insight on the public key and signature, but just mentions what is going on with the private key.

> private key (32 bytes):  Big endian integer.
>
>
> pubkey (48 bytes):  381 bit affine x coordinate, encoded into 48 big-endian bytes. Since we have 3 bits left over in the beginning, the first bit is set to 1 iff y coordinate is the lexicographically largest of the two valid ys. The public key fingerprint is the first 4 bytes of hash256(serialize(pubkey)).
>
>
> signature (96 bytes):  Two 381 bit integers (affine x coordinate), encoded into two 48 big-endian byte arrays. Since we have 3 bits left over in the beginning, the first bit is set to 1 iff the y coordinate is the lexicographically largest of the two valid ys. (The term with the i is compared first, i.e 3i + 1 > 2i + 7). The second bit is set to 1 iff the signature was generated using the prepend method, and should be verified using the prepend method.

Are these 32 bytes related to the parameter `r` [defined here](https://electriccoin.co/blog/new-snark-curve/)? Or is just an un-educated guess?

> As is common, we target a subfamily of these curves that has optimal extension field towers and simple twisting isomorphisms. In order to ensure Montgomery reductions and other approximation algorithms are space-efficient, we target r≈2^255 so that the most significant bit of rr (and qq) are unset with 64-bit limbs.

Any pointer will be appreciated.

**Herman**

## Replies

**kobigurk** (2019-09-17):

Hey Herman,

A BLS private key is a number in the scalar field. So indeed, that’s a number < r.

---

**hermanjunge** (2019-09-17):

Answering to myself here:

#### Private Keys: 32 Bytes.

- The private key is just a scalar that your raise curve points to the power of. The subgroup order for G1 and G2 is r~2^255, so for private keys higher than this the point just wraps around. Therefore, useful private keys are <2^255 and fit into 32 bytes.
- Recall that r is defined here: https://electriccoin.co/blog/new-snark-curve/

#### Public Keys: 48 Bytes.

- 381 bit affine x coordinate, encoded into 48 big-endian bytes.
- See also https://github.com/ethereum/eth2.0-specs/blob/7a5cdc2a9df9a19c3abe47d88a8b7587a9f109d3/specs/core/0_beacon-chain.md#custom-types

#### Signatures: 96 Bytes.

- Two 381 bit integers (affine x coordinate), encoded into two 48 big-endian byte arrays.
- The signature is a point on the G2 subgroup, which is defined over a finite field with elements twice as big as the G1 curve (G2 is over Fq2 rather than Fq. Fq2 is analogous to the complex numbers).
- See also https://github.com/ethereum/eth2.0-specs/blob/7a5cdc2a9df9a19c3abe47d88a8b7587a9f109d3/specs/core/0_beacon-chain.md#custom-types

---

**kobigurk** (2019-09-17):

Important to note that the public keys and signatures are not just the x coordinate, they’re compressed points. So the encoding has bits signifying which of the two possible ys is chosen.

