---
source: ethresearch
topic_id: 20349
title: Accessible Encryption for Ethereum Rollups with Fairomon
author: shakeshack
date: "2024-08-28"
category: Layer 2
tags: [rollup]
url: https://ethresear.ch/t/accessible-encryption-for-ethereum-rollups-with-fairomon/20349
views: 362
likes: 3
posts_count: 1
---

# Accessible Encryption for Ethereum Rollups with Fairomon

[![690x435](https://ethresear.ch/uploads/default/optimized/3X/5/f/5fa5f78d2b4b44708e03133cf29d1de097113e36_2_690x435.jpeg)690x4351200×757 210 KB](https://ethresear.ch/uploads/default/5fa5f78d2b4b44708e03133cf29d1de097113e36)

Co-authored by [@pememoni](/u/pememoni) and [@shakeshack](/u/shakeshack). With special thanks to the rest of the Fairblock team!

Fairomon is a special fairy type pokemon that combines the work of Fairblock and Monomer - a framework that enables builders to create Ethereum rollups with built-in encryption with minimal lift.

# Background

Monomer is a rollup framework that enables Cosmos SDK app chains to be deployed as rollups on Ethereum. Internally, Monomer is built on top of the OP stack relying on it for chain derivation and settlement while supporting an ABCI interface for a Cosmos SDK app chain to be deployed on top. Fairblock provides threshold MPC encryption that can be utilized in Monomer rollups through a module built for Cosmos SDK chains.

[![451x500](https://ethresear.ch/uploads/default/optimized/3X/2/3/2311821ac2a3b134e2df081bbf12f2d71f2c31cc_2_451x500.png)451x5001336×1478 36.6 KB](https://ethresear.ch/uploads/default/2311821ac2a3b134e2df081bbf12f2d71f2c31cc)

Fairblock enables blockchain developers to integrate pre-execution encryption. This pre-execution encryption is made possible through their threshold MPC network that delivers identity-based encryption (IBE), and soon custom encryption schemes, to partner chains. Fairblock’s MPC network, called Fairyring, generates threshold encryption and decryption keys for each supported Monomer rollup, while the rollups themselves receive and process encrypted transactions natively.

# How it Works

FairyRing uses decentralized key generation to issue a master secret key (MSK) for each epoch (every 100 blocks). From each MSK, a master public key (MPK) can be derived. Once the MPK is derived, it is relayed to a Monomer chain where it will be used to encrypt each requested transaction. In parallel, the MSK is split into equal shares for the amount of FairyRing validators participating in the network. For each request for decryption, FairyRing validators use their share of the MSK to collectively derive the associated private keys.

In threshold IBE, users or developers can program the decryption conditions for transactions. Onchain conditions that could trigger decryption could be a block height, the price of an asset, a smart contract call, verification of a ZK proof, or the end of a governance poll, for example. Identity-based encryption allows for the programmability of decryption and allows for decryption to be triggered by “IDs,” which can be either onchain conditions or on/offchain identifiers or attributes that certain wallets prove ownership of.

# What’s Possible with Fairomon

MPC encryption can make a number of previously inaccessible applications possible within rollups, most notably encrypted mempools, censorship-resistant sequencing, and DeFi and gaming apps such as encrypted orders, leaderless NFT auctions, ID-gated content, and highest-hand-wins card games like blackjack.

The transaction flow for an application is as follows:

- User submits an encrypted tx and decryption condition (e.g. target height) to an app
- Chain receives encrypted txs in mempool
- Encrypted txs are sorted by target heights and ordering within a block is committed to inside of the integrated x/pep module
- When target height or decryption condition is reached, the app chain receives decryption key from the Fairyring chain
- Encrypted txs are decrypted and executed inside the BeginBlock method of the x/pep module

See the architecture diagram below for a detailed description of how Fairyring integrates with a Monomer appchain.

[![690x147](https://ethresear.ch/uploads/default/optimized/3X/7/2/723cc342b05947059263449d26d5e63a0010c14a_2_690x147.png)690x1471600×341 106 KB](https://ethresear.ch/uploads/default/723cc342b05947059263449d26d5e63a0010c14a)

Monomer links:

- Github
- Docs

Fairblock links:

- Website
- Github
- Docs
