---
source: magicians
topic_id: 9612
title: Standard For Specific NFT Owned Smart Contracts
author: mnkhod
date: "2022-06-14"
category: Magicians > Primordial Soup
tags: [erc, nft]
url: https://ethereum-magicians.org/t/standard-for-specific-nft-owned-smart-contracts/9612
views: 816
likes: 0
posts_count: 3
---

# Standard For Specific NFT Owned Smart Contracts

This idea has been formed around NFT’s having more utility. I truly believe more utility would come forth to the NFT ecosystem if Smart Contract ownerships can be enhanced with Specific NFT’s.

Instead of having Address Ownership like the one we use from OpenZeppelin’s Ownable contract , i believe there should be a standard for Smart Contract NFT Ownership.

Allowing smart contracts to be only accessible by certain NFT holders will bring more utility to the NFT Ecosystem. Truly bringing more innovation to Smart Contract Wallets or Business Logic related smart contracts & allowing NFT holders to have more utility rather than flipping all day long

NFT holders are incentivized to hold their NFT than flipping them.

Having this standard will incentivize developers to create more innovative smart contracts that utilizes NFT’s

I believe this can be achieve & i will also be including an implementation soon on this thread.



      [github.com](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.6.0/contracts/access/Ownable.sol)





####



```sol
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts v4.4.1 (access/Ownable.sol)

pragma solidity ^0.8.0;

import "../utils/Context.sol";

/**
 * @dev Contract module which provides a basic access control mechanism, where
 * there is an account (an owner) that can be granted exclusive access to
 * specific functions.
 *
 * By default, the owner account will be the one that deploys the contract. This
 * can later be changed with {transferOwnership}.
 *
 * This module is used through inheritance. It will make available the modifier
 * `onlyOwner`, which can be applied to your functions to restrict their use to
 * the owner.
 */
abstract contract Ownable is Context {
```

  This file has been truncated. [show original](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.6.0/contracts/access/Ownable.sol)

## Replies

**riksucks** (2022-08-04):

Hello [@mnkhod](/u/mnkhod) !

I am new here, so pardon me if I do anything out of place. I think this indeed is a good idea. Right now the stuff that are being done when it comes to “membership” stuff using NFT is tokengating. Which is mostly frontend/backend. But not on chain.

I believe, an upgradation of `AccessControl` by openzeppelin can be made that is based around owning a certain kind of NFT or any sort of FT. Maybe even generalize it and make it for ERC-1155.

---

**urataps** (2023-05-05):

Hello this idea looks interesting and I’ve been thinking about it for a long time. I’m glad somebody else also thought about it.

But, the whole idea behind NFTs is that they are unique, so if a smart contract is an NFT then there should not be allowed any `delegatecall` to it, since that would copy the smart contract entirely.

Also another problem, NFTs are controlled by the ERC721 specification, therefore NFT owned smart contracts should be deployed via a Factory that is ERC721, so at each NFT mint a new contract is deployed. But again, how the Factory gets this implementation and how unique it is at each mint.

