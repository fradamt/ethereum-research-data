---
source: magicians
topic_id: 21501
title: "ERC-7798: Tap to Pay"
author: amhed
date: "2024-10-29"
category: ERCs
tags: [erc, payments]
url: https://ethereum-magicians.org/t/erc-7798-tap-to-pay/21501
views: 162
likes: 3
posts_count: 4
---

# ERC-7798: Tap to Pay

This ERC defines a standard for contactless payment transactions that can allow for interoperable customer to merchant onchain payments, regardless of the wallets the customer and merchant are using.

**Comprised of three parts:**

- A new Ethereum Provider JavaScript API method called requestContactlessPayment
- An agreement on the payload for data exchange between the parties
- An optional mechanism for relaying large JSON payloads using a backend relayer

https://github.com/ethereum/ERCs/pull/686

## Replies

**hellohanchen** (2024-11-04):

How is this compatible with account abstraction?

---

**amhed** (2024-11-04):

This would just be a mechanism for signaling the intent of paying over NFC, the signing or account format is irrelevant for this specific standard

---

**radek** (2024-11-06):

How do you pass the intention reference and further reconcile the payment with that intention?

We have created ERC-7699 for the ERC20 for that, but welcome any other suggestions.

