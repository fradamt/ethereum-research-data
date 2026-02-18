---
source: magicians
topic_id: 11167
title: EIP-7943 On-Chain IP Ownership
author: 0xSimon
date: "2022-10-03"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-7943-on-chain-ip-ownership/11167
views: 554
likes: 0
posts_count: 2
---

# EIP-7943 On-Chain IP Ownership

EIP-7943

ERC721-Linked-Intellectual Property Rights

By [@0xSimon](/u/0xsimon)_

**Pre-Read:**

I’m proposing that we publish IP-Rights related to ERC721 assets on-chain. This information can exist on an interface, or on a separate contract referred to as the “Master” contract. The master will be upgradable according to the Diamond Proxy pattern to accommodate for ever-growing needs and specified details. This is still a work in progress, there are many optimizations that can be made on the coding,logic, and legal levels. If this subject particularly interests you as a developer or lawyer, please feel free to reach out at [simon@sleepyslothsociety.io](mailto:simon@sleepyslothsociety.io) !

Thanks for taking the time to read this.

**Part 1. The Interface**

**Abstract**

This standard is an extension of ERC-721. It proposes an additional interface to query information regarding NFTs’ intellectual property ownership and brand copyright information. This interface includes functions to query whether a specific address holds full monetization and intellectual property rights of a specific tokenID, whether a collection is CC0, whether the company logo is free for public use, and a url string that contains any extra information.

**Motivation:**

Intellectual Property has become an essential part of the NFT and Ethereum Community. It has played an essential role in the ERC721 Ecosystem, yet there are no on-chain methods to gather the information related to IP Ownership. Consumers and decentralized platforms are forced to spend time to find accurate and precise information about a company’s position on intellectual property ownership.

There are three main target groups that would benefit from this added functionality.

**The Founders / Company of An ERC721 Collection**

They would be able to create an on-chain record of how their brand wishes to handle IP ownership and brand identity

This can help protect the brand later down the line and can help the brand set standards in regards to who is allowed to monetize from the assets

They can reassure their community that commercial rights will be defined via smart contract.

Historic data can be queried by block in case of dispute

**Consumers**

Holders of ERC721’s could use more transparency regarding their relationship with the intellectual property and how that will be managed over time.

Consumers can be often-times blind-sided by changing IP Ownership standards. This proposal would not explicitly remove that volatility, but at least holders of a collection can understand the environment in which they are operating.

**Decentralized Protocols/ Third Party Companies**

Good actors should be able to query on-chain information in regards to an ERC721’s collection  to ensure that neither the platform, nor the digital asset owner, is infringing upon copyrighted or reserved material as defined by the parent company

For example, there may be a game that allows users to capitalize off their digital assets indirectly via creation of some derivative asset. In this scenario, it would be beneficial for all to know whether a user (owner or authorized user) has the right to monetize said asset.

**Specification**

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

The technical specification should describe the syntax and semantics of any new feature. The specification should be detailed enough to allow competing, interoperable implementations for any of the current Ethereum platforms (go-ethereum, parity, cpp-ethereum, ethereumj, ethereumjs, and others 2).

```auto
/// SPDX-License-Identifier: CC0-1.0
pragma solidity ^0.8.0;
import "./interfaces/IERC7943.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
/// @author 0xSimon_
contract ERC7943  is IERC7943,ERC721{
    TrademarkInformation private trademarkInformation = TrademarkInformation({
        isCC0:Status.TRUE,
        isLogoPublicDomain:Status.TRUE,
        trademarkDocumentLink:"https://project-xyz.io/trademarkDocuments"
    });
    constructor(string memory name, string memory symbol)
    ERC721(name,symbol)
    {}
    function hasFullIPRights(address holder, uint tokenId) external view virtual override returns(bool){
        return  holder == ownerOf(tokenId);
    }
    function getTrademarkInformation() external view  virtual override returns(TrademarkInformation memory) {
        return trademarkInformation;
    }
    function updateTrademarkInformation(TrademarkInformation memory newTrademarkInformation) external virtual override {
        trademarkInformation = newTrademarkInformation;
        emit UpdatedPolicy(block.timestamp,newTrademarkInformation);

    }

    function supportsInterface(bytes4 interfaceId) public view virtual override returns(bool) {
        return interfaceId == type(IERC7943).interfaceId || super.supportsInterface(interfaceId);
    }

}
```

The hasFullIPRights(address holder,uint256 tokenId) function MAY be implemented as pure or view.

The getTrademarkInformation() function MAY be implemented as pure or view.

The updateTrademarkInformation() function MAY be implemented as external or public

The UpdatedPolicy(uint indexed timestamp, TrademarkInformation) event must be emitted when the TrademarkPolicy is modified.

The supportsInterface method MUST return true when called with 0xadbfd142

**Rationale**

This standard aims to create a standard regarding IP ownership in ERC721 Collections.

Easy Integration

Because this standard is fully EIP-721 compliant, existing protocols will be able to facilitate IP Ownership information regarding NFTs out of the box. With only a few functions to add, protocols will be able to define how they wish to handle the ownership of intellectual property and help promote transparency across the NFT ecosystem.

**Backwards Compatibility**

This standard can be fully EIP-721 compatible by adding an extension function set.

The new functions introduced in this standard add minimal overhead to the existing EIP-721 interface, which should make adoption straightforward and quick for developers.

**Part 2: Aggregator / Master Contract**

I also propose to have a master contract in which ownable ERC721 collections’ owners can modify their TrademarkInformation struct and input an address that can handle these on-chain queries in-stead of the actual contract. Motivation for this could be to reduce byte-code upon deployment, or maybe because a collection has already launched and does not have the means to add this functionality.

I propose to make the Master Contract use the Diamond Proxy Standard as coined in EIP-2535.

```auto
// SPDX-License-Identifier: Unlicensed
pragma solidity 0.8.17;

/// @author 0xSimon_
import "@solidstate/contracts/proxy/diamond/SolidStateDiamond.sol";


contract IPManagementDiamond is SolidStateDiamond {

}
```

We then create an AppStorage facet that contains two mappings. One for trademarkInformation and one for the trademarkDocumentLink. The variables inside this TrademarkInformation struct are almost identical as the ones in the original interface, with the addition of a delegateContract variable (which we will talk about soon) and the omission of `string trademarkDocumentLink` (moved to a separate mapping). Over time, since the structs are stored in a mapping, it will be possible to add more variables, and hence adjust for the ever-changing regulations that surround the intersection of the blockchain and IP space.

**App Storage Structure**

```auto
struct AppStorage {
    mapping(address => TrademarkInformation) trademarkInformation;
    mapping(address => string) trademarkDocumentLink;
}

TrademarkInformation Struct
// SPDX-License-Identifier: MIT
pragma solidity 0.8.17;
enum Status {
    NOT_SET,
    FALSE,
    TRUE
}
struct TrademarkInformation {
    Status isCC0;
    Status isLogoPublicDomain;
    address delegateContract;
}
```

**Delegate Contract Role:**

As per the original IERC, you’ll notice that there’s a

`function hasFullIPRights(address holder, uint tokenId) external view returns(bool)`

If a contract has already been deployed, it will be impossible to add this function unless the contract is built on some sort of proxy. Hence, existing collections can specify a contract that will fulfill this function. Here’s the proposed implementation in the internal Solidity Library, and external facet.

**Step 1: Set The Delegate Contract**

```auto
    function setDelegateContract(address contractAddress, address delegateContract)internal {
        AppStorage storage s = appStorage();
        if(!MinimalOwnableIERC721(contractAddress).supportsInterface(IERC721_INTERFACE_ID)) revert DoesNotSupportIERC721();
        if(msg.sender != MinimalOwnableIERC721(contractAddress).owner()) revert NotERC721Owner();
        if(!MinimalIERC7943(delegateContract).supportsInterface(IERC7943_INTERFACE_ID)) revert  DoesNotSupportIERC7943();
        s.trademarkInformation[contractAddress].delegateContract = delegateContract;
        }
```

**Step 1 Pseudo-Code:**

Check if the contractAddress supports IERC721 interface.

Check to make sure that the msg.sender is the owner of that contract.

Check that the delegateContract supports IERC7943

Set the delegateContract.

**Step 2: Query**

```auto
           function hasFullIPRights(address tokenContract,address holder,uint tokenId) internal view returns(bool) {
        AppStorage storage s = appStorage();
        //If tokenContract Supports The Interface
        if(!MinimalOwnableIERC721(tokenContract).supportsInterface(IERC721_INTERFACE_ID)) revert DoesNotSupportIERC721();
        if(MinimalOwnableIERC721(tokenContract).supportsInterface(IERC7943_INTERFACE_ID)) {
            return MinimalIERC7943(tokenContract).hasFullIPRights(holder,tokenId);
        }
        address delegateContract = s.trademarkInformation[tokenContract].delegateContract;
        if(delegateContract == address(0)) revert ZeroContract();
        return MinimalIERC7943(delegateContract).hasFullIPRights(holder,tokenId);
    }
```

**Pseudo-Code For Part 2:**

Function takes in a tokenContract (The Deployed ERC721) a holder address, and a tokenID.

If the tokenContract supports IERC7943 and IERC721, query the hasFullPRights as outlined in Part 1.

Else, check the delegateContractAddress.

If It’s not set, revert

If it is set, return the hasFullIPRights call from that contract.

Please let me know your thoughts and you can find the github Repo here:

https://github.com/simonbindefeld/eip-7943

## Replies

**abcoathup** (2022-10-04):

EIP editors assign EIP numbers and it is generally the PR number in [Pull requests · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pulls), at this stage it is likely to start with a 5, e.g. EIP-5###

> EIP-1: EIP Purpose and Guidelines
> Assign an EIP number (generally the PR number, but the decision is with the editors)

