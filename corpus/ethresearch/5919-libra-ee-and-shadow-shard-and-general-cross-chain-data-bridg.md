---
source: ethresearch
topic_id: 5919
title: Libra EE and Shadow Shard (and general cross-chain data bridging)
author: loredanacirstea
date: "2019-08-03"
category: Sharded Execution
tags: [execution-environment]
url: https://ethresear.ch/t/libra-ee-and-shadow-shard-and-general-cross-chain-data-bridging/5919
views: 2007
likes: 3
posts_count: 1
---

# Libra EE and Shadow Shard (and general cross-chain data bridging)

***This is a high-level idea, posted for initial feedback.***

The idea of adding Libra’s VM as an execution environment (EE) to Ethereum 2.0 has already been proposed before (e.g. https://twitter.com/protolambda/status/1141010821939650560), however, we are proposing something more: a Libra EE and a read-only shadow shard that is kept in sync with the Libra chain.

In addition, high-frequency data from Libra (or any other chain) can be brought into the [Master Shard](https://ethresear.ch/t/a-master-shard-to-account-for-ethereum-2-0-global-scope/5730). Data compatible with [dType](https://ethresear.ch/t/dtype-decentralized-type-system-on-ethereum-2-0/5721) can be cached in the Master Shard under dType and be available to other shards in an Ethereum-compatible format.

## As Bulk Oracle

Oracles are meant to bring off-chain data into the EVM on-demand. The Libra shadow shard will act as a bulk oracle, where “off-chain” data is actually made available in bulk, in a shard.

There are proposals to migrate the Eth1 chain to an Eth2 shard, by using the Eth2 consensus mechanism and a network of Relayers, which hold Eth1 chain data.

The current proposal is somewhat different: it does not require consensus for adding blocks - this is handled by Libra itself. However, it does require that block hashes are stored in Eth2 and that their existence is verified in the Libra chain. This can be extended to any blockchain that contains data of interest for Ethereum users.

Therefore, one cannot send Libra transactions to the Libra shadow shard. It is read-only.

If `ShardX` contains a smart contract that needs to read Libra data, it will retrieve it from the Libra shadow shard. The user can also provide a Libra block hash that he knows to contain the expected state transitions and this hash will be checked to see if it exists in the shadow shard, along with the actual data verification.

There have been talks for the Ethereum Foundation to enter the Libra Association. In this case, having an EF Libra validator could help secure this unidirectional bridge between Libra and the shadow shard.

## Synergy with the Master Shard

Libra block hashes can be stored on the Master Shard. These will act as verification that a certain block has indeed been included in the Libra chain.

In addition, the Master Shard can be a cache for high-frequency, cross-shard Libra data reads.

## Synergy with dType

dType can have support for Libra types (resources) and data inside Eth2. The Libra resources that are highly used can also be cached on the Master Shard in dType format, making them directly available to other shards. Both type definitions and data can be cached.

dType is, therefore, a way of standardizing non-Eth2 chain data, for the purpose of creating rich data bridges between previously incompatible shards, with different EEs. You will be able to use shard resources in a common format, without needing to understand the intricacies of each shard.

Therefore, we can have two independent ways of caching Libra on the Master Shard: directly, or through a dType-like system.

## From Oracle to Executor

If needed, we can transform this read-only Libra shard, from an oracle to an actual executor of new transactions.

This can happen if the Libra Association will not be able to run Libra due to regulatory issues or if the Association will run into consensus problems - of any kind.

We should be prepared to integrate Libra, especially if it will contain high-value data for the public or if it brings new users to Eth2.
