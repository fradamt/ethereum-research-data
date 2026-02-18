---
source: magicians
topic_id: 24798
title: "Solx: New Solidity Compiler For Ethereum"
author: zkllvm
date: "2025-07-14"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/solx-new-solidity-compiler-for-ethereum/24798
views: 188
likes: 3
posts_count: 1
---

# Solx: New Solidity Compiler For Ethereum

solx is a new LLVM-based Solidity compiler for Ethereum. Today it eliminates the long-standing **stack-too-deep** error *without* introducing [semantic changes](https://x.com/real_philogy/status/1939481261669601459) or a separate pipeline, so contracts behave exactly as they do with solc’s default path—just without the failure and at lower runtime gas cost.

It already **passes the full solc internal test-suite** *plus* our own corpus of **2 000 + contracts** drawn from Uniswap V4, Aave, Solady, and other production projects. solx is built on the *same* LLVM fork that has powered ZKsync in production since 2021.

As for performance, **≈ 92 % of benchmarks show lower gas usage than solc** ([per project breakdown](https://matter-labs.github.io/solx/dashboard/)), while the emitted bytecode is only **~6 % larger on average** ([unaggregated data](https://matter-labs.github.io/solx/codesize/0.1.0/)). Given these results, we label solx **beta**: suitable for non-mission-critical deployments today, with more features, security hardening, and size tuning on the way before a stable release.

We invite you to try solx at **[https://solx.zksync.io](https://solx.zksync.io/)**. If you’d like deeper context, see our three Mirror posts:

1. solx Beta – Status Update – current capabilities, numbers, roadmap.
2. solx Alpha – Early Walk-through – published with our first release in May, though status is outdate, the text provide code examples where solx is better than solc.
3. Why LLVM Matters for Solidity – how LLVM let us fix stack-too-deep in two months and keep our fork to ~9 k LoC.

**Please share your feedback—positive or constructive.**

*Does Ethereum need a second Solidity compiler? What does solx still lack for you to adopt it in production?*
