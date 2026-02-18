---
source: magicians
topic_id: 15510
title: An Efficient Schnorr Multi-Signature Implementation
author: merkleplant
date: "2023-08-21"
category: Magicians
tags: [cryptography]
url: https://ethereum-magicians.org/t/an-efficient-schnorr-multi-signature-implementation/15510
views: 1946
likes: 4
posts_count: 1
---

# An Efficient Schnorr Multi-Signature Implementation

This post presents an implementation to efficiently verify aggregated Schnorr signatures.

Note that to make aggregated Schnorr signatures useful, and prevent having to store the combinatoric explosive number of possible aggregated public keys onchain, the key aggregation of the signers’ public keys must be performed onchain as well.

The implementation can be found in [Chronicle Labs](https://chroniclelabs.org/)’ new [Scribe](https://github.com/chronicleprotocol/scribe/tree/main) oracle contract. Via using Schnorr signatures we were able to reduce gas costs by [~60%](https://github.com/chronicleprotocol/scribe/blob/main/docs/Benchmarks.md) compared to our current [Median](https://github.com/makerdao/median/blob/master/src/median.sol) oracle. A further [optimistic Scribe flavor](https://github.com/chronicleprotocol/scribe/blob/main/docs/Scribe.md#optimistic-flavored-scribe)  with onchain fault resolution has near-constant gas usage for a variable amount of signers.

## Motivation

There are currently two ways to implement multi-signatures in smart contracts, with each having its drawbacks regarding gas usage:

- Using sets of ECDSA signatures
- Using BLS signatures on the alt_bn128 curve

Using sets of ECDSA signatures has linear runtime and calldataload as each signature needs to be pushed and verified onchain.

BLS signatures are [expensive in terms of gas usage](https://hackmd.io/@liangcc/bls-solidity#Gas-Consumption). Furthermore, using alt_bn128 is discouraged due to its decreasing security.

### Schnorr Signature Scheme

*Note that the following paragraphs are mostly copied from [Scribe’s Schnorr Specification](https://github.com/chronicleprotocol/scribe/blob/bad331f66efcfc5f0c87eaf2ec5ff7ee01ca12ce/docs/Schnorr.md).*

### Terminology

- H() - Keccak256 hash function
- ‖   - Concatenation operator, defined as abi.encodePacked()
- G - Generator of secp256k1
- Q - Order of secp256k1
- x  - The signer’s private key as type uint256
- P  - The signer’s public key, i.e. [x]G, as type (uint256, uint256)
- Pₓ - P’s x coordinate as type uint256
- Pₚ - Parity of P’s y coordinate, i.e. 0 if even, 1 if odd, as type uint8
- m - Message as type bytes32. Note that the message SHOULD be a keccak256 digest
- k - Nonce as type uint256

### Signing

1. Select a cryptographically secure k ∊ [1, Q)
2. Compute R = [k]G
3. Derive Rₑ being the Ethereum address of R
 Let Rₑ be the commitment
4. Construct e = H(Pₓ ‖ Pₚ ‖ m ‖ Rₑ) mod Q
 Let e be the challenge
5. Compute s = k + (e * x) mod Q
 Let s be the signature

=> The public key `P` signs via the signature `s` and the commitment `Rₑ` the

message `m`

*A Solidity implementation can be found [here](https://github.com/chronicleprotocol/scribe/blob/bad331f66efcfc5f0c87eaf2ec5ff7ee01ca12ce/script/libs/LibSchnorrExtended.sol#L64).*

### Verification

- Input : (P, m, s, Rₑ)
- Output: True if signature verification succeeds, false otherwise

1. Compute challenge e = H(Pₓ ‖ Pₚ ‖ m ‖ Rₑ) mod Q
2. Compute commitment:

```auto
  [s]G - [e]P               | s = k + (e * x)
= [k + (e * x)]G - [e]P     | P = [x]G
= [k + (e * x)]G - [e * x]G | Distributive Law
= [k + (e * x) - (e * x)]G  | (e * x) - (e * x) = 0
= [k]G                      | R = [k]G
= R                         | Let ()ₑ be the Ethereum address of a Point
→ Rₑ
```

1. Verification succeeds iff ([s]G - [e]P)ₑ = Rₑ

*A Solidity implementation can be found [here](https://github.com/chronicleprotocol/scribe/blob/bad331f66efcfc5f0c87eaf2ec5ff7ee01ca12ce/src/libs/LibSchnorr.sol#L15).*

### Key Aggregation for Multisignatures

To efficiently aggregate public keys onchain, the key aggregation

mechanism for aggregated signatures is specified as the sum of the public

keys:

```auto
Let the signers' public keys be:
    signers = [pubKey₁, pubKey₂, ..., pubKeyₙ]

Let the aggregated public key be:
    aggPubKey = sum(signers)
              = pubKey₁     + pubKey₂     + ... + pubKeyₙ
              = [privKey₁]G + [privKey₂]G + ... + [privKeyₙ]G
              = [privKey₁   + privKey₂    + ... + privKeyₙ]G
```

Note that this aggregation scheme is vulnerable to rogue-key attacks!

To prevent such attacks, it **MUST** be verified that participating

public keys own the corresponding private key.

Note further that this aggregation scheme is vulnerable to public keys with

linear relationships. A set of public keys `A` leaking the sum of their private

keys would allow the creation of a second set of public keys `B` with

`aggPubKey(A) = aggPubKey(B)`. This would make signatures created by set `A`

indistinguishable from signatures created by set `B`.

To prevent such issues, it **MUST** be verified that no two distinct

sets of public keys derive to the same aggregated public key. Note that

cryptographically sound created random private keys have a negligible

probability of having a linear relationship.

## Other Security Considerations

Note that the signing scheme deviates slightly from the classical Schnorr

signature scheme.

Instead of using the secp256k1 point `R = [k]G` directly, this scheme uses the

Ethereum address of the point `R`. This decreases the difficulty of

brute-forcing the signature from `256 bits` (trying random secp256k1 points)

to `160 bits` (trying random Ethereum addresses).

However, the difficulty of cracking a secp256k1 public key using the

baby-step giant-step algorithm is `O(√Q)`, with `Q` being the order of the group.

Note that `√Q ~ 3.4e38 < 128 bit`.

Therefore, this signing scheme does not weaken the overall security.

## Important Optimizations

### Elliptic Curve Addition

The key aggregation computes the sum of a set of secp256k1 points. In order to save computation-heavy conversions from Jacobian coordinates - which are used for point addition - back to Affine coordinates - which are used to store public keys -, one can use the [madd-2007-bl](https://www.hyperelliptic.org/EFD/g1p/auto-shortw-jacobian.html#addition-madd-2007-bl) addition formula expecting one point’s `z` coordinate to be 1. Effectively allowing to add a point in Affine coordinates to a point in Jacobian coordinates.

This optimization enables computing the sum of secp256k1 points in an efficient manner by only having to convert the end result from Jacobian coordinates to Affine coordinates. Note that to convert from Jacobian coordinates to Affine coordinates the modular inverse of the `z` coordinate needs to be computed.

*A Solidity implementation can be found [here](https://github.com/chronicleprotocol/scribe/blob/main/src/libs/LibSecp256k1.sol#L153).*

### Elliptic Curve Multiplication

The Schnorr verification procedure needs to verify an elliptic curve multiplication. This computation can be done performantly by misusing the `ecrecover` precompile. For more info, see [Vitalik’s ethresear.ch post](https://ethresear.ch/t/you-can-kinda-abuse-ecrecover-to-do-ecmul-in-secp256k1-today/2384) and *Scribe*’s [documentation](https://github.com/chronicleprotocol/scribe/blob/main/docs/Schnorr.md#implementation-optimizations).
