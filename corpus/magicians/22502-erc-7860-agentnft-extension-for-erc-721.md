---
source: magicians
topic_id: 22502
title: ERC-7860 AgentNFT Extension for ERC-721
author: lanyinzly
date: "2025-01-12"
category: ERCs
tags: [erc, nft, token, erc-721]
url: https://ethereum-magicians.org/t/erc-7860-agentnft-extension-for-erc-721/22502
views: 138
likes: 2
posts_count: 4
---

# ERC-7860 AgentNFT Extension for ERC-721

This extension allows a NFT (ERC-721) token to store prompts and AI agent’s address, facilitating the establishment of an on-chain identity for AI-powered entities.

As artificial intelligence becomes increasingly integrated with blockchain technology, there is a growing need for standardized interfaces that enable NFTs to interact with AI systems. Current ERC-721 tokens lack native support for AI integration. However, ERC-721 tokens are non-fungible, transferable, capable of storing data, and compatible with extensions such as ERC-6551 wallets. These characteristics make ERC-721 a suitable standard for serving as an on-chain identity for AI agents.

At present, prompts and other relevant information are often stored in the NFT token URI without a standardized format, making recognition and application challenging. This extension addresses these limitations by providing:

1. A decentralized on-chain identity for AI agents – By associating AI agents with AgentNFTs, this extension enables them to interact with smart contracts in a highly composable manner.
2. A transferable and non-custodial asset type – AgentNFTs function as liquid assets, facilitating ownership transfers while preserving on-chain value.
3. An interface for storage and management of prompts and AI agent addresses – Each AgentNFT securely maintains its associated AI agent’s address and prompt data, ensuring consistency and interoperability.

## Replies

**KBryan** (2025-01-15):

This is interesting and needed. I was thinking about something similar for creating Agentic NPCs in a game I’m working on. I would love to collaborate.

---

**lanyinzly** (2025-01-19):

Sounds great! We can definitely talk. DM you.

---

**bomanaps** (2025-03-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lanyinzly/48/10565_2.png) lanyinzly:

> This extension allows a NFT (ERC-721) token to store prompts and AI agent’s address, facilitating the establishment of an on-chain identity for AI-powered entities.
>
>
> As artificial intelligence becomes increasingly integrated with blockchain technology, there is a growing need for standardized interfaces that enable NFTs to interact with AI systems. Current ERC-721 tokens lack native support for AI integration. However, ERC-721 tokens are non-fungible, transferable, capable of storing data, and compatible with extensions such as ERC-6551 wallets. These characteristics make ERC-721 a suitable standard for serving as an on-chain identity for AI agents.
>
>
> At present, prompts and other relevant information are often stored in the NFT token URI without a standardized format, making recognition and application challenging. This extension addresses these limitations by providing:
>
>
> A decentralized on-chain identity for AI agents – By associating AI agents with AgentNFTs, this extension enables them to interact with smart contracts in a highly composable manner.
> A transferable and non-custodial asset type – AgentNFTs function as liquid assets, facilitating ownership transfers while preserving on-chain value.
> An interface for storage and management of prompts and AI agent addresses – Each AgentNFT securely maintains its associated AI agent’s address and prompt data, ensuring consistency and interoperability.

good job! I went throuhh the agent contract but I noticed that the contract has Incomplete Agent Identity Management

The contract allows setting and updating an agent address, but no validation or standardization of what constitutes a valid “AI agent”

