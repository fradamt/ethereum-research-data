---
source: magicians
topic_id: 14468
title: "Introducing New EIP: NFT Relationship Enhancement"
author: xg1990
date: "2023-05-28"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/introducing-new-eip-nft-relationship-enhancement/14468
views: 1773
likes: 2
posts_count: 3
---

# Introducing New EIP: NFT Relationship Enhancement

Hello Ethereum community!

I would like to introduce a new EIP called the NFT Relationship Enhancement. This proposal aims to enhance the functionality of non-fungible tokens (NFTs) by providing a standardized way to establish **relationships between NFTs and set quantifiable attributes for those relationships**.

Motivation: The motivation behind this EIP is to enable more complex and interesting use cases for NFTs. By allowing NFT creators and users to define relationships and quantify attributes between NFTs, we can track ownership history, establish provenance, and create interactive games and experiences within the NFT ecosystem.

Unlike existing EIPs, the NFT Relationship Standard focuses specifically on both ERC-721 and ERC-1155 tokens and extends their capabilities to handle referring relationships and quantifiable attributes between NFTs. This provides a powerful toolset for managing and quantifying relationships within NFT ecosystems.

Read the full EIP draft here: [NFT Relationship Enhancement](https://github.com/ethereum/EIPs/pull/7085/)

Looking forward to your thoughts

## Replies

**SamWilsn** (2023-09-21):

Hey! Here are those technical concerns I mentioned:

- You don’t standardize any way to read the attributes. Arguably that’s even more important than being able to write them. In your reference implementation you have some public mapping variables, but you probably want those in your Specification section as well.
- I’d recommend using a Solidity interface to specify your functions. It makes it way easier for people to import it as a library.
- You might want to look into ERC-165 and add support for that.

---

**xg1990** (2023-10-07):

Thanks Sam! I just submitted a PR to update the draft according to your comments.

