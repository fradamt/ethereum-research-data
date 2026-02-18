---
source: magicians
topic_id: 27448
title: "Hegotá Headliner Proposal: EIP-8105 Universal Enshrined Encrypted Mempool (EEM)"
author: jannikluhn
date: "2026-01-16"
category: Magicians > Primordial Soup
tags: [hegota, headliner-proposal]
url: https://ethereum-magicians.org/t/hegota-headliner-proposal-eip-8105-universal-enshrined-encrypted-mempool-eem/27448
views: 351
likes: 6
posts_count: 2
---

# Hegotá Headliner Proposal: EIP-8105 Universal Enshrined Encrypted Mempool (EEM)

## Hegotá Headliner Proposal: EIP-8105 Universal Enshrined Encrypted Mempool (EEM)

### Summary (ELI5)

EIP-8105 ([ethresear.ch thread](https://ethresear.ch/t/universal-enshrined-encrypted-mempool-eip/23685/13), [GitHub PR](https://github.com/ethereum/EIPs/pull/10943)) introduces the Universal Enshrined Encrypted Mempool (EEM) as an optional, protocol-level feature. It allows users to submit transactions that remain encrypted until they are included in a block, protecting them from front-running, sandwich attacks, and real-time censorship.

EEM aims to restore Ethereum’s public mempool as a single, open coordination layer where all users can participate on equal footing. Today, most users avoid the public mempool because transactions are visible as soon as they are broadcast, which allows others to interfere with them. This has pushed transaction flow into private order flow systems, causing fragmentation, greater reliance on trusted third parties, and increased builder centralization. By making the public mempool safe to use again, EEM strengthens decentralization, openness, and credible neutrality at the core of Ethereum.

The design is encryption-technology agnostic, providing a generalized encrypted mempool interface that supports multiple independent key providers to encrypt/decrypt transactions (e.g. TEEs, threshold encryption, FHE-based schemes), without locking Ethereum into a single approach.

EEM is designed to fit naturally with ePBS: builders can include encrypted transactions without understanding their contents, while plaintext transactions remain fully supported and unaffected, with no added latency or impact on existing transaction flows.

### Champion

Jannik Luhn ([jannikluhn · GitHub](https://github.com/jannikluhn))

## Detailed Justification

### Primary and secondary benefits

**Primary benefits**

1. Improved real-time censorship resistance Encrypting transaction contents until inclusion prevents builders, relays, and searchers from selectively censoring transactions based on calldata, recipients, or economic intent.
2. Reduced builder centralization pressure MEV is a powerful centralizing force: the more MEV a builder can extract, the more capital, market share, and dominance they accumulate across the transaction supply chain. By reducing extractable MEV through transaction encryption, EEM weakens this feedback loop.
Users no longer need to route transactions through the largest or most “trusted” builders to avoid front-running, since encrypted transactions are equally safe regardless of who builds the block, making builder size and privileged relationships less decisive and lowering centralization pressure.
3. Protection from malicious MEV Front-running and sandwich attacks that rely on mempool visibility are prevented due to the nature of the transactions being hidden, without requiring application-specific mitigations or private infrastructure. Backrunning of the encrypted transactions remains possible after inclusion and is naturally performed by the builder of the subsequent block, preserving legitimate price discovery and arbitrage without exposing users to pre-execution exploitation

**Secondary benefits**

1. Restoration of a unified public mempool Today’s mempool is effectively fragmented into many private orderflow channels, forcing users into opaque, permissioned pathways that are inefficient and unfair. By encrypting transactions rather than hiding them, EEM makes the public mempool viable again, reducing fragmentation, shrinking private orderflow, and re-establishing a single, open coordination layer where all users can participate on equal footing.
2. Improved builder participation and revenue diversity Encrypted transactions allow builders to earn fees from orderflow that would otherwise bypass the public pipeline, creating additional revenue opportunities without requiring privileged access or trust. By making transaction safety independent of builder size or reputation, EEM levels the playing field, allowing smaller builders to compete more effectively and reducing the advantage of large, highly trusted builders.
3. Protocol extensibility The encryption-agnostic design supports multiple key-provider models and opens a new, competitive market for key providers to offer services directly to the protocol. By splitting responsibilities between builders, validators, and independent key providers, EEM adds new decentralized stakeholders to the transaction pipeline and enables future extensions such as stronger scheduling primitives.

### Why now?

- ePBS provides the architectural foundation for separating transaction inclusion from execution details, making an encrypted mempool a natural next step. Latency of non-encrypted transactions is not affected.
- Encrypted mempools are already deployed out-of-protocol, reducing implementation risk and providing operational experience.
- MEV-driven centralization and censorship concerns are increasingly first-order protocol issues rather than edge cases.
- There is a broader push toward privacy on Ethereum, even when privacy is temporary rather than permanent, as a means to improve fairness, censorship resistance, and UX.
- Relevant encryption technologies have matured significantly in recent years (MPC, TEE-based systems, and FHE-related schemes) making protocol-level integration more realistic and lower risk than in earlier roadmap phases.
- Hegotá is well positioned to prioritize fairness, decentralization, and censorship resistance as explicit upgrade goals.

### Why this approach?

- Protocol-level, optional design: avoids liquidity fragmentation while preserving full backwards compatibility.
- Encryption-agnostic interface: prevents premature standardization around a single cryptographic scheme.
- Builder-compatible ordering model: encrypted transactions can be appended without opportunity cost.
- Graceful failure modes: chain liveness is preserved even if key providers fail or withhold keys.

Especially compared to application-level or private mempool solutions, EEM offers higher systemic impact with lower coordination risk.

## Stakeholder Impact

### Positive

- Users & wallets: MEV protection, predictable execution, better UX.
- Institutions: MEV protection, complies with potentially upcoming MEV/front-running regulation.
- Applications & DeFi protocols: reduced reliance on fragile anti-MEV patterns.
- Builders & relays: Leveling the playing field/less reliance on trust could benefit smaller builders to be able to compete. Additional revenue from processing encrypted transactions, reduced regulatory exposure.
- Ethereum protocol: lower centralization pressure and improved censorship resistance.

### Negative / Trade-offs

- New trust assumptions around key providers

Mitigated via multiple providers, cryptographic enforcement, and reputation mechanisms.

**Additional protocol complexity across EL and CL**

- Accepted in exchange for addressing systemic MEV and censorship externalities

**Potential UX complexity**

- Optional usage ensures unaffected workflows for existing users.

**Increased block building complexity**

- Builders need to conform to additional block building constraints

## Technical Readiness

- Draft EIP with detailed execution-layer and consensus-layer changes
- Prior work from the Shutterized Beacon Chain and production encrypted mempools
- Active discussion and review on EthResearch and Ethereum Magicians
- No mandatory cryptographic primitives or new precompiles required

## Security & Open Questions

**Transaction ordering and key-withholding influence** A key question concerns whether key providers could influence transaction outcomes by selectively withholding decryption keys. As clarified in follow-up discussion, this influence is constrained to a single bit (key revealed or not), affects only encrypted transactions that follow within the same block, and does not impact plaintext transactions or earlier encrypted transactions. The remaining risk is bounded, well-understood, and comparable to trust assumptions already present in MEV-aware block construction.

**Key provider technology and ecosystem selection** An open question is which concrete key-provider technologies and operators should initially integrate with EEM (e.g. TEE-based, threshold encryption, or FHE-based providers), and what incentive or reputation mechanisms they should adopt. The proposal intentionally does **not** lock this down at the protocol level. Several viable candidates already exist, and the expectation is that this ecosystem evolves through competition rather than premature standardization.

## Replies

**jannikluhn** (2026-02-02):

We’re hosting a Q&A and discussion session on EIP-8105 tomorrow **Tuesday, February 3 2025, 9am EST / 3pm CET / 10 PM HKT**. Anyone reading this, you’re invited to join! [EIP-8105 Q&A Discussion Session](https://calendar.google.com/calendar/event?&eid=NHU1ZTFwYW1ycDJ2MGJ0azdwcXJoM2FmZmcgY185ZTEzYWFmYjc4Mjk5Nzc4MDJmOWRhZGFhMzM0ZmY2NDhkN2FjOTZkNDRmYjQzZjJiZmM4NmIzOTdjMGRiZjVjQGc&tmsrc=c_9e13aafb7829977802f9dadaa334ff648d7ac96d44fb43f2bfc86b397c0dbf5c)

