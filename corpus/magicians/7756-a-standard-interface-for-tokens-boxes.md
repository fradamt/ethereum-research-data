---
source: magicians
topic_id: 7756
title: A standard interface for tokens boxes
author: vrolland
date: "2021-12-13"
category: Magicians > Primordial Soup
tags: [token, erc-721, erc1155, erc20, box]
url: https://ethereum-magicians.org/t/a-standard-interface-for-tokens-boxes/7756
views: 1003
likes: 0
posts_count: 2
---

# A standard interface for tokens boxes

Hi everyone,

We are working on a project to turn an ERC721 into a box able to store and transfer other tokens (ETH, ERC20, ERC721, and ERC1155).

Developing it, we thought it would interest others and we could suggest it as a new EIP.

Here is the suggested EIP and, at the end, a github repo with an implementation of this interface. What do you think?

---

## eip:
title: Token box standard
description: A token box standard allowing contracts to store and withdraw multiple tokens with a unique call.
author: vrolland (github/vrolland), wabi (github/wabieth), yomarion (github/yomarion)
discussions-to:
type: Standards Track
category: ERC
status: Draft
created: 2021-12-13

## Simple Summary

A standard interface for token boxes

## Abstract

The following standard proposes an interface for contracts to store and withdraw many tokens (ETH, ERC20, ERC721, and ERC1155) in a single call.

It can be used, e.g:

- to create boxes allowing users to transfer a batch of diverse assets under one NFT.
- by smart contract wallets to handle multiple tokens transfers in a standard way.

## Motivation

We needed this interface to transform ERC721 into boxes that can store assets and implement custom logic. That might save time to others.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

**Every box compliant contract must implement the `IERC721Receiver`, `IERC1155Receiver` and `ERC165` interfaces**:

```solidity
pragma solidity ^0.8.0;

 * @title token box standard
 *  Note: the ERC-165 identifier for this interface is 0xaf0eefe8.
interface IBox /* is ERC165, IERC721Receiver, IERC1155Receiver */ {
    /// @dev ERC721 token information {address and token ids} used for function parameters
    struct ERC721TokenInfo {
        address addr;
        uint256[] ids;
    }
    /// @dev ERC20 token information {address and amount} used for function parameters
    struct ERC20TokenInfo {
        address addr;
        uint256 amount;
    }
    /// @dev ERC1155 token information {address, token ids and token amounts} used for function parameters
    struct ERC1155TokenInfo {
        address addr;
        uint256[] ids;
        uint256[] amounts;
    }

    /// @dev This is emitted when ethers and/or tokens are stored in a box
    event Store(
        uint256 indexed boxId,
        uint256 ethAmount,
        ERC20TokenInfo[] erc20s,
        ERC721TokenInfo[] erc721s,
        ERC1155TokenInfo[] erc1155s
    );

    /// @dev This is emitted when ethers and/or tokens are withdrawn from a box
    event Withdraw(
        uint256 indexed boxId,
        uint256 ethAmount,
        ERC20TokenInfo[] erc20s,
        ERC721TokenInfo[] erc721s,
        ERC1155TokenInfo[] erc1155s,
        address to
    );

    /// @dev This is emitted when ethers and/or tokens are transferred from a box to another
    event TransferBetweenBoxes(
        uint256 indexed srcBoxId,
        uint256 indexed destBoxId,
        uint256 ethAmount,
        ERC20TokenInfo[] erc20s,
        ERC721TokenInfo[] erc721s,
        ERC1155TokenInfo[] erc1155s
    );

    /**
     * @notice Store tokens in a box
     * @param _boxId id of the box to store the tokens in
     * @param _erc20s list of erc20 to store
     * @param _erc721s list of erc721 to store
     * @param _erc1155s list of erc1155 to store
     */
    function store(uint256 _boxId, ERC20TokenInfo[] _erc20s, ERC721TokenInfo[] _erc721s, ERC1155TokenInfo[] _erc1155s) external;

     /**
     * @notice Withdraw tokens from a box to an external address
     * @dev Throws if the box does not contain ALL the tokens listed and their required balance
     * @param _boxId id of the box to store the tokens in
     * @param _erc20s list of erc20 to withdraw
     * @param _erc721s list of erc721 to withdraw
     * @param _erc1155s list of erc1155 to withdraw
     * @param _to address to receive the tokens
     */
    function withdraw(uint256 _boxId, ERC20TokenInfo[] _erc20s, ERC721TokenInfo[] _erc721s, ERC1155TokenInfo[] _erc1155s, address _to) external;

     /**
     * @notice Transfer tokens from a box to another
     * @dev Throws if the box does not contain ALL the tokens listed and their required balance
     * @param _boxSrcId id of the box to withdraw the tokens from
     * @param _boxDestId id of the box to store the tokens in
     * @param _erc20s list of erc20 to transfer
     * @param _erc721s list of erc721 to transfer
     * @param _erc1155s list of erc1155 to transfer
     */
    function transferBetweenBoxes(uint256 _boxSrcId, uint256 _boxDestId, ERC20TokenInfo[] _erc20s, ERC721TokenInfo[] _erc721s, ERC1155TokenInfo[] _erc1155s) external;

     /**
     * @notice Returns the balance of an erc20 of a box
     * @param _boxId id of the box
     * @param _tokenAddress the erc20 token address
     * @return The balance owned by `_boxId`, possibly zero
     */
    function erc20BalanceOf(uint256 _boxId, address _tokenAddress) external view returns (uint256);

     /**
     * @notice Returns the balance of an erc721 token of a box
     * @param _boxId id of the box
     * @param _tokenAddress the erc721 address
     * @param _tokenId the token id to query the ownership
     * @return 1 if the token is in the box, 0 otherwise
     */
    function erc721BalanceOf(uint256 _boxId, address _tokenAddress, uint256 _tokenId) external view returns (uint256);

     /**
     * @notice Returns the balance of an erc1155 token of a box
     * @param _boxId id of the box
     * @param _tokenAddress the erc1155 address
     * @param _tokenId the token id to query the balance
     * @return The balance owned by `_boxId`, possibly zero
     */
    function erc1155BalanceOf(uint256 _boxId, address _tokenAddress, uint256 _tokenId) external view returns (uint256);
}

```

### Caveats

In order to ease the implementation, the standard does not force the support of boxes containing other boxes.

## Implementations

CryptoTreasure – a first implementation

- github repository
- web site

## Replies

**MidnightLightning** (2022-06-14):

For discussion/comparison/reference, this concept seems similar to the ([now abandoned](https://github.com/ethereum/EIPs/issues/998#issuecomment-1012320451)) [EIP998](https://eips.ethereum.org/EIPS/eip-998) proposal (which poses it as a “composability” feature, intending the ownership to be more “tree-like” than “box-like”), and the [Charged Particles protocol](https://docs.charged.fi/) (created as “a protocol” rather than “a standard”, such that one central contract on each chain can control the logic of the “contents”, while the NFT collection itself can be just a pointer/identifier that acts as a “key” to gain access to those contents).

