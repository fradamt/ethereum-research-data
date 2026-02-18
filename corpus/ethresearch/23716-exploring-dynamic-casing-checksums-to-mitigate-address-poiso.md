---
source: ethresearch
topic_id: 23716
title: Exploring Dynamic Casing Checksums to Mitigate Address Poisoning
author: Mitsuhamizu
date: "2025-12-21"
category: UI/UX
tags: []
url: https://ethresear.ch/t/exploring-dynamic-casing-checksums-to-mitigate-address-poisoning/23716
views: 66
likes: 0
posts_count: 1
---

# Exploring Dynamic Casing Checksums to Mitigate Address Poisoning

## TL;DR

Address poisoning works because humans verify only the **prefix/suffix** of an address. This post proposes a wallet/UI-only mechanism: the receiver shares a short-lived receiver code, and the sender’s wallet uses `Keccak256(address || code)` to derive a **dynamic checksum casing fingerprint**. If the sender accidentally pastes a poisoned lookalike address, verification fails because the attacker doesn’t know the code.

---

## Motivation: the common habit poisoning exploits

In practice, few users verify 40 hex characters end-to-end. The dominant workflow—especially when copying from recent activity—is:

- check the first 4–6 chars
- check the last 4–6 chars
- assume the middle is fine

Poisoning attacks target this directly:

1. attacker generates an address with the same visible prefix/suffix as a commonly used recipient
2. attacker sends a 0-value/dust transfer so the lookalike appears in “recent” history
3. user copies the wrong entry, prefix/suffix matches, funds are sent to the attacker

This is primarily a UI/human-verification failure, not a protocol bug.

---

## Intuition: Ethereum transfers lack a “second confirmation”

In many traditional payment flows you effectively confirm two things:

- the destination identifier (account number)
- an independent confirmation signal (payee name / confirmation prompt)

Ethereum has a strong destination identifier (the address), but the second confirmation is usually missing when users are transferring to raw `0x…` recipients. The goal here is to add a lightweight second factor that is:

- off-chain (wallet-only)
- cheap (no extra on-chain steps)
- hard for a poisoner to anticipate for a specific payment

---

## Background: what checksum casing is, and why it’s insufficient

Wallets often show mixed-case “checksummed” addresses. The general idea is:

- compute a hash from the address
- use bits of that hash to decide which a–f hex letters are upper/lower case
- if the address changes, the casing pattern is unlikely to remain valid, helping catch typos

The widely used Ethereum convention here is [EIP-55](https://eips.ethereum.org/EIPS/eip-55) checksum casing.

Limitation for poisoning: this casing is static per address and publicly computable, so a poisoned lookalike can also be displayed in a “valid checksummed” form.

---

## Proposal: make checksum casing depend on a receiver-provided code (dynamic fingerprint)

### Inputs

- addr: recipient address (20 bytes)
- code: short receiver code (string; recommended one-time or short-lived)

### Hash

We compute:

H = Keccak256(addr\_bytes || code\_utf8)

where `addr_bytes` is the 20-byte address and `code_utf8` is the UTF-8 encoding of the receiver code. Using the 20-byte address keeps concatenation boundaries unambiguous.

### Casing rule

Render the address as hex (as usual). For each character:

- digits 0–9 unchanged
- letters a–f are uppercased/lowercased according to successive bits of H
(same spirit as EIP-55, but using H above)

Result: the same underlying address now has a **code-specific casing fingerprint**.

---

## Flow

### Receiver (Alice)

1. Alice generates a receiver code (wallet-generated recommended), e.g. lamp-snow-47.
2. Wallet displays the address with casing derived from H.
3. Alice shares (address, code) with the sender.

### Sender (Bob)

1. Bob pastes the address.
2. Bob enters the receiver code.
3. Wallet recomputes and verifies the casing fingerprint:

match → verified
4. mismatch → warn/block (wrong code, wrong address, or possible poisoning)

The intent is that users rely on a clear verified/not-verified state rather than visually inspecting casing.

---

## Why this mitigates poisoning (for the target scenario)

Poisoning succeeds when a user accidentally selects a prefix/suffix lookalike from history. With a receiver code:

- an attacker can still manufacture lookalike addresses and get them into the user’s history
- but the attacker cannot make that poisoned address validate under the receiver’s code
- so “copy wrong address from history” becomes a deterministic verification failure instead of a silent success

---

Looking forward to your thoughts—especially on the UX trade-offs and any potential pitfalls in the threat model or implementation that I might have overlooked. Thanks in advance for the feedback!
