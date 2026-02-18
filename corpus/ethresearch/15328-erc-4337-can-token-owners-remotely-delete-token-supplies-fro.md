---
source: ethresearch
topic_id: 15328
title: ERC-4337 - Can Token owners remotely delete token supplies from abstract smart contract wallets?
author: howardleejh
date: "2023-04-17"
category: Security
tags: []
url: https://ethresear.ch/t/erc-4337-can-token-owners-remotely-delete-token-supplies-from-abstract-smart-contract-wallets/15328
views: 800
likes: 0
posts_count: 2
---

# ERC-4337 - Can Token owners remotely delete token supplies from abstract smart contract wallets?

Firstly, apologies as I’m a noob here, can I ask what happens when exploiters create an ICO project and sell their tokens, and upon completion of sale, decides to burn all the tokens that belong to abstract smart contract wallet owners? Am I right to say that because a smart contract does not require an `approve()` before making a `safeTransferFrom()` to a `0x00` address, essentially “burning the tokens” and affecting total supply on the ERC20 tokens, that this might be a possible exploit for ERC-4337 smart contract wallet owners?

## Replies

**howardleejh** (2023-04-17):

Sorry, just read forum rules and shouldn’t be posting this here. My bad.

