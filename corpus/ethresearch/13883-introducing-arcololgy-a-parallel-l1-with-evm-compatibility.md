---
source: ethresearch
topic_id: 13883
title: Introducing Arcololgy, a parallel L1 with EVM compatibility
author: laurentyzhang
date: "2022-10-08"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/introducing-arcololgy-a-parallel-l1-with-evm-compatibility/13883
views: 2304
likes: 2
posts_count: 6
---

# Introducing Arcololgy, a parallel L1 with EVM compatibility

**What is Arcology**

Arcology is an L1 blockchain with capability to process transitions in full parallel. Conceptional, you can think Arcology as APTOS with EVM compatibility. In fact, Arcology has a very different parallel execution design and can do more than APTOS.

**Parallel Processing**

Conventional, blockchains process transactions in sequential order. Transaction only be processed one by one. The deterministic nature of blockchains makes most common synchronization mechanisms unusable. This is a major scalability bottleneck.

**How we did it**

In Arcology, transactions are processed in full parallel. VMs are wrapped into transaction execution units called EUs, which basically take in transactions and spit out some state transitions (or delta writes in APTOS terminology). Below is the whole process:

- All the EUs are running in full isolation and aren’t aware of each other
- Different EUs are running in different threads
- All the EUs are executing against the latest clear states
- State changes generated during the execution will be temporarily cached
- A module called Arbitrator will be responsible for detecting potential conflicts among these state transitions.
- Only the nonconflicting transitions will be committed to the StateDB. The transactions calling state conflicts will be reverted.

Arcology can take full use of the processing power of the hosting server. The more threads available, the faster it can run.

**Cluster Computation**

In case you are running out all the threads on a single machine.

Arcology can further expand the parallel processing power to multiple machines. For example, you can connect two machines with 64 cores on each and they will work just like one with 128 cores.

**Scalability**

There is no theoretical limit on how fast Arcology can go, it scales up pretty linearly with the number of processors available. As a rule of thumb,250~300TPS / core running complex smart contracts is reasonable in a real-life scenario with all the bells and whistles attached.

An execution-only test (what APTOS does) can be 10 times faster.

[www.arcology.network](http://www.arcology.network)

## Replies

**MicahZoltu** (2022-10-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/laurentyzhang/48/5537_2.png) laurentyzhang:

> Only the nonconflicting transitions will be committed to the StateDB. The transactions calling state conflicts will be reverted.

This strategy feels fairly hostile to applications that receive a significant amount of usage (e.g., Uniswap) as it essentially means only one transaction for that app can go through at a time and the rest fail just because they happened to be at the same time and were selected against (randomly?).

Separately, it seems that you need to detect not just state changing conflicts, but also when one thing writes to state and another reads from it.  If a transaction conditionally changes A based on the state of B, and another transaction conditionally changes B based on the state of A, then you must have one happen before the other, they cannot be parallelized even though they don’t *mutate* the same same state.

---

**laurentyzhang** (2022-10-09):

Good questions. These are common problems of all parallelization strategies on blockchain.

Question 1:

1. Scheduler:
The scheduler receives all the transactions from the transaction pool and find the best execution plans possible. Contracts causing too many conflicts will be labelled as serial only.  There is a dedicated EU for these contracts.
2. Concurrent Library
Not all contracts are fully parallelable without some modifications. That is where the concurrent library （wrapped in solidity) come in handy

Concurrent containers
3. Defer calls (Fork / Join model）

**Question 2**:

There are a few things that I didn’t cover in the post above. The whole concurrency framework is much more complex than I described.

|  | Read | Write | Delta Write |
| --- | --- | --- | --- |
| Read | OK | Conflict | Conflict |
| Write | Conflict | Conflict | Conflict |
| Delta Write | Conflict | Conflict | OK |

Transaction #1 read state A and then changed the state B and transaction #2 read state B then changed state C. Based on the rules above, they are classified as conflicting. No state inconsistency will ever happen.

---

**ivan-homoliak** (2022-10-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/laurentyzhang/48/5537_2.png) laurentyzhang:

> As a rule of thumb,250~300TPS / core running complex smart contracts

What is the size of the network for this TPS and how does this number change with the number of nodes in Arcology’s consensus protocol?

---

**laurentyzhang** (2022-10-14):

As long as the bandwidth allows

1. Similar to APTOS, Arcology uses Meta Blocks only, which don’t contain any transaction bodies but the short hashes of transactions. This design cuts down the block sizes by 95% at least. It will save a lot of bandwidth.
2. Arcology allows parallelization between the proposer and the validators, similar to APTOS, which basically means as soon as the proposer has successfully reaped a list of transactions, it will immediately propose a block using the transaction hashes and broadcast it to other validators.

So, the proposer and validators can start processing transactions almost simultaneously. No need for validators to wait for the proposer to finish transaction processing first.

In case you are running out of bandwidth on a single machine, try the cluster deployment mode. You can start multiple dedicated P2P servers and bind their bandwidth together. This feature is extremely useful when running nodes on cloud.

[![image](https://ethresear.ch/uploads/default/optimized/2X/a/afd565c8c69cc1b04ea0f6d6b7c5803507f8913c_2_690x309.png)image818×367 34.2 KB](https://ethresear.ch/uploads/default/afd565c8c69cc1b04ea0f6d6b7c5803507f8913c)

---

**ivan-homoliak** (2022-10-15):

(1) Regarding TPS and the number of nodes, I wanted to see some concrete numbers from experiments, etc.

(2)

![](https://ethresear.ch/user_avatar/ethresear.ch/laurentyzhang/48/5537_2.png) laurentyzhang:

> Similar to APTOS, Arcology uses Meta Blocks only, which don’t contain any transaction bodies but the short hashes of transactions. This design cuts down the block sizes by 95% at least. It will save a lot of bandwidth.

At the first glance exluding txs bodies from block proposal seems as a dangerous practice to me. E.g., the producer of the winning block (miner) may intentionally create a tx that only he knows the body, then gosip the block and let other nodes stuck with the execution of the missing tx. Anyway, let’s say that you could fix it as the part of the consensus protocol that would accept the winning block only when it contains txs hashes to all known txs’ bodies that were delivered later in whatever way. This would imply that the processing of txs would have to be delayed until their bodies are delivered, which further implies that in the next round (i.e., block) we do not know yet what txs we can accept as valid since we do not know the resulting state (updated balances, storages) from the last round. So, this indirectly indicates to me that we cannot postpone the delivery of txs’ bodies coz they are needed for the state update. Therefore, I’d say the only viable solution is to include full txs within the gossiped blocks. Do I miss something?

