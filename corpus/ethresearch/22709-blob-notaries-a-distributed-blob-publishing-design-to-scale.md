---
source: ethresearch
topic_id: 22709
title: "Blob Notaries: a distributed blob publishing design to scale DA"
author: merklefruit
date: "2025-07-07"
category: Sharding
tags: [data-availability]
url: https://ethresear.ch/t/blob-notaries-a-distributed-blob-publishing-design-to-scale-da/22709
views: 605
likes: 8
posts_count: 1
---

# Blob Notaries: a distributed blob publishing design to scale DA

> by Nicolas, Lorenzo and Jonas from Chainbound.
> Thanks to Francesco and Julian for the early feedback!

Or, how to separate blob *data dissemination* from *consensus* in Ethereum.

**TL;DR:** This proposal stems from the recent discussions on sharding the blob mempool to reach the medium-term scaling goals set out by the Ethereum roadmap. It can be summarized as:

- Delegating a subset of Ethereum nodes to attest to having seen specific blobs
- Delaying DA checks until the next slot, to prevent DoS and allow more time for propagation
- Replacing blob transaction sidecars in the EL mempool with lightweight DA certificates

## Contents

1. Introduction
2. Existing Proposals
3. Proposal: Blob Notaries
3.1. New Blob Transaction Flow
4. Benefits of this approach
5. Compatibility with ePBS (EIP-7732)
6. Open Questions
7. Implementation Notes
8. Future Work
9. References

## 1. Introduction

Ethereum’s DA scaling roadmap has been primarily concerned with scaling DA on the consensus layer through DAS ([PeerDAS](https://eips.ethereum.org/EIPS/eip-7594), Proto-Danksharding). The core idea here is that data is securely sharded and dispersed across the validator set, with some mechanisms to ensure that the data in question is truly available without having to download all of it. This will allow us to scale DA to potentially hundreds of blobs per block.

But as shown in a [recent post](https://ethresear.ch/t/on-the-future-of-the-blob-mempool/22613) by Mike Neuder, the EL blob mempool (*blobpool*) has not been given the same attention. In fact, **in the blobpool today, every validator still downloads the full type 3 transaction (including blobs)** through a lazy-pull mechanism. This asymmetry, even if not a problem today, could definitely become a bottleneck in the future. Furthermore, **scaling DA on the CL will eventually be bottlenecked by the uplink of the (local) block builder**, as the proposer is required to upload the entire blob bundle. We’ll see later that our proposal for fixing the blobpool unlocks distributed blob publishing as well.

## 2. Existing Proposals

Many solutions have been proposed for the asymmetry pointed out above. Here is a brief overview of these, along with their limitations:

- Deprecate the blobpool: remove the blobpool from the EL and rely on builders to offer private blob inclusion endpoints. The problems here are the following:

we want a public blobpool for censorship resistance (CR), because without them, type 3 transactions could never be part of inclusion lists (ILs). CR would overall be much worse.
- builders become responsible for propagating all the blobs as fast as possible, or they risk their block not becoming canonical. The blobpool today also serves as a pre-proposal blob distribution mechanism. For local block builders, this might force them to not include blobs at all, because they can’t deal with the required upload bandwidth. More on that in this post.

**Vertically shard the blobpool**: we can just mirror the structure on the CL, and require blob senders to vertically shard their blob before propagating it. The main concern here is DoS: malicious participants can flood the network with invalid shards, i.e. shards that don’t belong to a valid, fee-paying transaction, or just incomplete data. Researchers have proposed solutions including a [data-driven approach](https://notes.ethereum.org/@dankrad/BkJMU8d0R#Vertically-sharded-mempool) (i.e. gate the ability to send blobs based on some heuristics to make sure that senders won’t spam the network) and a [market-driven one](https://ethresear.ch/t/on-the-future-of-the-blob-mempool/22613) (i.e. use an in-protocol auction to gate access to the blobpool).
**Horizontally shard the blobpool**: blob transactions are still broadcast in full, like today, but they are propagated in different mempools or *subnets* based on some predicate (like sender address or transaction hash). The main advantage here is that it’s simple, and DoS resistant. But it would still require (local) block builders to download and propagate all blobs in order to propose them, as Dankrad pointed out [here](https://notes.ethereum.org/@dankrad/BkJMU8d0R#Vertically-sharded-mempool).

The [most recent proposal](https://ethresear.ch/t/on-the-future-of-the-blob-mempool/22613) builds on vertical sharding, but includes a market mechanism to determine who can write to the blobpool. This ensures that there’s always an upfront cost to publishing blobs that can only be recovered when the full blob is included, and thus remediates the DoS issues with the original proposal. The main downsides we see are the following:

- As a blob publisher:

The delay between having a blob to include and when it’s actually included.
- The execution gas cost of placing a bid.

As a protocol:

- Running an auction on the L1 can introduce significant complexity
- Using Ethereum blockspace and gas for auction tickets might not be very efficient

## 3. Proposal: Blob Notaries

We propose to introduce a new committee (the *Blob Committee*) that is a random subset of the validator set with the following responsibilities:

- Receiving type 3 transactions (carrying blobs) and validating them
- Attesting to the availability of the blob data by producing blob certificates (BLS signatures over the blob commitments)
- Sharding and publishing the columns on the CL eventually

We call these committee members ***Blob Notaries***. Blob notaries are able to isolate initial blob and transaction validation to protect against network-wide DoS. Additionally, they can be relied on as a temporary DA oracle during block production, which can therefore remove download bottlenecks from the hot-path of proposal, both with local building and PBS. Finally, they can increase the throughput of blob dissemination by distributing the work between themselves, unlocking *distributed blob publishing*.

Note that this committee could eventually evolve into a separate validator role, skewed towards higher bandwidth usage, in the spirit of [rainbow staking](https://ethresear.ch/t/unbundling-staking-towards-rainbow-staking/18683).

### 3.1. New Blob Transaction Flow

We will focus on the proposal happy path to avoid cluttering the article with complexity. However, some preliminary questions and answers can be found in *Implementation Notes* below.

**Step 1: Acquire Blob Quorum Certificates (QCs)**

[![shapes at 25-06-24 14.46.37](https://ethresear.ch/uploads/default/optimized/3X/9/0/90d9d4630a578c3751626ff3a9d772cd3f8687ed_2_690x482.jpeg)shapes at 25-06-24 14.46.371668×1167 183 KB](https://ethresear.ch/uploads/default/90d9d4630a578c3751626ff3a9d772cd3f8687ed)

- The blob sender gossips the type 3 transaction (including the blob sidecar) to all blob notaries for that slot.
- The blob notaries will validate the transaction on the pending state, and respond with their signature over the blob commitment. We call this signature a Blob Certificate.
- The blob sender aggregates these BLS signatures into a 2/3 majority, obtaining a blob Quorum Certificate (QC).

This step ensures that, between committee members, enough honest members custody the blob data and attest that the transaction is valid. The QC is a reflection of that. However, the existence of a QC does not guarantee DA at network-level, as the attesters haven’t voted yet. They can be thought of as a “credible signal”, but not guaranteed availability.

**Step 2**: **Broadcast to the EL Mempool**

[![shapes at 25-06-24 14.49.14](https://ethresear.ch/uploads/default/optimized/3X/0/f/0fa00555bd8c16820f6d14a2a75e22fe9f0486d2_2_690x211.jpeg)shapes at 25-06-24 14.49.141860×570 81.1 KB](https://ethresear.ch/uploads/default/0fa00555bd8c16820f6d14a2a75e22fe9f0486d2)

- Once the QC is obtained, the blob sender can send the type 3 transaction envelope with QC on the EL mempool instead of the type 3 transaction with blob sidecar.
- Regular nodes only need to propagate the transactions with lightweight certificates.
- Validating QC requires some level of communication with the CL. The design space is quite large, but we haven’t found a convincing design yet. See the Open Questions section for more details.

**Step 3: block proposal and attestation**

[![shapes at 25-06-24 14.59.08](https://ethresear.ch/uploads/default/optimized/3X/4/0/4085cc2c201b70fda2dc53518004a1eb23ddfac9_2_690x183.jpeg)shapes at 25-06-24 14.59.082164×575 86.1 KB](https://ethresear.ch/uploads/default/4085cc2c201b70fda2dc53518004a1eb23ddfac9)

- The proposer includes type 3 transactions in its block as usual. However, instead of adding the blob bundle to the beacon block envelope, it will add the QCs of the blobs. This consists in a new field blob_quorum_certificates on the BeaconBlockBody container.
- The beacon block envelope does not contain the full blob bundle here anymore.
- When the attesters receive the new block, they won’t validate the availability of its QCs yet, but instead they will only validate the execution of the block (more on this later).
- If the block receives enough valid votes in time, it will become canonical, as usual.

**Step 4: blob shard propagation**

[![shapes at 25-06-24 15.09.58](https://ethresear.ch/uploads/default/optimized/3X/d/e/de717c5af15042b863190a604888af7e951ada60_2_690x490.jpeg)shapes at 25-06-24 15.09.582142×1524 218 KB](https://ethresear.ch/uploads/default/de717c5af15042b863190a604888af7e951ada60)

- Now that the attesters have voted and added the new block to their canonical chain, the blob notaries can start disseminating the blob data to the rest of the network via vertical shards.
- Any node is able to immediately verify that these shards are valid, because they belong to blobs whose commitment were included in the chain’s head block, with valid QCs. This prevents the DoS vector identified in the Existing Proposals above.
- Blob notaries have already signed the blobs in the canonical block, so they are fully incentivized to share the data before the data availability attestation deadline.

**Step 5: DA Attestation**

[![shapes at 25-06-24 15.22.27](https://ethresear.ch/uploads/default/optimized/3X/2/1/215995b199184d62d999ddb974d25dc7cbfed9c3_2_651x500.jpeg)shapes at 25-06-24 15.22.271920×1474 86.1 KB](https://ethresear.ch/uploads/default/215995b199184d62d999ddb974d25dc7cbfed9c3)

- The next slot starts, and attesters are asked to vote for two things:

Valid execution of the block proposed in that slot (block N)
- Data availability of the blobs proposed in the previous slot (block N-1)
- Logically these are conceived as two attestation events, but in practice we can think of the attestation as accommodating a new, more sophisticated fork-choice rule:

block N execution must be valid, AND block N-1 data must be available.

This mechanism allows for a full-slot worth of time to propagate the blob shards: approximately from the previous slot’s attestation deadline to the current slot’s attestation deadline.

## 4. Benefits of this approach

**1. High blob throughput**

Blob throughput in Ethereum is bottlenecked by the following factors:

- validators (including solo-stakers) need to upload the entire blob bundle when proposing
- after PeerDAS, proposers will still have limited time to propagate blob shards in the CL

Our proposal tries to address these limitations with traditional scaling methodologies:

- Horizontal scaling: by having many blob notaries instead of just one proposer, the network’s cumulative blob uplink can be orders of magnitude higher.
- Vertical scaling: by designating a specific network role (à la rainbow staking) for blob notaries, we can extend their hardware/bandwidth requirements without compromising on the nice properties of a credibly decentralized attester set, such as censorship and collusion resistance.

**2. No blob shard spam on the CL**

If CL nodes were to receive a shard that is not part of any recent blob, they can reject it and apply the necessary reputation penalties to the peer that shared it, minimizing the DoS potential.

As a side benefit, delaying the DA checks to the next slot will also maximize the likelihood of data being available in time, because blob notaries now have a full slot (roughly from the previous slot’s attestation deadline to the current’s slot attestation deadline) to propagate shards.

**3. Cheaper blob transaction replacements in the EL**

Currently, replacing a type 3 transaction is very expensive (e.g. [Geth requires a 100% fee bump](https://github.com/ethereum/go-ethereum/blob/b47e4d5b38b34c045cb10af6c0b5603c285310cd/core/txpool/blobpool/blobpool.go#L1142-L1179)). This is mainly because the network has to incur the cost of propagating the full blob sidecar in the EL mempool. With blob committees, transactions in the EL mempool would only carry lightweight QCs, making transaction replacements as cheap as other transaction types.

**4. Lower “cost of latency” for including blobs**

Blob transactions in PBS today need to pay an indirect latency cost. This is because blocks with more blobs [need to compete with more lightweight blocks in the PBS auction](https://ethresear.ch/t/blobs-reorgs-and-the-role-of-mev-boost/19783). With this proposal, blocks with more blobs would only carry a marginal size increase for their certificate.

**5. Trivial support for type 3 IL transactions**

Since the full blob is replaced by a lightweight DA certificate in the EL mempool, type 3 transactions become much smaller and can be supported by [FOCIL](https://eips.ethereum.org/EIPS/eip-7805). Validating the QC would be part of the [CL P2P validation rules](https://eips.ethereum.org/EIPS/eip-7805#cl-p2p-validation-rules) for validating ILs.

## 5. Compatibility with ePBS ()

The current ePBS spec makes it possible to shift the execution and DA attestations into the same slot, allowing for a much simpler fork-choice rule. However, since there is no natural “commit” phase for the QCs anymore, nodes must rely on weaker guarantees to counter DoS.

Essentially, blob notaries would need to wait for the payload release before they can start propagating blob shards. This way, recipient nodes would be able to verify that the data they’re receiving is actually part of the payload they just received from peers. Any shard not part of the payload would be discarded, and the sender would accrue negative reputation. To address data races, nodes could even wait for a payload before judging the validity of recently received shards.

Here is the slot structure, following the recent [double deadline PTC vote](https://notes.ethereum.org/@anderselowsson/Dual-deadlinePTCvote) ePBS design:

[![shapes at 25-07-07 16.07.43](https://ethresear.ch/uploads/default/optimized/3X/6/6/669a79822663ba5abf1537ed4686a7fda4dfc214_2_690x263.png)shapes at 25-07-07 16.07.432025×772 70.9 KB](https://ethresear.ch/uploads/default/669a79822663ba5abf1537ed4686a7fda4dfc214)

Blob shards received before the red X would be cached by attesters for a short while, and once the payload arrives, they would be validated. If they don’t match any of the blob commitments included in the payload, then they can be discarded and the sending peer penalized. If they are valid, then they can be broadcast to other peers. This way, regular attesters will only participate in fan-out once they know they are propagating valid data, which is desired.

## 6. Open Questions

1. The blob notaries will most likely require higher bandwidth than regular attesters. How should the network deal with low-performing notaries? Should they simply miss the rewards or get slashed? How does the network detect (poor) performance reliably?
2. Should blob notaries be rewarded fairly for their job in-protocol? If so, how?
3. How to verify QCs in the EL mempool? Any solution would require some communication of CL data to the EL; here are some possible options we’ve thought of:

We could store and update the blob notaries pubkeys in a system contract which gets regularly updated, and broadcast on the EL an aggregation bitlist in the new EIP-4844 variant along with the QCs (sort of similar to EIP-4788).
4. The existing engine API could be extended by sending tuples of (tx_hash, quorum_certificates) periodically via an endpoint engine_newQuorumCertificates. When a type 3 transaction announcement is received on devp2p, it is pulled only if the transaction hash has been already heard from the CL.
5. There is no validation of QCs in devp2p, but when the next proposer creates a block from EL data, in the engine_forkchoiceUpdated PayloadAttributes we also send a list of QCs already validated by the CL client. While this can still ensure proposal of valid transactions, it might open some DoS concerns in the EL mempool.

How would private blob submission to block builders work under this model?

1. Perhaps it would be possible to keep the current blob transaction pipeline as a fallback, which can then be used by builders to include blobs. Essentially, this means it would be possible to include a blob by either providing its entire contents in the proposal OR a valid signed QC. In case the beacon block envelope carries some full blobs, the block builder and proposer for that slot carry the extra risk of distributing the data in time for the DA attestation. This added risk could simply be absorbed by the PBS market by making private blobs more expensive to send on average, which also aligns with the desiderata of not straining the regular attesters with added bandwidth requirements.

Failure cases for attestation, missing DA, blob notary rewards, etc are still mostly TBD!

## 7. Implementation Notes

**1. On EIP-4844 transaction envelope and certificates**

We introduce a new EIP-4844 transaction **variant** which carries a *quorum certificate* instead of the blob sidecar. The signed transaction envelope won’t change, as it already doesn’t include the sidecar today, but rather the QC will be treated as a new consensus layer item.

Here is a short overview of how we imagine blobs could exist in the protocol:

- With full blob sidecar: on the EL, at the RPC layer only (necessary for ingestion from users)
- With a QC: in the EL mempool when the transaction can be included

Note: we are not proposing to create a new transaction type. The EL spec already involves different representations of how EIP-4844 transactions can be seen: one with and one without the blob sidecar. We propose to add a new variant: without the blob sidecar but *with the QC*.

**2. A malicious user might send type 3 transactions to the blob notaries, but then never submit the transactions in the mempool, wasting the resources of the blob notaries**

- To avoid this, we can leverage the role of aggregators in the beacon chain to provide redundancy, so that any of them can submit the valid transaction in the EL mempool in place of the blob originator; this would look similar to the current attestation subnet aggregators, randomly selected between the committee members.
- Blob aggregators perform their duty in step 1) of the proposed flow. In step 2), aggregators can send the blob transaction in the mempool for added redundancy.

**3. Why separate the two attestations (execution and DA)?**

- The idea is that with this distinction the shards of blobs that are still pending wouldn’t be allowed to enter the CL P2P network, minimizing DoS vectors overall.
- The added benefit is a much larger time frame for disseminating data, which scales well with throughput increases.

## 8. Future Work

- We plan to study compatibility with other EIPs currently planned for the Glamsterdam hard-fork, such as EIP-7886: Delayed execution, and six-second slot times as proposed in EIP-7782: Reduce Block Latency.
- We’d like to come up with theoretical benchmarks for throughput allowed by this technique, based on existing p2p data and the new slot deadlines.
- The requirements and economics of blob notaries are also an interesting topic that is out of scope of the technical spec but would be nice to explore.

## 9. References

- On the future of the blob mempool
- Payload-timeliness committee (PTC) – an ePBS design
- Estimating Validator Decentralization Using p2p Data
- Decoupling throughput from local building
- Time, slots, and the ordering of events in Ethereum Proof-of-Stake - Paradigm
- EIP-7886: Delayed execution
- Sharded blob mempool and distributed block production - HackMD
