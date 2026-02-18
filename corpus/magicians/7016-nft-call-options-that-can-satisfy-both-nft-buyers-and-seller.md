---
source: magicians
topic_id: 7016
title: NFT call options that can satisfy both NFT buyers and sellers(creators)
author: maxareo
date: "2021-09-07"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/nft-call-options-that-can-satisfy-both-nft-buyers-and-sellers-creators/7016
views: 1425
likes: 1
posts_count: 8
---

# NFT call options that can satisfy both NFT buyers and sellers(creators)

Currently, NFT creators have difficulty setting up initial prices and NFT buyers have the fear of missing out good NFTs. A mid-layer can be added between the two sides by minting ERC3754 NFTs as rights to purchase NFTs. NFT creators can presale such rights at lower prices and hence are able to set the initial prices higher. For NFT buyers, buying such rights is a small commitment and can sell them if they do not like the NFTs minted later on. The rights are made liquid by EIP-3754.

Such right can be best understood as a call option on an NFT. Effectively, this is a market making layer by reducing the bid-ask spread.

Would love to hear your thoughts. Thanks!

## Replies

**norswap** (2021-09-13):

What avoids a gold rush on the call options instead of the current gold rush on the NFTs themselves?

---

**maxareo** (2021-09-14):

Call options provide owners the right but not obligation to exercise the right of buying the underlyings. Hence, call options encourage risking less capital in gold rush on the NFTs themselves.

---

**norswap** (2021-09-14):

Fair, I was coming at this from the perspective that the main issue with NFT drops was the congestion it caused in the chain. (And that the price issue you highlighted was that drops where priced too low, which caused this gold rush.)

---

**Hay-sharptech** (2021-09-14):

The fuel of the “gold rush” which is the low price cannot be taken away as this is the main reason for the explosion in the NFT market place. Attempt to increase price will ground the boom as gas price is already doing justice to this.

---

**maxareo** (2021-09-15):

The idea of an option is to lock the opportunity of getting an NFT at an even lower price. The value-add is this is achieved at no cost of the token creators, since the creators can set the initial sale price higher. The exact conversion between an option and an NFT needs some calculated design though.

---

**maxareo** (2021-09-15):

A Solidity implementation of the NFT option idea can be found [here](https://github.com/simontianx/ERC3754/blob/main/contracts/NFTOption.sol).

---

**AndersonTray** (2021-12-16):

The NFTs by this standard aspire to be acknowledged and known as expressing abstract ownership, as they are already widely accepted and known as reflecting ownership of digital goods. This is accomplished by enabling and encouraging the creation of abstraction layers on top of them. Having the rights to perform functions allocated to such tokens is similar to owning such NFTs. This tokenization also facilitates the transfer of such rights. To differentiate this standard from [ERC-721], data fields and functions related to but is that *, when gas prices are high, minting an NFT, can cost an artist a tidy sum in Etheruem *. As a result, if you need to mint a large number of NFTs, this contract isn’t the best option. while im on it I just want to share a game called [cryptospacegame](https://www.ruju1978.com/), I know some of you have a family i’ve been playing this with them, its a board game that is very fun, I enjoyed having time with my family and also earn at the same time.  back to the topic, your idea about this is pretty cool I think it should be put to also reduce the chance of price getting lower

I’m sorry if I didn’t answer your question I’m just sharing my thoughts and knowledge

