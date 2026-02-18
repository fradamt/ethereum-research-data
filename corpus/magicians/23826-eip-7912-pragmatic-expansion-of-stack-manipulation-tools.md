---
source: magicians
topic_id: 23826
title: "EIP-7912: Pragmatic expansion of stack manipulation tools"
author: matt
date: "2025-04-24"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7912-pragmatic-expansion-of-stack-manipulation-tools/23826
views: 407
likes: 3
posts_count: 8
---

# EIP-7912: Pragmatic expansion of stack manipulation tools

PR: [Add EIP: Pragmatic expansion of stack manipulation tools by lightclient · Pull Request #9501 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9501)

Add `SWAP17`-`SWAP24`, `DUP17` - `DUP24`, `SWAPN`, `DUPN`, and `EXCHANGE`

instructions. The arbitrary depth operations must be preceded by `PUSH1` instructions defining operands.

## Replies

**wjmelements** (2025-04-24):

> The argument X must be provided by a PUSH2 operation immediately preceding the EXCHANGE instruction

> This argument must be provided by a PUSH1 operation immediately preceding the SWAPN and DUPN instructions.

Why not just read from the stack and exceptional-halt if the param is too large?

---

**matt** (2025-04-24):

> Why not just read from the stack and exceptional-halt if the param is too large?

You do read them from the stack, but this simplifies static analysis i) by ensuring the operand is available directly before the instruction and ii) avoiding dynamic stack manipulation by using values from calldata or storage as the operand.

---

**Arvolear** (2025-04-26):

We really need this more than the entire EOF. Even though the Solidity compiler might have fixed its “stack-too-deep” errors by putting local variables into memory.

---

**benaadams** (2025-04-27):

Why burn 17 opcodes for the fixed values and add 2 dynamic ones for same gas that do the same thing?

Also the 4 dynamic opcodes have 34 byte code look backs so 3 gas seems very low?

---

**matt** (2025-04-27):

I think we have ample opcodes left and stack-too-deep is a common issue. The static N versions relieve some pressure efficiently while the dynamic N versions support much deeper stack manipulation at a slightly higher cost.

Yeah 3 has could be too low, will have to see how expensive the look back ends up being. Could also consider doing look after.

---

**matt** (2025-05-05):

[@benaadams](/u/benaadams) btw I added a note in the EIP, but I remembered why the dynamic opcodes are actually not that expensive. You just need to look at `pc-2` and see if it is a valid jump destination. If so, we know it executed since there couldn’t be any other operation in between. Another way to do this is just store an interpreter flag `is_last_op_push1` and only set it when a PUSH1 is executed and unset after.

---

**frangio** (2025-08-24):

Historical note: This design for DUPN/SWAPN was considered in the first version of EIP-663 before it got switched to EOF.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/blob/064a435161e2/EIPS/eip-663.md#L43-L45)





####

  [064a435161e2](https://github.com/ethereum/EIPs/blob/064a435161e2/EIPS/eip-663.md#L43-L45)



```md


1. ### Option A+
2.
3. The difference to Option A is that `DUPn` and `SWAPn` must be preceded by a `PUSHn` opcode. Encountering `DUPn` and `SWAPn` without a preceding `PUSHn` results in out of gas.


```

