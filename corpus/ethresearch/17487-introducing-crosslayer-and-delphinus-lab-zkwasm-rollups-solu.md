---
source: ethresearch
topic_id: 17487
title: "Introducing CrossLayer and Delphinus Lab: zkWasm Rollups solution brings eWASM to Layer2"
author: bngjly
date: "2023-11-23"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/introducing-crosslayer-and-delphinus-lab-zkwasm-rollups-solution-brings-ewasm-to-layer2/17487
views: 1403
likes: 0
posts_count: 2
---

# Introducing CrossLayer and Delphinus Lab: zkWasm Rollups solution brings eWASM to Layer2

TL; DR:

- zkWasm rollup solution is more suitable than eWASM for Ethereum to build Web 3.0.
- zkWasm and zkEVM can broaden the Web 3.0 ecosystem and connect with Web 2.0.
- On-Chain Contracts + Off-Chain Virtual Machine (VM) + WASM Composability.

zkWasm Rollups Solution:

Sinka Gao from DelphinusLab drafted a zksnark wasm emulator paper to demonstrate the zkWasm solution. https://jhc.sjtu.edu.cn/~hongfeifu/manuscriptb.pdf. They present ZAWA, a ZKSNARK backed virtual machine that emulates the execution of WASM bytecode and generates zero-knowledge-proofs can be used to convince an entity with no leakage of confidential information. The result of the emulation enforces the semantic specification of WASM.

For large applications that provide large execution traces, the ZAWA scales when the program size grows. Regarding the performance, carious optimization can be applied in the future including improving the commitment scheme, adopting a better parallel computing strategy by using SNARK-specific hardware etc.

zkWasm rollups combine zk-proofs with WebAssembly, and Ethereum is the

> Data Availability (DA) + Settlement + Consensus

base layer, which can allow developers to easily build and deploy apps, especially convenient for browser apps and games.

[![无标题](https://ethresear.ch/uploads/default/optimized/2X/e/e34d56b63d30704ba8884dbb7b309a1f1ab46121_2_690x328.jpeg)无标题1920×914 125 KB](https://ethresear.ch/uploads/default/e34d56b63d30704ba8884dbb7b309a1f1ab46121)

zkWasm rollups solution has the most advantage of eWASM and can broaden the Web 3.0 ecosystem with zkEVM together. The performance is kind of like Ethereum has EOS layer 2.

Several Web3 games with zkWasm examples: https://delphinuslab.com/wp-content/uploads/2023/04/zksummit-presentation-zkwasm-game-1.pdf

zkWasm Emulator: https://github.com/DelphinusLab/zkWasm

we want to get more feedback from the Ethereum community and hope more developers including former eWASM contributors can build the zkWasm ecosystem together, let’s bring more flexibility and mass adoption to Ethereum. Welcome to leave your comments or send email to me: [Putin@crosslayer.io](https://Putin@crosslayer.io)

## Replies

**bngjly** (2023-11-29):

on-chain game 2048 built on zkWasm: https://g1024-eeni9pldu-zkcross.vercel.app/

