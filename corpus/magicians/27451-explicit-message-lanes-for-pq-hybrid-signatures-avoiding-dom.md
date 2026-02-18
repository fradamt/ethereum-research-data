---
source: magicians
topic_id: 27451
title: Explicit Message Lanes for PQ & Hybrid Signatures (avoiding domain-separation wormholes)
author: pipavlo82
date: "2026-01-17"
category: Uncategorized
tags: [account-abstraction, signatures, erc-1271, erc-7913]
url: https://ethereum-magicians.org/t/explicit-message-lanes-for-pq-hybrid-signatures-avoiding-domain-separation-wormholes/27451
views: 36
likes: 2
posts_count: 1
---

# Explicit Message Lanes for PQ & Hybrid Signatures (avoiding domain-separation wormholes)

As Account Abstraction and post-quantum / hybrid signatures begin to coexist on Ethereum, we’re quietly accumulating a new class of failure that is **not cryptographic**, but semantic.

I’ll call it a **domain-separation “wormhole”**.

---

## The problem (short)

The *same* signature can be:

- cryptographically valid, yet
- replayed or reinterpreted across different verification surfaces

(e.g. ERC-1271 ↔ ERC-7913 ↔ AA `validateUserOp` ↔ future precompiles)

if the signed digest does **not explicitly bind** *where* and *how* the signature is meant to be verified.

This is replay-by-interpretation, not replay-by-nonce.

---

## Why this matters now

We are entering a transition period with:

- multiple verification surfaces,
- hybrid (ECDSA + PQ) signatures,
- multiple hash/XOF constructions,
- adapters and partial migrations.

In this environment, *implicit* domain separation becomes fragile.

---

## Proposal: Explicit Message Lanes (v0)

I propose a minimal, versioned **digest envelope** — an explicit message lane — that every signature must bind to.

**Lane envelope (v0):**

lane_version chain_id verifier_binding surface_id algo_id (incl. hash/XOF lane) payload

The signature is over the hash of this envelope.

---

## Minimal binding rules

- AA: bind verifier_binding to the EntryPoint address
- ERC-1271 / ERC-7913: bind to the verifying contract
- Precompiles: bind to a precompile identifier (address or opcode-id)

`algo_id` **must include the hash/XOF choice**, otherwise cross-XOF wormholes remain.

---

## What this is not

- Not a new signature scheme
- Not an on-chain mandate
- Not a finished standard

It’s a **spec-level invariant**:

> same cryptography, same surface semantics, same lane.

---

## Questions for feedback

1. Is EntryPoint address sufficient as verifier identity for AA?
2. For precompiles, is address-binding enough or should opcode-id be explicit?
3. Should algo_id always include hash/XOF (I think yes)?
4. Is a time-boxed v0 → v1 lane migration acceptable?

Happy to hear criticism — especially from folks working on AA, ERC-1271/7913, or PQ precompile design.
