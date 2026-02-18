---
source: magicians
topic_id: 24989
title: "ERC-8001: Secure Intents: A Cryptographic Framework for Autonomous Agent Coordination"
author: KBryan
date: "2025-08-02"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8001-secure-intents-a-cryptographic-framework-for-autonomous-agent-coordination/24989
views: 270
likes: 1
posts_count: 2
---

# ERC-8001: Secure Intents: A Cryptographic Framework for Autonomous Agent Coordination

This topic is for discussion of a new Ethereum ERC draft titled:

**Secure Intents: A Cryptographic Framework for Autonomous Agent Coordination**

**Abstract:**

This ERC proposes a cryptographic framework that enables autonomous agents to coordinate securely without relying on trusted intermediaries. The framework introduces a structured “Secure Intent” format that combines encrypted payloads, temporal validity constraints, digital signatures, and metadata. This structure ensures authenticity, integrity, confidentiality, and replay protection across chains and systems.

It is designed for use in:

- Cross-chain arbitrage or DeFi agent strategies
- AI coordination protocols and secure agent tooling
- Agentic in-game NPCs
- Web3 game tournament payout systems
- Secure on-chain execution of pre-authorised instructions

The full draft is available here:

[ERC-8001](https://eips.ethereum.org/EIPS/eip-8001)

This thread is intended for:

- Feedback on cryptographic structure and primitives
- Thoughts on EIP-712 integration and metadata schema
- Considerations for implementation in smart contracts, wallets, or cross-chain bridges
- Security, gas cost, or UX concerns

All constructive input is welcome.

—

Kwame Bryan

[@kbryan](https://github.com/kbryan)

## Replies

**KBryan** (2025-12-25):

## Update: ERC-8001 + Bounded Execution — Live on Base Sepolia

Following the ERC reaching **Final status**, I wanted to share a significant implementation update.

### The Problem We Solved

ERC-8001 defines multi-party coordination (propose → accept → execute). But consensus alone doesn’t limit what an agent can do. A compromised agent with a private key could still drain an entire wallet.

**We needed: Consensus + Execution Guardrails**

### Bounded Execution Layer

We’ve built and deployed a **BoundedAgentExecutor** that integrates with ERC-8001:

```auto
┌─────────────────────────────────────┐
│  ERC-8001: "Do all parties agree?"  │  ← Coordination
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│  BoundedExecutor: "Is this allowed?"│  ← Enforcement
│  • Merkle-proven policy tree        │
│  • Daily spending budget            │
│  • Per-transaction limits           │
│  • Timelocked governance (2 days)   │
└─────────────────────────────────────┘
```

**Key insight:** Even if all parties agree, bounded limits still apply. Compromised agent = daily budget loss, not total loss.

### Deployed Contracts (Base Sepolia)

| Contract | Address |
| --- | --- |
| VoxelVerseCoordination (ERC-8001) | 0xc5E3F06AbC4FD34Cc39D42b62064AA159CB4e8B5 |
| BoundedAgentExecutor | 0xC0f1b75dc084E91EEa55b483eD71dc960744db24 |
| BoundedVoxelVerseCoordination | 0x4a5f5eA4C3314294682FA92925856861d1b81B96 |

### Working Demo

Full flow tested on-chain:

1. proposeCoordination() — Player proposes trade
2. acceptCoordination() — NPC agent accepts (ERC-1271)
3. executeBoundedCoordination() — Executes with guardrails

Transaction: [0xc9d1b8b0…](https://sepolia.basescan.org/tx/0xc9d1b8b059a021a3ea3ac2bcb1650eb04e441368be0a7bce8e0ba325a5458b6d)

### Security Properties

| Property | How It’s Enforced |
| --- | --- |
| Policy membership | Merkle proof against policyRoot |
| Daily budget | Rolling 24-hour window per agent |
| Per-tx limit | Encoded in policy tree leaves |
| Governance | 2-day timelock + guardian veto |
| Signature | EIP-712 typed data |

### Use Case: Agent-Managed Treasury

An AI agent managing a $100M treasury can now operate with:

- $10K daily budget (bounded loss)
- Policy tree restricting to approved counterparties
- ERC-8001 consensus for multi-party approvals
- Timelocked governance changes

Worst case if compromised: lose $10K, not $100M.

### What’s Next

1. Mainnet deployment — Moving from testnet to production
2. Audit — Seeking formal review (recommendations welcome)
3. SDK — JavaScript library for easy integration
4. More integrations — Looking for agent platforms to collaborate

### Questions for the Community

1. Are there other execution guardrail patterns we should consider?
2. Interest in a companion ERC for the bounded execution layer specifically?
3. Feedback on the policy tree structure (Merkle leaves = (target, asset, amount))?

### Resources

- EIP: ERC-8001: Agent Coordination Framework
- Reference Implementation: [GitHub link]
- Demo Video: [Coming soon]

Happy to answer questions or discuss design decisions. The goal is to make this a foundational primitive for the emerging agent economy.

— Kwame Bryan ([@KBryan](/u/kbryan))

