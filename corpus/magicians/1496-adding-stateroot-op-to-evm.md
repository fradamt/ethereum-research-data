---
source: magicians
topic_id: 1496
title: Adding StateRoot OP to EVM
author: adamskrodzki
date: "2018-09-30"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/adding-stateroot-op-to-evm/1496
views: 669
likes: 0
posts_count: 1
---

# Adding StateRoot OP to EVM

Hi everyone,

below is thing I found missing in EVM

Like Now there exist

BLOCKHASH

Geting the hash of one of the 256 most recent complete blocks

there should be:

BLOCKSTATEHASH

returning stateRoot same way BLOCKHASH returns hash

That would allows for much easier on-Chain merkle proofs of former state of a blockchain

Example usecase On-Chain Voting that do not require token locking and still prevent multiple votes with same tokens
