---
source: magicians
topic_id: 5422
title: "EIP-911 (?) : circuit breaker standard for smart contracts"
author: crypto-pumpkin
date: "2021-02-26"
category: Magicians > Primordial Soup
tags: [security, smart-contracts]
url: https://ethereum-magicians.org/t/eip-911-circuit-breaker-standard-for-smart-contracts/5422
views: 744
likes: 1
posts_count: 1
---

# EIP-911 (?) : circuit breaker standard for smart contracts

This topic is for discussion of a circuit breaker standard for smart contracts.

Some projects have implemented a circuit breaker, including Maker, Cover, Ruler, etc., where a responder (usually a multi-sig) can (and only) pause critical functionalities (chosen by the project) on the smart contract when abnormal activities detected.

Each implementation is different.

One example is on the [BonusRewards.sol](https://github.com/CoverProtocol/cover-rewards/blob/main/contracts/BonusRewards.sol#L245-L248) from Cover Protocol.They have used a list of responders.

A standardized circuit breaker would benefit a lot of projects and enable tons of possibilities like a Global Responder Group DAO who can act as a guard towards exploits.

I am pretty new to the space and wanted to start the conversation here to hear your opinion on this.
