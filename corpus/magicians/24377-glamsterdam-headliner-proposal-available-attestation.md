---
source: magicians
topic_id: 24377
title: "Glamsterdam headliner proposal: Available Attestation"
author: mingfei
date: "2025-05-29"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/glamsterdam-headliner-proposal-available-attestation/24377
views: 320
likes: 1
posts_count: 2
---

# Glamsterdam headliner proposal: Available Attestation

This is a headliner proposal for [Available Attestation (AA)](https://ethereum-magicians.org/t/eip-7942-available-attestation-a-reorg-resilient-solution-for-ethereum/23927) for Glamsterdam.

## Summary (ELI5)

Available Attestation (AA) is a proposed security upgrade to Ethereum that prevents malicious validators from reorganizing (reordering) blocks to steal transactions or manipulate the blockchain. Currently, attackers with enough stake can create competing blockchains and force the network to switch between them, causing instability. AA requires that before a new block can be built, it must prove that enough validators (at least 1/3) have seen and agreed on the previous block. This creates a “stability barrier” that prevents attackers from secretly building alternative chains and surprising the network with them later. The proposal benefits all Ethereum users by making the network more stable and secure against sophisticated attacks.

## Detailed Justification

### Primary Benefits

- Provable reorg resistance: Unlike current ad-hoc mitigations, AA provides formal mathematical guarantees against all known reorganization attacks in synchronous networks
- Unified defense: Replaces multiple band-aid solutions (proposer boosting v1/v2, safe-slots, various upgrades) with a single coherent mechanism

### Secondary Benefits

- Simplified protocol: Removes complex filtering rules and mid-epoch justification processes
- Better worst-case behavior: In attack scenarios, provides predictable degradation rather than catastrophic reorganization
- Academic rigor: Backed by peer-reviewed research (USENIX Security 2025 acceptance)

### Why Now?

1. Escalating attack sophistication: The progression from ex-ante reorg → balancing attack → sandwich reorg → staircase attack shows attackers are getting more sophisticated
2. Mitigation fatigue: Each new attack requires a new patch, creating complexity and potential new vulnerabilities
3. Network maturity: With ~1M validators, Ethereum now has the scale where AA’s assumptions (large committee sampling) work reliably
4. Proven alternatives failing: Current mitigations like proposer boosting create new attack vectors rather than solving the root problem

### Approach Justification vs Alternatives

- vs. Incremental fixes: AA addresses the root cause (ability to create surprise competing chains) rather than symptoms
- vs. Stronger assumptions: Unlike solutions requiring <20% adversarial stake, AA works with standard 1/3 Byzantine fault tolerance
- vs. Heavy protocol changes: AA requires minimal modifications compared to alternatives like complete fork choice overhauls

## Stakeholder Impact

### Positive Impact

- All users: Reduced risk of transaction reordering, MEV attacks, and chain instability
- DeFi protocols: More predictable transaction ordering reduces sandwich attack risks
- Node operators: Simpler fork choice logic reduces implementation complexity
- Researchers: Provides a formally verified foundation for future protocol development

### Negative Impact & Mitigations

- None

## Technical Readiness

### Maturity Assessment: Medium-High

- Specification: Complete formal specification provided in EIP-7942
- Research foundation: Peer-reviewed paper with formal proofs and 16,384 validator simulation
- Implementation status: Pseudocode provided, but production client implementations needed

### Missing Components

- Reference implementation in major clients (Prysm, Lighthouse, Teku, etc.)
- Comprehensive test vectors
- Devnet deployment and testing
- Integration with existing tooling (block explorers, analytics)

## Security & Open Questions

### Known Security Properties

- Proven secure against all documented reorg attacks in synchronous networks
- Maintains safety/liveness in partially synchronous networks (standard assumption)
- No new attack surfaces introduced

### Threat Model Assumptions

- Standard 1/3 Byzantine fault tolerance
- Eventually synchronous network (GST exists)
- Random committee sampling works as designed (no adaptive corruption during committee selection)

### Next Steps

1. Security audit: Formal review by multiple security firms
2. Stress testing: Large-scale testnet with adversarial scenarios
3. Economic analysis: Game-theoretic evaluation of validator incentives
4. Client diversity: Implementations across all major client teams before mainnet consideration

### Critical Dependencies

- Accurate validator committee sampling randomness
- Network synchrony assumptions holding in practice
- No undiscovered interactions with existing protocol mechanisms (MEV, withdrawal queues, etc.)

## Replies

**mingfei** (2025-06-06):

Google Drive link to ACD presentation:



      [drive.google.com](https://drive.google.com/file/d/1eRukEyj1wJbghAX0uvrV0cJRUFmdngn0/view?usp=drive_link)



      https://drive.google.com/file/d/1eRukEyj1wJbghAX0uvrV0cJRUFmdngn0/view?usp=drive_link

###

Google Drive file.

