---
source: magicians
topic_id: 3895
title: ERC EIP for lending NFT (ERC-721) tokens?
author: mars
date: "2020-01-02"
category: Uncategorized
tags: [nft]
url: https://ethereum-magicians.org/t/erc-eip-for-lending-nft-erc-721-tokens/3895
views: 2875
likes: 0
posts_count: 2
---

# ERC EIP for lending NFT (ERC-721) tokens?

I can imagine that key to my home is an ERC-721 compatible token.

I would like to rent my home for a period of 12 months.

I would like to keep the compatibility with all the existing standards and infrastructure.

https://eips.ethereum.org/EIPS/eip-721

> function ownerOf(uint256 _tokenId) external view returns (address);

I was searching for “NFT lending” and saw this diagram via `tinlake.com`

[![examples](https://ethereum-magicians.org/uploads/default/optimized/2X/6/64dde2015e7e617664bf3b00c3d4c5ae76aafcc8_2_690x340.png)examples1184×585 51.4 KB](https://ethereum-magicians.org/uploads/default/64dde2015e7e617664bf3b00c3d4c5ae76aafcc8)

It seems like the situation I describe would require “NFT Deposit Contract” or “NFT Wrapper Contract” that would be a superset of ERC-721. It would implement all the ERC-721 methods and a few more things:

- internal state of ownership
- function transferring the barebone (unwraped, raw) token to the rightful owner

Before I start overthinking too much, are you aware of any similar work in the space?

## Replies

**flaskr** (2022-02-09):

Hey, did you ever go anywhere with this? I don’t see any other works at the moment. I’m hoping that a standardized way of checking ownership can be used by apps, and a common interface can allow the wrappers to cross-check with other wrappers using `ownerOf` and EIP-165.

I think that this can be very useful, on top of rental use cases. I also made a prototype of this here:



      [github.com](https://github.com/flaskr/nft-lend-v2)




  ![image](https://opengraph.githubassets.com/e0f474c8e03c15d763d8bb62cd653316/flaskr/nft-lend-v2)



###



Non-custodial NFT lending via pseudo-ownership










I’ll like to build on it to include functions for

- WrapperFactory that tracks created wrappers
- Ability to query for ‘virtual ownership’ across different wrapper contracts.

