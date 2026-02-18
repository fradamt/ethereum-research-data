---
source: ethresearch
topic_id: 5524
title: Fast Multiparty Threshold ECDSA possible on Ethereum today?
author: SCBuergel
date: "2019-05-29"
category: Cryptography
tags: [signature-aggregation]
url: https://ethresear.ch/t/fast-multiparty-threshold-ecdsa-possible-on-ethereum-today/5524
views: 2107
likes: 8
posts_count: 3
---

# Fast Multiparty Threshold ECDSA possible on Ethereum today?

I just came across [this paper](https://eprint.iacr.org/2019/114.pdf) when discussing multi-signature schemes that do not involve smart contracts and instead would work on protocol-level today. I’m wondering if anyone is doing research and development in that direction as it would save us a lot of multisig pains. It seems that the it is possible to run such a setup on consumer hardware today.

Some motivations:

1. Much more gas efficient multi-signature transactions
2. Much more efficient multisig setup: Today, deploying 1000 multi-sigs would be super expensive. Taking 1000 keys to obtain 1000 threshold addresses would not require any on-chain activity at all.

## Replies

**seresistvan** (2019-05-29):

[@omershlo](/u/omershlo) and KZen already did a great effort to implement the before mentioned threshold ECDSA paper. Have a look [here](https://github.com/KZen-networks/multi-party-ecdsa). Also you might be interested in this mixer protocol which uses threshold ECDSA. We’ve recently published it on e-print. See that [here](https://eprint.iacr.org/2019/563.pdf).

---

**burdges** (2019-06-03):

Also https://github.com/KZen-networks/multi-hop-locks

