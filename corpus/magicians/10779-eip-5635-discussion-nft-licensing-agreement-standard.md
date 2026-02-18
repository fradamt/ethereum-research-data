---
source: magicians
topic_id: 10779
title: "EIP-5635 Discussion: NFT Licensing Agreement Standard"
author: 0xTimi
date: "2022-09-09"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-5635-discussion-nft-licensing-agreement-standard/10779
views: 2400
likes: 0
posts_count: 7
---

# EIP-5635 Discussion: NFT Licensing Agreement Standard

https://github.com/ethereum/EIPs/pull/5635

## Replies

**0xTimi** (2022-09-09):

## Motivation

In general, some creators of NFTs will transfer intellectual property (IP), commercial, and exclusive licensing rights to the individual NFT holders. This enable NFT owners to create artworks and products by themselves. However, currently there isn’t a standardized and clear way in which NFT owners are able to grant others rights of recreating derivative works based on their owned NFT.

This standard allows the NFT owner, knowns as “Licensor”, to have a standardized way to signal a licensing agreement to re-creators, knowns as “Licensee”, in exchange for an agreed payment, known as a “Royalty”.  With this licensing agreement,  the licensee has the right to recreate relevant dNFTs which clearly declare the authorized agreements.  Meanwhile, this declaration should be able to be verified by a creditable decentralized **Registry** service at any given time.  In such way,  the licensing royalty payment can be paid to licensors every time dNFT is sold or re-sold as regulated by the agreement. Taking the moment when the dNFT is minted as the cut-off point, the stage before is called the **Licensing** stage, and the subsequent stage is called the **Discovery** stage.

This standard defines the **Licensing** as a loose and optional interface, but the **Discovery** as a strict and compulsory interface. The reason here is that, no matter how the licensing agreement is licensed via a **Registry**, the most important thing is that marketplaces and application can adopt a  unified interface to discover and verify these agreements.

To be specific, to support standard **Discovery**,

1. dNFT must implement authorizedBy() interface to return a list of

- the credential which represent the authorized licensing agreements .
- the address of  Registry contract which issued the credential.

1. The credentials can be verified by Registry at any anytime where verification includes:

the oNFT contract and ID
2. Licensor
3. validity of license / expiry date
4. date of signature
5. licensing agreement identifier similar to SPDX-License-Identifier: MIT
6. licensing agreement uri
7. type of licensing agreement

Non-Exclusive   // default
8. Exclusive
9. Sole
10. scopes, e.g.  artworks // TODO: in discussion

*To implement an practicable **Licensing**, two recommend options are proposed in the **Specification** section. The first is that both the licensor and the licensee sign the license agreement at the same time. The second is that the licensor release the licensing agreement first, and then sells the licensing agreement to the licensee through auction or resale. A **Registry** can also use other mechanism to implement **Licensing** as long as it can fairly support the validation of licensing agreements following the standard **Discovery** as mentioned before.*

It is worth noting that an infringing **dNFT** may forge a credential with a faked **Registry**, where the faked **Registry** offers a forged verification for the infringing **dNFT**. In order to avoid this problem, marketplaces/applications must be sure that is a reliable **Registry** , e.g.  which is in a creditable list  or double checked by a reliable oracle service.

Without an licensing agreement standard, the NFT ecosystem will lack an effective means to verify whether an NFT derivative work is licensed or not, original NFTs’ owners will not receive ongoing licensed fee they deserve,  recreators cannot clearly know ehether they are entitled to perform derivative creations, and NFT marketplaces aren’t able to distinguish licensed derivative works from unauthorised ones so that it is hard to ward off infringements. This will hamper the growth of NFTs, damage the interests of the NTF owners, and demotivate recreators from minting new and innovative derivatives.

Enabling all NFT ecosystem to unify on a single licensing agreement standard will benefit the entire NFT ecosystem.

While this standard focuses on NFTs and compatibility with  ERC-721, ERC-1155 and EIP-2981 standards, EIP-56XX does not require compatibility with ERC-721, ERC-1155 and EIP-2981 standards. Any other contract could integrate with EIP-56XX to return licensing agreement information. ERC-56XX is, therefore, a universal licensing agreement standard for many asset types.

---

**Origenes** (2022-09-26):

The proposal is definitely brilliant! Looking forward to the changes

---

**Jamesjl** (2022-09-26):

Appreciate the ideas. Defining licensing interface as optional and discovery interface as compulsory is a good design. Adaptable to more use cases. Wonder if these dNFT can be chained. Like one dNFT based on another dNFT?

---

**Vanessa-Y** (2022-09-26):

Like the idea of scopes in the credentials as it provides flexibility to support different types of IP. Also the discovery interface helps tracking the source of derivative NFT. This provides a solution of IP generation and verification, and could potentially be the bedrock for NFT IP market. Nice work.

---

**pxrv** (2022-09-29):

Would love to start working on a draft implementation if you could provide an interface

---

**0xArtherius** (2023-05-09):

What happened to this proposal?

