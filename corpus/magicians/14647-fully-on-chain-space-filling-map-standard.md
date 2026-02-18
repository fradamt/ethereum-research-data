---
source: magicians
topic_id: 14647
title: Fully on-chain space-filling map standard
author: RayHuang
date: "2023-06-11"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/fully-on-chain-space-filling-map-standard/14647
views: 295
likes: 0
posts_count: 1
---

# Fully on-chain space-filling map standard

There are more and more projects in web3 that are doing virtual land-related NFT or on-chain land-related businesses, such as The Sandbox, Decentraland, and CryptoVoxels…etc.

So this is a proposal to formulate relevant interfaces so that such projects can be used as standards for better integration. Whether in the real world or those map protocols, a location is represented by 2D coordinates, but a unique number (index) is required to represent it in algorithmic or `ERC721` tokens (tokenId).

Therefore, there will be a need for a 1D and 2D exchange interface, no matter what algorithm or method is used to implement their conversion.

```auto
function index2xy(uint256 index) external pure returns (uint256 x, uint256 y);
```

```auto
function xy2index(uint256 x, uint256 y) external pure returns (uint256 index);
```

In addition, the interface must also be able to view the owner of each grid (land) and the balance of every grid (land) owner

```auto
function ownerOf(uint256 index) external view returns (address owner);
```

```auto
function balanceOf(address owner) external view returns (uint256 balance);
```

It can be seen that the interface of `ownerOf` and `balanceOf` are exactly the same as `ERC721`, so it can be perfectly integrated with `ERC721` if necessary

In this repo, I implemented a contract that integrates this interface with `ERC721`. The conversion of `index` and `(x, y)` uses the hilbert-curve algorithm, and other functions of `ERC721` refer to OpenZeppelin.

https://github.com/RayHuang880301/hilbert-curve-map
