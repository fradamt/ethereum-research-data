---
source: magicians
topic_id: 17640
title: "ERC-7582: Modular Accounts with Delegated Validation"
author: nerderlyne
date: "2023-12-25"
category: ERCs
tags: [erc, account-abstraction, eip-4337]
url: https://ethereum-magicians.org/t/erc-7582-modular-accounts-with-delegated-validation/17640
views: 1442
likes: 6
posts_count: 2
---

# ERC-7582: Modular Accounts with Delegated Validation

A proposal for efficiently adding (nonce-encoded) plugin functionality to ERC4337 (modular accounts) without requiring any new interface by leveraging the existing Entry Point accounting structure:

https://github.com/ethereum/ERCs/pull/170

[![base-flow](https://ethereum-magicians.org/uploads/default/optimized/2X/d/ddd2318249422b76a034798af5bea04020e7494c_2_495x500.png)base-flow1185×1196 30.5 KB](https://ethereum-magicians.org/uploads/default/ddd2318249422b76a034798af5bea04020e7494c)

## Replies

**nerderlyne** (2024-06-29):

Just published a package convenience for working with `ERC7582` nonce extraction (the validator encoded in nonce is what receives the `validateUserOp` and validates return): [GitHub - nerderlyne/eip-7582-utils: helpers](https://github.com/nerderlyne/eip-7582-utils)

A reference `ERC7582` account: https://eips.ethereum.org/assets/eip-7582/MADVAccount.sol

Can install directly via `npm install eip-7582-utils viem`

`ERC7582` has now progressed to `draft` stage. Please provide any comments or requests before we finalize. Thanks!

