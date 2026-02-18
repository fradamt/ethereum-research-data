---
source: magicians
topic_id: 14516
title: "ERC-7110: NFT Dynamic Ownership"
author: hiddenintheworld
date: "2023-05-31"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/erc-7110-nft-dynamic-ownership/14516
views: 1131
likes: 5
posts_count: 8
---

# ERC-7110: NFT Dynamic Ownership

---

## eip: 7110
title: NFT Dynamic Ownership
description: An innovative extension to NFT token that introduces dynamic ownership and nesting capabilities
author: hiddenintheworld.eth ()
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2023-06-01
requires: 721

## Abstract

A standard interface for non-fungible tokens (NFTs) with dynamic ownership, which extends the capabilities of the original `ERC-721` standard by enabling NFTs to be owned by either addresses or other NFTs. The proposed `ERC-721D` standard introduces dynamic ownership in the world of NFTs. Instead of a token being owned solely by an address, as it is in the `ERC-721` standard, tokens following the `ERC-721D` standard can be owned by either an address or another token. This opens up new possibilities and adds an extra layer of complexity and opportunity in the NFT space. This EIP outlines the rules and functions needed to support this dynamic ownership model while maintaining compatibility with `ERC-721` standards.

## Motivation

Non-fungible tokens (NFTs) have paved the way for unique digital assets. However, they are inherently restricted by their static ownership. `ERC-721D` aims to innovate the concept of NFT ownership by allowing tokens to have dynamic ownership chains. This could unlock an entirely new dimension for tokenized digital assets and decentralized applications (dApps).

## Specification

### Overview

`ERC-721D` is a standard interface for NFTs with dynamic ownership. It provides essential functionalities to manage, transfer, and track the ownership of tokens. It is an extension of the `ERC-721` standard.

### Data Structures

The `ERC-721D` standard introduces a new data structure, **`Ownership`**. Each token has an **`Ownership`** associated with it that consists of the **`ownerAddress`** and the **`tokenId`**. The **`ownerAddress`** is the address of the token owner, which can be an EOA or a contract address. If the owner is another NFT, then tokenId represents the ID of the owner token.

### Functions

The `ERC-721D` standard defines a set of functions for interacting with tokens. It includes existing functions from the `ERC-721` standard, like **`balanceOf`** and **`ownerOf`**, with necessary modifications to support dynamic ownership. It also introduces new functions like **`setOwnership`** to manage dynamic ownership. The **`mint`** and **`burn`** functions have been overridden to account for changes in the balance of dynamic owners. The **`_transfer`** function has been updated to handle transfers involving dynamic owners.

### Implementation

Below is the full implementation:

```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/*

The ERC721D standard is an advanced and dynamic implementation of the ERC721 token standard.
This innovative contract takes the non-fungible token (NFT) concept a step further by introducing dynamic ownership.
In conventional NFTs, a token can only be owned by an address.
However, in the ERC721D standard, ownership can be dynamic, meaning an NFT can be owned by either an address or another NFT.
This introduces a new layer of complexity and opportunity in the NFT space.

*/
contract ERC721D is ERC721, Ownable {

    // The Ownership structure represents the owner of the token
    struct Ownership {
        address ownerAddress;  // The address of the owner
        uint256 tokenId;       // The token Id of the owner if the owner is an NFT
    }

    // Mapping from token ID to Ownership
    mapping(uint256 => Ownership) private _owners;

    // Mapping from owner address to token balance
    mapping(address => uint256) private _balances;

    constructor() ERC721("ERC721D", "ERC721D") {}

    // Mint new token
    // `to` is the address that will own the minted token
    // `tokenId` is the identifier for the new token
    function mint(address to, uint256 tokenId) public onlyOwner {
        _mint(to, tokenId);
        _owners[tokenId] = Ownership(to, 0);
        _balances[to] += 1;
    }

    // Burn token
    // `tokenId` is the identifier for the token
    function burn(uint256 tokenId) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721D: caller is not owner nor approved");

        Ownership memory oldOwnership = _owners[tokenId];
        if (oldOwnership.ownerAddress != address(0)) {
            // Decrease the balance of the old owner
            _balances[oldOwnership.ownerAddress] -= 1;
        }

        // Set token ownership to the zero address (burning the token)
        _owners[tokenId] = Ownership(address(0), 0);
        _burn(tokenId);
    }

    // Transfer Nested Ownership of a token
    // `tokenId` is the identifier for the token
    // `newOwnerAddress` is the address of the new owner
    // `newTokenId` is the token Id of the new owner if the owner is an NFT
    function transferNestedOwnership(uint256 tokenId, address newOwnerAddress, uint256 newTokenId) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721D: caller is not owner nor approved");
        Ownership memory oldOwnership = _owners[tokenId];

        // First time ownership, balance increases
        // Ownership is changing, adjust the balances
        if (oldOwnership.ownerAddress == address(0) || oldOwnership.ownerAddress != newOwnerAddress) {
            address oldOwner = oldOwnership.ownerAddress;
            _balances[oldOwner] -= 1;
            _balances[newOwnerAddress] += 1;
        }
        // Else: The token is being re-assigned to a different token but the same owner, do not change the balance.

        _owners[tokenId] = Ownership(newOwnerAddress, newTokenId);
    }

    // Overrides the 'ownerOf' function from the ERC721 standard.
    // Returns the current owner of the token identified by `tokenId`.
    // It navigates through potential layers of ownership, making it suitable for dynamic token structures.
    function ownerOf(uint256 tokenId) public view override(ERC721) returns (address) {
        address currentOwnerAddress = _owners[tokenId].ownerAddress;
        uint256 currentTokenId = _owners[tokenId].tokenId;

        // This loop will go through the ownership layers of the token.
        // It stops if the owner address is zero (no owner), or if there's an error calling the ownerOf function on the owner contract,
        // or if the returned owner is the same as the current owner (end of ownership chain).
        while (currentOwnerAddress != address(0)) {
            bytes memory payload = abi.encodeWithSignature("ownerOf(uint256)", currentTokenId);
            (bool success, bytes memory result) = currentOwnerAddress.staticcall(payload);
            if (!success || result.length == 0) {
                break;
            }

            address newOwnerAddress = abi.decode(result, (address));
            if (newOwnerAddress != currentOwnerAddress) {
                currentOwnerAddress = newOwnerAddress;
                currentTokenId = _owners[currentTokenId].tokenId;
            } else {
                break;
            }
        }

        // Return the final owner in the chain
        return currentOwnerAddress;
    }

    // This internal function is used to implement the transfer of tokens, following the ERC721 standard but allowing dynamic token ownership.
    // It transfers the `tokenId` token from the `from` address to the `to` address.
    function _transfer(address from, address to, uint256 tokenId) internal virtual override {
        require(ownerOf(tokenId) == from, "ERC721D: transfer of token that is not owned");
        Ownership memory oldOwnership = _owners[tokenId];

        _approve(address(0), tokenId);
        _owners[tokenId] = Ownership(to, 0);

        if (oldOwnership.ownerAddress == address(0)) {
            // The token is being owned for the first time, increase the balance of the new owner
            _balances[to] += 1;
        } else if (oldOwnership.ownerAddress != to) {
            // The token is changing owner, adjust the balances
            address oldOwner = oldOwnership.ownerAddress;
            _balances[oldOwner] -= 1;
            _balances[to] += 1;
        }

        emit Transfer(from, to, tokenId);
    }

    // An internal function that checks if a `spender` is an approved operator or the owner of a token.
    // Returns true if the `spender` is an approved operator or the owner of the `tokenId` token.
    // The function follows the ERC721 standard requirements.
    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view override returns (bool) {
        require(_exists(tokenId), "ERC721D: operator query for nonexistent token");
        address owner = ownerOf(tokenId);
        return (spender == owner || getApproved(tokenId) == spender || isApprovedForAll(owner, spender));
    }

    // Overrides the `balanceOf` function from the ERC721 standard.
    // Returns the balance (number of owned tokens) of the `owner` address.
    // It checks for the zero address and returns the balance from the internal _balances mapping.
    function balanceOf(address owner) public view override(ERC721) returns (uint256) {
        require(owner != address(0), "ERC721D: balance query for the zero address");
        return _balances[owner];
    }

    // This function returns the ownership details of the `tokenId` token.
    // Returns a struct with the owner's address and the token id of the token owned by the returned token (if any).
    function owners(uint256 tokenId) public view returns (Ownership memory) {
        return _owners[tokenId];
    }

}
```

## Rationale

The `ERC-721D` standard seeks to expand the potential of NFTs by introducing dynamic ownership. This innovation could open up new use cases in the fields of digital assets, dApps, digital identity, and more. As the digital economy evolves, the need for complex and dynamic relationships between tokens will become increasingly relevant, and the `ERC-721D` standard addresses this need.

## Backwards Compatibility

`ERC-721D` is fully backward compatible with the `ERC-721` standard. It extends the `ERC-721` standard by adding dynamic ownership while maintaining all existing functionalities. Any existing `ERC-721` token can be upgraded to an `ERC-721D` token while retaining its original capabilities.

## Security Considerations

As with any smart contract standard, security considerations are paramount. Implementers of `ERC-721D` should ensure that they have robust systems in place for managing the Ownership structure and that transfers, minting, and burning of tokens are handled securely. It’s crucial to thoroughly test and audit any contracts that implement `ERC-721D` to avoid potential security risks. Moreover, dealing with dynamic ownership presents additional complexities, which require extra caution while implementing this standard.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**abcoathup** (2023-06-01):

Before you get too far using the name ERC8192.  EIP editors assign an EIP number (generally the PR number, but the decision is with the editors) (from: [EIP-1: EIP Purpose and Guidelines](https://eips.ethereum.org/EIPS/eip-1#eip-numbers)).

Suggest reading: [Guidelines on How to write EIP. Do’s and Don’ts including examples | by Anett | The Fellowship of Ethereum Magicians | Medium](https://medium.com/ethereum-magicians/guide-on-how-to-write-perfect-eip-70488ad70bec)

---

**hiddenintheworld** (2023-06-01):

Thank you for the tips, I have editted the format according to the guideline.

---

**MidnightLightning** (2023-06-01):

This proposal seems fundamentally similar to [ERC6059](https://eips.ethereum.org/EIPS/eip-6059) (which is out of draft phase and accepted as a standard). Both this and ERC6059 target new tokens, baking the logic into the collection contract itself. What benefits does this proposal have over ERC6059?

Giving this proposal a nickname of “ERC721D” follows the trend of some different implementations of the ERC721 standard naming themselves that way (e.g. [ERC721A](https://www.erc721a.org/), [ERC721X](https://erc721x.org/)). But those are are custom implementations by specific companies/teams, not an EIP standard. If this proposal seeks to be an EIP, then I feel it is an anti-pattern to refer to another ERC’s number in the name/nickname of the new EIP.

Additionally, this proposal “extending the ERC721 standard” is different than the proposal being “backwards compatible with the ERC721 standard”. Being “backwards compatible” means the older thing (ERC721 in this case) can be used with the new thing with no changes. Requiring the older thing upgrade/change in order to be part of the system is not backwards compatibility.

---

**hiddenintheworld** (2023-06-01):

I didn’t know about ERC6059 when I was writting this, thank you for telling me this.

I have read through EIP-6059 and noticed there are some differences:

EIP-6059 focuses on child-parent management in which in the proposed ERC-8192, the child and parent mapping is also available(stored in the struct also) but does not need to keep track of it, since you can already do a query and return each NFT’s owner(another address / NFT).

If you actually run the code, you will see that even `_balances` is already handled perfectly which is not discussed in ERC-6059. I think the steps of

**1. Reject child token**

**2. Abandon child token**

**3. Unnest child token**

is redundant and by taking the simpler approach in EIP-8192 which is running while loop of the recursive mapping.

The actual implementation of EIP-6059 is questionably hard since it could be costly in terms of gas while this proposed EIP-8192 already tackled everything (from considering `ownerOf` , and `balanceOf` to the compatibility of functions and variables in ERC-721). If you tried running the smart contract, it is extremely gas efficient.

It is backward compatible because the contract is still an ERC-721 standard. In general, if a smart contract overrides a function specified in the ERC-721 standard, it can still be considered ERC-721 compliant as long as the function maintains the same interface and semantics as defined in the ERC-721 standard.

---

**hiddenintheworld** (2023-06-01):

Overriding a function does not necessarily break backward compatibility, but it can potentially do so if the changes in the function’s behavior disrupt the functionality of existing systems using the ERC-721 standard. But the functions which have been override could still be be run directly on an ERC-721 contract.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> function ownerOf

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> function _transfer

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> function _isApprovedOrOwner

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> function balanceOf

---

**stoicdev0** (2023-06-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> EIP-6059 focuses on child-parent management in which in the proposed ERC-8192, the child and parent mapping is also available(stored in the struct also) but does not need to keep track of it, since you can already do a query and return each NFT’s owner(another address / NFT).

I don’t really get your point here, what mapping are you talking about that this has and 6059 does not? In 6059 you can get the direct owner or root owner, and children for each NFT.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> you will see that even _balances is already handled perfectly which is not discussed in ERC-6059

Not being discussed does not mean it does not handle them, I encourage you to give a try. There are ready to use implementations on [this npm package](https://www.npmjs.com/package/@rmrk-team/evm-contracts).

On that topic, I suspect you have problem on the way you handle balances. I might be wrong but this is a problem we encountered long ago while building 6059, so we decided to keep track of balances for the direct owners only, otherwise gas consumption would make it unusable.

Say Alice holds Token A, which owns token B, which owns token C. Alice’s balance is 3 as expected. Now transfer token B to Bob. Since you are not recursively updating balances on children (which would be too expensive with this model)  Alice’s balance will be 2 and Bob’s 1, even though Alice owns now only A and Bob owns B and C.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> I think the steps of
>
>
> 1. Reject child token
> 2. Abandon child token
> 3. Unnest child token
>
>
> is redundant

These are not steps, they are different operations that can be done with the `transferChild` method. We expanded for clarity. You can bypass the accepting of children, which has been discussed on the thread and addressed in the rationale, in which case you do not need accept or reject/abandon operations.

By doing that, you are only left with 5-6 operations which would cover the functionality you are proposing. We did not propose only those since we wanted a more robust standard. In other words, the functionality proposed here can be achieved by simply auto-accepting children, but it is not the case the other way around.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hiddenintheworld/48/9658_2.png) hiddenintheworld:

> The actual implementation of EIP-6059 is questionably hard since it could be costly in terms of gas

Difficulty is subjective. I find diamonds too complex for my taste, but they are widely used. Although we include over 10 methods, we do so to provide huge flexibility. Additionally, this was the result of over a year of iterations to make sure it was safe and did not have problems as the one I suspect you currently have with balances tracking.

We also provide the aforementioned npm package with a minimal implementation and ready to use implementations (Open-zeppelin style) so less advanced users can take advantage of it with very few code. It is open source and has close to 100% test coverage, [this is the repo](https://github.com/rmrk-team/evm) if you are curious. We even have an [template repo](https://github.com/rmrk-team/evm-template) for quick start. The sample contract uses an implementation of ERC-6220, but it is just as simple to start using ERC-6059.

Regarding gas, we use some optimizations as asking indexes for operations and keeping balances for direct owners only, we found that every operation will take AT MOST twice as operations on ERC-721, say mint, transfer, burn. In most cases, the gas is comparable.

I hope you find this useful, I’m happy to answer any doubts you have regarding ERC-6059.

---

**hiddenintheworld** (2023-06-07):

Thx for your information, you are correct that only direct ownership should be kept track of, if token A is owned by token B, the balance will be counted inside balanceOf[tokenBContractAddress] inside the contract of tokenA.

