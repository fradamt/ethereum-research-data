---
source: magicians
topic_id: 27577
title: "ERC-8137: Trustless Cross-Chain Execution for ERC-4337 Accounts"
author: docbot
date: "2026-01-23"
category: ERCs
tags: [account-abstraction, cross-chain, erc-4337]
url: https://ethereum-magicians.org/t/erc-8137-trustless-cross-chain-execution-for-erc-4337-accounts/27577
views: 43
likes: 0
posts_count: 1
---

# ERC-8137: Trustless Cross-Chain Execution for ERC-4337 Accounts

## Abstract

This ERC proposal defines **WeissChannels**, a protocol extension for ERC-4337 Smart Accounts. It enables single-signature, atomic, cross-chain execution without custodial intermediaries. The protocol introduces ephemeral, “just-in-time” state channels secured optimistically by Ethereum Layer 1, allowing users to control assets and execute transactions across multiple L2 chains with a single Merkle root signature.

Unlike intent-based systems where users delegate execution to third parties, WeissChannels enable users to execute their own transactions on destination chains, using Crosschain Liquidity Providers (XLPs) only for liquidity and gas fronting.

**Read more:** **[Full ERC-8888 Proposal](https://github.com/eil-docbot/ERCs/blob/master/ERCS/erc-8888.md)

Ethresear.ch thread:** https://ethresear.ch/t/eil-trust-minimized-cross-l2-interop/23437

---

## Reference Implementation

A reference implementation is available including the `CrossChainPaymaster`, `L1AtomicSwapStakeManager`, and bridge connectors.

**Contracts:** [https://github.com/eth-infinitism/eil-contracts](https://www.google.com/search?q=https://github.com/eth-infinitism/eil-contracts)

**SDK:** [https://github.com/eth-infinitism/eil-sdk](https://www.google.com/search?q=https://github.com/eth-infinitism/eil-sdk)



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1486)














####


      `master` ← `eil-docbot:master`




          opened 05:11PM - 23 Jan 26 UTC



          [![](https://avatars.githubusercontent.com/u/256784999?v=4)
            eil-docbot](https://github.com/eil-docbot)



          [+2167
            -0](https://github.com/ethereum/ERCs/pull/1486/files)







## Summary
- Adds ERC-8888: a protocol extension for ERC-4337 Smart Accounts en[…](https://github.com/ethereum/ERCs/pull/1486)abling single-signature, atomic, cross-chain execution
- Introduces ephemeral "just-in-time" state channels secured optimistically by Ethereum L1
- Allows users to execute transactions across multiple L2 chains with a single Merkle root signature

## Key Features
- **Single-signature cross-chain execution** via Merkle tree of UserOps
- **Optimistic security model** with 1-of-N honest assumption
- **Crosschain Liquidity Providers (XLPs)** for liquidity and gas fronting
- **Hardware wallet compatible** - one signature authorizes all chains
- **Full ERC-4337 compatibility**

## Reference Implementation
- https://github.com/eth-infinitism/eil-contracts
- https://github.com/eth-infinitism/eil-sdk
