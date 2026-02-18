---
source: magicians
topic_id: 24520
title: "RIP-7993: Rollup Interoperable Gas Interface Declaration (RIGID)"
author: sajz
date: "2025-06-11"
category: RIPs
tags: [gas, rrc, draft]
url: https://ethereum-magicians.org/t/rip-7993-rollup-interoperable-gas-interface-declaration-rigid/24520
views: 226
likes: 2
posts_count: 1
---

# RIP-7993: Rollup Interoperable Gas Interface Declaration (RIGID)

We’ve been looking for a more transparent and standardized way to understand gas costs across rollups.

Today, each L2 defines its own gas pricing logic in an often opaque and offchain way, making it hard for developers and agents to find the information, estimate fees, plan transactions, or optimize routing.

This proposal introduces RIGID (Rollup Interoperable Gas Interface Declaration), a standard onchain interface for declaring rollup gas market characteristics.

RIGID replaces fragmented, manual fee research with a unified, automated approach based on verifiable onchain data. Systems can compute fees reliably using standardized declarations, stay aware of gas market updates, and apply RPN-encoded formulas with context-aware variables.

This can be especially valuable for crosschain protocols and agents that rely on accurate, comparable, and up-to-date fee mechanism information to operate efficiently across L2s.

We believe gas is a critical piece of the interoperability puzzle and that RIGID can help facilitate better coordination and smarter routing across the rollup ecosystem - ultimately improving the user experience across the broader Ethereum ecosystem.

We welcome your feedback on the current version of RIGID.

https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7993.md
