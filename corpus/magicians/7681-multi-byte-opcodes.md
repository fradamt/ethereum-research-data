---
source: magicians
topic_id: 7681
title: Multi-byte opcodes
author: uink45
date: "2021-12-04"
category: EIPs > EIPs core
tags: [opcodes]
url: https://ethereum-magicians.org/t/multi-byte-opcodes/7681
views: 2273
likes: 1
posts_count: 3
---

# Multi-byte opcodes

**Abstract**

Reserve `0xEB` and `0xEC` for usage as extended opcode space.

**Motivation**

It would be convenient to introduce new opcodes that are likely to be infrequently used, whilst also being able to have greater than 256 opcodes in total. As a single byte opcode is half the size of a double byte opcode, the greatest efficiency in code sizes will be one where frequently used opcodes are single bytes. Two prefix bytes are used to accommodate up to 510 double byte opcodes.

**Specification**

For example, a new arithmetic opcode may be allocated to `0xED 01`(`ADD`), and a novel opcode may be introduced at `0xEB F4`(`DELEGATECALL`).

Triple byte opcodes may be doubly-prefixed by `0xEB EB`, `0xEC EC`, `0xEB EC` and `0xEC EB`. It is possible to allocate experimental opcodes to this triple-byte space initially, and if they prove safe and useful, they could later be allocated a location in double-byte or single-byte space.

Only `0xEB EB`, `0xEC EC`, `0xEC EC`, and `0xEB EC` may be interpreted as further extensions of the opcode space. `0xEB` and `0xEC` do not themselves affect the stack or memory, however opcodes specified by further bytes may. If a multi-byte opcode is yet to be defined, it is to be treated as `INVALID` rather than as a NOP, as per usual for undefined opcodes.

**Rationale**

Both `0xEB` and `0xEC` were chosen to be part of the E-series of opcodes. For example, the`0xEF` byte is reserved for contracts conforming to the Ethereum Object Format. By having unassigned opcodes for extending the opcode space, there will be a lower risk of breaking the functionalities of deployed contracts compared to choosing assigned opcodes.

**Backwards Compatibility**

Previous usage of `0xEB` and `0xEC` may result in unexpected behavior and broken code.

**Copyright**

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**matt** (2021-12-06):

I think your EIP is under-specified in a scenario like `600456eb5b`. If the `0xeb` were replaced with `0x60`, the `JUMPDEST` would be considered invalid. In your EIP, it is currently considered valid.

---

**MicahZoltu** (2021-12-07):

What is the reason for reserving two opcodes rather than a single extension opcode?  It seems that one would suffice just as well as two, and we gain essentially nothing from reserving 2.

