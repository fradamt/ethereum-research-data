---
source: magicians
topic_id: 10310
title: "EIP-5521: ERC-721 Referable NFT"
author: OniReimu
date: "2022-08-10"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5521-erc-721-referable-nft/10310
views: 5254
likes: 10
posts_count: 32
---

# EIP-5521: ERC-721 Referable NFT

---

## eip: 5521
title: Referable NFT
description: An ERC-721 extension to construct reference relationships among NFTs
author: Saber Yu (), Qin Wang , Shange Fu , Yilin Sai , Shiping Chen , Sherry Xu , Jiangshan Yu
discussions-to:
status: Review
type: Standards Track
category: ERC
created: 2022-08-10
requires: 165, 721

## Abstract

This standard is an extension of ERC-721. It proposes two referable indicators, referring and referred, and a time-based indicator `createdTimestamp`. The relationship between each NFT forms a directed acyclic graph (DAG). The standard allows users to query, track and analyze their relationships.

[![system-arch](https://ethereum-magicians.org/uploads/default/optimized/2X/d/daebc700a8febe3c983d31de0caa333e82cabc3e_2_690x223.png)system-arch2678×867 182 KB](https://ethereum-magicians.org/uploads/default/daebc700a8febe3c983d31de0caa333e82cabc3e)

## Motivation

Many scenarios require inheritance, reference, and extension of NFTs. For instance, an artist may develop his NFT work based on a previous NFT, or a DJ may remix his record by referring to two pop songs, etc. Proposing a referable solution for existing NFTs and enabling efficient queries on cross-references make much sense.

By adding the `referring` indicator, users can mint new NFTs (e.g., C, D, E) by referring to existing NFTs (e.g., A, B), while `referred` enables the referred NFTs (A, B) to be aware that who has quoted it (e.g., A ← D; C ← E; B ← E, and A ← E). The `createdTimestamp` is an indicator used to show the creation time of NFTs (A, B, C, D, E).

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

- Relationship: a structure that contains referring, referred, referringKeys, referredKeys, createdTimestamp, and other customized and OPTIONAL attributes (i.e., not necessarily included in the standard) such as privityOfAgreement recording the ownerships of referred NFTs at the time the rNFTs were being created or profitSharing recording the profit sharing of referring.
- referring: an out-degree indicator, used to show the users this NFT refers to;
- referred: an in-degree indicator, used to show the users who have refereed this NFT;
- referringKeys: a helper for mapping conversion of out-degree indicators, used for events;
- referredKeys: a helper for mapping conversion of in-degree indicators, used for events;
- createdTimestamp: a time-based indicator, used to compare the timestamp of mint, which MUST NOT be editable anyhow by callers;
- safeMint: mint a new rNFT;
- setNode: set the referring list of an rNFT and update the referred list of each one in the referring list;

setNodeReferring: set the referring list of an rNFT;
- setNodeReferred: set the referred list of the given rNFTs sourced from different contracts;

setNodeReferredExternal: set the referred list of the given rNFTs sourced from external contracts;

`referringOf`: get the referring list of an rNFT;
`referredOf`: get the referred list of an rNFT.

Implementers of this standard **MUST** have all of the following functions:

```solidity
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/utils/introspection/IERC165.sol";

interface IERC_5521 is IERC165 {

    /// Logged when a node in the rNFT gets referred and changed.
    /// @notice Emitted when the `node` (i.e., an rNFT) is changed.
    event UpdateNode(uint256 indexed tokenId,
                     address indexed owner,
                     address[] _address_referringList,
                     uint256[][] _tokenIds_referringList,
                     address[] _address_referredList,
                     uint256[][] _tokenIds_referredList
    );

    /// @notice set the referred list of an rNFT associated with different contract addresses and update the referring list of each one in the referred list. Checking the duplication of `addresses` and `tokenIds` is **RECOMMENDED**.
    /// @param `tokenId` of rNFT being set. `addresses` of the contracts in which rNFTs with `tokenIds` being referred accordingly.
    /// @requirement
    /// - the size of `addresses` **MUST** be the same as that of `tokenIds`;
    /// - once the size of `tokenIds` is non-zero, the inner size **MUST** also be non-zero;
    /// - the `tokenId` **MUST** be unique within the same contract;
    /// - the `tokenId` **MUST NOT** be the same as `tokenIds[i][j]` if `addresses[i]` is essentailly `address(this)`.
    function setNode(uint256 tokenId, address[] memory addresses, uint256[][] memory tokenIds) external;

    /// @notice get the referring list of an rNFT.
    /// @param `tokenId` of the rNFT being focused, `_address` of contract address associated with the focused rNFT.
    /// @return the referring mapping of the rNFT.
    function referringOf(address _address, uint256 tokenId) external view returns(address[] memory, uint256[][] memory);

    /// @notice get the referred list of an rNFT.
    /// @param `tokenId` of the rNFT being focused, `_address` of contract address associated with the focused rNFT.
    /// @return the referred mapping of the rNFT.
    function referredOf(address _address, uint256 tokenId) external view returns(address[] memory, uint256[][] memory);

    /// @notice check supported interfaces, adhereing to ERC165.
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}

interface TargetContract is IERC165 {
    /// @notice set the referred list of an rNFT associated with external contract addresses.
    /// @param `_tokenIds` of rNFTs associated with the contract address `_address` being referred by the rNFT with `tokenId`.
    /// @requirement
    /// - `_address` **MUST NOT** be the same as `address(this)` where `this` is executed by an external contract where `TargetContract` interface is implemented.
    function setNodeReferredExternal(address _address, uint256 tokenId, uint256[] memory _tokenIds) external;

    function referringOf(address _address, uint256 tokenId) external view returns(address[] memory, uint256[][] memory);

    function referredOf(address _address, uint256 tokenId) external view returns(address[] memory, uint256[][] memory);

    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}

```

## Rationale

This standard is intended to establish the referable DAG for queries on cross-relationship and accordingly provide the simplest functions. It provides advantages as follows.

*Clear ownership inheritance*: This standard extends the static NFT into a virtually extensible NFT network. Artists do not have to create work isolated from others. The ownership inheritance avoids reinventing the same wheel.

*Incentive Compatibility*: This standard clarifies the referable relationship across different NFTs, helping to integrate multiple up-layer incentive models for both original NFT owners and new creators.

*Easy Integration*: This standard makes it easier for the existing token standards or third-party protocols. For instance, the rNFT can be applied to rentable scenarios (cf. ERC-5006 to build a hierarchical rental market, where multiple users can rent the same NFT during the same time or one user can rent multiple NFTs during the same duration).

*Scalable Interoperability* From March 26th 2023, this standard has been stepping forward by enabling cross-contract references, giving a scalable adoption for the broader public with stronger interoperability.

## Backwards Compatibility

This standard can be fully ERC-721 compatible by adding an extension function set.

## Test Cases

```javascript
// Right click on the script name and hit "Run" to execute
const { expect } = require("chai");
const { ethers } = require("hardhat");

const TOKEN_NAME = "ERC_5521_NAME";
const TOKEN_SYMBOL = "ERC_5521_SYMBOL";
const TOKEN_NAME1 = "ERC_5521_NAME1";
const TOKEN_SYMBOL1 = "ERC_5521_SYMBOL1";
const TOKEN_NAME2 = "ERC_5521_NAME2";
const TOKEN_SYMBOL2 = "ERC_5521_SYMBOL2";

function tokenIds2Number(tokenIds) {
    return tokenIds.map(tIds => tIds.map(tId => tId.toNumber()));
}

function assertRelationship(rel, tokenAddresses, tokenIds) {
    expect(rel[0]).to.deep.equal(tokenAddresses);
    expect(tokenIds2Number(rel[1])).to.deep.equal(tokenIds);
}

describe("ERC_5521 - single token contract scenario", function () {
    let tokenContract1;

    beforeEach(async () => {
        const RNFT = await ethers.getContractFactory("ERC_5521");
        const rNFT = await RNFT.deploy(TOKEN_NAME,TOKEN_SYMBOL);
        await rNFT.deployed();
        console.log('ERC_5521 deployed at:'+ rNFT.address);
        tokenContract1 = rNFT;
    });

    it("should report correct token name and symbol", async function () {
        expect((await tokenContract1.symbol())).to.equal(TOKEN_SYMBOL);
        expect((await tokenContract1.name())).to.equal(TOKEN_NAME);
    });

    it("can mint a token with empty referredOf and referringOf", async function () {
        await tokenContract1.safeMint(1, [], []);
        assertRelationship(await tokenContract1.referredOf(tokenContract1.address, 1), [], []);
        assertRelationship(await tokenContract1.referringOf(tokenContract1.address, 1), [], []);
    })

    it("cannot query relationships of a non-existent token", async function () {
        const mintToken1Tx = await tokenContract1.safeMint(1, [], []);
        // mint tx of token 1 must be mined before it can be referred to
        await mintToken1Tx.wait();
        // wait 1 sec to ensure that token 2 is minted at a later block timestamp (block timestamp is in second)
        await new Promise(r => setTimeout(r, 1000));
        await tokenContract1.safeMint(2, [tokenContract1.address], [[1]]);

        // tokenContract1 didn't mint any token with id 3
        await expect(tokenContract1.referringOf(tokenContract1.address, 3)).to.be.revertedWith("token ID not existed");
        await expect(tokenContract1.referredOf(tokenContract1.address, 3)).to.be.revertedWith("token ID not existed");
    })

    it("must not mint two tokens with the same token id", async function () {
        await tokenContract1.safeMint(1, [], []);
        await expect(tokenContract1.safeMint(1, [], [])).to.be.revertedWith("ERC721: token already minted");
    })

    it("can mint a token referring to another minted token", async function () {
        const mintToken1Tx = await tokenContract1.safeMint(1, [], []);
        // mint tx of token 1 must be mined before it can be referred to
        await mintToken1Tx.wait();
        // wait 1 sec to ensure that token 2 is minted at a later block timestamp (block timestamp is in second)
        await new Promise(r => setTimeout(r, 1000));
        await tokenContract1.safeMint(2, [tokenContract1.address], [[1]]);

        const referringOfT2 = await tokenContract1.referringOf(tokenContract1.address, 2)
        assertRelationship(referringOfT2, [tokenContract1.address], [[1]]);

        const referredOfT2 = await tokenContract1.referredOf(tokenContract1.address, 2)
        assertRelationship(referredOfT2, [], []);

        const referringOfT1 = await tokenContract1.referringOf(tokenContract1.address, 1)
        assertRelationship(referringOfT1, [], []);

        const referredOfT1 = await tokenContract1.referredOf(tokenContract1.address, 1)
        assertRelationship(referredOfT1, [tokenContract1.address], [[2]]);
    })

    it("cannot mint a token referring to a token that is not yet minted", async function () {
        await expect(tokenContract1.safeMint(2, [tokenContract1.address], [[1]])).to.be.revertedWith("invalid token ID");
    })

    it("can mint 3 tokens forming a simple DAG", async function () {
        const mintToken1Tx = await tokenContract1.safeMint(1, [], []);
        // mint tx of token 1 must be mined before it can be referred to
        await mintToken1Tx.wait();
        // wait 1 sec to ensure that token 2 is minted at a later block timestamp (block timestamp is in second)
        await new Promise(r => setTimeout(r, 1000));
        const mintToken2Tx = await tokenContract1.safeMint(2, [tokenContract1.address], [[1]]);
        await mintToken2Tx.wait();
        await new Promise(r => setTimeout(r, 1000));
        const mintToken3Tx = await tokenContract1.safeMint(3, [tokenContract1.address], [[1, 2]]);
        await mintToken3Tx.wait();

        const referringOfT2 = await tokenContract1.referringOf(tokenContract1.address, 2)
        assertRelationship(referringOfT2, [tokenContract1.address], [[1]]);

        const referredOfT2 = await tokenContract1.referredOf(tokenContract1.address, 2)
        assertRelationship(referredOfT2, [tokenContract1.address], [[3]]);

        const referringOfT1 = await tokenContract1.referringOf(tokenContract1.address, 1)
        assertRelationship(referringOfT1, [], []);

        const referredOfT1 = await tokenContract1.referredOf(tokenContract1.address, 1)
        assertRelationship(referredOfT1, [tokenContract1.address], [[2, 3]]);

        const referringOfT3 = await tokenContract1.referringOf(tokenContract1.address, 3)
        assertRelationship(referringOfT3, [tokenContract1.address], [[1, 2]]);

        const referredOfT3 = await tokenContract1.referredOf(tokenContract1.address, 3)
        assertRelationship(referredOfT3, [], []);
    })

    it("should revert when trying to create a cycle in the relationship DAG", async function () {
        const mintToken1Tx = await tokenContract1.safeMint(1, [], []);
        // mint tx of token 1 must be mined before it can be referred to
        await mintToken1Tx.wait();
        // wait 1 sec to ensure that token 2 is minted at a later block timestamp (block timestamp is in second)
        await new Promise(r => setTimeout(r, 1000));
        await tokenContract1.safeMint(2, [tokenContract1.address], [[1]]);
        await expect(tokenContract1.safeMint(1, [tokenContract1.address], [[2]])).to.be.reverted;
    })

    it("should revert when attempting to create an invalid relationship", async function () {
        const mintToken1Tx = await tokenContract1.safeMint(1, [], []);
        // mint tx of token 1 must be mined before it can be referred to
        await mintToken1Tx.wait();
        // wait 1 sec to ensure that token 2 is minted at a later block timestamp (block timestamp is in second)
        await new Promise(r => setTimeout(r, 1000));
        // Intentionally creating an invalid relationship
        await expect(tokenContract1.safeMint(2, [tokenContract1.address], [[1, 2, 3]])).to.be.revertedWith("ERC_5521: self-reference not allowed");
        await expect(tokenContract1.safeMint(2, [tokenContract1.address], [[1, 3]])).to.be.revertedWith("invalid token ID");
        await expect(tokenContract1.safeMint(2, [tokenContract1.address], [])).to.be.revertedWith("Addresses and TokenID arrays must have the same length");
        await expect(tokenContract1.safeMint(2, [tokenContract1.address], [[]])).to.be.revertedWith("the referring list cannot be empty");
    });
});

describe("ERC_5521 - multi token contracts scenario", function () {
    let tokenContract1;
    let tokenContract2;

    beforeEach(async () => {
        const RNFT = await ethers.getContractFactory("ERC_5521");

        const rNFT1 = await RNFT.deploy(TOKEN_NAME1,TOKEN_SYMBOL1);
        await rNFT1.deployed();
        console.log('ERC_5521 deployed at:'+ rNFT1.address);
        tokenContract1 = rNFT1;

        const rNFT2 = await RNFT.deploy(TOKEN_NAME2,TOKEN_SYMBOL2);
        await rNFT2.deployed();
        console.log('ERC_5521 deployed at:'+ rNFT2.address);
        tokenContract2 = rNFT2;
    });

    it("should revert when referring and referred lists have mismatched lengths", async function () {
        await expect(tokenContract1.safeMint(1, [tokenContract1.address], [[1], [2]])).to.be.reverted;
    });

    it("can mint a token referring to another minted token", async function () {
        const mintToken1Tx = await tokenContract1.safeMint(1, [], []);
        // mint tx of token 1 must be mined before it can be referred to
        await mintToken1Tx.wait();
        // wait 1 sec to ensure that token 2 is minted at a later block timestamp (block timestamp is in second)
        await new Promise(r => setTimeout(r, 1000));
        await tokenContract2.safeMint(2, [tokenContract1.address], [[1]]);

        // relationships of token 2 can be queried using any ERC5521 contract, not necessarily the contract that minted token 2
        const referringOfT2QueriedByC1 = await tokenContract1.referringOf(tokenContract2.address, 2)
        const referringOfT2QueriedByByC2 = await tokenContract2.referringOf(tokenContract2.address, 2)
        assertRelationship(referringOfT2QueriedByC1, [tokenContract1.address], [[1]]);
        assertRelationship(referringOfT2QueriedByByC2, [tokenContract1.address], [[1]]);

        const referredOfT2QueriedByC1 = await tokenContract1.referredOf(tokenContract2.address, 2)
        const referredOfT2QueriedByC2 = await tokenContract2.referredOf(tokenContract2.address, 2)
        assertRelationship(referredOfT2QueriedByC1, [], []);
        assertRelationship(referredOfT2QueriedByC2, [], []);

        const referringOfT1QueriedByC1 = await tokenContract1.referringOf(tokenContract1.address, 1)
        const referringOfT1QueriedByC2 = await tokenContract2.referringOf(tokenContract1.address, 1)
        assertRelationship(referringOfT1QueriedByC1, [], []);
        assertRelationship(referringOfT1QueriedByC2, [], []);

        const referredOfT1QueriedByC1 = await tokenContract1.referredOf(tokenContract1.address, 1)
        const referredOfT1QueriedByC2 = await tokenContract2.referredOf(tokenContract1.address, 1)
        assertRelationship(referredOfT1QueriedByC1, [tokenContract2.address], [[2]]);
        assertRelationship(referredOfT1QueriedByC2, [tokenContract2.address], [[2]]);
    })

    it("cannot query relationships of a non-existent token", async function () {
        const mintToken1Tx = await tokenContract1.safeMint(1, [], []);
        // mint tx of token 1 must be mined before it can be referred to
        await mintToken1Tx.wait();
        // wait 1 sec to ensure that token 2 is minted at a later block timestamp (block timestamp is in second)
        await new Promise(r => setTimeout(r, 1000));
        await tokenContract2.safeMint(2, [tokenContract1.address], [[1]]);

        // tokenContract1 didn't mint any token with id 2
        await expect(tokenContract1.referringOf(tokenContract1.address, 2)).to.be.revertedWith("token ID not existed");
        await expect(tokenContract1.referredOf(tokenContract1.address, 2)).to.be.revertedWith("token ID not existed");
    })

    it("cannot mint a token referring to a token that is not yet minted", async function () {
        await expect(tokenContract2.safeMint(2, [tokenContract1.address], [[1]])).to.be.revertedWith("invalid token ID");
    })

    it("can mint 3 tokens forming a simple DAG", async function () {
        const mintToken1Tx = await tokenContract1.safeMint(1, [], []);
        // mint tx of token 1 must be mined before it can be referred to
        await mintToken1Tx.wait();
        // wait 1 sec to ensure that token 2 is minted at a later block timestamp (block timestamp is in second)
        await new Promise(r => setTimeout(r, 1000));
        const mintToken2Tx = await tokenContract2.safeMint(2, [tokenContract1.address], [[1]]);
        await mintToken2Tx.wait();
        await new Promise(r => setTimeout(r, 1000));
        const mintToken3Tx = await tokenContract2.safeMint(3, [tokenContract1.address, tokenContract2.address], [[1], [2]]);
        await mintToken3Tx.wait();

        const referringOfT2 = await tokenContract1.referringOf(tokenContract2.address, 2)
        assertRelationship(referringOfT2, [tokenContract1.address], [[1]]);

        const referredOfT2 = await tokenContract1.referredOf(tokenContract2.address, 2)
        assertRelationship(referredOfT2, [tokenContract2.address], [[3]]);

        const referringOfT1 = await tokenContract1.referringOf(tokenContract1.address, 1)
        assertRelationship(referringOfT1, [], []);

        const referredOfT1 = await tokenContract1.referredOf(tokenContract1.address, 1)
        assertRelationship(referredOfT1, [tokenContract2.address], [[2, 3]]);

        const referringOfT3 = await tokenContract1.referringOf(tokenContract2.address, 3)
        assertRelationship(referringOfT3, [tokenContract1.address, tokenContract2.address], [[1], [2]]);

        const referringOfT3fromContract2 = await tokenContract2.referringOf(tokenContract2.address, 3)
        assertRelationship(referringOfT3fromContract2, [tokenContract1.address, tokenContract2.address], [[1], [2]]);

        const referredOfT3 = await tokenContract1.referredOf(tokenContract2.address, 3)
        assertRelationship(referredOfT3, [], []);
    })

});
```

## Reference Implementation

```solidity
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./IERC_5521.sol";

contract ERC_5521 is ERC721, IERC_5521, TargetContract {

    struct Relationship {
        mapping (address => uint256[]) referring;
        mapping (address => uint256[]) referred;
        address[] referringKeys;
        address[] referredKeys;
        uint256 createdTimestamp; // unix timestamp when the rNFT is being created

        // extensible parameters
        // ...
    }

    mapping (uint256 => Relationship) internal _relationship;
    address contractOwner = address(0);

    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {
        contractOwner = msg.sender;
    }

    function safeMint(uint256 tokenId, address[] memory addresses, uint256[][] memory _tokenIds) public {
        // require(msg.sender == contractOwner, "ERC_rNFT: Only contract owner can mint");
        _safeMint(msg.sender, tokenId);
        setNode(tokenId, addresses, _tokenIds);
    }

    /// @notice set the referred list of an rNFT associated with different contract addresses and update the referring list of each one in the referred list
    /// @param tokenIds array of rNFTs, recommended to check duplication at the caller's end
    function setNode(uint256 tokenId, address[] memory addresses, uint256[][] memory tokenIds) public virtual override {
        require(
            addresses.length == tokenIds.length,
            "Addresses and TokenID arrays must have the same length"
        );
        for (uint i = 0; i = block.timestamp) { revert("ERC_5521: the referred rNFT needs to be a predecessor"); } // Make sure the reference complies with the timing sequence

                    relationship.referred[address(this)].push(tokenId);
                    emitEvents(_tokenIds[i][j], ownerOf(_tokenIds[i][j]));
                }
            } else {
                TargetContract targetContractInstance = TargetContract(addresses[i]);
                bool isSupports = targetContractInstance.supportsInterface(type(TargetContract).interfaceId);
                if (isSupports) {
                    // The target contract supports the interface, safe to call functions of the interface.
                    targetContractInstance.setNodeReferredExternal(address(this), tokenId, _tokenIds[i]);
                }
            }
        }
    }

    /// @notice set the referred list of an rNFT associated with different contract addresses
    /// @param _tokenIds array of rNFTs associated with addresses, recommended to check duplication at the caller's end
    function setNodeReferredExternal(address _address, uint256 tokenId, uint256[] memory _tokenIds) external {
        for (uint i = 0; i = block.timestamp) { revert("ERC_5521: the referred rNFT needs to be a predecessor"); } // Make sure the reference complies with the timing sequence

            relationship.referred[_address].push(tokenId);
            emitEvents(_tokenIds[i], ownerOf(_tokenIds[i]));
        }
    }

    /// @notice Get the referring list of an rNFT
    /// @param tokenId The considered rNFT, _address The corresponding contract address
    /// @return The referring mapping of an rNFT
    function referringOf(address _address, uint256 tokenId) external view virtual override(IERC_5521, TargetContract) returns (address[] memory, uint256[][] memory) {
        address[] memory _referringKeys;
        uint256[][] memory _referringValues;

        if (_address == address(this)) {
            require(_exists(tokenId), "ERC_5521: token ID not existed");
            (_referringKeys, _referringValues) = convertMap(tokenId, true);
        } else {
            TargetContract targetContractInstance = TargetContract(_address);
            require(targetContractInstance.supportsInterface(type(TargetContract).interfaceId), "ERC_5521: target contract not supported");
            (_referringKeys, _referringValues) = targetContractInstance.referringOf(_address, tokenId);
        }
        return (_referringKeys, _referringValues);
    }

    /// @notice Get the referred list of an rNFT
    /// @param tokenId The considered rNFT, _address The corresponding contract address
    /// @return The referred mapping of an rNFT
    function referredOf(address _address, uint256 tokenId) external view virtual override(IERC_5521, TargetContract) returns (address[] memory, uint256[][] memory) {
        address[] memory _referredKeys;
        uint256[][] memory _referredValues;

        if (_address == address(this)) {
            require(_exists(tokenId), "ERC_5521: token ID not existed");
            (_referredKeys, _referredValues) = convertMap(tokenId, false);
        } else {
            TargetContract targetContractInstance = TargetContract(_address);
            require(targetContractInstance.supportsInterface(type(TargetContract).interfaceId), "ERC_5521: target contract not supported");
            (_referredKeys, _referredValues) = targetContractInstance.referredOf(_address, tokenId);
        }
        return (_referredKeys, _referredValues);
    }

    /// @dev See {IERC165-supportsInterface}.
    function supportsInterface(bytes4 interfaceId) public view virtual override (ERC721, IERC_5521, TargetContract) returns (bool) {
        return interfaceId == type(IERC_5521).interfaceId
            || interfaceId == type(TargetContract).interfaceId
            || super.supportsInterface(interfaceId);
    }

    // @notice Emit an event of UpdateNode
    function emitEvents(uint256 tokenId, address sender) private {
        (address[] memory _referringKeys, uint256[][] memory _referringValues) = convertMap(tokenId, true);
        (address[] memory _referredKeys, uint256[][] memory _referredValues) = convertMap(tokenId, false);

        emit UpdateNode(tokenId, sender, _referringKeys, _referringValues, _referredKeys, _referredValues);
    }

    // @notice Convert a specific `local` token mapping to a key array and a value array
    function convertMap(uint256 tokenId, bool isReferring) private view returns (address[] memory, uint256[][] memory) {
        Relationship storage relationship = _relationship[tokenId];

        address[] memory returnKeys;
        uint256[][] memory returnValues;

        if (isReferring) {
            returnKeys = relationship.referringKeys;
            returnValues = new uint256[][](returnKeys.length);
            for (uint i = 0; i CC0.

## Replies

**f123** (2022-08-12):

Looks good, I think the market needs a protocol like this to start the season.

---

**web3ycy** (2022-08-13):

Hi bro, inspiring thoughts and nice writing! What I am wondering is, in other applications, the usual case is that both block/tx location and unix timestamp are allowed, but in the security protocols normally only the block/tx location is used, are there any security issues that can be raised regarding this?

---

**OniReimu** (2022-08-15):

Hi, the timestamp is additional protection IMO, but yes, we welcome all discussion regarding the potential security issue with or without the UNIX timestamp.

---

**QA-AT** (2022-08-15):

If we do need a timestamp, what is the format? I see the code suggests using unix timestamp when the rNFT is being created. Is this the only format we want to support?

---

**web3ycy** (2022-08-15):

Thanks for the reply bro, may I ask why is a timestamp needed? ![:face_with_monocle:](https://ethereum-magicians.org/images/emoji/twitter/face_with_monocle.png?v=12)

---

**OniReimu** (2022-08-16):

Basic yes. Unix timeframe is a good tool tho.

---

**OniReimu** (2023-03-27):

A promising use case related to LLM such as ChatGPT is welcomed for discussion.

**Applying the EIP-5521 Standard to Decentralize the Development and Maintenance of Large Language Models (LLMs)**

The development and maintenance of Large Language Models (LLMs), such as ChatGPT, has been predominantly controlled by a few centralized entities, such as OpenAI and Microsoft. Despite being considered one of the most powerful and generic LLMs, ChatGPT is closed-source and lacks community-driven development. This use case explores the application of the EIP-5521 standard in the LLM area, specifically for promoting a decentralized, open-source LLM developed and maintained by the community. By leveraging the concept of referable NFTs and the spirit of the EIP-5521 standard, we aim to build a decentralized LLM that thrives in the Web3 world, with a more transparent and fair distribution of ownership and contribution.

*The current state of LLMs and their limitations* -  ChatGPT, a powerful LLM developed by OpenAI and Microsoft, is closed-source and owned by these entities. Although it is deemed the most powerful and generic LLM, its development and maintenance lack the contribution and influence of decentralized communities. This centralization leads to several negative consequences, such as limited access to the model, potential biases in the model, lack of transparency in development, and possible misuse or monopolization by the controlling entities.

*The need for a decentralized, community-driven LLM* - In contrast to the centralized development and maintenance of LLMs like ChatGPT, there is a growing need for a decentralized, community-driven LLM that can be developed and maintained by various stakeholders. Such an approach would not only ensure a more transparent and democratic development process but also create a more inclusive and diverse model that caters to different needs and use cases. It would also promote innovation and collaboration among developers, researchers, and users, resulting in a more robust and adaptable LLM.

*Applying the EIP-5521 standard to LLMs* - The EIP-5521 standard introduces the concept of referable NFTs, with indicators such as `referring`, `referred`, and `createdTimestamp`, forming a Directed Acyclic Graph (DAG). By applying the concept and spirit of the EIP-5521 standard to the LLM area, we can promote a truly open-source LLM, which is developed and maintained by decentralized communities.

*Ownership and sharing in a decentralized LLM* - Using the concept of referable NFTs, we can determine the ownership and sharing of micro-models or domain-driven datasets during the aggregation and evolution of the global model. Model/data watermark techniques can be used to define ownership, which can then be uploaded to and protected by the public blockchain network. Sharing can also be explicitly determined based on the contribution of training the global model. For example, suppose a researcher contributes a dataset related to healthcare to the decentralized LLM. In that case, the ownership of this dataset can be established using watermark techniques, ensuring that the researcher receives due credit and reward for their contribution. Similarly, when another developer builds upon this dataset to create a new model for drug discovery, the new model can refer back to the original dataset, preserving the lineage and enabling fair sharing of benefits.

*A decentralized workflow for open-source LLMs* - Applying the EIP-5521 standard enables a decentralized workflow for constructing an open-source and more domain-driven LLM, potentially rivaling the performance of ChatGPT. By encouraging contributions from the community, the development of the LLM becomes a more transparent and collaborative process.

*The benefits of a decentralized LLM in the Web3 world* - In the Web3 world, a decentralized LLM would be free from centralized control and could evolve more healthily and beneficially for humanity. LLM regulations and maintenance would be distributed among community members, ensuring a more balanced and democratic approach to development. This decentralized LLM would encourage innovation, foster collaboration, and provide better access to powerful language models for a broader range of users.

Additionally, a decentralized LLM would help prevent the potential misuse or monopolization of such technology by a single entity or a few entities, ensuring that the benefits are distributed more fairly and equitably. With a more diverse set of contributors, the model would be better equipped to address and minimize biases, resulting in a more inclusive and representative LLM.

In conclusion, applying the concept and spirit of the EIP-5521 standard to the LLM area offers a promising path towards building a decentralized, community-driven language model that can rival the performance of closed-source models like ChatGPT. By leveraging referable NFTs and encouraging the contribution and collaboration of decentralized communities, we can create a more transparent, inclusive, and adaptable LLM. In the Web3 world, this approach would help mitigate the negative consequences associated with centralized control of LLMs, promote fair distribution of ownership and rewards, and ultimately lead to a more beneficial and democratic development of language models for humanity.

**Note**

Our group has released a fully decentralized Federated Learning (FL) framework that seamlessly matches this concept, named [IronForge](https://ieeexplore.ieee.org/document/10323597). Please feel free to have a look.

---

**xinbenlv** (2023-08-02):

I like the idea!

There are two recommendation if my mind:

1. Consider generalize: I think the referrable idea is an interesting and useful topic. The way you use it was based on the extendable bytes data.  One of the related ERC is ERC-5750: General Extensibility for Method Behaviors. In addition to ERC-721, any tokens or smart contract implemented the ERC-5750 will be able to support similar behavior of Referrer / Referee identifier. For example, someone could claim a ENS by setting the referrer / referee. I wonder if you would be interested to make it generally referrable.
2. Consider to signup to present at next AllERCDevs to get feedback from other Authors and dApp builder peers. AllERCDevs is a regular meetup for the ERC Authors, Contributors and dApp developers together to get tech peer feedback and advocate for standardization and adoption. We usually present ERCs (including drafts and final ones), smart contracts, libraries and dApps.

---

**deep_blue** (2023-08-04):

Yes, but our proposal is open to other formats once being standardized, such as https://quant.network/news/quant-granted-patent-for-chronologically-ordering-blockchain-transactions/

---

**deep_blue** (2023-08-04):

Thanks for your recommendations. We will look into ERC-5750 for a possible adoption and join AllERCDevs.

---

**xinbenlv** (2023-08-08):

Looking forward to it. The next [allercdevs](/tag/allercdevs) will current in about 2h. See [[Current] 7th AllERCDevs Agenda · Issue #8 · ercref/AllERCDevs · GitHub](https://github.com/ercref/AllERCDevs/issues/8) for meeting links

---

**OniReimu** (2023-08-23):

We are finalizing the draft right before moving forward to the review phase, hopefully within a week.

---

**Mani-T** (2023-08-23):

Decentralizing the development and maintenance of LLMs addresses the concerns of centralized control.  It promotes collaboration, innovation, and the involvement of a broader range of stakeholders. It’s really a fantastic idea.

---

**OniReimu** (2023-09-04):

The introduction of EIP-5521 enhances the utility of NFTs and presents opportunities with advanced frameworks such as the one ([IronForge](https://ieeexplore.ieee.org/document/10323597)) we mentioned above. Specifically, EIP-5521 can be leveraged to bolster Federated Tuning/Training for any kind of model, including LLMs. This can be accomplished by establishing new reference relationships among NFTs in a parallel chain (parallel to the model markets, etc). The cross-compatibility between EIP-5521 and [IronForge](https://ieeexplore.ieee.org/document/10323597) enriches the scope of collaborative research and practical applications, particularly in the burgeoning academic disciplines within the Web3 ecosystem. This reinforces EIP-5521’s wide-ranging applicability and its role as a cornerstone for innovative strategies in decentralized networks.

---

**OniReimu** (2023-09-04):

One more follow-up message is that we just proposed moving to Review today. Welcome all for any further discussion.

---

**ruismoore** (2023-09-04):

Avoid being duped by several online testimonies that are almost certainly false. I have used a number of recovery methods that left me unsatisfied in the end, but I have to admit that Alien Wizbot crypto recovery is the tech brilliance I ultimately discovered to be the best available. It is advisable that you take the time to identify a reputable specialist who can assist you in recovering your lost or stolen cryptocurrency rather than being a victim of other inexperienced hackers who are unable to complete the task. The most trustworthy and genuine blockchain technology expert you may engage with to get back what you lost is Alienwizbot crypto recovery. I’m grateful to them for helping me get back on my feet. Send them an email right away to get your missing coins back. alienwizbot. com

---

**OniReimu** (2023-09-17):

We also added the system architecture figure here.

---

**OniReimu** (2023-10-27):

We are pleased to step into the review stage. The current version post here has been up to date.

---

**jnj** (2023-11-25):

Nice work, and I can see a lot of potentials, some practical cases such as: book adapted movies.

One question is that I think EIP-5521 (ERC-721 Referable NFT) is different from, somehow sharing something in common with ERC-6551 (Non-fungible Token Bound Accounts, [ERC-6551: Non-fungible Token Bound Accounts](https://eips.ethereum.org/EIPS/eip-6551)).

ERC-6551

[![Screenshot 2023-11-25 at 14.46.18](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4731650130ae98e3200bedf89159a826381e9818_2_690x324.jpeg)Screenshot 2023-11-25 at 14.46.181666×784 47.7 KB](https://ethereum-magicians.org/uploads/default/4731650130ae98e3200bedf89159a826381e9818)

reference video https://www.youtube.com/watch?v=vmSbDArbrwI

That would be great if you could elaborate on both the differences and similarities, and even the possible composition and collaboration between the two.

Thanks.

---

**Chan** (2023-11-25):

Thanks for your positive feedback and question. Let me try:

We are both trying to address NFT dependence problems, but our approaches and focuses are different. While ERC-6551 uses an NFT as a broker/delegator to own the other NFTs on behalf of one or a set of accounts, we try to build the dependency/relationship between NFTs directly using our EIP-5521. We believe our approach is simple/elegant and thus can be used for more application scenarios.


*(11 more replies not shown)*
