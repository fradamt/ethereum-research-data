---
source: magicians
topic_id: 9217
title: ENS bounded Non-transferable NFTs
author: aditya0212jain
date: "2022-05-10"
category: EIPs
tags: [ntt]
url: https://ethereum-magicians.org/t/ens-bounded-non-transferable-nfts/9217
views: 1355
likes: 8
posts_count: 5
---

# ENS bounded Non-transferable NFTs

Non-transferable NFTs/Tokens (hereafter referred to as NTTs for convenience) have been discussed at length in multiple EIPs[1][2][3][4] and Vitalik’s Soulbound post[5]. All the EIPs consider the NTTs as bounded to a crypto wallet address. However, I think there are two problems with that approach:

1. People might want to migrate their assets from one wallet to another due to various reasons, for example: in case of compromise, rotating private keys, etc.
2. Some people may create dummy wallets to store the NTTs and sell that wallet itself. This would defeat the purpose of the whole credential use case of NTTs.

Some of the implementations in the mentioned EIPs do talk about the reassignment of the NTT at the discretion of the owner of the contract to tackle the 1st problem but I am not sure how effective that would be since convincing the owner of the contract that the wallet in which to transfer the NTT is also owned by the same current owner of the NTT should be difficult.

This brings us to the current topic of discussion: what if we bind an NTT to the ENS of a user as also mentioned in Vitalik’s post[5] i.e. NTTs owned by ENS domain names and not wallet addresses. This would solve the 1st problem since people can change as many wallets as they want as long as they have the domain name with themselves the NTTs will be theirs. And it would mitigate the 2nd problem to some extent assuming that people would not want to trade their ENS domain names as easily as their crypto wallet address.

On the implementation side, this is what I think:

ENS domain names can not be assigned as owners of any ERC20/ERC721/ERC1155 token because they do not have any unique public address. So none of the existing interfaces can be used to create the above-mentioned NTTs. This I think would mean that wallets/marketplaces would not have the support to show these NTT right away but they can implement the new standard if they want.

The goal of this topic is to discuss whether such a standard is needed and can benefit users and the technical challenges in implementing it.

cc: [@dtedesco1](/u/dtedesco1)

References:

[1] https://ethereum-magicians.org/t/eip-4974-fungible-non-tradable-tokens-or-exp/8805

[2] https://ethereum-magicians.org/t/eip-4973-account-bound-tokens/8825

[3] https://ethereum-magicians.org/t/eip-4671-non-tradable-token/7976

[4] https://github.com/ethereum/EIPs/issues/1238

[5] https://vitalik.ca/general/2022/01/26/soulbound.html

## Replies

**toledoroy** (2022-05-16):

Well. Short answers is that

1. a central entity (contact owner) might still have the ability to transfer the tokens.
2. You can’t really sell private keys because there’s no way to make sure that the seller has fully forgotten the keys,

---

**carlosdp** (2022-05-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/toledoroy/48/5677_2.png) toledoroy:

> You can’t really sell private keys because there’s no way to make sure that the seller has fully forgotten the keys,

fwiw, that’s not actually true. I can imagine one scenario right now: Multi-Party Computation based keys (like the ones used in Fireblocks). Since transactions are signed by multiple parts with one part in the hands of an entity that respects a ruleset, it’s possible to “sell” a private key and guarantee it can’t be used by the original seller.

There are decentralized versions of this solution in development too, like Entropy.

---

**dcposch** (2022-05-16):

This makes a ton of sense.

ENS is already surprisingly widespread, to the point where I think it’s a Schelling point for identity.

One data point. Here are the most popular NFTs on an experimental Ethereum-based social network.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/9/93733c4b9c5ee3d976099cb2a25d99796aaadb08_2_426x499.jpeg)image1188×1392 135 KB](https://ethereum-magicians.org/uploads/default/93733c4b9c5ee3d976099cb2a25d99796aaadb08)

ENS is the most popular by a factor of 4! Most active users already have one.

It has nice properties, too. Like domain names, some ENS are more sellable than others. For example, if you own schellingpoint.eth, that’s a company or a placeholder for a project and can be sold. If I own dcposch.eth, it doesn’t make sense to sell, or for anyone else to buy, unless they have the same name as I do. My own name is inherently more valuable to me than to anyone else.

This maps well onto the soulbound concept. Some things that are “soulbound” *should* transfer with a company or brand. For example, reviews for an online store. You should not be able to buy review points from someone else’s store, but you *can* buy the whole store. In that case, the brand (ENS) and reputation (SBTs) come with it.

Other soulbound tokens should stick with an individual, and ENS facilitates that as well. There is a great chance that vitalik.eth will one day point to a different address (say, once a contract wallet standard emerges). When that happens, any reputation / SBTs should stay with Vitalik.

---

**toledoroy** (2022-05-17):

Nothing is a 100% secure.

You can always give your driver license to your identical twin ![:stuck_out_tongue_winking_eye:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue_winking_eye.png?v=12)

This is why a reputation system is such an important part of this whole operation.

