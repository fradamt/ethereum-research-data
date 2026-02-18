---
source: ethresearch
topic_id: 22934
title: Zk-pushr - A zkVM for Genetic Programming on Ethereum
author: johba
date: "2025-08-18"
category: Layer 2 > ZK Rollup
tags: [zk-roll-up]
url: https://ethresear.ch/t/zk-pushr-a-zkvm-for-genetic-programming-on-ethereum/22934
views: 180
likes: 1
posts_count: 1
---

# Zk-pushr - A zkVM for Genetic Programming on Ethereum

## The Problem

DeFi protocols can’t optimize their parameters without trust assumptions. They either pay consultants like Gauntlet millions per year or stick with static parameters that leave money on the table. The numbers are substantial—Uniswap V3 LPs lose hundreds of millions to poor range management, lending protocols maintain unnecessarily conservative parameters.

The obvious solution would be to run optimization algorithms on-chain, but that’s not feasible. LLMs and neural networks require floating-point matrix operations, gigabytes of memory, and non-deterministic sampling. Even simple models would cost millions in gas.

## A Different Path: Genetic Programming in Zero-Knowledge

I’m building [zk-pushr](https://codeberg.org/johba/zk-pushr) a zkVM for PUSH3, a stack-based language designed for genetic programming. The idea is straightforward:

1. Optimizers evolve algorithms off-chain using standard genetic programming techniques
2. When a protocol needs optimization, the algorithm runs in a zkVM
3. The protocol gets results with a STARK proof of correct execution

Genetic algorithms work here because they’re just arithmetic operations on stacks—no matrices, no floating point madness, just integer math that maps cleanly to arithmetic circuits.

## Technical Approach

### PUSH3 Language

[PUSH3](https://faculty.hampshire.edu/lspector/push.html) is a simple stack language with separate stacks for different types (INTEGER, FLOAT, BOOLEAN, CODE, EXEC, NAME). Programs are just sequences of operations and literals. If an operation doesn’t have enough arguments on the stack, it becomes a no-op instead of crashing.

Example program:

```push3
( PRICE VOLATILITY FLOAT.* 2.0 FLOAT./
  RANGE.MIN FLOAT.- RANGE.MAX FLOAT.+ )
```

### The zkVM Implementation

The implementation takes PUSH3 programs and generates STARK proofs of their execution using [OpenVM](https://openvm.dev/):

```auto
PUSH3 Program → Trace Recording → OpenVM Chips → STARK Proof
```

Proof generation takes about 2 minutes and produces ~500KB proofs. Those proofs can then be rolled up into a STARK to be submitted on chain.

## Current State

Working:

- Basic arithmetic (ADD, SUB, MUL, DIV) on INTEGER/FLOAT/BOOLEAN stacks
- Trace recording that feeds into OpenVM
- STARK proof generation using Plonky3

Not implemented yet:

- CODE/EXEC/NAME stacks (needed for actual genetic programming)
- Most stack manipulation (DUP, YANK, SHOVE)
- Control flow operations

## The Vision

If this gets built out into a rollup, Ethereum gains something interesting: any protocol that can define a fitness function can evolve its own optimization algorithms.

I image the following effects:

- AMMs evolve fee tiers and concentrated liquidity ranges
- Lending protocols evolve risk parameters and interest curves
- Options protocols evolve pricing models
- MEV protection evolves counter-strategies

All without trusting anyone—just math proving the algorithm ran correctly.

One possible development path: finish the zkVM, then explore deployment as a based rollup. The idea would be a registry where protocols request optimizations with a fitness function, any-one can submit solutions, the best according to the fitness function is registered and it’s executions are proven and verified on-chain.

This isn’t about replacing human judgment or building AGI. It’s about giving Ethereum native optimization capabilities that don’t require trust. Other chains are adding AI coprocessors and LLM oracles—Ethereum could have something that actually works on-chain.

## Selection of Open Questions

- Are evolved PUSH3 programs expressive enough for real DeFi optimization? Genetic programming can discover surprising solutions, but can a stack-based language really encode the complex strategies needed for things like concentrated liquidity positioning or multi-asset risk management?
- What’s the actual cost-benefit here? Generating a STARK proof for every optimization run adds overhead. For frequently-updated parameters, is the gas cost of verification worth the trustlessness? Especially when the algorithm itself might be mediocre?
- How do you handle algorithm inputs? DeFi optimization needs price feeds, TVL data, historical volatility—does every data source need its own zkVM adapter?
- How do you prevent overfitting? An algorithm evolved on historical data might look perfect but fail catastrophically in new market conditions.
- Is trustless optimization actually valuable if you still need to trust the fitness function design? Bad fitness functions could be worse than static parameters.
- Could you achieve similar results with deterministic optimization algorithms that are easier to verify?
