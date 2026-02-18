---
source: magicians
topic_id: 7685
title: A new ERC idea for Spatial and Temporal Dividable Non-Fungible Token (STD-NFT)
author: fullnodes
date: "2021-12-04"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/a-new-erc-idea-for-spatial-and-temporal-dividable-non-fungible-token-std-nft/7685
views: 811
likes: 0
posts_count: 3
---

# A new ERC idea for Spatial and Temporal Dividable Non-Fungible Token (STD-NFT)

Hi the ethereum magicians, I am looking for vet of a new ERC proposal.

I am a computer graphics researcher working on metaverse application based on Ethereum. I am thinking of extending the ERC721 token standard to encoded a little bit data on chain to describe the spatial shapes and temporal periods of a NFT, that can be split and merged. It is designed for describing a spatial region like a land with a 2d shape (instead of always boring squares), or a room in a building. It is also designed for describing a temporal period which enables time-shared owning of NFTs. Following is a glance of the draft and looking for vetting of the full draft, a bit lengthy.

– fullnodes.

## Simple Summary

A standard interface for non-fungible tokens that can be divided and merged over spatial and/or temporal domain.

## Abstract

The following standard allows for the implementation of a standard API within smart contracts that extends the NFT standard with capabilities of being divided or merged, spatially or temporally. For NFTs having a sense of spatial shape or temporal scope, this standard provides basic functionality to divide a NFT into multiple adjacent fractions as new NFTs, and to merge multiple adjacent fractional NFTs into one.

We considered use cases of Spatial and Temporal Dividable Non-Fungible Tokens (“STD-NFT”) of representing ownership over assets with spatial metric like land, 2D artwork, spherical surface of a planet, 3D space of the universe, or assets with temporal metric like music, video, animation sequences, calendar.

## Motivation

An unique asset, represented by a NFT, can be divided into multiple unique fractions, each can be represented also by NFTs. For example, a physical land in real world or a virtual land in metaverse can be described its locations, size and specific shape. It can be divided in multiple ways and result in several unique pieces of lands, each will be presented by a new NFT. Such assets should be able to divide and separately owned and transacted on blockchain, which will enrich the NFT ecosystem and enable new applications especially for metaverse and games. Besides spatial division, another important use case is partially owned NFT on time-sharing basis by dividing the available time over calendar. Both cases are beyond the scope of the ERC-721 standard.

The STD-NFT standard proposed by EIP-xxx allows an NFT to be divided into fractions as new NFTs, and to be merged back. STD-NFT is differentiated from fungible token (ERC-20) as each divided fraction is unique. Also such dividing is finite which is subject to granularity restriction (e.g. minimal allowed area, or volume). Component-NFT (ERC-3664) introduced a bottom-up paradigm for objectizing NFTs, which starts from small unique components and assembles. The STD-NFT standard is designed with an opposite perspective. It introduced a down-top paradigm by dividing a NFT as a whole piece into fractions. The STD-NFT standard is also different from tokenization of NFTs in the sense of purpose and implementation, which issues new fungible tokens backed on reservation of specific NFTs. Securitization is not the goal of the proposed STD-NFT standard.

The STD-NFT standard allows game creator forges a whole piece of land or a planet, then divides and sells. A NFT can be partially owned with time-sharing based on temporal division on calendar. An 2D artwork can be broken into pieces with arbitrary shapes and owned by different users. The STD-NFT standard provides versatile functionalities to build the future NFT ecosystem for metaverse and games on blockchains. It is extension standard of ERC-1155 and ERC-721, which implies compatibility with the these standard and interoperability of state-of-art NFT exchanges and wallets.

Optionally, a predefined series of quantitative properties, *STD-NFT factors*,  is associated with each STD-NFT instance, which indicates different numeric conditions of a STD-NFT. For example, a property can be the height limit of building in street blocks, air density of areas, energy supply per volume of rooms in a building and mining yield per area in lands. All STD-NFT factors are defined in a sense of quantity per size of the spatial(-temporal) domain so that factors can be simply duplicated when a STD-NFT is split, and can be weighted-averaged on merging. STD-NFT factors can be redistributed among adjacent STD-NFTs that owned by the same address while conservation of total summed `factor⨯size` is required, or can be set to arbitrary values by special owners (e.g. the game master)

## Replies

**fullnodes** (2021-12-04):

Also the EIP would come with a proposal of a library-like contract that aids other developers on computational geometry for operating shapes. Representing and handling of geometry shapes without losing information is a non-trivial task in Solidity, partially because of lacking floating point numbers.

---

**fullnodes** (2021-12-06):

Do I followed the right procedure? or it should be something else to have an EIP get review??  plz help ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=10)

