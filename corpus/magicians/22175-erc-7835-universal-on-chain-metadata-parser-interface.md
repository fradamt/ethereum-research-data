---
source: magicians
topic_id: 22175
title: "ERC-7835: Universal On-Chain Metadata Parser Interface"
author: ZeroKPunk
date: "2024-12-11"
category: ERCs
tags: [evm, wallet]
url: https://ethereum-magicians.org/t/erc-7835-universal-on-chain-metadata-parser-interface/22175
views: 127
likes: 0
posts_count: 4
---

# ERC-7835: Universal On-Chain Metadata Parser Interface

Hi, so happy to share my design of a standardized interface for parsing on-chain metadata, this is greatly inspired by vitalik’s recent article: [What I would love to see in a wallet](https://vitalik.eth.limo/general/2024/12/03/wallets.html)

## Abstract

This proposal defines a standardized interface for parsing on-chain metadata (MetaData) relevant to Wallets. The standard consists of two core components:

- 1.Wallet-level parser interface: wallet_metaDataAbstractParser

A universal entry point that Wallets can use to request metadata parsing.

- 2.Smart contract-level parsing logic: parserHandler and parserData

Smart contracts that handle specific parsing logic, receiving parameters from Wallets and returning readable metadata.

The aim of this proposal is to establish a general-purpose, trustless, and decentralized metadata parsing standard that enhances user experience, security, and the readability of Ethereum ecosystem metadata.

## Motivation

Wallets serve as the primary interface between users and the Ethereum ecosystem. To improve user experience and security, Wallets need to parse various types of on-chain metadata, such as:

- ENS mappings to addresses.
- Standard assert’s readable label (eg. ERC-20, ERC-721)
- On-chain content (e.g., resources like eth.limo).
- Cross Chain intentions standard like EIP-7683
- Other human-readable on-chain information.

Currently, Wallets lack a standardized way of parsing metadata, leading to several challenges:

- 1.Inconvenience: Different Wallets implement metadata parsing differently, resulting in inconsistent user experiences.
- 2.Security Risks: Scattered parsing logic increases the attack surface for malicious actors.
- 3.Low Readability: On-chain data is often difficult for users to understand without additional processing.

This proposal aims to solve these problems by creating a standardized, secure, and user-friendly way for Wallets to parse on-chain metadata.

## Specification

Workflow

[![workflow](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c264d7df07e0b24721658daaa6adeed5ea7bff17_2_653x500.png)workflow1996×1528 161 KB](https://ethereum-magicians.org/uploads/default/c264d7df07e0b24721658daaa6adeed5ea7bff17)

Please check out the full spec in github:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/755)














####


      `master` ← `ZeroKPunk:master`




          opened 10:25AM - 06 Dec 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/8c46b064cc95f28a2a0334fb19d32ae6c58f3a63.jpeg)
            ZeroKPunk](https://github.com/ZeroKPunk)



          [+250
            -0](https://github.com/ethereum/ERCs/pull/755/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/755)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**SamWilsn** (2025-01-17):

Bit of bikeshedding, but RPC endpoints are normally named as actions, so `wallet_metaDataAbstractParser` might become `wallet_parseAbstractMetaData`.

---

**SamWilsn** (2025-01-17):

> wallet_metaDataAbstractParser is a universal interface that Wallets can use to request metadata parsing.

The wallet can request metadata parsing? The `wallet_` family of functions are normally provided *by* wallets for dapps to use. If wallets are supposed to consume this function, who is providing it?

---

**SamWilsn** (2025-01-17):

I guess I don’t really understand how this is different from just using `eth_call` with a standardized interface.

