---
source: magicians
topic_id: 15297
title: "EIP-7425: Tokenized Reserve"
author: jimstir
date: "2023-07-31"
category: EIPs
tags: [vaults, reserve]
url: https://ethereum-magicians.org/t/eip-7425-tokenized-reserve/15297
views: 1626
likes: 1
posts_count: 3
---

# EIP-7425: Tokenized Reserve

Tokenized Reserve is a proposal that allows stakeholders to audit on-chain actions. A traditional reserve fund is created by an entity with banking account systems. Funds flow in and out of the account based on certain rules the owner or entity creates. This proposal is a mechanism to allow stakeholders to show support for out flows from the reserve by creating reserve tokens. Based on use case, extension contracts can be used to allow stakeholders to restrict owner access, require certain criteria before withdrawal, give ownership to new owner after poor ownership.

The goal is to allow entities to participate in the future of tokenization by creating an environment that is transparent.

https://github.com/ethereum/EIPs/pull/7427

## Replies

**jimstir** (2023-08-04):

Reference implementation located here. Needs some testing, and some documentation to make understanding EIP-7425 easier. [GitHub - jimstir/Reserve-Vault](https://github.com/jimstir/Reserve-Vault/tree/main)

---

**jimstir** (2023-08-16):

Here is an educational article about the core logic of tokenized reserves [Tokenized Reserve: An Introduction | by Jimmy Debe | Aug, 2023 | Medium](https://medium.com/@jimstir/tokenized-reserve-an-introduction-bbc8131347c4)

