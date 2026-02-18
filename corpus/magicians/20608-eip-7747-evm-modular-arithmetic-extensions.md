---
source: magicians
topic_id: 20608
title: "EIP-7747: EVM Modular Arithmetic Extensions"
author: jwasinger
date: "2024-07-21"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7747-evm-modular-arithmetic-extensions/20608
views: 343
likes: 0
posts_count: 2
---

# EIP-7747: EVM Modular Arithmetic Extensions

This is the discussion thread for EIP-7747.  EIP-7747 is a proposal for cost-efficient, expanded-width modular addition/subtraction/multiplication opcodes for the EVM.  The EIP is currently a [PR](https://github.com/ethereum/EIPs/pull/8743) on the EIPs repo.

## Replies

**jwasinger** (2024-07-23):

I’ve published [The Case for an Aggressive Arithmetic Opcode Gas Pricing Model for EIP-7747](https://hackmd.io/QzHNML0YTYGy_djuAEl5Vg) .

In it, I break down the performance of current EIP-7747 Geth implementation, comparing an EVM implementation of BLS12-381 G1/G2 point multiplication with corresponding native implementation from [gnark-crypto](https://github.com/consensys/gnark-crypto/): the backing library for the Geth implementation of EIP-2537.

For bit-widths with desirable use-cases, pricing `ADDMODX`/`SUBMODX`/`MULMODX` opcodes against the performance of an implementation which uses hand-written assembly for the arithmetic can yield substantial cost-savings for certain applications compared to the conservative model in EIP-7747.

It’s worth considering whether the complexity is worth it, and evaluating additional use-cases, how to implement them in the EVM, and available optimizations which can reduce costs further.

