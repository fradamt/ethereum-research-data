---
source: magicians
topic_id: 10551
title: EIP-5553 - Representing intellectual property on chain with Royalty Portions
author: royo
date: "2022-08-28"
category: EIPs
tags: [nft, royalties, licensing]
url: https://ethereum-magicians.org/t/eip-5553-representing-intellectual-property-on-chain-with-royalty-portions/10551
views: 2131
likes: 0
posts_count: 4
---

# EIP-5553 - Representing intellectual property on chain with Royalty Portions

Hey folks.

Proposing a standardized way to represent intellectual works on chain, along with a refined royalty representation mechanism and associated metadata. This standard is not associated with a specific type of work and could represent many types of works such as musical works, videos, books, images and more.

The standard is kept very generic on purpose to allow the industry to evolve new ecosystems that can all rely on the same basic standard at their core



      [github.com](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-5553.md)





####



```md
---
eip: 5553
title: Representing IP and its Royalty Structure
description: A way of representing intellectual property and its respective royalty structure on chain
author: Roy Osherove (@royosherove)
discussions-to: https://ethereum-magicians.org/t/eip-5553-representing-intellectual-property-on-chain-with-royalty-rights/10551
status: Review
type: Standards Track
category: ERC
created: 2022-08-17
requires: 20, 721
---

## Abstract
This proposal introduces a generic way to represent intellectual property on chain, along with a refined royalty representation mechanism and associated metadata link. This standard is not associated with a specific type of IP and could represent many types of IP, such as musical IP, videos, books, images, and more.
The standard is kept very generic to allow the industry to evolve new ecosystems that can all rely on the same basic standard at their core.

This standard allows market participants to:
1) Observe the canonical on-chain representation of an intellectual property
2) Discover its attached metadata
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-5553.md)

## Replies

**royo** (2022-08-28):

This standard allows market participants to:

```
Observe the canonical on-chain representation of an intellectual work
Discover its attached metadata
Discover its related royalty rights holders
In the future, this will enable building registration, licensing and payout mechanisms for intellectual property assets.
```

---

**royo** (2022-08-28):

There is no accepted standard mechanism to license a work, or to represent it, except using traditional NFTs. But regular NFTs only represent a collectible item use case, and cannot easily represent more complicated use cases of licensing a work for different types of uses. To enable such mechanisms, we need a more robust mechanism for :

```
Declaring that a work exists, SEPARATE from its purchase ability
Declaring possibly multiple interested parties to be paid for such work
```

for #1 no standard exists today. For #2 we only have regular splits standards based on NFT purchases, or through mechanisms like 0xsplits. While these are a great headstart, they do not contain the ability to name multiple types of collaboration participants, and more importantly, do not contain an easy way to manage the splits in a way that feels natural.

With this proposal, registration is taken care of, and splits are taken care of by defining the splits as an open array of EIP-20 tokens that represent split percentages. Moving splits to various participants will be as simple as sending an EIP-20 token from one wallet to another. discovering split movements is as simple as checking EIP-20 transfer events.

In the future, we can build full payout mechanisms based on these simple split tokens, and licensing standards on top of those payout mechanisms, which are not possible today due to the complexity of splits management in the traditional web2 world.

---

**royo** (2022-08-30):

A thought: This could also fit well with EIP-2158, in that a payment for a license can be distributed to holders of the royaltyinterestTokens() holders.



      [github.com](https://github.com/royosherove/EIPs/blob/master/EIPS/eip-5218.md)





####



```md
---
eip: 5218
title: NFT Rights Management
description: An interface for creating copyright licenses that transfer with an NFT.
author: James Grimmelmann (@grimmelm), Yan Ji (@iseriohn), Tyler Kell (@relyt29)
discussions-to: https://ethereum-magicians.org/t/eip-5218-nft-rights-management/9911
status: Draft
type: Standards Track
category: ERC
created: 2022-07-11
requires: 721
---

## Abstract

The following standard defines an API for managing NFT licenses. This standard provides basic functionality to create, transfer, and revoke licenses, and to determine the current licensing state of an NFT. The standard does not define the legal details of the license. Instead, it provides a structured framework for recording licensing details.

We consider use cases of NFT creators who wish to give the NFT holder a copyright license to use a work associated with the NFT. The license can optionally be revoked under conditions specified by the creator. The holder of an active license can issue sublicenses to others to carry out the rights granted under the license.
```

  This file has been truncated. [show original](https://github.com/royosherove/EIPs/blob/master/EIPS/eip-5218.md)

