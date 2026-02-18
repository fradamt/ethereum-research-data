---
source: ethresearch
topic_id: 1205
title: Simple honest-majority collation availability proof
author: JustinDrake
date: "2018-02-22"
category: Sharding
tags: []
url: https://ethresear.ch/t/simple-honest-majority-collation-availability-proof/1205
views: 2501
likes: 1
posts_count: 6
---

# Simple honest-majority collation availability proof

**TLDR**: We propose a data availability scheme for collation bodies. The scheme requires collation proposers to prepare availability proofs for their proposals and requires validators to add those to the collation headers in the VMC. Assuming an honest-majority of validators the scheme guarantees both availability and liveliness of collation proposals, and allows for [fork-free sharding](https://ethresear.ch/t/fork-free-sharding/1058). The proof is succinct and simple to produce.

**Construction**

Let B be a collation body for which a proposer wants to produce an availability proof. Let V be the (ordered) list of validators of size |V|=n. For simplicity we assume that validators have fixed-size deposits. The proposer does the following:

1. Shares B with validators and gathers \lceil n/2\rceil BLS signatures for B.
2. The \lceil n/2\rceil BLS signatures are aggregated into a single BLS signature.
3. The proof is the BLS signature plus n bits describing which signatures have been aggregated.

BLS signatures are 20 bytes. So if we have 2048 validators the availability proof is a total of 276 bytes. The VMC rewards every validator that contributed to the BLS signature with a small “signing reward”.

**Analysis**

- Liveliness: By the honest-majority assumption it is always possible to find \lceil n/2\rceil validators that are willing to sign B.
- Availability: By the honest-majority assumption any sampling of \lceil n/2\rceil validators contains at least one honest validator that will broadcast B to the world (e.g. seed B to IPFS).

## Replies

**JustinDrake** (2018-02-22):

An alternative to BLS signatures is to use a threshold signature, and instead of the VMC giving signing rewards, the proposer pays “signing fees” to validators out-of-band.

---

**nate** (2018-02-22):

It seems like when the VMC receives this proof, it actually has to check that the \lceil n/2\rceil  validators who are said-to-have-signed are really the validators that signed - so it can make sure it’s distributing rewards to the right people - which seems like a considerable amount of overhead for the VMC. I don’t know much crypto, though, so let me know if I’m missing something ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**JustinDrake** (2018-02-22):

You’re probably right that checking said-to-have-signed validators is unnecessary onchain work. In the threshold signature alternative the VMC only has to check a single threshold signature without any knowledge of how the threshold signature was constructed.

---

**vbuterin** (2018-02-23):

You can reduce overhead to the VMC by making the signatures off-main-chain and the signer incentivizations be at the shard layer. That would remove the desirable property of having the VMC itself check the signatures, but that’s very high overhead in any case.

---

**kladkogex** (2018-02-23):

Does anyone here have a Solidity implementation of BLS signature verification?

Here is a StackExchange topic

[discussing this](https://crypto.stackexchange.com/questions/53509/can-the-precompiles-in-ethereum-byzantium-for-pairings-be-used-for-implementation)

For BLS signature generation there are several opensource implementations I am aware of: one in DFINITY and another in Hyperledger …

