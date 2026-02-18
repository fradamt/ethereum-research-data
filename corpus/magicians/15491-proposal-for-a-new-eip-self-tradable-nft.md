---
source: magicians
topic_id: 15491
title: "Proposal for a New EIP: Self Tradable NFT"
author: Hanul
date: "2023-08-19"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/proposal-for-a-new-eip-self-tradable-nft/15491
views: 1020
likes: 6
posts_count: 7
---

# Proposal for a New EIP: Self Tradable NFT

> Discussion thread for ERC-7502: Self Tradable NFT

Hello, Ethereum Magicians!

I’m excited to introduce a concept I’ve been working on: Self Tradable NFT. This contract proposal aims to grant creators full control over the trading of their NFTs and the distribution of royalties without being heavily dependent on third-party marketplaces. Here’s a detailed breakdown:

## Overview

While the present NFT landscape has given birth to various marketplaces that facilitate NFT trades, creators largely remain dependent on them for selling, trading, and even distributing royalties. With the growth and maturation of the ecosystem, the need for a decentralized mechanism where creators have greater agency in these processes becomes more apparent.

Self Tradable NFT is designed to fill this gap, making it possible for creators to manage direct trades and handle royalties without intermediaries.

## Key Features

1. Direct P2P Trading - A direct trading system where both parties agree upon a trade, sign it, and execute it without relying on an external marketplace.
2. Integrated Royalty Management - Built-in royalty distribution system where a set percentage of sales can be sent as royalties to the creator and an optional contributor.
3. Creator-centric Controls - Extensive control features allowing the creator to dictate the behavior of their NFTs. This includes setting up metadata, transferring creator control, changing royalty percentages, etc.
4. Flexibility - Ability to toggle on/off the self-trading functionality, providing creators the freedom to decide how they want their assets to be traded.

## Specification

- ContractURI: A URI pointing to off-chain contract metadata.
- Royalty: Built-in royalty management system where creators can define a royalty percentage (e.g., 1000 for 10%) and an optional contributor percentage.
- Contributor: The contract allows for an optional contributor who can also receive a portion of the royalties.
- Self-Trade Execution: A trade involves a token, price, seller, buyer, expiry, and a nonce. Both seller and buyer sign the trade data, and the trade can be executed by anyone. A trade can only be executed once.
- Blacklisting Trades: Either the buyer or the seller can blacklist a trade using their signature, preventing the trade from being executed.

## Feedback

I’m eager to hear your thoughts, critiques, and suggestions. This proposal is just the beginning, and community feedback will be invaluable in refining and possibly implementing this EIP.

Looking forward to a constructive discussion. Thank you for your time!

## Replies

**Mani-T** (2023-08-21):

It emphasis on giving creators direct control over their NFTs’ trading and royalties is a significant advantage.

---

**Hanul** (2023-08-21):

Yes! this EIP aim to empower creators with autonomy, allowing them to operate without reliance on marketplaces. I believe this aligns with the core principles of decentralization too.

---

**nathanglb** (2023-08-21):

The wishlist isn’t 100% the same, but much of the wishlist sounds like what Limit Break has done with ERC721-C and its Payment Processor marketplace protocol.

https://medium.com/limit-break/introducing-erc721-c-a-new-standard-for-enforceable-on-chain-programmable-royalties-defaa127410

https://medium.com/limit-break/introducing-erc721-c-payment-processor-a-game-changing-nft-marketplace-protocol-355b840dfd5d

I would encourage you to read the articles and the code repos/docs for inspiration.

---

**Hanul** (2023-08-22):

Thanks for sharing the info!

---

**Hanul** (2023-09-10):

In ERC-7502, blocking Approval when NFT is in Self Tradable mode ensures safety against hacking attempts to acquire Approval.

---

**moneyseeker** (2023-10-17):

I hope this works ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

[ethereum](https://bitcial.com/market/currency/ethereum)

