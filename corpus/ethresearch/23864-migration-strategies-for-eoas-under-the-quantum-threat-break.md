---
source: ethresearch
topic_id: 23864
title: "Migration Strategies for EOAs under the Quantum Threat: Breakages, and Open Questions"
author: Marcolopeez
date: "2026-01-16"
category: Cryptography
tags: [post-quantum]
url: https://ethresear.ch/t/migration-strategies-for-eoas-under-the-quantum-threat-breakages-and-open-questions/23864
views: 215
likes: 14
posts_count: 3
---

# Migration Strategies for EOAs under the Quantum Threat: Breakages, and Open Questions

Hi all, I’m Marco López (University of Málaga / NICS Lab + Decentralized Security).

We just got a paper accepted on **migration strategies for Ethereum EOAs** under a future **cryptographically relevant quantum computer (CRQC)** threat to **secp256k1/ECDSA**.

[Paper](https://www.researchgate.net/publication/399001903_Migration_Strategies_for_Ethereum_Externally_Owned_Accounts_under_the_Quantum_Threat)

We intentionally scoped the paper to the **execution layer** (EOA authorization, tx/signature flows, …). We don’t cover consensus-layer PQ migration (validator signatures, BLS/KZG, etc.).

## Quick context: great prior ethresearch work we’re building on

Before posting, we caught up on several excellent threads already exploring PQ transaction signatures and practical engineering trade-offs. Huge thanks to the folks driving these discussions, especially asanso and seresistvanandras:

- asanso (Part 1): “So you wanna Post-Quantum Ethereum transaction signature”
- asanso (Part 2): “Falcon as an Ethereum Transaction Signature: The Good, the Bad, and the Gnarly”
- asanso (Part 3): “The road to Post-Quantum Ethereum transaction is paved with Account Abstraction (AA)”
- seresistvanandras: “poqeth: Efficient, post-quantum signature verification on Ethereum” (+ benchmarks + naysayer mode)
 ePrint || Repo

Our paper is meant to be a simple first-pass survey of migration routes, but with a heavier emphasis on compatibility breakages and the attack surface that shows up during transitions.

## Why I’m posting here (call to the community)

This work is a **first (and intentionally simple) iteration**. We tried to map the main migration routes people discuss for making EOAs more resilient under a CRQC threat, and to highlight where things might break in practice.

The goal of this post is to **gather community input and consolidate effort** around the execution-layer side of this problem:

- Are we missing relevant mitigation options / migration routes?
- What other compatibility breakages (on-chain and off-chain) should be on the radar?
- What adversarial behavior / MEV / operational risks are we under-weighting?
- What prior papers / repos / threads should we cite or learn from?
- Who else is actively working on this, and where could collaboration make sense?

If you’re working on wallets, AA, infra, protocol research, audits, or L2 ecosystems, your perspective would be extremely valuable.

## What the paper covers (survey of routes + trade-offs)

We mapped the main approaches we see discussed for EOA migration toward post-quantum security, and tried to make the trade-offs explicit, especially where the approach intersects with today’s infrastructure and contract patterns.

- Native PQ signatures (protocol/EVM path): replace ECDSA with a PQ scheme.
 Conceptually straightforward, but verification costs and signature/key sizes vary widely by scheme, affecting tx size, gas/performance, and sometimes address derivation. It’s also a slower protocol-level rollout.
 Hash-based note (minimalism angle): we spend some time discussing hash-based signatures, because Ethereum already relies heavily on hash functions as a core primitive. Using hash-based signatures can look “cryptographically minimal” (you’re not introducing a brand-new hardness assumption the way lattice/isogeny/etc. would). Also, many hash-based constructions can have very small “public keys” on-chain (often just a hash / root commitment), which aligns with the “Large public keys are a no-go in the context of Ethereum.” theme highlighted in poqeth. Of course, the trade-offs move elsewhere (signature sizes, statefulness, UX/mempool friction), which is exactly where we want more community input.
 Small nuance we mention: stateful hash-based signatures (e.g., XMSS/LMS) can be awkward in general systems because they require state management, but blockchains can potentially manage that state on-chain (index/nonce-like). There are precedents in other ecosystems (e.g., QRL using XMSS).
- ERC-4337 account abstraction: usable today; verification happens inside the account contract, so a wallet can require PQ signatures to authorize operations and reduce the user’s direct exposure to ECDSA-based quantum attack.
 The catch (discussed in the asanso series as well) is that the bundler still posts an ECDSA-signed transaction, so the end-to-end flow is not fully PQ-resistant. It also introduces extra moving parts (mempool-like infrastructure, fees, operational complexity).
- Native AA proposals (RIP-7560 / EIP-7701 directionally): a clean crypto-agility endgame: accounts are defined by attached verification logic (PQ verification, multisigs, passkeys, etc.), removing fixed ECDSA assumptions at the account model level.
 Requires deep protocol changes; timelines and final designs are uncertain.
- EIP-7702 delegation: a pragmatic hook to attach new validation logic to an existing EOA/address without migrating to a new account model. This can enable experimentation with PQ-aware validation and account policy while preserving the address and existing relationships.
 Key limitation: as long as the protocol still accepts the EOA’s ECDSA key, it remains the “root authority” (in a CRQC setting, that residual authority is particularly problematic).
- EIP-7702 + key-deactivation variants: discussed ideas to close that loop: after delegation, the original ECDSA key could be deactivated (ideally permanently), so control routes exclusively through delegated logic while preserving the address and its associated assets/relationships.
 We treat these as part of the broader design space for eliminating “root ECDSA authority” once a more flexible validation mechanism exists.

Across all routes, we try to keep a practical lens: **where does ECDSA still remain**, what new infrastructure assumptions appear, and what breaks in the ecosystem during a transition.

## Compatibility / breakage hotspots (“dirty zone”)

Where we expect most of the challenges:

- ecrecoverbased auth in deployed contracts (signatures-as-identity).
 A lot of on-chain authorization is effectively “signature-as-identity” via ecrecover. In a PQ migration, it’s not enough to stop using ECDSA at the transaction layer. As long as ecrecover remains a valid precompile for ECDSA, existing contracts can continue to treat ECDSA off-chain signatures as authoritative. So any serious transition needs a story for how ECDSA ecrecover-style verification is handled (and whether it is restricted, replaced, or complemented by new verification paths), otherwise legacy off-chain signatures may keep power inside contracts even after EOAs stop using ECDSA for transactions.
 (Related: As raised in asanso’s AA/Falcon thread, many PQ schemes don’t support “key recovery”, for example “plain” Falcon doesn’t support public key recovery from a signature, so ecrecover-style patterns don’t carry over. A Falcon-based wallet would typically need to verify against a stored/registered public key. There is also a “recoverable” model discussed in the Falcon paper (Section 3.12, as Renaud Dubois pointed out) that enables key recovery, but it roughly doubles the signature size, which has obvious on-chain/bandwidth implications)
- ERC-2612 permit + broader off-chain signing flows (typed data, app-specific auth, meta-tx patterns)
- tx.origin assumptions (EOA vs contract identity, brittle authorization logic)
- L2s + cross-chain drift (identity semantics, replay domains, bridging assumptions)
- MEV during migration windows (ordering/races around delegation, revocation, “last valid signature” moments)

A big part of what we want from the community is: what else belongs on this list, and what’s actually most damaging in practice?

## Quantum emergency hard fork as a fallback (in parallel)

Separately from “smooth migration” paths, the **quantum emergency hard-fork** idea is an important piece of the resilience story.

Vitalik’s March 2024 post ([“How to hard-fork to save most users’ funds in a quantum emergency”](https://ethresear.ch/t/how-to-hard-fork-to-save-most-users-funds-in-a-quantum-emergency/18901)) frames a credible last-resort response if practical quantum capabilities appeared suddenly and large-scale theft started happening: rollback to pre-theft, disable legacy EOA transactions, and provide a recovery path that moves control into quantum-safe smart-contract validation.

We mention this not as a plan to push proactively (it’s costly and socially/operationally heavy), but as a reminder that **emergency planning matters,** and that in parallel, the ecosystem can (and arguably should) work on routes that enable **more gradual crypto agility** so we’re not forced into “break glass” mode.

## What we’re explicitly asking for

If you reply, pointers to **threads/papers/repos/teams** are extremely helpful.

1. Are there migration routes / mitigations we’re missing (at the execution layer), or important variants we should incorporate?
2. What compatibility breaks (on-chain and off-chain) do you think are most urgent or most likely to cause real user harm? Any concrete examples appreciated.
3. What adversarial behavior / MEV / operational risks should be considered during migration (front-running/races, griefing, “last valid signature” issues, infra compromise, stuck-tx dynamics for one-time/stateful schemes, etc.)?
4. Are there known classes of contracts or wallet patterns where ecrecover, permit, or tx.origin assumptions make migration particularly nasty?
5. Do you know of measurements/datasets/tools that help quantify the prevalence of these patterns (e.g., scans for ecrecover, permit usage in the wild, …)?
6. Who else is actively working on CRQC / crypto agility for EOAs right now? If you’re involved (or know someone who is), we’d love to connect.

We’re approaching this as a **public good** effort (UMA/NICS Lab + Decentralized Security). Very open to review, corrections, and collaboration where it makes sense.

## Closing / events

We’ll be presenting the paper at a congress at the University of La Laguna (Tenerife, Spain) in mid-March. We’re also aiming to present follow-up work at the **Workshop on Cryptographic Tools for Blockchains** ([CTB-26](https://www.ctb-workshop.org/)), associated to Eurocrypt in Rome in 9 May 2026.

If you’re working in this area, we’d be happy to meet you at either event.

By the way, the submission deadline for CBT26 is at the end of February, so you still have time.

Thanks!! looking forward to your feedback.

## Replies

**SirSpudlington** (2026-01-16):

I am the author of [EIP-7932: Secondary Signature Algorithms](https://eips.ethereum.org/EIPS/eip-7932) which is designed to be a crypto-agile framework for the execution layer. It was meant to be for transaction migration, but the core developer teams seemed to favour account abstraction (see [All Core Devs Execution #225 - Forkcast](https://forkcast.org/calls/acde/225/#t=4544) and [All Core Devs Execution #224 - Forkcast](https://forkcast.org/calls/acde/224/#t=4157)) over native transactions, so it was slimmed down to be just an algorithm registry and an `ecrecover` alternative. Even still, [EIP-6404](https://eips.ethereum.org/EIPS/eip-6404#:~:text=Transaction%20signatures%20are%20represented%20by%20their%20native%2C%20opaque%20representation%2C%20prefixed%20by%20a%20value%20indicating%20their%20algorithm) natively supports the 7932 registry and [EIP-8030: P256 algorithm support](https://eips.ethereum.org/EIPS/eip-8030), [EIP-8051: Precompile for ML-DSA signature verification](https://eips.ethereum.org/EIPS/eip-8051) and [EIP-8052: Precompile for Falcon support](https://eips.ethereum.org/EIPS/eip-8052) support the EIP-7932 framework (though EIP-8051 & EIP-8052 still use the old algorithm trait).

From what I have seen, the whole PQ migrations roadmap is very fragmented. Proposals are generally competing with each other so I wouldn’t consider any proposal the current one (except maybe for account abstraction which can happen without much protocol modification)

---

**shemnon** (2026-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/marcolopeez/48/21707_2.png) Marcolopeez:

> Native PQ signatures (protocol/EVM path): replace ECDSA with a PQ scheme.

The paper is gated behind ResearchGate so I haven’t read it, but this section should discuss Cryptographic Agility. Any EOA revision should allow for multiple signature algorithms and strengths, even if mainnet settles on a subset. I expect at least one PQ scheme to be busted (or at least busted to the level it is deprecated) in the next 10-20 years after selection. If I knew which one it was I’d have a different job.

