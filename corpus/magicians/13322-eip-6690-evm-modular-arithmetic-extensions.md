---
source: magicians
topic_id: 13322
title: "EIP-6690: EVM Modular Arithmetic Extensions"
author: jwasinger
date: "2023-03-15"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-6690-evm-modular-arithmetic-extensions/13322
views: 2610
likes: 2
posts_count: 6
---

# EIP-6690: EVM Modular Arithmetic Extensions

This is the discussion thread for EIP-6690 (EIPs repository [pull request](https://github.com/ethereum/EIPs/pull/6690), [viewable markdown file](https://github.com/jwasinger/EIPs/blob/evmmax-no-eof/EIPS/eip-6690.md)).  This is is adapted from [EIP-6601](https://ethereum-magicians.org/t/eip-6601-evm-modular-arithmetic-extensions-evmmax/13168) and modifies the spec so that it does not require EOF as a dependency.

## Replies

**jwasinger** (2023-04-05):

Moving conversation from the EIP PR to this thread:

I wrote:

> … I think a good first step would be to collect more desired use-cases (curves, zk-friendly hash functions, zkp schemes, etc.) and analyze them. So I would be curious from to hear from the AA side: what additional curves (and curve operations) would be most important to you for unlocking new use-cases?

[@dror](/u/dror) replied:

> The most important curve is sec256r1.
> This curve is standardized and supported by secure enclaves on various devices (iPhones, Android, macos) and have standard a opis on those devices, as on common browsers.
>
>
> Existing evm code to verify the signature is roughly 600k gas, which is too expensive for general use.
> It would be desirable to have it cost roughly as
> Sec256k1 (evrecover), and then it could become a few facto standard signature.

The ecrecover precompile is priced to match the performance of optimized native code with handwritten assembly for hot paths. I think that creating an EVM implementation comparable in price is out of the question.

Based on the algorithm I found [here](https://cryptobook.nakov.com/digital-signatures/ecdsa-sign-verify-messages#ecdsa-verify-signature), I predict that the cost for a straightforward EVM implementation (with room for optimization) would be ~73810 gas.

### Rationale:

The algorithm requires 2 point multiplications, 1 point addition and 2 modular inverses (we have to do an additional inverse at the end to convert the final result point from projective to affine coordinates)

note: cost for 256bit `ADDMODX`/`SUBMODX`, `MULMONTX` is 1 and 2 gas respectively.  This is the same as 321-384 bit widths because it is priced aggressively compared to 193-256 bit widths.

#### Point Multiplication/Addition

estimated cost for variable-point sec256r1 multiplication is 36344 gas.  The cost of point addition is 42 gas.

Assuming the implementation double-and-add algorithm, the scalar is 255 bits (?) in size with roughly equal number of 1s and 0s in binary representation:

- take algorithms 1 and 3 for point addition/doubling from this paper
- Extrapolate from my bls12-381 implementation of point multiplication:

255 doubles, 127 additions
- compared to bls12381 formulas:

point double has 16 more ADDMODX/SUBMODX, 3 more MULMODX
- point addition has 1 more ADDMODX/SUBMODX, 3 less MULMODX

`total_cost = bls12_381_cost + extra_cost = 32137 + 4207 = 36344` gas

When the point is fixed (as is the case with one of the multiplications), there are optimizations that can reduce the cost significantly.  In the case of bls12-381, I estimated that using the windowed optimization [here](https://crypto.stackexchange.com/a/82015) with a window size of 4 would cost ~20000 gas.

#### Modular inverse:

Cost per modular inverse is 540 gas.

We can do it with a modular exponentiation (via Fermat’s Little Theorem).  For sec256r1 I computed an addition chain which requires 270 multiplications ([example](https://github.com/jwasinger/evmmax-bls12-381/tree/main/templates/invmod) for bls12-381).

---

**jwasinger** (2023-04-05):

Whoops.  I referenced ecdsa verify instead of [ecrecover](https://crypto.stackexchange.com/a/18106).  Looks like they do mostly the same thing though.

---

**odysseus0** (2023-04-19):

Hi [@jwasinger](/u/jwasinger), just trying to make sure I understand what you mean.

You are saying that with EVMMAX, a straightforward EVM implementation of secp256r1 curve would be ~73810 gas right?

---

**jwasinger** (2023-04-21):

Yes.  Based on the cost model in the EIP, an implementation of secp256r1 ecrecover that doesn’t make use of any optimizations for elliptic curve multiplication should be roughly that amount (give or take a few thousand gas).

---

**odysseus0** (2023-04-28):

Would love to invite you to join a group of account abstraction builders who are actively pushing for supporting additional elliptic curves on EVM. Please feel free to DM me on Twitter @odysseus0z

