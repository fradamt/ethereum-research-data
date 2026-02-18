---
source: magicians
topic_id: 11613
title: "Idea : minting one billion NFTs or 2^256"
author: sciNFTist.eth
date: "2022-11-04"
category: Magicians > Primordial Soup
tags: [nft, token, eip-2309]
url: https://ethereum-magicians.org/t/idea-minting-one-billion-nfts-or-2-256/11613
views: 882
likes: 0
posts_count: 1
---

# Idea : minting one billion NFTs or 2^256

# Abstract

minting arbitrary number of NFT can be done in one transaction using efficient data structures.

quoted from EIP-2309:

> This allows for the original Transfer event to be emitted for one token at a time, which in turn gives us O(n) time complexity. Minting one billion NFTs can be done in one transaction using efficient data structures, but in order to emit the Transfer event - according to the original spec - one would need a loop with one billion iterations which is bound to run out of gas, or exceed transaction timeout limits. This cannot be accomplished with the current spec. This extension solves that problem.

# Motivation

Since [EIP-2309](https://eips.ethereum.org/EIPS/eip-2309) provide more scalability of the ERC-721 specification, It is possible to create, transfer, and burn `2^256` non-fungible tokens in one transaction.

this changes provide a pragmatic way to mint arbitrary number of token in constructor with `O(1)` time complexity.

# Specification

for in depth implementation see the [eip-draft_ERC721FancyMint](https://ethereum-magicians.org/t/eip-draft-mint-arbitrary-number-of-tokens-erc-721-via-eip-2309/11589)

- preOwner is the creator/receiver  address
- maxSupply is desired( Batch token creation
>
>
> emit ConsecutiveTransfer(1, 100000, address(0), toAddress);

# EIP draft

eip draft is proposed at ethereum-magicians [here](https://ethereum-magicians.org/t/eip-draft-mint-arbitrary-number-of-tokens-erc-721-via-eip-2309/11589/1). and you can see reference implementation for more details. I wish to hear your thoughts.
