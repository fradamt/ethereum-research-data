---
source: magicians
topic_id: 6810
title: "EIP-3709: Deprecate Type 1 Transactions"
author: greg
date: "2021-08-07"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-3709-deprecate-type-1-transactions/6810
views: 2828
likes: 5
posts_count: 5
---

# EIP-3709: Deprecate Type 1 Transactions

This is the discussion for [EIP-3709](https://github.com/ethereum/EIPs/pull/3709/files).

## Replies

**q9f** (2021-12-23):

What about deprecation of legacy transactions too?

---

**greg** (2021-12-23):

There is a strong argument that there could be “stowed away” transactions signed off with legacy. Breaking those could cause some serious concern.

---

**q9f** (2022-01-14):

> gas_price: Should be removed in favour of max_fee_per_gas & max_priority_fee_per_gas (see EIP-1559 for proper usage).

How would a wallet provider implement this? It needs to warn the user to enter updated values for max fee and priority fee? I don’t see how that would work in an automated manner unless you set the priority fee to 0 and max fee to gas price.

If this is the intention of the proposal, we could implement the same for legacy transactions as the difference is the same, plus setting the access list to `[]`.

---

**greg** (2022-01-14):

Wallet provider would have to reject the ability to create legacy or type 1 all together.

If you were to automate the process, you could set the `max_fee_per_gas` to equal the `gasPrice` and the `max_priority_fee_per_gas` to whatever the standard is, `1` or `2`? Either way the end user is paying less.

