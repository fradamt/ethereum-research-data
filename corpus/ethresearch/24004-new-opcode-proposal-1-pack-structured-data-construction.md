---
source: ethresearch
topic_id: 24004
title: "New Opcode Proposal 1: `PACK` Structured Data Construction"
author: ghasshee
date: "2026-02-02"
category: EVM
tags: []
url: https://ethresear.ch/t/new-opcode-proposal-1-pack-structured-data-construction/24004
views: 42
likes: 0
posts_count: 1
---

# New Opcode Proposal 1: `PACK` Structured Data Construction

# PACKn — Structured Data Construction Opcode

---

## Abstract

This proposal introduces a new family of EVM opcodes, `PACKn`, which pop `n` values from the stack and combine them into a single packed structured value that is pushed back onto the stack.

This enables native construction of structured data (such as lists, tuples, or trees) directly at the EVM level, improving efficiency and expressiveness for on-chain interpreters, DSL runtimes, and higher-level virtual machines implemented in smart contracts.

---

## Motivation

The current EVM only supports primitive 256-bit word values. Structured data (lists, trees, ASTs, etc.) must be manually constructed in memory or storage using `MSTORE`, `SSTORE`, and pointer conventions.

This leads to:

- High gas costs due to heavy memory/storage usage
- Complex pointer manipulation in interpreter-style contracts
- Code bloat when building deeply nested structures
- Lack of VM-level awareness of structural boundaries, limiting optimization opportunities

By introducing `PACKn`, structured data can be handled as first-class stack values, allowing:

- MSTORE/SSTORE can store data of arbitrary length at once.
- More efficient on-chain interpreters and DSL engines
- Natural encoding of functional data structures (e.g., cons-lists)

---

## Specification

### Opcode Family

```auto
PACK0
PACK1
PACK2
...
PACK16
```

The exact opcode numbers are to be assigned. A reasonable upper bound (e.g., 16) SHOULD be defined for `n`.

---

### Stack Behavior

For `PACKn`:

**Stack input:**

```auto
..., vₙ, vₙ₋₁, ..., v₂, v₁
```

**Stack output:**

```auto
..., P
```

Where `P` is a packed structured value containing the ordered sequence:

```auto
[v₁, v₂, ..., vₙ]
```

---

### Semantics

`PACKn` performs the following steps:

1. Pop n values from the stack
2. Preserve their order
3. Create a new packed structured value P containing those values
4. Push P onto the stack

`PACK0` produces an empty structure (analogous to `nil`).

**Example (tuple-like):**

```auto
PUSH1 0x03
PUSH1 0x02
PUSH1 0x01
PACK3
```

Top of stack now holds a packed value equivalent to:

```auto
(1, 2, 3)
```

---

### Nested Structures

Packed values are ordinary stack values and can be nested:

```auto
PUSH1 0x03
PACK1          ; (3)

PUSH1 0x02
PACK2          ; (2, (3))

PUSH1 0x01
PACK2          ; (1, (2, (3)))
```

This corresponds to the cons-list:

```auto
cons 1 (cons 2 (cons 3 nil))
```

---

### Internal Representation

A packed value `P` is an abstract EVM value type with:

- Length n
- Ordered elements [v₁ … vₙ]

This is a **new internal value type**, distinct from a 256-bit word. Client implementations MUST treat packed values as opaque structured objects.

---

### Interaction With Existing Opcodes

| Opcode Category | Behavior with Packed Values |
| --- | --- |
| Arithmetic (ADD, MUL, etc.) | Invalid operation (exception) |
| Stack ops (DUP, SWAP, POP) | Operate normally |
| MSTORE, SSTORE | Packed value is serialized to a byte representation |
| KECCAK256 | Hashes the serialized form |
| Comparison (EQ) | Structural equality |

Serialization format MUST be specified (e.g., length-prefixed ABI-like encoding).

---

## Gas Cost

```auto
Gas(PACKn) = G_base + n × G_element
```

Suggested initial values:

- G_base = 5
- G_element = 3

This makes `PACKn` cheaper than building structures via memory, but more expensive than simple arithmetic.

---

## Backwards Compatibility

Existing bytecode does not use these opcodes, so no behavioral change occurs. New opcodes MUST be allocated from currently unused opcode space.

---

## Future Extensions

Possible follow-up opcodes:

- UNPACK — destructure packed values
- GETi — access the i-th element of packed data
