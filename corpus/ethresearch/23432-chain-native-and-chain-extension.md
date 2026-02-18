---
source: ethresearch
topic_id: 23432
title: Chain-Native and Chain-Extension
author: Lawliet-Chan
date: "2025-11-12"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/chain-native-and-chain-extension/23432
views: 94
likes: 1
posts_count: 1
---

# Chain-Native and Chain-Extension

## Introduction: A Dual-Layer Universe in Blockchain Architecture

In the blockchain world, every chain resembles a meticulously engineered fortress whose structure is divided into two distinct layers: **chain native** and **chain extension**. The native layer forms the “skeleton” and “heart,” defining the core identity and operating logic of the chain. It covers the account system (such as Ethereum’s EOAs), the virtual machine (the EVM), the consensus mechanism, the transaction pool (mempool), and more. These functions are embedded at the protocol layer, determining the chain’s essential functionality, performance, security, and immutability.

In contrast, the **extension layer** largely refers to the smart contract layer. It acts like the “loft” constructed atop the native framework, enabling developers to build custom logic and unlock open-ended possibilities. Like any architecture, however, these two layers are not isolated—they interlock and build upon each other. Understanding the boundaries and synergies between native and extension layers is crucial when designing an efficient blockchain. This article systematically explores this architectural paradigm, from conceptual definitions and constraints to evolution paths and practical use cases.

## 1. Native vs. Extension: Boundaries and Capabilities

The chain’s native functionality is “built-in and indispensable,” determining its **identity** and **baseline performance**. For example:

- EOA (Externally Owned Accounts): user-controlled accounts that support signed transactions and form the bedrock of Ethereum’s monetary circulation.
- EVM (Ethereum Virtual Machine): the “engine” that executes smart contracts, yet it is itself part of the native layer.
- Consensus mechanisms (such as PoS or PoW): guaranteeing network-wide consistency.
- Transaction pool: temporarily storing transactions before they are included in blocks.

These components operate at the **protocol layer**, delivering high efficiency, minimal gas costs, and the full protection of network consensus.

The extension layer is implemented through **smart contracts**, letting developers deploy code that augments functionality. DeFi protocols, NFT marketplaces, and DAO governance flourish here. Yet not everything is suited to “float up” into the extension layer:

> Many things can be done in smart contracts, but not everything should be.

A classic example is **MEV (Miner/Maximal Extractable Value)**. MEV arises from RBF fairness issues in transaction ordering. Smart contracts alone can’t fundamentally fix it because they lack control over the mempool’s sorting and packaging logic—core responsibilities of the native layer. True MEV resistance demands redesigning those primitives at the **chain native layer**.

## 2. Ethereum Precompiles: Extensions Migrating Downward

Ethereum’s evolution illustrates how extensions can migrate downward into native functionality. **Precompiles** essentially hard-code high-frequency, compute-intensive operations (such as elliptic curve math or SHA-256 hashing) from the smart contract layer into the native layer.

- Early days: developers had to implement these operations directly in contracts, incurring colossal gas costs (for example, Keccak-256 used to cost 30 gas per byte).
- After optimization: precompiles moved these routines into native opcodes, slashing gas consumption to 3–15 and accelerating execution by several multiples.

This is more than a performance upgrade—it is a statement of **architectural philosophy**: **the more frequently used and protocol-relevant a function is, the more it should be pushed down into the native layer**. Looking ahead, L2 systems (like Optimism) and Danksharding will continue blurring the boundary, potentially making rollup logic native as well.

For a **general-purpose chain like Ethereum**, however, indiscriminately adding native features backfires. Doing so **sacrifices generality** (tying the protocol to specific use cases and fragmenting the developer ecosystem) and **raises the frequency of hard forks** (ballooning upgrade costs and deepening community coordination risks). **Downward migration must be done with caution**. General chains should stay extension-first, while specialized chains can afford aggressive native integration.

## 3. The Essence of Native vs. Extension: A Chain’s DNA and Muscles

The distinction between native and extension functionality is a philosophical dividing line. It dictates a chain’s positioning, evolution, and ecosystem scope.

**Chain native** features are its **DNA**—the fundamental identity and core operations. Native capabilities must be **built-in, protocol-level, and hard to change**, embedded into the protocol code and enforced by global consensus. They answer the question, “**What is this chain?**” The native layer provides **baseline performance** (maximal throughput and minimum cost), **top-tier security**, and **functional anchoring** (defining the chain’s unique value). Once established, these features are as stable as DNA; changing them requires a hard fork and incurs staggering costs. The native layer is not “feature accumulation” but a **curated essence**—every opcode serves the chain’s core purpose, and redundancy is toxic.

Conversely, **chain extensions** are the **muscle system**—the dynamic enhancements that magnify the native essence. Extensions live in the smart contract layer, are **flexible, pluggable, and community-driven**, and answer the question, “**How does this chain grow stronger?**” Developers can stack intricate logic on top of the native base to enable personalized innovation, but extensions **depend on the native layer** (running on the VM), **trade off performance** (higher gas costs), and **impose self-managed risk** (contract vulnerabilities). Extensions don’t get to rewrite the DNA; they only enlarge it. The best extensions function like “plugins” or “scripts”—just plug them in.

Take **Ethereum** as an example:

- Native essence: money and finance. It isn’t a generic compute farm but the world’s financial heart.
- Native layer: the EOA account model, balancing transfers, and nonce-based replay protection—the atomic operations of finance—simple, reliable, and globally composable.
- Extension layer: smart contracts amplify that core through standards like ERC-20 and protocols like Uniswap, expanding from mere transfers to complex markets while staying aligned with Ethereum’s financial DNA.

In short: **the native layer forges the soul; the extension layer supplies the strength**. When designing a chain, first forge the native identity (ask “what are we?”), then build the extension muscles (ask “how do we grow?”). Ignore this playbook, and your chain becomes a confused chimera—slow, insecure, and ecosystem-poor.

## 4. Mirrors in Traditional Internet: Lessons from Chrome and Video Games

“Native versus extension” is not unique to blockchains; it is ubiquitous in traditional internet platforms.

**Consider the Chrome browser:**

| Layer | Chrome Core | Chrome Extensions (Plugins) |
| --- | --- | --- |
| Essence | Renders webpages, executes JS | Enhances browsing (e.g., AdBlock) |
| Strengths | Blazing fast, sandboxed security | Customizable, plug-and-play |
| Constraints | Extension can’t rewrite the core | Bound permissions, added overhead |
| Collaboration | WebExtensions API interface | Calls native APIs (tabs, storage) |

The extension ecosystem transformed Chrome from “just a browser” into a “super tool.”

**Video games offer another analogy:**

The **base game** is the developer’s native work, defining gameplay mechanics, engine rendering, and level design to ensure a stable experience. **Mods** are the community’s extension art—leveraging official APIs to add new maps, custom skills, side quests, and even UI overhauls.

| Layer | Base Game (Native) | Game Mods (Extensions) |
| --- | --- | --- |
| Essence | Core gameplay, map, character systems | New maps, skills, story upgrades |
| Developers | Official studio, production-grade | Community builders, rapid iteration |
| Strengths | Polished, QA’d stability | Infinite creativity, free expansion |
| Collaboration | Official mod APIs (e.g., the Civ series) | Rides on the base engine, honors core design |

The **Civilization series** is a textbook example: the base game from Firaxis sets the “skeleton” (turn-based strategy, tech trees, diplomacy and conquest), while the mod community supplies the “flesh” (thousands of new civilizations, units, maps, and balance tweaks). Mods give the game persistent life and explosive sales—but absent the base game, everything collapses. It’s the perfect mirror of **native as foundation, extension as wings** for designing blockchain appchains.

Look deeper and the pattern holds. Chrome’s native engine evolves cautiously because touching the core affects compatibility and security. Every major update (say, a V8 engine upgrade) undergoes months of testing and rollbacks to guarantee zero bugs and cross-platform stability. That is constitutional behavior: the native layer acts like a “constitution,” defining boundaries and guarding the essence. Extensions evolve at a blistering pace: Chrome can see thousands of plugins launched in a week, and Civilization VI’s Steam Workshop churns out hundreds of mods daily—from “Alien Civilizations” to “Modern Nuclear Warfare” patches. The community iterates freely because the risk surface is lower.

The native–extension interface is well-defined: APIs are explicit, extensions cannot override the core logic (mods can’t alter Civilization’s turn calculation), yet they complement each other. The native layer provides a stable base; extensions add boundless vitality. Together they turn Chrome into a “living OS” and Civilization into an “eternal empire simulator.” Specialized blockchains should take the same cue: keep the native layer rock solid, let extensions bloom.

## 5. Designing Specialized Chains: An Orderbook DEX Case Study

Today’s **general-purpose chains** (like Ethereum) face a “thousand chains, one template” stagnation. The future is **specialized chains (AppChains)**. Opting for a generic **EVM + Solidity** stack for everything is a **strategic shortcut** that piles on technical debt and stifles innovation. We must rethink which components deserve to become native for a given use case and which belong in extension land.

**Case: A specialized orderbook DEX chain**

Imagine building a chain dedicated to **high-frequency orderbook-based DEXs**, aiming for **sub-second matching, zero MEV interference, and zero-friction access for global traders**. This is not “putting Uniswap on Ethereum.” Instead, we would **reconstruct the native layer** so that the orderbook DEX becomes the chain’s DNA—making fair trading as ubiquitous as air and execution as fast as lightning.

**Native customization** is the soul:

- MEV resistance at the native level: We natively integrate the MEVless protocol (details). It separates sequencing blocks from execution blocks, committing to an order before transaction contents are revealed. Users first submit transaction hashes with a prepayment (fixed gas plus optional tip); nodes sort these hashes by prepayment and reach consensus on a sequencing block. Only then do users reveal their full transactions, and execution blocks follow the committed order. Sequencers “sort blind,” eliminating sandwich attacks and frontrunning. This is trust-minimized and enforced on-chain—not a contract patch but protocol DNA—tailor-made for DeFi appchains that need pure price discovery and zero slippage.
- Selecting UTXO as the account model: Replace the account-based model with UTXO. Each order behaves like Bitcoin’s “atomically destroy + create” outputs, enabling massive parallelism and shedding state bloat. TPS skyrockets while gas fees plummet.
- A native orderbook engine: Hard-code matching logic for limit and market orders at the protocol level, with real-time depth queries. Traders don’t need to write a line of code to place, cancel, or match orders—the DEX core runs with zero-gas overhead and millisecond latency, rivaling centralized exchanges.

**Extension layer**: To attract Wall Street traders and HFT market makers, we can embed a **Python-friendly VM**. They author **strategy plugins**—arbitrage bots, adaptive market-making algorithms—in Python. Deployment is one click, these plugins call native orderbook APIs, and there’s no performance penalty. Think of it as a “DEX app store” where the community—from retail to institutions—releases strategies. Extensions don’t steal the native spotlight; they elevate it.

## Conclusion: Native as Bedrock, Extension as Wings

“Chain native and chain extension” is the **golden rule** of blockchain architecture: the native layer forges the essence, while the extension layer drives innovation. As the appchain wave rises, specialized chains will dominate. Whether you build a finance chain, a gaming chain, or a social chain, the strategic question remains: how will you draw the line between the native DNA and the extension muscles?
