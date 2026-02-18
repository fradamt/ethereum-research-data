---
source: magicians
topic_id: 5821
title: EIP-3386 - Wrapping ERC721/ERC1155 with ERC20
author: ashrowz1
date: "2021-03-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-3386-wrapping-erc721-erc1155-with-erc20/5821
views: 860
likes: 0
posts_count: 2
---

# EIP-3386 - Wrapping ERC721/ERC1155 with ERC20

EIP3386 proposes to create an interface to the exchange between NFTs and their derivative ERC20 tokens. This involves the transfer of NFTs into the pool in exchange for minted ERC20s, and the burning of ERC20s in exchange for NFTs from the pool.

The issue: https://github.com/ethereum/EIPs/issues/3384

The pull request: https://github.com/ethereum/EIPs/pull/3386

Existing examples of this concept include NFTX, NFT20, WrappedKitties.

## Replies

**ashrowz1** (2021-04-06):

Created an example implementation using ERC721 here: https://github.com/ashrowz/erc-3386

