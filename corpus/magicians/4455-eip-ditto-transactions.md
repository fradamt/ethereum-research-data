---
source: magicians
topic_id: 4455
title: "EIP: Ditto Transactions"
author: rook
date: "2020-07-28"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-ditto-transactions/4455
views: 710
likes: 1
posts_count: 3
---

# EIP: Ditto Transactions

This a proposal to address the problem of high transaction fees and scalability.  By having a smaller transaction type, individuals will pay lower gas fees - and the network as a whole can confirm more transaction in a block - thus preserving Inclusive Accountability.  As apart of EIP-1, any EIP should get feedback prior to sending a PR.  So here is my proposal:


      [github.com](https://github.com/TheRook/EIPs/blob/master/EIPS/eip-TODO.md)




####

```md
---
eip:
title: Ditto Transactions
author: Michael Brooks
discussions-to:
status: Draft
type:
category (*only required for Standard Track):
created:
requires (*optional):
replaces (*optional):
---

## Simple Summary
A ditto transaction allows for a user to duplicate any previously confirmed transaction.  A transaction has multiple fields that maybe useful to re-use, which includes script code that makes up the smart contracts. A ditto, or copy of an existing transaction is the smallest form of a signed signature that can be used to convey value across the Ethereum network. A smaller transaction size reduces gas prices and frees up more confirmation bandwidth.

## Abstract
If some previous transaction shares simulators with a transaction a user is about to make, then fewer bytes of data are needed to represent this transaction to the blockchain. Because previously confirmed transaction are immutable and global, they can be referenced and reused.

## Motivation
```

  This file has been truncated. [show original](https://github.com/TheRook/EIPs/blob/master/EIPS/eip-TODO.md)

## Replies

**matt** (2020-07-28):

Hi [@rook](/u/rook), thanks for you post! Two quick pieces of feedback:

1. It looks like you’re missing the preamble for your EIP (the part sandwiched by ---).
2. We’ve recently achieved an EFI status for EIP-2718. I would recommend that you specify your new transaction type using that standard.

---

**rook** (2020-07-28):

Great feedback - on it!

