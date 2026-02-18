---
source: magicians
topic_id: 11713
title: MZERO instruction
author: axic
date: "2022-11-11"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/mzero-instruction/11713
views: 556
likes: 1
posts_count: 1
---

# MZERO instruction

I would like to float the idea of an `MZERO` opcode here. It would take two arguments, `ptr` and `len`, and would set each byte in the memory between `[ptr, ptr+len]` to the value zero.

Zeroing out memory is a common task, mostly for overwriting previously potentially-used memory (i.e. during memory allocation). Solidity sometimes does tricks like `calldatacopy(ptr, calldatasize(), len)` to use the zero-padding feature of `calldatacopy`, `codecopy` or `extcodecopy`. See also this [Solidity proposal](https://github.com/ethereum/solidity/issues/13218) for making that pattern more prevalent.

While this pattern works, it sounds like an abuse of those opcodes and we could do better, both in terms of clarity, cost, and aiding analysis/optimisation. The usual counter argument is that it “wastes” the opcode space and it is yet another instruction.

P.S. There’s an adjacent [MCOPY proposal already](https://ethereum-magicians.org/t/eip-5656-mcopy-instruction/10890).
