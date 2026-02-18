---
source: magicians
topic_id: 2278
title: Root contract for governed sidechains
author: rumkin
date: "2018-12-22"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/root-contract-for-governed-sidechains/2278
views: 519
likes: 1
posts_count: 1
---

# Root contract for governed sidechains

Today any account can create any contract and transfer tokens to anyone on blockchain. This is good for general blockchain but not for something special like corporate or community chain, which need to have more control. This suggestion provide description of the Root contract which is using to resolve permissions:

- who can transfer coins,
- who can create contract,
- which contract code could be deployed.

As an option root contract can be located at pseudo-address `0x00`, that will solve missed funds problem.

Contract interface:

```
contract Root {
    function canTransfer(address _from, address _to, uint256 _amount) returns(bool) {}
    function canCreateContract(address _from, bytes _code, bytes _args) returns(bool) {}
    function withdraw(address _to, uint256 _amount) public {}
}
```

This allows to create full specter of chains from centralized to fully decentralized.

## Simple example

Suppose I’m going to create a chain which driven by group of experts like TC39 or WhatWG. All contracts should be specified and published only by this group. This is what for `canCreateContract()` exists. This group creates contracts factories and publish to the network. Then this group grants permission to create contracts to this factory contract. When user decided to publish a contract he call one of the factory’s methods instead of directly publishing contract code.

The other limitation that could be realized is payments. For example this network supports only account-to-contract and contract-to-account transactions. This is possible with `canTransfer()` which receives sender and receiver of the transfer and decide is payment allowed.
