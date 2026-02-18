---
source: magicians
topic_id: 23029
title: Uncouple execution payload from beacon block
author: g11in
date: "2025-03-01"
category: EIPs > EIPs core
tags: [consensus-layer]
url: https://ethereum-magicians.org/t/uncouple-execution-payload-from-beacon-block/23029
views: 93
likes: 1
posts_count: 3
---

# Uncouple execution payload from beacon block

## Abstract

Currently the beacon block in ethereum consensus embeds the transactions in `ExecutionPayload` field of `BeaconBlockBody`. This EIP proposes to replace `ExecutionPayload` with `ExecutionPayloadHeader` in `BeaconBlockBody` and to independently transmit `ExecutionPayloadWithInclusionProof`.

However this EIP makes no change to the block import mechanism except that block availability also now includes waiting for the availability of `ExecutionPayloadWithInclusionProof` and this is where its different (and simpler) from proposals like ePBS.

But this availability requirement can infact be restricted to `gossip` import while allowing optimistic syncing of ELs on checkpoint/range sync as EL can pull full blocks from their peers in optimistic sync as they do now.

## Motivation

Ethereum protocol has an ambitious goal to grow the `gasLimit` of the execution payloads (possibly by 10X). This introduces bigger and bigger messages in the networking and block processing pipeline of the CL clients leading to following issues:

1. Latency for the arrival of Beacon Block increases and make it more and more dependent on the bandwidth resources available to the running node.
2. The greater number/size of transactions directly increase the merkelization compute time directly affecting the import time of the block.

We know from timing games that the block import latency greatly affects a client’s performance to make correct head attestations. With this EIP, block transmission and import pipeline will be unchocked and allows for greater flexibility in reception of huge `ExecutionPayloadWithInclusionProof` while the beacon block can undergo processing.

Infact EL clients can also independently participate in the propagation/pull of the execution blocks. That mechanism however can be independently developed and is not the part of this EIP.

Other side benefits of this EIP are that

- consensus clients don’t need to store and serve blocks with transactions and provides greater efficiency and reduced resource requirement for running the nodes.
- the PBS pipleline becomes more efficient by proposer transmitting the signed block directly to the p2p network while also submitting to the builder/relay for independent reveal of the ExecutionPayloadWithInclusionProof.
- in future with ZK proof of the EL block execution, one could treat the transactions just like blobs leveraging DAS mechanisms for the availability without worrying about their execution validity.

## Specification

- ExecutionPayload in the BeaconBlockBody is replaced by ExecutionPayloadHeader
- ExecutionPayloadWithInclusionProof is computed by the proposer/builder and transmitted independently on a gossip channel.
- data availability checks now also wait for availability of a VALID ExecutionPayloadWithInclusionProof
- newPayload on engine api is modified to now accept newPayloadHeader and a new method for newExecutionPayload is introduced to check the vailidity of the ExecutionPayload recieved within ExecutionPayloadWithInclusionProof

ELs can optionally introduce `getExecutionPayload` method (like `getBlobs`) to help fast recovery of execution payload from the EL p2p network but as noted above that mechanism could be independently speced and is not part of this EIP.

#### Update Log

- 2025-03-01: initial draft https://github.com/ethereum/EIPs/pull/9432

#### External Reviews

## Replies

**sbacha** (2025-03-02):

Why should timing games be of any consideration?

---

**g11in** (2025-03-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/g11in/48/3906_2.png) g11in:

> We know from timing games that the block import latency greatly affects a client’s performance to make correct head attestations

its not a concern of this EIP but inference how critical the latency of import pipeline can get for a CL client

