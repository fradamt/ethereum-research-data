---
source: ethresearch
topic_id: 23567
title: "DeDe Protocol: A Trustless Settlement Layer for Physical Delivery"
author: pablo-chacon
date: "2025-11-29"
category: Applications
tags: [zk-roll-up, p2p, public-good, dao]
url: https://ethresear.ch/t/dede-protocol-a-trustless-settlement-layer-for-physical-delivery/23567
views: 194
likes: 1
posts_count: 3
---

# DeDe Protocol: A Trustless Settlement Layer for Physical Delivery

**TL;DR**

DeDe is a minimal Ethereum-based protocol for decentralized physical delivery.

It handles settlement, not logistics: **No fleet, no terminal, no app, no routing, no identity.**

Just trustless escrow, deterministic parcel lifecycle, and immutable protocol fees.

---

## Motivation

We have decentralized infrastructure for:

- Money (Bitcoin)
- Communication (Matrix)
- Compute (Ethereum)
- Privacy (Tor)

But physical delivery still a key part of human coordination remains centralized, fragile, and opaque.

Postal systems are slow, expensive, often fail to deliver, and structurally incompatible with privacy.

Meanwhile, enormous underutilized capacity exists in everyday human movement:

people walk, bike, drive, and commute along routes that could carry parcels.

**DeDe lets anyone tap into that movement.**

It enables real-world delivery as a **trustless, peer-to-peer settlement flow**, not a logistics monopoly.

---

## What It Is

DeDe is **not** an app, not a marketplace, and not a company.

It is a small Ethereum smart contract protocol that allows:

- Senders to register a parcel NFT + escrow
- Carriers to voluntarily pick it up
- Delivery to be confirmed (opt-in)
- Settlement to be finalized without trusted intermediaries

The protocol governs:

- Who gets paid
- Under what conditions
- How funds are held and released
- Immutable protocol fee routing
- Minimal incentive alignment

All logistics, routing, and app-specific behavior happens off-chain.

---

## Architecture

**Core contracts:**

### 1. ParcelCore

- ERC-721 parcels with deterministic lifecycle states
- Immutable protocol fee (e.g. 0.5%)
- Support for platform-level BPS fee schedules
- Finalization window (e.g. 72h after pickup)

### 2. Escrow

- Holds ETH/ERC-20 funds keyed by parcelId
- Releases funds to carrier, protocol treasury, platform treasury, and finalizer tip
- Enforces deterministic payout logic

### 3. AStarSignerRegistryStaked

- (Optional) registers routing signers with stake
- Ties dropoff event to a verifiable off-chain route hash
- Allows eventual zkRoute integrations

All state transitions are **public and auditable**.

DeDe does not include any GPS, KYC, login systems, or metadata on-chain.

---

## On-chain Privacy Model

- On-chain: only tokenId, state enum, and lifecycle timestamps
- Off-chain: pickup/dropoff locations, photo proofs, routing paths
- Metadata is stored in NFT, encrypted, or referenced via IPFS hashes
- Ethereum only sees a hash

---

## What Makes DeDe Unique

- It’s a protocol, not a platform
- No centralized operator, job board, or trusted intermediary
- Anyone can build an app, mint a parcel, or pick one up
- Payments settle only if both sides confirm (or finalize automatically)
- Protocol fee is immutable, finalizer tip is capped, all logic is deterministic

No pricing engine.

No identity layer.

No assignment logic.

Just **neutral rails**.

---

## Use Cases

- P2P delivery during commutes (side income for regular people)
- Local business delivery without contracts or apps
- Decentralized logistics experiments (DAOs, disaster relief, rural mobility)
- Trust-minimized gig networks in low-trust regions

---

## Economics

- Protocol fee: immutable (e.g. 0.5%)
- Platform fee: configurable, set by each integrator
- Finalizer tip: small % (e.g. 0.05%), capped
- DeDe does not reduce escrow value over time (no built-in decay)
- Settlement is voluntary; payment is conditional on mutual confirmation

---

## Why Ethereum?

DeDe works best when:

- The settlement layer is public, neutral, auditable
- Applications are permissionless and forkable
- The infrastructure isn’t subject to any central actor’s control

---

## Deployed to Ethereum Mainnet

- ParcelCore: 0xeF1D4970c3B988840B13761Ec4FBb85106d789F8
- Escrow: 0x834317eFB2E6eE362a63474837398086cC302934
- AStarSignerRegistryStaked: 0x311A4c3Ed79D4467C55dd7CEE0C731501DF3f161
- protocolTreasury: 0x9C34d6a6BF1257A9e36758583cDC36F4cE2fA78F

---

## Related Work / Inspiration

- Matrix (as infra for decentralized messaging)
- Monero (for privacy guarantees in adversarial environments)
- Tor / IPFS / Nostr (for neutrality under pressure)
- Ethereum itself (as settlement infrastructure)

---

## Future Directions

- zkDeliveryProofs (optional: SNARKs for delivery receipt)
- L2 deployment for micropayments
- Local delivery DAO coordination
- Indexers / GraphQL APIs / “DeDeScan” explorer
- Mobile UX kits and white-label apps
- Monero bridge / atomic swaps for cross-chain delivery privacy

---

## Source

**MIT Licensed**



      [github.com](https://github.com/pablo-chacon/dede-protocol)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/c/f/cf6fd97854528f8bc8c5c0384ba75dcd34f34203_2_690x344.png)



###



DeDe Protocol, Neutral, Trustless Settlement Rails for P2P Crowdshipping

## Replies

**Citrullin** (2026-01-03):

What about insurance in case the parcel blows up in my face when I pick it up?

How does the insurance get distributed. Or what about legal liability support in case it’s drugs or something similar? I am not a registered parcel delivery service.

Can I only pick people who have a long track record or delivering? Or is that rather scope of a platform on top of it?

---

**pablo-chacon** (2026-01-04):

These are all valid concerns, but they live at the platform or application layer, not the protocol layer.

DeDe does not attempt to solve insurance, liability, dangerous goods, or trust scoring, because those require jurisdiction-specific contracts, underwriting, and off-chain enforcement.

A platform built on top of DeDe can:

- restrict who can carry parcels
- require identity or track records
- bundle insurance
- exclude certain parcel types
- provide legal support

DeDe itself only enforces escrow and settlement.

To keep DeDe-Protocol, neutral everything else is intentionally out of scope.

The dede-templates repository shows how platforms might implement these concerns on top.



      [github.com](https://github.com/pablo-chacon/dede-templates)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/0/1/0144582200c0477f9256ba72ef9c00690e675670_2_690x344.png)



###



Quick start templates to build on-top of DeDe-Protocol

