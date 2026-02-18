---
source: ethresearch
topic_id: 22955
title: Parallel Auctions on Commit-Boost
author: wooju
date: "2025-08-22"
category: Architecture
tags: [mev]
url: https://ethresear.ch/t/parallel-auctions-on-commit-boost/22955
views: 359
likes: 5
posts_count: 3
---

# Parallel Auctions on Commit-Boost

*This article is authored by Chanyang Ju([wooju](https://x.com/woojucy)), Researcher at [Radius](https://twitter.com/radius_xyz). Thanks to [Hugo](https://x.com/meveloper) for his contribution to the PoC and [AJ](https://twitter.com/ZeroKnight_eth) for reviewing this post.*

# 1. Abstract

---

This article introduces **State Lock Commitment**, a new blockspace commitment mechanism for Proposer-Builder Separation (PBS). Current inclusion-based commitments fail to guarantee execution consistency, leading searchers to adopt risk-averse strategies that reduce market efficiency. We propose a dual-component approach that goes beyond simple inclusion promises. First, an **Exclusion Commitment** is issued: a builder-agnostic, upfront reservation that guarantees a specific state will not be altered by conflicting transactions. This is followed by a standard **Inclusion Commitment** (preconfirmation) for the bundle that wins the subsequent auction. Together, these commitments provide strong guarantees equivalent to **Execution Commitment**, allowing searchers to bid with greater confidence. The architecture includes a **Gateway** (for proposers) and a **LockEngine** (for builders), enabling proposers to auction exclusive state rights, prevent conflicts, increase revenue, and foster a more robust and efficient MEV market.

## 1.1 Background

Proposer-Builder Separation (PBS) treats blockspace as a tradable asset, enabling proposers to auction off the right to build a block. This allows partial delegation of block building through commitments sold to external participants, such as builders and searchers. Currently, most of these commitments are inclusion-based (like inclusion lists and preconfirmations), though the market continues to evolve.

However, there is no widely adopted system that guarantees a bundle will execute in its intended state, due to technical and economic limitations. As a result:

- Even if a preconfirmed bundle is included in a block, its intended execution can change, or the transaction may fail if the state is altered beforehand.
- Since inclusion guarantees alone are insufficient for consistent execution, searchers must hedge their risks, discouraging aggressive bidding.
- Frequent included-but-failed executions undermine trust in commitments and reduce market efficiency, eventually decreasing proposer revenue.

To progress, blockspace commitments must evolve beyond simple inclusion promises and move toward execution-level guarantees that ensure state consistency.

## 1.2 Solution: State Lock Commitment

To address the limitations, we introduce **State Lock Commitment**: a mechanism where the proposer explicitly promises exclusive execution rights over the state that a bundle accesses. This commitment goes beyond simple inclusion by ensuring a defined scope of state within the block remains unaltered, enabling stable bundle execution.

Rather than imposing a global state lock, our approach applies a **Local State Lock** on a per-bundle basis. This avoids global synchronization or mempool-wide control, and instead constrains only potentially conflicting state scopes. A critical aspect of the architecture is that the proposer must consistently communicate exclusive execution rights for a specific EVM state to all builders. In other words, even as different builders construct different candidate blocks, this constraint must function as a common access restriction rule across all options being considered.

State Lock Commitment operates in two stages, acting as a partial constraint on builders:

1. Exclusion Commitment: The proposer declares a specific stateScope as a lock candidate and broadcasts this to all builders, instructing them not to include conflicting transactions.
2. Inclusion Commitment: Once the auction for the stateScope concludes,  preconfirms the bundle that wins inclusion in the final block.

Using these two commitments in tandem significantly increases the likelihood of consistent bundle execution and conflict avoidance. Under certain conditions, this can provide a strong level of execution guarantee (execution commitment). When the Exclusion Commitment is propagated to and consistently enforced by all builders, the searcher gains a competitive advantage under the assumption that “no one will touch my designated state,” even without an inclusion guarantee that “my bundle will be at the top of the block.”

Therefore, an inclusion promise based on a state-level constraint (exclusion) can be seen as part of a continuous spectrum of execution commitments. As a builder-agnostic constraint, this mechanism could reshape both block-building dynamics and future MEV market incentives and competition.

### 1.2.1 Overview

**Components & Responsibilities**

| Component | Responsibility |
| --- | --- |
| Proposer | Proposes blocks, declares state locks, requests commitment generation. |
| Gateway | Coordinates bundle auctions, manages commitment requests. |
| Builder | Constructs blocks. |
| Searcher | Composes bundles, participates in auctions. |

**Procedural Flow**

1. Submission & Auction: A searcher submits a bundle to the Gateway.
2. Coordination & Auction Start: The Gateway simulates the bundle to automatically extract its stateScope (e.g., access list) and initiates an auction for this specific stateScope.
3. Exclusion: While the auction is ongoing, the proposer (via the Gateway) announces the stateScope as a lock candidate. This acts as an initial Exclusion Commitment and is broadcast to all participating builders.
4. Bidding & Preconfirmation: Builders, aware of the constraint, provisionally construct blocks avoiding conflicting transactions. Once the auction concludes, a preconfirmation request for the winning bundle is sent to the builders.
5. Enforcement & Building: The builder verifies the signed commitment and ensures the final block adheres to the stateScope constraint by including the preconfirmed bundle. Subsequently, the builder can release the exclusion and proceed with block building.

### 1.2.2 Architectural Significance

This architecture offers distinct advantages over existing models like inclusion lists (e.g., EIP-7547) and enables a more granular and flexible blockspace market. Specifically, the Exclusion Commitment provides searchers with an upfront guarantee of their bundle’s executability and gives builders clear criteria for conflict avoidance, allowing it to function as a de facto execution-level commitment.

Under this model, a proposer can declare multiple, non-conflicting Exclusion Commitments in parallel, assigning a unique `LockId` to each respective `stateScope`. Each lock is associated with a separate bundle, and for any identical or overlapping state scopes, only one winner is selected and issued a single preconfirmation.

This structure yields the following benefits:

- State-Centric, Not Transaction-Centric: By focusing on state scopes rather than entire transaction lists, the proposer grants builders more flexibility. Builders only need to avoid a smaller, clearly defined state region, leaving them free to optimize the remainder of the block.
- Parallel, Non-Conflicting Auctions: Proposers can run multiple auctions simultaneously for non-overlapping state scopes. This allows for the inclusion of several independent MEV strategies within a single block, maximizing its value.
- Improved Incentives for All Participants:

Searchers: Gain execution certainty faster than block time, allowing them to bid more aggressively and confidently deploy capital-intensive strategies.
- Proposers: Create new revenue streams by auctioning exclusive state access and maximize block rewards by safely including multiple high-value bundles.
- Builders: Receive clear, early constraints, enabling them to optimize block construction without waiting for a full transaction list. This enhances their strategic flexibility and efficiency compared to scenarios with global constraints.

Essentially, State Lock Commitments can transform the blockspace market from one of simple inclusion guarantees to a sophisticated futures market for Ethereum state. It provides the assurances necessary for a more stable, efficient, and profitable MEV ecosystem.

## 1.3 Infrastructure Components: Gateway and LockEngine

To implement this state-constraint-based commitment structure within the PBS infrastructure, we propose an extension of the existing Commit-Boost functionality. Specifically, we expand the roles of the **Signer**, which handles the proposer’s commitment generation, and the **Gateway**, which mediates bundle coordination, to handle state-level commitments. Correspondingly, a new auxiliary module, the **LockEngine**, is introduced on the builder side. This design allows for the consistent processing of state-constraint-based preconfirmations without significant modifications to the existing PBS/MEV-Boost infrastructure.

### 1.3.1 Gateway

- Role: An off-chain relay infrastructure that forwards the proposer’s commitment requests, coordinates competition between bundles, and handles the collection and delivery of signatures through integration with the Signer.
- Functions:

Receives and manages bundles based on their stateScope.
- Manages conflicts between bundles competing for the same stateScope.
- Receives and coordinates bundles and bids from searchers participating in auctions.
- Relays the proposer’s commitment requests and signature requests to the Signer.
- Communicates commitment results to builders and searchers.

**Characteristics:**

- An off-chain intermediary that operates outside the core PBS protocol and does not directly interact with validators.
- Can be configured as a neutral relay infrastructure to support various strategies.

### 1.3.2 Signer

- Role: A protocol that generates signature-based commitments for the proposer’s exclusion/inclusion promises. It receives delegated signing authority from the proposer via a proxy key to handle signature creation. Its purpose is to enable trustless collaboration between proposers and builders and to enhance the safety and efficiency of MEV transactions.
- Functions:

Processes commitments on a stateScope basis.
- Coordinates BLS signatures (commit → reveal → aggregate procedure).
- Provides functionality to prevent duplicate commit/reveal actions for the same slot.
- Prevents duplicate commit/reveal actions for the same LockId.

**Characteristics:**

- Processes signatures for requests forwarded by the Gateway (proposer signature delegation model).
- Multiple Gateways can share the same Signer instance (neutrality).
- Installed as a sidecar next to the proposer node, capable of running in parallel with or integrated into MEV-Boost.

### 1.3.3 LockEngine (Builder Sidecar)

- Role: A sidecar module that assists the builder in complying with the stateScope constraints set by the proposer during block construction.
- Functions:

Verifies commitment signatures issued by the Signer.
- Detects conflicts for each stateScope and filters transactions accordingly.
- Proactively removes conflicting transactions from the builder’s mempool.
- Supports transaction reordering and bundle recombination.

**Characteristics:**

- Can be operated as a sidecar without modifying the builder’s core logic.
- Receives commitment and stateScope information from the proposer or Gateway.
- Ensures stateScope conflict avoidance at the pre-execution stage.

## 1.4 Definitions of Key Components

- Proposer

Proposes blocks on the Beacon Chain.
- Delegates signing authority to the Signer via a proxy key.
- Based on searcher bundles and their corresponding access lists (stateScope) received from the Gateway, declares locks on non-contested state scopes (i.e., requests Exclusion + Inclusion Commitments).
- Requests the Signer to sign the winning auction results.

**Gateway**

- Receives bundles from searchers and extracts their access lists (stateScope) via EVM simulation.
- Determines conflicts between bundles accessing the same state scope.
- Forwards all bundles and related metadata to the Relay.
- Communicates the winning bundle to the Proposer.
- Forwards the Proposer’s commitment signing requests to the Signer.
- Records and propagates all commitment requests and their processing results.

**Relay**

- Receives all bundles and bid information from the Gateway.
- Propagates information about selected bundles to the Gateway and Proposer.
- After block submission, verifies whether the builder actually fulfilled the Proposer Commitment (e.g., inclusion, state conflict avoidance, inclusion within the specified height).
- In case of non-compliance, it can collect slashing proofs and forward them to an AVS or a monitoring network.

**Signer**

- At the Proposer’s request, signs Exclusion/Inclusion Commitments in a verifiable way for builders.
- Processes signatures (e.g., using BLS) under the delegated authority of the proposer.

**Builder**

- Constructs blocks in compliance with the stateScopebased constraints received via the LockEngine.
- Must include the bundle specified in the preconfirmation and must not include (or must reorder) transactions that conflict with the stateScope.
- Faces penalties such as slashing or block rejection for violating these conditions.

**LockEngine**

- A sidecar module running alongside the builder node.
- Receives preconfirmation and state constraint information (stateScope, LockId, etc.) from the Gateway.
- Monitors the builder’s mempool to filter or reorder transactions that conflict with the stateScope.
- Assists in ensuring the preconfirmed bundle is included in the block.
- Allows the builder to adhere to proposer constraints without modifying its core logic.

**Searcher**

- Identifies MEV opportunities off-chain, constructs bundles, and submits them to the Gateway.
- Does not need to explicitly specify the stateScope for their bundle; the Gateway extracts it automatically.
- Competes with other searchers for the same state scope, with the winning bundle receiving the final preconfirmation.
- Can employ more aggressive bidding strategies for committed bundles due to the reduced risk of execution failure.

# 2. Key Features

---

## 2.1 Local State Lock (Exclusion Commitment)

Prior to issuing a preconfirmation, the proposer declares an exclusive access constraint on the state scope (`stateScope`) that a specific bundle accesses to guarantee its execution. This declaration functions as an **Exclusion Commitment**. It operates as a preemptive mechanism to prevent conflicts by having the proposer unilaterally notify the builder that the specified state is off-limits.

In this model, the State Lock is established without prior negotiation with the builder and is applied according to the following flow:

1. The Exclusion Commitment contains the following fields:

LockId
2. stateScope // A set of accounts based on the access list
3. inclusionHeight // Defines the state from the searcher’s perspective
4. signature
5. After analyzing the state scope of a given bundle, the proposer declares an exclusive access constraint for that scope. The stateScope is an address list of the states accessed by the transactions within the bundle.
6. This declaration is broadcast to all builders via the Gateway.
7. The LockEngine (on the builder’s side) receives this message and applies it as a local state access restriction.
8. While the LockId is active, the builder must not include any conflicting transactions in its block.

## 2.2 Preconfirmation (Inclusion Commitment)

A preconfirmation is a cryptographic promise from the proposer to include a specific bundle in a designated block. It functions as the **Inclusion Commitment** that finalizes the outcome of the blockspace auction. This commitment is made on the foundation of an Exclusion Commitment, meaning its executability has already been secured in advance.

### 2.2.1 Preconfirmation Generation Process

1. The proposer issues a preconfirmation for the winning bundle, which is then signed via the Signer and delivered to the builder.
2. The Inclusion Commitment contains the following fields:

LockId // Matches the one from the Exclusion Commitment
3. bundleTxs
4. inclusionHeight
5. signature

### 2.2.2 Roles and Effects

- Proposer: Responsible for including the bundle at the inclusionHeight specified in the Inclusion Commitment.
- Builder: Constructs the block based on the constraints from both the Exclusion and Inclusion Commitments.
- LockEngine: Enforces access control over the state scope according to the Exclusion Commitment.

Although the Exclusion Commitment (state conflict prevention) and the Inclusion Commitment (block inclusion promise) are distinct components, they provide the following effects when they work together:

- For Searchers: Guarantees that their submitted bundle will execute in a specific state and will not fail due to state conflicts.
- For Proposers: Provides a framework to combine non-conflicting bundles in parallel.
- For Builders: Offers the flexibility to build blocks ahead of time without waiting for the complete set of bundles.

## 2.3 Builder Constraint Handling

The builder receives two types of constraints from the proposer: a state access restriction for a `stateScope` (Exclusion Commitment) and an inclusion promise for a specific bundle (Inclusion Commitment, i.e., preconfirmation). These act as structural constraints that must be adhered to for the block to be considered a valid candidate by the proposer. This is not a mere recommendation but a mandatory condition. The commitments are delivered through the following path:

> Proposer → Gateway → Relay → Builder (via LockEngine sidecar)

The Relay ensures that Proposer Commitments are propagated consistently to all builders across the network, preventing any single builder from unilaterally ignoring or circumventing the constraints.

### 2.3.1 Proposer Commitment Constraints

The builder must construct its block according to the following two constraints:

1. StateScope Exclusion Constraint

The proposer creates a lock (commitment) that disallows state conflicts for a specific stateScope.
2. The Gateway receives this lock declaration and propagates it to the builder network via the Relay. Each lock is identified by a unique LockId.
3. The builder must handle any transaction accessing this scope in one of the following ways:

Do not include it (strict exclusion).
4. Order it after the confirmed bundle to ensure no state conflict occurs.
5. Preconfirmation Inclusion Constraint

The proposer cryptographically promises (preconfirms) that a specific bundle will be included at a designated block height (inclusionHeight).
6. The builder must include this bundle at the specified position. Failure to do so will render the block invalid from the proposer’s perspective.

These two conditions work in tandem. If either is violated, the proposer may refuse to accept the block or impose a penalty on the builder.

### 2.3.2 Constraint Enforcement & Verification

Relays and third-party verifiers (e.g., Gateways, AVSs) can independently verify if a builder’s block faithfully reflects the Proposer Commitments based on the following criteria. This verification assumes that the information in both the Exclusion and Inclusion Commitments is public and accompanied by the proposer’s cryptographic signature.

- Exclusion Commitment Verification

Commitment Information:

LockId
- stateScope
- inclusionHeight
- Proposer’s signature

**Verification Procedure:**

1. The Relay receives and stores the Exclusion Commitment issued by the proposer.
2. It simulates or statically analyzes the block candidate submitted by the builder to extract the set of states accessed by the transactions within it.
3. It checks if this extracted set of accessed states intersects with the committed stateScope.

Intersection found → Exclusion Violation.
4. No intersection → Exclusion Fulfilled.

**Violation Proof:**

- The Relay can generate a slashing proof by presenting the violating block alongside the corresponding Exclusion Commitment, demonstrating that “this block violated a stateScope explicitly locked by the proposer.”

**Inclusion Commitment Verification**

- Commitment Information:

LockId
- bundleTxs
- inclusionHeight
- Proposer’s signature

**Verification Procedure:**

1. The Relay checks the height of the block submitted by the builder against the inclusionHeight.
2. It verifies that the exact same bundle of transactions is included in the block.
3. It confirms that the inclusion order and execution position satisfy the conditions defined in the commitment (e.g., placed at the top, executed after the lock).

Not included or incorrect order → Inclusion Violation.
4. Correctly included → Inclusion Fulfilled.

**Violation Proof:**

- The Relay can generate an Inclusion Violation proof by presenting the submitted block header and transaction list as evidence that “the builder failed to include the promised bundle at the specified block height.”

**Accountability Mechanisms**

This verification process can be automated at the Relay level. In case of a violation, the following actions can be taken:

- Slashing (via Slashing Proof Submission):

The violation proof (Commitment + violating block’s transaction set) is submitted to an on-chain contract.
- The corresponding builder’s stake is burned or penalized.

**Reputation-Based Exclusion:**

- The Relay/Gateway network flags the violating builder as untrustworthy.
- The proposer subsequently denies block revenue opportunities to that builder.

Future extension paths, such as TEE attestations and ZK Proof-based verification, can also be considered.

| Verification Method | Description |
| --- | --- |
| TEE-based | Use remote attestation for blocks generated in a trusted execution environment (TEE) like SGX. |
| ZK-based | Generate a Zero-Knowledge Proof for the transaction order and execution path within the stateScope, to be verified by a Gateway/AVS. |

# 3. Parallel Auction on Commit-Boost

---

## 3.1 Sequence Diagram

[![Parallel_Auction_on_Commit-Boost](https://ethresear.ch/uploads/default/optimized/3X/9/0/90ef8eaf266fd5f52899d65634f871c90b513d7c_2_452x500.jpeg)Parallel_Auction_on_Commit-Boost1920×2123 107 KB](https://ethresear.ch/uploads/default/90ef8eaf266fd5f52899d65634f871c90b513d7c)

## 3.2 Process

1. Auction Initiation

- The Gateway declares the start of an auction for a specific slot (e.g., slot N)
- Broadcasts StartAuction(slot N) to all participating Searchers

1. Bundle Submission and StateScope Definition

- Searcher1 → Gateway: submits a bundle containing:

txList1
- bid1
- inclusionHeight

`Gateway`:

- Simulates the bundle and extracts the AccessList
- Derives the corresponding stateScope
- Generates a unique LockId for the bundle

1. Exclusion Commitment Request and Signing

- Gateway → Signer: RequestSig(LockId, stateScope)
- Signer:

Signs the ExclusionCommitment
- Returns ExclusionSig

`Gateway` → `LockEngine`: sends the `ExclusionCommitment`
`LockEngine`:

- Verifies the commitment
- Prepares for stateScope-based transaction filtering

1. StateScope Broadcast and Filtering

- Gateway:

Broadcasts the stateScope to all Searchers
- Prevents overlapping bids and encourages strategy differentiation

`LockEngine`:

- Filters mempool transactions that conflict with the locked stateScope
- Delivers a filtered list of non-conflicting transactions to the Builder

`LockEngine` → `Builder`: `DeliverFilteredTxList`
`Builder`: begins block construction based on the filtered transactions

1. Additional Bids and Auction Finalization

- Searcher2 → Gateway: submits another bundle

Includes:

txList2
- bid2
- inclusionHeight

`Gateway`

- Compares bids and selects the winning bundle (e.g., Searcher2)
- Declares EndAuction and communicates the result

1. Inclusion Commitment Issuance

- Gateway → Signer: RequestSig(bundleHash, inclusionHeight)
- Signer:

Signs the InclusionCommitment (preconfirmation)
- Returns InclusionSig

`Gateway` → `LockEngine`: sends the signed Inclusion Commitment

1. Final Block Construction

- LockEngine:

Verifies the InclusionSig

`LockEngine` → `Builder`: `Send(txList2)`
`Builder`:

- Constructs the block including the given transaction list
- Ensures the bundle is included at the specified inclusionHeight

1. Block Submission and Inclusion Proof

- Builder → Proposer: submits the finalized block
- Builder → Gateway: submits InclusionProof(bundle)
- Gateway → Relay: relays the InclusionProof(bundle)
- Relay:

Verifies fulfillment of the commitment.
- If necessary, propagates proof to the AVS or other monitoring infrastructure

# 4. Handling Race Conditions and Conflicts

---

## 4.1 Preconfirmation Conflict Rule

- Only one valid preconfirmation can be issued for the same stateScope.

A single LockId is assigned to only one winning searcher.
- At the time of the auction, the Gateway determines if a state conflict exists and selects only one winner from the bundles competing for the same stateScope.

If `stateScope`s access mutually disjoint states, preconfirmations can be issued in parallel.

- The Gateway can run auctions for multiple LockIds in parallel.
- The builder, via the LockEngine, manages multiple LockIds in parallel, coordinating the bundles to coexist within the block without interference.

## 4.2 Conflict Detection Criteria and Locus

- Conflict Criteria:

A conflict is identified if two bundles access a state (stateScope) that contains the same contract address or slot-level item.
- The stateScope can be defined at the contract level or slot level; there is a trade-off between implementation complexity and the degree of parallelism achievable.

**Conflict Detection Locus:**

- Gateway: Simulates searcher bundles and extracts their access lists.
- LockEngine: Performs real-time filtering on the builder’s mempool to preemptively remove or reorder conflicting transactions.

## 4.3 Commitment Failures and Penalties

A builder may face slashing or other penalties for violating any of the following conditions:

- Failing to include the winning bundle at the specified inclusionHeight.
- Causing the bundle to fail by including another transaction that accesses the same stateScope before the preconfirmed bundle.
- Omitting or manipulating the signed information from the preconfirmation when constructing the block.
- Proof Submission and Slashing:

The Gateway or the searcher can submit the relevant block and the corresponding Commitment (Exclusion/Inclusion) to an AVS or an on-chain verification module.
- An InclusionProof (e.g., Merkle proof) or the full block data can be used as evidence.

**Exception Handling:**

- If an Inclusion Commitment is not issued after an Exclusion Commitment:

The LockEngine (builder) can automatically release the lock after a certain period.
- A maximum lock duration needs to be set (e.g., within 8 seconds).
- The builder can proceed with block construction, excluding the relevant transaction.

In cases where inclusion is invalidated due to events like a chain re-org, it is necessary to distinguish between proposer fault and builder fault.

# 5. Proof-of-Concept (PoC) Implementation

---

This protocol is not merely a theoretical proposal; we have conducted a practical Proof-of-Concept (PoC) by extending the Commit-Boost architecture in the form of a Local State Lock protocol. The design focused on reusing the existing PBS infrastructure and Commit-Boost design as much as possible while adding new functionalities.

## 5.1 Scope of Implementation

The PoC implemented the following two key commitment processes in code:

1. Exclusion Commitment

Defined the stateScope for a bundle submitted by a searcher.
2. The proposer generated a “conflict prevention” message based on this stateScope and delivered it to all builders.
3. The builder’s LockEngine received this, filtered conflicting transactions from its mempool, and updated its local state.
4. Inclusion Commitment

The proposer determined the winner through a stateScope auction.
5. A preconfirmation was issued to the winner (searcher), containing the LockId, bundleHash, inclusionHeight, etc.
6. This was signed via the Signer module and delivered to the builder.

## 5.2 Operational Flow (PoC)

The end-to-end execution flow implemented in the PoC is as follows:

1. Searcher → Gateway: Submits a bundle and provides its stateScope specification.
2. Gateway → Proposer: Gathers a set of bundles and determines conflicts. For disjoint stateScopes, it runs parallel auctions.
3. Proposer → Builder: Broadcasts the Exclusion Commitment. Issues an Inclusion Commitment for the winning bundle.
4. Builder (LockEngine): Enforces the Exclusion Commitment by excluding conflicting transactions. Enforces the Inclusion Commitment by including the bundle in the specified slot.

## 5.3 Key Experimental Results

- Predictable Execution Guarantees:

Searcher bundles were executed without conflicts from competing bundles accessing the same state, as the lock was applied at the stateScope level.

**Confirmation of Parallel Auction Feasibility:**

- We confirmed that multiple bundles could receive preconfirmations simultaneously when their stateScopes were disjoint.

**Ease of Builder Integration:**

- By implementing the LockEngine as a sidecar, we verified that commitment constraints could be applied without significant modifications to the existing builder logic.

## 5.4 Limitations and Future Work

- The PoC was implemented with a coarse-grained focus on contract-level granularity rather than slot-level locking.
- Some edge cases, such as reorg scenarios, lock timeout handling, and the submission of slashing proofs, remain unimplemented.
- Future work will require integrating TEE/ZK-based block verification and defining more granular stateScopes.

# References

https://github.com/radiusxyz/parallel-auction-commit-boost

https://ethresear.ch/t/state-lock-auctions-towards-collaborative-block-building/18558

https://ethresear.ch/t/commit-boost-proposer-platform-to-safely-make-commitments/20107

https://eips.ethereum.org/EIPS/eip-2930

https://eips.ethereum.org/EIPS/eip-7547

## Replies

**jvranek** (2025-08-25):

This is cool, sounds like a similar approach as [CUSTARD](https://ethresear.ch/t/custard-improving-ux-for-super-txs/21273/1). Something I’ve been considering lately is [EIP-7928](https://eips.ethereum.org/EIPS/eip-7928) can significantly simplify all execution commitments as they expose post-transaction state diffs. Potentially something down the line to consider here.

---

**wooju** (2025-09-03):

Thanks for the great feedback. It gave us a chance to think more deeply about CUSTARD.

**Regarding EIP-7928**

We view the mention of EIP-7928 very positively. Our proposal aims to guarantee a successful execution environment by preventing state conflicts before a transaction is executed. We think EIP-7928 could be an excellent complement to this; it could be used to easily and reliably verify that the post-execution results match the original intent, which would further strengthen the reliability of our proposal.

**On CUSTARD vs. Our Proposal**

We agree with your point. CUSTARD’s “Exclusion preconfirmation” and our proposer-driven approach share the same fundamental goal: to guarantee execution. The core idea of a proposer (or a validator in CUSTARD’s case) assuring a transaction’s success is common to both.

However, we believe there is a subtle difference in the primary scenarios each approach targets.

- CUSTARD’s Target Scenario: It appears to be more focused on ensuring the consistency of a transactional journey when a single user needs to execute a sequence of transactions across multiple domains (e.g., L1 and L2). The key objective seems to be achieving “cross-domain atomicity for an individual user” by locking the user’s own state to ensure their subsequent transactions don’t fail.
- Our Proposal’s Target Scenario: Our approach focuses more on situations where multiple participants, like MEV searchers, compete for a specific shared state (e.g., an AMM liquidity pool) within a single block. The main goal here is to guarantee the deterministic, conflict-free execution of searchers’ strategies by having the proposer directly identify and lock the contested shared state itself, going beyond just an individual user’s assets.

**Question**

To summarize, we think CUSTARD is specialized for “cross-domain consistency via user-driven state locking,” while our proposal is specialized for “guaranteeing competitive intra-block transaction execution via proposer-driven shared state locking.”

We’re curious about your thoughts on whether these two approaches could evolve into a complementary relationship, each solving a different problem space. For instance, could CUSTARD serve to universally improve the cross-chain experience for general users, while our proposal establishes itself as a specialized solution for specific problems within the MEV supply chain (e.g., private order flow, complex multi-party arbitrage)?

We would appreciate hearing your thoughts on this.

