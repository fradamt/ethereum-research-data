---
source: magicians
topic_id: 27415
title: "Discussion topic for EIP (pre-draft): Connector Transparency — Making Wallet Connection Mediation Explicit"
author: Madeindreams
date: "2026-01-11"
category: EIPs
tags: [wallet, security, privacy, ux, eip-1193]
url: https://ethereum-magicians.org/t/discussion-topic-for-eip-pre-draft-connector-transparency-making-wallet-connection-mediation-explicit/27415
views: 19
likes: 0
posts_count: 1
---

# Discussion topic for EIP (pre-draft): Connector Transparency — Making Wallet Connection Mediation Explicit

*This is a pre-draft discussion intended to gather early feedback before opening a formal EIP PR.*

---

## Summary

This discussion explores **connector transparency** in wallet–dApp interactions.

While wallets are typically treated as the primary trust anchor, real-world connections are often mediated by **connectors / SDKs and auxiliary infrastructure** that are not explicitly disclosed at connection time. This proposal aims to make those trust boundaries **explicit and inspectable**, without mandating behavior or architecture.

---

## Motivation

While working on a privacy-first wallet connector, I encountered a structural blind spot that does not appear to be explicitly addressed by existing standards: **wallets and connectors are not the same thing, yet users are typically asked to trust them as if they were**.

In practice, a typical dApp connection often involves multiple layers:

- the wallet,
- the connector or SDK selected by the application,
- and potentially additional relay, discovery, or RPC infrastructure.

Wallets may be secure and transparent in isolation, but connectors frequently mediate the connection, perform discovery, route traffic, or introduce third-party infrastructure in ways that are **not visible to users at connection time**. This information may exist in documentation or source code, but it is rarely disclosed in a standardized or user-visible way.

As a result, applications and users routinely operate with **implicit trust assumptions** about how a connection is mediated, what infrastructure is involved, and which parties may observe or influence traffic.

---

## Core Idea

This proposal focuses on **disclosure, not enforcement**, and separates two distinct responsibilities:

### 1. Wallet-reported connection transparency

An optional, read-only provider method (e.g. `eth_getConnectorInfo`) allowing wallets to disclose **factual information** about how the connection is mediated, such as:

- whether the connection is direct or relayed,
- RPC visibility characteristics,
- involvement of third-party infrastructure known to the wallet.

This information is wallet-reported and reflects what the wallet can assert about the connection path. Absence of disclosure is expected and handled gracefully.

---

### 2. Connector-authored disclosure

A **self-declared disclosure authored by the connector itself**, describing its own behavior, such as:

- network requests or relays,
- telemetry or analytics,
- local storage or caching,
- discovery or fallback behavior.

This disclosure is intentionally **separate from wallet claims** and clearly labeled as connector-authored. It represents a statement of intent or behavior by the connector, not a guarantee.

---

### Application expectations

Applications are expected to:

- handle missing disclosures gracefully,
- clearly distinguish between:

 wallet-reported information,
- connector-authored disclosure,
- and locally inferred observations.

No behavior is mandated. No architecture is prescribed.

The goal is simply to make **trust boundaries explicit** rather than implicit.

---

## What This Proposal Does Not Do

- It does not enforce privacy guarantees.
- It does not restrict existing connector ecosystems.
- It does not assume wallets or connectors are inherently trustworthy.
- It does not require protocol-level changes.
- It does not attempt to classify “good” or “bad” connectors.

---

## Relation to Existing Work

This proposal is intended to be **complementary**, not disruptive, to existing standards and practices, including:

- EIP-1193 provider interfaces,
- wallet discovery mechanisms (e.g. EIP-6963),
- EOAs, account abstraction, session keys, and delegated signing models.

It does not replace or modify these systems, but instead adds an **explicit disclosure surface** so applications and users can reason about how connections are mediated.

---

## Draft & Reference Implementation

- Draft EIP: (to be published once scope stabilizes)
- A reference implementation exists and includes:

 best-effort inference when wallets do not disclose,
- explicit labeling of inferred vs reported information,
- a simple UI surface exposing connection transparency to users.

The implementation is provided as **evidence that the disclosure model is practical**, not as a prescribed architecture.

---

## Feedback Requested

I’d appreciate feedback on:

- whether the separation of wallet-reported vs connector-authored disclosure makes sense,
- whether this fits best as a Standards Track / Interface EIP, or another classification,
- overlap (or lack thereof) with existing wallet or connector standards,
- anything that feels out of scope, underspecified, or incorrectly framed.

Happy to clarify or iterate based on feedback.

---

## Update Log

- 2026-01-10: Initial discussion draft posted on Ethereum Magicians.

---

## External Reviews

None as of 2026-01-10.

---

## Outstanding Issues

- 2026-01-10: Should wallet-reported disclosure be standardized as a provider method or another mechanism?
- 2026-01-10: Should connector-authored disclosure be machine-readable, human-readable, or both?
- 2026-01-10: Does this fit best as a Core EIP, an Interface EIP, or a paired Core + ERC approach?
