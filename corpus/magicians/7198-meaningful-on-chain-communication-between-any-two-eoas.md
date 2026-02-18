---
source: magicians
topic_id: 7198
title: Meaningful on-chain communication between any two EOAs
author: maxareo
date: "2021-10-03"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/meaningful-on-chain-communication-between-any-two-eoas/7198
views: 568
likes: 0
posts_count: 1
---

# Meaningful on-chain communication between any two EOAs

Hey guys, a simple on-chain communication system between any pair of EOAs is made possible in [EIP-4341](https://github.com/simontianx/ERC4341/blob/main/EIP/eip-4341.md). It works by transferring [EIP-3754](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3754.md) vanilla NFTs with unicoded tokenIds in a batch sort of like transferring tokens in ERC1155, however, the ordering information in this case shall be maintained.

This is particularly efficient and useful for emojis and languages that are based on **[logographs](https://en.wikipedia.org/wiki/Logogram)**  such as *hanzi* in Mandarin, *kanji* in Japanese, *hanja* in Korean, and etc, given their simplicity and conciseness in expressing meanings.

As far as I know, this is a new application. Is there already similar use cases? Thanks.
