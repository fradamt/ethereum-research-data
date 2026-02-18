---
source: magicians
topic_id: 14549
title: "ERC-7121: SoulBounds Interface"
author: llleo
date: "2023-06-02"
category: ERCs
tags: [nft, erc1155, sbt, soulbounds]
url: https://ethereum-magicians.org/t/erc-7121-soulbounds-interface/14549
views: 655
likes: 0
posts_count: 4
---

# ERC-7121: SoulBounds Interface

The SoulBounds EIP proposes a standard interface, called SoulBounds, that extends the `ERC-1155` token standard to support the representation and management of soulbound assets on the Ethereum network. Soulbound assets are unique digital items that are permanently bound to a specific user or address, preventing transferability to other addresses.

## Replies

**abcoathup** (2023-06-02):

https://github.com/ethereum/EIPs/pull/7121/files

---

**SamWilsn** (2023-10-24):

Regarding the `soulbind` and `soulunbind` functions, other token standards omit functions which are only likely to be called by the deployer of the contract. For example, ERC-1155 does not specify a `mint` or `burn` function. I’d recommend not including the `soulbind` and `soulunbind` functions because they aren’t likely to be used by most people interacting with the contract. Further, some contracts may not even support unbinding tokens, so that function will be entirely useless for them.

---

**SamWilsn** (2023-10-24):

Bit of [bikeshedding](https://en.wiktionary.org/wiki/bikeshedding), but have you considered `soulOf` as an alternative to `soulboundOf`?

