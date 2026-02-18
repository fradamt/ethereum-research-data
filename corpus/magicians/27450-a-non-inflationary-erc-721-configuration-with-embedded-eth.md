---
source: magicians
topic_id: 27450
title: A Non-Inflationary ERC-721 Configuration with Embedded ETH
author: ten-io-meta
date: "2026-01-16"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/a-non-inflationary-erc-721-configuration-with-embedded-eth/27450
views: 10
likes: 0
posts_count: 1
---

# A Non-Inflationary ERC-721 Configuration with Embedded ETH

This post does not propose a new ERC or standard.

It documents a concrete configuration of existing Ethereum primitives that satisfies irreversible-supply invariants similar to those described in ERC-8098, but applied to non-fungible assets instead of ERC-20 balances.

---

### Overview

The system is implemented as an ERC-721 contract where each token embeds a fixed amount of native ETH at mint time.

- No ERC-20 token is issued.
- All value is held in native ETH (not wrapped).
- Total supply is fixed at creation and can only decrease.
- Burning the NFT irreversibly releases the embedded ETH to the holder.

The holder is the sole authority over execution. No intermediaries, liquidity pools, or secondary markets are required for value realization.

---

### Properties

- Irreversible supply: burned assets cannot be recreated.
- Non-inflationary by design: no minting beyond the initial supply.
- Unilateral execution: the holder may burn at any time to retrieve the embedded ETH.
- Autocustodial value: ETH is not represented or claimed, but contained.
- Market independence: value does not depend on price discovery or liquidity.

---

### Relation to ERC-8098

ERC-8098 formalizes irreversible-supply invariants for fungible tokens.

This configuration demonstrates that the same invariants can be satisfied in an object-based (ERC-721) context, where irreversibility applies to individual assets rather than aggregate balances.

No changes to ERC-8098 are proposed or required.

---

### Reference Implementation

A live reference implementation is available at:

https://tenio.eth.limo

This deployment serves as a running proof that irreversible-supply semantics and native ETH containment are enforceable today using existing Ethereum standards.
