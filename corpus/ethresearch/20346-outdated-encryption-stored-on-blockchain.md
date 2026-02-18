---
source: ethresearch
topic_id: 20346
title: Outdated encryption stored on blockchain
author: knev
date: "2024-08-28"
category: Security
tags: []
url: https://ethresear.ch/t/outdated-encryption-stored-on-blockchain/20346
views: 241
likes: 4
posts_count: 7
---

# Outdated encryption stored on blockchain

Please pardon my ignorance. I’ve read several publications related to blockchain being used in healthcare, construction and the like. Many of these publications state that blockchain allows the storage of secured data.

My question is this: If data is “securely” stored on blockchain (I assume encrypted) and the encryption algorithm LATER (after long-term usage) is proven to be “cryptographically broken” (e.g., SHA-1) …

- does this not mean all “secured” data on the blockchain using that algorithm is suddenly public?
- are there steps that can be taken to re-encrypt the data to avoid the massive leak of data?

Kind regards.

## Replies

**MicahZoltu** (2024-08-28):

Anytime you publish some encrypted data publicly, you should assume that if the encryption algorithm is ever broken then the data is now public.  This is true for *all* systems of publishing encrypted data publicly, including blockchains.

---

**knev** (2024-08-28):

Then it is entirely unclear to me how something like patient record in healthcare applications can be put on the blockchain. And, how these articles can claim that blockchain will provide secure data storage. Yes, the data can be anonymized, but that has also been proven to only have limited success.

---

**MicahZoltu** (2024-08-29):

My guess is that it is assumed that cryptography won’t be broken.  FWIW, it is also assumed that healthcare databases won’t be hacked, but history suggests that is more likely than cryptography getting broken, so I don’t think that public+encrypted is any better than private+unencrypted.

---

**mratsim** (2024-08-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/knev/48/17256_2.png) knev:

> I’ve read several publications related to blockchain being used in healthcare, construction and the like.

Do you have a link to those publications?

---

**knev** (2024-08-29):

Here’s one…

https://doi.org/10.3390/su13042090

> “Blockchain can store data securely and easily for query on the chain, …”
> “Blockchain can efficiently process transactions, secure data, reduce labor costs, and improve transparency and security [87].”

Other publications talk about securely accessing data, which I think is valid, but it is the storing of secured data that I’m concerned with.

---

**parseb** (2024-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/knev/48/17256_2.png) knev:

> it is the storing of secured data that I’m concerned with

Ethereum might prune its records in the future. That might also be of concern.

There’s other more useful things smart contract blockchains aim to shine shine at than storage.

