---
source: magicians
topic_id: 25931
title: "ERC-8102: Permissioned Pull"
author: recurmj
date: "2025-10-23"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8102-permissioned-pull/25931
views: 178
likes: 0
posts_count: 5
---

# ERC-8102: Permissioned Pull

**Author:** Mats Heming Julner (Recur Labs)

**Status:** Draft

**Type:** Standards Track (Verification)

*(Note: “RIP-001” here refers to the Recur Improvement Proposal draft; not yet part of the official Rollup RIP process.)*

Sharing this draft based on recent discussion with Ethereum Foundation contributors around formalizing the permissioned-pull primitive as an ERC-level standard.

Feedback on structure, naming, and security model is warmly welcome before moving toward ERC-A / ERC-B drafts.

## Abstract

The current financial architecture of Ethereum remains push-based; transfers occur only after imbalance or failure, resulting in reactive liquidity and fragmented settlement.

The **Permissioned-Pull Standard (RIP-001)** introduces a consent-driven flow layer that allows value to move *before* failure through revocable pull permissions.

This standard aims to make digital value continuous instead of event-based, unlocking on-chain subscriptions, streaming payments, and dynamic credit flows built natively into Ethereum’s account abstraction model.

## Motivation

While ERC-20 standardized fungibility and ERC-2612 enabled delegated approvals, neither define a generalized, safe mechanism for *permissioned value retrieval.*

A universal pull primitive would allow protocols, wallets, and dApps to coordinate recurring, metered, or conditional transfers without requiring custodial trust.

The intent is to evolve “payments” into “flows”; a foundation for continuous commerce, automated obligations, and on-chain financial continuity.

## Specification Outline

This will mature through discussion, but the split that James proposed gives perfect clarity:

### ERC-A: Permission State (Grant / Revoke)

- Defines a minimal interface for granting, viewing, and revoking pull permissions.
- Can be implemented by any token or account.

### ERC-B: Pull Execution (Request / Fulfil)

- Defines how an authorized pull request executes against a permissioned account.
- Includes safety, expiry, and nonce patterns to prevent abuse.

Together, these two ERCs form the basis for *consented flow of value* across Ethereum networks.

## Reference Implementation

A working prototype and SDK structure are live at:

[github.com/recurmj/recur-standard](https://github.com/recurmj/recur-standard)

Maintained by **Recur Labs,** the repository demonstrates the canonical Solidity implementation, developer tooling, and security guidelines.

## Next Steps

1. Community feedback and naming refinement via Ethereum Magicians.
2. Alignment with Account Abstraction and Safe Modules for native integration.
3. Drafting ERC-A / ERC-B proposals for formal review and EIP number assignment.

## Authors

**Recur Labs:** Mats Heming Julner (GitHub: [@recurmj](/u/recurmj))

**Advisory contributor (discussion):** James (Ethereum Foundation)

*(additional contributors to be added as discussion evolves)*

## Replies

**recurmj** (2025-11-10):

Following up on the initial draft above (RIP-001), sharing a quick progress report and next steps before preparing the ERC-A / ERC-B formal drafts.

Since the original post 18 days ago, we successfully executed the **first cross-network permissioned pull** — proving that a signed consent (EIP-712 Authorization) can be **observed and verified across chains** without transferring custody.

This validates the core idea of *Recur’s permissioned-pull primitive* as a portable consent layer rather than a chain-bound payment mechanism.

—-

### What’s been proven

- A single EIP-712 Authorization struct signed by the grantor was executed on Ethereum Sepolia and then mirrored on Base Sepolia via observeAndVerify().
- The same structHash + domainSeparator verified correctly on both networks.
- This demonstrates that consent continuity (not custody) is sufficient to authorize value flow across chains; establishing a “flow layer” on top of existing liquidity rails.

—-

### What’s next

Following guidance from EF contributors (James & Jason), I’m now preparing the split into two ERCs:

| Draft | Scope | Analogy |
| --- | --- | --- |
| ERC-A: Permissioned Authorization (PPO) | Defines the EIP-712 struct, fields (grantor, grantee, token, maxPerPull, validAfter, validBefore, nonce), and replay protection rules. | ERC-2612 (Permit) |
| ERC-B: Pull Execution Interface | Defines how compliant contracts (PullSafe, SettlementMesh, etc.) interpret and execute PPOs. | ERC-20 transferFrom() |

—-

The goal is to make permissioned-pull a **native capability inside the account abstraction stack,** not an external payment app; aligning with ERC-4337, ERC-6900, and ERC-7579 so wallets can treat “consented flow” as a first-class operation.

### Implementation references

- Contract: RecurPullSafeV2.sol
- Registry: RecurConsentRegistry.sol
- Cross-Network Mirror: PullMirrorV3.observeAndVerify()
- Demo: Successful on Sepolia + Base Sepolia, Oct 31 – Nov 1 2025
•	Core insight: “Consent, not custody, is the root primitive for cross-network value. Liquidity becomes statelessly attachable.”

—-

### Feedback welcome

Before formalizing ERC-A and ERC-B, I’d love peer review on:

1. Struct field layout and naming consistency with existing ERCs (esp. 2612, 4337).
2. Recommended security model for cross-network attestation (Merkle proof vs. signature-only).
3. Any prior art or overlaps worth referencing in the ERC drafts.

---

**recurmj** (2025-11-11):

**Follow-up verification note**

The cross-network demo used an internal prototype of PullMirrorV3.observeAndVerify() that verifies the same EIP-712 digest on the destination chain.

The contract hasn’t been published yet; I’ll release a minimized version once the ERC-A / ERC-B drafts are finalized so reviewers can reproduce the flow.

For anyone wanting to verify the hashes from the demo:

```auto
chainId (Sepolia): 11155111
chainId (Base Sepolia): 84532
AUTH_TYPEHASH  = 0x93c66a08da40a7ae602ecf25c64e31553efb281773a258d11616988f8619b956
structHash     = 0x0197dfa646216beddb9b3d2c6a2f6151bc7424a8ece75c853b48ea9f0095b396
authHash       = 0x3ed08d1d3735db3e432c83497f29537bdd04dc83373675d0f826036fa4817ccf
domainSeparator= 0x43a35c311d91ebc05929a3d8d3d64ce5ab5100f03890766dd93e4726a39dee761
```

Demo window: **Oct 31 – Nov 1 2025** (Sepolia ↔ Base Sepolia).

---

**recurmj** (2025-11-12):

**Update:**

ERC-A and ERC-B reference implementations are now live on GitHub.

The repository includes specs, contracts, and Foundry tests verifying dual-path revocation (local cancel + registry).

Frozen draft release: https://github.com/recurmj/permissioned-pull-standard/releases/tag/v1-draft

Feedback welcome before formal ERC submission.

---

**recurmj** (2025-12-10):

**Update: RIP-001 Canonical Revision (Alignment with RIP-000)**

Following community feedback and the publication of **RIP-000: The One-Shot Authorization Flaw**, I have published a fully updated version of **RIP-001: The Permissioned-Pull Primitive**.

### What changed:

### 1. Framing cleanup

All philosophical or narrative framing has been removed.

RIP-001 is now strictly:

- architectural,
- normative,
- minimal,
- and aligned 1:1 with the problem defined in RIP-000

(“durable, revocable, portable authorization” as the missing primitive).

This brings RIP-001 fully in line with Ethereum EIP expectations.

---

### 2. ERC-A / ERC-B split merged into RIP-001

Earlier drafts (ERC-A for the Authorization object, ERC-B for the Pull Executor) were originally suggested by EF reviewers to modularize the standard.

Those drafts remain available for comparison, but **RIP-001 now supersedes them as the canonical specification**:

- It incorporates:

 the Authorization struct
- the executor interface
- revocation semantics
- EIP-712 domain rules
- nonce usage guarantees
- error conditions and event expectations

This keeps the standard cohesive and removes fragmentation for reviewers.

A later ERC submission may still choose the A/B split, but **RIP-001 is now the authoritative spec the ERC will be derived from**.

---

### 3. Alignment with RIP-000

RIP-001 now explicitly positions itself as the concrete solution to the architectural gap identified in RIP-000:

> one-shot authorization cannot express durable, revocable, portable consent.

> RIP-001 defines the minimal primitive required to fill that gap.

No over-claiming, no references to unrelated system failures, strictly scoped to the absence of persistent authorization.

RIP-000 post:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recurmj/48/16307_2.png)

      [[Recur] [RIP-000] The One-Shot Authorization Flaw in Digital Value Systems](https://ethereum-magicians.org/t/recur-rip-000-the-one-shot-authorization-flaw-in-digital-value-systems/27042) [Primordial Soup](/c/magicians/primordial-soup/9)




> Why Momentary Consent Limits Coordination, Automation, and Cross-Domain Workflows
> Authors: Recur Labs Research
> Category: Informational / Architectural Analysis
> Status: Draft for community discussion
> Date: 2025
>
> Summary
> This post introduces RIP-000, an architectural analysis of the limitations inherent in one-shot authorization — the dominant model used across today’s blockchain systems, where a signature is consumed immediately upon execution.
> While suitable for discrete transfers and final…

---

### 4. Canonical Standard Draft

The new RIP-001 draft is now:

- fully self-contained
- normative
- ready for ERC conversion
- cleanly implementable
- consistent with the Recur Consent Layer terminology introduced in RIP-000

This is now the version I will maintain going forward. All prior drafts (ERC-A/B, early versions, prototype specs) are preserved but are no longer authoritative.

---

### Link to updated RIP-001:



      [github.com/recurmj/recur-standard](https://github.com/recurmj/recur-standard/blob/main/docs/RIP-001.md)





####

  [main](https://github.com/recurmj/recur-standard/blob/main/docs/RIP-001.md)



```md
# RIP-001: The Permissioned-Pull Standard
**Category:** Standards Track (Core Primitive)
**Author:** Recur Labs
**Status:** Draft (canonical post-RIP-000 alignment)
**Created:** 2025
**Replaces:** ERC-A / ERC-B split drafts (superseded by unified RIP-001)
**Depends on:** EIP-712

---

## Abstract

RIP-001 defines the **Permissioned-Pull Standard**, a durable authorization primitive that enables safe, scoped, revocable, grantee-initiated transfers of ERC-20 tokens.

A **grantor** signs an off-chain *Authorization object* describing:
- who may pull,
- which token,
- how much per pull,
- when the authorization is valid,
- and a unique nonce for replay protection.
```

  This file has been truncated. [show original](https://github.com/recurmj/recur-standard/blob/main/docs/RIP-001.md)










Feedback especially from wallet authors, AA implementers, security researchers, and protocol developers is very welcome before locking the ERC version.

