---
source: magicians
topic_id: 21435
title: "EIP 7790: Parameters to increase the gas limit"
author: Giulio2002
date: "2024-10-22"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7790-parameters-to-increase-the-gas-limit/21435
views: 156
likes: 4
posts_count: 4
---

# EIP 7790: Parameters to increase the gas limit

This EIP proposes increasing the gas limit through EIP7783 in the span of 2 years from 30 to 60 million. starting in february 2025.

- After 6 months: Gas Limit = 37.5 Mn
- After 12 months: Gas Limit = 45 Mn
- After 18 months: Gas Limit = 52.5 Mn
- After 24 months: Gas Limit = 60 Mn

## Replies

**wjmelements** (2024-10-24):

We don’t need an EIP to raise the gas limit. The gas limit is dynamic. Each block votes the limit up or down. It’s at 30m right now because of consensus.

---

**Giulio2002** (2024-10-24):

It’s an informational proposal so - it is still valid

---

**SamWilsn** (2024-12-18):

I’d suggest merging this with [EIP-7783: Add Controlled Gas Limit Increase Strategy](https://eips.ethereum.org/EIPS/eip-7783) and withdrawing it.

The newly combined proposal could be considered Standards Track / Core (from EIP-1):

> changes that are not necessarily consensus critical but may be relevant to “core dev” discussions

I’d also be fine with Informational, especially if another Editor suggested that category.

