---
source: magicians
topic_id: 6058
title: "EIP 3520: Transaction Destination Opcode"
author: alex-ppg
date: "2021-04-20"
category: EIPs > EIPs core
tags: [evm, opcodes, core-eips]
url: https://ethereum-magicians.org/t/eip-3520-transaction-destination-opcode/6058
views: 2244
likes: 0
posts_count: 1
---

# EIP 3520: Transaction Destination Opcode

Hello everyone,

Given the inclusion ever-growing for smart contracts to be inter-connected, I wanted to come up with an idea to aid developers in building “smarter” multi-contract systems by being able to apply introspection to the entrypoint of a blockchain transaction.

Put briefly, I have introduced a new EVM instruction that permit introspection to be applied to the original transaction data by being able to access the original `data` payload as well as the original recipient of the transaction, the `to` address. This would primarily allow more complex types of “basic” contracts to be created, such as ERC-20 tokens that are aware of exactly what type of action (i.e. “buy” or “sell”) is performed on a DEX like Uniswap.

To properly function, it relies on EIP-3508 which still in a Draft phase.

Let me know your thoughts.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/3520)














####


      `master` ← `alex-ppg:transaction-destination-eip`




          opened 11:37AM - 20 Apr 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/5/578753eaaa997ff602b43c278bd0e4a3342f0d20.jpeg)
            alex-ppg](https://github.com/alex-ppg)



          [+93
            -0](https://github.com/ethereum/EIPs/pull/3520/files)







Hello,

This PR is meant to introduce a new EIP for accessing a transaction's […](https://github.com/ethereum/EIPs/pull/3520)original recipient to allow advanced forms of introspection to manifest.

Feedback is welcome on all points.
