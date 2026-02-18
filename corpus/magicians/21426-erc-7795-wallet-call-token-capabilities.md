---
source: magicians
topic_id: 21426
title: "ERC-7795: Wallet Call Token Capabilities"
author: MilkyTaste
date: "2024-10-21"
category: ERCs
tags: [erc, wallet, account-abstraction]
url: https://ethereum-magicians.org/t/erc-7795-wallet-call-token-capabilities/21426
views: 155
likes: 0
posts_count: 3
---

# ERC-7795: Wallet Call Token Capabilities

https://github.com/ethereum/ERCs/pull/681

## Abstract

This ERC addresses the lack of communication channels between the dapp and smart contract wallets. Wallets are tasked with sending transactions on behalf of the user, but dapps craft these transactions. The challenge is that dapps don’t have a way of communicating the prerequisites for these transactions, so wallets can’t fulfill them.

To solve this issue, an additional optional field is included in the transaction request. This field is a list of “requirements” that the wallet has to fulfill for the requested transactions to be considered “ready.”

Wallets can use this list of requirements, alongside their knowledge about the addresses of the user, to decide how to act next. Depending on the availability of funds and the list of requirements, the options could be: send the transaction right away, send the transaction with a prefix that fulfills the requirements, or ask the user to select a path to fulfill the requirements.

Wallets would be tasked with finding all possible paths to fulfill these requirements, while dapps SHOULD NOT attempt to check the requirements themselves, letting the wallet handle scenarios like “low balance” or “low allowance.”

---

For more information please see the ERC.

## Replies

**MilkyTaste** (2024-11-24):

This ERC has been updated to leverage ERC-5792’s Wallet Call API and now provides additional “capabilities” instead of a new RPC method.

---

**dror** (2025-04-08):

One thing I would add to this ERC is to let the wallet perform the actual approve.

That is, the wallet should add a `token.appove(target.amount)` at the beginning of the batch, make the calls the application needs and at the end add `token.approve(target,0)`

With this pattern, the user is no longer “plagued” with dangling approvals.

