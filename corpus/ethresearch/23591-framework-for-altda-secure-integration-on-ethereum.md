---
source: ethresearch
topic_id: 23591
title: Framework for AltDA Secure Integration on Ethereum
author: bxue-l2
date: "2025-12-02"
category: Layer 2
tags: [data-availability]
url: https://ethresear.ch/t/framework-for-altda-secure-integration-on-ethereum/23591
views: 264
likes: 7
posts_count: 1
---

# Framework for AltDA Secure Integration on Ethereum

# Framework for AltDA Secure Integration on Ethereum

### Introduction

We present a technical framework and set of definitions for secure AltDA integration. This aspect of system design is often under-specified in current AltDA protocols, leaving L2 chains vulnerable to safety and liveness failures. Our aim is to offer a framework that is broadly applicable across Ethereum L2, enabling secure AltDA integration with little or no modification to existing architectures.

This framework builds on the same core premise articulated in L2Beat’s article [Secure Integration of Alt-DA L2s with Data Availability Verifiers](https://forum.l2beat.com/t/secure-integration-of-alt-da-l2s-with-data-availability-verifiers/408), that any secure integration must assume the sequencer may behave maliciously. While the L2Beat article outlines high-level requirements and attack scenarios, our approach formalizes these ideas with explicit domain definitions and total functions. This provides a more precise way to specify integration requirements and to compose them into a complete validation flow.

At a high level, we view AltDA integration as a sequence of deterministic data transformations across three data structures. Each step must be deterministic, well-defined, and correct for all possible inputs.

### Background

At the high level, an Ethereum rollup consists of

- An L1 inbox accepts DA commitment submitted from L2 sequencers. Each DA commitment contains sufficient data to retrieve the unique blob from the Data Availability network. The ordering of the DA commitments in the L1 inbox defines the canonical ledger for a L2 consensus.
- A Data Availability(DA) network stores blobs and guarantees their retrievability for a defined period. Each blob has a corresponding DA commitment binding to the blob, making it infeasible to find another blob that maps to the same DA commitment.
- A L2 consensus contains derivation logics that consumes a DA commitment and produces rollup payloads from blobs. A rollup payload is a data structure native to L2 consensus; whereas a blob is native to DA network.

We use sequencer to denote the entity that submits AltDA commitments to L1 and blobs to the DA network. We use proposer for the entity that posts L2 state roots on Ethereum. For a secure integration, the L2 proposer and sequencer must not be trusted for safety and liveness of the L2 consensus.

In the following section, we show how failing to satisfy certain constraints can break safety or liveness. Safety failures typically cause L2 forks: among offchain consensus nodes and among L2 light clients on Ethereum, which ultimately protect the funds locked in the L1 bridge. Liveness failures halt the L2 chain, preventing withdrawals or further activity. In some cases, liveness failures also enable bridge theft.

[![Screenshot 2025-11-24 at 4.26.11 PM](https://ethresear.ch/uploads/default/optimized/3X/c/0/c0fab32d0b41c93f90f910ad0c5dbb9ae5722a2c_2_690x329.png)Screenshot 2025-11-24 at 4.26.11 PM1922×918 75.4 KB](https://ethresear.ch/uploads/default/c0fab32d0b41c93f90f910ad0c5dbb9ae5722a2c)

```auto
            L2 node deriving rollup payload from AltDA Commitment
```

### AltDA Secure Integration as Data Transformation

A L2 consensus processes DA commitments sequentially. For each commitment, it fetches the corresponding blob from the DA network and decodes it into a rollup payload. We define:

- AltDA Commitment: a byte-array submitted to L1. Unlike Ethereum native versioned KZG commitments, an AltDA Commitment may contain a merkle commitment or KZG commitment over other curves. AltDA Commitment can include extra metadata such as DA operator attestations showing the blob has been stored.
- Blob: A binary data structure stored in the AltDA network, whose commitment appears in the AltDA commitment.
- Rollup Payload: The L2 native data structure derivable from a blob.

To start, we assume an honest sequencer who always posts valid AltDA commitments to L1 and stores well-formed blobs in the DA network. This simplifies the analysis and lets us focus on attacks from malicious proposers and malicious blob providers. Under this assumption, the following two constraints ensure that adversaries cannot induce forks among L2 nodes, either offchain or onchain.

### Binding between data commitment and Blob

If the underlying commitment scheme (Merkle or KZG) is compromised or incorrectly implemented, an adversary can produce a second preimage. In other words, for a given data commitment `g = H(X)`, where `X` is the original data, a malicious blob provider can find another `Y ≠ X` such that `g = H(Y)`. By distributing different valid blobs to different L2 nodes, the adversary can induce a fork. Even worse, a malicious proposer can present either blob to an L2 light client on Ethereum and convincingly prove its validity, creating an L2 fork at the L1 level.

For this reason, the DA network must use a binding commitment scheme, and every L2 node must verify that the blob it retrieves actually matches the commitment included in the AltDA commitment.

### Decode Blob Deterministically

Decoding must be deterministic so that any two honest nodes, when given the same blob, always derive the same rollup payload.

Consider an flawed integration scheme, where L2 nodes skip both commitment checking and decoding, and instead trust someone for rollup payload directly. This approach reintroduces the risk of L2 forking for the same reason as in the previous example, because there is no enforced linkage between the rollup payload, the blob, and the AltDA commitment. Without the linkage, honest challengers have no reliable evidence to prove which payload is legitimate.

### Malicious Sequencer

To make the system truly secure, we must assume the sequencer can behave arbitrarily. A malicious sequencer can: 1. post corrupted data to the L1 inbox, 2. encode rollup payloads incorrectly before storing the corresponding blobs. Without proper AltDA integration, the sequencer can exploit these behaviors to halt the L2 chain by feeding undefined or invalid inputs into the derivation process. Most of these attacks causes liveness failures, but in some cases they can escalate into attacks that drain the L1 bridge, including the [data withholding attack](https://forum.l2beat.com/t/secure-integration-of-alt-da-l2s-with-data-availability-verifiers/408#p-683-potential-attack-scenarios-and-mitigations-6).

[![Screenshot 2025-11-24 at 4.26.31 PM](https://ethresear.ch/uploads/default/optimized/3X/2/2/22bfb0456e06d12a20da018b14ca698f80f1ec31_2_690x357.png)Screenshot 2025-11-24 at 4.26.31 PM1936×1002 82.6 KB](https://ethresear.ch/uploads/default/22bfb0456e06d12a20da018b14ca698f80f1ec31)

```auto
    Unlike last diagram malicious sequencer can put anything
    in L1 inbox, the red arrow represents discarding of the corrupted data
```

### Deserializing bytes into AltDA commitment

When sequencers are not trusted, L1 inbox entries can contain arbitrary byte strings. The first step is to check whether they can be deserialized into a valid AltDA commitment. If deserialization fails, the bytes must be discarded and consensus proceeds to the next inbox item.

However, deserialization alone is insufficient. A malicious sequencer can serialize a syntactically valid (by assigning random value) but semantically fake AltDA commitment. Additional checks are required to detect such commitments.

### Data Availability Verifier

A Data Availability Verifier(DAV) verifies whether AltDA commitments corresponds to some blobs that have been stored by DA network. The L2beat [article](https://forum.l2beat.com/t/secure-integration-of-alt-da-l2s-with-data-availability-verifiers/408) highlights its role in preventing the Data Withholding Attack. Here we formalize it within the data-transformation framework.

Given some arbitrary bytes `X` taken from the L1 inbox, the possible set of value for `X` are {0,1}^1048576, , assuming the maximal transaction size is 128KiB (though theoretically the transaction size might be [larger](https://eips.ethereum.org/EIPS/eip-7623) because the protocol constraint is placed on gas). Only a subset of these bytes can be deserialized to a valid AltDA commitment data structure, and denote this subset by `S`. The `DAV` is then a function on `S` that that returns 1 if the corresponding blob is stored by the DA network and 0 otherwise. This partitions `S` into two sets D and D’, where values in D maps to 1.

[![Screenshot 2025-11-19 at 11.52.19 AM](https://ethresear.ch/uploads/default/optimized/3X/b/6/b6ec3bcc9caebbac3ebcfd6130c19a794e7e214d_2_690x262.png)Screenshot 2025-11-19 at 11.52.19 AM1726×656 80.5 KB](https://ethresear.ch/uploads/default/b6ec3bcc9caebbac3ebcfd6130c19a794e7e214d)

### Total vs Partial vs Incorrect DA Verifier Implementation

Different AltDA networks have different commitment formats and DA verifier logic, but all implementations can be characterized by totality and correctness:

A `DAV` implementation is total if all values from `S` evaluate to some output; it is partial if some values cannot be evaluated. For instance, if a `DAV` implementation only evaluate on `D`, and a malicious sequencer submit `q \in D'`, then the `DAV` will encounter an undefined case. This can cause the L2 consensus to halt, effectively freezing all funds.

A DA verifier is incorrect if it misclassifies AltDA commitments. If it returns 1 to some AltDA commitments whose blobs are not stored by the network, the consequence is data withholding attack. If it returns 0 for some AltDA commitments with stored blobs. This is a weaker liveness attack. Although the sequencer’s data is ignored, most rollup designs allow users to exit via force-inclusion mechanisms, and in this case the L2 consensus does not halt.

A total and correct DAV implementation is necessary for light clients to assert L2 state without exposing attack vectors. If the `DAV` implementation is native on Ethereum, the light client can simply make the contract call; otherwise, the light client must rely on a cryptographic proof that DA verifier is executed correctly.

Halting failures can lead to loss of L1 funds for rollups using challenge games. For instance, the data withholding attack is a halting failure which prevents honest challengers from retrieving data to win the game. Likewise, if a challenge game requires challengers to submit a valid state transition, any halt in L2 consensus prevents them from deriving the correct state and can cause them to lose challenges.

### Recency Checks in the Framework

Even if a AltDA commitment passes the DA verifier, it may still be unavailable due to a [Recency / Timing Attack](https://forum.l2beat.com/t/secure-integration-of-alt-da-l2s-with-data-availability-verifiers/408#p-683-potential-attack-scenarios-and-mitigations-6): the sequencer may delay posting the AltDA commitment until after the DA network prunes the blob. A recency check is another function that returns 1 only if the commitment is recent. This further partitions `D` and composes naturally with more checks. The order of checks is irrelevant because an AltDA commitment is acceptable only if all the checks pass.

### Blob and Rollup Payload

After confirming that the AltDA commitment corresponds to an available blob, the next step is to retrieve and decode the blob into a rollup payload. A rollup payload is an abstract concept, which is a data structure native to rollup stack, such that any data corruption in the rollup payload will be handled by the rollup stack itself. For example, in native Ethereum DA, a malicious sequencer can put gibberish data into the blob, but the rollup stack can detect and drop the invalid rollup payload. This allows us to focus on the encoding and decoding between rollup payload and blob.

For merkle commitment, a blob consists of a list of merkle leaf each holding some power of 2 bytes; some metadata is required to specify which and how many leaves belong to the blob given there are other leaves in the merkle tree. To convert a rollup payload to a blob, the rollup payload data is chopped into some number of leaves.

With KZG commitments, blobs are made of field elements, which are small fixed-size units each carrying about 254 bits. Ethereum always uses exactly 4096 of these units, but AltDA systems can allow variable length, and must include metadata to specify the exact number. Rollup payloads almost never align naturally with field element boundaries, so extra padding is required to convert the payload’s bytes into a valid list of field elements.

Regardless of the commitment scheme, the size of the rollup payload almost never fits evenly into the basic data unit, whether the unit is a merkle leaf or a field element. This means the payload must be padded before it can be converted into leaves or field elements during encoding. To later remove this padding during decoding, the original rollup payload size must be passed as a part of the metadata, which either lives in the blob content itself, or in the AltDA commitment.

### Decoding Blob to Rollup Payload

Just as a malicious sequencer can post meaningless data to the L1 inbox, it can also create a blob from a valid rollup payload but encode it incorrectly. For example, the sequencer may claim in the metadata that the payload is larger than the blob actually contains, or it may change a version byte that controls the data layout or the decoding algorithm. Either case can cause decoding to fail.

When a blob cannot be decoded, the AltDA integration for any L2 consensus must simply skip it. Otherwise, the L2 consensus may halt or crash.

### L2 consensus light client on L1

Unlike a L2 consensus node, a light client cannot download or execute all the checks above, as the execution is expensive. But given a well defined data transformation procedures, the light client can rely on an interactive game or zk proof to ensure any claimed L2 state adhering to the all the necessary checks.

### Conclusion

As the L2Beat article highlights, the derivation logic for AltDA-integrated L2 chains can be specified with great precision. In this article, we presented a general framework based on viewing AltDA integration as a sequence of data transformations. This perspective helps clarify the essential checks required for secure integration and extensible to add new requirements. The framework is intended to apply broadly to any L2 architecture that processes DA commitments through an L1 inbox.

EigenLabs provides a secure OP Stack integration that implements all parts of this framework. The core library, [hokulea](https://github.com/Layr-Labs/hokulea) and [eigenda-proxy](https://github.com/Layr-Labs/eigenda/tree/master/api/proxy#eigenda-proxy-), have been audited by [Veridise](https://github.com/Layr-Labs/hokulea/blob/2e726fb83cc33f4370d581d9b8f152df8e40c0ff/audits/Hokulea%2520Veridise.pdf) and SigmaPrime respectively, following the same principles described in this article. For a full end-to-end architecture that adheres to this framework, please refer to the EigenDA integration [specification](https://layr-labs.github.io/eigenda/integration/spec/6-secure-integration.html#eigenda-blob-derivation).

[![Screenshot 2025-11-20 at 4.26.02 PM](https://ethresear.ch/uploads/default/original/3X/4/2/429581fb60b00017d01bba2b06b79c05eb3a9369.png)Screenshot 2025-11-20 at 4.26.02 PM1736×838 14.7 KB](https://ethresear.ch/uploads/default/429581fb60b00017d01bba2b06b79c05eb3a9369)

An informal illustration of how invalid data from a L2 sequencer is filtered during the data-transformation process. Red dots represent inbox entries that fail one or more checks and are discarded. Blue dots represent AltDA commitments that pass all checks, as well as the rollup payloads that are deterministically decoded from the corresponding blobs. The blue dots entering the funnel are valid AltDA commitments, and the blue dots exiting at the bottom are the resulting rollup payloads. Note decoding blob to rollup payload is also part of the funnel.
