---
source: magicians
topic_id: 1320
title: Tools for implementing EIP-681 and EIP-831
author: brunobar79
date: "2018-09-12"
category: EIPs
tags: [tooling, qr-codes, eip-831, eip-681, url-parsing]
url: https://ethereum-magicians.org/t/tools-for-implementing-eip-681-and-eip-831/1320
views: 3015
likes: 8
posts_count: 6
---

# Tools for implementing EIP-681 and EIP-831

Cross posting from [github](https://github.com/ethereum/EIPs/pull/681#issuecomment-420779728)

Hey guys, just wanted to share two tools here that might be useful for people trying to implement this EIPs on their end:

- eth-url-parser - JS module that handles parsing and building ethereum standard urls
- link generator - Web app that allows you to generate valid ethereum links (and it’s corresponding QR code)

Note: I wrote both in a rush so please lmk if you find any issues with it (or even better submit a PR and fix it!)

## Replies

**josefrichter** (2021-05-25):

I was looking into payment links and QR codes recently. It seems like EIP-681/831 are not properly implemented in almost any wallet, for some reason. When you generate a payment link/QR, most wallets will pick up just the recipient address, but ignore the amount and currency/contract. What’s worse, I didn’t find a single wallet that would allow generating the QR codes. Is there a reason why all this is largely ignored?

The typical use case is this:

1. I go to coffeeshop and buy a coffee for $5
2. The merchant types 5 USDC to his wallet (or point-of-sale terminal) and generates a payment QR
3. I scan the code and just confirm the payment

^ this is very much akin to how payment cards / applepay work nowadays

I understand that current gas prices are not feasible for micropayments, but that may soon change with eth 2.0 and/or layer 2 solutions.

One bonus use case would be if both recipient and sender could set the currency, and it would be converted during the transaction. In other words, the merchant accepts only USDC, but I hold only EURT in my wallet, I still want to be able to transact before going to dex first.

Anyway, is any of the above possible, or are there some obstacles I am not aware of? Thank you.

---

**ligi** (2021-05-26):

Yea - this is the unfortunate reality. I think nowadays one should go the WalletConnect route. And due to the bidirectional nature of WC you can even improve the UX of your use-case by querying the address first - then analyzing which assets the user has (on which chain/layer) that you would like to trade for your goods or services.

---

**josefrichter** (2021-05-30):

[@ligi](/u/ligi) Not sure I understand - you can use WC for micropayments somehow? Or how do you mean?

---

**ligi** (2021-06-01):

You can do with WC all that 681 and 831 can do. And yea also micropayments should be possible.

---

**php4fan** (2022-06-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/josefrichter/48/3976_2.png) josefrichter:

> Is there a reason why all this is largely ignored?

The reason is that the people developing wallet apps are stupid.

