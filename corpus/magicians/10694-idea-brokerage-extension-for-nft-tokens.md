---
source: magicians
topic_id: 10694
title: "IDEA: Brokerage Extension for NFT tokens"
author: njrapidinnovation
date: "2022-09-06"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/idea-brokerage-extension-for-nft-tokens/10694
views: 431
likes: 0
posts_count: 1
---

# IDEA: Brokerage Extension for NFT tokens

## Abstract

Most of the content is taken from [EIP-2981]

([EIPs/EIPS/eip-2981.md at master · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-2981.md))

This standard allows contracts, such as NFTs that support [ERC-721]and [ERC-1155] interfaces, to inform a brokerage amount to be paid to the NFT creator or rights holder every time the NFT is sold or re-sold through a broker. This is intended for NFT marketplaces that want to support the ongoing funding of artists and other NFT creators. The brokerage payment must be voluntary, as transfer mechanisms such as `transferFrom()` include NFT transfers between wallets, and executing them does not always imply a sale occurred. Marketplaces and individuals implement this standard by retrieving the brokerage payment information with `brokerageInfo()`, which specifies how much to pay to which address for a given sale price.

## Motivation

There are many marketplaces for NFTs but none of them provide a feature to earn high profits. Just like the early days of ERC-20 tokens, NFT marketplace smart contracts are varied by ecosystem and not standardized. This EIP enables all marketplaces to retrieve brokerage payment information for a given NFT.

This minimalist proposal only provides a mechanism to fetch the brokerage amount and recipient. The actual funds transfer is something which the marketplace should execute.

This standard allows NFTs that support [ERC-721] and [ERC-1155] interfaces, to have a standardized way of signalling brokerage information. More specifically, these contracts can now calculate a brokerage amount to provide to the rightful recipient.

Brokerage amounts are always a percentage of the sale price. It is believed that the NFT marketplace ecosystem will implement this brokerage payment standard; in a bid to provide good profits for artists/creators. Brokers will assess the brokerage percentages when making NFT marketing decisions

to attract best buyers.

Without an agreed brokerage payment standard, the NFT ecosystem will lack an effective means to collect brokerage across all marketplaces. This will hamper the growth and adoption of NFTs and demotivate NFT creators from minting new and innovative tokens.

## Advantages

1. To get high sale price as brokers are involved in this process.
2. Enables accurate brokerage payments regardless of which marketplace the NFT is sold or re-sold at.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Marketplaces that support this standard SHOULD implement some method of transferring brokerage to the rightful broker.

Marketplaces MUST pay the brokerage in the same unit of exchange as that of the _salePrice passed to brokerageInfo(). This is equivalent to saying that the _salePrice parameter and the brokerageAmount return value MUST be in the same decimal units. For example, if the sale price is of 18 decimal value, then the brokerage payment must also be paid in 18 decimal value, and if the sale price is in 6 decimal value, then the brokerage payment must also be paid in 6 decimal value.

Implementers of this standard MUST calculate a percentage of the _salePrice when calculating the brokerage amount.

Marketplaces that support this standard SHOULD NOT send a zero-value transaction if the brokerage amount returned is 0. This would waste gas and serves no useful purpose in this EIP.

Implementers of this standard MUST have all of the following functions:

pragma solidity ^0.6.0;

import “./IERC165.sol”;

///

/// dev Interface for the NFT Brokerage Standard

///

interface IBroker is IERC165 {

/// ERC165 bytes to add to interface array - set in parent contract

/// implementing this standard

///

/// bytes4(keccak256(“brokerageInfo(uint256,uint256)”)) == 0xe006f264

/// bytes4 private constant _INTERFACE_ID_BROKER = 0xe006f264;

/// _registerInterface(_INTERFACE_ID_BROKER);

```
/// notice Called with the sale price to determine how much brokerage will be given
/// param _tokenId - the NFT asset queried for brokerage information
/// param _salePrice - the sale price of the NFT asset specified by _tokenId
/// return receiver - address of who should be sent the payment without brokerage
/// return brokerageAmount - the brokerage payment amount for _salePrice
function brokerageInfo(
    uint256 _tokenId,
    uint256 _salePrice
) external view returns (
    address receiver,
    uint256 brokerageAmount
);
```

}

interface IERC165 {

/// notice Query if a contract implements an interface

/// param interfaceID The interface identifier, as specified in ERC-165

/// dev Interface identification is specified in ERC-165. This function

///  uses less than 30,000 gas.

/// return `true` if the contract implements `interfaceID` and

///  `interfaceID` is not 0xffffffff, `false` otherwise

function supportsInterface(bytes4 interfaceID) external view returns (bool);

}
