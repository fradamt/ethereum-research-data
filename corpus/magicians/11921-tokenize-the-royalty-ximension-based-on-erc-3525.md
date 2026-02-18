---
source: magicians
topic_id: 11921
title: Tokenize the Royalty - ‘Ximension’ based on ERC-3525
author: SpiderAres
date: "2022-11-29"
category: ERCs
tags: [nft, token]
url: https://ethereum-magicians.org/t/tokenize-the-royalty-ximension-based-on-erc-3525/11921
views: 1247
likes: 1
posts_count: 3
---

# Tokenize the Royalty - ‘Ximension’ based on ERC-3525

**ERC-3525** is a general-purpose and omni-asset standard that combines the quantitative attributes of an ERC20 token and the descriptive features of an ERC721 token (NFT). It is the most advanced digital representation of ownership, value, rights, status, and identity.

The royalty of an NFT collection is non-transferable and non-tradeable. However, by taking advantage of ERC3525, royalties are feasible to be tokenized, shared with contributors and communities, or served as collaterals. The state-of-the-art tokenized asset is, what we would call, the ‘predictable cashflow certificate’.

In summary, ‘predictable cashflow certificate’ has the following two features

- tokens represent shares of the project, which can be held to gain income with the market value of the platform/project.
- tokens represent shares of the project, which can be held to enjoy the income from the platform/project dividends.

At the specific code level, our contract architecture is shown in the following diagram.

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/1/172f69a61da0e61f9b22bcea7b79411dfd69020a_2_507x290.jpeg)1600×917 81.3 KB](https://ethereum-magicians.org/uploads/default/172f69a61da0e61f9b22bcea7b79411dfd69020a)

Now let’s break down the overall architectural design of this project, and the functional features of each contract.

**`'Ximension' Factory`**

Used as a factory contract to generate ‘predictable cashflow certificate’. It has two main functions.

1. Generate a new ‘Ximension’ project Token.
2. Enquiry whether the Token is generated based on this factory schema.

**`'Ximension'`**

A single contract based on the ERC3525 ‘predictable cashflow certificate’ project, which consists of 3 internal modules and 1 external module.

The internal modules are:

1. ERC3525, providing EIP3525-compliant functional Tokens.
2. Vault, the vault contract, used to access Native Token and calculate users’ earnings information.
3. VaultConfig, the vault configuration contract, provides information related to the creator’s configuration project.

The external modules are:

1. Platfrom, used to store platform information and related security measures globally.

**`ERC3525`**

With the contractual implementation of ERC3525, it has a unique slot and value features to provide broader financial application scenarios. In addition to its own functionality, the extensions in the project are as follows.

1. Project initialization functions.
2. Splitting and combining tokens and tying them to their share and gain collection.
3. Adding/removing slot whitelists.

**`Vault Contract`**

As a vault management center, it mainly carries out the collection and distribution of ‘predictable cashflow certificate’ proceeds held by users. It has the following functions:

1. User withdrawals.
2. Wallet-type contracts with deposit/withdrawal of funds.
3. Confirm the tokens available for withdrawal by the user.
4. Confirm the tokens the user has withdrawn.
5. Querying user extraction information.
6. Re-entry security lock.
7. Safe handling accurately.
8. Distribution of the fee which the platform and creators enjoy.

**`VaultConfig Vault Configuration Contract`**

It is mainly used to configure information about the creators of this vault, presenting relevant messages to the public in an open and transparent form. The following functions are available.

1. Configuring the creator’s address.
2. Configuring creator incentive rates.
3. Related rights management functions.

As the above modules together constitute the main features of a ‘predictable cashflow certificate’, users hold a ‘predictable cashflow certificate’ to enjoy share gains while also enjoying the gains from the growth of the platform. It is a new blockchain financial model that is more beneficial for holders/creators to enjoy their own rights and interests.

> Reconfiguration of business scenarios based on the above solutions, especially in NFT, Gamefi, etc.

**1、Royalty scenario**

1. Royalty incentives for their own community, creators or creators’ studio can be designed from the mechanism of the creative link, such as A as a painter to complete the creation of layers, B as a stencil artist to complete the visual design of the nft.
In the process of division of labor, They make an appointment to the distribution ratio of royalties and submit the corresponding metadata, everyone in accordance with the division of labor and the negotiated vouchers held to receive royalties or trade royalty income rights.
2. To offer the possibility of buying and selling projects.

The past project buying and selling relies on receiving address updates or delegating to a trusted platform for settlement, however these solutions are not essentially the full link of onchain, based on Ximension proposed solution offers the possibility of on-chain project trading. The trading platform scenario, the tournament scenario works equally well.

**2、Based on this extension out of the new organizational structure form**

In the original ERC721 or ERC20 organizational incentive structure, it can be clearly found: ERC20 as a token, means that only one person can sell to the highest point, in a zero-sum game incentive model, while ERC721 due to its non-homogeneity, resulting in weak consensus, while based on the ERC3525 organizational model and in the above solution elaboration, it can be found that introducing an organizational structure based on ‘predictable cashflow certificate’ is more operative both in terms of incentives and division of labor and is a positive-sum game.

**3、Related ecological opportunities**

'predictable cashflow certificate’bot, ‘predictable cashflow certificate’'s on-chain browser and ‘predictable cashflow certificate’'s collaboration tools or ‘predictable cashflow certificate’'s use of community are currently the more promising ecological opportunities. Relevant introductions will be introduced in subsequent articles.

## Replies

**SpiderAres** (2022-11-30):

The Github repository link : [GitHub - kasodesyn/DimensionX-3525-application-fork](https://github.com/kasodesyn/DimensionX-3525-application-fork)

---

**kasodesyn** (2022-12-01):

Great innovation! It is expected that the project will be implemented and everyone can use it.

