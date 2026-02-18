---
source: magicians
topic_id: 4594
title: Finalizable Service Token (FST) what do you think?
author: AlePart
date: "2020-09-10"
category: EIPs
tags: [token]
url: https://ethereum-magicians.org/t/finalizable-service-token-fst-what-do-you-think/4594
views: 577
likes: 0
posts_count: 1
---

# Finalizable Service Token (FST) what do you think?

I thought a particular token designed for companies and generally service selling.

The token can be admitted and transferred only n-times and can be finalized to an address with data (like a receipt)

[discussion on github](https://github.com/ethereum/EIPs/issues/2965)

## Simple Summary

A standard interface for Finalizable Service Token enables companies or professionals to emit a token for its services.

## Abstract

This improvemnt wnats to **propose** a **service token transferable n-times** and **mintable**.

The main focus of this token Is about a distributed service that can be used with this token.

## Motivation

I will try to explain this initial idea by examples.

### Application Example 1 (On Demand Service)

A company wants to emit a license for software that it develops the machine with this software wants to send a paid token with its custom data to a user wallet to enable software X on machine Y for 1 yr.

The token can’t be transferred after finalization with or without data or after a certain amount of transfer. The multi transfer can be useful in case of using other contracts before or using different company wallets.

### Application Example 2 (Validation service)

let Actor1 Actor2 buy 2 different Token and wants to make a Deal with a Validation using a contract Validator.

- Actor1 finalize a token with data given by Actor2 and sent it to a Validator
- Actor2 finalize a token with data given by Actor1 and sent it to a Validator
- Validator mint 2 different tokens as a Deal form Actor1 and Actor2 and finalize 2 tokens that send to actors.

## Specification

I just thought an initial basic interface for this EIP and a possible implementation

```auto
pragma solidity ^0.7.1;
// SPDX-License-Identifier: MIT

interface IERCXXX{

    /**
     * @dev Emitted when `tokenId` token is transfered from `from` to `to`.
     */
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
        /**
     * @dev Emitted when `owner` enables `approved` to manage the `tokenId` token.
     */
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);

    /**
     * @dev Returns the amount of tokens in existence.
     */
    function totalSupply() external view returns (uint256);

    /**
     * @dev Returns the amount of tokens owned by `account`.
     */
    function balanceOf(address account) external view returns (uint256);

    /**
     * @dev Mint a given `tokenId` to `to`
     *
     *Requirements:
     *
     * - `to` cannot be the zero address.
     * - `tokenId` token must not exist.
     * - `allowedMaxTransfer` maximum transfers for the minted token
     * Emits a {Transfer} event.
     */
    function mint(address to, uint256 tokenId, uint256 allowedMaxTransfer) external;

    /**
     * @dev Finalizes the token with given `tokenId` and send it from `from` to `to` adding `data` to token.
     * after calling this function token can't be anymore transfered and data can't be modified anymore.
     *
     *Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must exist.
     * Emits a {Transfer} event.
     */
    function finalizeAndTransferFrom(address from,address to, uint256 tokenId, string memory data) external;

     /**
     * @dev Transfer token from `from` to `to` and decrement the internal transfer counter.
     *
     *Requirements:
     *
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must exist.
     * Emits a {Transfer} event.
     */
    function transferFrom(address from,address to, uint256 tokenId) external;

    /**
     * @dev Gets the token by giveing the `tokenId`.
     *
     *Requirements:
     *
     * - `tokenId` token must exist.
     */
    function getTokenData(uint256 tokenID) external view returns(string memory);

    /**
     * @dev Gets the remaining transfer for the given `tokenId`.
     *
     *Requirements:
     *
     * - `tokenId` token must exist.
     */
    function getResidualTransfer(uint256 tokenId) external view returns(uint256) ;

    /**
     * @dev Gives permission to `to` to transfer `tokenId` token to another account.
     * The approval is cleared when the token is transferred.
     *
     * Only a single account can be approved at a time, so approving the zero address clears previous approvals.
     *
     * Requirements:
     *
     * - The caller must own the token or be an approved operator.
     * - `tokenId` must exist.
     *
     * Emits an {Approval} event.
     */
    function approve(address to, uint256 tokenId) external;

    /**
     * @dev Returns the account approved for `tokenId` token.
     *
     * Requirements:
     *
     * - `tokenId` must exist.
     */
    function getApproved(uint256 tokenId) external view returns (address[] memory operators);

}
contract ERCxxx is IERCXXX{

    string private _name;
    string private _symbol;
    mapping(address=>bool) private _approvedMinters;
    mapping(uint256 => uint256) private _residualTransfer;
    mapping(uint256 => address[]) private _tokenOwners;
    mapping(uint256 => string) private _tokenData;
    mapping(address => uint256) private _balances;

    uint256[] private _tokens;

    constructor(string memory tokenName, string memory tokenSymbol)
    {
        _name = tokenName;
        _symbol = tokenSymbol;

        _approvedMinters[msg.sender] = true;
    }
    function Symbol()public view returns(string memory)
    {
        return _symbol;
    }
    function _exists(uint256 tokenId) private view returns(bool)
    {
        if(_tokenOwners[tokenId].length == 0)
            return false;
        return true;
    }

    function _isOwnerOf(address owner,uint256 tokenId) private view returns(bool)
    {
        address[] memory addr = _tokenOwners[tokenId];
        for(uint256 i =0; i 0, "ERCXXX: transfer limit reached for this token");
        require(_isOwnerOf(from,tokenId), "ERCXXX: only token owner can finalize and/or transfer");
    }
    function finalizeAndTransfer(address to, uint256 tokenId, string memory data) public
    {
        _transferCheck(msg.sender,tokenId);
        _residualTransfer[tokenId]=1;
        _transfer(msg.sender,to,tokenId,data);
    }

    function transfer(address to, uint256 tokenId) public
    {
        _transferCheck(msg.sender,tokenId);
        _transfer(msg.sender,to,tokenId,"");
    }

    function finalizeAndTransferFrom(address from,address to, uint256 tokenId, string memory data) public override
    {
        _transferCheck(from,tokenId);
        _residualTransfer[tokenId]=1;
        _transfer(from,to,tokenId,data);
    }

    function transferFrom(address from,address to, uint256 tokenId) public override
    {
        _transferCheck(from,tokenId);
        _transfer(from,to,tokenId,"");
    }


    function getResidualTransfer(uint256 tokenId) public view override returns(uint256)
    {
        return _residualTransfer[tokenId];
    }

    function balanceOf(address wallet) public view override returns(uint256)
    {
        return _balances[wallet];
    }

    function approve(address to, uint256 tokenId) public override
    {
        _tokenOwners[tokenId].push(to);
    }

    function getApproved(uint256 tokenId) public view override returns (address[] memory operators)
    {
        return _tokenOwners[tokenId];
    }

    function getTokenData(uint256 tokenID) public view override returns(string memory)
    {
        return _tokenData[tokenID];
    }
}
```
