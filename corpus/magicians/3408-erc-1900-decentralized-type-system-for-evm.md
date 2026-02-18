---
source: magicians
topic_id: 3408
title: ERC-1900 Decentralized Type System for EVM
author: jpitts
date: "2019-06-25"
category: EIPs
tags: [interop, data-types, erc-1900]
url: https://ethereum-magicians.org/t/erc-1900-decentralized-type-system-for-evm/3408
views: 901
likes: 0
posts_count: 1
---

# ERC-1900 Decentralized Type System for EVM

[ERC-1900](https://github.com/ethereum/EIPs/issues/1882) proposes a decentralized Type System for Ethereum, an on-chain type registry, and using these resources in order to separate definitions & rules from data in smart contracts.

https://medium.com/@loredana.cirstea/dtype-decentralized-type-system-functional-programming-on-ethereum-4f7666377c9f

> Aside from the type libraries and storage contracts, developers can create  contracts or libraries with pure functions , that know how to interact with the chosen types. We are separating business logic from the state. And this is the first step to a general functional programming system on Ethereum.
>
>
> If you register these pure functions in the  dType Registry  and tell the Registry what type of inputs and outputs the function has, you can start doing some awesome things. You can have automation in the system.

And the implications are big considering possible future inter-op with the proposed Libra network, and finding commonality with Libra’s smart contracts (known as “Move Modules”).

https://medium.com/@loredana.cirstea/ethereum-libra-and-a-unified-type-system-7cafa6ea0bc0
