---
source: magicians
topic_id: 27135
title: "ERC-8103: Permissioned Authorization Object"
author: recurmj
date: "2025-12-12"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8103-permissioned-authorization-object/27135
views: 52
likes: 2
posts_count: 3
---

# ERC-8103: Permissioned Authorization Object

This thread proposes a new ERC defining a **Permissioned Authorization Object**:

a portable, revocable EIP-712 authorization struct for bounded pull-based transfers.

This ERC focuses **only** on the authorization primitive itself. Execution semantics are defined separately (see ERC-8102: Permissioned Pull).



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recurmj/48/16307_2.png)

      [ERC-8102: Permissioned Pull](https://ethereum-magicians.org/t/erc-8102-permissioned-pull/25931) [ERCs](/c/ercs/57)




> Author: Mats Heming Julner (Recur Labs)
> Status: Draft
> Type: Standards Track (Verification)
> (Note: “RIP-001” here refers to the Recur Improvement Proposal draft; not yet part of the official Rollup RIP process.)
> Sharing this draft based on recent discussion with Ethereum Foundation contributors around formalizing the permissioned-pull primitive as an ERC-level standard.
> Feedback on structure, naming, and security model is warmly welcome before moving toward ERC-A / ERC-B drafts.
> Abstract
> Th…

---

## Summary

A **Permissioned Authorization Object (PPO)** is an off-chain signed authorization that allows a grantee to pull ERC-20 tokens from a grantor under explicit constraints:

- who may pull (grantee)
- which token
- maximum amount per pull
- validity window
- single-use nonce (revocable prior to execution)

PPOs are:

- signed off-chain (EIP-712),
- revocable before use,
- executor-agnostic,
- portable across chains and systems that adopt the same struct,
- compatible with existing ERC-20 tokens (no token changes required).

This ERC does **not** define how pulls are executed on-chain. That responsibility lives in a companion standard (ERC-8102).

---

## Motivation

Existing primitives do not provide a clean, general authorization object for *retrieving* value by consent.

Today we have:

- transfer — one-shot push
- approve / transferFrom — persistent allowances (often infinite, token-state-bound)
- permit (EIP-2612) — signature-based approvals, but tightly coupled to token contracts

What’s missing is a **chain-agnostic authorization object** that:

- encodes bounded consent in a single signed payload,
- is easy for wallets and AA stacks to surface and revoke,
- can be verified by any compliant executor,
- composes with any ERC-20 without requiring token changes,
- cleanly separates authorization from execution.

This ERC specifies that missing authorization primitive.

---

## Specification

### EIP-712 Authorization Type

```plaintext
Authorization(
  address grantor,
  address grantee,
  address token,
  uint256 maxPerPull,
  uint256 validAfter,
  uint256 validBefore,
  bytes32 nonce
)
```

## Replies

**0xTraub** (2025-12-15):

I’m intrigued by the idea of a more general purpose authorization scheme for token approvals. Can you elaborate on how this is an improvement over say the `Permit2` Library for signed token approvals?

Would this be implemented similarly using a contract to track and enable approvals and authorizations?

---

**recurmj** (2025-12-23):

Great question. Permit2 is a useful comparison point.

The key distinction is that ERC-8103 defines a general authorization object, not an approval system or registry.

Permit2 is an opinionated implementation:

• approvals are ultimately modeled as allowances,

• state lives in a canonical Permit2 contract,

• execution is routed through that contract.

In contrast, a Permissioned Authorization Object (PPO):

• is a pure EIP-712 signed payload describing bounded pull consent,

• does not require a central contract or registry,

• does not track cumulative balances or allowances,

• is domain-bound to the executor, not globally scoped.

PPOs are intentionally executor-agnostic. Any contract implementing ERC-8102 can verify and execute a PPO, using its own domain separator and revocation model.

Registries may exist (for revocation or observability), but they are optional and out of scope of the authorization primitive itself.

In short: Permit2 is a concrete approval mechanism; ERC-8103 is a minimal, reusable authorization primitive that executors, wallets, AA stacks, or registries can build on in different ways.

