---
source: magicians
topic_id: 6004
title: ERC-4000 Staking-Reward Pool Standard (request for comments)
author: cryppadotta
date: "2021-04-15"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-4000-staking-reward-pool-standard-request-for-comments/6004
views: 997
likes: 2
posts_count: 2
---

# ERC-4000 Staking-Reward Pool Standard (request for comments)

Staking-reward pools are a common way for projects to incentivize desired behaviors like providing liquidity, bonding, token distribution, or loan origination, but nearly every project implements the interface differently.

Myself, vfat, and DkNinja have drafted [an EIP for an ERC Staking-Reward Pool Standard](https://hackmd.io/@dotta/erc4000-pool-std) based on our experience of writing code to interact with hundreds of “Masterchef-” and "Synthetix-"style staking-rewards pools.

Staking-reward pools are widespread and we believe that the adoption of a standard for staking-reward pools will benefit the entire ecosystem through better user interfaces and composability with smart contracts such as yield aggregators.

In this EIP, we’ve tried to carve a minimal surface area that should be easy for users to understand and require minimal changes from existing pool contracts. (For example, we envision teams should be able to quickly write adapter-proxies for any existing Masterchef-style contracts.)

We’d appreciate your comments here on eth-magicians (or on the hackmd directly) before we move to submitting a formal pull request.

[Link to the draft HackMD](https://hackmd.io/@dotta/erc4000-pool-std)

## Replies

**DeFi_initiate** (2021-04-15):

I commend you for this much-needed initiative!

There are four components that are missing from this proposal in my view. These are:

- Locking and vesting: how much of the stakes/rewards are locked, for how long, and what is the vesting (unlocking) schedule
- Fees and taxes: deposit, withdrawal and performance fees, burning schedule, transaction tax, reflection
- Farm information: name, website, and other attributes such as contact info and social media accounts
- Chain information: I imagine you would like to have this standard also adopted for the Binance Smart Chain (and other compatible chains). If so, specifying the chain would be advisable.

These are very important considerations for users, and lacking an easy mechanism to collect this data will reduce the usefulness of the standard.

Other than the above, the proposal seems comprehensive and well-thought-out. You may want to include an Applications section, in which you could give examples of where and how the standard would be used.

This is a great start - good luck with finalizing it and having it implemented!

