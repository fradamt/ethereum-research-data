---
source: magicians
topic_id: 7187
title: "EIP-4341: Unicoded NFT Standard"
author: maxareo
date: "2021-10-02"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-4341-unicoded-nft-standard/7187
views: 986
likes: 5
posts_count: 4
---

# EIP-4341: Unicoded NFT Standard

## Abstract

Simple on-chain communication between EOAs is made possible by transferring [EIP-3754](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3754.md) NFTs with unicoded tokenIds in a batch as proposed in this standard. This is particularly efficient and useful for emojis and languages that are based on **[logographs](https://en.wikipedia.org/wiki/Logogram)** . Examples include *hanzi* in Mandarin, *kanji* in Japanese, *hanja* in Korean, and etc. Many more applications are opened up for speakers of these languages as by-products.

## Motivation

Currently for a blockchain system, communication between two accounts when at least one of the two is a smart contract is possible, however, direct and meaningful communication between two EOAs is not so straightforward. This standard aims to fill in the missing part.

A logograph is a written character that represents a word or morpheme, whereas a unicode is an information technology standard for the consistent encoding, representation, and handling of texts. A vanilla NFT by [EIP-3754](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3754.md) with `tokenId` being specified as a certain unicode can be used to represent a logograpic character on-chain. This standard aims to combine the two and introduce the necessary functionalities for batch transfer and representation of vanilla NFTs. As a result a new language system can be opened up for on-chain representation of logograpic languages.

This is particularly valuable for logographs because a rich amount of meanings can be transmitted in just a few characters. For non-logographic languages, although the same unicode standard can be applied, it is not providing significant additional utility to be practically useful. Emojis are similar with logographs and can be included as well.

A motivating example is instead of sending the two Chinese characters of the Great Wall `长城`, two EIP-3754 tokens with ID`#38271` and ID`#22478` that are the corresponding decimal unicodes can be sent. The receiving end decodes the IDs and retrieves the original characters. A key point is the ordering information matters in this scenario since the tuples `(#38271, #22478)` and `(#22478, #38271)` mean `长城` and `城长`, respectively, and both are legitimate words in the Chinese language.

Besides, in the eastern Asian culture, characters are sometimes considered or practically used as gifts in holidays such as Spring Feastival, etc. `(#24685, #21916, #21457, #36001)` `恭喜发财` can be used literally as a gift to express the best wishes for financial prosperity. That said, logographs do possess

the nature of an asset, which is well resembled by this standard.

What is even more interesting is in that culture, people consider ancient teachings, poems and proverbs as treasures which are usually written in a concise way such that a handful of characters can unfold a rich amount of meanings. Modern people now get a chance to speak to the future generations by sending tokens.



      [github.com/simontianx/EIPs](https://github.com/simontianx/EIPs/blob/master/EIPS/eip-4341.md)





####

  [master](https://github.com/simontianx/EIPs/blob/master/EIPS/eip-4341.md)



```md
---
eip: 4341
title: Ordered NFT Batch Standard
description: The ordering information of multiple NFTs is retained and managed
author: Simon Tian (@simontianx)
discussions-to: https://github.com/ethereum/EIPs/issues/3782
status: Draft
type: Standards Track
category: ERC
created: 2021-10-01
---

## Abstract
This standard introduces a smart contract interface that can represent a batch
of non-fungible tokens of which the ordering information shall be retained and
managed. Such information is particularly useful if `tokenId`s are encoded with
the sets of `unicodes` for logographic characters and emojis. As a result, NFTs
can be utilized as carriers of meanings.

## Motivation
```

  This file has been truncated. [show original](https://github.com/simontianx/EIPs/blob/master/EIPS/eip-4341.md)

## Replies

**abcoathup** (2021-10-04):

If I understand correctly this EIP is to standardize using a subset of unicodes in a specific order to create phrases.

Are phrases unique in a contract?  If there isn’t a uniqueness constraint on phrases per contract, could this be done in a single contract?.

As an aside, there was a recent NFT project of unicode characters.



      [twitter.com](https://twitter.com/nicksdjohnson/status/1436809373125201920)



    ![image](https://pbs.twimg.com/profile_images/1758137158765105152/FtdJVxgx_200x200.jpg)

####

[@nicksdjohnson](https://twitter.com/nicksdjohnson/status/1436809373125201920)

  Have you always wanted to own 'x'? Does the idea of possessing '😂' appeal? Introducing Unicode (for Geeks). All 143,859 Unicode characters, as NFTs. Free to mint!

https://t.co/oU6rUCU0PB

  https://twitter.com/nicksdjohnson/status/1436809373125201920

---

**maxareo** (2021-10-04):

Hey [@abcoathup](/u/abcoathup), thanks for the questions and info.

Lately I came to realize a bigger problem that there is a lack of direct and meaningful communication between any pair of EOAs can be solved by this standard. The general idea is yes, characters of unicodes, which may or may not be all unique due to overloading of meanings for certain characters, can be grouped as phrases or short sentences in a fixed order. Tokens of such unicodes can be sent in a batch as a means of communication. Phrases may be stored as a tuple in a contract, and tokens may get sent again just like regular NFTs. So there is some duplication. By saying phrases, I was really thinking about just a handful of characters. It can be 4, 2 or even just 1 character. A unicode like `24065` can be decoded as `token`, `coin` or `currency` depending upon the context.

It may not be fully possible with today’s infrastructures, and a dedicated wallet or wallet funcationality might be needed, besides, you were right that gas fees can be a big barrier for practical applicability, but I think that’s why logographs are shining in this scenario and there is more value to be explored in this direction.

---

**abcoathup** (2021-10-05):

Hi [@maxareo](/u/maxareo),

For EOA communication, some people use input data in a transaction, see: https://etherscan.io/idm

I’ll be following to see if what demand there is for a token messaging standard.

