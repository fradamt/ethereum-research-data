---
source: magicians
topic_id: 16876
title: Payment Splitter 2.0
author: Garito
date: "2023-11-30"
category: Magicians > Process Improvement
tags: [payments]
url: https://ethereum-magicians.org/t/payment-splitter-2-0/16876
views: 666
likes: 1
posts_count: 2
---

# Payment Splitter 2.0

Hi

I’m trying to develop a version 2.0 of payment splitter since v1.0 has been deprecated

in that version, I would like to use an ERC20 as shares and make it dynamic (on v1.0 the share distribution is static at deployment time)

I have the naive algorithm looping all stakeholders when a payment arrives. This should be unacceptable since will be O(n)

Can you help me develop the O(1) withdraw algorithm?

Thanks

## Replies

**matejfalat** (2023-11-30):

Hi, maybe take a look at [this](https://etherscan.io/address/0xce9f5cCdE61528e2d5625c86bFEFc0054DE4E592#code). It’s called staking but it’s the same thing, ERC20 as shares and O(1) withdrawals and ETH deposits.

