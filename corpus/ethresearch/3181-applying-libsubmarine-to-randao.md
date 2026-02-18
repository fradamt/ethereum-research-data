---
source: ethresearch
topic_id: 3181
title: Applying LibSubmarine to RANDAO
author: Mikerah
date: "2018-09-02"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/applying-libsubmarine-to-randao/3181
views: 2059
likes: 0
posts_count: 2
---

# Applying LibSubmarine to RANDAO

In previous post, Vitalik went over the manipulability of RANDAO ([RNG exploitability analysis assuming pure RANDAO-based main chain](https://ethresear.ch/t/rng-exploitability-analysis-assuming-pure-randao-based-main-chain/1825/5) and [RANDAO beacon exploitability analysis, round 2](https://ethresear.ch/t/randao-beacon-exploitability-analysis-round-2/1980)).

Would applying something like LibSubmarine (https://hackernoon.com/libsubmarine-temporarily-hide-transactions-on-ethereum-cheaply-6910191f46f2?gi=ffb1a94bc2a1) decrease the influence of the last revealer having power over the final random number?

## Replies

**seresistvan** (2018-09-02):

tl;dr Not really.

As of my understanding LibSubmarine could only help in hiding that one is participating in RANDAO at all. With the help of LibSubmarine you can commit to a transaction from a freshly generated Ethereum address **A** of which you do not know the private key by design. So it is impossible to send another transaction from address **A**, meaning that in case of applying LibSubmarine to RANDAO you can easily generate a RANDAO-commit transaction from a freshly generated address **A** , but essentially you can not reveal your RANDAO share since you do not have the corresponding private key of address **A**, so you can not send another transaction from address **A** .

Even if somehow you manage to overcome this obstacle the last revealer will always have the power to manipulate the RANDAO output. This is inherent to RANDAO design.

