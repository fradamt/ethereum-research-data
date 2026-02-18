---
source: ethresearch
topic_id: 5029
title: Zether - The first privacy mechanism designed for Ethereum
author: MihailoBjelic
date: "2019-02-20"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/zether-the-first-privacy-mechanism-designed-for-ethereum/5029
views: 11889
likes: 11
posts_count: 10
---

# Zether - The first privacy mechanism designed for Ethereum

I thought this might be share-worthy.

Benedikt Bunz (co-author of Bulletproofs), Dan Bohen et al. proposed [Zether](https://crypto.stanford.edu/~buenz/papers/zether.pdf), the first privacy mechanism built specifically for Ethereum, i.e. account-based smart contract platforms. All notable blockchain privacy mechanisms developed so far (the authors refer to 10 of them), were designed for Bitcoin/UTXO-based chains.

Zether provides both confidentiality (by hiding payment amounts) and anonymity (by hiding the identities of senders and recipients).

The mechanism is practical today (no changes to Ethereum protocol required). The authors implemented it as an Ethereum smart contract and a single transaction costs 7M+ gas, but if two already discussed EIPs were to be implemented, it would go down to 1.7M and also the contract itself could be further optimized.

https://crypto.stanford.edu/~buenz/papers/zether.pdf

## Replies

**kunxian-xia** (2019-02-26):

Where can we find the smart contract code for this protocol

---

**kladkogex** (2019-02-26):

great paper ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) we may use this in our network

---

**lovesh** (2019-02-28):

I reviewed this some time ago at https://medium.com/coinmonks/notes-on-zether-towards-privacy-in-a-smart-contract-world-6c4333f975d

---

**MihailoBjelic** (2019-03-28):

Sorry for the late reply [@kunxian-xia](/u/kunxian-xia), here’s a part of the implementation: https://github.com/bbuenz/BulletProofLib/tree/master/src/main/java/edu/stanford/cs/crypto/efficientct/zetherprover.

---

**robert.zaremba** (2019-08-21):

Hi,

What are the benefits of Zether compared to [AZTEC](https://www.aztecprotocol.com/)?

Few differences I can identify:

- Zether is using  the account model (no extra storage required if one is doing many split transactions)
- Zether doesn’t require a  trusted setup, but AZTEC requires it only once for many contracts (they separate the engine into a different smart contract)
- AZTEC is cheaper and easier to reason about.

Any other feedback someone can share?

---

**Boogaav** (2020-03-28):

Hi [@MihailoBjelic](/u/mihailobjelic),

I wonder if you could share what kind of progress have been made and if there are any difficulties you guys faced so far?

---

**axic** (2020-04-15):

From page 19:

> There currently exists an EIP to reduce the gas cost of elliptic curve multiplications by a factor of 6.66 and additions by a factor of 3.33 [bn1b]. A further EIP reduces the cost of calling a precompiled contract [pre] which would reduce the cost for each cryptographic operation by another 700 units of gas. If both of these were implemented, the cost of a Zether transfer would reduce to roughly 1.7 million gas (0.36 USD).

Here [bn1b] refers to EIP-1108 and [pre] refers to EIP-1109.

[EIP-1108](https://eips.ethereum.org/EIPS/eip-1108) went live with Istanbul. [EIP-1109](https://eips.ethereum.org/EIPS/eip-1109) is not planned for Berlin, but an alternative, [EIP-2046](https://eips.ethereum.org/EIPS/eip-2046) is – it is not reducing the cost to 0, but 40 (in its current and not final form).

Wondering if anyone will pick Zether up after these changes go live?

---

**Mikerah** (2020-04-15):

The Blockchain Team at JP Morgan have made significant improvements to the original Zether implementation. Further, they have came up with designs to add anonymity to Zether’s original designs. I would reach out to Benjamin Diamond to see if they would also deploy a version on mainnet Ethereum and not only on Quorum.

---

**nhathuyenqt** (2021-05-16):

Thank you MihailoBjelic for your sharing.

Could you explain the proof for anonymous version?

I don’t understand how to use 1-out-of-many to prove AnonTransfer.

Thank you so much

