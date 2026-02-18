---
source: magicians
topic_id: 16446
title: "ERC-2125: Fractional NFT standard combining ERC-20, (ERC-721), and ERC-1155"
author: Ashraile
date: "2023-11-05"
category: EIPs
tags: [nft, eip, fractionalized]
url: https://ethereum-magicians.org/t/erc-2125-fractional-nft-standard-combining-erc-20-erc-721-and-erc-1155/16446
views: 881
likes: 0
posts_count: 2
---

# ERC-2125: Fractional NFT standard combining ERC-20, (ERC-721), and ERC-1155

Abstract:

An ERC2125 contract can natively exist within both ERC20 marketplaces and ERC1155 NFT marketplaces. ERC2125 is not natively compatible with ERC721 at this time.

There is a NFT that is ‘bound’, to a base ERC20 token.

This ERC20 token should have an internal reserved ERC1155 namespace / id of slot (0).

This implementation takes advantage of function overloading, due to the fact that ERC1155 and ERC20 functions do not directly overlap.

```
interface IERC2125 is IERC20, IERC20Metadata, IERC165, IERC1155, IERC1155TokenReceiver {
    function version() external view returns (string memory); // contract version
    function releaseDate() external view returns (uint40); // contract genesis date (timestamp)
    function releaseSupply() external view returns (uint256); // ERC-20 token release supply
    function releaseSupply(uint ID) external view returns (uint256); // ERC-1155 namespaced release
      supply.
    function ownerOf(uint tokenID, uint namespace) external view returns (address owner); // owner
}
```

Functions with the same name, but different arguments are implicitly determined to be either ERC20 or ERC1155 due to the number of arguments supplied.

Functions supplied with more arguments than the base ERC20 implementation are implicitly considered ERC1155 implementations.

Example:

balanceOf(address owner) => ERC20

balanceOf(address owner, uint ID) => ERC1155

ERC-2125 specific interface proposals:

releaseSupply()

releaseSupply(uint ID)

releaseDate()

version()

ownerOf(uint tokenID) // ERC721

ownerOf(uint tokenID, uint namespace) // ERC721 to 1155

To be continued.

## Replies

**abcoathup** (2023-11-06):

There isn’t an ERC2125 (that I can see), numbers are assigned by EIP/ERC editors: https://ercs.ethereum.org/ERCS/erc-2125

