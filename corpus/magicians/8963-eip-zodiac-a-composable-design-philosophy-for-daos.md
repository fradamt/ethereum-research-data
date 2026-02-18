---
source: magicians
topic_id: 8963
title: "EIP-?: Zodiac - A composable design philosophy for DAOs"
author: auryn
date: "2022-04-19"
category: EIPs
tags: [dao]
url: https://ethereum-magicians.org/t/eip-zodiac-a-composable-design-philosophy-for-daos/8963
views: 2482
likes: 6
posts_count: 5
---

# EIP-?: Zodiac - A composable design philosophy for DAOs

This is a long overdue post to discuss the Zodiac standard as an EIP.

You can keep track of this EIP’s progress at PR [#5005 in the EIP repo](https://github.com/ethereum/EIPs/pull/5005).

---

```auto
eip: 5005
title: Zodiac Avatar Accounts
description: A composable design philosophy for programmable accounts.
author: Auryn Macmillan (@auryn-macmillan), Kei Kreutler (@keikreutler)
discussions-to: https://ethereum-magicians.org/t/eip-zodiac-a-composable-design-philosophy-for-daos/8963
status: Draft
type: Standards Track
category: ERC
created: 2022-04-14
requires: 165
```

## Abstract

ERC-5005 (Zodiac Avatar Accounts) is a philosophy and open standard for composable and interoperable tooling for programmable Ethereum accounts. Zodiac-compatible tooling separates the account taking actions/holding tokens (known as the “avatar”) and the authorization logic into two (or more) separate contracts. This standard defines the `IAvatar` interface, to be implemented by avatar contracts, while the authorization logic can be implemented with any combination of other tools (for example, DAO tools and frameworks).

## Motivation

Currently, most programable accounts (like DAO tools and frameworks) are built as somewhat monolithic systems, wherein account and control logic are coupled, either in the same contract or in a tightly bound system of contracts. This needlessly inhibits the future flexibility of individuals and organizations using these tools and encourages platform lock-in via extraordinarily high switching costs.

By using the Zodiac standard to decouple account and control logic, individuals and organizations are able to:

1. Enable flexible, module-based control of programmable accounts
2. Easily switch between tools and frameworks without unnecessary overhead.
3. Enable multiple control mechanism in parallel.
4. Enable cross-chain / cross-layer governance.
5. Progressively decentralize their governance as their project and community matures.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

The Zodiac standard consists of four key concepts—Avatars, Modules, Modifiers, and Guards:

1. Avatars are programmable Ethereum accounts. Avatars are the address that holds balances, owns systems, executes transaction, is referenced externally, and ultimately represents your DAO. Avatars MUST expose the IAvatar interface.
2. Modules are contracts enabled by an avatar that implement some control logic.
3. Modifiers are contracts that sit between modules and avatars to modify the module’s behavior. For example, they might enforce a delay on all functions a module attempts to execute or limit the scope of transactions that can be initiated by the module. Modifiers MUST expose the IAvatar interface.
4. Guards are contracts that MAY be enabled on modules or modifiers and implement pre- or post-checks on each transaction executed by those modules or modifiers. This allows avatars to do things like limit the scope of addresses and functions that a module or modifier can call or ensure a certain state is never changed by a module or modifier. Guards MUST expose the IGuard interface. Modules, modifiers, and avatars that wish to be guardable MUST inherit Guardable, MUST call checkTransaction() before triggering execution on their target, and MUST call checkAfterExecution() after execution is complete.

```solidity
/// @title Zodiac Avatar - A contract that manages modules that can execute transactions via this contract.

pragma solidity >=0.7.0 =0.7.0 =0.7.0 =0.7.0 =0.7.0 CC0.

## Replies

**TimDaub** (2022-06-26):

What makes me uneasy about reading this EIP is that much for the terminology isn’t borrowed from past EIPs but that it is rather copied from Gnosis software and other places of the web.

I’d have no problem with this EIP if its language was either self-referentially defined or pointing back to prior EIPs.

I guess here’s a norm: Consider boardind a flight and only downloading ethereum/EIPs. There’s no WIFI, can you understand the document inflight (e.g. reading other EIPs is fine)?

IMO this document wouldn’t pass the test. E.g. what is a “Gnosis Safe,” a “Zodiac?” What is this philosophy?

---

**auryn** (2022-07-04):

I think that’s a really great observation! I’ll have a crack at removing the language that makes references to, or assumes knowledge of, things outside of the EIP repo.

---

**auryn** (2022-07-05):

Ok, I made a PR which both generalizes the language and removes external references. Also edited OP with the corresponding changes.

https://github.com/ethereum/EIPs/pull/5200

---

**colinnielsen** (2023-03-25):

I think it would be extremely valuable to index both `address` fields on the `ModuleEnabled` and `ModuleDisabled` events. This would allow for module permissions to be discovered and indexed off chain for a given address - thus increasing permissions transparency.

