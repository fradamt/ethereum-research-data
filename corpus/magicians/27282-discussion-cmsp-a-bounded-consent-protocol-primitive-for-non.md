---
source: magicians
topic_id: 27282
title: "[Discussion] CMSP: A Bounded-Consent Protocol Primitive for Non-Custodial Recurring Payments"
author: dperezcabrera
date: "2025-12-22"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/discussion-cmsp-a-bounded-consent-protocol-primitive-for-non-custodial-recurring-payments/27282
views: 22
likes: 0
posts_count: 1
---

# [Discussion] CMSP: A Bounded-Consent Protocol Primitive for Non-Custodial Recurring Payments

This post introduces **CMSP (Capped Mandate Subscription Protocol)**, a design-complete protocol primitive for non-custodial recurring payments, published for **adversarial technical review**.

This is **not a product launch** and **not production-blessed**.

The goal is to validate (or break) a set of **explicit security invariants** around recurring payments on EVM chains.

The design emerged from repeated failure modes observed in existing approval-based and custodial subscription patterns.

---

## Motivation

Most on-chain subscription approaches today fall into one of three categories:

1. Custody / escrow (honeypots)
2. Infinite ERC-20 approvals (unbounded loss)
3. Manual per-period signing (UX failure)

CMSP reframes subscriptions as a **bounded-consent problem**, not an automation or scheduling problem.

Automation without limits effectively collapses into custody.

---

## Core Idea

A subscription is modeled as a **mandate**:

- cryptographically signed by the payer
- explicitly time-bounded
- strictly capped per period (maxPerPeriod)
- enforced on-chain
- executed opportunistically off-chain

The **worst-case loss is deterministically bounded**, even under:

- malicious workers
- malicious merchants
- MEV activity
- infrastructure failure

Liveness is best-effort. Safety is mandatory.

---

## EVM-Specific Design Choices

The EVM reference design relies on:

- EIP-712 structured data signing (chainId enforced)
- EIP-2612 / Permit-style flows for one-signature setup
- Two mandate types:

Fixed mandates: permissionless execution with deterministic amount
- Variable mandates: merchant-signed invoices, executor-bound to prevent MEV fee theft

A core invariant is that the **CMSP contract never holds funds**.

---

## What CMSP Explicitly Does Not Do

- No custody
- No debt or catch-up billing
- No guaranteed execution
- No pricing logic
- No oracle integration
- No privacy guarantees
- No cross-chain abstraction

These non-goals are intentional and documented.

---

## Specification & Reference Code

- Repository: GitHub - CleanSky-labs/cmsp-protocol: CMSP: Capped Mandate Subscription Protocol. An open, non-custodial standard for recurring payments. Bounded risk through time-limited and amount-capped mandates across EVM, Solana, and Cosmos.
- Whitepaper: high-level philosophy and design rationale
- RFC-0001: core specification
- RFC-0002: threat model
- RFC-0005: worker constraints
- RFC-0007: non-goals and limits

The EVM reference implementation is written in Solidity 0.8.20 and is illustrative, not production-ready.

---

## Feedback Requested

I’m particularly interested in feedback on:

- Whether the security invariants are complete
- EVM-specific edge cases or failure modes
- Interactions with ERC-20 quirks, Permit2, or AA wallets
- Worker incentive modeling and MEV considerations

Are there EVM-specific scenarios where this bounded-consent model breaks down in practice?
