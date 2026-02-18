---
source: magicians
topic_id: 18466
title: "ERC-7615: Atomic Push-based Data Feed Among Contracts"
author: lanyinzly
date: "2024-02-03"
category: ERCs
tags: [smart-contracts, onchain, data-push]
url: https://ethereum-magicians.org/t/erc-7615-atomic-push-based-data-feed-among-contracts/18466
views: 1171
likes: 0
posts_count: 2
---

# ERC-7615: Atomic Push-based Data Feed Among Contracts

An Atomic Mechanism to Allow Publisher Contract Push Data to Subscriber Contracts

## Abstract

This ERC proposes a push-based mechanism for sending data, allowing publisher contract to automatically push certain data to subscriber contracts during a call. The specific implementation relies on two interfaces: one for publisher contract to push data, and another for the subscriber contract to receive data. When the publisher contract is called, it checks if the called function corresponds to subscriber addresses. If it does, the publisher contract push data to the subscriber contracts.

## Motivation

Currently, there are many keepers rely on off-chain data or seperate data collection process to monitor the events on chain. This proposal aims to establish a system where the publisher contract can atomicly push data to inform subscriber contracts about the updates. The direct on-chain interaction bewteen the publisher and the subscriber allows the system to be more trustless and efficient.

This proposal will offer significant advantages across a range of applications, such as enabling the boundless and permissionless expansion of DeFi, as well as enhancing DAO governance, among others.

### Lending Protocol

An example of publisher contract could be an oracle, which can automatically push the price update through initiating a call to the subscriber protocol. The lending protocol, as the subscriber, can automatically liquidate the lending positions based on the received price.

### Automatic Payment

A service provider can use a smart contract as a publisher contract, so that when a user call this contract, it can push the information to the subsriber contracts, such as, the users’ wallets like NFT bound accounts that follows ERC-6551 or other smart contract wallets. The user’s smart contract wallet can thus perform corresponding payment operations automatically. Compared to traditional `approve` needed approach, this solution allows more complex logic in implementation, such as limited payment, etc.

### PoS Without Transferring Assets

For some staking scenarios, especially NFT staking, the PoS contract can be set as the subscriber and the NFT contracts can be set as the publisher. Staking can thus achieved through contracts interation, allowing users to earn staking rewards without transferring assets.

When operations like `transfer` of NFT occur, the NFT contract can push this information to the PoS contract, which can then perform unstaking or other functions.

### DAO Voting

The DAO governance contract as a publisher could automatically triggers the push mechanism after the vote is completed, calling relevant subscriber contracts to directly implement the voting results, such as injecting funds into a certain account or pool.

### A Graph Visualization of the Structure

```auto
+---------+               +-----------+                                           +-------------+
| Client  |               | Publisher |                                           | Subscriber  |
+---------+               +-----------+                                           +-------------+
     |                          |                                                        |
     | Call somefunc(...)       |                                                        |
     |------------------------->|                                                        |
     |                          |                                                        |
     |                          | Query Subscriber                                       |
     |                          |-----------------                                       |
     |                          |                |                                       |
     |                          ||
     |                          |                                                        |
     |                          |                                                 Result |
     |                          |







####


      `master` ← `lanyinzly:Contract_push`




          opened 05:48PM - 03 Feb 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/3/3f296adafbbd6e66b286ffb581808bc8faf08266.png)
            lanyinzly](https://github.com/lanyinzly)



          [+359
            -0](https://github.com/ethereum/ERCs/pull/235/files)







Add ERC: Smart Contract Data Push Mechanism

An Atomic Mechanism to Allow Publ[…](https://github.com/ethereum/ERCs/pull/235)isher Contract Push Data to Subscriber Contracts

## Replies

**Arvolear** (2024-12-09):

Could you please elaborate why would anyone consider using the “push over pull” strategy when conventional wisdom says it is either insecure (if one of the batch pushes fail, the whole batch fails) and too expensive to justify?

Usually protocols tend to externalize gas fees (make users pay), rather than paying themselves. To be honest, I think this EIP unwillingly promotes bad development practice and will instantly create technical debt for anyone who uses it.

