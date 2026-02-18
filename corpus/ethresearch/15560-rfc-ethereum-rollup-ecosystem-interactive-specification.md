---
source: ethresearch
topic_id: 15560
title: "RFC: Ethereum Rollup Ecosystem - Interactive Specification"
author: Daniel-K-Ivanov
date: "2023-05-11"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/rfc-ethereum-rollup-ecosystem-interactive-specification/15560
views: 943
likes: 0
posts_count: 1
---

# RFC: Ethereum Rollup Ecosystem - Interactive Specification

As the Ethereum Rollup ecosystem grows, it becomes increasingly difficult for developers to keep up with the new rollups being deployed. This fragmentation of knowledge makes it challenging to assess the differences between developing on L1 versus a given Rollup, or between different Rollups. Additionally, it is unclear what custom precompiles exist on Rollups, which precompiles are supported, what L1 state is exposed on a Rollup, what system-level contracts exist, what the gas costs, latency and interface are for L1 - L2 messaging and how EVM gas pricing has changed.

In the coming months, there will be a rapid deployment of Rollups through OP Chains, Arbitrum Orbit, zkSync HyperChains, and multiple Rollup-as-a-Service solutions. This deployment will only add to the confusion around what is available and how it differs from other options. Solutions like Arbitrum’s EVM+ or Stackr’s Micro-rollups will change the programming platform introducing even more fragmentation to the developer experience.

To address this issue, I propose the creation of an Interactive Reference Specification for the Ethereum Rollup Ecosystem. This website would serve as a valuable resource for developers and provide clarity on the differences between various Rollups. The website would be extending upon the idea of [evm.codes](https://www.evm.codes/) as a base, but would incorporate information on Rollups (differences from L1, gas-costs, custom precompiles, native precompiles support, system contracts, properties of the native L1 <-> L2 messaging protocol provided by the given rollup etc).

I believe that such a knowledge base will be valuable to dApp/infrastructure/rollup developers and auditors.

**I welcome feedback on the idea and any suggestions for additional information that would be valuable for you to see and to be included.**
