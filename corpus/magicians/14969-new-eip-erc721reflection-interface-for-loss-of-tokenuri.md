---
source: magicians
topic_id: 14969
title: New EIP - "ERC721Reflection" (interface) - for loss of tokenURI
author: deepak-chainxt
date: "2023-07-07"
category: EIPs
tags: [erc, nft, token, erc-721]
url: https://ethereum-magicians.org/t/new-eip-erc721reflection-interface-for-loss-of-tokenuri/14969
views: 503
likes: 1
posts_count: 1
---

# New EIP - "ERC721Reflection" (interface) - for loss of tokenURI

Hi,

NFT tokens play a crucial role in the overall Blockchain Ecosystem, and their significance continues to grow as they contribute to the creator economy. However, many owners still find it risky to rely solely on the NFT creator’s infrastructure, IPFS, or central storage for their NFT’s metadata and media files. In the event of the absence of these resources, owners can lose all their valuable data. While there are some services and protocols available, such as Aleph.im, clubNFT, and filebase, that allow users to back up their metadata and media files, there is currently no way to change the “tokenURI” if the metadata JSON is lost. Consequently, owners have limited control over their media, even after investing money to acquire it.

To address this issue, I propose the implementation of an “ERC721Reflection” interface. If creators adopt this interface, owners would have the option to assign a reflectionURI for their NFT’s metadata and media, which they would store in their own IPFS or central storage. In the event of a loss of the tokenURI, the owner would still have the fallback option of the reflectionURI. At any point during their ownership of the NFT, owners could download and create a copy of their metadata and media files on their personal IPFS, subsequently updating the reflectionURI. For instance, if an owner decides to list their NFT on a platform like Opensea, but their tokenURI is lost, Opensea could retrieve the content from the reflectionURI and proceed with listing the NFT. This way, owners would feel more empowered to retain control over both their NFT and its associated metadata.

Proposed ERC721Reflection :

interface ERC721Reflection {

/// this emits when reflectionURI set created

event Reflected(uint256 indexed _tokenId);

/// for setting the reflection URI

/// Throws unless `msg.sender` is the current owner, an authorized

///  operator, or the approved address for this NFT. Throws if `_from` is

///  not the current owner. Throws if `_to` is the zero address. Throws if

///  `_tokenId` is not a valid NFT.

function createReflection(uint256 _tokenId, string  memory _reflectionURI);

/// this will return reflection URI

function reflectionURI(uint256 _tokenId) external view returns (string);

}
