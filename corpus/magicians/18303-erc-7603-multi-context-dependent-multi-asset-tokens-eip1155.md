---
source: magicians
topic_id: 18303
title: "ERC-7603: Multi-Context Dependent Multi-Asset Tokens, EIP1155-Extension"
author: haruu8
date: "2024-01-25"
category: ERCs
tags: [erc, erc-1155]
url: https://ethereum-magicians.org/t/erc-7603-multi-context-dependent-multi-asset-tokens-eip1155-extension/18303
views: 987
likes: 1
posts_count: 7
---

# ERC-7603: Multi-Context Dependent Multi-Asset Tokens, EIP1155-Extension

[PRs](https://github.com/ethereum/ERCs/pull/220)

An ERC-1155 compatible multi-context dependent multi-asset token, referenced from ERC-5773.

I’ve very inspired by [ERC-5773](https://eips.ethereum.org/EIPS/eip-5773) about concept, and implementation, and I wrote the proposal based on it.

Multi-asset compatibility with ERC-1155 is important to enhance interoperability as well as ERC-5773 seeks to develop cross-metaverse and cross-engine standards in ERC721.

Let me know what you think, thank you for your support.

## Replies

**Mani-T** (2024-01-26):

This has the potential to significantly enrich the token landscape on Ethereum. Good job.

---

**stoicdev0** (2024-01-26):

You are fully copying as far as I can see the ERC-5773 implementation without any mention to it on your proposal which does not seem right.

On top of that, since it seems to be exactly the same, have you tried using ERC-5773 on top of an ERC-1155? It might work just as it is with no need for an additional ERC.

---

**haruu8** (2024-01-27):

I apologize for my rudeness. I was indeed affected by ERC-5773 and submitted the EIP with reference to it. Not mentioning ERC-5773 is disrespectful in retrospect, so I added a sentence I’ve inspired in the message in the body of the thread.

I think it’s rewarding to standardize multi-context dependent multi-asset tokens compatible with ERC-1155, not ERC-721. Multi-Context Dependent Multi-Asset Tokens are the crucial standard for implementing cross-metaverse and cross-engine and enhancing interoperability in the Ethereum network.

I’d just develop a combination of ERC1155 and part of a multi-asset feature in ERC5773 if I just developed a smart contract for myself. However, to make the implementation of multi-metaverse and multi-engine, I believe I should listen to the voices of various dApp developers through discussion for standardization and discuss and implement standards that many developers find easy to use.

That’s why I posed new standards of multi-context dependent multi-asset tokens as an ERC-1155 extension.

---

**stoicdev0** (2024-01-27):

I did not see any difference in what you propose. Can you let me know what is different?

Did you try using it as it is for a 1155?

---

**haruu8** (2024-01-29):

Currently, there are no differences. Also, I have not yet attempted to do so for actual use. I believe that ERC5773 should be used as a reference for multimedia data management, but we would like to discuss with developers who use ERC1155 on a regular basis and make changes to this proposal if necessary. I would like to discuss this with various developers and proceed with standardization based on ERC5773.

---

**SamWilsn** (2024-05-15):

Have you looked at [EIP-4955](https://eips.ethereum.org/EIPS/eip-4955) by any chance? Vaguely similar idea.

