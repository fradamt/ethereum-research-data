---
source: ethresearch
topic_id: 14106
title: EIP-5875 Opcode for TXNUM
author: xinbenlv
date: "2022-11-04"
category: EVM
tags: []
url: https://ethresear.ch/t/eip-5875-opcode-for-txnum/14106
views: 1282
likes: 0
posts_count: 1
---

# EIP-5875 Opcode for TXNUM

Hi, all I am proposing EIP-5875 to add opcode to retrieve TXNUM

A TX is an *atomic* point of time for world state.

Currently we have access to `blocknum` but there is no way to access a `txnum` within a smart contract.

We hereby propose a `TXNUM` opcode instruction to fetch TXNUM which can be used to

1. identify the ordering of exact transaction in its block
2. Better than blockNum: identifying uniquely and unambiguously the world state.
3. Better than txHash: allow simply arithmatic by BlockNum.TxNum

It would be helpful for on-chain and off-chain indexing and snapshotting.

An example of use-case is [EIP-5805 Voting with Delegation](https://ethereum-magicians.org/t/eip-5805-voting-with-delegation/11407) wants to store snapshot of voting rights. The current option with with either block.timesamp or block.number all only have the granularity at the level of blocks. But world state changes across transaction. If there is any TX in the same block cause a voting right to change, the blocknum or block.timstamp will not be sufficient to pin-point the world state of snapshot of voting rights.

Please share your feedback in the main discussion thread

https://ethereum-magicians.org/t/eip-5875-opcode-for-tx-number-in-a-block/11612
