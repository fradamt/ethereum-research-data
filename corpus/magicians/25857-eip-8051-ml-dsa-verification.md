---
source: magicians
topic_id: 25857
title: "EIP-8051: ML-DSA verification"
author: simonmasson
date: "2025-10-17"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8051-ml-dsa-verification/25857
views: 454
likes: 11
posts_count: 6
---

# EIP-8051: ML-DSA verification

# Introducing an Ethereum Integration Proposal for ML-DSA Signatures

## Abstract

We are introducing an Ethereum Integration Proposal for ML-DSA signatures, aligning with the [FIPS 204 standard](https://csrc.nist.gov/pubs/fips/204/final) and ensuring compatibility with NIST Known Answer Test (KAT) vectors.

## Motivation

ML-DSA (Module Lattice–based Digital Signature Algorithm) is one of the NIST-selected post-quantum signature schemes, designed to offer strong security guarantees against both classical and quantum attacks.

Our proposal brings ML-DSA verification capabilities natively into Ethereum smart contracts, enabling future-proof authentication and secure decentralized applications.

## Specification

### The MLDSA_VERIFY contract (4500 gas)

To make this practical on-chain, we developed the MLDSA_VERIFY smart contract, which:

- Implements ML-DSA verification according to FIPS 204,
- Is fully compliant with NIST KAT test vectors,
- Uses the same hash functions and parameters as the reference standard.

This ensures that on-chain verification behaves identically to the standardized cryptographic primitives — a crucial property for interoperability, auditing, and security.

### The MLDSA_VERIFY_ETH contract (4500 gas)

While the standard version uses SHAKE256 as the underlying hash function, this can be inefficient in the EVM environment.

To address this, we introduce an alternative variant, MLDSA_VERIFY_ETH, which:

- Replaces SHAKE256 with Keccak256 in counter mode,
- Reduces the computational overhead significantly,
- Keeps the algorithm semantically equivalent, but optimized for the EVM.

This change allows ML-DSA verification to run more efficiently on-chain while maintaining cryptographic soundness.

## Rationale

### Comparison with other signature schemes

The choice of post-quantum signature scheme for Ethereum is not finalized and multiple candidates are being evaluated by the community..

Falcon, as implemented in [DRAFT EIP](https://github.com/ethereum/EIPs/pull/10560), produces smaller signatures — around 666 bytes for an equivalent security level — which is attractive for on-chain storage and gas costs.

However, it also has higher signing complexity, which can make generating signatures slower and more resource-intensive, especially in constrained environments.

By contrast, ML-DSA offers simpler signing and verification procedures, with a slightly larger signature size. This EIP provides an alternative approach that balances efficiency, on-chain performance, and post-quantum security, and is meant to be compared directly with EIP-9999 to inform the community’s final decision.

The following table compares the public key and signature size for ML-DSA and FN-DSA:

| Scheme | Public key | Signature |
| --- | --- | --- |
| ML-DSA | 1312B | 2420B |
| FN-DSA | 897B | 666B |

## EIP-7932 Compatibility

The proposal specifies EIP-7932 fields (Algorithmic Transaction Types), defining:

- ALG_TYPE = 0xD1 for NIST-compliant ML-DSA
- ALG_TYPE = 0xD2 for EVM-friendly ML-DSA
- MAX_SIZE = 2420 bytes for the signature_info container
- GAS_PENALTY ≈ 4500 gas (subject to benchmarking)

This ensures seamless integration with the emerging transaction type framework for alternative signature schemes.

## Next Steps and Community Feedback

We invite the Ethereum community to:

- Review the technical specification and implementation
- Provide feedback on the tradeoffs between ML-DSA and other post-quantum schemes
- Test the contracts in various use cases
- Contribute to gas optimization efforts

Current repo allow to use python signer and verify onchain signatures. In the next days a hardware implementation (non genuine Ledger application) will be provided to experiment wallet integration. All those are public good delivered to the community.

## Additional Resources

- NIST Post-Quantum Cryptography Standardization
- FIPS 204: Module-Lattice-Based Digital Signature Standard
- Ethereum Post-Quantum Cryptography Discussion
- EIP-DRAFT: Falcon Signature Verification
- EIP-DRAFT: Dilithium Signature Verification
- ZKNOX solidity implementation

## Replies

**SirSpudlington** (2025-10-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/simonmasson/48/16253_2.png) simonmasson:

> ## EIP-7932 Compatibility
>
>
>
> Our proposal is fully compatible with EIP-7932 (Algorithmic Transaction Types), defining:
>
>
> ALG_TYPE = 0xFA for NIST-compliant Falcon-512,
> ALG_TYPE = 0xFB for EVM-friendly Falcon-512,
> MAX_SIZE = 699 bytes for the signature_info container,
> GAS_PENALTY ≈ 3000 gas (subject to benchmarking).
>
>
> This ensures seamless integration with the emerging transaction type framework for alternative signature schemes.

Author of EIP-7932 here. It is really awesome to see people adopting the 7932 framework. I have just a couple *minor* issues with the implementation:

- The verify function was updated to return the full public key instead of the address. (This should be as easy as just removing return ExecutionAddress(keccak256(pubkey)[12:]) and adding return pubkey.
- I’d recommend moving the EIP-7932 algorithm definition into the Specification section. According to the Template EIP, the Backwards Compatibility section of an EIP is for documenting potential incompatibilities. I don’t believe you can define new parts of the specification in there.
- Edit: Also for clarification, ALG_TYPE and the first byte of signature_info are not the same thing. They are handled separately.

Other than those two issues, this (and EIP-8052) seem like a good step towards post-quantum readiness on Ethereum.

---

**simonmasson** (2025-11-01):

Thanks for your feedbacks. I have updated the EIPs with the whole public key, moved to the specification section.

---

**SirSpudlington** (2025-12-29):

I was considering to submit a PR to update EIP-8051 / EIP-8052 with the new EIP-7932 interface format, but I have some questions about the current implementation, namely, what does the `lookup_pubkey` function do? And why does EIP-8052 use an undefined variable `pubkey_hash`?

Any clarification would be appreciated.

---

**pipavlo82** (2026-01-04):

Hi — thanks for posting this.

Quick question about the stated gas numbers. The post mentions an `MLDSA_VERIFY` (and `MLDSA_VERIFY_ETH`) contract at **~4500 gas**, and also a **GAS_PENALTY ≈ 4500**.

Can you clarify what surface that number refers to?

1. Is ~4500 gas intended as a precompile/native cost model, or a very narrow micro-surface (e.g., container parsing / EIP-7932 dispatch), rather than full on-chain verification?
2. If a precompile is assumed: do you have a canonical ABI / input container you want implementers to converge on (so different projects benchmark the same convention)?

I’m collecting reproducible, provenance-pinned EVM benchmarks across surfaces (sig-only vs ERC-1271 vs AA) here:

[https://github.com/pipavlo82/gas-per-secure-bit](https://github.com/pipavlo82/gas-per-secure-bit?utm_source=chatgpt.com)

Happy to align on shared test vectors / ABI conventions so we don’t accidentally compare different conventions.

---

**simonmasson** (2026-01-30):

Hi,

From now, the gas estimation is a simple approximation of the cost. This can be refined if it is not accurate.

About the new EIP-7932 interface, `pubkey_hash` is a mistake and it would be awesome to have an updated version. Thank you for your help in advance.

