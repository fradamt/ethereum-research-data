---
source: magicians
topic_id: 15535
title: "EIP-XXX: Ed25519 Signature Verification"
author: rdubois-crypto
date: "2023-08-24"
category: EIPs
tags: [precompile, signatures, cryptography]
url: https://ethereum-magicians.org/t/eip-xxx-ed25519-signature-verification/15535
views: 1832
likes: 10
posts_count: 5
---

# EIP-XXX: Ed25519 Signature Verification

Discussion for the addition of edDSA precompiles (ed25519 curve). Along with efficient computations, ed25519 being schnorr based provides:

- MPC friendlyness (while MPC-ECDSA schemes suffer many vulnerabilities, Musig2 remains untouched)
- zk friendlyness
- WebAuthn compatibility, enabling use of passkeys with account abstraction powered by EIP4337.
Latest modifications include a mulmuladd operation performing the operation u.P+vQ, enabling to select the hash function used outside of the precompile.

## Replies

**Mani-T** (2023-08-29):

It’s an exciting development to further expanding the possibilities for privacy-preserving transactions and applications on the blockchain.

---

**zigtur** (2023-09-13):

+1, I personally think that bringing ed15519 on Ethereum would allow more efficient computations.

It would allow zkRollups based on edDSA in a near future.

---

**rdubois-crypto** (2023-09-21):

After digging into implementation details, it appears that ed25519 as standardized requires SHA512. Also following EIP-7212 discussion ([EIP-7212: Precompiled for secp256r1 Curve Support - #39 by ccamrobertson](https://ethereum-magicians.org/t/eip-7212-precompiled-for-secp256r1-curve-support/14789/39)), it seems preferable to externalize the call to hash function to the elliptic precompile, to enable alternative hash (like poseidon) for zkp usage.

The question is now quite similar to EIP7212 ones should we choose:

- a full RFC8032 compatible precompile
- a ecrecover compatible precompile (takes h,v,r,s) as input
- a ec_mulmuladd (compute uG+vQ over Ed25519 curve) precompile?

The first one is the choice of current EIP6565, but appears to limit its use and the process seems stuck.

Preliminary implementation of curve computations is available here and one block only SHA512 is available here to be pushed as progressive precompile.

https://github.com/rdubois-crypto/FreshCryptoLib/blob/master/solidity/src/FCL_eddsa.sol.

The expensive cost of SHA512 (around 120K for now) suggests to also push a precompile for the SHA512 call, either in the same EIP, either in a distinct one.

---

**TtheBC01** (2024-10-01):

Given that passkeys support Ed25519 as an algorithm type, this precompile would be super useful for new wallet abstraction use cases:

https://www.w3.org/TR/webauthn-2/#sctn-alg-identifier

