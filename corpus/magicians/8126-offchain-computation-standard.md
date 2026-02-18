---
source: magicians
topic_id: 8126
title: Offchain computation standard
author: npasquie
date: "2022-01-27"
category: Magicians > Primordial Soup
tags: [erc, eip, gas-saving]
url: https://ethereum-magicians.org/t/offchain-computation-standard/8126
views: 929
likes: 2
posts_count: 1
---

# Offchain computation standard

Hello Magicians ![:sparkles:](https://ethereum-magicians.org/images/emoji/twitter/sparkles.png?v=15),

This is a pre-PR discussion for the EIP : Offchain computation standard. You can find a first version here : [EIPs/EIPS/eip-xxxx.md at master · npasquie/EIPs · GitHub](https://github.com/npasquie/EIPs/blob/master/EIPS/eip-xxxx.md)

# Simple Summary

Standard to request & access offchain computed data while preserving composability

# Abstract

A standard API is proposed to request & access offchain-computed data in smart-contracts in a composable way. It includes a smart-contract on chain and specifications for clients.

# Motivation

Off-chain computation checked on-chain has become a common pattern in Dapps, virtually enabling usage of large data sets or complex computations in smart contracts within their limited resources. This is usually achieved through a script in a front-end app generating the correct parameters required by a contract call for a transaction signature. This pattern is by nature non-composable, any protocol that needs to be integrated by other protocols must resolve to implement those costly operations on chain.

The proposed new standards would greatly broaden the possibilities of smart-contract developers, especially in the interactions accross protocols. L2-scaling alone can’t provide this kind of application-specific optimisations.

Any reflexion/feedback is greatly appreciated ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)
