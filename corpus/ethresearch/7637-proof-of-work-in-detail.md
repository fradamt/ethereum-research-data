---
source: ethresearch
topic_id: 7637
title: Proof of work in detail
author: Joncarre
date: "2020-07-04"
category: Cryptography
tags: []
url: https://ethresear.ch/t/proof-of-work-in-detail/7637
views: 1381
likes: 1
posts_count: 5
---

# Proof of work in detail

Hello guys!!

First of all, excuse me if this post doesn’t go here. I’m trying to find out if it’s possible to encrypt data at the Ethereum and how the proof of work works in detail. Let me explain: I’ve read papers about frameworks for encrypting information, but I don’t know if this is correct. In the blockchain, should all the information be (obligatorily) visible, or is there a way to encrypt the data (or a little part) of a transaction? This concept is a bit annoying for me because if the information could be encrypted, then the network nodes could not perform the proof of work and validate the transaction, right?

I’m having a hard time finding information about this, can anyone help me? Any reliable link about these concepts would help me a lot. Thank you!!!

## Replies

**barryWhiteHat** (2020-07-04):

[en.wikipedia.org](https://en.wikipedia.org/wiki/Zero-knowledge_proof)





###

In cryptography, a zero-knowledge proof (also known as a ZK proof or ZKP) is a protocol in which one party (the prover) can convince another party (the verifier) that some given statement is true, without conveying to the verifier any information beyond the mere fact of that statement's truth. The intuition behind the nontriviality of zero-knowledge proofs is that it is trivial to prove possession of the relevant information simply by revealing it; the hard part is to prove this possession wit In...

---

**Joncarre** (2020-07-04):

Ty! ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=14) Ok, ok. Got it. But… Does this mean that the information is public but not readable?

Also, I read that the transaction information is encrypted with a hash and stored in the merkle tree. If this is so, then no one should be able to read the information (because it is encrypted), right? Or is this tree only used to have a hierarchy of transactions and does not interfere at all in the proof of work?

What am I getting wrong?

---

**barryWhiteHat** (2020-07-05):

> Does this mean that the information is public but not readable?

Everything is public execpt for stuff that we use ZKPs to hide.

> Also, I read that the transaction information is encrypted with a hash and stored in the merkle tree.

Hash != encryption all data is stored in merkle tree. But anyone can reconsturct the whole tree. this is one of the central secuirty problems of block chain. It is called the data availability problem. It means everyone has the data to reconstruct the merkle tree.

---

**Joncarre** (2020-07-05):

So all the information is public… What if I encrypt information in a Smart Contract? Could the nodes validate my transactions by not knowing the data?

Thanks again btw ^^

