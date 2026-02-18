---
source: ethresearch
topic_id: 24006
title: "New Opcode Proposal 2: `L / R` Structured Skip Region"
author: ghasshee
date: "2026-02-03"
category: EVM
tags: []
url: https://ethresear.ch/t/new-opcode-proposal-2-l-r-structured-skip-region/24006
views: 70
likes: 0
posts_count: 1
---

# New Opcode Proposal 2: `L / R` Structured Skip Region

# Structured Skip Regions via L / R Opcodes

## Abstract

This introduces two new EVM opcodes, **`L` (Left delimiter)** and **`R` (Right delimiter)**, which define *structured skip regions* in bytecode.

When executed, `L` causes the EVM to skip forward to its matching `R` without executing the enclosed bytes. These regions allow contracts to embed **non-executable structured data directly inside bytecode** while preserving deterministic execution.

---

## Motivation

EVM bytecode currently has no native way to distinguish:

- Executable instructions
- Embedded metadata
- Compiler tables
- Structured constants
- Alternative code paths meant only for off-chain tools

All bytes are treated as potentially executable instructions, and the only way to skip code is through dynamic jumps.

This leads to problems:

- Compilers cannot safely embed structured data in bytecode
- Static tools must conservatively treat all bytes as executable
- Bytecode cannot carry rich internal structure without risking accidental execution
- Control-flow must be expressed using unstructured jumps

We propose **structured skip regions** that behave like *non-executed islands* inside bytecode.

These regions allow bytecode to safely contain:

- Lookup tables
- Jump tables
- Type metadata
- ABI-like internal descriptors
- Compiler hints
- Future extension payloads

without affecting execution.

---

## Specification

### New Opcodes

| Opcode | Name | Stack | Description |
| --- | --- | --- | --- |
| 0x?? | L | — | Begin skip region |
| 0x?? | R | — | End skip region |

---

## Semantics

### 1. L — Skip Forward to Matching R

When the EVM executes opcode `L`:

- It enters skip mode
- It scans forward in bytecode to find the matching R
- All bytes in between are ignored and never executed
- Nested L/R pairs must be balanced

#### Matching Algorithm

```auto
depth = 1
pc = pc + 1

while depth > 0:
    opcode = code[pc]

    if opcode == L:
        depth += 1
    else if opcode == R:
        depth -= 1

    pc += 1
```

---

### 2. R — Structural Delimiter

Execution resumes at the first opcode **after** the matching `R`.

If no matching `R` is found → exceptional halt.

---

## Structural Rules

### 1. Regions Are Non-Executable

Bytes inside an `L … R` region:

- Must never be executed
- Are treated as opaque payload
- May contain arbitrary byte values, including invalid opcodes

---

### 2. Jumping Into or Out of Regions is not forbidden

It is valid to:

- JUMP or JUMPI to a location inside a skip region
- Jump from inside a region to outside

---

### 3. Nesting Is Allowed

Skip regions may be nested:

```auto
L

   L

   R
R
```

The matching algorithm ensures correct pairing.

---

## Gas Costs

| Opcode | Gas |
| --- | --- |
| L | 3 |
| R | 2 |

Clients MAY preprocess bytecode to map matching pairs, allowing `L` to execute in constant time.

---

## Rationale

### Bytecode as a Structured Container

This proposal lets contracts treat bytecode not just as instructions, but as a **container format**.

With `L/R`, bytecode can safely include:

| Use Case | Example |
| --- | --- |
| Constant data blobs | Precomputed tables, large constants |
| Jump tables | Dense switch dispatch tables |
| ABI-like internal layouts | Type descriptors for internal DSLs |
| Debug info | Source maps, symbolic names |
| Compiler metadata | Optimization hints, layout info |
| Versioned extensions | Forward-compatible payload regions |

All without risking accidental execution.

---

### Why Not Just Use JUMP?

Using `JUMP` to skip over data:

- Requires dynamic control flow
- Leaves the skipped bytes syntactically executable
- Makes static analysis ambiguous
- Cannot safely contain arbitrary byte patterns

`L/R` instead create **explicit non-executable regions**, similar to data sections in traditional binaries.

---

### Why Not Reuse JUMPDEST?

`JUMPDEST` marks valid jump targets but does not mark **non-executable regions**.

We need the opposite: a way to declare **“this is not code.”**

---

## Backwards Compatibility

Fully backward compatible:

- Existing contracts contain no L or R
- Old bytecode behavior unchanged
- New semantics apply only when opcodes are present

---

## Example: Embedding a Data Table

```auto
PUSH1 0x00
SSTORE

L
   0x12 0x34 0x56 0x78
   0x9a 0xbc 0xde 0xf0
R

PUSH1 0x01
SSTORE
```

The bytes inside `L … R` are never executed and can be read by off-chain tools or by copying code via `EXTCODECOPY`.

---

## Conclusion

`L` and `R` introduce **structured non-executable regions** to the EVM, enabling bytecode to function as a **hybrid of code and structured data**.

This:

- Improves analyzability
- Enables safer compiler-generated metadata
- Allows dense in-bytecode data structures
- Preserves full backward compatibility
- Requires minimal changes to the execution model

A small opcode addition turns EVM bytecode into a **self-describing, structured artifact**, not just a flat instruction stream.
