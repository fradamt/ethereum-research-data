---
source: magicians
topic_id: 27658
title: "Hegota Headliner: LUCID encrypted mempool"
author: jflo
date: "2026-02-05"
category: Magicians > Primordial Soup
tags: [hegota, headliner-proposal]
url: https://ethereum-magicians.org/t/hegota-headliner-lucid-encrypted-mempool/27658
views: 86
likes: 4
posts_count: 1
---

# Hegota Headliner: LUCID encrypted mempool

# Hegota Headliner: LUCID encrypted mempool

Authors: Anders Elowsson [@aelowsson](/u/aelowsson) , Julian Ma, Justin Florentine [@jflo](/u/jflo)

## Motivation

FOCIL promotes censorship resistance (CR) by letting includers propagate inclusion lists (ILs) of transactions that must be included in the next slot. However, FOCIL can unfortunately not facilitate CR for transactions subject to MEV extraction, since these transactions could be front-run if propagated openly. Allowing ILs to provide CR for MEV inducing transactions would significantly widen the protection from censorship provided by FOCIL.

Transaction ordering power among builders has led to the industrialization of toxic MEV, specifically front-running and sandwich attacks, where sophisticated actors exploit public knowledge of pending trades. This imposes immediate financial losses on honest users, degrading the user experience and effectively taxing network participation.

Users have resorted to protecting themselves from MEV extraction by trusting third parties with their plaintext transactions. As trust grows, so does centralization. Trusted entities grow more and more powerful, the mempool starves, and Ethereum moves further from its ideals. It is in this context vital to provide a trustless path to inclusion for transactions sensitive to MEV.

## Proposal

We propose pursuing a [minimum viable EIP](https://ethresear.ch/t/lucid-encrypted-mempool-with-distributed-payload-propagation/24042#p-58297-minimum-viable-eip-37) of the [LUCID](https://ethresear.ch/t/lucid-encrypted-mempool-with-distributed-payload-propagation/24042) encrypted mempool. LUCID is general purpose and can be used for, e.g., trustless self-decryption by the sender, decryption by a trusted party, or in threshold designs. The core mechanism is as follows:

1. Slot N (Commitment Phase):

Sealed Transactions (STs): Users broadcast STs consisting of an ST ticket for payment handling and the encrypted transaction bytes. The detailed encryption scheme can be decided by the decrypting party.
2. Inclusion Lists: FOCIL committee members (includers) pick up these STs and propagate them in their ILs.
3. Builder Commitment: The builder for Slot N includes commitments to these STs in their auditable builder bid (ABB).
4. Unconditional Inclusion Lists (UIL). Each includer is allotted a fixed gas limit and the builder must include ST-commitments from timely ILs up to this limit.
5. Slot N (Key Release):

Upon observing the ABB in the beacon block for Slot N, decryptors (entities designated in the ST ticket) broadcast the decryption keys.
6. This happens after the order is fixed but before execution starts.
7. Slot N (Payment): The ST ticket goes into the payload for Slot N and the sender is charged the full gas limit of the encrypted transaction.
8. Slot N+1 (Execution Phase):

Top-of-Block (ToB): The builder for Slot N+1 takes the revealed keys and executes the now-decrypted transactions at the top of the block. Since the plaintext is available before Slot N+1 commences, the BAL can be constructed as required.
9. Ordering: Decrypted transactions are strictly ordered by their ToB_fee (set by the user and revealed upon decryption).
10. MEV protection: The sender is protected from MEV extraction because the commitment allows the transaction to execute ToB, and the from field can remain hidden until decryption.

---

### Problem Statement

The current Ethereum landscape forces users to choose between **safety** and **decentralization**.

- Toxic MEV: To avoid frontrunning and sandwich attacks, users currently rely on private RPCs to access private mempools. This bypasses and starves the public mempool, centralizing order flow into the hands of a few dominant builders and eroding the protocol’s censorship resistance.
- The FOCIL Gap: While FOCIL empowers validators to force-include transactions, those transactions are visible to the builder. If a transaction is visible, a sophisticated builder can sandwich it.

The goal is to create a **trustless inclusion path** where:

1. Builders cannot see content until the transaction’s position in the block is committed (preventing front-running).
2. Includers (Validators) can force inclusion regardless of the builder’s preference (preventing censorship).

---

### Trade-Off Analysis

#### 1. Security & Trust Assumptions

- Trustless MEV Protection: Unlike private RPCs, LUCID does not require trusting a specific builder or decryptor. It relies on an honest majority of attesters to facilitate commitment, inclusion, and decryption.
- Decryption Liveness: If a decryptor fails to release a key, the transaction is skipped. While the user pays for the full envelope, the transaction does not execute and the transaction body does not enter the payload. Thus, the ST consumes very little resources and pays in full for resources it did not consume. This payment is burned.
- Subjective Timeliness: Relying on the PTC to vote on key availability introduces a subjective timing assumption. However, this is already a dependency for ePBS/FOCIL designs generally.

#### 2. Impact on Stakeholders

This proposal fundamentally realigns the transaction supply chain to prioritize censorship resistance and MEV protection.

- Users gain cryptographic immunity to front-running and sandwich attacks but must accept a slight increase in latency (execution in slot N+1) and a stricter “pay-for-envelope” fee model where they are charged for the declared gas limit regardless of actual usage.
- Builders see a loss in revenue, as their ability extract MEV falls.
- Validators (acting as includers) reclaim significant agency over the chain’s contents via unconditional inclusion of MEV-protected transactions, ensuring that valid transactions cannot be silenced by profit-maximizing builders.
- Client and Wallet developers must integrate encryption standards and handle the new commitment lifecycle.

---

### Why now?

- As of this writing one builder has grown to dominate 50% of the builder market.
 (mevboost.pics)
- The public mempool is currently starved; non-mev participating proposers routinely do not have enough transactions to propose blocks at target gas.
- Providing an optional encrypted mempool, where front-running protection becomes free, incentivizes wallets to send traffic there, which replenishes the public mempool.
- The lack of execution privacy and the certainty of value extraction likely deters traditional financial entities from deploying high-value settlement infrastructure on Ethereum, as they require markets with guaranteed integrity and protection against predatory extraction.

An encrypted mempool reduces incentives to use private order flow.

---

### Relation to Existing Work

- EIP-7732 (ePBS): LUCID is built directly on the ePBS foundation, adding to the SignedExecutionPayloadHeader to form the ABB, to commit to transactions.
- EIP-7805 (FOCIL): LUCID acts as a “FOCIL++”. It uses the FOCIL committee structure but upgrades the content to be encrypted and mandates unconditional inclusion for STs.

---

### Call for Feedback

We invite protocol researchers, client developers, and rollup teams to critique this “Minimum Viable LUCID” approach, as we are currently in the drafting process of an EIP.

- Client Teams: Can this be implemented alongside FOCIL?
- Builders: Does the N+1 execution model sufficiently preserve back-running incentives?

Please reply with alternative designs, potential attack vectors on the UIL mechanism, or considerations regarding the encryption usage.
