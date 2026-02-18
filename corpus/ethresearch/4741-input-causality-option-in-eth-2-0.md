---
source: ethresearch
topic_id: 4741
title: Input causality option in ETH 2.0?
author: kladkogex
date: "2019-01-04"
category: Cryptography
tags: []
url: https://ethresear.ch/t/input-causality-option-in-eth-2-0/4741
views: 2088
likes: 3
posts_count: 3
---

# Input causality option in ETH 2.0?

Since in ETH 2.0 validators are going to have BLS key, there is an interesting proposal to include input causality into ETH 2.0.

For input causality, you do not know what transaction is included in the blockchain, until the moment it is included.  The transaction is threshold-encrypted by the user, and only once it is included in the block and finalized,  validators collectively exchange messages, decrypt it and run EVM on it.

A system like this would automatically prevent front running.

## Replies

**MihailoBjelic** (2019-01-05):

Would this be effectively similar to HoneyBadger modules?

Any estimations of the additional overhead it would introduce?

---

**kladkogex** (2019-03-03):

It introduces a decryption step - once a transaction is added to the blockchain, it needs to be decrypted …

