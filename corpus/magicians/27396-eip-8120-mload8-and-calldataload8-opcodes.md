---
source: magicians
topic_id: 27396
title: "EIP-8120: MLOAD8 and CALLDATALOAD8 Opcodes"
author: Helkomine
date: "2026-01-07"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-8120-mload8-and-calldataload8-opcodes/27396
views: 44
likes: 0
posts_count: 1
---

# EIP-8120: MLOAD8 and CALLDATALOAD8 Opcodes

## Abstract

This EIP introduces new EVM opcodes that allow loading a single byte from memory or calldata in a single operation, reducing gas cost and bytecode size compared to existing patterns based on `MLOAD (0x51)` or `CALLDATALOAD (0x35)` followed by bit shifting.

## Motivation

Currently, the only way to read a single byte from calldata or memory is to use `CALLDATALOAD` or `MLOAD` and then shift the loaded 32-byte word. For example, reading the byte at offset x from calldata requires:

```auto
PUSH x
CALLDATALOAD
PUSH1 248
SHR
```

This pattern increases runtime gas cost and adds three extra bytes to the deployed bytecode for each single-byte access. Contracts that frequently parse byte-oriented calldata or instruction streams incur unnecessary overhead. This EIP proposes two new opcodes that allow loading a single byte directly in one operation.

> Link
>
>
> EIPs/EIPS/eip-8120.md at master · ethereum/EIPs · GitHub
