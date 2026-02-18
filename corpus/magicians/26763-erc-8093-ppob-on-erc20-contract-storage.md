---
source: magicians
topic_id: 26763
title: ERC-8093 PPoB on ERC20 contract storage
author: jakeolo
date: "2025-11-28"
category: ERCs
tags: [erc, zkp, erc20, erc-8093]
url: https://ethereum-magicians.org/t/erc-8093-ppob-on-erc20-contract-storage/26763
views: 75
likes: 3
posts_count: 2
---

# ERC-8093 PPoB on ERC20 contract storage

# EIP-8093: Private ERC-20 — Zero-Knowledge Burns for Token Privacy

## Summary

EIP-8093 extends the zero-knowledge proof-of-burn mechanism from [EIP-7503](https://eips.ethereum.org/EIPS/eip-7503) to ERC-20 tokens. Users can burn tokens by transferring them to cryptographically unspendable addresses, then privately re-mint equivalent tokens using Merkle Patricia Trie (MPT) storage proofs and zero-knowledge circuits—all without revealing the original burn transaction.

**Pull Request**: https://github.com/ethereum/ERCs/pull/1379

**EIP**: [EIP-8093](https://eips.ethereum.org/EIPS/eip-8093)

---

## Motivation

EIP-7503 introduced “Zero-Knowledge Wormholes” for native ETH, enabling privacy-preserving burns and re-mints. However, the vast majority of value on Ethereum exists in ERC-20 tokens (USDC, DAI, WETH, etc.). Users deserve the same privacy guarantees for their token holdings.

### Current Privacy Solutions Fall Short

| Solution | Drawback | EIP-8093 Advantage |

|----------|----------|-------------------|

| **Mixer Contracts** | Require direct contract interaction → traceable deposit/withdrawal patterns | Burns are standard `transfer()` calls—indistinguishable from regular transactions |

| **Centralized Bridges** | Require trusting bridge operators | Fully trustless; cryptographic proofs replace trusted parties |

### Smooth Transition to Privacy

A key benefit of EIP-8093 is that it enables a **smooth transition path** to privacy for existing tokens:

- No Breaking Changes: The privacy mechanism can be added to existing ERC-20 tokens via proxy upgrades without changing any core ERC-20 functionality
- Backwards Compatible: All existing transfers, approvals, and integrations continue working exactly as before
- Opt-in Privacy: Users who want privacy can use the burn/mint flow; others continue using the token normally
- Gradual Adoption: Token projects can add privacy features incrementally without migrating liquidity or breaking DeFi integrations

This makes EIP-8093 ideal for established tokens that want to offer privacy without disrupting their ecosystem.

---

## How It Works

### 1. Burn Phase (Public)

The user generates a random `secret` and derives an unspendable burn address:

```auto
commitment = keccak256(secret)

burn_address = hash_to_curve(commitment)

```

The burn address is unspendable because finding a private key `k` such that `k × G = hash_to_curve(h)` is computationally infeasible.

The user then performs a standard ERC-20 `transfer()` to this burn address. No special contract interaction required—just a normal token transfer.

### 2. Proof Generation (Private)

After the burn block is finalized, the user generates:

1. Account Proof: MPT proof from block’s stateRoot to the token contract, extracting storageRoot
2. Storage Proof: MPT proof from storageRoot to the balance at the burn address
3. ZK Proof: Proves knowledge of secret and validity of proofs without revealing the burn address

### 3. Claim Phase (Public)

The user submits the proofs to a verifier contract, which:

1. Verifies block finality
2. Verifies the account proof against stateRoot
3. Verifies the ZK proof
4. Checks nullifier uniqueness (prevents double-claiming)
5. Mints/releases equivalent tokens to the recipient

---

## Key Design Decisions

### Two-Level Proof Structure

Unlike ETH balances stored in account state, ERC-20 balances live in contract storage. This requires:

1. Account proof (stateRoot → token contract)
2. Storage proof (storageRoot → balance slot)

This adds ~1M constraints to the ZK circuit but maintains equivalent privacy guarantees.

### Why Storage Proofs Over Event Logs?

We considered proving `Transfer` events but rejected this approach:

- Event logs reveal the sender address (privacy leak!)
- Receipt proofs are larger than storage proofs
- Events don’t cryptographically bind to unspendable addresses

### Nullifier Construction

```auto
nullifier = keccak256(secret || tokenAddress)

```

Including `tokenAddress` in the nullifier:

- Prevents cross-token collisions
- Allows the same secret for different tokens (safe, though not recommended)
- Binds claims to specific tokens for simpler verification

### Variable Storage Layouts

Different ERC-20 implementations store balances at different slots:

| Pattern | Mapping Slot | Examples |

|---------|--------------|----------|

| OpenZeppelin ERC-20 | 0 | Most tokens |

| OpenZeppelin (older) | 2 | Legacy tokens |

| USDC (FiatTokenV2) | 9 | USDC |

Implementations should provide a registry or discovery mechanism.

---

## Security Considerations

### Block Reorganization

Proofs MUST only be accepted for finalized blocks (2 epochs / ~12.8 minutes on post-merge Ethereum).

### Front-Running Protection

Claim transactions reveal the nullifier in the mempool, but front-running is not profitable:

- The ZK proof binds to specific parameters
- Changing the recipient requires a new valid proof
- Attackers cannot generate valid proofs without the secret

### Anonymity Set

The anonymity set is all burn addresses holding the same token. Users concerned about amount-based correlation should use common round amounts.

### Upgradeable Contracts

For proxy contracts, storage layouts may change. Users should claim promptly; historical proofs remain valid for their proven block.

---

## Open Questions for Discussion

1. Mapping Slot Discovery: Should we standardize a slot registry contract, or rely on off-chain discovery (e.g., Etherscan storage layout)?
2. Minimum Anonymity Set: Should implementations enforce minimum burn amounts or waiting periods to ensure adequate anonymity?
3. Fee Abstraction: How should users pay gas for claims without linking to their identity? Meta-transactions? Relayers?
4. Cross-Chain: How might this interact with L2s and bridges? Should we define a standard cross-chain claim mechanism?
5. Proving System Choice: Groth16 has faster verification but requires trusted setup per circuit. PLONK is universal but has larger proofs. What’s the right tradeoff?
6. Rebasing Tokens: How should we handle tokens with non-standard balance mechanics? Explicit incompatibility list?

---

## Relationship to EIP-7503

EIP-8093 is designed as a companion to EIP-7503:

| | EIP-7503 | EIP-8093 |

|—|---------|----------|

| **Asset** | Native ETH | ERC-20 tokens |

| **Proof Structure** | Account state | Account + Storage |

| **Nullifier** | `keccak256(secret)` | `keccak256(secret \|\| tokenAddress)` |

| **Burn Method** | Transfer to burn address | Transfer to burn address |

The same secret/burn address pattern works for both, enabling unified privacy workflows.

---

## Reference Implementation

A Python reference implementation for proof generation is available at: [jakeolo/private-erc20](https://github.com/jakeolo/private-erc20)

The implementation includes:

- MPT proof generation using eth_getProof RPC
- MPT proof verification
- Storage slot calculation for ERC-20 balances
- Mapping slot discovery for various tokens

---

## Feedback Welcome

We’re particularly interested in feedback on:

- ZK circuit optimizations
- Token compatibility edge cases
- Integration patterns for wallets and dApps
- Security model review

Looking forward to the community’s thoughts!

---

**Authors**: Jake ([@jakeolo](https://github.com/jakeolo))

## Replies

**SamWilsn** (2026-01-20):

Is this related at all to [Add ERC: Dual-Mode Fungible Tokens by 0xRowan · Pull Request #1359 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1359/files#diff-43aa64ec6861437334a4401b062ccb283d70b6160f793a3e69e7e514f9d32b2e) ? Would it make sense to collaborate with those authors?

