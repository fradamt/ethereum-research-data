---
source: magicians
topic_id: 10138
title: "EIP-4519: Non-Fungible Tokens Tied to Physical Assets"
author: Arcenegui
date: "2022-07-27"
category: EIPs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/eip-4519-non-fungible-tokens-tied-to-physical-assets/10138
views: 884
likes: 0
posts_count: 1
---

# EIP-4519: Non-Fungible Tokens Tied to Physical Assets

## Abstract

This EIP proposes a standard interface for non-fungible tokens that represent physical assets, such as Internet of Things (IoT) devices. A SmartNFT is tied to a physical asset that can check if the tie is authentic or not. The SmartNFT can include an Ethereum address of the physical asset and, consequently, the physical asset can sign messages or transactions. The physical asset can operate with an operating mode that is defined by its SmartNFT with an attribute named state. The token state can define if the token owner or the token user can use the asset or not. A cryptographically secure mutual authentication process can be carried out between the physical asset and its owner or its user. SmartNFTs extend [ERC-721](https://eips.ethereum.org/EIPS/eip-721) non-fungible tokens, which only allow representing assets by a unique identifier, but not by an Ethereum address. Moreover, SmartNFTs extend ERC-721 NFTs to include users in addition to owners.

Link: https://eips.ethereum.org/EIPS/eip-4519
