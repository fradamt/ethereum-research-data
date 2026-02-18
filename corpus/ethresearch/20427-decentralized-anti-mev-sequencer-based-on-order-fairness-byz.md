---
source: ethresearch
topic_id: 20427
title: Decentralized Anti-MEV sequencer based on Order-Fairness Byzantine Fault-Tolerant (BFT) consensus
author: 0x1cc
date: "2024-09-13"
category: Layer 2
tags: [mev, rollup]
url: https://ethresear.ch/t/decentralized-anti-mev-sequencer-based-on-order-fairness-byzantine-fault-tolerant-bft-consensus/20427
views: 370
likes: 2
posts_count: 3
---

# Decentralized Anti-MEV sequencer based on Order-Fairness Byzantine Fault-Tolerant (BFT) consensus

*by [KD.Conway](https://x.com/0x_1cc)*

## TL;DR

- This post introduces a Decentralized Anti-MEV Sequencer based on Order-Fairness Byzantine Fault-Tolerant (BFT) Consensus, a mechanism designed to counteract MEV and ensure transaction fairness.

## Order Fairness

**Received-Order-Fairness**[1]: with parameter 1/2 < 𝛾 ≤ 1 dictates that if 𝛾 fraction of honest nodes receive a transaction tx before tx′, then tx should be ordered no later than tx’.

## Introducing the Anti-MEV Sequencer

Our proposed solution is a **Decentralized Anti-MEV Sequencer** that leverages an **Order-Fairness Byzantine Fault-Tolerant (BFT) consensus** mechanism. This system provides:

1. Decentralization: Instead of a centralized sequencer, we will build a sequencer network with multiple nodes contributing to transaction ordering and batching.
2. Order-Fairness: Transactions are processed based on the time they were received by the nodes in the sequencer network, ensuring no one participant can manipulate transaction ordering.
3. Byzantine Fault Tolerance: The consensus protocol ensures the system remains operational even if some of the participants behave maliciously.

## Workflow

1. When a user wants to send a transaction on a layer 2 blockchain, they submit the transaction to the sequencer network.
2. The Order-Fairness BFT consensus is employed to determine the correct order of transactions. This guarantees that, even if a minority of nodes act maliciously, the system can still reach consensus on a fair transaction order.
3. After reaching consensus, the sequencer batches the transactions and submits them to the Rollup smart contract on Ethereum, where they are executed in the agreed-upon order.

For details on the system implementation of the Order-Fairness BFT consensus, please refer to the corresponding references at the end of this post.

## References

[1] Kelkar, Mahimna, et al. “Order-fairness for byzantine consensus.” *Advances in Cryptology–CRYPTO 2020: 40th Annual International Cryptology Conference, CRYPTO 2020, Santa Barbara, CA, USA, August 17–21, 2020, Proceedings, Part III 40*. Springer International Publishing, 2020.

[2] Kelkar, Mahimna, et al. “Themis: Fast, strong order-fairness in byzantine consensus.” *Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security*. 2023.

## Replies

**owizdom** (2024-09-17):

this is actually a genius scheme and has good direction if done correctly.

But here are my concerns

- Won’t this scheme just shift mechanics to the reordering of timestamps?
- there are centralizing forces due to latency games, making colocation a sophisticated strategy. This scheme is interesting but without more randomness and privacy, they fall apart and can be easily gamed or captured. So any plans on how to combat the privacy and randomness.

---

**0x1cc** (2024-09-20):

Thank you for your interest.

- As for the first concern, according to the definition of order fairness, if 𝛾 fraction of honest nodes receive a transaction tx before tx′, then tx should be ordered no later than tx’.Therefore, the minority of malicious nodes cannot manipulate the transaction order within a block. In this approach, shorter network latency may provide an advantage in terms of MEV.
- As for privacy, it is possible to utilize zero-knowledge proofs to create a privacy layer 2 similar to Zcash. For randomness, a straightforward method involves having the sequencer first batch the transactions into a block and then use a verifiable random function to generate a random number, which can be employed to permute the transaction order.

