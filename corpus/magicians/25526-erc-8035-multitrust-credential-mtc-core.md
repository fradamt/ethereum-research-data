---
source: magicians
topic_id: 25526
title: "ERC-8035: MultiTrust Credential (MTC) — Core"
author: y_hoshino
date: "2025-09-19"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8035-multitrust-credential-mtc-core/25526
views: 271
likes: 6
posts_count: 16
---

# ERC-8035: MultiTrust Credential (MTC) — Core

Hello everyone,

We are proposing a minimal on-chain anchor for VC-aligned reputation credentials (MTC Core) and an optional ZK presentation interface (MTC-ZK) with a fixed Groth16 ABI—enabling privacy-preserving, interoperable eligibility checks (e.g., score ≥ 80, violations ≤ 2). We are seeking community feedback on the initial draft.

## Problem & Motivation

dApps need to evaluate user reputation or eligibility across apps without revealing raw data. Today’s approaches are bespoke or SBT-centric, fragmenting semantics and making revocation and consistency difficult.

**MTC** standardizes issuing/updating/revoking a **non-transferable** credential and verifying **only the predicate** (not the raw value) via a fixed ZK ABI, so wallets/SDKs/dApps can check the same thing the same way.

## Use cases

### A. Learning: “Reward NFT for score ≥ 80”

- A platform issues an examScore metric to the student’s address via MTC (on-chain stores only a commitment; the actual score remains off-chain).
- The student presents a ZK proof for score ≥ 80; no raw score is disclosed.
- A rewards contract calls proveMetric(...) → true ⇒ mints a “Pass” NFT.
- If cheating is later found, the issuer revokes the metric; subsequent claims fail automatically.

**Benefits:** Show only “qualified,” reuse the same predicate across apps, immediate and auditable revocation.

### B. Community/Mobility: “VIP event for violations ≤ 2”

- The operator tracks violationPoints on MTC; policy (LTE) is fixed via CompareMask (GTE/LTE/EQ, inclusive) and may be frozen.
- Users prove violations ≤ 2 with ZK for entry; violation details remain private.
- Staff updates/penalizes via updateMetric/slash; rule changes are governed and logged.

**Benefits:** User privacy; consistent policy and instant revocation; transparent audit trail.

## Specification (at a glance)

**MTC Core (ERC category)**

- Schema: registerMetric(metricId, role, mask)
- Write: mint / mintBatch / updateMetric / updateMetricBatch / revokeMetric / slash
- Read: getMetric(tokenId, metricId), tokenIdOf(address)
- Non-transferable & one token per subject: MUST
- CompareMask: GTE=1, LTE=2, EQ=4 (inclusive); after freeze, setCompareMask MUST revert
- Events: MetricRegistered / MetricUpdated / MetricRevoked / Slash / CompareMaskChanged / MaskFrozenSet
- ERC-165: MUST implement and expose interfaceId

**MTC-ZK (optional)**

- proveMetric(a,b,c,publicSignals) with fixed order [mode, root, nullifier, addr, threshold, leaf]
- Binding: root == leafFull (current Core anchor), tokenId == tokenIdOf(address(uint160(addr)))
- Policy: mode must be allowed by Core mask; mask mismatch and mode==0 MUST revert
- Domain separation (in circuit):
treeLeaf = Poseidon(leaf, addr, keccak256(abi.encode(chainid(), address(this))))
- Optional events: VerifierSet, ProofVerified

## Why MTC (design benefits)

- Privacy × Interop: Predicate-only proofs; one stable ABI across wallets/dApps
- Instant revocation: revokeMetric makes future claims fail by construction
- Policy consistency: CompareMask (+ freeze) avoids ad-hoc rule changes
- One per subject, non-transferable: Prevents lending/marketplaces
- Replay-safe: Bound to Core’s current anchor and a domain-separated leaf

### Related ERCs — Differences at a Glance

| Aspect | MTC (proposed) | ERC-725/735 | ERC-4973 | ERC-5192 |
| --- | --- | --- | --- | --- |
| Goal / Scope | VC-aligned reputation metrics on a non-transferable credential; issue / update / revoke; verify predicates only via ZK | 725: identity registry; 735: claims model | Account-bound token (ABT) | Minimal SBT (lock state only) |
| Representation | Non-transferable credential + metric (value kept as commitment) | Identity / claims registry (may contain PII) | Non-transferable token | Non-transferable token |
| Transferability | MUST NOT transfer; one token per subject (MUST) | N/A | Non-transferable | Non-transferable |
| On-chain data | Commitment + timestamps; PII stays off-chain | Claims (content depends on app; may include PII) | Token ownership | Token ID + lock state |
| Verification | Fixed ZK ABI checks predicate only (e.g., score ≥ threshold) | Claim validity / signatures | Ownership ≈ eligibility | Locked ≈ eligibility |
| Revocation | revokeMetric ⇒ immediate invalidation (later proofs fail) | Claim revocation (app-specific) | Up to issuer (out of scope) | Minimal (lock/unlock) |
| Policy control | CompareMask (GTE/LTE/EQ, inclusive) + freeze (no further changes) | Out of scope | Out of scope | Out of scope |
| ZK | Yes (optional): proveMetric(a,b,c,publicSignals) with fixed order | Not specified | Not specified | Not specified |
| Replay resistance | Current Core anchor (root == leafFull) + domain-separated leaf (chainId + contract) | Impl-specific | Impl-specific | Impl-specific |
| ERC-165 | Required (Core & ZK) | Impl-specific | Yes | Yes |
| Typical use | Threshold checks (scores/violations), reward NFTs, gated entry | KYC/attribute claims storage & presentation | Achievement badges, memberships | Minimal “present/issued” signal |
| Composability | Use MTC to decide, then mint 4973/5192 tokens as badges | Can back MTC via off-chain VC layer | Use MTC as pre-check; mint ABT on success | Use MTC as pre-check; minimal SBT for display |

> TL;DR: MTC standardizes predicate verification (not raw values) with ZK.
> 725/735 = claim/identity layer; 4973/5192 = token representations. MTC sits upstream as a shared, privacy-preserving decision layer and composes well with them.

## Draft EIPs (EIP-1 compliant)

- Core: Add ERC: MultiTrust Credential (MTC) by YutaHoshino · Pull Request #1233 · ethereum/ERCs · GitHub
- MTC-ZK: Add ERC: ZK Presentation Interface for MTC by YutaHoshino · Pull Request #1234 · ethereum/ERCs · GitHub

## Reference implementation (non-normative)

Contracts: [MultiTrustCredential.sol](https://github.com/hazbase/contracts/blob/main/multi-trust-credential/contracts/MultiTrustCredential.sol)

---

As this is our initial draft, I’d greatly appreciate broad feedback—on terminology, spec clarity, and interop. Suggestions and alternatives are welcome.

## Replies

**y_hoshino** (2025-09-29):

We have built a simple test code to experiment with the proposed **MultiTrust Credential (MTC)** concept.

In this demo, you can record hidden information into MTC (e.g., country of affiliation, exam score) and then generate ZK proofs to show:

- whether your country is included in a whitelist,
- whether your score is above a given threshold,
without revealing the raw values.

More details and usage instructions are in the README:



      [github.com/hazbase/zk](https://github.com/hazbase/zk/blob/main/README.md)





####

  [main](https://github.com/hazbase/zk/blob/main/README.md)



```md
# @hazbase/zk
[![npm version](https://badge.fury.io/js/@hazbase%2Fzk.svg)](https://badge.fury.io/js/@hazbase%2Fzk)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview
`@hazbase/zk` is an utility toolkit for **Poseidon hashing**, **Merkle trees**, and **Groth16 proofs**.
It is designed to be used **together with MultiTrustCredential (MTC) and Whitelist** and provides low-level APIs to verify **commitment-based metrics** (e.g., score ≥ threshold, membership, allowlists) with **minimal disclosure**.

Core capabilities:
- Poseidon helpers (`init`, `toF`, `H1/H2/H3`, `genSalt`)
- Repeatable, **deterministic** Merkle construction (normalize → deduplicate → sort ascending → pad)
- Root recomputation, path generation, and verification (`buildAllowTree`, `getProofByIndex`, `findLeafIndex`, etc.)
- **Groth16** proof generation (`generateProofAllowlist`) with pre-proof sanity checks
- First-class integration with **MTC (@hazbase/kit)** for on-chain proof flows

---

## Requirements
- **Node.js**: 18+ (ESM recommended)
- **Deps**: `snarkjs`, `circomlibjs`, `ethers`
```

  This file has been truncated. [show original](https://github.com/hazbase/zk/blob/main/README.md)










Feedback on the implementation, spec alignment, and use cases would be highly appreciated.

---

**y_hoshino** (2025-10-15):

I’ve summarized the worldview achievable with MTC in a short story format.

I’d love to hear your thoughts.


      ![image](https://miro.medium.com/v2/5d8de952517e8160e40ef9841c781cdc14a5db313057fa3c3de41c6f5b494b19)

      [Medium – 13 Oct 25](https://medium.com/@hazbase/the-power-of-zero-knowledge-proofs-1d1d820d75b5)



    ![image](https://miro.medium.com/v2/resize:fit:1200/1*JxQvadXYmy4wnK_cR8aWTQ.png)

###



“May I check your age?”
 “Sure. Here’s proof I’m 21 or older… but my birthdate stays private.”
— It sounds like the future, but it’s…



    Reading time: 5 min read

---

**allfinan** (2025-12-12):

Right now the CompareMask supports EQ / GTE / LTE.

For credit modules, two more conditions might be useful to be added:

- bounded range (e.g., score ∈ [x,y])
- delta constraints (e.g., “score hasn’t decreased more than Δ since last epoch”)

---

**y_hoshino** (2025-12-12):

Thanks a lot for the suggestion. Totally agree these are very relevant for credit modules.

For bounded range (x ≤ score ≤ y), today it can be expressed by combining GTE and LTE checks, but having a first-class “RANGE” style predicate could simplify UX/SDK and on-chain integration. Happy to explore that.

For delta constraints (e.g., “no more than Δ change since last epoch”), I also agree it’s useful, though it likely needs an explicit epoch/freshness model (and possibly referencing a prior epoch state). My initial thought is to keep ERC-8035 minimal and maybe we can discuss RANGE/DELTA as part of the ZK/presentation extension (ERC-8036) or a credit-focused extension.

---

**allfinan** (2025-12-15):

That makes a lot of sense — I agree with keeping ERC-8035 minimal and pushing higher-order constraints into a presentation or domain-specific extension.

I like the idea of **RANGE** as a first-class predicate mainly for UX and integration clarity, even if it compiles down to GTE+LTE internally. That feels like a clean win for SDKs and downstream credit modules.

For **DELTA**, I agree it naturally ties into an explicit epoch/freshness model. Treating it as a presentation-layer concern sounds right and keeps MTC-Core simple and future-proof.

If you’re planning an ERC-8036 or credit-focused extension, I’d be very interested in contributing ideas or concrete interfaces — especially around epoch binding and replay safety.

---

**y_hoshino** (2025-12-17):

Thanks! Really glad we’re aligned.

I’ll put together a draft update for ERC-8036 to cover RANGE and DELTA, and let’s continue the discussion in the ERC-8036 thread:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/y_hoshino/48/15903_2.png)
    [ERC-8036: ZK Presentation Interface for MTC (8035)](https://ethereum-magicians.org/t/erc-8036-zk-presentation-interface-for-mtc-8035/25648) [ERCs](/c/ercs/57)



> MTC-ZK defines an optional, fixed Groth16-style ABI (proveMetric) to verify predicates only (e.g., score ≥ threshold) against MTC Core (ERC-8035) anchors—without revealing raw values.
> Problem & motivation
> dApps often need threshold checks while preserving privacy and supporting revocation at scale. MTC-ZK provides a stable verifier ABI and binding rules so wallets/dApps can verify the same predicate the same way.
> Scope
>
> proveMetric(a,b,c,publicSignals) with fixed order [mode, root, nullifier…

I’d love your input on the concrete interfaces there, especially around epoch binding and replay safety.

---

**allfinan** (2025-12-30):

Here’s another suggestion.

For multi-market credit systems, I’d recommend binding proofs to:

- contract address
- chainid
- anchor root
- epoch/version

The epoch field prevents long-lived proofs from being reused across credit cycles.

---

**y_hoshino** (2025-12-31):

Thanks Alan, really helpful suggestion.

We already bind proofs to chainId + contract address (domain separation) and to the anchor root in the current draft/implementation.

The remaining question is whether we should generalize epoch/version binding across *all* proofs (baseline included), or keep it mandatory only for certain predicate types (e.g., DELTA) where replay across credit cycles is a bigger concern.

I’ll think through the trade-offs (UX/complexity vs. replay resistance) and update the draft accordingly. If you have a strong opinion on “MUST vs SHOULD” for epoch/version, I’d love to hear it.

---

**MASDXI** (2026-01-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/y_hoshino/48/15903_2.png) y_hoshino:

> complexity vs. replay resistance

I think should care about to replay resistance first UX/complexity is later.

---

**y_hoshino** (2026-01-12):

Thanks, I totally agree. Replay resistance should come first and we can iterate on UX later.

My current take is below, curious if you see any pitfalls.

We already bind proofs via domain separation (chainId + contract address) and the anchor root.

I’m leaning toward generalizing epoch/version across predicates (MUST for DELTA, likely SHOULD for others), and we can consider extending the baseline flow next.

---

**CertifiedCryp** (2026-01-14):

Thoughts:

# ERC-8035 Forum Post Draft

-–

Really excited to see this proposal. I’ve been thinking about trust infrastructure for DeFi from a market making perspective, and MTC addresses gaps I’ve encountered firsthand.

## Context: Why This Matters for Trading Infrastructure

I’m building market making systems on Linea (Avellaneda-Stoikov framework + orderbook analysis). The missing piece has always been a trust layer that doesn’t require doxxing counterparties or relying on centralized reputation providers.

## Concrete Use Cases for MTC in Trading/DeFi

****1. Market Maker Credentialing****

- Prove “liquidations < X in 90 days” without revealing trading history

- Prove “volume > Y threshold” for tier access without exact amounts

- DEXs could gate MM programs on verifiable track records

****2. Counterparty Risk in OTC/RFQ****

- Prove “wallet age > 6 months” + “no flagged interactions”

- Settlement confidence without KYC exchange

****3. Anti-Sybil for Airdrops/Rewards****

- Prove “unique human” or “completed action X” without linkable identity

- Prevents farming while preserving privacy

****4. Cold-Start & Post-Exploit Recovery****

This is personal - I recently lost funds to an EIP-7702 phishing attack (malicious delegation via fake dapp). Now I’m on a fresh wallet with zero on-chain history. Rebuilding trust is currently impossible.

****The bootstrap problem MTC should address:****

**Option A: Migration Proof**

- Sign a message from OLD wallet attesting “NEW wallet is my successor”

- Issuer verifies signature, revokes old credential, issues to new address

- ZK variant: prove ownership of old credential without revealing old address (privacy from chain analysis)

**Option B: Vouching/Invite System**

- Existing credential holders can “vouch” for new addresses

- Voucher stakes reputation (slash if vouchee misbehaves)

- Creates web-of-trust bootstrap path

- Could require N vouches from holders with score ≥ threshold

**Option C: Probationary Credentials**

- New wallets get time-limited, lower-tier credentials

- Graduate to full credentials after behavioral proof (time + activity)

- Allows participation while building history

**Option D: Off-chain Bridge**

- KYC provider or trusted third party issues credential to new address

- Proves continuity of identity without on-chain linkage

- Privacy tradeoff but practical for recovery scenarios

Without a bootstrap mechanism, MTC only works for established wallets - excluding anyone who’s been compromised, lost keys, or is genuinely new. This seems critical for adoption.

****5. Sanctions/Whitelist Compliance****

- Prove “NOT on OFAC list” without revealing jurisdiction

- Prove “passed KYC with provider X” without sharing PII

- Enables compliant DeFi without centralized gatekeepers

## Technical Suggestions

On the RANGE/DELTA discussion - for trading contexts, I’d also consider:

****TIME-WEIGHTED predicates****

- “Average score ≥ X over period Y”

- Prevents gaming via temporary spikes

****MONOTONIC constraints****

- “Value has never exceeded X” (useful for violation caps)

- Different from point-in-time checks

****Composite credentials****

- Prove multiple predicates atomically

- “score ≥ 80 AND violations ≤ 2 AND age > 180 days”

## On Replay Resistance

Strongly agree with [@allfinan](/u/allfinan) on epoch binding being critical. For credit/trading contexts, a proof from 6 months ago is nearly meaningless.

Lean toward MUST for epoch in any financial predicate, SHOULD for social/achievement credentials where staleness is less critical.

## Integration Path

I see MTC sitting upstream of:

- Access control for DEX tiers/features

- Collateral requirements (better reputation = lower requirements)

- Fee structures (verified MMs get better rates)

- Dispute resolution (credential history as evidence)

## High Trust Counter: Wallet UX & Behavioral Metrics

Borrowing from the Coulter Counter philosophy - simple, direct measurement reveals what complex analysis obscures.

****Signature-Level Protection (Wallet UX)****

Every signature should require explicit disclosure + passkey/biometric:

```

![:locked_with_key:](https://ethereum-magicians.org/images/emoji/twitter/locked_with_key.png?v=15) High Trust Counter - Signature Required

This action will:

→ Send 100,000 LINEA from your wallet

→ To: 0x9b1b…

→ Estimated value: $4,200

[Biometric/Passkey to Confirm]

```

For EIP-7702 delegations specifically:

```

![:warning:](https://ethereum-magicians.org/images/emoji/twitter/warning.png?v=15) DANGER: WALLET DELEGATION

This signature grants contract 0x3Ae1…2D10

FULL CONTROL of your wallet on ALL EVM CHAINS

This is NOT a normal transaction.

Tokens at risk: ALL CURRENT + FUTURE DEPOSITS

[Cancel] [I understand the risks - Passkey to Confirm]

```

****Why this matters:**** I lost 100K LINEA to a 7702 phishing attack. The wallet showed a generic “Sign message?” prompt. No simulation, no warning, no passkey gate. This should be a solved problem.

****Behavioral Metrics via Simple Counting****

MTC could anchor behavioral credentials derived from on-chain activity:

| Metric | Calculation | Use Case |

|--------|-------------|----------|

| `cancelRatio` | orders_cancelled / orders_placed | If > 1%, likely maker wallet (MM behavior) |

| `fillRate` | orders_filled / orders_placed | Execution quality signal |

| `toxicityScore` | adverse_selection_rate | VPIN-style flow toxicity |

| `settlementRate` | settled_on_time / total_settlements | Counterparty reliability |

| `walletAge` | blocks_since_first_tx | Sybil resistance |

| `delegationCount` | active_7702_delegations | Risk flag if > 0 unexpectedly |

****Behavioral Profiles from Simple Counting:****

| Profile | Signal | Credential Use |

|---------|--------|----------------|

| ****Maker**** | `cancelRatio > 1%` | MM program access, fee tiers |

| ****Community Participant**** | holds N+ ecosystem tokens over T+ days | Governance weight, airdrop eligibility |

| ****Drainer (Compromise)**** | batch-sweeps N+ tokens (including dust) in tight window | Flag for review, freeze credentials |

****The key insight:****

The **same tokens** produce completely different behavioral signatures based on **pattern of interaction**:

- ****Accumulation over time**** (RUSTY, BOL, ZERO, REX held for months) = community participant ✓

- ****Batch sweep in single tx**** (same tokens drained including dust) = compromise signature ✓

Diverse ecosystem token holdings accumulated gradually = ****trust signal****

Diverse ecosystem tokens swept in batch = ****compromise signal****

****Drainer Detection Metrics:****

| Signal | Pattern |

|--------|---------|

| `sweepBreadth` | # of unique tokens moved in <1 hour |

| `dustInclusion` | moved tokens worth < $X threshold |

| `batchTiming` | multiple token types in single tx or tight window |

| `outflowDirection` | one-way (out only) vs bidirectional |

This enables MTC to not just credential good behavior, but also detect and flag compromises - protecting the ecosystem while preserving privacy for legitimate users.

These are all “counting” operations - no complex ML, no oracles, just on-chain event tallies anchored to MTC credentials with ZK predicates.

****Proposed Extension:****

An ERC for “Signature Impact Disclosure” that:

- MUST simulate and display token outflows before signature

- MUST decode 7702/permit2/approval signatures in human terms

- MUST require passkey/biometric for signatures above configurable threshold

- SHOULD integrate with MTC for behavioral credential generation

Would love to see reference implementations targeting DEX integrations. Happy to contribute use cases from the MM perspective.

-–

**certifiedcryp**

HighTrustCrypto

Liquid Appreciation

Nominal Gold

AnnexVZ

-–

---

**y_hoshino** (2026-01-15):

Really interesting ideas. Thank you for sharing such a detailed set of use cases and the trust migration framing.

I agree migration/transfer of credentials could be important (especially for compromised/lost-key scenarios), but the identity/ownership proof and recovery policy need careful design (e.g., old-key signature vs. theft, challenge periods, issuer re-verification, vouching/slashing).

I’d like to think this through and come back with a concrete proposal (probably as an optional extension / best-practice section). If you have thoughts on minimal safe requirements for migration, I’d love to hear them.

---

**CertifiedCryp** (2026-01-18):

Keystroke id - similar to a fingerprint the people have unique keystroke characteristics. Misspellings typos etc .  It would have to be more than 1 sentence sure

---

**y_hoshino** (2026-01-23):

Thanks!

For the ERC itself, I’m cautious about standardizing keystroke-ID since it’s highly device/language dependent and would likely require off-chain measurement plus a trusted issuer/oracle. That said, it could fit well as an issuer-side verification method (best practice) or as an optional predicate in a higher-level profile.

Also worth exploring: community/DAO-based recovery, or leveraging third-party proof-of-personhood/biometric credentials (e.g., World ID) depending on the ecosystem — though those come with their own trust/compliance tradeoffs.

---

**y_hoshino** (2026-02-04):

I’ve been thinking about recovery for MultiTrustCredential (MTC) and wanted to share a quick breakdown and get feedback from others.

### Possible recovery approaches

1. Account-level recovery (Smart Accounts / AA)
Recovery is handled entirely at the account layer (e.g. social recovery, guardian-based key rotation). From the MTC perspective, the subject address remains stable, so no special logic is required in the credential standard itself.
2. Issuer / Governance-mediated rebinding
A DAO or issuer-governed process allows rebinding a credential to a new address after off-chain verification (identity checks, dispute windows, etc.). This is powerful but introduces governance and policy complexity, and can vary significantly by deployment.
3. Hybrid / profile-based approaches
Combining AA-based recovery with an optional governance-controlled rebind flow, documented as a reference or profile rather than a core standard requirement.

### Tentative conclusion

My current thinking is that recovery should probably not be part of the core ERC (8035 / 8036).Including it in the standard risks over-constraining implementations and mixing account-layer concerns with credential semantics.

Instead, recovery could be:

- handled at the account layer (AA),
- defined as an operational / governance process, or
- documented as a separate profile or informational extension, rather than baked into the ERC itself.

Curious how others think about this:

- Do you see a strong case for standardizing recovery at the ERC level?
- Or does it make more sense to keep it out-of-scope and handle it via AA and governance patterns?

