---
source: magicians
topic_id: 21484
title: ERC-XXXX – Non-Custody Cross-Chain Protocol (Non-CCCP)
author: k06a
date: "2024-10-28"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-xxxx-non-custody-cross-chain-protocol-non-cccp/21484
views: 472
likes: 13
posts_count: 7
---

# ERC-XXXX – Non-Custody Cross-Chain Protocol (Non-CCCP)

**Non-Custody Cross-Chain Protocol (Non-CCCP)** introduces a robust alternative to centralized and semi-centralized bridges. It is highly interoperable, working with nearly any blockchain, including non-EVM chains like Bitcoin and Solana.

### Key Features

1. Self-custodial: Users maintain ownership of their assets throughout the entire cross-chain swap process, eliminating counterparty risk by using atomic swaps scheme.
2. Ownerless: Developers can implement cross-chain protocol on any blockchain without approval, allowing for permissionless protocol expansion.
3. Dutch Auction Pricing: A Dutch auction model with competing resolvers (order fillers) ensures optimal pricing, eliminating transaction reverts and risk of MEV

This proposal is currently a draft on HackMD, but it will soon be published as an ERC to the Ethereum github: [ERC-XXXX - Non-Custody Cross-Chain Protocol (Non-CCCP) - HackMD](https://hackmd.io/FDfvW-MbQhGjqVaOMOHdeA?2)

The purpose of this thread is to collect feedback from engineers having experiences with different blockchains to make this standard as broad as possible.

Please feel free to share your thoughts, feedback and questions. Contributions are highly encouraged.

## Replies

**abcoathup** (2024-10-29):

ERCs aren’t for marketing purposes so you shouldn’t use a project/company name in the title of an ERC.

Once you have created a PR, an editor or associate with manually assign an ERC number.

---

**k06a** (2024-11-01):

Thank you for the feedback [@abcoathup](/u/abcoathup)! I tried to come up with a concise name that captures the core features of the protocol while adding a bit of irony. I believe **Endgame Cross-Chain Protocol** not only conveys the essence but also serves as a bit of a meme.

---

**abcoathup** (2024-11-01):

I’d go for simplicity, “Cross-chain atomic swaps” for an ERC title.  Just say what it does.

---

**k06a** (2024-11-05):

[@abcoathup](/u/abcoathup) Maybe it makes more sense to call it “Non-Custody Cross-Chain Protocol (Non-CCCP)” since “Atomic Swaps” is just a way to achieve non-custody.

---

**Alex_Kaon.one** (2024-11-06):

This is a great proposal, just sharing some thoughts below:

1. To properly identify customers, traders, and destinations for non-EVM chains (e.g., UTXO), it’s important to consider an extended address standard — for example, CAIP-10. Deeper support for sigscript addresses could be introduced as a special clause within the standard.
2. Chain reorganizations raise a broad range of issues, including malicious or massive reorgs, sandwiching possibilities (i.e., incentivizing miners or validators to perform reorgs), and refunds and disputes.

A key question at the token standard level is: Who is responsible for the reorg? This is open for discussion, but I see two options:

a) The seller is responsible for the sender chain, and the receiving trader is responsible for the receiver chain.

b) It’s a flexible setup where each deal can be adjusted accordingly.

1. It’s also worth highlighting that atomicity is not immediate. Since fees can vary across pools, this may introduce opportunities to drain pools. One way this could be prevented is through repeated spamming with intermediate loans with a predetermined window of acceptance.
2. Another important consideration is that in some chains, such as Bitcoin, it’s important to verify the rating of received liquidity. This means the token standard should have the capability to incorporate different filtering logic and its providers.

---

**k06a** (2024-11-06):

Thank you for your comments! I’d be happy to discuss how we can make the protocol specification more Bitcoin-friendly and adaptable to all chains.

My responses to your points:

1. CAIP-10 and network hierarchy: We concluded that the CAIP-10 hierarchy is excessive for an atomic swap protocol. A flat numbering structure is sufficient, especially given that numerical identifiers are slightly more canonical at the protocol level than strings. SLIP-44, in turn, seems abstract enough and sufficiently complete for our purposes.
2. Chain reorganizations and responsibility: Both the trader and resolver have the option to manipulate the start time of their escrow contract, creating flexibility around the finality of both networks. In particular, the resolver can professionally manage risks to reduce their delay. To prevent unnecessary delays and establish market-based incentives for resolvers to complete transactions promptly for the user’s benefit, a second auction is planned with adverse rate adjustments for resolvers. This structure helps optimize completion times, enhancing user benefits and balancing risk.
3. Non-atomic swaps and potential attacks: To minimize the surface area for this type of attack (while not critical, it could be disruptive), we propose including a resolver whitelist within the order structure, based on recommendations from the DApp (protocol operator).
4. Asset origin responsibility: Responsibility for the origin of assets received by the user lies with the operator and the resolver, depending on their agreements. I don’t see a technical possibility of managing this within the protocol for atomic swap execution.

Thank you for the constructive feedback. I’m open to discussing any additional ideas or suggestions!

