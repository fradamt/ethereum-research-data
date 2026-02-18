---
source: ethresearch
topic_id: 11877
title: Single-slot PBS using attesters as distributed availability oracle
author: vbuterin
date: "2022-01-27"
category: Proof-of-Stake
tags: [mev, proposer-builder-separation, single-slot-finality]
url: https://ethresear.ch/t/single-slot-pbs-using-attesters-as-distributed-availability-oracle/11877
views: 6062
likes: 9
posts_count: 5
---

# Single-slot PBS using attesters as distributed availability oracle

This post describes a possible alternative paradigm to [two-slot PBS](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980) for designing proposer/builder separation mechanisms. The basic philosophy of this approach is simple: take [MEV Boost](https://ethresear.ch/t/mev-boost-merge-ready-flashbots-architecture/11177) and replace the relayer with a size-256 committee of validators.

- A builder, instead of sending their payload to a relayer, now erasure-codes their payload into 256 chunks (85 needed to recover), encrypts the i’th chunk to the public key of the i’th committee member, and sends this into a p2p subnet.
- Each committee member decrypts their message, and validates the proof. If the proof is valid, they make a pre-attestation to that payload’s header.
- The proposer accepts the highest-bid header for which they found at least 170 signatures
- Upon seeing the proposal, the committee reveals the chunks, and the network reconstructs missing chunks if needed
- Attesters vote on the proposal only if the proposal AND the payload are available

[![mevboost.drawio](https://ethresear.ch/uploads/default/original/2X/9/93ab6d0179b5845d6ce6de9536970b792a01a97d.png)mevboost.drawio581×221 8.31 KB](https://ethresear.ch/uploads/default/93ab6d0179b5845d6ce6de9536970b792a01a97d)

*Simplified diagram of MEV boost*

[![committeeboost.drawio](https://ethresear.ch/uploads/default/original/2X/b/b22665e3a2302aa38bf8e556889f2cc83a41fa14.png)committeeboost.drawio581×361 17.9 KB](https://ethresear.ch/uploads/default/b22665e3a2302aa38bf8e556889f2cc83a41fa14)

*Simplified diagram of this proposal*

### Interaction with sharding

The above diagram assumed a non-sharded chain. There are two natural ways to make this scheme work with the 32 MB payloads of sharding:

1. Require the builder to evaluate the degree-256 polynomial of EC points of the blobs at 768 other points (to preserve zero knowledge), and encrypt the full blob corresponding to each evaluation (or set of 3 blobs) to the corresponding committee member.
2. Apply the non-sharded scheme above only to the ExecutionPayload, and expect the committee to only care about the payload. Once the proposal is published, the committee would decrypt and reveal the ExecutionPayload and the attesters would data-availability-sample the corresponding blobs, expecting them to already be available.

(1) preserves pre-publication-zero-knowledge of the blobs, (2) does not [it only preserves pre-publication zero-knowledge of *which blobs were chosen*]. But (2) is much more efficient and lower-overhead than (1), and requires much less work from the builder.

### DoS protection

When a builder makes a payload of size N, this imposes:

- O(1) load to the entire network
- O(N) load with a very small constant factor (the aggregate signature verification) to the entire network
- O(N) load spread across 256 nodes (so, roughly O(1) load per node if we assume there are as many builder proposals as there are validators)

The second can be managed by splitting committees into many subnets, and the third can be managed by making sure that there are not *too* many payloads (eg. allow each builder to propose a max 3 per block, and increase the min deposit to be a builder). As a practical example, if there are 100000 total validators, and there are 1000 size-1-MB payloads, then the per-validator downloaded data would only be 10 kB.

### Advantages of this proposal vs two-slot PBS

- Single slot, requires less fork choice complexity
- In the same “format” as MEV Boost, requires much less transition complexity for an ecosystem already running on MEV Boost
- Avoids increasing block times
- Possibly higher security margins (1/3 instead of 1/4)?
- No block/slot required
- Easier backoff (just only allow proposals >= k slots after previous proposer to give time to decrypt and attest)

### Disadvantanges of this proposal vs two-slot PBS

- Less convenient for SGX-based searcher/builder architecture, because there is no pre-builder-reveal attester committee that could be used to trigger decryption (such an architecture would have to use its own proposal availability oracle)
- Depends on majority being online to decrypt (possible fix: choose committee from validators present in previous epoch)
- Requires more cryptographic primitives that have not yet been implemented (standardized asymmetric encryption)
- Variant (1) of integration with sharding makes it much harder to make a distributed builder (because of the need to encrypt full bodies of the extension)
- Variant (2) of integration with sharding does not seem to preserve pre-publication zero knowledge of bundles (though maybe pre-publication zero knowledge of _the choice of which bundles_is good enough)

## Replies

**terence** (2022-01-29):

1.) Is the builder here a first-class citizen in the protocol? (i.e. validator)

2.) Does this affect danksharding? if yes, what are the positives and negatives? I guess one positive is the notion of the committee is there already and we can just increase `TARGET_COMMITTEE_SIZE` to 256

3.) How Is size-256 chosen?

---

**vbuterin** (2022-01-30):

1. Even in the existing danksharding spec, the builder needs to be a validator.
2. Actually designing this approach definitely does have some interaction with what the sharding scheme is; but what I have written above already is how it interfaces with danksharding.
3. Smallest completely safe committee size.

---

**taoeffect** (2022-12-13):

Hi all, forgive the very basic question, as basically all of this is over my head and I really do not understand what you guys are doing.

What is a proposer? Are they a staker?

Also, what does MEV have to do with the current situation of stakers censoring the majority of blocks not because of MEV, but because of regulations?

---

**taoeffect** (2022-12-14):

Someone forwarded this video to me from Eric Wall: [Social Slashing by Eric Wall | Devcon Bogotá - YouTube](https://www.youtube.com/watch?v=sFMEeQ4mebA)

It seems to partly answer my question - that you all believe that the current censorship is not being done by validators but by some off-chain group, and that by messing around with MEV incentives and mechanisms you think you might fix the problem.

OK, well, good luck with that. It doesn’t seem to address the fundamental issue, and we’ll see what happens.

