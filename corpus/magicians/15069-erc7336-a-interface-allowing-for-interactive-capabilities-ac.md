---
source: magicians
topic_id: 15069
title: "ERC7336: A interface allowing for interactive capabilities across multiple registries like ENS"
author: zihaoccc
date: "2023-07-15"
category: EIPs
tags: [ens, registry]
url: https://ethereum-magicians.org/t/erc7336-a-interface-allowing-for-interactive-capabilities-across-multiple-registries-like-ens/15069
views: 480
likes: 1
posts_count: 2
---

# ERC7336: A interface allowing for interactive capabilities across multiple registries like ENS

The objective of this EIP is to propose the **Universal Domain Namespace(UDoN)**, which aims to facilitate onchain registry entries. Each entry in this structure adopts a mapping type, allowing for interactive capabilities across multiple registries like ENS and NFT accounts.

The necessity for a unified method of data retrieval across various registries is apparent. A structured methodology that allows for seamless reading of data from one registry to another, effectively linking chains of information, is thus proposed. This EIP seeks to standardize an interface that not only supports interaction but also promotes integration with multi-protocol registries. With the utilization of such an interface, a single deployed contract can retrieve records from different combinations of registries, such as ENS (ERC-137), the registry for royalty payments of NFTs (ERC-6786), the registry for smart contract accounts owned by ERC-721 tokens (ERC-6551), and other registries as defined by varying protocols.

The URL to the proposal is as follows:

https://github.com/ethereum/EIPs/pull/7336

## Replies

**technicallykind** (2023-07-27):

What would the compliance process look like for new registries?

