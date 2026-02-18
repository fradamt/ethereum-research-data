---
source: ethresearch
topic_id: 8580
title: Custody provider hack
author: kladkogex
date: "2021-01-27"
category: Economics
tags: []
url: https://ethresear.ch/t/custody-provider-hack/8580
views: 838
likes: 0
posts_count: 1
---

# Custody provider hack

**TL;DR**

Most custody providers charge a large fee (0.5% per year) for token custody. There is a hack to totally avoid paying this fee.

**Description**

The funny thing is that the hack described below allows anyone to totally avoid paying the fee while keeping exactly the same security. Namely, to steal the money you need to hack the provider.

Here is how it works:

1. You open an NFT token deposit account with a custody provider, and get a wallet address (WA)
2. You then deposit your money (say $1B) as well as an NFT  into a smart contract SC.
3. To send money to someone,  you first send a request to the SC. The SC records the request and sends the NFT token to WA.
4. You then access your custody provider wallet, and simply send the NFT token back to the SC address.
5. When the SC receives the NFT token, it executes the money transfer.

Note that you effectively custody $1B, but only pay to custody a single NFT token!

This can also be done using ERC-20 instead of NFT.
