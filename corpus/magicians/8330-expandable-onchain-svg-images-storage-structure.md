---
source: magicians
topic_id: 8330
title: Expandable Onchain SVG Images Storage Structure
author: Soohan-Park
date: "2022-02-16"
category: Magicians > Primordial Soup
tags: [nft, token, onchain, svg]
url: https://ethereum-magicians.org/t/expandable-onchain-svg-images-storage-structure/8330
views: 1261
likes: 0
posts_count: 1
---

# Expandable Onchain SVG Images Storage Structure

Hey, Ethereum Magicians ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=15)![:unicorn:](https://ethereum-magicians.org/images/emoji/twitter/unicorn.png?v=15)

How are you all doing? Spring is slowly approaching in South Korea.

Anyway, as you can see from the title and the content of the Abstract below, I have envisioned an Expandable Onchain NFT Images Storage, and based on this, I’m preparing an EIP.

And I’d like to know what you guys think about this.

Finally, I am always happy to get to your feedback, such as the possibility of adopting the EIP and comments on further improvements.

So everyone, be careful of COVID-19, and have a good day today!

## Simple Summary

It is a Expandable Onchain SVG Images Storage Structure Model on the Ethereum.

## Abstract

This standard proposal is a Expandable Onchain SVG Images Storage Structure Model on the Ethereum that permanently preserves images and prevents tampering, and can store larger-capacity images furthermore.

It is a structure designed to store SVG images with a larger capacity by distributed SVG images in units of tags on Ethereum.

The structure presented by this EIP consists of a total of three layers as shown below.

[![Structure Diagram](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e34dce111baba1baffa7519925f19cd7bd066600_2_690x283.jpeg)Structure Diagram781×321 22.4 KB](https://ethereum-magicians.org/uploads/default/e34dce111baba1baffa7519925f19cd7bd066600)

> Storage Layer ─ A contract layer that stores distributed SVG images by tags.
> Assemble Layer ─ A contract layer that creates SVG images by combining tags stored in the Storage Layer’s contract.
> Property Layer ─ A contract layer that stores the attribute values for which SVG tag to use.

It is designed to flexibly store and utilize larger capacity SVG images by interacting with the above three layer-by-layer contracts each other.

Also, you can configure the Onchain NFT Images Storage by adjusting the Assemble Layer’s contract like below.

- A storage with expandability by allowing additional deployment on Storage Layer’s contracts
- A storage with immutability after initial deployment

Additionally, this standard proposal focuses on, but is not limited to, compatibility with the [EIP-721](https://eips.ethereum.org/EIPS/eip-721) standard.

## Motivation

Most NFT projects store their NFT metadata on a centralized server rather than on the Ethereum. Although this method is the cheapest and easiest way to store and display the content of the NFT, there is a risk of corruption or loss of the NFT’s metadata.

To solve this problem, most NFT metadata is stored on Ethereum. However, it can only be expressed as a simple shape such as a circle or a rectangle, since one contract can be distributed 24KB size for maximum.

We propose this model *─ a more secure way to store NFT metadata ─*  to create and own high-quality of NFT metadata.

## Reference Implementation

### Proxy Layer

```solidity
pragma solidity ^0.8.0;

import {ERC721} from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import {IAssembleContract} from "./IAssembleContract.sol";

/**
 * @title PropertyContract
 * @author
 * @notice A contract that stores property values.
 */
contract PropertyContract is ERC721 {
    /**
     * @notice A variable that stores the object of `AssembleContract`.
     */
    IAssembleContract public assembleContract;

    // Storing property values corresponding to each number of storage. (tokenId -> attr[])
    mapping(uint256 => uint256[]) private _attrs;

    /**
     * @dev `name_` and `symbol_` are passed to ERC-721, and in case of `assembleContractAddr_`, the `setAssembleContract` function is used.
     */
    constructor(string memory name_, string memory symbol_, address assembleContractAddr_) ERC721(name_, symbol_) {
        setAssembleContract(assembleContractAddr_);
    }

    /**
     * @dev See {IAssembleContract-getImage}
     */
    function getImage(uint256 tokenId_) public view virtual returns (string memory) {
        return assembleContract.getImage(_attrs[tokenId_]);
    }

    /**
     * @param newAssembleContractAddr_ Address value of `AssembleContract` to be changed.
     * @dev If later changes or extensions are unnecessary, write directly to `constructor` without implementing the function.
     */
    function setAssembleContract(address newAssembleContractAddr_) public virtual {
        assembleContract = IAssembleContract(newAssembleContractAddr_);
    }

    /**
     * @param tokenId_ The token ID for which you want to set the attribute value.
     * @dev Set the attribute value of the corresponding `tokenId_` sequentially according to the number of asset storage.
     */
    function _setAttr(uint256 tokenId_) internal virtual {
        for (uint256 idx=0; idx "));

        for (uint256 i=0; i '));

        return imageString;
    }

    /**
     * See {IAssembleContract-getStorageCount}
     */
    function getStorageCount() external view virtual override returns (uint256) {
        return _assets.length;
    }

    /**
     * @param storageAddr_ Address of `StorageContract`.
     * @dev If later changes or extensions are unnecessary, write directly to `constructor` without implementing the function.
     */
    function addStorage(address storageAddr_) public virtual returns (uint256) {
        _assets.push(AssetStorage({
            addr: storageAddr_,
            stock: IStorageContract(storageAddr_)
        }));
        return _assets.length-1; // index
    }
}
```

### Storage Layer

```solidity
pragma solidity ^0.8.0;

/**
 * @title IStorageContract
 * @author
 * @dev A contract that returns stored assets (SVG image tags). `setAsset` is not implemented separately.
 * If the `setAsset` function exists, the value of the asset in the contract can be changed, and there is a possibility of data corruption.
 * Therefore, the value can be set only when the contract is created, and new contract distribution is recommended when changes are required.
 */
interface IStorageContract {
    /**
     * @notice Returns the SVG image tag corresponding to `assetId_`.
     * @param assetId_ Asset ID
     * @return A SVG image tag of type String.
     */
    function getAsset(uint256 assetId_) external view returns (string memory);
}
```

```solidity
pragma solidity ^0.8.0;

import {IStorageContract} from "./IStorageContract.sol";

/**
 * @title StorageContract
 * @author
 * @notice A contract that stores SVG image tags.
 * @dev See {IStorageContract}
 */
contract StorageContract is IStorageContract {

    // Asset List
    mapping(uint256 => string) private _assetList;

    /**
     * @dev Write the values of assets (SVG image tags) to be stored in this `StorageContract`.
     */
    constructor () {
        // Setting Assets such as  _assetList[1234] = "<circle ...";
    }

    /**
     * @dev See {IStorageContract-getAsset}
     */
    function getAsset(uint256 assetId_) external view override returns (string memory) {
        return _assetList[assetId_];
    }
}
```

---

Additionally, there is one thing I would like to ask you for your opinion on this EIP!

When I first conceived this EIP, it was designed so that **the contract that stores assets of the storage layer can be replaced.** However, while materializing the proposal, I thought that **REPLACEABLE** would go against the immutability of the blockchain, so I excluded it from the current version of the proposal.

I’d like to get opinions on whether it’s better to not have **REPLACEABLE** like the current version, or a replaceable version is better in your opinion.
