---
source: magicians
topic_id: 22391
title: "ERC-7857: An NFT Standard for AI Agents with Private Metadata"
author: spark
date: "2025-01-02"
category: ERCs
tags: [erc, nft, token]
url: https://ethereum-magicians.org/t/erc-7857-an-nft-standard-for-ai-agents-with-private-metadata/22391
views: 1163
likes: 11
posts_count: 8
---

# ERC-7857: An NFT Standard for AI Agents with Private Metadata

With the increasing intelligence of AI models, agents have become more and more powerful to be able to help people process meaningful daily tasks autonomously. In blockchain industry, a lot of projects have provided functionality to create agents for their users. The trend will continue and “agent x crypto” has been recognized as the biggest narrative in the next few years. Currently, one key thing that is still missing is the management of the ownership of an agent in a decentralized way. Specifically, when you create an agent on a platform like Virtuals or EternalAI, there is no on-chain information that can acknowledge that the agent you created does belong to you. We think that a key solution to this problem is something like NFT.

NFT is a smart contract technology to help users manage their ownership of non-fungible assets. We see that an agent has non-fungible property either. Every agent can be treated as unique to others. It also has ownership property to its creator. An NFT token may have some metadata that can usually be a unique image representing its appearance. Likewise, an agent may also have some metadata that defines its capability. This metadata may include the neural network model, the memory, and the character of the agent. Therefore, it seems natural to associate an agent with an NFT token.

However, there is a challenge to simply use the existing NFT standard like ERC721 to abstract the agent. One of the major reasons is as follows. When transferring an agent NFT token, we are not only transferring the tokenId ownership, but also transferring the ownership of the metadata. And the metadata of an agent is so valuable (it could be the major purpose of this transfer) that it is often stored in a private environment or in a public environment with encryption. Therefore, the actual transferring of the agent metadata needs to be done in a privacy-preserving and verifiable manner. ERC721 lacks the capability of fulfilling this way of transferring.

Here is the proposal of a new ERC to better associate an agent with an NFT so to give the ownership of the agent to a user’s wallet address in a decentralized way.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/824)














####


      `ethereum:master` ← `0glabs:master`




          opened 01:51PM - 02 Jan 25 UTC



          [![Wilbert957](https://avatars.githubusercontent.com/u/161988856?v=4)
            Wilbert957](https://github.com/Wilbert957)



          [+587
            -0](https://github.com/ethereum/ERCs/pull/824/files)







A standard interface for NFTs specifically designed for AI agents, where the met[…](https://github.com/ethereum/ERCs/pull/824)adata represents agent capabilities and requires privacy protection. Unlike traditional NFT standards that focus on static metadata, this standard introduces mechanisms for verifiable data ownership and secure transfer. By defining a unified interface for different verification methods (e.g., TEE, ZKP), it enables secure management of valuable agent metadata such as models, memory, and character definitions, while maintaining confidentiality and verifiability.












With this, users can create Eliza and Virtuals agents with true ownership and put its intelligence (metadata) in decentralized storage for permanent memory.

## Replies

**baconvalley** (2025-01-10):

i’m so bullish on this proposal! this proposal completes the Decentralized AI Agent’s component

cheers for [@spark](/u/spark) to create this proposal! ![:beers:](https://ethereum-magicians.org/images/emoji/twitter/beers.png?v=12)

---

**EugeRe** (2025-01-17):

Hey [@spark](/u/spark) ! Can you help me to understand how your proposal significantly differs from existing ERC 7662?

Many thanks!

---

**spark** (2025-02-04):

I think 7662 doesn’t touch how the agent metadata can be transferred with privacy preserving.

---

**CROME** (2025-08-13):

Working on something that treats agents as unique, ownable, and transferable on-chain, but with privacy-preserving and verifiable metadata transfer built in. Think of it as the next step beyond ERC-721, purposefully built for Intelligent Finance.

---

**CROME** (2025-08-13):

Correct yeah, we have worked on something that addresses this. With Liquid Agents, metadata transfer is both verifiable and privacy-preserving, so ownership and capabilities move together without exposing sensitive data.

---

**SamWilsn** (2025-09-09):

> ```auto
> intelligentDatasOf
> ```

“Data” is already plural (or possibly an uncountable noun if you’re weird like me), so you shouldn’t put an “s” on it.

---

**Wilbert957** (2025-09-10):

![:ok_hand:](https://ethereum-magicians.org/images/emoji/twitter/ok_hand.png?v=12) Yes, it can be easily fixed, and no worries about it.

