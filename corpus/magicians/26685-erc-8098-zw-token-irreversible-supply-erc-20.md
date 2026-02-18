---
source: magicians
topic_id: 26685
title: "ERC-8098: ZW-Token — Irreversible-Supply ERC-20"
author: ten-io-meta
date: "2025-11-23"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8098-zw-token-irreversible-supply-erc-20/26685
views: 140
likes: 1
posts_count: 6
---

# ERC-8098: ZW-Token — Irreversible-Supply ERC-20

Opening Note

This thread introduces a proposal for an irreversible-supply fungible token primitive (ZW-Token).

Before posting the full EIP, I want to provide context, motivation, and the implementation experience that led to this design.

Implementation Context

Before drafting this EIP, I deployed a live mainnet experiment ([TEN.IO](http://TEN.IO) – Fragment 0, “EL UMBRAL”) implementing irreversible-supply semantics in practice.

The system currently shows:

• 11 existing units,

• 3 units irreversibly destroyed,

• 0 wrapped or synthetic representations,

• all value accounted for in a single ERC-721 state,

• no re-entry path for burned supply, and

• no private, mirrored or alternate supply states.

This experiment demonstrates that:

• irreversible supply is viable on Ethereum without requiring wrappers,

• supply can remain strictly single-state even with mint–burn dynamics, and

• privacy or transformation layers do not require alternate value representations.

The ZW-Token ERC generalizes these semantics for fungible assets, defining a formal standard for strictly non-increasing supply, single-state value representation, and privacy without supply fragmentation.

Transition Note

The implementation above demonstrated that irreversible supply and single-state value representation are feasible on Ethereum today.

The following message contains the full EIP draft for feedback.

I welcome comments, constraints, counterexamples and alternative formulations of the supply invariants.

## Replies

**ten-io-meta** (2025-11-23):

eip: XXXX

title: ZW-Token — Single-State Irreversible-Supply ERC-20 With Non-Representational Privacy

description: A fungible token whose total supply is strictly non-increasing and whose optional privacy layer operates only as a transfer-obfuscation mechanism, never as a value container. This ERC enforces irreversible supply semantics, single-state supply, and privacy without alternate value representations.

author: TEN (@ten_io_meta; tenio.eth)

status: Draft

type: Standards Track

category: ERC

created: 2025-XX-XX

requires: ERC-20

---

## 1. Abstract

This EIP defines the ZW-Token primitive:

a fungible token that preserves full ERC-20 compatibility while enforcing:

- strictly non-increasing total supply,
- a single global supply state, and
- privacy-as-transformation rather than privacy-as-representation.

A ZW-Token MAY integrate unlinkable transfers, but MUST NOT introduce private balances, wrapped supply, mirrored supply, shielded value, or any representation of value outside the public ERC-20 state.

This fills a structural gap in Ethereum:

no existing ERC standardizes irreversible supply or privacy without supply fragmentation.

---

## 2. Motivation

ERC-20 defines flexible fungible assets.

ERC-721 defines non-fungible uniqueness.

This proposal introduces a missing third axis:

**fungible assets with irreversible supply semantics and a single supply state.**

Existing tokens enable wrapping, reversible privacy, and synthetic representation.

All known designs allow supply to re-enter circulation through:

- unwrap paths
- remint paths
- private-balance exits
- dual-mode switching
- synthetic recreation through bridges or vaults

Because ERC-20 does not define supply semantics, irreversible burn cannot be enforced at the standard level.

This EIP defines a primitive with:

- irreversible supply,
- no alternate supply representations, and
- privacy layers that never store value.

---

## 3. Problem Statement

Current privacy or wrapping models fall into three categories.

### 3.1 Wrapper-based privacy

**ERC-20 → Wrapped Private Token → ERC-20**

- mirrored supply
- reversible by design
- unwrapping reconstructs supply
- liquidity split across states

### 3.2 Dual-mode tokens

**Public ↔ Private**

- two supply states
- balances exist in parallel ledgers
- privacy requires alternate representation

### 3.3 Native privacy tokens (commitment-based)

- commitments represent value
- private trees hold supply
- exits re-mint value on the public side

### 3.4 Shared limitation

All existing models allow supply to re-enter circulation.

Ethereum lacks a fungible standard that enforces:

- irreversible supply
- a single-state supply model
- privacy without value containment
- no remint, unwrap, or synthetic re-entry paths

---

## 4. Definitions

**Supply Integrity**

The guarantee that all value exists solely in the public ERC-20 storage, with no wrapped, mirrored, private, synthetic, or off-chain representations.

**Single-State Supply**

A model in which totalSupply is the only supply definition in existence.

**Supply Fragmentation**

Any system where value exists in more than one representation (wrapped, private, mirrored, shielded, synthetic).

**Unlinkable Transfer**

A transfer in which sender and/or receiver are obfuscated without storing balances privately.

**Irreversible Burn**

A burn operation for which no mechanism—direct or indirect—can reconstruct the burned units.

---

## 5. ZW-Token Primitive (Definition)

A ZW-Token is an ERC-20 whose:

1. totalSupply is strictly non-increasing,
2. all value exists exclusively in the public ERC-20 state, and
3. any privacy subsystem acts only as a transformation layer, never representing or storing supply.

The primitive is defined by three invariants.

---

## 6. Core Invariants

### Invariant 1 — Strictly Non-Increasing Supply

```auto
totalSupply(n+1) ≤ totalSupply(n)
```

A ZW-Token MUST prohibit:

- mint
- remint
- unwrap
- synthetic recreation via bridges or vaults
- mirrored supply creation

Burn is final and irreversible.

---

### Invariant 2 — Single-State Supply

```auto
totalSupply = initialSupply − Σ(burns)
```

A ZW-Token MUST NOT introduce:

- private supply
- wrapped supply
- shielded supply
- commitments representing value
- dual supply counters

All value MUST exist in the public ERC-20 state.

---

### Invariant 3 — Privacy Without Value Representation

A privacy subsystem MAY hide:

- sender
- receiver
- transfer graph topology

But MUST NOT:

- contain balances privately
- represent value inside commitments
- maintain parallel ledgers
- wrap supply inside a privacy pool

**Privacy = transformation, not representation.**

---

## 7. What This Produces

ZW-Token creates a fungible asset with:

- irreversible supply
- deterministic burn semantics
- zero remint or unwrap paths
- single-state supply
- ERC-20 compatibility
- privacy without supply fragmentation

---

## 8. Non-Goals

###  Not a wrapper

- no underlying token
- no mirrored supply
- no reversible transitions

###  Not a dual-mode token

- no private balances
- no mode switching

###  Not a synthetic or derivative representation

- no re-entry from bridges
- burned supply is unrecoverable

###  Not a privacy token standard

- no commitments representing supply
- no ZK circuit specification

---

## 9. Relationship to Existing Standards

### ERC-20

Compatible except:

- mint() MUST NOT exist
- totalSupply MUST NOT increase

ERC-20 does not define supply semantics; ZW-Token does.

### IZRC20

Compatible only as a transfer-obfuscation layer.

A ZW-Token privacy subsystem MUST NOT store value.

### ERC-8060 / 6909 / 6551

Orthogonal.

ZW-Token defines supply semantics, not embedding or wrapping.

---

## 10. Supply Representation Models (Conceptual)

```auto
WRAPPER:
ERC-20  Wrapped Token
(two supply states; reversible)

DUAL-MODE:
Public  Private
(two representations; mode switching)

COMMITMENT-BASED:
Public + Private Tree
(private tree holds value)

ZW-TOKEN:
Public Only
(single supply state; irreversible)
```

---

## 11. Specification

A ZW-Token MUST:

- implement the ERC-20 interface
- expose standard Transfer events
- enforce strictly non-increasing totalSupply
- record burn as Transfer(from, 0x00..., amount)
- prohibit any supply-increasing function
- ensure privacy components do not represent value

A ZW-Token MUST NOT:

- maintain private balances
- store value inside commitments
- introduce wrapped, mirrored, or synthetic supply
- depend on bridges or vaults that recreate supply
- allow re-entry of burned units

A ZW-Token MAY:

- integrate unlinkable transfers
- emit additional burn-finality events
- use immutability or governance-locked upgrade paths

---

## 12. Rationale

ERC-20 does not define supply invariants.

It allows mint, remint, unwrapping, synthetic reconstruction, and bridges that create derivative supply.

Wrapper-based, dual-mode, and commitment-based designs introduce alternate supply states, making irreversible supply impossible at the ERC level.

This EIP introduces:

- a supply-irreversible ERC-20 primitive
- a strict separation between privacy and value
- single-state supply semantics
- deterministic burn

Alternative designs considered:

- capped supply → still reversible
- dual-mode privacy → two supply states
- shielded pools → private trees hold value
- wrapper privacy → mirrored supply

None meet the invariants defined here.

---

## 13. Threat Model

A ZW-Token MUST defend against:

### 13.1 Accidental Remint

via vaults, wrappers, LST/LRT systems.

### 13.2 Privacy layers that store value

via commitments-as-value, shielded pools, or balance-bearing circuits.

### 13.3 Proxy upgrades that reintroduce mint paths

Implementations SHOULD use immutability or governance-locked code.

### 13.4 Synthetic supply expansion

via bridges issuing derivative tokens.

---

## 14. Tooling & Compatibility Notes

- Explorers track totalSupply normally.
- Wallets MAY warn users about irreversible burns.
- Indexers require no special logic.
- Privacy scanners MAY track obfuscated transfers, not balances.

---

## 15. Open Questions

- Should minimal privacy constraints be standardized?
- Are bridge constraints necessary to prevent synthetic remint?
- Should irreversible-supply ERCs form a new ERC class?
- Is “single-state supply” the optimal terminology?

---

## 16. Reference Implementation

A minimal reference implementation enforcing all invariants will be provided in a public repository.

---

## 17. Copyright

This EIP is licensed under CC0 1.0 Universal.

---

**ten-io-meta** (2025-11-23):

Additional Notes

A live reference implementation is available at https://tenio.eth.limo (ENS gateway).

The implementation fully satisfies all invariants specified in this proposal and demonstrates that irreversible-supply semantics are enforceable today in production environments.

While this deployment is not presented as the final accepted form of the ERC, it serves as a concrete, running proof of the proposal’s correctness and feasibility.

---

**ten-io-meta** (2025-12-01):

**Update — GitHub Pull Request**

I have opened the formal Pull Request for this EIP in the Ethereum/EIPs repository.

Here is the link to the PR (now passing validation):

![:point_right:](https://ethereum-magicians.org/images/emoji/twitter/point_right.png?v=12) **[Add EIP: ZW-Token — Irreversible ERC-20 by ten-io-meta · Pull Request #10858 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/10858)**

The draft posted here in Ethereum Magicians and the PR in GitHub are fully synchronized.

Any feedback, constraints, or alternative formulations of the invariants are welcome —

I will update both the PR and this thread accordingly.

Thanks again for your time and review. I’ll keep following the process step by step.

---

**ten-io-meta** (2025-12-02):

**Update — New GitHub Pull Request**

The previous PR was closed during the transition from EIP → ERC, and the correct Pull Request is now open in the ERCs repository.

Here is the active PR (all checks passing):

![:point_right:](https://ethereum-magicians.org/images/emoji/twitter/point_right.png?v=12) [Add ERC-9999: ZW-Token — Irreversible ERC-20 by ten-io-meta · Pull Request #1390 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1390)

This thread and the new ERC PR are now fully synchronized.

Any feedback or constraints can be provided here in Magicians or directly on GitHub — I will update both accordingly.

Thank you again for your time and review.

---

**ten-io-meta** (2025-12-30):

**Additional Notes**

A live reference implementation is available at **https://tenio.eth.limo** (ENS gateway).

The implementation fully satisfies all invariants specified in this proposal and demonstrates that irreversible-supply semantics are enforceable today in production environments.

While this deployment is not presented as the final accepted form of the ERC, it serves as a concrete, running proof of the proposal’s correctness and feasibility.

