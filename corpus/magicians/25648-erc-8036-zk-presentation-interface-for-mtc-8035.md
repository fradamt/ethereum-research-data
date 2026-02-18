---
source: magicians
topic_id: 25648
title: "ERC-8036: ZK Presentation Interface for MTC (8035)"
author: y_hoshino
date: "2025-10-02"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8036-zk-presentation-interface-for-mtc-8035/25648
views: 59
likes: 0
posts_count: 2
---

# ERC-8036: ZK Presentation Interface for MTC (8035)

MTC-ZK defines an optional, fixed Groth16-style ABI (`proveMetric`) to verify **predicates only** (e.g., score ≥ threshold) against MTC Core (ERC-8035) anchors—without revealing raw values.

**Problem & motivation**

dApps often need threshold checks while preserving privacy and supporting revocation at scale. MTC-ZK provides a stable verifier ABI and binding rules so wallets/dApps can verify the same predicate the same way.

**Scope**

- proveMetric(a,b,c,publicSignals) with fixed order [mode, root, nullifier, addr, threshold, leaf]
- Binding (MUST): root == leafFull (current Core anchor), tokenId == tokenIdOf(address(uint160(addr)))
- Policy (MUST): mode allowed by Core mask; mask mismatch and mode == 0 revert
- Domain separation (circuit): treeLeaf = Poseidon(leaf, addr, keccak256(abi.encode(chainid(), address(this))))
- ERC-165 compliance (MUST)
- Optional events: VerifierSet, ProofVerified

**Comparison semantics**

GT: value > threshold; LT: value < threshold; EQ: value == threshold (inclusive).

**Draft EIP (EIP-1 compliant)**



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1234)














####


      `master` ← `YutaHoshino:feat/mtc-zk`




          opened 05:20PM - 02 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/13161055?v=4)
            YutaHoshino](https://github.com/YutaHoshino)



          [+140
            -0](https://github.com/ethereum/ERCs/pull/1234/files)







The following PR has been split.
https://github.com/ethereum/ERCs/pull/1229

[…](https://github.com/ethereum/ERCs/pull/1234)Summary
MTC-ZK defines an optional, fixed Groth16-style ABI (`proveMetric`) to verify **predicates only** (e.g., score ≥ threshold) against MTC Core anchors—without revealing raw values.

Files: EIPS/eip-8036.md

Discussion: https://ethereum-magicians.org/t/erc-8036-zero-knowledge-presentation-interface-for-multitrust-credential-8035/25648












**Reference implementation (non-normative)**



      [github.com/hazbase/contracts](https://github.com/hazbase/contracts/blob/main/verifier/circom-zk/circuit.circom)





####

  [main](https://github.com/hazbase/contracts/blob/main/verifier/circom-zk/circuit.circom)



```circom
pragma circom 2.1.8;

include "poseidon.circom";
include "mux1.circom";
include "bitify.circom";

template GEQ32() {
    signal input  a;           // 0 … 2^32-1
    signal input  b;
    signal output out;         // 1 ⇔ a ≥ b

    signal diff;
    diff <== a + (1 << 33) - b;        // 0 … 2^33 + 2^32 − 2

    component bits = Num2Bits(34);
    bits.in <== diff;

    out <== bits.out[33];
}

```

  This file has been truncated. [show original](https://github.com/hazbase/contracts/blob/main/verifier/circom-zk/circuit.circom)












      [github.com/hazbase/contracts](https://github.com/hazbase/contracts/blob/main/verifier/circom-zk-group/circuit.circom)





####

  [main](https://github.com/hazbase/contracts/blob/main/verifier/circom-zk-group/circuit.circom)



```circom
pragma circom 2.1.8;

include "poseidon.circom";
include "mux1.circom";
include "bitify.circom";

/**************************************************
 * MerkleProof — fixed-depth Merkle inclusion check
 *  - `indices` are boolean (0: left, 1: right)
 **************************************************/
template MerkleProof(n) {
    signal input root;
    signal input leaf;
    signal input siblings[n];
    signal input indices[n];

    component hashers[n];
    signal cur[n + 1];
    cur[0] <== leaf;

```

  This file has been truncated. [show original](https://github.com/hazbase/contracts/blob/main/verifier/circom-zk-group/circuit.circom)










**Related**

Core discussion: [ERC-8035: MultiTrust Credential (MTC) — Core](https://ethereum-magicians.org/t/erc-8035-multitrust-credential-mtc-core/25526)

**Feedback**

As this is our initial draft, we’d greatly appreciate broad feedback—on terminology, spec clarity, and interop. Suggestions and alternatives are welcome.

## Replies

**y_hoshino** (2025-12-17):

Based on the [discussion](https://ethereum-magicians.org/t/erc-8035-multitrust-credential-mtc-core/25526/4), the draft now formally includes an **additive ZK presentation extension** while keeping the original fixed Groth16 interface intact.

[ChangeLog](https://github.com/ethereum/ERCs/pull/1234/commits/ba2a8ea2cef090227bb85fd0658d0b911e3c3ff7)

Key updates:

- Introduced an additive interface (IMultiTrustCredentialZKEx) for richer predicates.
- Formally defined RANGE and DELTA (epoch-based) predicate semantics as OPTIONAL extensions.
- Clarified that the original fixed ABI remains the stable baseline (v1), preserving backward compatibility.
- Unified binding rules (anchor binding, address binding, comparison mask enforcement, and domain separation) across both the base and extended interfaces.
- Clarified mode semantics as a bitmask (GT/LT/EQ), with mode == 0 allowed only for KYC-only proofs.

Many thanks to [allfinan](https://ethereum-magicians.org/u/allfinan) for the thoughtful feedback and suggestions around range predicates, delta constraints, and epoch-based freshness.

The intent remains to keep MTC Core minimal, while allowing credit- and risk-oriented logic to evolve cleanly at the presentation layer.

Feedback on the extended predicate model and interface shape is very welcome.

