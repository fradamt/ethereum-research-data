---
source: magicians
topic_id: 12131
title: Ethereum invoices
author: ProgramFilesx86
date: "2022-12-13"
category: EIPs
tags: [evm]
url: https://ethereum-magicians.org/t/ethereum-invoices/12131
views: 491
likes: 0
posts_count: 2
---

# Ethereum invoices

In may centralized finance systems we can pay via invoices, but in ethereum I missed that in may cases so I decided to build a one, a simple standard to create, pay, cancel invoices which users can use it to pay invoices with specific token, and amount of it as well

The standard example can be found at : [GitHub - ProgramFilesx86/example-invoice-standard](https://github.com/ProgramFilesx86/example-invoice-standard)

Create : to create an invoice

Pay : to pay a specific invoice

Cancel : to cancel a specific invoice

this standard can be implemented as contracts by tokens (as such usdc / dai) so users will use it to pay their invoices with such tokens, the token company will have fees as well

and many other cases can be used

## Replies

**anett** (2022-12-14):

I don’t think so we need standard for Ethereum Invoices. There are projects like [Request](https://www.request.finance/) which works great

