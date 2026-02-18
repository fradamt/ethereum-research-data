---
source: magicians
topic_id: 25860
title: "EIP-8052: Precompile for Falcon support"
author: rdubois-crypto
date: "2025-10-17"
category: EIPs
tags: [postquantum]
url: https://ethereum-magicians.org/t/eip-8052-precompile-for-falcon-support/25860
views: 308
likes: 10
posts_count: 9
---

# EIP-8052: Precompile for Falcon support

# EIP for a Modular FNDSA

## Abstract

This [EIP](https://github.com/ethereum/EIPs/pull/10560) introduces two precompiles for Falcon-512 signatures. The signatures is split into two to provide both alignment with the NIST standardization and ensuring compatibility with NIST Known Answer Test (KAT) vectors and ZK-friendlyness and flexibility of the hash function.

## Motivation

Falcon (Fast Fourier Lattice-based Compact Signatures over NTRU) is one of the NIST-selected post-quantum signature schemes, designed to offer strong security guarantees against both classical and quantum attacks. Based on lattice cryptography and the Short Integer Solution (SIS) problem over NTRU lattices, Falcon provides an efficient alternative for quantum-resistant authentication.

The proposal brings Falcon verification capabilities natively into Ethereum smart contracts, enabling future-proof authentication and secure decentralized applications with compact signatures. It also use a modular approach to anticipate the ZK end game.

## Specification

### Modular Architecture: Separating Challenge Generation from Core Verification

The main difference of this proposal compared to [existing ones](https://ethereum-magicians.org/t/eip-7592-falcon-signature-verification-pre-compile/18053) is the **modular design** that separates signature verification into two distinct components:

1. HASH_TO_POINT (challenge generation)
2. FALCON_CORE (signature verification)

This separation provides significant flexibility and opens up multiple use cases:

- Standard Compliance: Using SHAKE256-based HASH_TO_POINT ensures full NIST compliance
- EVM Optimization: Using Keccak256-based ETH_HASH_TO_POINT dramatically reduces gas costs
- ZK-Friendly Future: The modular design allows future implementations to substitute challenge generation with SNARK/STARK-friendly hash functions, enabling efficient ZK proofs of Falcon signatures. A Cairo implementation using the blake2s built-in has been developped.

If adopted, this precompile will allow ZKEVM to adopt partial compliance with L1 on the core verification, but adopt efficient hashing (avoiding keccak ZKEVM DDOS).

Examples and operational contracts are also provided in the assets.

### HASH_TO_POINT Precompile (1000 gas)

The `HASH_TO_POINT` precompile implements the NIST-compliant challenge computation using SHAKE256, which:

- Computes the HashToPoint challenge according to the Falcon specification
- Takes a 32-byte message hash and 666-byte signature as input
- Returns an 897-byte polynomial challenge
- Is fully compliant with NIST KAT test vectors

This ensures that on-chain challenge generation behaves identically to the standardized cryptographic primitives — a crucial property for interoperability, auditing, and security.

## ETH_HASH_TO_POINT Precompile (1000 gas)

While the standard version uses SHAKE256 as the underlying hash function, this can be inefficient in the EVM environment since the Keccak_f permutation lacks a dedicated opcode. To address this, we introduce an alternative variant, `ETH_HASH_TO_POINT`, which:

- Replaces SHAKE256 with Keccak256 in counter mode (Keccak-PRNG)
- Reduces the computational overhead significantly by leveraging existing Keccak256 precompiles
- Keeps the algorithm semantically equivalent, but optimized for the EVM
- Maintains the same security properties while reducing gas costs

This variant is provided as a first example of HashToPoint/CORE separation, providing gas reduction for the “progressive approach” (enabling cheaper verification from today while the EIP is discussed).

(By analogy, at the moment we publish this post, secp256r1 is still not deployed with incoming Fusaka, and [solidity emulation code](https://etherscan.io/address/0x0BA5ED0c6AA8c49038F819E587E2633c4A9F428a#code#F13#L1) is still in use in several wallet such as Coinbase one.

### FALCON_CORE Precompile (2000 gas)

The `FALCON_CORE` precompile handles the core verification algorithm, which:

- Takes the challenge polynomial, public key, and signature as input
- Performs Number Theoretic Transform (NTT) operations for efficient polynomial multiplication
- Verifies the L2 norm bound to ensure signature shortness
- Returns success or failure (1 or no output)
- Estimated gas cost: 2000 gas

Importantly, this component is **independent of the hash function choice**, meaning the same core verification works with either challenge generation method.

### Total Gas cost

The full signature requires a call to both function, leading to a total 3000 (plus some negligible data handling).

## Rationale

### Comparizon with Other Signature Schemes

The choice of post-quantum signature scheme for Ethereum is not finalized and multiple candidates are being evaluated by the community.

**Falcon pros:**

- Compact signatures: Around 666 bytes for Falcon-512 (compared to 2420 bytes for ML-DSA), which is attractive for on-chain storage and gas costs
- Efficient verification: Fast verification times suitable for blockchain environments
- Moderate public key size: 897 bytes (compared to 1312 bytes for ML-DSA)

**Falcon cons:**

- Signing complexity: Falcon has higher signing complexity compared to ML-DSA, which can make generating signatures slower and more resource-intensive, especially in constrained environments
- Implementation complexity: Lattice-based signatures over NTRU require careful implementation

By contrast, [ML-DSA](https://ethereum-magicians.org/t/add-eip-ml-dsa-verification/25857) offers simpler signing and verification procedures, with larger signature sizes. This EIP provides an alternative approach that prioritizes signature compactness and verification efficiency, and is meant to be compared directly with the ML-DSA proposal to inform the community’s final decision.

The following table compares the public key and signature sizes:

| Scheme | Public key | Signature |
| --- | --- | --- |
| ML-DSA | 1312B | 2420B |
| FN-DSA | 897B | 666B |

## EIP-7932 Compatibility

The proposal specifies EIP-7932 fields (Algorithmic Transaction Types), defining:

- ALG_TYPE = 0xFA for NIST-compliant Falcon-512
- ALG_TYPE = 0xFB for EVM-friendly Falcon-512
- MAX_SIZE = 699 bytes for the signature_info container
- GAS_PENALTY ≈ 3000 gas (subject to benchmarking)

This ensures seamless integration with the emerging transaction type framework for alternative signature schemes.

### Next Steps and Community Feedback

We invite the Ethereum community to:

- Review the Draft EIP
- Experiment with the contracts
- Contribute to gas optimization efforts

Current repositories allows to use Python signers and verify signatures on-chain. All of these are public goods delivered to the community.

### Open discussion

In a first version of the EIP, a “falcon with recovery” mode was specified, in order to mimic the ecrecover APIs. For easiness of integration and testing it has been decided not to do so, but the provided smart contracts offer this extra feature.

## Reference Implementation

- NIST Falcon Specification
- Ethereum Post-Quantum Cryptography Discussion
- FALCON EIP
- FALCON SmartContracts
- FALZKON, a zkfriendly implementation of falcon

## Security Considerations

A derivation path shall be specified to standardize the way keys are generated by wallets. The value of the string is TBD.

---

## Replies

**pipavlo82** (2026-01-09):

[@rdubois-crypto](/u/rdubois-crypto) This modular split (HASH_TO_POINT vs CORE) is exactly the kind of interface boundary that prevents “benchmarking different conventions by accident”.

I especially like that you make the two tracks explicit via EIP-7932 ALG_TYPE (0xFA NIST/SHAKE vs 0xFB EVM/Keccak-CTR). That’s a clean way to keep correctness/KAT-compatibility separate from EVM cost.

One practical ask: would you be open to converging on a shared, versioned test-vector + JSON schema for the wiring layer?

- HASH_TO_POINT(FIPS-SHAKE) vectors

- HASH_TO_POINT(Keccak-CTR) vectors

- CORE-only vectors (challenge, pk, sig → ok)

with explicit domain-separation tags + fixed encoding rules.

I already maintain an XOF vector suite + CI checks to prevent drift, and I’d be happy to adapt it to Falcon/8052 so different projects can benchmark apples-to-apples.

---

**mindlapse** (2026-01-24):

Hi all, over the past few weeks I’ve been working on a Rust implementation of Falcon-512 signature verification in a fork of `revm-precompile` the precompile library used by Reth (`https://github.com/paradigmxyz/reth`). The goal is to help support and de-risk EIP-8052 by providing a concrete, test-backed implementation that aligns with the current draft spec and to help serve as a practical step forward for post-quantum signature support in the Ethereum client ecosystem.

The implementation follows the modular split between Hash-to-Point and core verification, with current support for the NIST-compliant SHAKE256 Hash-to-Point path. It is structured so it can be cleanly wired into precompiles once addresses and remaining spec details are finalized. I’m sharing it now both to make the work visible and to sanity-check and correct a few consensus-critical details before pushing further upstream.

The implementation fork is here:

`https://github.com/mindlapse/revm/tree/falcon/crates/precompile/src`

At a high level, this includes:

- A full Falcon-512 verification pipeline matching the EIP’s split between Hash-to-Point and core verification.
- Integration into revm-precompile, with fixed-cost precompile semantics aligned with existing precompiles.
- Known Answer Test coverage using the official Falcon submission package (https://falcon-sign.info/), plus ~180 additional unit tests covering encoding, NTT/INTT behavior, norm bounds, and failure cases.

Unit tests and KAT verification can be run with:

`cargo test -p revm-precompile --features falcon`

**Current status and scope**

- The Falcon core verification logic and SHAKE256 Hash-to-Point implementation are complete and passing KATs.
- The code is wired internally but not yet mapped to concrete precompile addresses, since addresses are still TBD in the EIP.
- The precompile entrypoints exist as callable APIs, but are not yet registered in any default fork set.
- The Keccak-PRNG Hash-to-Point variant is not implemented yet.

Before proceeding further, I’d appreciate clarification on a few spec details that affect consensus-critical parsing.

**Challenge polynomial padding and length**

The EIP states that the 512 coefficients (14 bits each) are concatenated and then “left-pad the final byte with zero bits to reach exactly 897 bytes.” Since 512 × 14 = 7168 bits = 896 bytes exactly, this wording is ambiguous. Could you confirm:

- Whether the challenge encoding is intended to be exactly 897 bytes, and if so,
- Whether the extra byte is a leading zero byte (i.e., the first / leftmost byte of the 897), or whether padding is expected elsewhere.

**Public key header handling**

The EIP specifies that the public key is 897 bytes in the NTT domain. In the Falcon reference implementation and KATs, the public key encoding consists of:

- a 1-byte header (0x09 for Falcon-512, since log₂(512) = 9), followed by
- 896 bytes encoding 512 coefficients at 14 bits each, ordered from coefficient 0 to 511.

In the current EIP text (and in the implementation I’ve prepared), the 896-byte tail is interpreted as a packed bitstring of 512 coefficients mapped to the NTT domain in [0, q). Could you clarify:

- Whether the precompile should require the first byte to be exactly 0x09,
- If not, whether the first byte should be required to be 0x00, or whether any value should be accepted.

At the moment, the implementation assumes the public key provided to FALCON_CORE is already in the expected NTT-domain packed form, and this detail determines whether or how the first byte should be validated.

Finally, a couple of additional clarification points that may be worth addressing explicitly in the EIP text, based on implementation experience:

- Input concatenation order for FALCON_CORE: the EIP lists signature, public key, and challenge as inputs, but an explicit byte-level layout (e.g., sig || pubkey || challenge) would remove ambiguity across clients, since precompiles simply receive a single array of bytes as input (and a gas_limit).
- Gas semantics on malformed input: the “Gas burning on error” section states that malformed inputs or decompression failures should burn all gas supplied to the call, which appears to differ from existing crypto precompiles such as ECRECOVER, where a fixed cost is charged when callable and failure is signaled via empty output. Before locking this into client implementations, could you confirm that burning all remaining call gas in these cases is the intended EVM-level behavior, and that this is meant to differ from the usual fixed-cost (i.e., bounded worst-case) precompile semantics, given the potential for unbounded gas consumption on malformed input?

Thanks for all the work that’s gone into EIP-8052 and for taking the time to review these questions. I’m very happy to iterate on the implementation, add tests, or adjust semantics as the spec evolves, and I’m keen to keep this aligned with how other clients are thinking about Falcon support.

---

**simonmasson** (2026-01-26):

Hi,

Thank you for the amazing work on Falcon! Your feedback is super valuable.

Regarding the extra byte for the `HashToPoint` output and the public key, thanks for pointing this out. It would indeed be better to remove this prefix from the public key. Since the public key is part of the calldata, its length is already determined by the calldata size. Still, the verification must follow the NIST reference implementation, where the size of the public key is checked and the verification reverts in case of an invalid polynomial size.

The same structure can be used for the output of `HashToPoint`. With this construction, both the public key and the `HashToPoint` output are 896 bytes. We will modify the EIP in consequence.

Regarding the ambiguity of the input of `FALCON_CORE`, we will modify the EIP as suggested and will also provide test vectors for this function.

For gas semantics, I’ll let [@kevaundray](/u/kevaundray) answer for this part!

Thanks again for your feedback,

Simon

---

**kevaundray** (2026-01-26):

Hi,

Thanks for the review!

On gas semantics, the intention was to be inline with 2537: [EIP-2537: Precompile for BLS12-381 curve operations](https://eips.ethereum.org/EIPS/eip-2537#gas-burning-on-error)

In this case, I think I would say that the gas burned is however much gas is supplied to the call rather than it being unbounded.

Let me know if you think we should make something clearer, or whether you disagree!

---

**mindlapse** (2026-01-30):

Hi, thanks for the clarification, that helps. I have a few updates and follow-ups.

On inputs first: I’ve updated the draft implementation I linked in my earlier post to expect **896 bytes** for both the public key and the challenge, rather than 897. This reflects the recent discussion around removing the extra header byte and seems to simplify things for both the spec and implementation.

On semantics, I wanted to ask for clarification around how an **“invalid norm bound”** is intended to be treated. From a Falcon perspective, my understanding is that failing the norm bound *is* the verification predicate itself: it corresponds to a validly encoded input where the signature simply does not verify. Because of that, it feels more natural to treat an invalid norm bound as a normal verification failure that returns no output data, rather than grouping it with structural input errors like invalid length or invalid field element encoding (≥ q). As written today, including “invalid norm bound” alongside structural input errors makes it a bit unclear whether a validly encoded but incorrect signature should be treated as an error or as a normal verification failure (with no output), similar to `ecrecover`. Some clarification there would help implementers.

On gas semantics: I understand and appreciate the intent to align with `EIP-2537`, and I’m definitely open to that approach. I mainly wanted to check whether a fixed pricing model might also make sense here. Since malformed inputs can be rejected early and cheaply, charging the same fixed cost for both valid and malformed inputs wouldn’t appear to underprice any expensive execution path. One concern I have with “burn all provided gas on error” semantics is how it may influence contract authors: in practice, I could see it pushing callers toward defensively capping the gas they forward to the precompile to avoid griefing if an invalid signature is encountered. If the Falcon precompile’s gas cost later needs to be adjusted upward, those hardcoded caps can then become a source of breakage for otherwise correct contracts. This feels somewhat reminiscent of the lessons learned around `EIP-1884`, where upward gas repricing invalidated assumptions embedded in deployed code.  Here is some relevant history:

`https://medium.com/authereum/istanbul-gas-reprice-breaks-contract-interactions-4236fdddb5e0`

None of this is meant as a strong objection to 2537-style semantics, more as an open question about whether fixed pricing might give nicer long-term ergonomics here, given the structure of the algorithm and its early-reject behavior. I mainly wanted to raise it early so we can converge on something that’s both safe and comfortable to build on.

---

**pipavlo82** (2026-01-30):

Thanks for the clarifications — this is very helpful.

I’d like to propose tightening the semantics along two axes to reduce ambiguity for implementers and clients:

1. Failure semantics (norm bound):
I agree that invalid norm bound is a verification predicate failure, not a structural input error. Treating it as a normal verification failure (no output / false), analogous to ecrecover, seems more consistent and avoids conflating “well-formed but invalid” signatures with malformed calldata (length / field encoding errors). Explicitly stating this distinction in the EIP would help client implementers.
2. Gas semantics (fixed vs burn-remaining):
Given the early-reject structure of Falcon verification, I think it’s worth explicitly choosing bounded, fixed-cost semantics (similar to other crypto precompiles), rather than “burn remaining gas” on malformed inputs.
The latter risks reintroducing EIP-1884-style breakage if assumptions about gas caps leak into deployed contracts. A fixed upper bound provides safer long-term ergonomics and makes Falcon composable with higher-level abstractions (ERC-7913 adapters, AA, zk-proxy paths).
If helpful, I’m happy to contribute:
concrete wording for the success / failure matrix (structural error vs verification failure),
test vectors that distinguish malformed inputs from valid-but-invalid signatures, and
a short rationale section comparing fixed-cost vs burn-remaining semantics in the context of Falcon’s control flow.
Looking forward to aligning this with how other clients are thinking about Falcon support.

---

**simonmasson** (2026-01-30):

Thanks for your remarks. I have updated the EIP with the remarks, and I agree that a valid-encoding signature that is rejected should not return an error. I also updated this part of the EIP.

I did not touch the gas semantics section.

Thanks for your help with this EIP!

---

**mindlapse** (2026-01-31):

Hi all, one additional update that may be useful for implementers.

I’ve put together a larger set of **Falcon-512 test vectors (10,000 signatures)** here:

https://github.com/mindlapse/falcon-vectors

These are intended to help with stress-testing decoding & verification beyond the original KAT set.

In particular, the `falcon512-KAT.rsp` file in that repo can be dropped in as a **direct replacement** for the existing KAT file currently used by the draft Falcon-512 implementation in `revm` linked above, located at:

```bash
crates/precompile/src/falcon/kat/falcon512-KAT.rsp

```

(the existing file there contains 100 signatures from the original Falcon submission package and can be swapped out for the 10000 signatures).

Once swapped in, the verification suite can be run as part of the unit test suite with:

```bash
cargo test -F falcon

```

In addition to positive verification tests, the suite also includes **negative tests over the same vector file**: for each example, a low-order byte of a randomly selected signature coefficient is flipped (so the coefficient remains within a valid range), and the test then confirms that the modified signature does *not* verify. This might be useful.

