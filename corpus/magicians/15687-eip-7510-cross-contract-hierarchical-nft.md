---
source: magicians
topic_id: 15687
title: "EIP-7510: Cross-Contract Hierarchical NFT"
author: minkyn
date: "2023-09-06"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-7510-cross-contract-hierarchical-nft/15687
views: 1833
likes: 4
posts_count: 9
---

# EIP-7510: Cross-Contract Hierarchical NFT

Hi Magicians,

I’d like to introduce a new extension to ERC-721 standards. It proposes a way to maintain hierarchical relationship between tokens from different contracts. This standard provides an interface to query the parent tokens of an NFT or whether the parent relation exists between two NFTs.

Existing ERC-6150 has a similar feature, but it only builds hierarchy between tokens within the same contract. More than often we need to create a new NFT collection with the derivative tokens. For example, a 2D NFT image would like to publish its 3D model as a new derivative NFT. In addition, deriving from multiple parents is very common in the scenario of IP licensing. Such cases include a movie NFT featuring multiple characters from other NFTs. But the existing standard doesn’t support that either.

For details, please see the submitted pull request:

https://github.com/ethereum/EIPs/pull/7638

Looking forward to the feedback from the community!

## Replies

**Mani-T** (2023-09-06):

Nice idea. It addresses scenarios where tokens need to be organized hierarchically across multiple collections. Meanwhile, hierarchical relationships can also facilitate metadata management.

---

**fayang** (2023-09-07):

We’ve developed an online service for BAYC and Doodles owners, allowing them to sculpt 3D models ([3D BAYC](https://www.comoco.xyz/series/bayc)) for their NFTs. What sets our work apart is our focus on maintaining the derivative relationship between the parent and children NFTs. We’ve integrated the principles outlined in EIP-7510 into our solution.

In practice, this means that our service not only generates 3D models but also ensures these derivative NFTs maintain a clear and traceable connection to their parent NFTs with our smart contract implementation([Comoco Licensor](https://www.comoco.xyz/smart_contract)). This aligns with the broader goals of the NFT community in establishing transparent and verifiable derivative relationships.

---

**fayang** (2023-09-07):

And [3D Doodles](https://www.comoco.xyz/series/doodles-official)

---

**stoicdev0** (2023-09-13):

Have you checked [ERC-6059: Parent-Governed Nestable Non-Fungible Tokens](https://eips.ethereum.org/EIPS/eip-6059)? It’s on final state and it solves the same problem in a much more complete way.

---

**minkyn** (2023-09-14):

That is a very interesting idea. I would imagine it would be useful for an existing NFT holder who wants to have all its derivative assets bundled together.

However, it’s not applicable for the scenario this proposal is trying to address, which is the most common way of IP licensing. Take Disney for example, it wants to license its IP to different toy manufacturers, but won’t be any owner of such toys. Instead, all those derivative assets can have their separate owners and be traded normally in the marketplace. Disney only takes the role of collecting royalties from the trading of those derivatives.

Back to the NFT world, this proposal follows the same protocol. Derivative NFTs are not *bundled* to the original NFTs. They are *linked* instead, via interfaces defined in this proposal. And it is up to the application to define the behavior that comes with this link, usually related to royalties.

---

**stoicdev0** (2023-09-14):

Thanks for the answer!

It wasn’t clear to me that this was about licensing, the name suggests directly what 6059 does. I agree that it is different under this point of view, since 6059 requires parents to have full ownership of their children.

---

**drllau** (2024-01-10):

This EIP/ERC labelnum is breaking all sorts of links. The ERC-7510 is [here](https://github.com/ethereum/ERCs/blob/master/ERCS/erc-7510.md). Some thoughts …

- are you postulating simple partOf or hasComponent relationships
- or is it going to be a richer tree analogous to VRML where you apply transformations/compositions?
- licensing … the general rule is unless there is sufficiently transformative work, you cannot sublicense more powers than originally granted … so what set of rights are being negotiated? (eg limited edition as might be case for short-run metaverse items).

---

**minkyn** (2024-01-10):

Your questions have been addressed in the previous threads, if you read carefully. Examples were also given.

