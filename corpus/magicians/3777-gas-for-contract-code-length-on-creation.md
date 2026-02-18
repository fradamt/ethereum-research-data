---
source: magicians
topic_id: 3777
title: Gas for contract code length on creation
author: efn
date: "2019-11-13"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/gas-for-contract-code-length-on-creation/3777
views: 601
likes: 0
posts_count: 2
---

# Gas for contract code length on creation

Hello,

I was working on recreating contracts in multiple shards and measuring gas by the operations when I observed that a transaction pays for gas based on the contract’s length even when the contract code already exists.

When contract code exist nothing is really altered in the db so the costs are very inflated, that’s it if you don’t save the code in the transaction.

Instead of passing code in a transaction one could pass the hash under which the code already exists, saving a lot of gas in the process.

## Replies

**Agusx1211** (2019-11-22):

A version of this already exists, using a [MinimalProxies](https://github.com/ripio/marmo-contracts/blob/master/contracts/commons/MinimalProxy.sol) to delegate all calls to a “source” contract, is worth noticing that this “proxy” solution has two drawbacks, it has to write each contract to the database and also it has to load two contracts (and that adds an additional gas cost on each call).

How does the contract code storage “pruning” currently works? What happen if you selfdestruct a contract that has a “duplicated” one? does the db keeps a counter with how many accounts are using that code? does the database never deletes the code of selfdestruct contracts?

