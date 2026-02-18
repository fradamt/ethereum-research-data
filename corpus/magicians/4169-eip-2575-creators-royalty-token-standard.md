---
source: magicians
topic_id: 4169
title: "EIP-2575: Creators' Royalty Token standard"
author: naomasabit
date: "2020-03-29"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2575-creators-royalty-token-standard/4169
views: 868
likes: 0
posts_count: 1
---

# EIP-2575: Creators' Royalty Token standard

## Simple Summary

A standard interface for non-fungible tokens that enables artwork creators to receive a fee not only when their works are sold for the first time, but also their works are resold.

## Abstract

This standard outlines a smart contract interface based on ERC-721, which is a standard for non-fungible tokens. The key issue of using it is that an original author who creates an item cannot receive any fees after giving or selling it to another.  Creator’s Royalty Token enables creators to get a fee whenever the token is transferred, which has a function of the decentralized exchange. Hence, a partial amount of the transaction value will always be paid to the creator.

## Detail



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/2575)












####



        opened 12:31PM - 29 Mar 20 UTC



          closed 03:58PM - 31 Mar 20 UTC



        [![](https://avatars.githubusercontent.com/u/31416389?v=4)
          naomasabit](https://github.com/naomasabit)










```
---
eip: 2575
title: Creators' Royalty Token standard
author: Nao Hanamu[…]()ra(@naomasabit),
       Shoji Fukunaga(@mogya2) <s.fukunaga@conata.world>,
       Wataru Shinohara(@wshino),
       Shumpei Koike(@shunp),
       Akira Tsuruoka(@akira-19)
discussions-to: https://github.com/ethereum/EIPs/issues/2575
status: Draft
type: Standards Track
category: ERC
created: 2020-03-29
---
```

## Simple Summary
A standard interface for non-fungible tokens that enables artwork creators to receive a fee not only when their works are sold for the first time, but also their works are resold.

## Abstract
This standard outlines a smart contract interface based on ERC-721, which is a standard for non-fungible tokens. The key issue of using it is that an original author who creates an item cannot receive any fees after giving or selling it to another.  Creator’s Royalty Token enables creators to get a fee whenever the token is transferred, which has a function of the decentralized exchange. Hence, a partial amount of the transaction value will always be paid to the creator.

## Motivation
It is predicted that a lot of creators who design a piece of artwork would associate their items with non-fungible tokens based on ERC-721.  The expected issue in this case is that the artwork would be resold on the secondary market, such as OpenSea, even though the artist cannot get any fees.  This problem often happens even in the real world, and that makes creators disappointed.
The new functionality is possible with the design of receiving a fee for the sale whenever non-fungible tokens are transferred. You do not need to embed any code but use this interface instead of ERC-721 so that artwork creators can receive a fee. Currently, we are developing a product called [Conata](https://conata.world/) and will implement the token based on this standard.

## Specification
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

**Smart contracts implementing the ERC-2575 standard MUST implement all of the functions in the ERC-2575 interface.**

**Smart contracts implementing the ERC-2575 standard MUST implement the ERC-721.**

```solidity
contract IERC2575 is ERC721Full, ERC721Mintable, Ownable {

    event ReadyForSale(
        address buyer,
        uint256 tokenId,
        uint256 price,
        uint256 expireBlockNumber);

    function getPublisherFeeRate() public view returns (uint256);

    function getCreator(uint256 tokenId) public view returns (address payable);

    function getCreatorFeeRate(uint256 tokenId) public view returns (uint256);

    function getTradeExpires(bytes32 tradeHash) public view returns (uint256);

    function getTradePrices(bytes32 tradeHash) public view returns (uint256);

    function setPublisherFeeRate(uint256 feeRate) external;

    function setCreator(uint256 tokenId, address payable creator) public;

    function setCreatorFeeRate(uint256 tokenId, uint256 feeRate) external;

    function readyForSale(address buyer, uint256 tokenId, uint256 price, uint256 expireBlockNumber) external;

    function cancelTradeOrder(address buyer, uint256 tokenId) external;

    function tradeAndDistributeFees(address payable seller, uint256 tokenId) external payable;
}

```

The token contract MUST implement the above contract. The implementation MUST follow the specifications described below.

**Creator’s Royalty Token Overview**

<img width="518" alt="Creator’s Royalty Token Overview" src="https://user-images.githubusercontent.com/31416389/77847492-516ac000-71f8-11ea-8c40-009acbcefef8.png">

## Creator’s Royalty Token

**Buyer**
Everyone can buy non-fungible tokens via Creator’s Royalty Token contract. The buyer pays ETH as the token price. Paid ETH is distributed to Publisher and Creator as a trade fee.

**Seller**
The owner of a non-fungible token can sell it via Creator’s Royalty Token contract. The seller sends the non-fungible token to a buyer.

**Creator**
Creators produce artworks such as characters, music and digital arts. Their artworks are published as non-fungible tokens.

**Publisher**
Publishers mint a creator's token instead of the creator. The role of them is to advertise artworks and enhance their brand images. The Creator’s address should be set if there is no publisher. In this case, creators manage their token themselves.

## View Functions

The view functions detailed below MUST be implemented.

**getPublisherFeeRate function**

`function getPublisherFeeRate() public view returns (uint256)`

Get the fee rate used on a publisher.
returns: Fee rate of the publisher

**getCreator function**

`function getCreator(uint256 tokenId) public view returns (address payable)`

Get the creator’s address.
params: tokenId: tokenID used on ERC721
returns: Address of the creator

**getCreatorFeeRate function**

`function getCreatorFeeRate(uint32 tokenId) public view returns (uint256)`

Get the fee rate according to the tokenId.

params: tokenIdassetType: tokenID used on ERC721
returns: Fee rate of the asset type

NOTE: If the contract has a large number of tokenIDs, you can optionally set the classification as an asset type by token digits and link the classification to the creator instead of using the tokenID. In that case, the contract has to have a state valuable that plays a role as a filter.

NOTE: If the contract has a large number of tokenIDs, you can optionally set the classification as an asset type by token digits and link the classification to the creator instead of using the tokenID. In that case, the contract has to have a state valuable that plays a role as a filter.

- The buyer argument MUST be the address of an account/contract that wants to buy the asset (is not the same as msg.sender, which is the publisher’s address)
- The price argument MUST be more than zero.
- The expireBlockNumber MUST be between more than zero and less than the number of the current block.
- The keccak256 hash, which is calculated by msg.sender, buyer and tokenId,  is stored as state value to use in the TradeAndDistributionFees function.

(implementation)
```solidity
function readyForSale(
   address buyer,
   uint256 tokenId,
   uint256 price,
   uint256 expireBlockNumber) external {
        require(buyer != address(0), "Buyer doesn't exist");
        require(price > 0, "Price argument must be more than zero");
        require(expireBlockNumber > 0, "ExpireBlockNumber must be more than zero");
        require(expireBlockNumber > block.number, "ExpireBlockNumber is expired");
        bytes32 tradeHash = keccak256(abi.encodePacked(msg.sender, buyer, tokenId));
        _setTradeExpires(tradeHash, expireBlockNumber);
        _setTradePrices(tradeHash, price);
        TradeOrders[tradeHash]._isCancelled = false;
        emit ReadyForSale(buyer, tokenId, price, expireBlockNumber);
    }
```
NOTE: This function emits the event named ReadyForSale.

**Trade and Distribution Fees**

`function tradeAndDistributeFees(address payable seller, uint256 tokenId) external payable`

Call this function to transfer the ownership of the artwork and distribute fees to the author. In this function, the two functions are invoked; _signAndPayTransfer and _changeTransfer.

- The seller argument MUST be the address of an account/contract that wants to sell the asset.
- The block number, when being called, MUST NOT exceed the limit data that can be fetched by the getTradeExpires function. -- - The block number is associated with a hash value, which is created by the seller address, the msg.sender address and tokenId.
- The msg.value MUST be more than the trade price, which is set through the _setTradePrices function.
- The hash value, which is calculated from the seller, msg.sender and tokenId, is used for checking whether or not it matches the value that is created in the ReadyForSale function.
- _tradeAndDistributeFees is a private function that distributes fees, which are computed in this function, to the creator, and the publisher. The code below is the implementation example.

```solidity
function _tradeAndDistributeFees(address payable seller, uint256 tokenId, uint256 price) internal {
        uint256 creatorFeeRate = getCreatorFeeRate(tokenId);
        uint256 creatorFee = _computeCreatorFee(price, creatorFeeRate);
        uint256 publisherFee = _computePublisherFee(price);
        uint256 payment = uint256(price.sub(creatorFee).sub(publisherFee));

        address payable creator = getCreator(tokenId);

        _transferFrom(seller, msg.sender, tokenId);
        creator.transfer(creatorFee);
        _publisher.transfer(publisherFee);
        seller.transfer(payment);
 }

```

`_changeTransfer` is a private function that returns ETH to the sender, which is the remaining number of the transaction. The code below is the implementation example.

```solidity
function _changeTransfer(uint256 tradePrice) internal {
        if (msg.value > tradePrice) {
            uint256 change = msg.value.sub(tradePrice);
            msg.sender.transfer(change);
        }
}
```

NOTE: The Transfer event, which is defined on the ERC-721, is emitted by this function.

Example) Creator’s Royalty Tokens related sequence flow on Conata Project.

![conata (1)](https://user-images.githubusercontent.com/31416389/77844506-5cb2f100-71e2-11ea-93ea-6369a517fcbc.jpg)

**Cancel TradeOrder**

`function cancelTradeOrder(address buyer, uint256 tokenId) external`

Call this function so that the buyer could cancel the order of the trade.
- The buyer argument MUST be the address of an account/contract that ordered the request for buying the token ID.
- The tokenId argument MUST be the number that the buyer has chosen.

**Setter Function**

`function setPublisherFeeRate(uint256 feeRate) external`

The feeRate argument CAN be set as a publisher fee rate by the owner of the contract.

`function setCreator(uint256 tokenId, address payable creator) public`

The creator argument MUST be the address of an account that created the artwork. The owner of the contract CAN map the tokenId and creator address.

`function setCreatorFeeRate(uint256 tokenId, uint256 feeRate) external`

The feeRate argument CAN be set as a creator fee rate by the owner of the contract.


## Rationale
**Based on ERC721**

ERC-721 is widely applied to many projects that use non-fungible tokens such as CryptoKitties. Since a creator’s artwork is registered as non-fungible tokens, this standard inherits ERC-721.

Each artwork has a unique token ID. Also, the token will be transferred through ERC-721 _transferFrom function in tradeAndDistributeFee function, though there are some restrictions to transfer tokens as explained in the following section.

**Limited Transfer**

This standard doesn’t provide a general transfer function, by which non-fungible tokens holders can transfer their non-fungible tokens freely whenever they want. This is because creators can’t get royalties if it is possible. Transfer is executed with tradeAndDistributeFees function, and every time holders transfer their non-fungible tokens, the creators can get royalties through the function.

**Decentralized Exchange Function**

This standard provides DEX through readyForSale function and tradeAndDistributeFee function. In order to allow a buyer to purchase a non-fungible token, the token’s holder (seller) passes a buyer’s address and a token ID as arguments to readyForSale function, and stores the hash value of the arguments with the seller’s own address. After that, the buyer calls tradeAndDistributeFee, which checks the hash value, and transfers the NFT and distributes the fees if the hash value is correct.

**Fee Distribution**

In this standard, not only creators but also publishers can get some fees. Furthermore, publishers can set the fee rate like OpenSea, which is one of the most famous non-fungible token secondary markets. A fee rate for publishers is set through setPublisherFeeRate and A fee rate for creators is set through setCreatorFeeRate.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).












Wanted to get feedback from the community.
