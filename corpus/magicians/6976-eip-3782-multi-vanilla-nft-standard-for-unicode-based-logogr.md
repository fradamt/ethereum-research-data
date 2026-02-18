---
source: magicians
topic_id: 6976
title: "EIP-3782: Multi vanilla NFT standard for unicode-based logographic representation (deprecated)"
author: maxareo
date: "2021-08-30"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-3782-multi-vanilla-nft-standard-for-unicode-based-logographic-representation-deprecated/6976
views: 1034
likes: 0
posts_count: 3
---

# EIP-3782: Multi vanilla NFT standard for unicode-based logographic representation (deprecated)

## Abstract

A vanilla non-fungible token standard proposed by [EIP-3754](https://github.com/ethereum/EIPs/issues/3753) combined with the established [unicode](https://home.unicode.org/) system can create an on-chain logographic system for representing language characters that are logographs. Examples include *hanzi* in Mandarin, *kanji* in Japanese, *hanja* in Korean, and etc.

## Motivation

A logograph is a written character that represents a word or morpheme, whereas a unicode is an information technology standard for the consistent encoding, representation, and handling of texts. A vanilla NFT by EIP-3754 can naturally combine the two into a new system that is ideal for on-chain representation of the logograpic language systems.

## Applications

On-chain chatting, blogs, micro-blogs systems can be built for communities using these languages with this new standard.

## Replies

**maxareo** (2021-08-30):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/3782)












####



        opened 06:08AM - 30 Aug 21 UTC



          closed 03:08AM - 06 Feb 23 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/8/8e5f7cce79e8b354fabb18a6c173307bb6d52dc4.jpeg)
          simontianx](https://github.com/simontianx)





          discussions-to







## Abstract
This standard introduces a smart contract interface that can repres[…]()ent a batch of non-fungible tokens of which the ordering information shall be retained and managed. Such information is particularly useful if `tokenId`s are encoded with the sets of `unicode`s for logographic characters and emojis. As a result, NFTs can be utilized as carriers of meanings.

## Motivation
Non-fungible tokens are widely accepted as carriers of crypto-assets, hence in both [ERC721](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-721.md) and [ERC1155] https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1155.md), the ordering information of multiple NFTs is discarded. However, as proposed in [EIP-3754](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3754.md), non-fungible tokens are thought of as basic units on a blockchain and can carry abstract meanings with unicoded `tokenId`s. Transferring
such tokens is transmitting an ordered sequence of unicodes, thus effectively transmitting phrases or meanings on a blockchain.

This standard aims to combine the two and introduce the necessary functionalities for batch transfer and representation of logographic characters. As a result, a language system can be built on-chain for logograpic languages.

For non-logographic languages such as English, although the same standard can be applied, the marginal utility is minimal to be practically useful. However, for logographic languages, since a rich amount of meanings can be transmitted in just a few characters, this standard is therefore particularly valuable. Emojis are similar with logographs and can be included as well.

A motivating example is instead of sending the two Chinese characters of the Great Wall `长城`, two NFTs with IDs `#38271` and `#22478` respectively can be transferred in a batch. The two IDs are corresponding to the decimal unicode of the two characters. The receiving end decodes the IDs and retrieves the original characters. A key point is the ordering information matters in this scenario since the tuples `(38271, 22478)` and `(22478, 38271)` can be decoded as `长城` and `城长`, respectively, and both are legitimate words in the Chinese language. This illustrates one key difference between this standard and ERC1155.

In-game characters, weapons, items can be represented by very few characters. Examples include `关羽` `(20851, 32701)` a famous fighter, `剑` `(21073)` a sword, `药水` `(33647, 27700)` a potion, and etc. On-chain gaming dapps can be largely enriched with elements by simply adopting this standard for players using logographic languages.

Besides, in the eastern Asian culture, characters are sometimes considered or practically used as gifts in holidays such as Spring Feastival, and etc. The characters `恭喜发财` or `(24685, 21916, 21457, 36001)` can be literally sent as a gift to express the best wishes for financial prosperity. That said, logographs do possess the nature of an asset, which is well resembled by this standard.

What is even more interesting is in that culture, people consider ancient teachings as treasures which are usually written in a concise way such that a handful of characters can unfold a rich amount of meanings. Modern people now get a reliable technical means to pass down their words, poems and proverbs to the future generations by sending tokens.

Other practical and interesting applications include Chinese chess, wedding vows, family generation quotes and sayings, funeral commendation words, prayers, anecdotes and etc.

---

**maxareo** (2021-10-02):

This one has been renamed as [EIP-4341](https://github.com/simontianx/EIPs/blob/master/EIPS/eip-4341.md).

