---
source: ethresearch
topic_id: 23588
title: Threshold Encrypted Mempools with mev-commit Preconfirmations
author: pepae
date: "2025-12-02"
category: Cryptography
tags: [mev, preconfirmations]
url: https://ethresear.ch/t/threshold-encrypted-mempools-with-mev-commit-preconfirmations/23588
views: 372
likes: 4
posts_count: 1
---

# Threshold Encrypted Mempools with mev-commit Preconfirmations

# Threshold Encrypted Mempools with mev-commit Preconfirmations

**by Murat Akdeniz (Primev), Bernardo Magri (Primev), Christian Matt (Primev), Punit Jain (Shutter Network), Anthony Caravello (Shutter Network), Luis Bezzenberger (Shutter Network)**

## Motivation

Ethereum users lose value daily to frontrunning, sandwich attacks, and censorship. A DEX swap gets sandwiched, an NFT mint gets frontrun. These attacks succeed because transactions sit visible in the public mempool before inclusion.

The user-side solution is encryption: hide transaction contents until execution order is fixed. But encryption alone isn’t enough. How do you ensure builders actually include encrypted transactions after committing to them?

This post presents the first threshold encrypted mempool for Ethereum’s out-of-protocol transaction supply chain. We combine Shutter’s threshold encryption with mev-commit’s preconfirmation infrastructure to create practical frontrunning protection deployable today without consensus changes.

**Key properties:**

- Users submit encrypted transactions hiding their intentions
- Builders commit blind before seeing contents
- Shutter Keypers release decryption keys only after sufficient commitments
- Oracle verifies inclusion and slashes builders who break commitments
- Validators can opt in seamlessly via mev-boost, Commit-Boost, or any other relay-supporting sidecar without additional operational overhead

We’re deploying a working proof of concept on Hoodi testnet. In the current PoC, the sequencer / RPC still sees transactions in plaintext briefly before encrypting them, so the main visibility improvement is between users and the public mempool / builders. In parallel, we are exploring integration with Kohaku-style approaches to move toward end-to-end pre-execution privacy where even the RPC cannot inspect transaction contents.

**Builder Integration**: Builders integrate with the encrypted mempool by extending their existing mev-commit provider workflow to accept and commit to blind encrypted bids. No changes to block construction logic are required beyond supporting the Shutterised Bid and placing decrypted transactions at the top of the block.

mev-commit exposes encrypted bids through its standard provider interface, allowing builders to receive them exactly like ordinary preconfirmation bids but without transaction contents. Builders evaluate these blind bids, issue commitments tied to transaction hashes, and rely on keypers to release decryption keys once the global commitment threshold is reached. After key release, builders fetch the decrypted transaction via the provider endpoint and include it in block construction.

**Validator Integration:** mev-commit integrates with commit-boost, mev-boost or any other sidecar that supports relays, allowing validators to opt into preconfirmations by simply selecting mev-commit-enabled relays in their Commit-Boost configuration.

## Background: Threshold Encryption and Preconfirmations

Threshold encryption distributes trust across multiple parties called **keypers**. A transaction encrypted under this scheme can only be decrypted when a threshold number of keypers (t out of n) cooperate to release their key shares. This prevents any single party from decrypting without a common decryption trigger.

The critical challenge for encrypted mempools is enforcement: how do we ensure builders actually include encrypted transactions they’ve committed to? Three approaches exist:

1. Trusted: Builders promise to include transactions (no enforcement)
2. Economic: Builders stake collateral that gets slashed for misbehavior (retroactive enforcement)
3. Cryptographic: Smart contracts or consensus rules prevent execution unless conditions met (proactive enforcement)

Our design uses economic enforcement through mev-commit’s preconfirmation infrastructure. Builders cryptographically commit to including specific transactions and back these commitments with slashable stake. We extend this mechanism to encrypted transactions, creating a system where builders commit blind to transaction contents.

The key insight is that commitment infrastructure already exists. Rather than waiting for consensus changes or smart account adoption, we can deploy encrypted mempools today by leveraging mev-commit’s existing slashing conditions and extending them to handle threshold-encrypted transactions.

## Design Overview

Our system integrates three components:

1. Sequencer: Receives encrypted transactions, along with identity preimages (random 32 bytes used for indexing encrypted transactions), generates bids for these transactions.
2. Keypers: Monitor builder commitments, release decryption keys when threshold met (≥3 commitments)
3. mev-commit: Provides commitment and slashing infrastructure through bidder/provider nodes and oracle

### Architecture

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/c/9ce588c6b5587d70120148a4748153de34802d43_2_690x438.png)image2230×1416 108 KB](https://ethresear.ch/uploads/default/9ce588c6b5587d70120148a4748153de34802d43)

### Transaction Flow

```auto
1. User encrypts via threshold cryptography
2. User submits encrypted transaction to sequencer
3. Sequencer submits encrypted bid to mev-commit bidder node
4. Bidder relays encrypted bid to builders (providers)
5. Builders evaluate and commit blind
6. Keypers validate commitment threshold, release keys
7. Builders decrypt and include transactions at top-of-block
8. Oracle verifies inclusion on L1
9. Oracle attests to mev-commit for rewards/slashing
```

The critical property is **conditional decryption**: keys are released only after sufficient builder commitments are secured. This prevents the “decryption then censorship” attack where builders see plaintext and selectively exclude transactions.

## Enforcement Mechanisms

### Commitment Threshold

Keypers implement threshold validation logic:

```go
func ShouldReleaseKey(identity Identity) bool {
  commitments := GetCommitments(identity)

  if len(commitments)  stake)
- Requires builder participation in mev-commit

Cryptographic enforcement through smart contracts would provide:

- Unconditional frontrunning protection
- No slashing of offline proposers
- Requires ERC-4337 adoption or similar account abstraction
- Needs new precompiles (TXINDEX, SLOT)
- Higher gas costs (on-chain validation)
- Limited to smart accounts without EIP-7702

These approaches are complementary. Future work could combine mev-commit commitments with smart contract validation for layered security.

### Out-of-Protocol vs. In-Protocol

Our out-of-protocol mev-commit approach:

- Deployable today
- Iterative improvement path
- Lower coordination cost
- Weaker guarantees than consensus enforcement
- Relies on economic security

In-protocol integration ([Shutter roadmap](https://ethresear.ch/t/the-road-towards-a-distributed-encrypted-mempool-on-ethereum/21717)) would provide:

- Strongest guarantees (consensus-enforced)
- No external slashing infrastructure
- Can integrate with FOCIL
- Requires hard fork
- Longer deployment timeline

## Open Questions

**Mechanism Design:**

1. Should commitment threshold vary by bid amount or validator participation?
2. Proportional vs. binary slashing? How to handle repeat offenders?
3. How should encrypted transactions be priced relative to normal transactions?

**Integration:**

1. In-wallet vs. dapp-side encryption?
2. What incentives drive builder participation?

**Security:**

1. Keyper selection for production: random validator sampling vs. dedicated set?
2. What if no builders commit? FOCIL integration?
3. Cross-domain MEV handling?

**Economics:**

1. Should backrunning profits be shared with users or keypers?
2. How do encrypted transactions compete for block space?
3. Can fees support keyper infrastructure long-term?

## Future Directions

**Short Term (3–6 months):** Builder onboarding, performance optimization, wallet integration, monitoring infrastructure

**Medium Term (6–12 months):** Dynamic thresholds, validator-backed keypers with slashing, relay integration

**Long Term (12+ months):** Smart contract integration for layered security, ePBS native support, FOCIL integration, in-protocol transition path, and deeper Kohaku / PSE-style integration for RPC-blind, end-to-end pre-execution privacy

The modular design allows incremental deployment without breaking existing functionality.

## Conclusion

We’ve presented a practical threshold encrypted mempool that leverages mev-commit’s preconfirmation infrastructure for economic enforcement. While retroactive slashing is weaker than proactive cryptographic enforcement, it offers a deployable path forward within Ethereum’s existing architecture.

The PoC on Hoodi testnet is the first step. Next steps involve expanding builder participation, optimizing performance, tightening RPC visibility with end-to-end approaches, and gathering data to inform production deployment and future in-protocol designs.

Encrypted mempools are critical for Ethereum’s fairness and decentralization. This work shows they can be deployed today. We invite builders, validators, and protocol developers to experiment with the PoC and provide feedback.

**Code & Documentation:**

- Sequencer: GitHub - shutter-network/primev-sequencer
- Keypers: rolling-shutter PR #629
- mev-commit: github.com/primev/mev-commit

**Acknowledgments:** This work builds on Shutter Network’s threshold encryption research and mev-commit’s preconfirmation infrastructure. Thanks to the broader encrypted mempool research community for valuable insights.
