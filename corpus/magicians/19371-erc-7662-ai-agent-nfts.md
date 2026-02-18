---
source: magicians
topic_id: 19371
title: "ERC-7662: AI Agent NFTs"
author: marleymarl
date: "2024-03-26"
category: ERCs
tags: [nft, ai, agents]
url: https://ethereum-magicians.org/t/erc-7662-ai-agent-nfts/19371
views: 946
likes: 1
posts_count: 3
---

# ERC-7662: AI Agent NFTs

## Abstract

This proposal introduces a standard for AI agent NFTs. In order for AI Agents to be created and traded as NFTs it doesn’t make sense to put the prompts in the token metadata, therefore it requires a standard custom struct. It also needs doesn’t make sense to store the prompts directly onchain as they can be quite large, therefore this standard proposes they be stored as decentralized storage URLs. This standard also proposes two options on how this data should be made private to the owner of the NFT, with the favored implementation option being encrypting the data using custom contract parameters for decryption that decrypt only to the owner of the NFT.

## Motivation

The creation and trading of AI Agent NFTs are a natural fit and offer the potential for an entirely new onchain market. This requires some custom data to be embedded in the NFT through a custom struct and this needs to be standardized so that any marketplace or AI Agent management product, among others, know how to create and parse AI Agent NFTs.

This is discussion for the PR: [Add ERC: AI Agent NFTs by marleymarl · Pull Request #348 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/348/files)

## Replies

**CROME** (2025-08-13):

Very interesting concept. Working on something that introduces this idea!

---

**marleymarl** (2025-09-10):

Hi Crome, that’s great that you are working on an implementation. I have a big one coming out soon as well.

Let me know if you need any tips or advice on your implementation - happy to help!

