---
source: magicians
topic_id: 19706
title: "ERC-7694: Solana Storage Router"
author: sshmatrix
date: "2024-04-18"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7694-solana-storage-router/19706
views: 847
likes: 3
posts_count: 2
---

# ERC-7694: Solana Storage Router

This standard is an extension to [EIP-7700](https://ethereum-magicians.org/t/erc-7700-cross-chain-storage-router-protocol/19853) introducing storage router for Solana. EIP-7700 introduces three external routers for deferring storage to L1, L2s and databases. This document extends that specification by introducing a fourth storage router targeting Solana as the storage provider.

Solana is a cheap L1 solution that is fairly popular among Ethereum community and is widely supported alongside Ethereum by almost all wallet providers. There are several chain-agnostic protocols on Ethereum which could benefit from direct access to Solana blockspace; ENS is one such example where it can serve users of Solana via its chain-agnostic properties while also using Solana’s own native storage. This development will surely encourage more cross-chain functionalities between Ethereum and Solana at core.

ERC Link: [ERCs/ERCS/erc-7694.md at solanaHandler · namesys-eth/ERCs · GitHub](https://github.com/namesys-eth/ERCs/blob/solanaHandler/ERCS/erc-7694.md)

Happy to hear comments & feedback.

## Replies

**SamWilsn** (2024-10-01):

Hey! I have a non-editorial related question about your proposal. ERC-3668 includes a section on [Gateway Response Data Validation](https://eips.ethereum.org/EIPS/eip-3668#gateway-response-data-validation). Should ERC-7694 include an algorithm/method/standard approach for doing data validation against the Solana blockchain? Something like a Solana lightclient in the EVM perhaps?

