---
source: magicians
topic_id: 8305
title: ERC-4884 Rentable NFT Standard
author: muhammedea
date: "2022-02-14"
category: ERCs
tags: [erc, nft, token, erc1155]
url: https://ethereum-magicians.org/t/erc-4884-rentable-nft-standard/8305
views: 1828
likes: 5
posts_count: 4
---

# ERC-4884 Rentable NFT Standard

# Renting Extension For NFT Contracts

## Abstract

This extension defines some extra functions to the ERC-721 standard for renting NFT tokens to another account.

This enables NFT owners to rent their assets to someone else for some period of time.

So the owner of the token will be changed temporarily.

This can be applied to ERC-1155 tokens too.

Because an ERC-1155 contract can have fungible tokens (FT) and non-fungible tokens (NFT), so this functionality will be usable by only NFTs.

So the contract should implement [split id proposal](https://eips.ethereum.org/EIPS/eip-1155#split-id-bits) in ERC-1155 standard

## Motivation

This kind of functionality is specifically important for gaming industry.

It is important for a gamer to have the ability to give an NFT to someone else for a period of time.

For example, you can give an NFT to someone else for playing for a period of time. So sharing an NFT will be possible.

## Specification

This specification defines an interface for ERC-721 and ERC-1155 contracts.

**rentOut** function will transfer the ownership to the renter.

After the renting period has passed, the actual owner can use **finishRenting** function to take the ownership back.

Renter can finish renting earlier than that.

**principalOwner** and **isRented** functions are helper functions.

```solidity
pragma solidity ^0.8.0;

/**
    @title ERC-721 Rentable
 */
interface ERC721Rentable /* is ERC165 */ {
    /**
        @dev This event will be emitted when token is rented
        tokenId: token id to be rented
        owner:  principal owner address
        renter: renter address
        expiresAt:  end of renting period as timestamp
    */
    event Rented(uint256 indexed tokenId, address indexed owner, address indexed renter, uint256 expiresAt);

    /**
        @dev This event will be emitted when renting is finished by the owner or renter
        tokenId: token id to be rented
        owner:  principal owner address
        renter: renter address
        expiresAt:  end of renting period as timestamp
    */
    event FinishedRent(uint256 indexed tokenId, address indexed owner, address indexed renter, uint256 expiresAt);

    /**
        @notice rentOut
        @dev Rent a token to another address. This will change the owner.
        @param renter: renter address
        @param tokenId: token id to be rented
        @param expiresAt: end of renting period as timestamp
    */
    function rentOut(address renter, uint256 tokenId, uint256 expiresAt) external;

    /**
        @notice finishRenting
        @dev This will returns the token, back to the actual owner. Renter can run this anytime but owner can run after expire time.
        @param tokenId: token id
    */
    function finishRenting(uint256 tokenId) external;

    /**
        @notice principalOwner
        @dev  Get the actual owner of the rented token
        @param tokenId: token id
    */
    function principalOwner(uint256 tokenId) external returns (address);

    /**
        @notice isRented
        @dev  Get whether or not the token is rented
        @param tokenId: token id
    */
    function isRented(uint256 tokenId) external returns (bool);
}
```

## Security Considerations

### Transfer Checks

A rented token can not be transferred to someone else. So on every transfer the token status should be checked.

If the token is rented, it can not be transferred to someone else.

### Finishing Renting

**finishRenting** function can be called by the renter anytime, but the owner can run only after expire time.

---

Really appreciate any thoughts or feedback!

Thanks all,

Muhammed

## Replies

**rayzhudev** (2022-04-12):

Great proposal! I’m a big fan of it. Two comments:

1. I would prefer to use the term lending rather than renting. Renting implies payment and that may not necessarily be the case.
2. I think there should be a function
expiryTime(uint256 tokenId) external returns (uint256);
to get the expiry date separately from the event.

---

**j-asefa** (2022-05-16):

Hi [@muhammedea](/u/muhammedea),

I’ve been thinking a lot about a similar standard. I’ve written up an implementation of something very similar called **ERC721Lendable** here: [GitHub - j-asefa/ERC721Lendable: An extension to the ERC721 standard that allows NFT owners to trustlessly lend their tokens to others for a fixed duration.](https://github.com/j-asefa/ERC721Lendable)

There are a lot of use cases even outside of gaming where this would be useful. I mention some examples in the readme. I would be happy to collaborate on an EIP for this with you if you are up for it!

---

**vicnaum** (2022-05-17):

This standard looks pretty good! We’re developing NFT rentals in Oiler (product is called Nafta, it’s already on Mainnet, and code is available on github, but we rely on flash-loans instead - so you don’t need collateral like here in ERC-4884, but also you don’t need to reimplement existing ERC721 contracts. We also have a long-term rent similar to this standard, sometimes with the help of Wrappers, but without ownerOf() support - which is really cool here!

Actually, I think that Nafta might be the first project to support this standard using its Wrappers? I need to research for a bit on how to connect this standard with flash-loans, or maybe we can make a separate Wrapper for making any NFT compliant with ERC-4884. Need to look at it and I will get back to you @muhhamedea

