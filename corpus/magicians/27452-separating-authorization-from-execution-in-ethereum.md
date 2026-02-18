---
source: magicians
topic_id: 27452
title: Separating Authorization from Execution in Ethereum
author: recurmj
date: "2026-01-17"
category: Magicians > Primordial Soup
tags: [authorization, erc-8103, erc-8102, permissioned-pull]
url: https://ethereum-magicians.org/t/separating-authorization-from-execution-in-ethereum/27452
views: 30
likes: 0
posts_count: 2
---

# Separating Authorization from Execution in Ethereum

### A Missing Layer Beneath Execution and Its Consequences for Custody

This post foregrounds two claims:

1. Authorization is a missing layer of machine state (RIP-100).
2. Permissioned pull is the only financial execution semantics that correctly respects that layer (RIP-001).

Everything else, including account models, vaults, wallets, and registries follows from these two facts.

---

## 1. The core observation

Modern execution systems (blockchains, smart contracts, automation frameworks) share a silent assumption:

> If an action can be executed, it is permitted.

This assumption held when execution was:

- local,
- infrequent,
- directly human-initiated.

It fails catastrophically once execution becomes:

- remote,
- automated,
- adversarial,
- irreversible.

The result is systemic failure across finance, automation, and digital custody.

---

## 2. RIP-100: Authorization Objects

RIP-100 names what these systems lack:

> Authorization as explicit, first-class machine state.

An **Authorization Object** is:

- typed,
- scoped,
- time-bounded,
- revocable,
- independent of execution.

Crucially:

- a valid signature no longer means “anything, forever”,
- it means “this bounded intent, under these conditions”.

Authorization becomes **state**, not a side effect.

---

## 3. RIP-001: Permissioned Pull

Once authorization is explicit state, execution semantics are no longer free.

RIP-001 formalizes the only financial profile and execution model that respects Authorization Objects:

> Execution is initiated by the grantee, not the grantor.

In permissioned pull:

- the holder of value does not push,
- the executor attempts execution,
- authorization state is checked at execution time,
- revocation can beat execution.

This is not a UX choice.

It is a semantic consequence.

---

## 4. The key invariant

Taken together, RIP-100 and RIP-001 imply a hard constraint:

> Any system that allows unilateral push execution cannot correctly enforce bounded authorization.

This is the invariant.

It explains:

- single-signature drains,
- phishing losses,
- infinite approvals,
- automation abuse,
- irreversibility under human error.

These are not wallet bugs. They are violations of the authorization–execution separation.

---

## 5. Custody is downstream

Once authorization is explicit state (RIP-100)

and execution obeys permissioned pull (RIP-001),

a further question becomes unavoidable:

> Where should value live under this model?

Traditional push-based accounts implicitly re-merge intent, authority and execution. That re-merging collapses the layer.

---

## 6. RIP-011 as a corollary (not a prerequisite)

RIP-011 (Pull-Secured Accounts) is **not required** to establish the authorization layer.

It is the **first natural custody structure implied by it**.

RIP-011 simply states:

- value containers must not be able to unilaterally push,
- value must only be released under bounded authorization,
- catastrophic failure modes must be structurally impossible.

You do not need to accept RIP-011 to accept RIP-100 + RIP-001.

But once you accept those two, **push-based custody is already semantically incomplete**.

---

## 7. Scope of this discussion

This post is **not** proposing:

- deprecation of EOAs,
- a wallet standard,
- a UX flow,
- protocol changes.

It is naming:

- a missing layer,
- its execution semantics,
- and the invariants that follow.

Everything else is engineering.

---

## 8. Why this is being posted now

This is not contingent on adoption, traction, or tooling.

It is a clarification of machine semantics.

Layers do not ask for permission to exist.

They are either named, rediscovered, or re-implemented.

This post exists to name it clearly.

— Mats

## Replies

**abcoathup** (2026-01-19):

Please add links to each RIP.  Recommend updating the title to provide more context.

