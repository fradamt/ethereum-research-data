---
source: magicians
topic_id: 11404
title: "Alternatives to ERC-4907: Rental standard with more adaptability to existing applications"
author: in2xx
date: "2022-10-20"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/alternatives-to-erc-4907-rental-standard-with-more-adaptability-to-existing-applications/11404
views: 735
likes: 1
posts_count: 4
---

# Alternatives to ERC-4907: Rental standard with more adaptability to existing applications

Hi, there, ![:waving_hand:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand.png?v=15)

Our team is considering proposing an alternative to ERC-4907 as a rental standard; ERC721Rental.

## Motivation

An ERC-4907 defines a user role that will expire in time. They separate NFT’s role into Ownership and temporary use rights.

ERC-4907 implements userOf methods to refer temporary users but most existing application does not support executing `userOf` methods.

So, if a renter rents NFT supported by ERC-4907 from a lender, they can not use NFT for any token gate application and also marketplace or wallet’s inventory.

Since the market already moves to “Application fat” from “Protocol fat”, we propose more adaptable rental standards that existing applications easily to support rental functions.

## Rental Mechanics

While ERC-4907 defines a user as a subordinate concept of owner, ERC721Rental defines superOwner as a superior concept of an owner. The owner authority defined in ERC721 is moved to a superOwner, and the user authority proposed in ERC-4907 is redefined as owner.

### How owner and superOwner works?

**balanceOf(address owner) → uint256 balance** *(external)*

Subtract the number of tokens temporarily loaned from the quantity of tokens owned by the `owner` account and add back the number of tokens loaned.

**superBalanceOf(address owner) → uint256 superBalance** *(external)*

Returns the number of tokens owned by the `owner` account.

See `ERC721.balanceOf`.

**ownerOf(uint256 tokenId) → temporary owner address** *(external)*

Returns the address of the temporary owner of `tokenId`, or `superOwnerOf` if there is no borrower.

**superOwner(uint256 tokenId) → address of the owner** *(external)*

Returns the address of the owner of the `tokenId` token.

See `ERC721.ownerOf`.

**setOwner(uint256 tokenId, address owner, uint64 expires)** *(external)*

Change the owner of the `tokenId` token to `owner` until the time specified by `expires`.

Emit an `UpdateOwner` event.

**approve(address to, uint256 tokenId)** *(external)*

Grant permission to transfer `tokenId` to another account or temporarily change the owner. Once the token is transferred, the permission is revoked.

Since only one account can be authorized at a time, previous permissions can be revoked by allowing 0x00…

Emit an `Approval` event.

**isApprovedForAll(address superOwner, address operator) → bool** *(external)*

Return whether the `operator` is allowed to manage all assets of the `superOwner`.

See `ERC721.setApprovalForAll`.

**_mint(address to, uint256 tokenId)** *(internal)*

Mint a new `tokenId` token to the `to` address. When minting, add `tokenId` to the `_allTokens` array.

Emit a `Transfer` event.

**_burn(uint256 tokenId)** *(internal)*

Change the owner of the `tokenId` token to 0x00… and the permission for the transfer to 0x00…

Also, remove `tokenId` from the `_allTokens` array when you burn it.

Emit a `Transfer` event.

## Questions

Do you think these would be meaningful use cases?

Do you have any thoughts on the implementation?

I feel at the same time a contradiction in rehashing the ERC-4907 discussion but would like to discuss how much of a challenge the applicability to applications is to this contradiction.

## Replies

**0xanders** (2022-10-20):

How to process when the rental is finished ?

The owner can list an NFT on OpenSea, but no one can buy it, the floor price will be nonsense.

---

**in2xx** (2022-10-20):

Thank you 0xanders.

It automatically returns when the rental time expires.

All approve function refers superOwner so the renter can not list NFT on Opensea.

so, the renter cannot operates a floor price.

---

**in2xx** (2022-10-21):

I am adding some source codes. The superOwner is equal to the owner of ERC721 and the owner of ERC721Rental is equal to the user of ERC-4907. this is a simple expression.



      [github.com](https://github.com/synschismo/RentafiNative/blob/master/contracts/RentafiNative.sol)





####



```sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import '@openzeppelin/contracts/token/ERC721/ERC721.sol';

contract RentafiNative is ERC721 {
  // Token name
  string private _name;

  // Token symbol
  string private _symbol;

  // MODIFIED - RentaFi Native
  // Array with all token ids, used for enumeration
  uint256[] private _allTokens;

  // MODIFIED - RentaFi Native
  struct OwnerInfo {
    address owner; // address of user role
    address superOwner;
```

  This file has been truncated. [show original](https://github.com/synschismo/RentafiNative/blob/master/contracts/RentafiNative.sol)

