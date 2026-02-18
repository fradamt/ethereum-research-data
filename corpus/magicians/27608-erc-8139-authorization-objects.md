---
source: magicians
topic_id: 27608
title: "ERC-8139: Authorization Objects"
author: recurmj
date: "2026-01-27"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8139-authorization-objects/27608
views: 18
likes: 0
posts_count: 1
---

# ERC-8139: Authorization Objects

Hi everyone,

Over the past year I’ve been working on a set of standards around permissioned execution (ERC-8102/8103), and one thing that keeps reappearing across multiple proposals (including recent “agent authorization” discussions) is the same missing layer:

> We lack a general, first-class authorization primitive that exists independently of execution.

Most systems today conflate authorization with:

- execution,
- scheduling,
- automation,
- or implicit contract state (approvals, allowances, sessions).

This makes permission difficult to reason about as a persistent object.

I’m proposing **Authorization Objects (AO)** as a minimal root primitive:

- an EIP-712 typed object,
- signed by a grantor,
- granting a grantee permission within an opaque scope,
- with explicit time bounds and revocation,
- and no execution semantics.

This ERC intentionally does *not* define:

- how or when anything executes,
- what assets are involved,
- or whether any action happens at all.

It only defines:

> how consent exists as machine-verifiable state.

Downstream standards (e.g. token pulls, agent delegation, API access, governance) can define **profiles** that interpret `scope`, without redefining the primitive.

PR here:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1491)














####


      `master` ← `recurmj:master`




          opened 09:12PM - 27 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/238723421?v=4)
            recurmj](https://github.com/recurmj)



          [+278
            -0](https://github.com/ethereum/ERCs/pull/1491/files)







This PR introduces **ERC-XXXX: Authorization Objects (AO)**, a general-purpose a[…](https://github.com/ethereum/ERCs/pull/1491)uthorization primitive for Ethereum.

The proposal defines a portable, revocable EIP-712 typed object representing explicit consent from a grantor to a grantee within an application-defined scope and time window.

Key properties:

- Authorization exists as a first-class object, independent of execution.
- The ERC defines no execution semantics, asset logic, or automation behavior.
- Consent is inspectable, revocable, and machine-verifiable as persistent state.
- Domain-specific standards can define *profiles* that interpret `scope` without redefining the primitive.

This ERC formalizes a root layer that downstream standards (e.g. token pulls, agent delegation, API access, governance) can consume without coupling authorization to any particular execution model.












Discussion welcome, especially around:

- scope representation,
- registry vs pure off-chain objects,
- and how people see this composing with existing standards.

– Mats
