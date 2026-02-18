---
source: magicians
topic_id: 3922
title: Saving the hash of a smart contract on Blockchain
author: samyborto94
date: "2020-01-11"
category: Uncategorized
tags: [questions]
url: https://ethereum-magicians.org/t/saving-the-hash-of-a-smart-contract-on-blockchain/3922
views: 1004
likes: 0
posts_count: 2
---

# Saving the hash of a smart contract on Blockchain

Hello everyone,

I am new here and to Blockchain technology, so I have some tricky questions for you :).

If I want to save data, for example transactions between two, on the Blockchain.

1. Is it possible to save only the hash on the blockchain and the rest on a cloud?
2. If I save the hash of the data on the Blockchain, is the data still as save as saving all the data on the Blockchain?
3. What else than saving storage is the difference between saving only the hash and saving all the data on the Blockchain?

I also got some questions concerning smart contracts. For the case that I want a fully automated documentation of transactions between two.

1. Is it possible to create the smart contract on a cloud and save the hash on the blockchain?
2. Does this have any disadvantage? Will the transactions still be recorded as save as on the blockchain?

I would be very glad, if you could answer my questions ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Best

Samy

## Replies

**3esmit** (2020-01-15):

1. Yes, but might not be useful by smart contracts.
2. No, if you need to load from this information you need  the piece you want to use and a proof that that information belongs in the hash stored in the contract. A common way of doing this is using Merkle Trees and it’s variants.
3. The difference is the cost of storage vs the cost of the proof.

Smart contracts are not aware of transactions, only about calls to them. So probably your notion on how things work is not correct.

1. Not possible. There is this research of Sharding, on ETH2.0, and Plasma chain, that would be probably what you are looking for.
2. Plasma is like a subchain with an authority but participants are trustless to leave, it is as you mention only a hash, which uses that merkle trees I mention in very fancy ways. No, in this case transactions are not recorded inchain, they are part of the subchain, which would have its own ledger.

Take a read on https://ethresear.ch/ on what the mages are doing there.

