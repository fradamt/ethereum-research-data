---
source: magicians
topic_id: 13528
title: "EIP-6774: Non-sellable tokens"
author: Raphael
date: "2023-03-25"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/eip-6774-non-sellable-tokens/13528
views: 1416
likes: 8
posts_count: 5
---

# EIP-6774: Non-sellable tokens

Hello!

We introduced an EIP that extend the EIP-721 to create non-sellable tokens (NST). It proposes to replace transfers functions by a barter mechanism to prevent one-way transfers and thus prevent speculation.

- EIP-draft
- Reference implementation

Here an [article](https://www.linkedin.com/pulse/non-sellable-token-nst-matthieu-chassagne/?trackingId=q4py17gSQLuzJaS0If8ofQ%3D%3D) that introduce the idea, we also created a [dApp](https://github.com/NST-Standard/nst-dapp) (with contracts deployed on Optimism goerli) to illustrate the mechanism of transfer.

We would love to discuss, have feedbacks and criticisms on this EIP.

## Replies

**alijasin** (2023-04-01):

So if I’ve understood this correctly, SBTs might in some cases be too restrictive and thus the need for this proposal. Interesting!

Have you considered the possibilities of circumventing the selling restriction by leveraging a smart contract to act as a custodian for the token. Requiring one party to enter a set amount of ether to be able to withdraw the token?

---

**Raphael** (2023-04-05):

Indeed for some purposes, we consider SBTs way too restrictive and NFT way too permissionless. Bypassing restrictions and royalties is made easy by the permissionless aspect of NFTs, wrapping up an NFT into another contract to bypass royalties enforcement is possible.

This standard relies on the value equivalence in a barter to keep the non-sellability. So, we designed the standard such as permissionless barter should be disabled.

Leaving bartering functions permissionless would render the standard ineffective, any NST owner could create or use a fake NST to perform a one-way transfer of their NST, allowing listing on a marketplace or an OTC sale.

We took the bias of the whitelist at the contract level to maintain this value equivalency and we relied on the creation of a NST barterable network instead. This was the most important subject in the creation of the standard which was worth many discussions.

What do you think about implementing such restrictions at the contract level to prevent sellability? Have you other suggestions to prevent the sellability of a token?

---

**Perrin** (2023-04-07):

Hi, a short description about the implemented of this Non Sellable Token and our questions:

- The goal of our proposal is to prevent speculation on NFT, we will detail the reason for that and use cases in next posts (the most obvious is to make sure that the token will be not considered as a security token but only as a utility token).
- You can only transfer a NST (NFT which is not sellable) to someone if he transferts another NST to you: a barter
- For performing this barter:

1. the user who wants to initiate barter (user A) has to sign a message taking up the terms of the barter: Which token (token A) does the owner want to exchange for which unowned token (token B)?
2. the owner of the token B (user B) receives the request and its barter terms
3. when the barter function is called, the contract ensures the NST compliance of the token A and B to perform the exchange. This control is done from a register (whitelist, see the previous message from @Raphael for explanation) that allows token addresses to be participants of NST exchange
4. The user B signs a message for barter acceptance.
5. Token A is transferred from User A to User B and Token B is transferred from user B

We are trying to create a standard, it means the most minimalist and simple rules possible, but we think the only way to ensure NST compliance for a token address is to use a register with a whitelist for token contracts. Do not hesitate to give us your point of views or share your opinion about our proposal and how we should implement it.

Thanks!

---

**Perrin** (2023-04-11):

[@omaraflak](/u/omaraflak) it is very similar to your topic [EIP-4671: Non-tradable Token](https://ethereum-magicians.org/t/eip-4671-non-tradable-token/7976), with the possibility of transfer as you said and with no monetary value. What is your point of view about our proposal?

