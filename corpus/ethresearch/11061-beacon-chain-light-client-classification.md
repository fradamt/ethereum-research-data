---
source: ethresearch
topic_id: 11061
title: Beacon Chain Light Client Classification
author: jinfwhuang
date: "2021-10-20"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/beacon-chain-light-client-classification/11061
views: 3159
likes: 3
posts_count: 3
---

# Beacon Chain Light Client Classification

## Beacon Chain Light Client Classification

A beacon chain light client allows access to Ethereum on resource-constrained environment, e.g. phones, metered VM, or browsers. A light-client should be defined with respect to the set of APIs that it could handle.

I could not find any posts or spec documents discussing the full scope of functionality that the beacon-chain light client is supposed to cover. Instead of narrowing down a single scope, I am listing out a reasonable progression of the functionalities that a light-client could. It ranges from the minimal client to a client resembling a full node.

For each of the level of functional completeness, I also sketch out what kind input data is required for the client to compute the answers of the API queries.

### Level 1: Minimum

The minimum beacon chain light client syncs to the latest header using sync_committee signatures. The client can only answer questions with the information contained in the BeaconBlockHeader.

#### Supported APIs

```auto
- /eth/v1/beacon/headers
- /eth/v1/beacon/states/{state_id}/root
```

#### Input Data

The client needs to have access the following two message types specified in the consensus-spec about [minimal light client](https://github.com/ethereum/consensus-specs/blob/a20f6f7b5f40292c2a864337336bff74ae318354/specs/altair/sync-protocol.md#altair----minimal-light-client).

```auto
LightClientSnapshot
LightClientUpdate
```

### Level 2: Access Beacon State

The client is able to answer most of the questions with regard to the [BeaconState](https://github.com/ethereum/consensus-specs/blob/0eb3a865df929e60e01104d83b2e8635c7d8d3e7/specs/altair/beacon-chain.md#beaconstate).

#### Supported APIs

The following list not exhaustive, but it is representative of the set of functions that this client intends to support.

```auto
​/eth​/v1​/beacon​/genesis
​/eth​/v1​/beacon​/states​/{state_id}​/root
​/eth​/v1​/beacon​/states​/{state_id}​/finality_checkpoints
​/eth​/v1​/beacon​/states​/{state_id}​/validators
​/eth​/v1​/beacon​/states​/{state_id}​/validators​/{validator_id}
​/eth​/v1​/beacon​/states​/{state_id}​/validator_balances
​/eth​/v1​/beacon​/states​/{state_id}​/committees
​/eth​/v1​/beacon​/states​/{state_id}​/sync_committees
```

#### Input Data

- Type 1: Updating to latest header

```auto
LightClientSnapshot
LightClientUpdate
```
- Type 2: Answering query on BeaconState

It is not likely that the client wants to keep an up-to-date copy of BeaconState locally. It only keeps track of the state root.
- To answer a query, the client needs access to the corresponding leave node of the beacon state. It gets the leave nodes and multiproof from a network layer.
- The client validates the proof and use the data to compute an answer.

```python
class BeaconStateProof(Container):
    leaves: Sequence[Bytes32],
    leave_indices: Sequence[Bytes32],
    proof: Sequence[Bytes32],
```

### Level 3: Support Attestation Client

The beacon chain client is able to support a validator that is only performing attestation tasks.

Attestation makes up the bulk of the workload for a validator client. If a “attestation client” could be supported by a light weight beacon chain client, it could open the door to allow a majority of the validation tasks to be run on resources constrained devices. The rest of the validation tasks, e.g. block proposing and sync committee signing, could be backed by a smaller set of full nodes with higher resources requirements.

#### Supported APIs

The client needs to support all the queries required to complete the attestation duties.

```auto
​/eth​/v1​/beacon​/states​/{state_id}​/validators​/{validator_id}
​/eth​/v1​/validator​/duties​/attester​/{epoch}
​/eth​/v1​/validator​/attestation_data
```

#### Input Data

- Type 1: Updating to latest header

```auto
LightClientSnapshot
LightClientUpdate
```
- Type 2: Accessing BeaconState

The client needs to calculate committee assignment.
- The client needs to access the beacon state’s random mix and validator information.

```python
BeaconStateProof
```

Type 3: Get full blocks

- Need to get the full blocks
- The client does not need to know every blocks. It only needs to know the blocks associated with the attestation client’s assigned slots.

```auto
BeaconBlock
```

### Level 4: Limiting Case: Approaching Full Node

It would be ideal if a light weight beacon chain client could support all the API needs of a validator client. Furthermore, the same light weight client is also able to answer queries with regard to the current state of transient gossiped data. However, this view might not be realistic as some of these functionalities will fundamentally require the client to process large amount data.

These functionalities are not likely to be supported by light weight clients. However, it is still instructive to list out these classifications of functionalities to understand where should be the design boundary of light weight clients.

#### Supported APIs

1. Support validator client that are performing attestation aggregations, sync-committee duties, and block proposing.
2. Support a slasher.
3. Be able to answer queries about beacon-state as well as providing summarizing statistics about transient data. That is, the client would have to maintain up-to-date pools for all the gossip messages such as sync committee signatures, attestation, slashings, voluntary exists, etc.

## Replies

**ralexstokes** (2021-10-30):

Hi [@jinfwhuang](/u/jinfwhuang) ! I’m excited to see this series of posts and to see your interest w/ light clients.

I think your classification of levels 1 and 2 makes a lot of sense, but I wanted to clarify that while level 3 is an interesting idea it actually opens the door to a class of validator that is less than “fully validating” which erodes protocol security.

A “light” validating node erodes protocol security as if a given validator does not fully validate the blockchain they attest to it would be possible for a malicious staker to insert an invalid block into the chain. A “light” validator that just blindly attests to the rest of the chain outside of their slot would lend their support towards finalizing such a bad block, and an attacker with `1 / SLOTS_PER_EPOCH` of the stake could attempt this attack on average once per epoch. We eliminate this attack surface in the protocol by requiring validators to fully validate each block transition in the chain.

We also generally want validators to be as “uniform” as possible, as this simplifies protocol design and analysis. Having a separate class of “lightly” validating nodes complicates the protocol on this front.

---

**jinfwhuang** (2021-10-31):

There was a key mistake on describing the input data of Level 3. Terrence pointed out to me earlier already. The client has to get all the full blocks, instead of just assigned full blocks, to gain a global view of all the votes.

I wouldn’t completely dismiss the possibility of “light attestor”. If empirical evidences show that there are a large percentage of attestors uses centrally operated beacon chain endpoints because regular beacon chain clients are too expensive to operate, then it would beg the question on how to enable “light validator”. For example, if a beacon chain client is built only for for attestors and there is a “light=client-snapshot” gossip topic available, one could build a “attestor” only beacon light client by stripping down a regular beacon client. This client still participates in the core p2p network; however, it would have instant sync and lower resources consumption, and it would be a strict improvement over attesting against a centrally operated endpoint. I am not saying that we will build that. But the general decision framework that “light client for some purpose” should be explored.

