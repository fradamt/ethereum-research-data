---
source: magicians
topic_id: 22427
title: "[ANN] Yolc - a safe, expressive, fun language for Ethereum"
author: hellwolf
date: "2025-01-06"
category: Magicians > Tooling
tags: [compilers]
url: https://ethereum-magicians.org/t/ann-yolc-a-safe-expressive-fun-language-for-ethereum/22427
views: 131
likes: 0
posts_count: 1
---

# [ANN] Yolc - a safe, expressive, fun language for Ethereum

Today is the launch of the technical preview of the [Yolc project](https://yolc.dev/). It is the first milestone where Yolc can produce a partial ERC20 code deployable to Ethereum networks, demonstrating the key idea of linear-type safety.

Yolc doesn’t rebuild wheels. Yolc integrates with [foundry](https://github.com/foundry-rs/foundry), generates Solidity/Yul code, and Yolc is not a language on its own since programming in Yul is programming in Haskell. What Yolc tries to achieve are:

- Being purely functional with linear-type safety and is made for the Ethereum virtual machine;
- Embedding itself in the Haskell language before being compiled into Solidity/Yul code;
- Allowing you to write safe code in production, a joyful experience for super coders.

Yolc aims to feature parity with Solidity plus additional advanced type-level features by 2025/Q1. At the same time, the prototype of the core of [Superfluid protocol](https://github.com/superfluid-finance/protocol-monorepo/) v3 will use Yolc.

Please find the complete introduction blog post of the Yolc project [here](https://yolc.dev/blog/introduce-yolc/), and follow its progress through your favorite channels listed at [linktr.ee/yolc](https://linktr.ee/yolc).

I look forward to having you join Yolc’s journey!
