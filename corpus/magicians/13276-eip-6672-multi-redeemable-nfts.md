---
source: magicians
topic_id: 13276
title: "EIP-6672: Multi-redeemable NFTs"
author: randyanto
date: "2023-03-13"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/eip-6672-multi-redeemable-nfts/13276
views: 3193
likes: 9
posts_count: 2
---

# EIP-6672: Multi-redeemable NFTs

This EIP proposes an extension to the ERC-721 standard for Non-Fungible Tokens (NFTs) to enable multi-redeemable NFTs. This extension would allow an NFT to be redeemed in multiple scenarios for either physical or digital objects and maintain a record of its redemption status on the blockchain.

## Motivation

ERC-5560 enables only one-time redemption of an NFT, which means the same NFT cannot be re-used for another redemption from different campaigns or events.

## Proposed Improvement

- Utilize the combination of _operator, _tokenId, and _redemptionId as the key in the redemption flag key-value pairs where _operator is the operator wallet address,tokenId is  the identifier of the token that has been redeemed, and _redemptionId is redemption identifier set by the operator.
- Additionally, to provide more granular information about a redemption, redemptions key-value pairs is added to the “ERC-721 Metadata Extension”. The key format for the redemptions key-value pairs MUST be standardized as operator-tokenId-redemptionId  The value of the key operator-tokenId-redemptionId is an object that contains the status and description of the redemption.

The redemption status can have a more granular level, rather than just being a flag with a true or false value, e.g. redeemed, paid, or shipping.
- The redemption description can be used to provide more details about the redemption, such as information about the concert ticket, a detailed description of the action figures, and more.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6672)














####


      `master` ← `redeemprotocol:master`




          opened 05:32AM - 10 Mar 23 UTC



          [![](https://avatars.githubusercontent.com/u/9522925?v=4)
            ArchieR7](https://github.com/ArchieR7)



          [+259
            -0](https://github.com/ethereum/EIPs/pull/6672/files)







An extension of EIP-721 which enables an NFT to be redeemed in multiple scenario[…](https://github.com/ethereum/EIPs/pull/6672)s for either a physical or digital object

## Replies

**poojaranjan** (2023-05-22):

[ERC-6672: Multi-redeemable NFTs](https://youtu.be/ZToiTpB87nQ) with BoYu Chu

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/1/128e740e470c6416328f415c1eca82e33bcecd81.jpeg)](https://www.youtube.com/watch?v=ZToiTpB87nQ)

