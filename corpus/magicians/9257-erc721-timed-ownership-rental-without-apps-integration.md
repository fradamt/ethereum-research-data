---
source: magicians
topic_id: 9257
title: ERC721 Timed Ownership (Rental) without apps integration
author: tommyshieh
date: "2022-05-14"
category: ERCs
tags: [token]
url: https://ethereum-magicians.org/t/erc721-timed-ownership-rental-without-apps-integration/9257
views: 647
likes: 0
posts_count: 2
---

# ERC721 Timed Ownership (Rental) without apps integration

## Abstract

This standard is an extension of ERC721. It proposes a new **TimedOwner** concept in addition to the existing Owner concept. For example address A is the **TimedOwner** of token P until  X timestamp. After X timestamp, the **TimedOwner** of the token P becomes B. This concept can easily achieves NFT rental without any extra third party integration which want to validate the ownership of a token. Also there’s no gas fee needed as there’s no transaction engaged.

## Motivation

There are many proposals to support “rental” functionality for ERC721.  For example:

1. EIP4907: ERC-721 User And Expires Extension
2. ERC721 extension to enable rental
3. ERC-4400: EIP-721 Consumable Extension

However, most of them introduce a new role (user, functional user, consumer..etc) and they require apps to integrate with the new interface in order to validate the renter/functional/consumer user. Also, transaction/gas fee is needed when renting a token. This whole thing can be simpler.

## Proposed solution

### Summary

- Introduce “TimedOwner”, the owner of a token in a period of time.
- Extend the ERC721 interface and introduce a timedTransferFrom method. This method transfers the ownership of  from the current owner to . The timed ownership is valid until the  time
- During the timed ownership, the ERC721 ownerOf function returns the address of timeOwner. This is the ONLY thing timedOwner can do and the restriction is enforced on the smart contract. TimeOwner CAN NOT do any other operation on the token, for example transfer, approve, burn.. etc.

With this proposal, any app can seamlessly integrate with the smart contract to validate the current ownership of a token.

### Interface (extend ERC721)

```auto
interface IERCXXX {
    /// @notice Transfer the token from owner to timedOwner with expirationTime
    /// @dev The zero address indicates there is no user
    /// Throws if `tokenId` is not valid NFT
    /// @param timedOwner  The timedOwner of the NFT
    /// @param expires  UNIX timestamp, The ownerOf function will return timedOwner before expires
    function timedTransferFrom(uint256 tokenId, address timedOwner, uint64 expirationTime) external;

    /// @notice Get owner of an NFT. And NFT can have sudoOwner and timedOwner at the same time.
    /// @dev The zero address indicates that there is no user or the user is expired
    /// @param tokenId The NFT to get the user address for
    /// @return The user address for this NFT
    function sudoOwnerOf(uint256 tokenId) external view returns(address);
}
```

### Implementation

```auto
/*
Introducing a new timed_owners mapping that maps from token ID to a
map of timeStamp to owner address, for example:
{
   1: [
	    {
            “timestamp”: 0
            “Owner”
        },
        {
	        “timestamp”: 1654041600
 	        “Owner”
        }
      ]
}
*/

struct TimedOwner {
    uint expirationTime;
    address owner
  }

mapping(uint256 => TimedOwner[]) private timed_owners;
```

- When the existing TransferFrom function is called, no data is added to the timed_owners as the TransferFrom is not a timed ownership transfer. Everything works same as how it works today.
- When the timedTransferFrom function is called, the expirationTime information is also stored in this timed_owners.
- When OwnerOf(A) is called, the smart contract first:

Check if there’s an entry A in timed_owners, if no, use the original logic openzeppelin-contracts/contracts/token/ERC721/ERC721.sol at master · OpenZeppelin/openzeppelin-contracts · GitHub
- If the entry A is presented in the timed_owners, compare the current timestamp with the record in the timed_owners to figure out the current owner.

Many functions in the ERC721 need to be overridden to prevent the timedOwner from doing operations like approve, transfer, burn .. etc, I am skipping those parts in this post.

Feedback?

## Replies

**TylerMeta** (2022-05-15):

https://github.com/ethereum/EIPs/pull/5058

EIP-5058 is an erc721 extension that supports block height-based locking of nft, which can meet rental needs without transferring nft.

