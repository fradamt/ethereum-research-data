---
source: magicians
topic_id: 27419
title: "Explicit Message Lanes for AA + PQ: Preventing Domain-Separation “Wormholes”"
author: pipavlo82
date: "2026-01-12"
category: ERCs
tags: [erc, evm, wallet, account-abstraction]
url: https://ethereum-magicians.org/t/explicit-message-lanes-for-aa-pq-preventing-domain-separation-wormholes/27419
views: 26
likes: 1
posts_count: 1
---

# Explicit Message Lanes for AA + PQ: Preventing Domain-Separation “Wormholes”

**TL;DR**

As AA + PQ/hybrid signatures become practical deployment targets, we risk domain-separation **“wormholes”**: *replay-by-interpretation across surfaces*.

I propose a **versioned digest envelope** that MUST bind:

- domain_tag (lane version / DOMAIN_TAG)
- chainId
- verifierBinding
- surface_id
- algo_id (including hash/XOF lane)
- payload (surface-defined)

For AA, binding to the **EntryPoint address** as verifier identity is the minimal deployable rule.

This also makes benchmarks reproducible (“same lane, same semantics”).

---

## Reminder: why this matters

We’re entering a transition where **Account Abstraction (AA)** and **post-quantum / hybrid signatures** are both real deployment targets. That creates a combinatorial explosion of verification surfaces:

- aa::validateUserOp
- sig::erc1271
- sig::erc7913
- sig::protocol (precompile/protocol-facing)

A signature can be cryptographically strong (PQ at 192–256-bit), yet become a “strong door in a weak frame” if the signed statement is **lane-ambiguous** and can be replayed/reinterpreted in another context.

### Concrete example (classical → AA)

A signature produced for an **ERC-1271 “login”** message can be reinterpreted as an **AA authorization** if the digest does not bind the intended surface and verifier identity (replay-by-interpretation).

This is also a benchmarking problem: without explicit lanes, “gas per verify” (and therefore gas-per-secure-bit) can silently compare **different semantics**.

---

## Proposal: make the message lane explicit (minimum bar)

Treat the signed/verified digest as a **versioned, domain-separated envelope** that binds:

1. a versioned domain tag
2. chain + verifier identity
3. the verification surface
4. algorithm/mode identifier (including hash/XOF lane)
5. surface-defined payload

### Sketch

```auto
digest = keccak256(abi.encode(
  DOMAIN_TAG,       // e.g. "EVM_SIG_LANE_V0"
  block.chainid,
  verifierBinding,  // verifyingContract OR protocol binding (precompile id)
  surface_id,       // aa::validateUserOp / sig::erc1271 / sig::erc7913 / sig::protocol
  algo_id,          // e.g. mldsa65_fips204_shake256_v0, falcon1024_keccakctr_v0, hybrid(...)
  payload           // surface-defined
));

```

Intent: **no lane ambiguity → no replay-by-interpretation**.

---

## Payload intuition (surface-defined)

- AA: payload can be EntryPoint.getUserOpHash(userOp) plus whatever the AA surface already commits to.
- ERC-1271: payload is typically the hash passed to isValidSignature(hash, sig).
- Protocol/precompile: payload is defined by the precompile ABI / tx envelope.

---

## Canonical hybrid ordering (avoid “same logic, different digest”)

Hybrid modes must be canonicalized. Otherwise `ecdsa+mldsa65` vs `mldsa65+ecdsa` becomes a semantic footgun and creates “fake algorithm diversity” in benchmarks.

Minimum rule:

- represent hybrids as an ordered set under a fixed canonicalization rule

 e.g., lexicographic ordering of canonical algo_id strings
- or registry-defined ordering

Example canonical form:

```auto
hybrid(ecdsa_secp256k1, mldsa65_fips204_shake256_v0)

```

---

## Upgradeability: lane versioning and migration

Versioned domain tags are deliberate: changing lane semantics should be explicit.

Practical guidance:

- verifiers/wallets MAY accept multiple lane versions concurrently (V0 and V1) under an explicit policy (allowlist/timebox)
- new signatures SHOULD target the latest lane version

Note: a future V1 could extend chain binding (e.g., include genesis/fork identifier) without changing the envelope shape.

---

## AA specifics: bind to EntryPoint identity to avoid schema drift

For AA, a main wormhole is **schema/wrapper drift** (e.g., EntryPoint v0.7 vs v0.8).

A minimal deployable rule:

- verifierBinding = EntryPoint address
- surface_id = aa::validateUserOp (no version suffix required)

Rationale: the EntryPoint address is a de-facto version identifier.

If EntryPoint is upgradeable/proxied, then versioning must become explicit (surface suffix or version field in payload) to avoid “sign against one schema, verify against another”.

Also: wallets **MUST NOT** attempt verification across multiple EntryPoints for the same statement; that reintroduces lane ambiguity.

---

## Protocol-facing surfaces (precompiles / EIP-7932-style)

For protocol-facing verification, `verifierBinding` can be:

- the reserved precompile address, or
- another agreed identifier (e.g., bytes32 domain tag)

If the precompile is parameterized (multiple modes/configs), then:

- verifierBinding + algo_id MUST uniquely determine semantics
Otherwise “one precompile with multiple behaviors” becomes another wormhole source.

---

## algo_id MUST include hash/XOF lane

I believe `algo_id` MUST include the hash/XOF lane (e.g., `*_shake256` vs `*_keccakctr`) to prevent semantic and cost drift.

This matters for:

- correctness/security assumptions (FIPS SHAKE vs custom Keccak-CTR-style XOF)
- benchmarking (hash lane can dominate cost)

---

## Questions for feedback

1. AA: is verifierBinding = EntryPoint address + surface_id = aa::validateUserOp sufficient in practice, or should we add an explicit EntryPoint version field in the envelope/payload?
2. Protocol/precompile surfaces: is verifierBinding = reserved precompile address the preferred verifier identity convention?
3. Should algo_id always include hash/XOF lane as a hard requirement?

If this direction resonates, I plan to codify it as a short methodology note for **reproducible benchmarking** (gas-per-secure-bit datasets), so vendors don’t accidentally benchmark different semantics.
