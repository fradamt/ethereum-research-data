---
source: ethresearch
topic_id: 7787
title: Parallelilizing EVM through end-of-the-block virtual transactions
author: kladkogex
date: "2020-07-31"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/parallelilizing-evm-through-end-of-the-block-virtual-transactions/7787
views: 4397
likes: 17
posts_count: 5
---

# Parallelilizing EVM through end-of-the-block virtual transactions

Currently EVM processes transaction sequentially.  While for the main net it is not a big deal since the blocks come slowly anyway, it is a problem for us at SKALE.

One would think that if transaction X modifies the state of a contract A and transaction Y modifies the state of contract B, then X and Y could be processed in parallel.

The problem is both A and B may call contract C. This couples the state of A and B and prevents parallel processing.

Here is how this can be solved:

When A wants to call C, instead of calling it directly, it creates a virtual transaction Z at the end of the block. This transaction calls C.

When all the original transactions are processed,  there is a set of virtual transactions at the end of the block S1.   These transactions are then ordered by hash, and processed as a virtual block B1.   This can lead to another vritual block B2, which is in turn processed by EVM.

Ultimately the processing converges, creating an empty virtual block.

Note, that at every processing stage figuring out parallelism is easy. Since there are now subcontract calls, two transactions that call two different contracts and have two different senders can be processed in parallel.

## Replies

**zmanian** (2020-07-31):

There is a ton of prior art on these designs.

like https://github.com/ethereum/EIPs/issues/648 and

https://arxiv.org/pdf/1901.01376.pdf

It’s mostly a social coordination problem of getting multiple users of EVM on BFT platforms to agree on an extension to the EVM spec rather than a research/design problem at this point.

---

**barryWhiteHat** (2020-07-31):

I was under the impression that the limiting factor is not compute but disk read and write. So these approaches were not attractive because it does not address the root problem which is loading the state so you can change it.

See from https://github.com/ethereum/EIPs/issues/648#issuecomment-310695339 on for discussion

---

**AlexeyAkhunov** (2020-08-01):

I am hoping that these kind of things will become interesting if we manage to introduce ReGenesis and limit the active state to something that can fit into RAM, and then we will have some interesting EVM optimisation problems, looking forward to it.

Having said that, we are already coming close to these bottleneck in some special cases, like running transactions in bulk when performing turbo-geth sync on a machine with the decent amount of memory. Since our representation of current State is about 50Gb, and the active part can actually fit into RAM on 32 Gb RAM machine, we are already getting to the point where we see bottlenecks in golang’s garbage collect, or in Jumpdest analysis etc.

---

**laurentyzhang** (2021-02-28):

If I understand it correctly, you want to divide the execution into multiple phases.   When executing A, as soon as the VM detects C is about to be invoked by A, hung A up and create a new virtual transaction  Z then attached it to the end of the block ?  This applies to all the transactions and when all the original transactions have been processed, start to process virtual transactions. Correct ?

**Questions:**

1. What happens to A after creating a virtual transaction  Z ? continue processing ? Revert ?
2. If it would continue, then what if the rest of A after creating  Z is dependent on some return value of C ? At this point, C hasn’t been executed yet.
3. If simply reverted A, there is no need to generate a virtual transaction just simply move the transaction A to a queue and execution all the transactions in the queue in sequential order afterwards.

It is not the smart contracts causing problems. It only has to do with state transitions. In fact,

A -> C and B -> C can be processed in parallel as long as C doesn’t change any states,  if C is a read-only LUT, then arbitrary number of transactions can access it without any problem.

