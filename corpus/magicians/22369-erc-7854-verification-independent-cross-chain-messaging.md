---
source: magicians
topic_id: 22369
title: "ERC-7854: Verification-independent Cross-Chain Messaging"
author: nambrot
date: "2024-12-30"
category: ERCs
tags: [interop]
url: https://ethereum-magicians.org/t/erc-7854-verification-independent-cross-chain-messaging/22369
views: 303
likes: 3
posts_count: 1
---

# ERC-7854: Verification-independent Cross-Chain Messaging

Official discussion thread for [ERC7854: Verification-independent Cross-Chain Messaging Standard](https://github.com/ethereum/ERCs/pull/817). It proposes an API for sending messages across chains to enable interoperability in the greater Ethereum ecosystem (but is flexible enough to encompass alternate VMs). It specifically is capable of sending messages via arbitrary transport and verifying them via diverse mechanisms. At the same time, it aims to provide enough standardization with a modular relaying mechanism to provide a consistent developer experience. As such, it allows for a clean separation of high level abstractions to be built by “application developers” like cross-chain tokens and account abstraction, while allowing for innovation at the verification and transport layer.
