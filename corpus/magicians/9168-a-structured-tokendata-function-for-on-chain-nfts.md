---
source: magicians
topic_id: 9168
title: A structured tokenData function for on-chain NFTs
author: clemlaflemme
date: "2022-05-05"
category: EIPs
tags: [nft, metadata, on-chain]
url: https://ethereum-magicians.org/t/a-structured-tokendata-function-for-on-chain-nfts/9168
views: 722
likes: 2
posts_count: 1
---

# A structured tokenData function for on-chain NFTs

## Abstract

A new interface that should implement on-chain NFTs projects, mimicking the current JSON scheme of the `IERC721Metadata`, but returning the data as a struct.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/7/72a1acebf8417c77bd1d291b9463bf5705d63e54_2_631x500.jpeg)image1598×1266 73.7 KB](https://ethereum-magicians.org/uploads/default/72a1acebf8417c77bd1d291b9463bf5705d63e54)

## Motivation

The ERC721Metadata standard defines a `tokenURI(uint256) returns (string memory)` that returns a URI containing the metadata for the token.

Most of the projects use centralized (e.g. own servers, AWS) or decentralized (e.g. IPFS) to store this data and consequently returns only a string, e.g. `ipfs://...`.

On-chain projects though have to build on-chain a data uri that is compliant with this interface.

However:

- it is painful and cost gas to inline all the data and manually jsonify a token
- it creates a barrier for composability as it is difficult to parse a data:application/json,... on-chain
- eventually it is a useless op that destructs data without any good reasons: some may think that it’s better to keep standard JSON for data interfacing but it’s not actually the case as a eth_call is not a REST API: even these data uri need to be decoded by eth clients.
- on the opposite, using such a tokenData would let front end users access directly a typed API. In other words, it’s less work for the on-chain solidity dev and more info for the end user.
- using the ERC165, there will be no more discussions about “is it on chain or not” ?
- overall this would incentivize creators to build on-chain to build on top of each others.
