---
source: magicians
topic_id: 9930
title: "EIP-5000: MULDIV instruction"
author: axic
date: "2022-07-13"
category: EIPs > EIPs core
tags: [evm, opcodes, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-5000-muldiv-instruction/9930
views: 3537
likes: 5
posts_count: 11
---

# EIP-5000: MULDIV instruction

This is the discussion topic for



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-5000)





###



Introduce a new instruction to perform x * y / z in 512-bit precision

## Replies

**axic** (2022-07-13):

[twitter.com](https://twitter.com/_hrkrshnn/status/1547235200048013313)





####

[@](https://twitter.com/_hrkrshnn/status/1547235200048013313)

  Fixed point arithmetic is the most widely requested solidity feature in the last few years.

We (@alexberegszaszi, @chfast) are proposing the opcode `muldiv` (https://t.co/Zbe9YoSSP1) that will allow us to have a cheap and generalized way to perform these operations, and more!

  https://twitter.com/_hrkrshnn/status/1547235200048013313










This twitter thread has some interesting questions, mostly from [@Recmo](/u/recmo).

Some initial discussions we had when writing the EIP:

1. Support both “checked” (abort on overflow) and “unchecked” (do not abort) case
2. Whether to return multiple stack items or not
3. Support accessing the hi bits (after division) or not

The current design wanted to avoid multiple opcodes and returning multiple stack items, hence we arrived at having the special case with `z=0`. However we cannot accommodate the case of getting the hi bits *after division*, only before.

If we do not have that special case, then we need multiple opcodes, and need to decide what happens in the `z=0` case. Existing opcodes (such as `DIV`, `ADDMOD`, `MULMOD`, etc.) handle it specially by just returning zero. One would think however that division-by-zero should be an abort, and result in a revert.

---

**k06a** (2022-07-27):

Nice idea. Current implementation in smart contract is way to heavy: [openzeppelin-contracts/Math.sol at c11acfd9d3b8713e196791690a7feded496ebd99 · OpenZeppelin/openzeppelin-contracts · GitHub](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/c11acfd9d3b8713e196791690a7feded496ebd99/contracts/utils/math/Math.sol#L55)

---

**radek** (2022-09-25):

Have you considered the carry flag? - see EIP 1051

---

**axic** (2022-09-25):

In fact we did, the entire conversation started from there (see also [EVM: overflow detection in arithmetic instructions · Issue #159 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/159) from 2016). These are the notes before we settled on the current design:

> Checked opcode #1:
>
>
> Abort on overflow
>
>
> Checked opcode #2:
>
>
> Returns two values (overflow flag)
>
>
> Checked opcode #3:
>
>
> New opcode which sets overflow flag
>
>
> (For the following we introduce a CLEAROF (clears the flag) and GETOF (puts the value of the flag on the stack) instruction.)
>
>
> Overflow-check clear-per-instruction:
>
>
> Perform the calculation
> Overwrite overflow flag
>
>
> Overflow-flag set-if-not-set:
>
>
> Perform the calculation
> Set overflow flag if it was zero prior the calculation
>
>
> Overflow toggle:
>
>
> Turn on overflow setting (two behaviours for opcodes like ADD)

---

**radek** (2022-09-26):

I see. Honestly, I still do not understand the carry flag was not pursued further when simple carry checks of arithmetic operations would result in smaller bytecode (comparing to safe math and now solc outcomes).

But this is OT for this EIP.

---

**RenanSouza2** (2023-03-28):

Is this EIP being considered for the next hard fork (not shanghai)

---

**radek** (2024-04-23):

see discussion wrt Pectra upgrade here: [Pectra Network Upgrade Meta Thread - #66 by radek](https://ethereum-magicians.org/t/pectra-network-upgrade-meta-thread/16809/66)

---

**wjmelements** (2024-04-24):

Shouldn’t the return values include both remainder and the quotient? This would be more useful than an overflow flag.

---

**radek** (2024-04-24):

So 2 stack inputs, 2 stack outputs? Would that have any impact on required gas?

---

**wjmelements** (2024-04-24):

It shouldn’t, since both are available at the end of the muldiv computation.

