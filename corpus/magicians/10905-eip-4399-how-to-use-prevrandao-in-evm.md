---
source: magicians
topic_id: 10905
title: "EIP-4399: How to use PREVRANDAO in evm?"
author: apiscerena
date: "2022-09-17"
category: EIPs
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/eip-4399-how-to-use-prevrandao-in-evm/10905
views: 1739
likes: 0
posts_count: 2
---

# EIP-4399: How to use PREVRANDAO in evm?

I didn’t find the documents about how to use random source in evm using solidity?

Is there a way to access the randao number in a specific block just like the funtion: blockhash(uint blockNumber) returns (bytes32)?

## Replies

**markuswaas** (2023-01-09):

Yes there is, although not yet for a specific block (or slot) number. See [EIP-4399: Supplant DIFFICULTY opcode with RANDOM](https://ethereum-magicians.org/t/eip-4399-supplant-difficulty-opcode-with-random/7368) and also [Solidity Deep Dive: New Opcode 'Prevrandao'](https://soliditydeveloper.com/prevrandao) about this.

