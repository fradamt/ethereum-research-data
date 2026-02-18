---
source: magicians
topic_id: 25605
title: EVM Immediates
author: frangio
date: "2025-09-27"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/evm-immediates/25605
views: 304
likes: 12
posts_count: 9
---

# EVM Immediates

All current EVM instructions other than the push opcodes take all of their operands from the stack. Many instructions have been proposed in the past that would’ve liked to use immediate operands, where the operand value is a constant hardcoded in the bytecode instead.

No such instruction has been accepted yet because of concerns about breaking existing EVM bytecode. EOFv1 ([EIP-7692](https://eips.ethereum.org/EIPS/eip-7692)) would have addressed this, but the proposal was ultimately rejected.

This post looks at the problem anew and describes options available for instructions that would like to use immediates. Only backward-compatible options are considered.

## Problem: Backward compatibility

Since SWAPN/DUPN were first proposed as [EIP-663](https://eips.ethereum.org/EIPS/eip-663) in 2019, it’s [been known](https://ethereum-magicians.org/t/eip-663-unlimited-swap-and-dup-instructions/3346/10) that introducing instructions with immediates is a breaking change if their immediates must be masked for jumpdest analysis, i.e., if a JUMPDEST opcode (`5b`) found as part of an immediate *should not* be considered a valid jump target, just like the PUSH operand is masked.

To understand this breaking change, consider the bytecode sequence `e6 5b` that currently disassembles and behaves as `INVALID JUMPDEST`. If an upgrade makes the opcode `e6` into an instruction “OP” with a 1-byte immediate, the same bytecode sequence would then disassemble to `OP 0x5b`, with no JUMPDEST and thus invalidating a jump target the contract may need to function. A similar thing can happen with push opcodes, for example, `e6 60 5b` would transform from `INVALID PUSH1 0x5b` to `OP 0x60 JUMPDEST`, *creating* a new valid jump target. And this may have a cascading effect on arbitrarily many subsequent instructions (consider `e6 60 60 …`).

Since the EVM doesn’t offer a dedicated section for data, arbitrary data may be embedded in code and serve as immutable data storage accessed via CODECOPY. Therefore, we must assume that arbitrary byte sequences may be found in contract code that should not be broken.

## Option 1: No immediates

It would be possible for the EVM to keep PUSH* as the only immediate-carrying instructions and to continue requiring that all operands go through the stack.

This raises the question of **why we might want immediates** instead. I believe this comes down to two reasons:

1. Efficiency: If operands are always known statically it is more efficient for the VM to skip stack manipulation and gas accounting.
2. Static analyzability: Values in the stack can come from user input and thus take arbitrary values. This can make static analysis of bytecode exponentially more difficult. Static analyses that are instead easy could be safely used in the execution layer without introducing DoS attack vectors, or could be used to improve the security of the application layer.

## Option 2: Immediates

### Option 2.1: Changes to jumpdest analysis

The simplest way to introduce immediates without breaking existing code is to use EOF-like **bytecode versioning** as enabled by [EIP-3541](https://eips.ethereum.org/EIPS/eip-3541). A prefix such as `ef00` at the beginning of the code might indicate that a variant of jumpdest analysis should be used instead of the original one, where certain opcodes would imply additional masking.

### Option 2.2: No changes to jumpdest analysis

#### Option 2.2.1: Disallowed immediate bytes

Observe that issues only arise when the JUMPDEST or PUSH* opcodes are found in the immediates. A new instruction can be designed so that this never happens in functional code: the bytes `5b` and `60` to `7f` are banned (only failing at runtime, with no validation during contract creation), and the immediate bytes are encoded at assembly or compile time, and decoded during execution, in a way that works around the banned bytes to make sure that a contiguous range of operand values can be used.

The downside of this option is the complexity of decoding, which must be carefully designed to balance efficiency and expressivity of the instruction, and arguably that it obfuscates the true immediate value in bytecode that is read without the help of a disassembler.

The spec for an instruction `I` with a one-byte immediate using this approach would consist of a function `DECODE_I`, with domain `DOMAIN_I` that excludes at least `5b` and `60`, …, `7f`, and the following addition to the EVM interpreter loop:

> When code[pc] is OP_I:
>
>
> Let x = code[pc + 1].
> If x is not in DOMAIN_I, halt with exceptional failure.
> Let y = DECODE_I(x).
> Apply instruction I(y).
> Set pc = pc + 2.

For a worked out example of this approach see [EIP-8024](https://eips.ethereum.org/EIPS/eip-8024#specification).

#### Option 2.2.2: PUSH prefix

Since the PUSH* instructions are already masked for jumpdest analysis, they can be used for immediates by mandating that an instruction be preceded by a PUSH (probably of a specific size) in the code.

An example of this approach is found in [EIP-7912](https://eips.ethereum.org/EIPS/eip-7912).

The downside is that the operand must still go through the stack and gas accounting, especially for an EVM implementation that executes bytecode directly without a preceding parsing step. As a result this approach only provides the benefit of static analyzability.

#### Option 2.2.3: PUSH postfix

Alternatively, an instruction could require that it be *followed* by PUSH, with it thus becoming part of the instruction encoding, since the PUSH would not be executed normally but instead can be read directly by the prior instruction and the program counter adjusted to skip over it.

This is a very nice option but one that increases the size footprint of instructions with immediates.

The spec for an instruction `I` with a one-byte immediate using this approach would consist of the following addition to the EVM interpreter loop:

> When code[pc] is OP_I:
>
>
> If code[pc + 1] != OP_PUSH1, halt with exceptional failure.
> Let x = code[pc + 2].
> Apply instruction I(x).
> Set pc = pc + 3.

## Replies

**gcolvin** (2025-09-28):

I’m generally in favor of 2.1 – I think it’s the cleanest option so far as easy decoding and readability.  The postfix `PUSH` is also good in that respect, and the extra byte “future-proofs” the immediate argument.

I propose the `PUSH` prefix in [EIP-7979](https://ethereum-magicians.org/t/eip-7979-call-and-return-opcodes-for-the-evm/24615) because I am restricting validated uses of `JUMP` to `PUSH const JUMP` (and adding `PUSH const CALLSUB`)  and don’t want to change the syntax.

I do propose to use immediate arguments in [EIP-8013](https://ethereum-magicians.org/t/eip-8013-static-relative-jumps-and-calls-for-the-evm/25222/1) which is all new opcodes intended to work only in `MAGIC` (0xE0) code.

---

**gcolvin** (2025-09-28):

I’m generally in favor of 2.1 – I think it’s the cleanest option so far as easy decoding and readability.  The postfix PUSH is also good in that respect, and the extra byte “future-proofs” the immediate argument.

I propose the PUSH prefix in [EIP-7979](https://ethereum-magicians.org/t/eip-7979-call-and-return-opcodes-for-the-evm/24615) because I am restricting validated uses of `JUMP` to `PUSH const JUMP` (and adding `PUSH const CALLSUB`)  and don’t want to change the syntax.

I do propose to use immediate arguments in [EIP-8013](https://ethereum-magicians.org/t/eip-8013-static-relative-jumps-and-calls-for-the-evm/25222/1) which is all new opcodes intended to work only in `MAGIC` (0xE0) code.

---

**wjmelements** (2025-10-02):

My preferred solution is [EIP-7921: Skip `JUMPDEST` immediate argument check](https://eips.ethereum.org/EIPS/eip-7921)

No solidity contracts will break. Just remove the damn check.

---

**Ankita.eth** (2025-10-07):

I think immediates could make the EVM more efficient and easier to analyze, especially for operations that use fixed constants. For example, instead of:

```auto
PUSH1 0x05
ADD
```

having something like `ADD1 0x05` would reduce stack usage and gas cost.

But since the EVM doesn’t separate code and data, adding immediates directly would risk breaking existing contracts — even small byte shifts can change valid `JUMPDEST`s. That’s why I believe the right path is through **EOF versioning**, where new rules apply only to new bytecode.

PUSH-prefix or postfix ideas are clever stopgaps, but EOF gives a cleaner, long-term structure to safely introduce immediates and other future upgrades.

---

**frangio** (2025-12-18):

I’ve added templates for specifying instructions with approaches 2.2.1:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> The spec for an instruction I with a one-byte immediate using this approach would consist of a function DECODE_I, with domain DOMAIN_I that excludes at least 5b and 60, …, 7f, and the following addition to the EVM interpreter loop:
>
>
>
> When code[pc] is OP_I:
>
>
> Let x = code[pc + 1].
> If x is not in DOMAIN_I, halt with exceptional failure.
> Let y = DECODE_I(x).
> Apply instruction I(y).
> Set pc = pc + 2.

and 2.2.3:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> The spec for an instruction I with a one-byte immediate using this approach would consist of the following addition to the EVM interpreter loop:
>
>
>
> When code[pc] is OP_I:
>
>
> If code[pc + 1] != OP_PUSH1, halt with exceptional failure.
> Let x = code[pc + 2].
> Apply instruction I(x).
> Set pc = pc + 3.

---

**gcolvin** (2026-01-16):

I’ve been told that the E0 prefix has already been used for one instruction, but I don’t remember which one.  Can someone tell me again?

---

**pdobacz** (2026-02-04):

Late to the party, but can we challenge this assumption?:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> … arbitrary data may be embedded in code and serve as immutable data storage accessed via CODECOPY. Therefore, we must assume that arbitrary byte sequences may be found in contract code that should not be broken

1. Is there any compiler or lib out there that does that, as opposed to putting all data at the end? AFAICT Solidity doesn’t and never has.
2. More broadly, would this layout work at all? Suppose I have:

I cannot jump to that 0x5b to execute  anyway. So any approach that embeds data would need to pad it with 32 bytes at the end, which in turn would protect against impact of a JUMPDEST-analysis-bearing byte sitting in the data

---

**frangio** (2026-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pdobacz/48/3042_2.png) pdobacz:

> Solidity doesn’t and never has.

This is a valid counter. I personally think if the EVM allows it we can’t break it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pdobacz/48/3042_2.png) pdobacz:

> So any approach that embeds data would need to pad it with 32 bytes at the end

The padding is not strictly necessary unless the data ends with a push opcode. If the data ends with a full push instruction including immediate, the padding may be omitted, and in this case, the effects of adding a new instruction with jumpdest-masking immediate could bleed out of the data section and break the contract. If 32 bytes of padding is always added, then no bleed out is possible, but we can’t assume this.

