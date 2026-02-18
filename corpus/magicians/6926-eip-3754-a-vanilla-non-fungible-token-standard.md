---
source: magicians
topic_id: 6926
title: "EIP-3754: A vanilla non-fungible token standard"
author: maxareo
date: "2021-08-22"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-3754-a-vanilla-non-fungible-token-standard/6926
views: 1290
likes: 1
posts_count: 6
---

# EIP-3754: A vanilla non-fungible token standard

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/3753)












####



        opened 02:23PM - 21 Aug 21 UTC



          closed 04:58PM - 21 Nov 22 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/8/8e5f7cce79e8b354fabb18a6c173307bb6d52dc4.jpeg)
          simontianx](https://github.com/simontianx)





          discussions-to







## Abstract
A vanilla NFT standard is proposed. In this standard, a non-fungibl[…]()e token stands as atomic existence and encourages layers of abstraction built on top of NFTs. Ideal for representing concepts like right, a form of abstract ownership. Such right, especially on-chain right, can then be made liquid because of this tokenization.

## Rationale
The primary intention of this proposal is not to make a technical improvement to ERC721, although a new technical direction in a subsequent proposal EIP-4341 does present new technical merits, but rather to improve the conceptual clarity of NFTs, i.e., NFTs for digital collectibles, crypto-assets are specified and known by ERC721, and NFTs for abstract ownership such as rights, membership, etc. are specified and known by EIP-3754.

## Use Cases
An example of applying this token to represent the right of making a function call to a contract is given [here](https://github.com/simontianx/ERC3754/blob/main/contracts/ERC3754Example.sol).

An on-chain subscription business model is also made possibe by adopting this token to represent quarterly or yearly membership (time-dependent right). An example can be fees per transaction for off-chain data via an oracle can be replaced by a long-term membership fee. Then as long as the caller has a valid EIP-3754 NFT, the consumption of data feeds is free (plus gas fees). NFTs can be transferred, so is the right of consuming data feeds. This has certain advantages over the current pay-as-you-go business model. An example can be found [here](https://github.com/simontianx/ERC3754/blob/main/contracts/OracleMembership.sol).

A mid-layer can be added between NFT buyers and NFT creators with this standard. Currently, NFT creators have difficulty setting up initial prices and NFT buyers have the fear of missing out good NFTs. A mid-layer can be added between the two sides by minting ERC3754 NFTs as rights to purchase NFTs. NFT creators can presale such rights at lower prices and set the initial prices higher. For NFT buyers, buying such rights is a small commitment and can sell such rights if they do not like the NFTs minted later on. It can be best understood as a call option on an NFT. Effectively, this is a market making layer by reducing the bid-ask spread. A similar but slightly different idea can be seen in "@0xKiwi_ designed for @uwucrewnft". An in-house toy example can be found [here](https://github.com/simontianx/ERC3754/blob/main/contracts/NFTOption.sol).

A virtual coupon can be built by this standard. Ownership of such NFTs can enjoy certain discounts over a preset period of time.

Another great illustration of this concept can be found in this [tweet](https://twitter.com/AndreCronjeTech/status/1432687892497895425) that Andre Cronje sold the naming rights to his Twitter account to FTX.














      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3754)














####


      `master` ← `simontianx:master`




          opened 02:38PM - 21 Aug 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/8e5f7cce79e8b354fabb18a6c173307bb6d52dc4.jpeg)
            simontianx](https://github.com/simontianx)



          [+74
            -0](https://github.com/ethereum/EIPs/pull/3754/files)







## Abstract
In this standard, a non-fungible token stands as atomic existence a[…](https://github.com/ethereum/EIPs/pull/3754)nd encourages layers of abstraction built on top of NFTs. Ideal for representing concepts like rights, a form of abstract ownership. Such right, especially on-chain right, can then be made liquid because of this tokenization.

## Motivation
Non-fungible tokens are popularized by the [ERC-721](./eip-721.md) NFT standard for representing "ownership over digital or physical assets". Over the course of development, reputable NFT projects are about crypto-assets, digital collectibles, etc. The proposed standard aims to single out a special type of NFTs that are ideal for representing abstract ownership such as rights. Examples include the right of making a function call to a smart contract, an NFT option that gives the owner the right but not obligation to purchase an ERC721 NFT, and the prepaid membership (time-dependent right) of accessing to data feeds provided by oracles without having to pay the required token fees. An on-chain subscription business model can then be made available by this standard. The conceptual clarity of an NFT is hence improved by this standard.

## Replies

**blockchain_addict** (2021-08-23):

According to the Open zeppelin documentation, the uri related methods are anyway optional and comes as part of `IERC721Metadata` Interface : [ERC 721 - OpenZeppelin Docs](https://docs.openzeppelin.com/contracts/2.x/api/token/erc721)

Is this EIP addressing this or is there any other aspect?

---

**maxareo** (2021-08-23):

ERC721 standard is indeed a super set to the proposed standard here. That also introduced problems. When applications of this 3754 standard are being explained to those who are deeply rooted in the current understanding of NFTs in ERC721 standard, costs are actually very high.

Therefore, the rationale of this standard is to free people from thinking of NFTs as tangile items such as digital-arts, in-games items or anything that is made available via `URI`.

Instead, a new standard ought to be developed to reduce the concept of NFT to its core, which is a non-fungible token. Nothing else would have to be attached to it. Interestingly, this simplification can open up new possibilities by allowing layers of abstraction built on top of it.

---

**maxareo** (2021-08-29):

One specific example and one new business model are given below. ERC-721 just seems unfit.

An example of applying this token to represent the right of making a function call to a contract is given [here](https://github.com/simontianx/ERC3754/blob/main/contracts/ERC3754Example.sol).

An on-chain subscription business model is also made possibe by adopting this token to represent quarterly or yearly membership (time-dependent right). An example can be fees per transaction for off-chain data via an oracle can be replaced by a long-term membership fee. Then as long as the caller has a valid ERC-3754 NFT, the consumption of data feeds is free (plus gas fees). NFTs can be transferred, so is the right of consuming data feeds. This definitely has great advantages over the current pay-as-you-go business model.

---

**maxareo** (2021-10-02):

This proposal has been merged. Check it out [here](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3754.md).

---

**Pandapip1** (2022-06-03):

What’s the difference between this and EIP-721 without the optional metadata extension? To me, this just seems like a duplicate.

