---
source: magicians
topic_id: 20687
title: Improving Multisig Wallet Standards
author: iamcapote
date: "2024-08-01"
category: Web > Wallets
tags: [wallet, multisigs]
url: https://ethereum-magicians.org/t/improving-multisig-wallet-standards/20687
views: 265
likes: 6
posts_count: 2
---

# Improving Multisig Wallet Standards

A multisig wallet is a smart contract-based wallet that requires multiple signatures to execute transactions. This mechanism enhances security by distributing control among multiple parties. However, there are areas for improvement to further secure and democratize the governance of multisig wallets, especially within decentralized autonomous organizations (DAOs).

### Proposed Improvements to the Multisig Standard

### 1. Time-Based Voting Shares

**Problem Statement:** Many DeFi protocols are managed using multisig wallets, which control the distribution of funds and participate in critical protocol decisions. Currently, there is no effective mechanism to remove bad actors from the core governance of a DAO if they form a majority within the multisig group or a majority within the community

**Solution:** Implement an election-based multisig process to address the issue of entrenched bad actors. This proposal includes the following features:

- Regular Elections: Members of the multisig wallet are elected by the community every four years. This process ensures that the control of the wallet remains in the hands of trusted and accountable members.
- Presidential Role: The multisig can have a president or owner, who may be chosen on a different schedule from other members or this role may not be voted on at all. This role provides an additional layer of oversight and leadership.
- Community Involvement: This standard allows the community to have an equal opportunity to influence the future of their platform through regular elections.

Not every DAO will require this standard, but it offers a democratic method for those that prioritize community governance.

This standard can also be incorporated with:

### 2. Time-Locked Transactions

**Feature:** Allow owners to set time delays on certain transactions.

**Benefit:** Provides a window to cancel potentially malicious transactions, enhancing the security and control over high-value or sensitive transactions.

### 3. NFT Tokenized Shares

**Feature:** Represent ownership shares in the multisig wallet as NFTs.

**Benefit:** Facilitates the distribution and transfer of ownership rights, making it easier to manage changes in ownership. Tokenized shares enable seamless transfer and management of ownership stakes, promoting flexibility and liquidity.

Note: This is an open proposal inviting any developer to create what is described here ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=15) credit would be nice thank you

## Replies

**kopykat** (2024-08-11):

Hey, have you checked out modular smart accounts ([ERC-7579](https://erc7579.com/))? Safe and other existing smart accounts are compatible and you can build modules that enable these features

