---
source: ethresearch
topic_id: 5062
title: "Blockchains must be MEV-free: BLS Threshold Encryption"
author: kladkogex
date: "2019-02-26"
category: Security
tags: []
url: https://ethresear.ch/t/blockchains-must-be-mev-free-bls-threshold-encryption/5062
views: 2498
likes: 0
posts_count: 4
---

# Blockchains must be MEV-free: BLS Threshold Encryption

At Skale, we need to do threshold encryption in our PoS chains in order to provide protections against front running (essentially a transaction is submitted to the chain in encrypted form, and then decrypted after it has been committed.

We already have BLS signatures implemented in a way compatible to precompiles from ETH 1.0. I am looking for a spec to implement threshold encrypt/decrypt using the same primitives and pairing used in BLS signatures.

## Replies

**lithp** (2022-02-24):

Years have passed but for future travellers [this scheme](https://protocollabs.notion.site/Timelock-Encryption-drand-f5df65a54a6641dfa77f9b8168c9b90b) seems relevant to the question. Using something like this anyone can encrypt their transactions and a threshold of peers is required to decrypt those transactions and it all happens with the BLS machinery.

---

**kladkogex** (2024-10-28):

Bumping this up since the topic has become trendy again.

I think people realized that MEV is simply not the way.  It is immoral and does not even happen on centralized exchanges.

---

**kladkogex** (2024-10-28):

Thanks! We will look into it !

Here is a talk from one of our developers on SKALE implementation

  [![image](https://ethresear.ch/uploads/default/original/3X/4/2/42e54b2fbc9b7e315eee84d3c07cc7ab723c4d61.jpeg)](https://www.youtube.com/watch?v=8RcU7fliHII)

