---
source: magicians
topic_id: 19916
title: "[Idea Discussion] NFT-Based Flexible Token Locking System for Liquidity and Vested Payments"
author: njrapidinnovation
date: "2024-05-06"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/idea-discussion-nft-based-flexible-token-locking-system-for-liquidity-and-vested-payments/19916
views: 604
likes: 4
posts_count: 5
---

# [Idea Discussion] NFT-Based Flexible Token Locking System for Liquidity and Vested Payments

**Abstract:**

We propose a novel NFT-based flexible token locking system that revolutionizes how token locking and liquidity management are approached in the blockchain space. Unlike traditional locking mechanisms, our system represents locked funds as NFTs, enabling seamless transfer of control to another owner by simply transferring the NFT to a new wallet address. This unique approach opens up innovative use cases, such as ‘vested’ payments to third parties like influencers, where tokens are transferred but remain inaccessible for a specified period or until certain conditions are met.

**Key Features:**

1. Flexible Locking Conditions: Our system supports a variety of locking conditions, including time periods, token price thresholds (using AMMs or Chainlink price feeds), market capitalization limits, token burn thresholds, multisig unlock conditions, and even custom conditions using EventSig to check specific pre-defined conditions on external contracts. These conditions can be combined using AND, OR operators to create sophisticated locking strategies.
2. Liquidity Management: One of the most significant applications of our system is in locking liquidity. Project developers can now access a portion of their token’s locked liquidity for pre-approved uses, either through community governance voting or by meeting predefined minimum liquidity requirements. This feature introduces a new level of flexibility and control over locked liquidity that was previously unavailable.
3. Easy Lock Info Access: Users can easily check the locking information associated with an NFT by accessing the metadata URL attached to the NFT. This provides transparency and visibility into the locking conditions and status of locked funds.

**Conclusion:**

Our NFT-based flexible token locking system introduces a paradigm shift in token locking and liquidity management, offering unprecedented flexibility and control to token holders and project developers. We believe that this system has the potential to unlock new possibilities in decentralized finance and token economics, and we welcome feedback and collaboration from the community to further refine and develop this innovative concept.

**Discussion Points:**

1. What are your thoughts on using NFTs to represent locked funds?
2. How can flexible token locking systems benefit decentralized finance projects?
3. What additional locking conditions or features would you like to see in such a system?
4. How can we ensure the security and integrity of locked funds and NFT representations?
5. Are there any potential regulatory or compliance challenges associated with this approach?

## Replies

**PaulRBerg** (2024-05-06):

[Sablier](https://sablier.com/) (note: I’m a cofounder) has had NFT-based vesting plans [since July 13, 2023](https://twitter.com/Sablier/status/1679567118898192384).

Each vesting plan is called a ‘stream’ and it represented by an NFT that look like this:

[![nft](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7ce1f29d7b076d12f862894cb1eb96ae7c8175a1_2_300x300.jpeg)nft1330×1330 99.6 KB](https://ethereum-magicians.org/uploads/default/7ce1f29d7b076d12f862894cb1eb96ae7c8175a1)

Though we only support time-based locking of funds, so your idea is a bit more general-purpose.

---

**njrapidinnovation** (2024-05-07):

[@PaulRBerg](/u/paulrberg) That’s really interesting! It’s great to see how Sablier has been using NFT-based vesting plans. We’re exploring a similar concept but with a twist. In our approach, users can create customizable locking conditions for their tokens, which can depend on various factors.

For instance, users could set a time period for locking their tokens, but also include an OR condition that checks the value of an external contract. This external contract call could return true or false, indicating whether the tokens should be unlocked early based on certain conditions. This value could be set through a DAO proposal, adding a layer of transparency and community governance to the unlocking process.

We believe this approach offers users greater flexibility and control over their locked tokens, allowing them to adapt to changing circumstances or project needs. What do you think of this approach?

---

**PaulRBerg** (2024-05-07):

I agree that your approach is more flexible.

Do you have a live product I could take for a spin?

---

**njrapidinnovation** (2024-05-07):

Thank you for your interest! While we’re excited about the concept, we don’t have a live product available for use just yet. However, we’ve started working on proof-of-concept (POC) contracts to demonstrate the core functionalities of our proposed NFT-based flexible token locking system.

