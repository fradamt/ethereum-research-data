---
source: magicians
topic_id: 25015
title: A Modular zk‑WASM Execution Layer
author: the-mhdi
date: "2025-08-05"
category: Magicians > Primordial Soup
tags: [evm, zkp, zk-wasm]
url: https://ethereum-magicians.org/t/a-modular-zk-wasm-execution-layer/25015
views: 71
likes: 0
posts_count: 1
---

# A Modular zk‑WASM Execution Layer

Hi Magicians,

starting this thread to address what I see as an “innovation bottleneck” in our ecosystem, something that made us fragment the network into countless L2s and slow down protocol updates.

**Abstract**

The concept is to allow Ethereum to delegate certain executions logic to verified **extensions** (off-chain computation modules), without requiring full consensus-layer changes or separate L2 systems.

This idea is part of a design I’m developing (I call it **Middle Client**) that introduces:

- Operation transactions that reference off-chain computations.
- A dual mempool architecture for Operations and Processed-Operations.
- Proof-based validation where a ZK-WASM Runtime submits zk proofs of extension execution correctness.

**Motivation**

Currently, innovating at the base layer is hard:

- Protocol upgrades require hard forks and long coordination.
- Many ideas that don’t fit inside the current EVM flow end up as separate L2 chains, fragmenting liquidity and security.
- Attempts to add new precompiles or execution logic face high friction due to consensus complexity.

by this design we can enable experimentation and heavy computation **without creating new blockchains**, keeping execution and state on Ethereum while still allowing novel features like:

- Custom signature schemes or cryptographic primitives
- Off-chain compute-intensive operations (verified with proofs)
- Modular extensions (e.g., new transaction types, gas pricing rules, privacy features)

**Design Overview:**

you can read about this concept on:

Github: [GitHub - the-mhdi/eSIaaS: A Modular Ethereum; Offloading specialized, semi-critical logics from the Execution Layer client](https://github.com/the-mhdi/Ethereum-Middle-Client)

medium: https://medium.com/@thisismahdikarimi/layer-1-5-ethereums-next-scaling-solution-extensions-and-middle-nodes-workflow-part-2-d0b63104323a

looking forward to your thoughts and feedback. My hope is to gather input from protocol researchers and client developers to refine the concept and understand whether this could be a viable direction.

[![Untitled Diagram (5)](https://ethereum-magicians.org/uploads/default/optimized/2X/0/0ff4911fe540258963fab12754c908efe51a1386_2_510x499.jpeg)Untitled Diagram (5)1501×1471 152 KB](https://ethereum-magicians.org/uploads/default/0ff4911fe540258963fab12754c908efe51a1386)

thank you!
