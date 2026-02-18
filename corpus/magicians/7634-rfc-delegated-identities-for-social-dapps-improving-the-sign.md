---
source: magicians
topic_id: 7634
title: "RFC: Delegated identities for social dApps, improving the \"Sign-in with Ethereum\" UX"
author: hazae41
date: "2021-11-30"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/rfc-delegated-identities-for-social-dapps-improving-the-sign-in-with-ethereum-ux/7634
views: 700
likes: 4
posts_count: 1
---

# RFC: Delegated identities for social dApps, improving the "Sign-in with Ethereum" UX

# Introduction

Currently, there are two major ways of connecting to a social dApp: using a cold account or using a hot account.

## The “cold” account

This account is usually on a cold, hardware, multisig, hard wallet. e.g. Ledger.

It holds your assets (tokens, NFTs, ENS, etc.) and proves your identity (signature, ENS).

While it is secure and trustworthy, it is definitely not practical for social dApps.

Thus, the following actions are a major drawback for users:

- Connecting to the dApp and proving your identity (usually requires a signature)
- Making small, inexpensive transactions: tipping an user, interacting with the blockchain.

## The “hot” account

This account is usually on a hot/software/unisig/soft wallet. e.g. Metamask.

While it is very practical and allows users to quickly get on track, it can be compromised.

Thus, it is definitely not safe to use it for holding assets and proving your identity, as both can be compromised.

# Proposal

My proposal is to have the best of both worlds by allowing users to **delegate their cold account’s identity to a hot account**.

You would connect for the first time to a dApp with your cold wallet for proving your identity, and then you would be able to delegate this identity to your hot wallet. You can then connect with both, and **can undo this delegation at any time**; just like you can remove an access token from your Github account, or disallow a device from using your Google account.

From the dApp perspective, an user can make actions either on-chain (on the blockchain) or off-chain (on a traditional server/database architecture). Both on-chain and off-chain actions can be separated into two categories.

## Weak actions

Those actions are usually small, inexpensive, not important.

They are feasible by both cold and hot accounts.

They do not have a large impact if the hot account is compromised.

For example:

- Tipping an user with a small amount (e.g. <$10)
- Posting something (off-chain or on-chain)
- Following an user, group, channel, topic, etc.
- Modifying the user’s profile (name, avatar, bio)
- Messaging someone (see next part for details)

## Strong actions

Those actions are usually expensive, important.

They are only doable by the cold account, for security reasons.

For example:

- Creating, minting, staking, transfering, withdrawing assets
- Modifying “hard” parts of the user’s profile (e.g. email address)
- Creating/deleting a social page, or some important stuff
- Undoing the delegation

# Technical considerations for even more secure dApps

The dApp could show which account was used when creating a post (e.g. a lock icon near the username).

The dApp could store an history of all actions made by the hot account, and could allow the user to rollback those actions if the hot account gets compromised.

For private conversations, each conversation could be hot or cold. Cold conversations would be used for even more private stuff. This way, if the hot account gets compromised, those conversations do not leak. While still allowing the hot account to quickly message someone.

# Implementation

The delegated identity system, while being more secure, can be somewhat hard to implement from both design and development perspectives.

On the design side, it needs to be clear for the end user how this system works.

Also, the dApp needs to define which action is strong and which one is weak.

On the development side, the dApp needs to abstract two accounts into one identity/profile, this can be hard to implement for existing social dApps. The dApp may also allow existing users to move their identity to a cold wallet when they first connected with a hot wallet.

Also, the action of delegating an identity to another account needs to require both accounts to accept it. Once the delegation is made, the hot account would see his identity/profile removed and replaced by the cold account’s identity. The hot account won’t be able to delegate his new identity to yet another account.

# Your comments are welcome
