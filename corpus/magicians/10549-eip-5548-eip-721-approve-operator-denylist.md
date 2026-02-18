---
source: magicians
topic_id: 10549
title: EIP-5548 - EIP-721 Approve Operator DenyList
author: mitchellfchan
date: "2022-08-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5548-eip-721-approve-operator-denylist/10549
views: 642
likes: 0
posts_count: 2
---

# EIP-5548 - EIP-721 Approve Operator DenyList

This EIP is currently in DRAFT status:



      [github.com](https://github.com/mitchellfchan/EIPs/blob/master/EIPS/eip-5548.md)





####



```md
---
eip: 5548
title: NFT Operator Approval Control
description: An EIP-721 extension to deny specific smart contracts the ability to spend tokens on an owner's behalf
author: Mitchell F Chan (@mitchellfchan), et al.
discussions-to: TK
status: Draft
type: Standards Track
category: ERC
created: 2022-08-27
requires: 165, 721
---

## Abstract

This EIP is an extension to [EIP-721](./eip-721.md) which standardizes NFT creators' ability to deny specific marketplaces or smart contracts the ability to spend tokens on an owner's behalf. This is achieved by adding a check against an owner-defined denyList in the `Approve` or `SetApprovalForAll` functions.

This is intended for NFT creators who wish to exercise some control over where their creations may be bought and sold, without limiting the rights of token holders.

There are many reasons why an NFT creator may wish to exercise control over which intermediary smart-contracts may buy and sell their creations on an owner's behalf. An intermediary platform may present artwork in a manner which the creator finds objectionable or dishonest, or the intermediary platform may openly disregard off-chain codes, conventions, or practices which the creator considers to be an essential part of the artwork or their career.
```

  This file has been truncated. [show original](https://github.com/mitchellfchan/EIPs/blob/master/EIPS/eip-5548.md)










In summary, it adds a check against an owner-defined denyList in the `Approve` or `SetApprovalForAll` functions.

## Replies

**SamWilsn** (2022-09-16):

I’m concerned that this EIP can be trivially defeated. You could easily transfer ownership to the marketplace, create and approve proxy contracts, or just list and sell wrapper tokens. Attempts to implement royalty payments on transfer on-chain are… difficult to say the least.

I’d encourage you to look into other alternative methods of generating continuing income. For example, Harberger taxes on NFTs have been a popular topic lately! (See [Harberger Taxes NFT](https://ethereum-magicians.org/t/eip-5320-harberger-taxes-nft/10084) for an example.)

That said, nothing I’ve said here is a blocker for getting your EIP merged!

