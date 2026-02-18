---
source: magicians
topic_id: 26637
title: "[Draft ERC] RIP-009: Cross-Network Consent Verification Standard"
author: recurmj
date: "2025-11-19"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/draft-erc-rip-009-cross-network-consent-verification-standard/26637
views: 94
likes: 0
posts_count: 4
---

# [Draft ERC] RIP-009: Cross-Network Consent Verification Standard

**Author:** Mats Heming Julner (Recur Labs)

**Status:** Draft

**Type:** Standards Track (Verification)

**Created:** 2025-11-20

**Requires:** RIP-001

---

*(Note: “RIP-009” here refers to the Recur Improvement Proposal draft; not yet part of the official Rollup RIP process.)*

## Abstract

RIP-009 defines the standard for **cross-network verification of signed Authorizations**.

It specifies how an independent system B reconstructs the exact EIP-712 digest originally signed for system A, and verifies the signature **without shared state, consensus, custody, or trust assumptions**.

The core contribution is the **Cross-System Consent Universality Theorem**, which proves:

> If two independent systems compute the same (domainSeparator, structHash) pair,
> then a signature over keccak256(0x1901 || domainSeparator || structHash)
> is valid in all systems; regardless of chain, VM, consensus, or execution environment.

This invariant is denoted **κ₍c₎**, the *consent constant*.

---

## Motivation

Existing cross-chain systems rely on:

- bridges
- custodians
- oracles
- relayers
- shared consensus

These systems introduce systemic risk, centralization, and multi-billion-dollar exploits.

RIP-009 removes all of these by showing that **consent itself is portable**.

A signature, once produced, exists in *mathematical space*, not chain space.

With RIP-009, any system can independently verify consent provided it reconstructs:

1. the same structHash, and
2. the same domainSeparator.

This unlocks:

- cross-chain Authorization
- observability without bridges
- chain-to-chain pull flows
- cross-network rebalancing
- multi-domain consent portability

RIP-009 does **not** define settlement or pull semantics; those are covered by RIP-001, RIP-002, and RIP-003/004.

—-

## Specification Overview

### Authorization Structure (RIP-001)

All fields and their ordering are inherited exactly from RIP-001.

```auto
grantor: address
grantee: address
token: address
maxPerPull: uint256
validAfter: uint256
validBefore: uint256
nonce: bytes32
signature: bytes
```

### AUTH_TYPEHASH

```auto
AUTH_TYPEHASH = keccak256(
    "Authorization(address grantor,address grantee,address token,uint256 maxPerPull,uint256 validAfter,uint256 validBefore,bytes32 nonce)"
);
```

### Struct Hash

```auto
structHash = keccak256(
    abi.encode(
        AUTH_TYPEHASH,
        grantor,
        grantee,
        token,
        maxPerPull,
        validAfter,
        validBefore,
        nonce
    )
);
```

> Note: This is a minimal reference verifier. Production implementations SHOULD enforce low-s signatures (EIP-2) and MAY support EIP-1271 smart wallets and EIP-2098 compact signatures.

### Domain Separator (EIP-712)

```auto
EIP712_DOMAIN_TYPEHASH = keccak256(
    "EIP712Domain(string name,string version,address verifyingContract,uint256 chainId)"
);

domainSeparator = keccak256(
    abi.encode(
        EIP712_DOMAIN_TYPEHASH,
        keccak256(bytes(name)),
        keccak256(bytes(version)),
        verifyingContract,
        chainId
    )
);
```

Systems interoperate only if domainSeparator is identical.

---

## Cross-System Consent Universality Theorem

### Statement

If two independent systems reconstruct:

- domainSeparator = D
- structHash = S

Then for:

```auto
digest = keccak256(0x1901 || D || S)
```

we have:

```auto
Verify_A(digest, σ) == Verify_B(digest, σ)
```

for any ECDSA secp256k1 signature `σ`.

Signature validity is independent of:

- chain
- VM
- consensus
- block time
- global state

The pair `(D, S)` is the invariant **κ₍c₎**.

### Proof Sketch

1. EIP-712 digest = deterministic hash over explicit bytes
2. Signature is over digest only
3. Signature verification reduces to checking recovery of the signer
4. ECDSA verification depends only on (digest, σ, pk)
5. Therefore, if digest is equal, signature validity is equal
6. Thus consent verification is invariant across systems

Full formal proof included in **Appendix X**.

---

## Observe-and-Verify Flow

System B performs:

1. Receive Authorization fields
2. Recompute structHash
3. Recompute domainSeparator
4. Compute digest
5. Verify signature via ecrecover
6. If recovered signer equals grantor → consent is valid

No bridge, oracle, or shared state is needed.

---

## Reference Implementation

```solidity
pragma solidity ^0.8.0;

contract RecurCrossNetworkVerifier {
    bytes32 public constant AUTH_TYPEHASH =
        keccak256(
            "Authorization(address grantor,address grantee,address token,uint256 maxPerPull,uint256 validAfter,uint256 validBefore,bytes32 nonce)"
        );

    bytes32 public immutable DOMAIN_SEPARATOR;

    constructor(
        string memory name,
        string memory version,
        address verifyingContract,
        uint256 chainId
    ) {
        bytes32 EIP712_DOMAIN_TYPEHASH = keccak256(
            "EIP712Domain(string name,string version,address verifyingContract,uint256 chainId)"
        );

        DOMAIN_SEPARATOR = keccak256(
            abi.encode(
                EIP712_DOMAIN_TYPEHASH,
                keccak256(bytes(name)),
                keccak256(bytes(version)),
                verifyingContract,
                chainId
            )
        );
    }

    function verify(
        address grantor,
        address grantee,
        address token,
        uint256 maxPerPull,
        uint256 validAfter,
        uint256 validBefore,
        bytes32 nonce,
        bytes memory signature
    ) public view returns (bool) {

        bytes32 structHash = keccak256(
            abi.encode(
                AUTH_TYPEHASH,
                grantor,
                grantee,
                token,
                maxPerPull,
                validAfter,
                validBefore,
                nonce
            )
        );

        bytes32 digest = keccak256(
            abi.encodePacked(
                "\x19\x01",
                DOMAIN_SEPARATOR,
                structHash
            )
        );

        (bytes32 r, bytes32 s, uint8 v) = _split(signature);
        return ecrecover(digest, v, r, s) == grantor;
    }

    function _split(bytes memory sig)
        internal pure returns (bytes32 r, bytes32 s, uint8 v)
    {
        require(sig.length == 65, "BAD_SIG");
        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }
    }
}
```

---

## Formal Derivation

Appendix X provides a full formal derivation of the **Cross-System Consent Universality Theorem**, with lemmas on:

- encoding determinism
- digest equivalence
- ECDSA invariance

This demonstrates that consent validity is **network-agnostic** as long as (domainSeparator, structHash) are preserved.

---

## Request for Comments

RIP-009 is intended to become a foundational standard for:

- cross-chain consent
- multi-domain Authorization
- off-chain verifiers
- multi-chain payment flows
- programmable treasury systems

Feedback requested on:

- boundary conditions
- domain separator namespacing
- revocation semantics
- cross-network replay rules
- off-chain verifier behavior

---

## Reference

https://github.com/recurmj/recur-standard/blob/main/docs/RIP-009.md

## Replies

**Ankita.eth** (2025-11-20):

Interesting proposal the core idea makes sense, but a few things need tightening before this can be safely adopted across domains:

1. Domain Separator Collisions
Right now the spec assumes all systems will perfectly align on name, version, and verifyingContract. That’s fragile.

- How do we prevent accidental or malicious collisions?
- Should the domain include an explicit namespace or unique identifier for multi-chain deployments?

1. Replay Semantics Need Clarity
Since the same signature can be valid on multiple chains, what’s the recommended replay model?

- Should nonces be global?
- Per-network?
- Or should the spec explicitly discourage multi-use signatures?

1. Revocation Is Underspecified
Once consent is signed, how does a system know when it’s revoked?

- Off-chain revocation?
- Chain-specific revocation registries?
Without a standard here, portability is risky.

1. EIP-1271 Behavior Across Chains
Smart contract wallets may have different code or versions on different chains.

- Should RIP-009 define expected 1271 behavior for multi-chain setups?
Otherwise a signature could verify on one chain and fail elsewhere.

1. Version Migration
What happens when the verifying contract upgrades?

- Does the domainSeparator change?
- Do old signatures become invalid on some chains but not others?

1. Interplay With ERC-7964
There is overlap around “universal” EIP-712 domain semantics.

- Should RIP-009 explicitly define how it relates or differs?
- Or adopt parts of 7964 to avoid parallel standards?

---

**recurmj** (2025-11-20):

Thanks for the thoughtful review. All six points are valid, and I agree each needs explicit treatment in the final draft. Here’s how RIP-009 intends to scope them:

## 1. Domain Separator Collisions

RIP-009 intentionally specifies verification only:

“If two systems derive the same (domainSeparator, structHash),

they must reach the same verdict.”

It does not prescribe domain construction.

Two practical options are emerging:

a. Logical namespaces:

Use a globally unique name/version (e.g. “RecurPPO”, “1”), and treat verifyingContract + a logical chainId namespace as part of the identity.

b. ERC-7964 semantics:

chainId: 0 is a valid special case for account-centric universality.

I will add a “Domain Namespacing” subsection recommending implementers include a globally unique identifier and choose either the logical-namespace or 7964-style pattern depending on use case.

## 2. Replay Semantics

RIP-009 does not define replay policy.

It only defines how a signature is verified across systems.

Replay prevention comes from:

- the per-Authorization nonce (RIP-001), and
- an optional Consent Registry (RIP-002) that tracks usage/revocation.

Implementers may choose:

- global nonces (shared registry),
- per-chain nonces,
- or one-time signatures.

I will add a “Replay Model” note clarifying that applications SHOULD pair RIP-009 with nonce + registry semantics appropriate for their domain.

## 3.  Revocation

Agreed this must be explicit.

The intended composition is:

- RIP-001 — Authorization definition
- RIP-002 — Revocation / usage registry
- RIP-009 — Cross-system verification of the same Authorization

Revocation is keyed by:

```auto
authHash = keccak256(Authorization)
```

Any system consulting the same registry reaches the same liveness verdict.

I will add a “Relationship to RIP-002” section making this explicit.

## 4. EIP-1271 Across Chains

Correct, 1271 divergence can produce inconsistent outcomes.

RIP-009’s invariant is:

> given a verifier that implements secp256k1 or 1271 semantics,
> identical (D, S) ⇒ identical verdict.

To avoid cross-chain 1271 divergence, implementers should:

- deploy identical 1271 code at the same address across chains or
- treat 1271 wallets as chain-local and avoid reusing domains across networks.

I will add a short subsection: “1271 and Multi-Chain Deployments”.

## 5. Version Migration

When verifyingContract or version changes, the domainSeparator changes; old signatures remain valid only under the old domain.

This is intentional, and mirrors EIP-712 practice.

Upgrades = new domain.

Registries may provide migration/deprecation paths.

I’ll add a “Versioning” note clarifying this.

## 6. Relationship to ERC-7964

Thank you for raising this. 7964 is relevant.

The way I see the split:

ERC-7964 defines one specific cross-chain domain policy (chainId: 0, account-centric, AA-focused). RIP-009 formalizes the general invariant underlying all such policies:

> equality of (domainSeparator, structHash) ⇒ equality of signature validity across systems.

Thus 7964 is one valid instantiation of a domain policy that satisfies RIP-009’s theorem.

I will add a “Relation to ERC-7964” section noting that 7964 is compatible and can be used as a domain strategy.

## Closing

RIP-009 stays deliberately narrow:

it standardizes the verification primitive, not the entire policy layer around it.

Happy to refine the draft to incorporate all six points.

---

**recurmj** (2025-12-04):

## Update: Revised RIP-009 Draft (Feedback Applied)

Thanks again for the thoughtful review. I’ve now completed a full revision of the RIP-009 draft based on the feedback in this thread. The updated version focuses strictly on the verification invariant and removes all unnecessary framing.

Below is a summary of the changes.

---

### 1. Removed non-essential framing

The earlier draft included broader architectural language that wasn’t necessary for a verification standard.

RIP-009 is now scoped strictly to:

- the equivalence condition
- digest reconstruction requirements
- signature-verification rules across systems

No additional interpretation or narrative is included.

---

### 2. Added explicit domain namespacing guidance (feedback #1)

The revised draft now discusses:

- globally unique domain naming conventions,
- logical namespace strategies, and
- compatibility with ERC-7964 for universal domain semantics.

This clarifies how to avoid unintentional domain collisions.

---

### 3. Clarified replay semantics (feedback #2)

RIP-009 now explicitly states that:

- replay prevention is not defined within this standard, and
- replay protection must come from RIP-001 (nonce), RIP-002 (registry), or the application layer.

RIP-009 only standardizes verification equivalence.

---

### 4. Added explicit revocation/liveness clarification (feedback #3)

A new section explains that:

- verification equivalence ≠ authorization liveness,
- revocation and usage tracking are defined by RIP-002, and
- systems must consult a registry to determine whether an Authorization is active.

---

### 5. Added EIP-1271 cross-chain considerations (feedback #4)

The updated text explains that:

- 1271 wallet implementations may differ across chains,
- multi-chain deployments should use identical code at identical addresses, or
- treat 1271 verification as chain-local and avoid domain reuse.

This avoids ambiguous verification outcomes.

---

### 6. Added versioning rules (feedback #5)

The draft now clearly states that:

- changing name, version, verifyingContract, or chainId
MUST produce a new domainSeparator.

Old signatures remain valid only under the former domain.

This is consistent with standard EIP-712 practice.

---

### 7. Added explicit relationship to ERC-7964 (feedback #6)

The updated draft clarifies:

- ERC-7964 defines one valid domain-policy strategy,
- RIP-009 defines the general invariant that applies to all strategies, and
- implementers may choose 7964 or an application-defined domain policy.

---

### 8. Reduced the normative surface to a single requirement

The revised RIP-009 now expresses one core rule:

> If (domainSeparator, structHash) match, verification results must match.

Everything else (domain rules, replay, revocation, trust assumptions) is explicitly delegated or left to implementers.

This aligns with Ethereum’s minimal EIP philosophy.

---

### 9. Added a separate technical explainer

Alongside the rewrite, I published a companion document:

**“Cross-System Authorization Identity”**

which formalizes the equivalence condition without any framing beyond the math.

---

###  Updated Draft

The revised RIP-009 draft is here:



      [github.com/recurmj/recur-standard](https://github.com/recurmj/recur-standard/blob/main/docs/RIP-009.md)





####

  [main](https://github.com/recurmj/recur-standard/blob/main/docs/RIP-009.md)



```md
# RIP-009: Cross-System Authorization Verification

**Category:** Standard Track — Core
**Status:** Draft
**Author:** Recur Labs
**Dependencies:** RIP-001, RIP-002, EIP-712
**Created:** 2025

---

Formal companion:
[Cross-System Authorization Identity](https://github.com/recurmj/recur-standard/blob/main/docs/cross-system-authorization-identity.md)

---

## 1. Abstract

RIP-009 defines the **verification invariant** for EIP-712–based Authorization objects (from RIP-001) across heterogeneous systems.

It does **not** set replay rules, domain construction, revocation semantics, or trust models.
```

  This file has been truncated. [show original](https://github.com/recurmj/recur-standard/blob/main/docs/RIP-009.md)










Happy to continue iterating, the review here has significantly improved clarity, scope fit, and implementability. Thanks again for the detailed feedback.

