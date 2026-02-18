---
source: magicians
topic_id: 12425
title: "EIP 5843: EVM Modular Arithmetic Extensions"
author: jwasinger
date: "2023-01-04"
category: EIPs > EIPs core
tags: [evm, cryptography]
url: https://ethereum-magicians.org/t/eip-5843-evm-modular-arithmetic-extensions/12425
views: 2159
likes: 4
posts_count: 10
---

# EIP 5843: EVM Modular Arithmetic Extensions

[github.com](https://github.com/jwasinger/EIPs/blob/evmmax/EIPS/eip-5843.md)





####



```md
---
eip: 5843
title: EVM Modular Arithmetic Extensions
status: Draft
type: standards track
author: Jared Wasinger , Alex Beregszaszi (@axic)
discussions-to: https://ethereum-magicians.org/t/eip-5843-evm-modular-arithmetic-extensions/12425
category: Core
created: 2022-10-26
requires: 4750, 3670
---

## Abstract

This EIP introduces EVMMAX (EVM Modular Arithmetic Extensions) - a set of opcodes for performing efficient modular addition, subtraction and Montgomery modular multiplication at varying bitwidths.

## Motivation
Additional crypto precompiles have long been desired for the EVM. Among these, operations for various elliptic curves have been proposed and not yet adopted ([BLS12-381](./eip-2537.md), [BW6-761](./eip-3026.md), [MNT4](./eip-1895.md), [Baby Jubjub](./eip-2494.md), [secp256k1](https://github.com/ethereum/EIPs/issues/603), [BLS12-377](./eip-2539.md), [BN256 HashToCurve](./eip-3068.md)).

Crypto precompiles can be problematic for several reasons:
```

  This file has been truncated. [show original](https://github.com/jwasinger/EIPs/blob/evmmax/EIPS/eip-5843.md)










This is a proposal to add EVM opcodes for efficient modular addition/subtraction/multiplication in cases where the modulus is odd, 1-1024 bits and fixed for many operations.  It is an iteration from previous work on [EVM384](https://ethereum-magicians.org/t/evm384-feedback-and-discussion/4533).

It makes use of the following observations to construct a more efficient model for modular arithmetic operations in the EVM:

- If the modulus is odd and fixed for multiple operations and we also precompute some values using it, caching these and the modulus in ephemeral call-scoped state: we can use Montgomery multiplication which is much more efficient than normal modular multiplication.
- If we require inputs to be less than the modulus, they don’t have to potentially be reduced at the start of each arithmetic operation.
- Passing arguments via the stack incurs extra gas cost.
- To support a wide range of bitwidths, we can store values in memory and and make arithmetic opcodes take offsets as inputs, placing them in immediate data appended to the opcode.

The result is a 94% reduction in gas cost for modular addition/subtraction and an 88% reduction for modular multiplication at 193-256bit widths for opcodes from EIP-5843 compared to `ADDMOD`/`MULMOD`.

There are several other resources:

- Analysis and Benchmarks of an EVM implementation of BLS12381 G1 point multiplication.  Benchmarks indicate that the Geth implementation of this EIP with arithmetic for 321-384 bitwidths implemented in x86 assembly can perform around ~2x the runtime of the native implementation of G1Mul from the github.com/ethereum/go-ethereum/crypto/bls12381 package when comparing the average-case runtime for the EVM implementation with the worst-case input runtime from the native code.
- Benchmarks of all supported modulus size configurations for various implementation variants of the arithmetic from the EIP.  This document presents a breakdown of sources of overhead (arithmetic, EVM interpreter loop).
- Huff support for the opcodes in this EIP.  See the EVM BLS12381 G1Mul implementation for an example.

## Replies

**shemnon** (2023-01-17):

I am concerned about the use of a context variable.  Specifically where a contract could call multiple SETMODX and then jump into different sections of code.  I’m concerned it will open up new classes of security and UX problems and I would want some time pokeing around and comparing to alternatives, such as keeping the context variables in memory rather than as a new EVM level concept.

---

**jwasinger** (2023-01-17):

Only one modulus can be set at a given time in the current call context so I am not seeing a potential security problem.

I agree that it would be nice to keep context information in memory, as it would be cleaner. However, this opens up a new problem: storing computed context info for MULMONTX/TOMONTX from `EVMMAXState` in memory, allows it to be modified/corrupted in the EVM which can cause the opcodes to return garbage values.

We don’t want to expose implementation-specific behavior (as client implementations may choose to implement Montgomery multiplication using different algorithms).

---

**shemnon** (2023-01-17):

That’s what I’m worried about.  If we set it to 64 bit, then call a section of code that does math, do a conditional jump that set it to 32 bit, but both branches go back to the same code section, it could be either in 32 or 64 bit mode.

It’s this category of mis-matched SETMODXes going into the same section of MODX operations I’m concerned about.  If we did something like also introduced a CLEARMODX operation that clears the context variable, and made SETMODX raise an exception if the context isn’t cleared we could prevent some coding errors.

Because SETMODX is ultimately dynamic (driven off of memory values) I don’t think there is any deploy-time validation that can be done to try and optimize the operations prior to execution.

---

**jwasinger** (2023-01-18):

Good point! I’m curious what use-cases would be impacted by not being able to do arithmetic on different odd moduli in the same call context.

If there aren’t any, then we can allow `SETMODX` to only be called once per call.

---

**jwasinger** (2023-01-18):

On second thought, I misread your message.

As it is currently specified, the modulus/inputs are always sized in 64bit increments (from the perspective of gas charging logic and the layout for values in memory).  Most use-cases for this EIP are going to be using bitwidths ~256bits and above.  the arithmetic operations can be made constant time, and pricing aims to capture the overhead of arithmetic + worst-case memory latency + interpreter loop overhead.

So at the moment, I can’t see a security issue.

On the point about deploy-time validation:

Yes, this is something that’s missing with the current proposal.  embedding context information in a dedicated EOF section at deployment time to give certain runtime guarantees (e.g. knowing that a given block of arithmetic opcodes will always use the same modulus) is being looked into.

---

**shemnon** (2023-01-18):

> As it is currently specified, the modulus/inputs are always sized in 64bit increments (from the perspective of gas charging logic and the layout for values in memory). Most use-cases for this EIP are going to be using bitwidths ~256bits and above. the arithmetic operations can be made constant time, and pricing aims to capture the overhead of arithmetic + worst-case memory latency + interpreter loop overhead.

Maybe not 32/64, but what about 256/384?  The issue still remains, what if the extension is primed for the wrong modulus.  It feels like it should be treated as a regular programming resource: you need to close it and reset it before re-using it

---

**axic** (2023-01-26):

We had a lengthy discussion between [@jwasinger](/u/jwasinger), [@chfast](/u/chfast) and me for improving EVMMAX based on EOF: [EVMMAX + EOF - HackMD](https://notes.ethereum.org/@ipsilon/BJICGFRoo)

[@jwasinger](/u/jwasinger) is working on drafting a proper EIP of this version.

---

**shemnon** (2023-01-27):

A very good improvement.

Having the setup section as a single EOF header that applies to the whole contract would address my concerns about SETMODX mismatches.

Would be interested what solidity thinks.  It would interact with the memory pointer as they would then need to make sure it’s above the reserved EVMMAX slots.

---

**axic** (2023-01-27):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Would be interested what solidity thinks. It would interact with the memory pointer as they would then need to make sure it’s above the reserved EVMMAX slots.

It would be unlikely that evmmax users would write Solidity contracts, but if so, one only needs to change the `free memory pointer` (e.g. `mstore(0x40, ...)`) prior to using evmmax instructions to avoid overlaps.

