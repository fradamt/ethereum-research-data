---
source: magicians
topic_id: 18550
title: "ERC-7653: Named NFTs (ERC-721 extension)"
author: xinbenlv
date: "2024-02-07"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7653-named-nfts-erc-721-extension/18550
views: 1249
likes: 1
posts_count: 2
---

# ERC-7653: Named NFTs (ERC-721 extension)

## Summary

ERC-721 and ERC-1155 uses `uint256 tokenId`, this standard extend them with `string name`.

## Motivation

For Marketplaces, Explorers, Wallets, DeFi and dApps to better display and operate NFTs that comes with a name.

## Specification

```solidity
interface IERCNamedNFT {
  function safeTransferFromByName(string memory _tokenName, address from, address to, bytes calldata);
  function approveByName(address _approved, string memory _tokenName) external payable;
  function idToName(uint256 _tokenId) external view returns (string);
  function nameToId(string memory _tokenName) external returns (uint256);
  function getApprovedByName(string memory _tokenName) external view returns (address);
}
```

## Security Considerations

1. Contract developer shall declare normalization mechanism

## Replies

**xinbenlv** (2024-02-22):

Moving forward with draft

