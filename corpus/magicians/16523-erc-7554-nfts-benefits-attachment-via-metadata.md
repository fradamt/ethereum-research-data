---
source: magicians
topic_id: 16523
title: "ERC-7554: NFTs Benefits Attachment via Metadata"
author: asghaier
date: "2023-11-08"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7554-nfts-benefits-attachment-via-metadata/16523
views: 834
likes: 1
posts_count: 5
---

# ERC-7554: NFTs Benefits Attachment via Metadata

A proposal for ERC to allow for attaching benefits to NFTs and allow easy and open access to how to discover and query the attached benefits. The proposed standard extends ERC-721.

This standard defines an interface extending EIP-721 to provide an easy and on-chain approach for discovery and query of benefits and perks attached to NFTs. The attached benefits are defined by a schema that is stored off-chain and with a set of events and functions on-chain to allow for querying and access to benefits data. The benefits can represent for example an e-commerce store coupon, an access to conference, or a discount on goods and services at a certain establishment.

Each of the attached benefits is described through benefits metadata that will allow any third party to easily discover, query and verify the attached benefits and the criteria for redemption.

The main motivation behind proposing this ERC is to consolidate efforts related to token-gating as most of these were built as silos relying on proprietary solutions and data that is limited in use to a single vendor. Moreover, NFT collection owners are left out of this process since any third party can start attaching benefits and perks to NFTs in a certain collection to target and acquire customers from that community without any involvement of the NFT collection owner or any royalty to be offered to the creator.

This standard aims to provide the capability to attach and manage benefits attached to NFTs using on-chain functionality and with a standardized benefits metadata that will make it easy for 3rd parties such as marketplaces, aggregators and data analytics actors to collect that information.

The standard aims to specify an interface that will allow capturing the events triggered by attaching and disattaching benefits as well as the standard functions to allow querying all benefits attached to a single NFT or a collection.

The use of NFT token-gating and benefits attachment has already been considered in many applications like the adoption of Shopify of the token-gating concept that can open the doors for many use cases including for example an online store offering a discount for customers who own a specific NFT; an airdrop to be limited to only owners of NFTs from a certain collection; a restaurant can offer certain coupons and discounts to some holders, and many others.

As mentioned above, the proliferation of token-gating and benefits attachment will mean that certain blue chip NFTs and collections with vibrant communities will be the target by many brands and businnesses to start utilizing that already established community and use it as an approach for customer acquisition. However, both NFT holders and creators are left outside of this equation, since most of that will be taking place in silo gated environments in which data related to the benefits will be proprietary data and managed by token gating platforms owned by brands and businesses. Therefore, this standard aims at defining the interfaces in terms of functions and events that extends ERC-721 to provide the complete functionality to manage those benefits and define the metadata standard that will allow an easy way to aggregate and query those benefits and their attributes.

The suggested approach will offer creators more capability to manage the community expectation and also allow holders to discover easily what types of benefits are available for the NFTs they hold. For example, a brand through certain analytics can identify a certain blue chip collection community as a fit for their campaign for a new product or service and start attaching benefits but that will need to be approved and handled by the collection creator. Let’s assume the case of VIP access to an airport lounge, the brand will aim to acquire those customers that belong to the collection community while the creator has no interaction at all. Also, the NFTs holders might not be easily able to identify the actual attached benefits value for the tokens they hold based on the different benefits attached to the NFT since that data is in scattered in silos and might be kept private by each entity.

Therefore, this standard proposes a set of interfaces that can allow creators to manage or approve the NFTs benefits attachment and to allow for easy discovery and verifiability of those benefits by the different entities involved.

https://github.com/ethereum/ERCs/pull/97

## Replies

**Mani-T** (2023-11-09):

Have you considered introducing a feedback mechanism?  Because incorporating a mechanism for community feedback or involvement in the standardization process could ensure that the proposal reflects a broader consensus and considers diverse perspectives.

---

**asghaier** (2023-11-09):

I thought having it here in the forum is the best way to get community feedback, do you have suggestion for other channels to funnel feedback to this forum and get wider community feedback.

---

**codervake** (2024-09-23):

sounds good, it there some practical examples to describe?

---

**aekiro** (2024-09-24):

Sounds interesting. Working on something that may use this idea in the future

