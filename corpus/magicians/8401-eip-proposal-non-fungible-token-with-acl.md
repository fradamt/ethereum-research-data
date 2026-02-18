---
source: magicians
topic_id: 8401
title: "EIP proposal: Non-fungible Token With ACL"
author: necokeine
date: "2022-02-23"
category: EIPs
tags: [erc, nft, acl]
url: https://ethereum-magicians.org/t/eip-proposal-non-fungible-token-with-acl/8401
views: 896
likes: 1
posts_count: 5
---

# EIP proposal: Non-fungible Token With ACL

Hi all,

We want to propose a standard for separating ownership and rights of use on digital assets, which is an extension to ERC721.

The motivation is as the supply grows, NFT owners may want to grant different permissions to others like timed ownership(rental), derivative works (IP licensing), co-edit. For example, renting items in blockchain games, licensing and earning royalty from PFP derivative works, hiring builders to build properties on virtual lands.

We have drafted an initial design where the ACL is represented in an u256 integer. The owner or delegate of the owner is able to give other users one or multiple permissions without transferring the ownership such that multiple users can access the NFT in different ways with overlaps in timeline. Also, the permission or “right” itself can be minted as an NFT.

We are organizing a working group for this, please contact necokeine@ or brianzzz95@ on twitter.

## Replies

**yy9527** (2022-04-10):

The proposal details are in [ERC-NFT-with-ACL/EIP proposal.md at master · SolitaireNFT/ERC-NFT-with-ACL · GitHub](https://github.com/SolitaireNFT/ERC-NFT-with-ACL/blob/master/EIP%20proposal.md)

---

**necokeine** (2022-04-24):

Some key point

1. Use a uint256 to represent the new ACL of NFT to users.
2. Keep the ownership (ownerOf()), but the ability to transfer may need some more permission.

---

**jamesavechives** (2024-07-17):

So ownership is much more super then other right?

If ownership transfered, will it affect the other rights?

---

**Mani-T** (2024-07-18):

This proposal holds significant practical value.

