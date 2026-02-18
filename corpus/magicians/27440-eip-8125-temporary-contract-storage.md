---
source: magicians
topic_id: 27440
title: "EIP-8125: Temporary Contract Storage"
author: weiihann
date: "2026-01-15"
category: EIPs > EIPs core
tags: [evm, state]
url: https://ethereum-magicians.org/t/eip-8125-temporary-contract-storage/27440
views: 62
likes: 3
posts_count: 3
---

# EIP-8125: Temporary Contract Storage

Discussion topic for [EIP-8125](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8125.md); [Web](http://eips.ethereum.org/EIPS/eip-8125);

**## Abstract**

This EIP introduces *temporary storage*: a new contract-accessible key-value store that persists across transactions and blocks, but is automatically cleared at a protocol-defined schedule. Two new opcodes are added:

- TMPSTORE(key, value) to write temporary storage for the executing contract.
- TMPLOAD(key) to read temporary storage for the executing contract.

Temporary storage is intended for data that does not need indefinite retention, providing a safer alternative to using permanent state for ephemeral data and enabling bounded growth of this class of state.

## Replies

**Helkomine** (2026-01-15):

It seems your link to the EIP is broken.

---

**abcoathup** (2026-01-15):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/11081/files)














####


      `master` ← `weiihann:temp-contract-storage`




          opened 03:13PM - 14 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/47109095?v=4)
            weiihann](https://github.com/weiihann)



          [+126
            -0](https://github.com/ethereum/EIPs/pull/11081/files)

