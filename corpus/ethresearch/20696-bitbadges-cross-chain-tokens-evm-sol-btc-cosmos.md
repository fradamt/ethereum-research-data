---
source: ethresearch
topic_id: 20696
title: "BitBadges: Cross-Chain Tokens (EVM <-> SOL <-> BTC <-> COSMOS)"
author: trevormil
date: "2024-10-18"
category: Applications
tags: []
url: https://ethresear.ch/t/bitbadges-cross-chain-tokens-evm-sol-btc-cosmos/20696
views: 266
likes: 5
posts_count: 5
---

# BitBadges: Cross-Chain Tokens (EVM <-> SOL <-> BTC <-> COSMOS)

I wanted to introduce you all to BitBadges and what we are building: a cross-chain token standard. See https://bitbadges.io for it in action or https://docs.bitbadges.io.

BitBadges offers a range of tools for building multi-chain applications (Bitcoin, Ethereum, Solana, and Cosmos). All tools are a single interface, a single service, but support users from all chains.

Our main service is tokens (badges) where an Ethereum user can transfer / send tokens to a Solana and vice versa, along with tons of new innovative features like fine-grained transferability, no smart contracts by default, time-dependent balances, and more.

How do we support multi-chain? We are our own L1 Cosmos blockchain but we support signatures from ANY user. Everything is scoped to our blockchain, so we are not “interoperable”, but we are signature compatible with any ecosystem.

Yes, there are tradeoffs with design, but if you need an all-in-one hub, BitBadges is the place to go.

[![image](https://ethresear.ch/uploads/default/original/3X/1/b/1b67f85c1f7a8c2da70e7d062287c2b64292a8b3.png)image597×366 23 KB](https://ethresear.ch/uploads/default/1b67f85c1f7a8c2da70e7d062287c2b64292a8b3)

## Replies

**donatik27** (2024-10-31):

This all-in-one approach to cross-chain compatibility sounds very innovative! How does BitBadges handle security and validation for transactions coming from different chains, especially considering the absence of smart contracts by default?

---

**trevormil** (2024-10-31):

So two things:

1. The absence of smart contracts by default is mainly just because everything is already written for you. There are smart contracts, but think about the main token standard like a standard API. All it takes is just configuring the request (rather than programming a whole contract). In other words, we just use Cosmos SDK Msgs.
2. We are not interoperable in the fact that we validate transactions from different chains. Everything is all on our chain, but we can verify signatures from any supported wallet. So for example, an Ethereum user signs our transaction and we verify the Ethereum signature on our chain.

---

**donatik27** (2024-11-02):

Thank you for your detailed response! I appreciate the clarification on how BitBadges handles smart contracts and transaction validation. It’s a great concept, and I’m excited to see how you continue to develop this innovative approach. Keep up the great work!

---

**trevormil** (2024-11-02):

No problem!

It is an alternative approach to the standard security models of Ethereum and L2s, but it offers something different for those that might be willing to accept the tradeoffs!

