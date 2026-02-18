---
source: magicians
topic_id: 4422
title: "EIP-1337: Subscriptions on the blockchain"
author: matt
date: "2020-07-15"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-1337-subscriptions-on-the-blockchain/4422
views: 3775
likes: 1
posts_count: 6
---

# EIP-1337: Subscriptions on the blockchain

Discussion thread for [EIP-1337: Subscriptions on the blockchain](https://github.com/ethereum/EIPs/blob/b43e387c1b0e74c14913a16b271c738893c2e9c9/EIPS/eip-1337.md).

Please note that this EIP has been discussed in many places in the past:

- https://github.com/ethereum/EIPs/pull/1337
- https://github.com/ethereum/EIPs/issues/948
- https://medium.com/gitcoin/technical-deep-dive-architecture-choices-for-subscriptions-on-the-blockchain-erc948-5fae89cabc7a
- https://github.com/EthereumOpenSubscriptions/standard
- https://gitcoin.co/slack

This thread should be the canonical thread for discussion going forward to avoid anymore fragmentation.

## Replies

**Derked** (2021-08-20):

What’s the status of this? I’m having trouble finding good information. I am very interested in using this type of subscription model in an app I’m working on. Is the contract safe to use? Is there work left to be done? Any information would be helpful. Thanks!

---

**matt** (2021-08-20):

The EIP is still in draft. I haven’t heard of any additional progress on this.

---

**Fran23** (2021-08-26):

While AFAIK there are a few implementations of EIP-1337 that made it into production, I’d invite you to checkout [superfluid](http://superfluid.finance) as a subscription solution, which has been running in production for a few months now

---

**maxareo** (2021-08-29):

Hey [@matt](/u/matt) , not sure if you have thought about on-chain subscription this way, but a EIP-3754 vanilla NFT standard may help take this further. Check it out [here](https://github.com/ethereum/EIPs/issues/3753).

---

**greentriangles1** (2021-09-29):

How do the developers ever plan on service providers being able to charge ERC20 tokens when ERC20 tokens require approval on the end user?

The end user could hypothetically approve the maximum amount (2^256), but that enables the possibility of the service provider to just take all their coins.

Wouldn’t an alternative coin standard need to be invented? The new approval function would take in a start date and a period length (monthly, yearly, etc.), and the provider could only charge once within the start date and period length (and then the start date would be updated to the latest timestamp)

