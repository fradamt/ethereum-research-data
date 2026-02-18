---
source: magicians
topic_id: 3973
title: Pre-compile for BLS
author: greg
date: "2020-01-30"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/pre-compile-for-bls/3973
views: 4462
likes: 0
posts_count: 5
---

# Pre-compile for BLS

Currently the EVM has no support for BLS signatures, there was a [proposed eip](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1829.md) although I don’t believe it made it in (or if it will make it in). Having the ability to perform on-chain BLS operations can be quite useful, especially since these curves are becoming increasingly popular in the rest of the blockchain world. More importantly, this would be an immense benefit for eth2.0.

Currently, the eth2.0 deposit contract is able to verify a deposit is correct, except for the actual signature. This means that if a user submits an invalid deposit they risk losing their 32 eth deposit. With a BLS pre-compile we could verify the deposits on-chain before the deposit occurs so users to do not burn there funds.

If this is somehing that would be considered I’m happy to draft the EIP ASAP. If there are suggested additions to this EIP (to make it more generalized, like the linked EIP) than I would also be happy to do that as well.

Counter argument: People will use eth2 software to ensure it is formed correctly.

Response: I’d rather be safe than sorry. We don’t need to do another bailout.

## Replies

**guthlStarkware** (2020-01-30):

Why cannot you do it with the existing precompile?

https://github.com/kfichter/solidity-bls

---

**greg** (2020-01-30):

I believe the cost of performing this verification is inherently expensive. Do you know the gas costs?

---

**ralexstokes** (2020-02-18):

This precompile will add support for the BLS12-381 curve (https://electriccoin.co/blog/new-snark-curve/) we are using in eth2.0. We do happen to be using the BLS signature scheme over this curve and most of the relevant pieces (except “hash to curve”) could be done in a smart contract w/ the appropriate precompiles for the BLS12-381 curve ops.

---

**mratsim** (2024-04-06):

This thread is listed as the discussion thread for [EIP-3068](https://eips.ethereum.org/EIPS/eip-3068) Precompile for BN256 HashToCurve Algorithms, which is proposal for [Pectra](https://ethereum-magicians.org/t/pectra-network-upgrade-meta-thread/16809).

I disagree with EIP-3068 as-is.

Since 2020, the IETF has standardized hashing-to-curve: [Hashing to Elliptic Curves](https://www.ietf.org/archive/id/draft-irtf-cfrg-hash-to-curve-16.html)

The EIP-3068 would be doing “encode-to-curve” of the spec instead of hash-to-curve. The implementation difference is minimal, hash-to-curve samples 2 points and sum them to combat bias in the random distribution.



      [github.com](https://github.com/kwantam/bls12-381_hash#bib)




  ![image](https://opengraph.githubassets.com/c5e468bf30a43d97f0b622cf2501df11/kwantam/bls12-381_hash#bib)



###



Fast and simple constant-time hashing to the BLS12-381 elliptic curve










[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9910e5db0c6d9f7d6880de71415bba6438799120_2_690x381.png)image1070×591 71 KB](https://ethereum-magicians.org/uploads/default/9910e5db0c6d9f7d6880de71415bba6438799120)

Implementations:

- Constantine: BN254 - Hash-to-Curve (SVDW method) by mratsim · Pull Request #190 · mratsim/constantine · GitHub
- Gnark: gnark-crypto/ecc/bn254/hash_to_g1.go at 73d59806bf0bd5c0fab56141d23b670a8d8fbdfa · Consensys/gnark-crypto · GitHub

