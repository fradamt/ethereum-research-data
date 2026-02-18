---
source: magicians
topic_id: 18602
title: To get verified the novelty of a concept for an EIP
author: mastrmind-dev
date: "2024-02-11"
category: EIPs
tags: [erc, nft, soul-bound]
url: https://ethereum-magicians.org/t/to-get-verified-the-novelty-of-a-concept-for-an-eip/18602
views: 677
likes: 0
posts_count: 5
---

# To get verified the novelty of a concept for an EIP

Hi all,

I have a concept to create a NFT standard that is shared among multiple accounts or in other words we can say, multiple accounts are pointed to the exact same NFT.

This is different than ERC1155 since there are no multiple instances of the same token, instead the exact same token is shared among multiple accounts.

For a use case, think a group of people has bought a NFT and each member needs to have an ownership for the NFT.

**As advised in [EIP-1](https://eips.ethereum.org/EIPS/eip-1), I want to get confirmed that this concept is not already in a prior EIP.** Please help me to move forward…

Edit-:

Thanks to [@CalMC](/u/calmc), I got a chance to tell you that this is not Fractional-NFT. In fact, I am not fractioning NFTs. [It is explained here (as a reply to this thread itself.)](https://ethereum-magicians.org/t/to-get-verified-the-novelty-of-a-concept-for-an-eip/18602/3)

## Replies

**CalMC** (2024-02-11):

Fractionalising NFTs? Think that’s a “Page Not Found”! ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

---

**mastrmind-dev** (2024-02-11):

[@CalMC](/u/calmc) Thank you for replying.

Fortunately my idea is different than Fractional-NFTs as well. I don’t make NFTs into fungible tokens like ERC20 like what happens in F-NFTs.

Instead, the NFT will be still an NFT yet multiple accounts are pointed to it. It is like a few people are sharing a property without dividing the property into fractions.

Or think about something like this:

1. A person holds a NFT
2. That person has multiple accounts
3. That person wants to have rights to the ownership of the NFT with all of her/his accounts.

So, at the end, there will be a single token with multiple accounts are pointed out to that single token.

---

**CalMC** (2024-02-11):

Thanks for clarifying. What are some good use case examples?

---

**mastrmind-dev** (2024-02-12):

Definitely, ID verification in decentralized environment. Actually I am doing a research on Sybil attack prevention. Below the basic idea,

1. We do an off-chain id verification for a person with his crypto account.
2. Mint an NFT to that person linking the hashed id data to the NFT.
3. Whenever he tries to get verified his another account the same hashed data is generated (since he has to go through the same id verification process.)
4. So, we point out his second account to the same NFT.

Specially this is suitable for the DAOs which use quadratic voting or any other voting methods on the purpose of reducing power concentration.

Also, any other off-chain application can use this (Check NFT details in the registration process to prevent creating fake accounts.)

Since this is for sybil attack prevention and sybil attack prevention is a common issue, I think this has a broad usability.

