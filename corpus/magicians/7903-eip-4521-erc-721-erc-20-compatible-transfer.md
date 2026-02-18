---
source: magicians
topic_id: 7903
title: "EIP-4521: ERC-721 / ERC-20-compatible transfer"
author: z0r0z
date: "2022-01-05"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-4521-erc-721-erc-20-compatible-transfer/7903
views: 2654
likes: 2
posts_count: 3
---

# EIP-4521: ERC-721 / ERC-20-compatible transfer

The goals of [EIP-4521](https://github.com/ethereum/EIPs/pull/4557) are modest but important for Ethereum users. Namely, it recommends a `transfer()` function for ERC-721 ‘NFTs’ in order to achieve backwards compatibility with ERC-20 tokens.

Currently, ERC-721 only supports `transferFrom()` and `safeTransferFrom()`, and in the event that an NFT is accidentally sent to a contract that only expects ERC-20, it will be locked and unable to be transferred out again.

Further, it is a convenience to smart contract developers to be able to write their contracts in the ERC-20 interface and yet have the ability to manage NFTs at same time without the need to import independent logic. Thus, EIP-4521 suggests a basic extension that allows tokens to work better with user apps, like wallets, and developers who want simpler code to handle a variety of assets, by placing `tokenId` into the typical `transfer` function:

`function transfer(address to, uint256 tokenId) public returns (bool success) { ... )`

## Replies

**mudgen** (2022-03-02):

Nice. I see this makes ERC721 contracts more interoperable with software that works with the ERC20 standard.

---

**ashhanai** (2022-04-18):

Can you help me understand this EIP better and provide an example where same logic can be applied to fungible and non-fungible tokens in a way that amount and id are interchangeable?

Even though the transfer function will not fail, I see a bunch of use cases where contract handles some kind of logic around token amount, which cannot be substituted by id.

