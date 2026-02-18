---
source: magicians
topic_id: 27042
title: "[Recur] [RIP-000] The One-Shot Authorization Flaw in Digital Value Systems"
author: recurmj
date: "2025-12-09"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/recur-rip-000-the-one-shot-authorization-flaw-in-digital-value-systems/27042
views: 40
likes: 0
posts_count: 1
---

# [Recur] [RIP-000] The One-Shot Authorization Flaw in Digital Value Systems

### Why Momentary Consent Limits Coordination, Automation, and Cross-Domain Workflows

**Authors:** Recur Labs Research

**Category:** Informational / Architectural Analysis

**Status:** Draft for community discussion

**Date:** 2025

---

## Summary

This post introduces **RIP-000**, an architectural analysis of the limitations inherent in *one-shot authorization* — the dominant model used across today’s blockchain systems, where a signature is consumed immediately upon execution.

While suitable for discrete transfers and final settlement, one-shot authorization becomes a structural limitation when applied to programmable finance and cross-domain coordination.

RIP-000 does **not** propose a protocol change.

It defines the problem space and provides the architectural motivation for RIP-001, which introduces a durable, revocable authorization primitive compatible with existing EVM systems.

RIP-000 should be evaluated on its diagnosis; RIP-001 addresses the corresponding solution.

---

## Motivation

Modern financial workflows require:

- durable, revisable authorization
- revocation paths
- pacing and throttling
- bounded delegation
- multi-step coordination
- cross-chain portability of intent

However, the dominant authorization model in blockchain systems:

- treats consent as a single-use instruction
- loses all authorization context after execution
- offers no native mechanism for revocation
- cannot express rate limits or time bounds
- requires each chain or domain to reconstruct intent independently

As a result, ecosystems rely on **external scaffolding** — keepers, bots, relayers, intents solvers, automation frameworks — to approximate behaviors that cannot be expressed natively.

RIP-000 formalizes this structural gap as the **One-Shot Authorization Flaw**.

---

## Problem Statement

The flaw can be summarized as follows:

### 1. Consent does not persist

After execution, no object representing ongoing authorization remains.

### 2. Revocation is impossible

A submitted instruction cannot be withdrawn once in flight.

### 3. No pacing or throttling

Systems cannot express “stream,” “rebalance gradually,” or “execute within bounds.”

### 4. Authorization is domain-bound

Intent cannot move across chains with consistent semantics.

### 5. Delegation cannot be safely scoped

Native primitives offer no time windows, budgets, roles, or multi-step permissions.

Because these requirements cannot be expressed at the authorization layer, applications must rebuild them at higher layers, leading to:

- brittle automation
- inconsistent cross-chain behavior
- timing vulnerabilities in automation flows
- fragmented authorization state

RIP-000 argues that this is not an implementation issue but an **architectural discontinuity**.

---

### Concrete Example: Subscription Services

Consider a streaming service accepting crypto payments:

**Desired:** User authorizes $15/month for 12 months, revocable anytime

**With one-shot authorization:**

- Service must prompt user every month
- Or user grants infinite approval (dangerous)
- No way to express “monthly for N months”
- Revocation requires manual transaction

**What’s needed:**

- User signs once: “Allow $15/month for 12 months”
- Service pulls monthly automatically
- User can revoke anytime
- Expires automatically after 12 months

This requires durable, bounded, revocable authorization.

---

## Diagram (One-Shot Consent vs Coordination Requirements)

```plaintext
+--------------------------------+

|   AUTHORIZATION PRIMITIVE      |

|      (ONE-SHOT CONSENT)        |

|--------------------------------|

| • momentary authorization      |

| • consumed upon execution      |

| • no pacing or throttling      |

| • no persistent consent        |

+---------------+----------------+

                |

                | structural gap

                v

+--------------------------------+

|    COORDINATION REQUIREMENTS   |

|--------------------------------|

| • revocation                   |

| • durable multi-step intent    |

| • pacing & throttling          |

| • bounded delegation           |

| • cross-domain continuity      |

+---------------+----------------+

                |

                | produces

                v

+--------------------------------+

|     EMERGENT WEAKNESSES        |

|--------------------------------|

| • automation brittleness       |

| • fragmented authorization     |

| • MEV in automation systems    |

| • cross-domain inconsistency   |

| • inability to pace flows      |

+--------------------------------+

```

---

## Related Work

Several existing mechanisms address parts of the problem space:

- ERC-20 approvals — persistent but overbroad and non-portable
- ERC-2612 Permit — stateless, but one-shot and non-revocable
- Permit2 — bounded approvals, but domain-specific
- Account Abstraction — flexible validation, but no durable consent primitive
- Automation networks — simulate persistence through repeated submissions
- Intents frameworks — express desired outcomes but rely on solvers and lack persistent delegated consent

All operate **on top of** one-shot authorization; none replace it.

---

## Scope Clarification

RIP-000:

- does not claim one-shot authorization is the root cause of MEV, liquidations, or bridge risk
- does not prescribe changes to consensus or base-layer execution
- does not define a new token standard

Instead, it identifies a **missing authorization primitive** needed for reliable coordination layers.

RIP-001 introduces the durable authorization primitive that addresses this gap. This post focuses only on the underlying problem (RIP-000).

**Key properties:** Signature-based (no token changes), cross-chain portable semantics, time and amount bounds, explicit grantee, nonce-based replay protection.

---

## Non-Goals

To keep discussion focused, RIP-000 explicitly does **not**:

- Replace ERC-20 or propose token standard changes
- Solve MEV, front-running, or privacy
- Define consensus-layer modifications
- Compete with Account Abstraction (complementary)
- Replace Permit2 for single-chain use cases

---

## Discussion Goals

Community feedback is sought on:

1. Problem validity

 Is one-shot authorization a meaningful architectural limitation?
2. Do developers encounter its constraints in real systems?
3. Problem scope

 Are there important coordination behaviors not covered here?
4. Are any of the identified weaknesses misattributed?
5. Terminology and framing

 Is “durable consent” a useful conceptual construct?
6. Is “one-shot authorization” the correct neutral term?
7. Placement within the standards stack

 Should durable authorization be considered:

 An application-layer pattern?
8. A middleware layer?
9. A candidate for standardization?

Feedback on strengths, omissions, technical framing, and alternate models is welcome.

---

## Links

- RIP-000 Full Specification: recur-standard/docs/RIP-000.md at main · recurmj/recur-standard · GitHub
- RIP-001 ERC Draft:
ERC-8102: Permissioned Pull

---

## Copyright

CC0 — This work is released into the public domain.
