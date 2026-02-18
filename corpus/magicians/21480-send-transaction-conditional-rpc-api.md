---
source: magicians
topic_id: 21480
title: Send Transaction Conditional RPC API
author: dror
date: "2024-10-27"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/send-transaction-conditional-rpc-api/21480
views: 160
likes: 2
posts_count: 3
---

# Send Transaction Conditional RPC API

This EIP proposes a new JSON-RPC API method `eth_sendRawTransactionConditional` for block builders and sequencers,

enhancing transaction integration by allowing users to express preconditions for transaction inclusion.

This method aims to improve efficiency by reducing the need for transaction simulation,

thereby improving the computational efficiency of transaction ordering.

https://github.com/ethereum/ERCs/pull/682

## Replies

**hellohanchen** (2024-11-03):

What would happen if the RPC provider cheats  users?

---

**dror** (2024-11-05):

This API can be used by users, not only services.

It is equivalent to “flashbots” private API.

The difference is that the service provider has a light check to know if the transaction might fail, and thus is not required to perform full tracing.

Once a transaction pass the validation, the provider should fully trace it. In case the transaction fails, it should drop it - and probably throttle down the caller, since this caller “lied”, by submitting a TX that reverts even if its preconditions are met.

