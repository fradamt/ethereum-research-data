---
source: magicians
topic_id: 5162
title: "Eip-3198: basefeeopcode"
author: abdelhamidbakhta
date: "2021-01-13"
category: EIPs > EIPs core
tags: [opcodes]
url: https://ethereum-magicians.org/t/eip-3198-basefeeopcode/5162
views: 58990
likes: 4
posts_count: 3
---

# Eip-3198: basefeeopcode

Add a `BASEFEE (0x48)` that returns the value of the base fee at the `current` block.

https://github.com/ethereum/EIPs/pull/3198

## Replies

**wjmelements** (2021-03-15):

Compatibility planning:

On blockchains without EIP-1559, I would expect `BASEFEE` to return 0. I expect most contracts using `BASEFEE` to do `GASPRICE - BASEFEE`, and I expect the constraint `BASEFEE <= GASPRICE` to hold in such case.

---

**poojaranjan** (2021-04-19):

An overview of EIP-3198: BASE FEE opcode with [@rai](/u/rai).

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/8/8898751326323234ef18cf0cd50d0221e3f8702b.jpeg)](https://www.youtube.com/watch?v=QQ3NHtEaCLk)

