---
source: magicians
topic_id: 11333
title: Best EIP for generalised ERC721 rentals
author: OxMarco
date: "2022-10-16"
category: EIPs
tags: [nft, metaverse]
url: https://ethereum-magicians.org/t/best-eip-for-generalised-erc721-rentals/11333
views: 486
likes: 1
posts_count: 1
---

# Best EIP for generalised ERC721 rentals

Hello everyone!

I am working on a way to perform on-chain rentals and mortgages on NFT, mainly virtual estate (metaverse LANDs), play2earn and gated communities.

Looking at the current proposed standards, the [EIP4907](https://eips.ethereum.org/EIPS/eip-4907) and EIP5501, they all include a `user`/`controller`/`operator` role while maintaining the ownership of the NFT unaltered. Despite seemingly being a very good solution, such approach is suitable for *Decentraland* and *the Sandbox* only.

In fact, in order to support the ever-increasing NFT uses, simply relying on a new mapping is not enough. For instance, the *Rentable* team specifically chose to create a NFT wrapper with a [proxy function](https://github.com/emilianobonassi/rentable-protocol-v1/blob/52fd52e6a9655fd8a369126ee0e3f75e10a45191/contracts/ERC721ReadOnlyProxy.sol#L78) to support interoperability with present and future NFT implementations.

What is the best solution to support both existing NFT uses (i.e. build on metaverses and access groups restricted to holders) and future ones among the current EIPs?
