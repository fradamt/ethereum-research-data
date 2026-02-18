---
source: magicians
topic_id: 19284
title: "ERC-7652: EIP-721 Guarantee Extension"
author: bl2
date: "2024-03-20"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7652-eip-721-guarantee-extension/19284
views: 701
likes: 1
posts_count: 2
---

# ERC-7652: EIP-721 Guarantee Extension

Hi Magicians，We would like to propose an extension for EIP-721.

## Abstract

This specification defines functions outlining a guarantor role for instance of EIP-721. The guarantee interface implements the user-set valuation and guarantee share for a given NFT (token ID), as well as the guarantee rights enjoyed and obligations assumed during subsequent transactions. An implementation enables the user to read or set the current guarantee value for a given NFT (token ID), and also realizes the distribution of guarantee interest and the performance of guarantee obligations. It sends the standardized events when the status changes. This proposal relies on and extends the existing EIP-721.

## Motivation

NFT (token ID) commonly face the issue of insufficient market liquidity: the main reason being the lack of transparency in NFT pricing, making it difficult for users to cash out after trading and purchasing NFT (token ID).With the introduction of the guarantor role, different guarantor groups can offer various price guarantees for NFT (token ID), establishing a multi-faceted price evaluation system for NFT (token ID).After purchasing an NFT (token ID), users can return it to the guarantor at any time at the highest guaranteed price to protect their interests.Additionally, after fulfilling their guarantee obligations, the guarantor can also request subsequent guarantors to provide guarantee obligations.When an NFT (token ID) is owned by the guarantor, and since the guarantor can be a DAO organization, this expansion allows the NFT (token ID) to continue operating as a DAO, thus further enhancing the social or community recognition of the NFT (token ID).

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.Every contract compliant to the `EIP721Guarantee` MUST implement the `IEIP721Guarantee` guarantee interface.The **guarantee extension**  is OPTIONAL for EIP-721 contracts.

EIP Page (the [PR](https://github.com/ethereum/ERCs/pull/349)):

## Replies

**bl2** (2024-03-27):

The document here [ERC-721 Guarantee Extension](https://github.com/iunknow588/EthCDao/blob/master/ERCS/erc-7652.md)

