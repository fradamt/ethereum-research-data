---
source: magicians
topic_id: 10291
title: NFT Bond (Option) Protocol
author: SpiderAres
date: "2022-08-08"
category: EIPs
tags: [nft, defi, gamefi]
url: https://ethereum-magicians.org/t/nft-bond-option-protocol/10291
views: 1330
likes: 1
posts_count: 2
---

# NFT Bond (Option) Protocol

## Abstract

Based on the reason of further improving the value empowerment and capture of creators’ derivative creations using the game editor, the proposal proposes an NFT bonding (or optioning) agreement that binds the value of creators and fans in a “crowdfunding-like” manner by combining actual interests.

The NFT bond would allow creators to raise more capital to expand their creative teams and expand their business, while providing fans with more creative and diverse game content, with a focus on content production. In addition, the creators can also provide more benefits to the fans who purchase the NFT bonds, such as exclusive content and interactive value-added services for fans, and early access to new versions of the game for trial play.

## Motivation

It has been a big problem for the web3 game creator platform to strike a good balance between commercialization of creators and fan community atmosphere. For a long time, the gamefi track has been taking the platform project side and major ecology as the main output source and wealth leader of creation, and it is difficult for ordinary game creators to have sufficient funds to support their creation even if they have good ideas and designs, and it is difficult for them to be known by the public, and at the same time, it is difficult for them to get rich income in creation.

The proposal hopes to realize the commercialization needs of creators through NFT bonds, a trading model, while incentivizing the continued output of quality creative content. Instead, it can provide users with higher quality content services without compromising their experience. In addition, since users can participate in the creation process of the creators, the content produced by the creators completes the last stage of information dissemination - that is, not only does it receive reactions from the audience, but the audience can also participate in the output content, which is a two-way cycle that promotes the output of better quality content.

## Proposal Design

### 1) Credit system & credit bond

We will design a credit system for the NFT bond. The system will combine the historical activity record of the creator’s wallet address, the creator’s personal public information and other data for weighted combination calculation, which is conducive to solving the problem of NFT bond development and credit. In addition, users can also accumulate their own credit points through multiple transactions, which positively promotes the transaction cycle of financial products.

- The debentures will be designed to be split and mergeable.
- Each bond product will be marked with necessary information such as issuer information, maturity time, and collateral.
- Regarding the credibility of credit bonds, we plan to solve it through multi-signature wallets:

> Multi-signature wallet credit guarantee:
>
>
> Person 1 (creator): the main issuer of rights and interests
> Person 2 (Credit Intermediary): A very reputable person in the crypto market
> Person 3 (platform): the core team members of the platform
> Person 4 (xxxx): …

#### Example

The creator Mora issued an NFT bond product “NFT option-A” through this agreement. The product agreed that after one year (12 months), users who purchased the product can use this voucher to receive the NFT heroes in the game made by the creator Mora. At this point, fans who buy the product can get the principal and NFT heroes if they keep holding the bond until it expires.

---

The NFT bond can be further designed as an NFT option (Take delivery voucher), which becomes a financial contract that can be traded and mortgaged.

#### Example

The creator Mora sells the NFT option to fans, and this contract states that once the transaction volume of the game developed by her reaches $1,000, 000, 20,000 game tokens will be unlocked in January of the following year.

### 2) Creator credit profile

For each individual creator, we will designate them to use a fixed wallet address to create and trade NFTs (considering the cumulative design of the reputation point system), and creators with different reputation levels will unlock different reputation marks.

We will evaluate and score the creator’s on-chain behavior as a first-level judgment standard, and will also investigate their public accounts on Web2 social media platforms such as Twitter, Instagram, Facebook, Youtube (private domain accounts are also a kind of collateral) as a secondary judging criterion. Based on his/her address activity, we will also build a reward and punishment mechanism to maximize the protection of the asset safety and rights of NFT bond/option buyers.

> We will also strictly require creators to issue bonds, and set certain thresholds for issuing bonds.
> Eg: An address can issue bonds only when the number of active transactions and the amount of active transactions within a year reach a certain number.

### 3) Advanced: Equityization of NFT transaction fees

The proposal also plans to package the transaction fee of the NFT marketplace as an equity product.

## Positive Circular Value of NFT Bonds

#### Creators

Through NFT bondage, creators can not only accumulate private traffic and accurately operate fans, but also obtain new ways of monetization and increase revenue. Moreover, in the form of NFT bonds, creators can create original VIP DAOs for fans who buy bonds. In this private domain DAO, loyal fans can provide creators with more direct and effective feedback to help creators optimize their content.

#### Users/Fans

- Users can put forward content requirements for the creators, and even put forward opinions on the topic selection, and participate in the creators’ content production process.
- By purchasing NFT bonds/options, users can get more rights, and lock in future creator benefits (such as airdrops, whitelists, etc.) in advance.
- Based on the design of the credit system, users who buy more bonds can get higher credit points. This will be of great help to its unsecured lending and encrypted credit in the future.
- This NFT bond/option can be traded in the secondary market as a crypto financial product. Fans can bet on its future value-added space as a stable financial product to increase their investment portfolio returns.

#### Platform

The platform can provide standard templates for designing NFT bonds/options to help creators easily issue their own NFT financial products, while charging a certain fee as platform revenue. Through the fans absorption effect of creators, the platform itself can also gain more attention and usage, and form a complementary and mutually beneficial partnership with creators.

## Discussion points

- Whether it can capture enough users who trust the product (that is, how big is the demand market for users who accept the NFT bond/option)
- Whether the public can understand the reputation system of financial products, and whether they can understand the profit and equity model of the NFT product
- During the bear market of the crypto market, major capital investment actions are more cautious, whether the launch of this product can be recognized by the capital.

## Replies

**SpiderAres** (2022-09-14):

New updated:

### The main elements

· Gamefi NFT

· Royalty SFT: stands for Royalty interest

· NFT Marketplace

· SFT Marketplace (Powered by SOLV)

### System framework

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e46f8f1f58b340a8629fbb1179591ec6a72d903b_2_690x402.jpeg)image1234×720 37.9 KB](https://ethereum-magicians.org/uploads/default/e46f8f1f58b340a8629fbb1179591ec6a72d903b)

### Instructions

1. Royalty SFT is compatible with ERC3525, realizing mint SFT, claim revenue, (partially) transfer functions.Reference implementation:



      [github.com/solv-finance/erc-3525](https://github.com/solv-finance/erc-3525/blob/main/contracts/ERC3525Upgradeable.sol)





####

  [main](https://github.com/solv-finance/erc-3525/blob/main/contracts/ERC3525Upgradeable.sol)



```sol
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts-upgradeable/utils/ContextUpgradeable.sol";
import "@openzeppelin/contracts/utils/introspection/IERC165.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "./IERC721Upgradeable.sol";
import "./IERC3525Upgradeable.sol";
import "./IERC721ReceiverUpgradeable.sol";
import "./IERC3525ReceiverUpgradeable.sol";
import "./extensions/IERC721EnumerableUpgradeable.sol";
import "./extensions/IERC721MetadataUpgradeable.sol";
import "./extensions/IERC3525MetadataUpgradeable.sol";
import "./periphery/interface/IERC3525MetadataDescriptorUpgradeable.sol";
import {Initializable} from "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract ERC3525Upgradeable is Initializable, ContextUpgradeable, IERC3525MetadataUpgradeable, IERC721EnumerableUpgradeable {
    using Strings for address;
    using Strings for uint256;
```

  This file has been truncated. [show original](https://github.com/solv-finance/erc-3525/blob/main/contracts/ERC3525Upgradeable.sol)










1. Royalty Pool plays two roles: managing slot properties as slot manager; managing the revenue fund pool corresponding to each slot as Vault.
2. Royalty SFT records each tokenId corresponding to the amount of withdrawn:claimedAmount (prevents repeated withdrawals).
3. Royalty SFT value (amount of extractable royalties) Calculation rules: The total issued supply corresponding to each slot is fixed. The royalty amount corresponding to tokenId is calculated according to the total revenue corresponding to totalSupply and slot, and then the extracted part claimedAmount is deducted.
4. Royalty SFT addresses and Royalty Slot information are maintained in the NFT (collections and slots can also be maintained in the NFT Marketplace). Royalties generated by NFT transactions in the NFT Marketplace are directly transferred to Royalty Pool and recorded under the corresponding revenue of slot.
5. Royalty SFT is available for trading on the Solv SFT Marketplace.
6. NFT contract:

**a.** NFT multi-layer structure, based on the actual business logic to evaluate whether to adopt ERC998 (998 implementation is complex, the standard is not maintained may be abandoned). If all NFTS are in the same contract MINT, we can simplify the ERC998 data structure (propose a new EIP?).

**b.** Spanning Network: Centralized system, Axelar Network, Spanning Network.

1. To be added.

