---
source: magicians
topic_id: 8245
title: "EIP-4786: Link Common Token to ERC-721"
author: poria-cat
date: "2022-02-09"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-4786-link-common-token-to-erc-721/8245
views: 704
likes: 0
posts_count: 2
---

# EIP-4786: Link Common Token to ERC-721

## Abstract

ERC-4786 provides an extension for ERC-721 to be composed with other Tokens (ERC-721/ERC-1155/ERC-20). This applies to the creation of a composable/graph NFT. In this standard, the ERC-721 Token is a first class citizen and can freely compose with other Tokens. The result is get an interesting NFT with a graph structure.

## Motivation

The ability to compose opens up many more possibilities for ERC-721, here are some possible scenarios:

1. assets owned by an address can be transformed into assets owned by an NFT.
2. Linking an avatar NFT to an ENS
3. an avatar/game character composed from different NFTs
4. a number of assets packaged with an NFT and sold together, etc.

ERC-998 attempts to solve this problem, but ERC-998 introduces more complexity to the composability, and the main advantages of the standard over ERC-998 are:

1. there is no top-down/bottom-up concept
2. the function names are closer to those of the regular operations graph structure (link/updateTarget/unlink), which makes the standard easier to understand
3. the function names are sufficiently uniform when dealing with different Tokens (linkERCx/updateERCxTarget/unlinkERCx)
4. easy to extend

Links:

PR: [ERC-4786: Link Common Token to ERC-721 by poria-cat · Pull Request #4786 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4786)

Reference implementation: [GitHub - poria-cat/ERC-4786](https://github.com/poria-cat/ERC-4786)

![:beers:](https://ethereum-magicians.org/images/emoji/twitter/beers.png?v=15)

## Replies

**poria-cat** (2022-02-11):

This is a thread for discussion of EIP, and I would collect to collect your feedback.

Many thanks!

![:beers:](https://ethereum-magicians.org/images/emoji/twitter/beers.png?v=10)

