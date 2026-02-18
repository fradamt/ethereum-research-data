---
source: ethresearch
topic_id: 21856
title: "Decentralized Random Block Proposal: Eliminating MEV and Fully Democratizing Ethereum"
author: malik672
date: "2025-02-28"
category: Proof-of-Stake
tags: [mev]
url: https://ethresear.ch/t/decentralized-random-block-proposal-eliminating-mev-and-fully-democratizing-ethereum/21856
views: 1259
likes: 3
posts_count: 8
---

# Decentralized Random Block Proposal: Eliminating MEV and Fully Democratizing Ethereum

Ethereum’s Proof of Stake (PoS) with Proposer-Builder Separation (PBS) mitigates Maximal Extractable Value (MEV) concentration but relies on centralized builders and relays, with 80% of blocks currently proposed by just two entities. This compromises decentralization and fairness. This research proposes a decentralized system where all Ethereum clients propose blocks using a shared random algorithm. By leveraging Byzantine Fault Tolerance (BFT), it eliminates block-level MEV, fully democratizes block proposing, and may accelerate propagation, while supporting Danksharding’s rollup future. Compared to PBS, it prioritizes trustlessness over optimization, offering a transformative shift for Ethereum.

#### 1. Introduction

Ethereum’s shift to PoS and adoption of PBS separates block proposing (validators) from building (specialized builders) to address MEV disparities. Yet, centralization persists: as of February 2025, approximately 80% of Ethereum blocks are proposed by just two entities—large builder-relay coalitions like Flashbots and their peers—concentrating power and profits. This undermines Ethereum’s decentralized ethos. MEV, the value extracted by reordering or censoring transactions, remains a challenge, with sophisticated actors dominating via PBS’s builder ecosystem.

This proposal introduces a decentralized random block proposal system. All Ethereum clients—not a handful of builders—construct blocks using a cryptographically random algorithm. Validators execute these blocks, achieving consensus via N ≥ 3T + 1 BFT. This eliminates block-level MEV, fully democratizes block proposing across Ethereum’s node network, and aligns with its trustless roots, while remaining compatible with Danksharding’s blob requirements.

#### 2. Proposed System

##### 2.1 Core Mechanism

- Block Proposal: Every Ethereum client (e.g., Geth, Nethermind) runs an identical random algorithm, seeded by RANDAO and a Verifiable Delay Function (VDF) from the validator set. It selects transactions and rollup blobs from the client’s local mempool, ensuring uniform blocks across honest nodes with aligned mempools.
- Broadcast: Clients relay their proposed block to validators simultaneously.
- Execution and Consensus: Validators execute the block, prune invalid transactions (e.g., double-spends), and compute a hash of the valid remainder. With N ≥ 3T + 1 (N = total validators, T = faulty), the majority hash wins if 2T + 1 agree, tolerating up to T dissenters (e.g., 33%).
- Rewards: Validators with the “correct” hash form a subset; a random subgroup is rewarded, keeping it fair and simple.
- Blob Integration: Clients randomly select up to the maximum blob capacity (e.g., 16 blobs at 125 KB each) alongside transactions, supporting Danksharding.

##### 2.2 Design Goals

- Eliminate Block-Level MEV: Random selection prevents profit-driven manipulation.
- Fully Democratize Proposing: Shifts block-building from two dominant entities to all clients.
- Enhance Speed: Parallel proposals may reduce slot times (e.g., 6-8 seconds vs. 12).
- Support Scalability: Handles rollup blobs for Ethereum’s future.

#### 3. Analysis

##### 3.1 MEV Suppression

Random selection ensures no entity can predict or control transaction order, eliminating block-level MEV (e.g., arbitrage, front-running). Unlike PBS, where builders extract and redistribute MEV, this system leaves mempool-level MEV as the only remnant—a smaller, less controllable slice.

##### 3.2 Decentralization

Currently, 80% of Ethereum blocks stem from two builder-relay coalitions, centralizing proposing power. This system flips that: block-building spreads to thousands of clients globally, fully democratizing the process. No single entity dominates—unlike PBS’s builder pool or a centralized mixer—and BFT mitigates mempool variance, ensuring robustness.

##### 3.3 Propagation Speed

Parallel client proposals and validator execution could shrink Ethereum’s 12-second slot to 6-8 seconds, outpacing PBS’s builder → relay → proposer → network flow. Mempool sync is key, but N ≥ 3T + 1 tolerates drift.

##### 3.4 Resilience

Randomness blunts DDoS—spam dilutes the mempool but doesn’t bias selection. Client redundancy eliminates central choke points, surpassing PBS’s relay risks. N ≥ 3T + 1 handles up to 33% validator faults (e.g., T = 100,000 of N = 300,000).

##### 3.5 Validator Simplicity

Validators execute, prune, and hash—lighter than PBS’s proposing and attesting. Random rewards within the correct-hash subset keep it straightforward.

##### 3.6 Scalability and Danksharding

Clients pack blobs randomly up to capacity (e.g., 1-2 MB per block), supporting rollups. Randomness doesn’t prioritize specific blob inclusion, potentially delaying rollup sequencing versus PBS’s optimization. Mempool sync scales with blob broadcasts—feasible with Ethereum’s P2P—though drift risks BFT limits if T grows.

#### 4. Comparison to PBS

| Metric | Decentralized Mixer | PBS |
| --- | --- | --- |
| MEV | Eliminated at block level | Redistributed via builders |
| Decentralization | High (all clients propose) | Moderate (80% by 2 entities) |
| Speed | Potentially faster (6-8s slots) | Slower (12s slots) |
| Resilience | Strong (client redundancy) | Good (builder failover, relay risk) |
| Simplicity | High (execution-only validators) | Moderate (propose + attest) |
| Scalability | Good (blob-compatible, less optimized) | Excellent (roadmap-optimized) |

#### 5. Trade-Offs

- Advantages: Eliminates MEV for unmatched fairness; fully democratizes proposing beyond PBS’s 80%-two-entity bottleneck; speeds up blocks; leverages client redundancy; keeps validators light.
- Drawbacks: Sacrifices gas-tip and rollup-specific blob optimization, potentially reducing L2 efficiency (this can be redesigned to favor L2 rollup-specific direction). Mempool sync must scale with blobs, risking consensus if drift exceeds T. Mempools may differ due to latency, so the initial block value V proposed by clients might not align. In this case, we select the most popular value V (via majority hash) or reselect at random from the proposed blocks, ensuring consensus persists.

#### 6. Conclusion

With 80% of Ethereum blocks currently controlled by two entities under PBS, this decentralized random block proposal system offers a radical fix. It eliminates block-level MEV, shifts proposing to all clients, and aligns with Ethereum’s trustless core while supporting Danksharding. PBS optimizes for rollup scalability, but this system prioritizes fairness and full democratization—crucial as centralization creeps in. It’s a trade-off: trustlessness over L2 precision. For an Ethereum valuing equity over efficiency, this wins; for one chasing scalability, PBS holds. Redesigning for rollup-specific optimization could bridge the gap, making it a versatile contender.

#### 7. Future Directions

- Simulate mempool sync with blob-heavy loads to test drift tolerance.
- Develop rollup-specific randomization to enhance L2 efficiency.
- Test consensus fallback (most popular V or random reselection) under high T scenarios.

## Replies

**chrmatt** (2025-03-03):

Interesting proposal! It seems a requirement is to have aligned mempools among honest validators. How do you want to achieve this? Local mempools are likely to keep changing continuously while new transactions are received.

---

**jonreiter** (2025-03-05):

agree with [@chrmatt](/u/chrmatt) that mempool synchronization is going to be a problem. maybe you can reorganize as a 3-step process where 1) set of tx gets locked 2) they are randomly reordered and 3) they are executed.

then you should be able to adapt a scheme like this to generate random orderings on-chain that cannot be predicted in advance and can be kept secret during a few rounds of whatever organizational work is needed: https://hal.science/hal-04176445/file/main.pdf

---

**malik672** (2025-03-05):

A good solution to this is to use FIFO queues, basically deterministic mempool ordering

---

**malik672** (2025-03-05):

this is a really good idea, mempool synchronization can be solved, we don’t need really to lock them, we need clients to order based on timestamps select a range and inside this range randomly select it

since it random selection everything will different, that’s why it wwould be a deterministic randomness

---

**chrmatt** (2025-03-05):

Using FIFO or timestamps of nodes would not work since different nodes at different geographic locations would receive the transaction at different times and in different orders. It seems this would require an additional consensus on the set of transactions to consider for the next block.

---

**jonreiter** (2025-03-06):

[@malik672](/u/malik672) to the extent your “mempool synchronization can be solved” means a deterministic scheme for everyone to agree the tx set: sorry flp blocks that. any solution will be randomized in the way consensus means for blockchain protocols.

from there [@chrmatt](/u/chrmatt) you can write a protocol where the randomzied consensus on the tx set also generates a randomization “seed” for ordering. it need not be a separate consensus. once you’ve got a random seed you can use the following scheme for ordering n tx:

hashes[1] = hash(seed)

hashes[i] = hash(hashes[i-1])

then order the tx by the size of the entries in hashes (or the last m digits maybe).

at this point you just need to battle collusion among the participants to set the “right” seed. if your random number protocol works this devolves to a proof-of-work style problem to block mev.

the downside is that everything becomes far less reliable, or far slower, when you cannot impose any ordering in advance.

that’s just a sketch but you can make this work if you give up on syncing the mempools and maintaining high throughput.

---

**malik672** (2025-03-06):

really need to study FLP again, that would technically be too slow, I’ve been thinking and I don’t think mempool synching is neccessary using set theory, we can just get the intersection of all Transaction from each clients and propose that to be executed concurrently instead

have some ideas but need to refine it first

