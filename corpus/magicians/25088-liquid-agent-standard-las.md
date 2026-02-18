---
source: magicians
topic_id: 25088
title: Liquid Agent Standard (LAS)
author: CROME
date: "2025-08-13"
category: ERCs
tags: [erc, token, evm, wallet, erc-721]
url: https://ethereum-magicians.org/t/liquid-agent-standard-las/25088
views: 103
likes: 0
posts_count: 1
---

# Liquid Agent Standard (LAS)

**Author**: CROME Team

**Type**: Standards Track

**Category**: ERC

**Created**: August 13, 2025

**Requires**: ERC-20, ERC-721, ERC-6551

---

## Abstract

The **Liquid Agent Standard (LAS)** defines **Tokenized Liquid Agents** which are transferable on-chain entities that combine fungible balances, unique NFT identities, and token-bound accounts (TBAs) with embedded logic.

These agents can hold assets, execute actions, message each other, and schedule recurring tasks.

**CROME** is poised to be the first public LAS implementation, introducing **Liquid Intelligence**: agents as programmable, composable actors that operate across DeFi, NFTs, DAOs, and games.

---

## Motivation

Ethereum’s core token standards solved problems in isolation:

- ERC-20 → fungible liquidity
- ERC-721 → unique identity & metadata
- ERC-6551 → per-token accounts with code and storage

What’s missing is a **standard agent interface** that fuses all three and enables:

- Transferable as value
- Addressable as identity
- Operable as an autonomous participant

LAS is designed to make a token *do things*, not just *represent things*.

---

## Specification (Draft)

The keywords “MUST”, “SHOULD”, “MAY” follow RFC 2119.

### 1. Composition

An LAS-compliant implementation MUST:

- Implement ERC-20 for fungible transfers
- Implement ERC-721 for agent IDs & metadata
- Integrate ERC-6551 for a per-agent TBA

---

### 2. Token-Bound Account Lifecycle

LAS MUST allow deterministic creation/resolution of TBAs:

```auto
function createAccount(
    address implementation,
    bytes32 salt,
    uint256 chainId,
    address tokenContract,
    uint256 tokenId
) external returns (address account);
```

- MUST return the same address if already created (idempotent)

---

### 3. Agent Authorization

Owner or approved operator MUST be able to grant/revoke execution rights:

```auto
event AgentAuthorized(uint256 indexed tokenId, address agent, bool authorized);

function authorizeAgent(
    uint256 tokenId,
    address agent,
    bool authorized
) external;
```

---

### 4. Inter-Agent Messaging (Optional but Recommended)

Compact cross-agent communication:

```auto
event AgentMessageSent(uint256 indexed fromTokenId, uint256 indexed toTokenId, bytes32 message);

function sendAgentMessage(
    uint256 fromTokenId,
    uint256 toTokenId,
    bytes32 message
) external;
```

---

### 5. Action Scheduling (Optional but Recommended)

Timed or recurring execution from an agent’s TBA:

```auto
event ActionScheduled(uint256 indexed tokenId, uint256 actionId, uint256 executeAt, uint256 interval);
event ActionExecuted(uint256 indexed tokenId, uint256 actionId, bool success);

function scheduleAction(
    uint256 tokenId,
    address to,
    uint256 value,
    bytes calldata data,
    uint8 operation,        // CALL / DELEGATECALL
    uint256 executionTime,  // Unix time
    uint256 interval        // 0 = one-shot
) external returns (uint256 actionId);
```

---

### 6. Metadata

Agents SHOULD expose a `baseURI` for off-chain rendering of live dashboards.

---

## Rationale

The trifecta (ERC-20 + ERC-721 + ERC-6551) enables:

- Value: liquid fungibility
- Identity: unique on-chain persona
- Agency: autonomous execution & state

By standardizing just three behaviors (auth, messaging, scheduling), LAS gives developers a common language for building interoperable agent ecosystems, much like ERC-4626 did for vaults.

---

## Example Workflows

**Create or resolve an agent account**:

```auto
address acct = createAccount(
    implementation,
    keccak256("agent_salt"),
    block.chainid,
    address(this),
    tokenId
);
```

**Authorize a keeper**:

```auto
authorizeAgent(tokenId, keeperAddress, true);
```

**Send a “PING” to another agent**:

```auto
sendAgentMessage(tokenIdA, tokenIdB, keccak256("PING"));
```

**Schedule a daily rebalance**:

```auto
scheduleAction(
    tokenId,
    vault,
    0,
    abi.encodeWithSelector(Vault.rebalance.selector),
    0,
    block.timestamp + 1 hours,
    24 hours
);
```

---

## Applications

1. DeFi Agents: automated LP managers, yield routers
2. Dynamic NFTs: evolving art or collectibles
3. DAO Delegates: autonomous proposal/voting logic
4. Game Avatars: in-game entities with skills & inventories
5. Synthetic Portfolios: on-chain indexes with rebalancing

---

## Reference Implementation: CROME

`CROME` (Solidity) includes:

- ERC-20 + ERC-721 + ERC-6551 registry/account integration
- authorizeAgent, sendAgentMessage, scheduleAction behaviors
- Optional fee routing & DEX swap hooks for on-chain operations

---

## Next Steps

- Publish minimal LAS interfaces & test vectors
- Deploy CROME instance for dev experimentation
- Gather Ethereum Magicians feedback before EIP draft submission
