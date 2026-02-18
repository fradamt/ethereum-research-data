---
source: ethresearch
topic_id: 19020
title: Minimal fully recursive zkDA rollup with sharded storage
author: snjax
date: "2024-03-16"
category: Layer 2 > ZK Rollup
tags: []
url: https://ethresear.ch/t/minimal-fully-recursive-zkda-rollup-with-sharded-storage/19020
views: 2620
likes: 4
posts_count: 11
---

# Minimal fully recursive zkDA rollup with sharded storage

## Current zk rollup state

zkRollups scale execution efficiently, but publish all blocks at L1. This is not scalable for storage and forbids recursive rollups: if we deploy a rollup on a rollup, we need to publish all the blocks of the inner rollup on the outer rollup, and the outer rollup will publish all its blocks on L1.

![native rollup](https://ethresear.ch/uploads/default/original/2X/e/e04f5c7f84d40add7840afa6a1f5fdc05bbc30af.svg)

There were some attempts to solve this problem, like validiums, but they are weak on both decentralization and security (2 of 3 in Vitalik’s trilemma).

## Existing improvements in unlocking data availability and decentralized storage

### Chia

Chia introduced a novel consensus algorithm called Proof of Space and Time (PoST), which provides a more decentralized and energy-efficient alternative to Proof of Work (PoW): Proof of Space-Time (PoST). PoST is a consensus algorithm that uses storage space as a resource to secure the network.

The current capacity of Chia Network is 33 EiB.

### EthStorage

Ethstorage is replication-based DA and storage, managed by a smart contract.

## Our results

In our [research draft](https://ethresear.ch/t/blockchain-sharded-storage-web2-costs-and-web3-security-with-shamir-secret-sharing/18881) we propose a solution for storage and data availability, friendly to zk rollups and unlocking new scalability opportunities.

### Sharding instead of replication

It is proposed to use k of n threshold data representation. So, any k numbers from the source file are transformed into n numbers. And any k of these n numbers can restore the source k numbers. This is called Shamir’s Secret Sharing.

This approach allows us to utilize storage 10-20 times more efficiently than the replication-based approach, according to our modeling.

Also, it gives us better protection from physical-level attacks, like target node destruction.

### Unlimited horizontal scalability

We propose to use a 2-level nested rollup structure (below we will describe, why it is possible). The top-level rollup manages participants of low-level rollups and mixes them to prevent the accumulation of malicious participants in one low-level rollup. Low-level rollups manages the data, stored in the nodes.

### Polynomial commitments everywhere

We propose to use Merkle trees on the top level of database. However, the minimal structure is a polynomial commitment to a cluster of data. So, it is very friendly to rollups, because we can use the same polynomial commitment to represent the rollup’s block.

Also, out of the box we have data availability oracle (just provide random polynomial lookup on the commitment) and all linear algebra we needed for sharding.

### Data mining

Nodes can use the data for mining, like in Chia. And the result of mining is zero-knowledge proof of data availability.

The complexity of storage is leveled, so it is the same complexity to store random data or zeros.

Nodes can join to network with trustless zk proof of their capacity.

## Bring it all together

ZK Rollups usually publish on-chain proof of execution and data of the block.

But our data availability and proof of storage are zk. So, we can merge it all together and publish the proof of execution and data availability and storage in one single ZK proof.

It unlocks the deployment of rollups on rollups, and the rollups on rollups on rollups, and so on. And way to transform Web2 into Web3.

Also, we can prevent the bloating of the blockchain: if we publish the snapshot state of the rollup, previous history could be removed.

![zkDA rollup](https://ethresear.ch/uploads/default/original/2X/e/e3e434b0992b133f32c8c4a33bcf390e04e571b6.svg)

## Some economics

On 1st Jan 2024 cost of storage, 1GiB was:

- Ethereum $1.8M
- EthStorage $10k
- Celestia $300
- Near $10

Based on [Hetzner sx294](https://www.hetzner.com/dedicated-rootserver/sx294/) with 8 blowup factor (what we need for >100 bits of security), the annual cost of storage 1GB is $0.15 usd.

The cost will be lower on specialized rigs.

## Call for discussion and feedback

We believe our proposed solution has the potential to significantly improve the scalability and efficiency of zk rollups and upgrade Web2 to Web3. However, we acknowledge that this is still a research draft and there may be challenges or considerations we haven’t fully addressed.

We welcome discussion, feedback, and constructive criticism from the community. If you have insights, ideas, or see potential issues with our approach, please share them.

## Replies

**wizicer** (2024-03-19):

Could you elaborate the difference between your proposal and Filecoin?

---

**snjax** (2024-03-19):

The key differences between the minimal fully recursive rollup proposal and Filecoin are:

1. Sharding vs replication: The proposal uses Shamir’s Secret Sharing (RS correction codes, this is the same in this case) to split data into shards, allowing 10-20 times more efficient storage utilization compared to Filecoin’s replication approach.
2. Rollup-friendly and recursive: The proposal is designed to be zkSNARK-friendly, allowing data availability proofs and storage proofs to be merged with rollup state transition proofs into one succint proof. This enables recursive rollups, where rollups can be deployed on other rollups in a nested manner, with no data floating up to L1. Filecoin is not designed for this.
3. Built-in blockchain-level security: The proposal provides storage with blockchain-level security out of the box (<1e-30 probability to lose the data), without users needing to manage data replication and storage provider selection directly. In contrast, Filecoin is more akin to decentralized storage-as-a-service, where users have direct control over who stores their data and how many replicas are made.

---

**Mirror** (2024-03-24):

Please provide more information on the issues related to decentralized ZKP generation. This is also a common pitfall in ZK solutions, and I would like to learn more.

---

**snjax** (2024-03-24):

ZK proofs are not generated in a decentralized way in this solution. Each participant on the network generates the proofs on his own. But you may include zk proofs of other participants in yours with recursive snarks, if you needed.

---

**Mirror** (2024-03-25):

What is the expected duration for the common proof generation? What specific models of devices are used in the experiment? Just considering the feasibility and universality of this approach.

---

**snjax** (2024-04-01):

Our novel result is not about new proof generation machines. So it is the same as for existing rollups.

If we are speaking about data-specific things, it is possible to reach about 1Gbit/s on modern CPUs (I tested on 7945HX and M2) for making polynomial commitments of the data, important for proofs.

So, if you use small dedicated servers on 1Gbit/s connection, it is working. If you utilize it, you will utilize all your CPU also.

---

**Wanseob-Lim** (2024-04-10):

Hey Igor please correct me if I’m not understand correctly.

So, the data availability will be committed on the layer-1 smart contract as an oracle data and it will include its zk proof for its security level for the data availability, which is PoST you’re mentioning here.

And that zk proof is a “recursive-able” proof so zk rollups can inherit them recursively to their n-th layer.

Is this correct?

---

**snjax** (2024-04-10):

Yes.

We can publish the hash on the top level, which is the state of zk oracle. Rollups can use this zk oracle to verify that the data is available and stored.

This oracle could be completely permissionless, based on PoST mining inside (so, if we have 100 EiB network, somebody needs one more 100 EiB network to fork it).

---

**billypham09** (2024-04-17):

This looks cool. I am curious how do you measure the proof generation capacity of a node? Do you rely on the node to advertise its capacity or do you measure the performance of mining activity?

---

**snjax** (2024-04-17):

We benchmarked, how much data is possible to represent as polynomial commitment per second.

