---
source: magicians
topic_id: 27449
title: "ERC-8127: Human Readable Token Identifiers"
author: nxt3d
date: "2026-01-16"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8127-human-readable-token-identifiers/27449
views: 45
likes: 0
posts_count: 1
---

# ERC-8127: Human Readable Token Identifiers

This ERC defines a URI-compatible format for identifying tokens across chains and registries, keeping human-meaningful parts upfront.

**Format:** `[alias.]tokenId@registry`

**PR:** [Add ERC: Human Readable Token Identifiers by nxt3d · Pull Request #1476 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1476)

## The Problem

Current formats like CAIP-19 bury token IDs behind opaque chain/contract addresses (e.g., `eip155:1/erc721:0x.../771769`). This makes identifiers hard to read, speak, and share.

## The Solution

Split identifiers into two parts:

1. Human readable: alias.tokenId (e.g., punk.2344, agent.235234, silver-bullion-bar.58348729)
2. Opaque locator: @registry (ERC-7930 address)

### Examples

- Agents: agent.235234@0x... or support-agent.3453@0x...
- Multi-token (ERC-1155/6909): neo.145@0x...
- RWAs: silver-bullion-bar.58348729@0x...

The alias is optional. It can come from registry metadata or be client-assigned.

## Benefits

- Human readable and portable (aliases can be shared between systems)
- URI compatible and globally unique
- Backwards compatible with alias-only matching

Looking forward to your feedback!
