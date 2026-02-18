---
source: magicians
topic_id: 18376
title: Adding `sendBatchTransaction` function in the wallet provider
author: arjn
date: "2024-01-29"
category: EIPs
tags: [erc, evm, wallet, account-abstraction, provider]
url: https://ethereum-magicians.org/t/adding-sendbatchtransaction-function-in-the-wallet-provider/18376
views: 700
likes: 4
posts_count: 2
---

# Adding `sendBatchTransaction` function in the wallet provider

**Introduction**

Account Abstraction has come a long way since the start of 2023 and there are multiple mobile and browser-based wallets built on top of Account Abstraction.

Research, discussion, and development have been going on in the space of [Account Abstraction (EIP-4337)](https://ethereum-magicians.org/t/erc-4337-account-abstraction-via-entry-point-contract-specification/7160), [Modular Smart Contract Accounts (ERC-6900)](https://ethereum-magicians.org/t/erc-6900-modular-smart-contract-accounts-and-plugins/13885), [Native Account Abstraction in the form of a RIP (Rollup Improvement Proposal) (RIP-7560)](https://ethereum-magicians.org/t/rip-7560-native-account-abstraction/16664).

Among many other smart functionalities, AA enables sending batch transactions that have huge implications in terms of improvement in user experience and security.

**Problem**

Batching enables atomicity that ensures that if one transaction in the batch fails, the whole batch reverts. This is particularly useful if the user wants to perform a token swap. If the approval transaction is successful and the swap fails for some reason, there is a pending approval on the contract that can act as an attack surface. Batching can ensure that the approval and swap happen in one go or revert completely, thus maintaining atomicity.

Even though batching is supported by some wallets like [WalletX](https://walletx.info), the dApps cannot leverage that functionality because of not have a provider function to send transaction parameters in an array of objects.

**Proposal**

This is the start of a proposal to add a new function to the provider as part of standardization. The provider function can be named `sendBatchTransaction` and this can be utilized by AA-compatible wallets. DApps can recognize AA-compatible wallets by using a getter function called `isAAWallet`.

More details and specifics to be added in the coming days.

Hoping to see the views and opinions of the community.

## Replies

**shakti** (2024-01-29):

It sounds great and I would love to see it implemented across the dApp ecosystem.

