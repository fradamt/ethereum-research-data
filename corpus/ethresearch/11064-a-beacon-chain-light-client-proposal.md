---
source: ethresearch
topic_id: 11064
title: A Beacon Chain Light Client Proposal
author: jinfwhuang
date: "2021-10-21"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/a-beacon-chain-light-client-proposal/11064
views: 1574
likes: 5
posts_count: 2
---

# A Beacon Chain Light Client Proposal

# A Beacon Chain Light Client Proposal

A beacon chain light client could be built in many different ways. A light client could be [classified](https://ethresear.ch/t/beacon-chain-light-client-classification/11061) by its API functionalities. A light client could use [different networking](https://ethresear.ch/t/beacon-chain-light-client-networking/11063) layers as its input data sources.

Any proposed light client implementation needs to define both of these components at a minimum. The supported APIs is the output of the client, and the networking environment is its input data.

Here, I am proposing a light client implementation that goes a step further than the minimum light client described in the [altair consensus-spec](https://github.com/ethereum/consensus-specs/blob/a20f6f7b5f40292c2a864337336bff74ae318354/specs/altair/sync-protocol.md). The proposed client aims to allow queries into the beacon state. The input data sources uses p2p networks that follow the specifications of [portal-network](https://github.com/ethereum/portal-network-specs/).

## Supported APIs

Here is a representative subset of APIs the client intends to support.

```auto
/eth/v1/beacon/headers
​/eth​/v1​/beacon​/states​/{state_id}​/root
​/eth​/v1​/beacon​/states​/{state_id}​/finality_checkpoints
​/eth​/v1​/beacon​/states​/{state_id}​/validators
​/eth​/v1​/beacon​/states​/{state_id}​/validators​/{validator_id}
​/eth​/v1​/beacon​/states​/{state_id}​/validator_balances
​/eth​/v1​/beacon​/states​/{state_id}​/committees
​/eth​/v1​/beacon​/states​/{state_id}​/sync_committees
```

## P2P Portal Networks

The input data could be put into two categories. The first category is the information required to move the block headers forward. The second category is the information required to build out part of the beacon state.

Note: We should write these networks as part of the portal-network specs.

#### Updating Headers

- gossip network: bc-light-client-snapshot

Data type: LightClientSnapshot

gossip network: `bc-light-client-update`

- Data type: LightClientUpdate

### Beacon State

- dht network: beacon-state

content_id: sha256(root | leaves_general_indices)
- content: root, leaves_general_indices, leaves, proof

## Replies

**Dumi2000** (2022-06-08):

Did you have any luck with this? I also want to test with a LightClient but could not find any working implementation yet.

