---
source: magicians
topic_id: 8399
title: ERC CallistoNFT standard
author: Dexaran
date: "2022-02-23"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/erc-callistonft-standard/8399
views: 2854
likes: 2
posts_count: 2
---

# ERC CallistoNFT standard

ERC - CallistoNFT

```auto
Preamble
EIP:
Title: Non-fungible Container Token Standard
Author: Dexaran
Type: Standard
Category: ERC
Status: Draft
Created: 2022-22-02
```

**Simple Summary**

An interface for non-fungible tokens and minor behavior logic standardisation.

**Abstract**

This standard allows for the implementation of a standard API for non-fungible tokens (henceforth referred to as “NFTs”) within smart contracts. This standard introduces the following features:

Built-in trades - user’s no longer need a 3d party markets to exchange NFTs of this standard. NFTs allow users to place “bids” and “asks” directly on desired NFT through the token contract.

Creators fee system - NFT creators can define a fee that will be subtracted from each built-in trade therefore monetizing their NFTs.

NFT Content - each NFT allows a piece of unique data to be written to it.

User-defined content - owner of a NFT can record their own data to this NFT.

Think of your NFTs as containers. Each container is unique. A manufacturer (creator of the token) can determine its initial properties: color, shape, put labels. If you own a container then you can place whatever you want inside it.

**Motivation**

This standard extends the functionality of ERC721. This standard addresses the problem of reliance on third party exchanges and NFT monetization and standardizes metadata storage methods which is essential in some specific cases.

Security. Giving third party exchange access to your NFT is a security risk. Every exchange is subject to hacks.

Monetization for NFT creators. Currently, NFT creators sell their NFTs in most cases - this is a one-time income. Built-in trades allow content creators to develop an additional revenue stream that scales with the number of deals a particular NFT faces.

Metadata storage. ERC721 introduces tokenURI function that suggests to store metadata off-chain. This proposal standardizes a method of on-chain metadata storing and accessing.

Specification

```auto
/// @title CallistoNFT standard
/// @dev   This is an alternative standard that provides NFT creators with additional features that ERC721 does not implement by default. This standard is NOT a set of features that extends ERC721 but a separate standard that defines alternative mechanisms. A token can be both ERC721 and CallistoNFT at the same time if it implements all functions required by both standards.

interface ICallistoNFT {

    /// @dev This emits when ownership of any NFT changes by any mechanism.
    ///  This event emits when NFTs are created (`from` == 0) and destroyed
    ///  (`to` == 0). Exception: during contract creation, any number of NFTs
    ///  may be created and assigned without emitting Transfer. At the time of
    ///  any transfer, the approved address for that NFT (if any) is reset to none.
    event Transfer     (address indexed from, address indexed to, uint256 indexed tokenId);

    /// @dev This emits when transfer occurs and records "data" parameter of this transfer.
    /// Exception: this event only triggers when an external party calls the contract
    /// to transfer tokens. If there are any internal mechanisms that change ownership of tokens
    /// then this event may be bypassed.
    /// Data assignment may be important to document financial operations on-chain.
    /// For example  this piece of data 54686973206973206D7920646F6E6174696F6E20746F204A6F65.
    /// is a Hex-encoded message "This is my donation to Joe"
    event TransferData (bytes data);

    /// @dev This emits when a new Bid is placed on an NFT.
    event NewBid       (uint256 indexed tokenID, uint256 indexed bidAmount, bytes bidData);

    /// @dev This emits when a requirements for Built-In trade are met i.e.
    /// a new Bid matched Ask or a new Ask matched existing Bid.
    event TokenTrade   (uint256 indexed tokenID, address indexed new_owner, address indexed previous_owner, uint256 priceInWEI);

    /// @dev A structure to store NFT metadata.
    struct Properties {

        // In this example properties of the given NFT are stored
        // in a dynamically sized array of strings
        // properties can be re-defined for any specific info
        // that a particular NFT is intended to store.

        /* Properties could look like this:
        bytes   bytes_property1;
        bytes   bytes_property2;
        address address_property3;
        */

        // NFTs of this standard MUST contain "properties" string array in their Properties structure
        // properties[0] is allocated for user-defined content.
        string[] properties;
    }

    /// @dev Returns a name of the token.
    function name() external view returns (string memory);

    /// @dev Returns a shortened version of the token name.
    function symbol() external view returns (string memory);

    /// @dev Returns the name of this standard if the contract implements all standardized functions.
    //  Can be useful for some UI implementations.
    /// @return Returns "CallistoNFT"
    function standard() external view returns (string memory);

    /// @notice Count all NFTs assigned to an owner
    ///  this function is compatible with ERC721 `balanceOf`
    /// @dev NFTs assigned to the zero address are considered invalid, and this
    ///  function throws for queries about the zero address.
    /// @param _who An address for whom to query the balance
    /// @return The number of NFTs owned by `_who`
    function balanceOf(address _who) external view returns (uint256);

    /// @notice Find the owner of an NFT
    ///  this function is compatible with ERC721 `ownerOf`
    /// @dev NFTs assigned to zero address are considered invalid, and queries
    ///  about them do throw.
    /// @param _tokenId The identifier for an NFT
    /// @return The address of the owner of the NFT
    function ownerOf(uint256 _tokenId) external view returns (address);

    /// @notice Transfers the ownership of an NFT from sender address to another address.
    ///  this function calls the onERC721Received on the receiver
    ///  because this NFT handler function is widely adopted already.
    /// @dev Throws unless `msg.sender` is the current owner of this NFT. Throws if `_to` is the zero address. Throws if
    ///  `_tokenId` is not a valid NFT. When transfer is complete, this function
    ///  checks if `_to` is a smart contract (code size > 0). If so, it calls
    ///  `onERC721Received` on `_to` and throws if the return value is not
    ///  `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`.
    /// @param _to Recipient of the transfer
    /// @param _tokenId The ID of NFT to transfer
    /// @param _data Additional data with no specified format, sent in call to `_to`
    /// @return Returns `true` if the transfer was successful
    function transfer(address _to, uint256 _tokenId, bytes calldata _data) external returns (bool);

    /// @notice This function is optional. Transfers the ownership of an NFT from sender address to another address
    ///  without notifying recipient of the transfer.
    /// @dev This function may be necessary in some specific situations
    ///  where it may be known that the address `_to` is designed to receive NFTs
    ///  but for some reason it is not clear if it implements `INFTReceived` interface.
    ///  For example during the initial token sale it is known that anyone who contributes the funds
    ///  must receive an NFT in exchange.
    /// @param _to Recipient of the transfer
    /// @param _tokenId The ID of NFT to transfer
    /// @param _data Additional data with no specified format, sent in call to `_to`
    /// @return Returns `true` if the transfer was successful
    function silentTransfer(address _to, uint256 _tokenId) external returns (bool);

    /// @notice Returns the value of the price specified by the owner of this NFT
    ///  at this price the NFT can be sold immediately if a bid matching this price is placed.
    /// @dev Returns 0 if there is no price specified by the owner of the NFT.
    ///  Also price automatically resets when NFT is transferred to a new owner.
    /// @param _tokenId The ID of NFT for which the price is queried
    /// @return Returns the amount of WEI that must be paid for this NFT in order to buy it automatically.
    function priceOf(uint256 _tokenId) external view returns (uint256);

    /// @notice Returns the value of highest placed bid for a queried NFT.
    /// @dev In reference implementation a token can only have highest bid and it returns the funds
    ///  to the previous bidder in case he is outbidded. There can be a more complex system of bidding
    ///  but this function returns the value of highest bid in WEI.
    ///  0 is returned if there are no bids for the queried NFT.
    ///  Bid value can not be higher than `priceOf(_tokenId)`
    /// @param _tokenId The ID of NFT for which the value of highest bid is queried.
    /// @return Returns the amount of WEI that bidder wants to pay in order to acquire this NFT.
    ///  The funds are deposited to the NFT contract upon bid placement.
    function bidOf(uint256 _tokenId) external view returns (uint256 price, address payable bidder, uint256 timestamp);

    /// @notice Returns the metadata for a queried NFT.
    /// @dev This function returns the whole `Properties` structure for given NFT.
    ///  `Properties` structure can contain custom set of variables specific for a particular NFT
    ///  and an array of strings called `properties`.
    /// @param _tokenId The ID of NFT for which Properties structure is queried.
    /// @return Returns the whole Properties structure for a given NFT.
    ///  This structure contains all metadata related to this specific token.
    ///  There can be another type of metadata related to a group of tokens (see Classified Extension)
    function getTokenProperties(uint256 _tokenId) external view returns (Properties memory);

    /// @notice Returns a specified piece of metadata for a queried NFT.
    /// @dev This function returns the value of `properties[_propertyId]`
    ///  for a NFT.
    ///  `properties[0]` is user-defined content. The owner of NFT can define value of `properties[0]`.
    ///  `properties[0]` does not reset when the NFT is transferred form one owner to another.
    ///  The new owner can overwrite the value of `properties[0]`.
    /// @param _tokenId The ID of NFT for which the value of metadata chunk is queried.
    /// @param _propertyId The index of queried metadata chunk in `properties[]` array.
    /// @return Returns the value of properties corresponding to _propertyId index (in text format)
    ///  it is recommended to store metadata in JSON format using properties.
    ///  It is important that the value of this properties[_propertyId] is a chunk of metadata
    ///  which is only specific for this unique NFT.
    function getTokenProperty(uint256 _tokenId, uint256 _propertyId) external view returns (string memory);

    /// @notice Returns NFT metadata that is defined by the owner of the NFT.
    /// @dev This function returns the value of `properties[0]` in reference implementation.
    ///  It is advised to use `properties[0]` for user-defined content.
    ///  In some cases an owner of NFT may have write access to multiple `properties` indexes
    ///  in this case the function MUST return the concatenated value of all user-defined strings
    ///  appended to each other without separators in index progression order
    ///  if it is possible within the scope of that NFT contract. "true" value of `_all` must be returned
    ///  if the function is capable of returning a full value of all user-defined content.
    /// "false" can be returned as `_all` return variable if it was not possible
    ///  to return all user-defined content. If "false" was returned as `_all` then
    ///  only value of `properties[0]` must be returned by this function.
    /// @param _tokenId The ID of NFT for which the value of metadata chunk is queried.
    /// @return _content Text value of the metadata that an owner of the queried NFT assigned to it.
    /// @return _all True if the function returns all metadata assigned by the owner of the NFT.
    ///  False if it is not possible to return all the user-defined metadata and only value of
    ///  `properties[0]` was returned.
    function getUserContent(uint256 _tokenId) external view returns (string memory _content, bool _all);

    /// @notice Assigns text metadata to a NFT.
    /// @dev Only an owner of the NFT can write data to that NFT.
    /// @param _tokenId The ID of NFT for which the value of metadata chunk is assigned.
    /// @param _content Text value that will be assigned to the specified NFT.
    /// @return Returns true if metadata assignment was successful.
    function setUserContent(uint256 _tokenId, string calldata _content) external returns (bool);

    /// @notice Creates an offer for a token. Only native currency can be used by default ($ETH for Ethereum Chain)
    /// @dev Funds must be deposited alongside this function call.
    ///  The deposit remains in the contract and can be withdrawn by the depositor.
    ///  If the amount of `msg.value` is higher or equal to `priceOf(_tokenId)`
    ///  then the bidder automatically becomes an owner of token with `_tokenId`
    ///  and the amount of `msg.value` is transferred to the previous owner of `_tokenId`.
    ///  New bid MUST be higher than the previous one in order to be placed.
    /// @param _tokenId The ID of NFT for which the offer is created.
    /// @param _data Metadata of the bid. Can be used for on-chain documenting of transactions
    ///  or as `_data` parameter of the `transfer(...)` performed in case of successful NFT purchase.
    function setBid(uint256 _tokenId, bytes calldata _data) payable external; // bid amount is defined by msg.value

    /// @notice Specifies the price at which the owner of NFT would automatically sell it
    ///  to whoever offers these funds.
    /// @dev The token MUST be sold at the price of highest bid if `priceOf(NFT)`
    ///  and `bidOf(NFT)` are not equal.
    ///  Example: Alice places `bid` = 10 ETH for NFT,
    ///  owner of the NFT calls `setPrice` = 7 ETH
    ///  the NFT must be sold at a price of 10 ETH.
    ///  Price resets to 0 when the automated trade is executed within smart-contract.
    ///  Price resets to 0 when NFT is transferred to a new owner.
    ///  Price value 0 makes NFT not tradeable (within smart-contract)
    ///  meaning that whatever the bid is placed for it - the NFT will not be sold.
    /// @param _tokenId The ID of NFT for which the price is assigned.
    /// @param _amountInWEI Amount of WEI that a bidder must pay
    ///  in order to automatically acquire this NFT.
    function setPrice(uint256 _tokenId, uint256 _amountInWEI) external;

    /// @notice Depositor can withdraw the amount of Bid that he placed earlier.
    /// @dev By default there is no order book in reference implementation of this token standard.
    ///  Therefore if the highest bid is withdrawn then the value of `bidOf(NFT)` becomes zero.
    ///  If token implements order book then the value of next bid in the orderbook must become
    ///  the `bidOf(NFT`.
    /// @param _tokenId The ID of NFT for which the bid is withdrawn.
    function withdrawBid(uint256 _tokenId) external returns (bool);
}
```

A token designed to receive NFTs must implement the following handler function

```auto
interface INFTReceiver {
    /// @notice Handle the receipt of an NFT
    /// @dev The NFT smart contract calls this function on the recipient
    ///  after a `transfer`. This function MAY throw to revert and reject the
    ///  transfer. Permissive fallback function MAY handle this function call
    ///  on the recipients side. No return values will be provided in case of
    ///  fallback function execution.
    ///  Note: the contract address is always the message sender.
    /// @param _operator The address which called `transfer` function
    ///  _operator and _from are always the same address when the transfer
    ///  is performed by CallistoNFT contract.
    /// @param _from The address which previously owned the token
    /// @param _tokenId The NFT identifier which is being transferred
    /// @param _data Additional data with no specified format
    /// @return ERC721 requires return value of `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`
    ///  This standard does not require any return values. Successful execution of the `onERC721Received` function
    ///  must be considered a successful transfer handling unless the receiver `throw`s on their side.
    function onERC721Received(address _operator, address _from, uint256 _tokenId, bytes calldata _data) external returns(bytes4);
}
```

**Classified Extension**

Code: [CallistoNFT/Extensions/ClassifiedNFT.sol at main · Dexaran/CallistoNFT · GitHub](https://github.com/Dexaran/CallistoNFT/blob/main/Extensions/ClassifiedNFT.sol)

In some cases there can be groups of NFTs that have some of their properties shared and other properties specific to each unique token. Example: Collectibles with “rarity” where each rarity class can have its own metadata shared across all tokens with the same rarity

For optimization reasons it can be useful to store class-specific metadata only once and then assign a reference to the Class metadata for each NFT instead of writing the metadata to each separate unit.

```auto
interface IClassifiedNFT is INFT {
    function setClassForTokenID(uint256 _tokenID, uint256 _tokenClass) external;
    function addNewTokenClass() external;
    function addTokenClassProperties(uint256 _propertiesCount) external;
    function modifyClassProperty(uint256 _classID, uint256 _propertyID, string memory _content) external;
    function getClassProperty(uint256 _classID, uint256 _propertyID) external view returns (string memory);
    function addClassProperty(uint256 _classID) external;
    function getClassProperties(uint256 _classID) external view returns (string[] memory);
    function getClassForTokenID(uint256 _tokenID) external view returns (uint256);
    function getClassPropertiesForTokenID(uint256 _tokenID) external view returns (string[] memory);
    function getClassPropertyForTokenID(uint256 _tokenID, uint256 _propertyID) external view returns (string memory);
    function mintWithClass(address _to, uint256 _tokenId, uint256 _classId)  external;
    function appendClassProperty(uint256 _classID, uint256 _propertyID, string memory _content) external;
}
```

Classified Extension can also change the way of token deployment. Instead of deploying a new token contract for each new NFT it is possible to deploy the token contract just once and then allow NFT creators to add new “classes” to this one token contract. Each new class in the contract may represent a class of collectibles with its own metadata defined by the class creator without a need to push a new token contract to the chain.

In most cases token contracts have little to no differences from each other which means that the chain could be optimized by making tokens a “state” of one contract instead of multiple instances of one contract.

**Rationale**

As the industry develops, new problems become more apparent and new demands arise.

With wider popularisation of NFTs it became obvious that uniqueness of each certain token makes it possible to distinguish one from another off-chain and therefore users may want to express interest in one particular token that they can find with a wide variety of ways using token explorers, blockchain browsers or other custom software.

It is not possible to express a desire to BUY a NFT a user is interested in unless the NFT is placed to a marketplace or the user knows the owner of the NFT.

It is not possible to express the desire to SELL a NFT that the user owns unless it is placed to a marketplace.

If a NFT is placed to the marketplace then it may not be placed to another at the same time without external risks.

Token uniqueness allows for attaching specific “price” to each particular unit.

Sometimes it is important to have some data recorded to a token in a trustless way directly through the contract.

It is also possible to give users the ability to record their own data to their owner NFTs which opens up multiple opportunities such as user authorisation based on NFT ownership. With this feature it is possible for a user to define some “secret” and record it to an owned NFT opening up the opportunity for “membership NFTs” implementations.

This standard extends the uniqueness of NFTs by adding the functionality on top of that.

**Backwards Compatibility**

ERC721 is the most widely used NFT standard. CallistoNFT uses the same communication model as ERC721 and onERC721Received(…) function for transfers handling.

Standards do not interfere and a token can support both at the same time.

**Reference implementation**



      [github.com](https://github.com/Dexaran/CallistoNFT/blob/main/CallistoNFT.sol)





####



```sol
// SPDX-License-Identifier: GPL

pragma solidity ^0.8.16;

library Address {
    /**
     * @dev Returns true if `account` is a contract.
     *
     * This test is non-exhaustive, and there may be false-negatives: during the
     * execution of a contract's constructor, its address will be reported as
     * not containing a contract.
     *
     * > It is unsafe to assume that an address for which this function returns
     * false is an externally-owned account (EOA) and not a contract.
     */
    function isContract(address account) internal view returns (bool) {
        // This method relies in extcodesize, which returns 0 for contracts in
        // construction, since the code is only stored at the end of the
        // constructor execution.

```

  This file has been truncated. [show original](https://github.com/Dexaran/CallistoNFT/blob/main/CallistoNFT.sol)










**Copyright**

Copyright and related rights waived via CC0

## Replies

**anett** (2022-02-25):

Hi Dexaran,

Thanks for sharing new idea on improvement of ERC-721. I like the security component in your ERC. On behalf of NFT Standards Working Group, [@Amxx](/u/amxx) tried to solve security issue with Permit singleton proposal. You may want to check it out

Find details here:

[Permit Singleton Wiki link](https://www.nftstandards.wtf/Working+Group+EIPs+and+implementations/Permit+Singleton)

[Full repo and implementation](https://github.com/Amxx/Permit)

