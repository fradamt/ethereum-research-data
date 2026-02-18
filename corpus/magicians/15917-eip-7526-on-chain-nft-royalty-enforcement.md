---
source: magicians
topic_id: 15917
title: "EIP-7526: On-chain NFT royalty enforcement"
author: arrans
date: "2023-09-26"
category: EIPs
tags: [nft, royalties]
url: https://ethereum-magicians.org/t/eip-7526-on-chain-nft-royalty-enforcement/15917
views: 1282
likes: 2
posts_count: 10
---

# EIP-7526: On-chain NFT royalty enforcement

Discussion of a game-theoretic mechanism to induce truthful revelation of NFT sales and their value to allow for decentralised royalty enforcement.

## Replies

**Mani-T** (2023-09-27):

Game theory relies on creating incentives that encourage rational actors to behave in a desired way.  In this case, the goal is to induce truthful revelation of NFT sales and their values.

---

**highlander** (2023-09-29):

It is a combination of incentives and disincentives that ensures honest behavior because it either achieves a Nash equilibrium of winning strategies or in n-player collaborative games (which royalties would be), the Shapley value is non-zero. That is hard to enforce because players would have to commit to hidden values with stakes before they are revealed.

In an experimental setting interesting, in the real world with real money, a total no-go based on my experience with royalties over the last 15+ years.

---

**highlander** (2023-09-29):

Just use [EIP-4910](https://eips.ethereum.org/EIPS/eip-4910). Royalties are calculated, collected, and paid out to all relevant parties onchain. There is even a [reference implementation](https://github.com/treetrunkio/treetrunk-nft-reference-implementation) … try it out. You might like it ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**arrans** (2023-10-14):

Thanks [@highlander](/u/highlander), we’ll take a look at 4910.

> That is hard to enforce because players would have to commit to hidden values with stakes before they are revealed.

There are no such values in this proposal. Can you please elaborate?

---

**arrans** (2023-10-14):

The reference implementation you linked to entirely blocks [transferFrom()](https://github.com/treetrunkio/treetrunk-nft-reference-implementation/blob/a28747e0a9d3669b0f2d8faac44e61ab80b6e0ce/contracts/RoyaltyBearingToken.sol#L320) and [safeTransferFrom()](https://github.com/treetrunkio/treetrunk-nft-reference-implementation/blob/a28747e0a9d3669b0f2d8faac44e61ab80b6e0ce/contracts/RoyaltyBearingToken.sol#L328), which breaks expected behaviour of ERC721 tokens. Is this absolutely necessary for implementation of ERC-4910 or is it just in this particular implementation?

---

**highlander** (2023-10-14):

[@arrans](/u/arrans) in trustless multi-player games, there must be a commitment to an outcome that not everyone should know – a blinded commitment such as a Pederson or El-Gamal Commitment – and to which the player puts skin in the game through a stake. If the commitment is opened AFTER the game is done, then the stake is returned + a fee, typically, if the commitment matches the outcomes (correct royalty amount). If not, then the stake is slashed.

The construction avoids the nothing-at-stake problem in multi-player games.

---

**highlander** (2023-10-14):

That is intentional. When you read 4910, you see that in order to ensure not circumventing royalties, simple transfers from A to B cannot be allowed. 721 behavior is not designed for complex financial transactions – digital assets with residuals. As you will see in 4910, the owner of all NFTs is the contract and not the EOA/whitelisted smart contract – they are only approved. Because the contract must be aware of all buy/sell transactions and manage all applicable cash flows including royalties WITHIN the contract, not outside of it.

---

**arrans** (2023-10-16):

> in trustless multi-player games, there must be a commitment to an outcome that not everyone should know – a blinded commitment such as a Pederson or El-Gamal Commitment – and to which the player puts skin in the game through a stake. If the commitment is opened AFTER the game is done, then the stake is returned + a fee, typically, if the commitment matches the outcomes (correct royalty amount). If not, then the stake is slashed.

Can you please reframe this with respect to the proposal we’ve made? I’m having trouble understanding how it’s relevant but that may just be because you’re speaking more generally and I haven’t seen the connection. While I’m sure that *some* or even many multi-player games have the requirement you describe, that doesn’t mean that *all* of them must.

> The construction avoids the nothing-at-stake problem in multi-player games.

Our mechanism places the NFT itself at stake. The owner attributes some (hidden) value that we want them to reveal and, If they don’t, then they may lose the token (see *take-back* in the EIP), which is analogous to slashing in your description. If they reveal untruthfully then they stand to lose the token in return for a sum of ETH less than how much they value the token. While there is no direct analogy with your description, this is best characterised as “partial slashing”, relative to the degree of untruthful revelation. No blinded commitment is necessary.

As mentioned in the `Rationale` section, a yellow paper will be made available before moving the EIP into `Review`. This will fully analyse the strategies.

> When you read 4910, you see that in order to ensure not circumventing royalties, simple transfers from A to B cannot be allowed.

Full compliance with ERC721 is a strict requirement for us, including permissionless transfers, so ERC4910 is unfortunately insufficient for our needs.

---

**SamWilsn** (2024-05-16):

How would this proposal defend against an owner wrapping the NFT in another NFT, and transferring the wrapper around? Seems like you would only have to pay royalties twice?

---

How similar is this concept to [Harberger Taxes](https://en.wikipedia.org/wiki/Harberger_Tax)? I think I’ve seen an EIP somewhere that used those to similar effect.

