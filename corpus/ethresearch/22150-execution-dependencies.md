---
source: ethresearch
topic_id: 22150
title: Execution Dependencies
author: Nero_eth
date: "2025-04-14"
category: Sharding
tags: [parallelization]
url: https://ethresear.ch/t/execution-dependencies/22150
views: 1634
likes: 12
posts_count: 9
---

# Execution Dependencies

# Execution Dependencies

> Thanks to Julian, Ignacio and Ben for feedback and review.

**TL;DR:** Most Ethereum blocks are highly parallelizable. On average, 60–80% of transactions are completely independent, and dependency chains are shallow. However, a small number of blocks have heavy entanglement and long critical paths, limiting parallelism — especially near the top-of-block (ToB), where MEV searchers compete for order.

Explore some transaction dependency graphs on [dependency.pics](https://dependency.pics/).

---

## Transaction dependency graphs

For the following, the goal is to quantify how dependent transactions within blocks are on one another, guiding us in understanding how well blocks are parallelizable.

> The dataset includes blocks from 22,195,599 to 22,236,441. It focuses specifically on storage-related dependencies, while other potential sources of dependencies—such as account balances—were intentionally excluded.

For each block B, we define a directed graph:

G_B = (V_B, E_B)

Where:

- Vertices:
V_B = \{ t_1, t_2, \dots, t_n \} represents the transactions in B, ordered by their transaction indices.
- Edges:
For any t_i, t_j \in V_B with i  Play around with such graphs yourself: dependency.pics

The **most dependent transactions** are generally found in the **top of the block** (ToB), a space that is particularly attractive for MEV searchers and builders.

[![histogram_tx_index (1)](https://ethresear.ch/uploads/default/optimized/3X/3/8/38a69ec32457e63af73ce84a789205629f021e7e_2_690x206.png)histogram_tx_index (1)1000×300 13.7 KB](https://ethresear.ch/uploads/default/38a69ec32457e63af73ce84a789205629f021e7e)

Furthermore, we observe substantial differences between local builders and MEV-Boost builders, with the former typically building blocks with fewer dependencies. Locally built blocks, on average, have **~14 transactions** with dependencies on prior transactions in the block. For MEV-Boost builders, it’s **~40 transactions** per block on average.

[![result_df (5)](https://ethresear.ch/uploads/default/optimized/3X/0/a/0aca12648b1c131f9bf595badbb8ab50336f22a1_2_690x134.png)result_df (5)6477×1260 397 KB](https://ethresear.ch/uploads/default/0aca12648b1c131f9bf595badbb8ab50336f22a1)

> Of course, the general trend towards the blocks of local builders getting smaller and smaller over time (more info here) also plays into that.

Finally, when looking into the **most frequently accessed contract and storage slot combinations**, we see several prominent projects among the top positions, including stablecoins, WETH, Uniswap, and MetaMask. Consistent with [findings from a previous analysis](https://ethresear.ch/t/block-level-warming/21452), we again identify the contract `0x399...` as the most frequently read contract (highest number of SLOADs). For further details and an explanation of this behavior, please refer to the linked analysis. Specific storage slots in contracts like WETH, USDC, or USDT experience reads and writes in nearly every block.

[![avg_slot_usage (3)](https://ethresear.ch/uploads/default/optimized/3X/5/3/537288446f4ea94a02c73ab9ee7beb8f18dd1f18_2_690x345.png)avg_slot_usage (3)1000×500 38.2 KB](https://ethresear.ch/uploads/default/537288446f4ea94a02c73ab9ee7beb8f18dd1f18)

## Further readings

- Parallel block building | Flashbots Writings
- https://www.scs.stanford.edu/24sp-cs244b/projects/Concerto_Transaction_Parallel_EVM.pdf
- https://www.microsoft.com/en-us/research/wp-content/uploads/2021/09/3477132.3483564.pdf
- Speeding up the EVM (part 1) | Flashbots Writings

## Replies

**Kapol** (2025-04-14):

Does this mean that if I pay large enough fees, I can draw my own shape?

---

**emiliano-conduitxyz** (2025-04-15):

Great writing [@Nero_eth](/u/nero_eth)

Thats a good signal to start exploring pipelining and speculative execution

Have worked a playbook some while ago for rollups that can be used in general for this kind of analysis

Sharing ‘here - x dot com/emilianobonassi/status/1782813438491639990’ (cannot include links for some reason)

---

**jeffchen006** (2025-04-15):

Great post!

Other execution dependencies can also come from:

1. Contract bytecode (e.g., via self-destruct + create/create2).
2. Account balances (ETH/token transfers).

Might be worth considering in future analyses.

---

**Nero_eth** (2025-04-15):

Right yeah. Ignored them here for simplicity, expecting that the nr. of dependencies based on balances and code to be rather negligible compared to storage, but agree, definitely worth considering!

---

**kladkogex** (2025-05-02):

It is an interesting discussion, but I am not sure what is the practical problem being solved

In general, EVM execution is currently not a bottleneck. I have a C++ implementation running on my laptop that achieves 1,500 transactions per second (TPS) for EVM execution.

The real bottlenecks are state database updates and network throughput. Until Ethereum reaches over 1,000 TPS, discussing EVM parallelization makes little sense, as it adds significant complexity.

If, 20 years from now, Ethereum aims to exceed 1,000 TPS, the most effective way to speed up the EVM would be through Just-in-Time (JIT) compilation.   You could also do agent-based programming which makes parallelization easy. You could specifically introduce parallel primitives such as vector operations.

---

**Po** (2025-05-06):

Yes, execution is not the bottleneck at the moment. In Geth, I/O reads and writes currently account for nearly 70% and 4% of the execution time, respectively. However, the author Toni is also working on block-level access list to help address the I/O issue.

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/9/9990ff4be22e71d8b36f26f9a703efb9c4b3eb6c_2_690x482.png)image932×652 43.9 KB](https://ethresear.ch/uploads/default/9990ff4be22e71d8b36f26f9a703efb9c4b3eb6c)

---

**Po** (2025-05-20):

It’d be great to identify the maximum critical path length for txs depending on contract creation to better support BAL

---

**Po** (2025-05-20):

FYI, with the next Geth release(1.15.12), the metric would be updated — I/O reads account for ~13% of the total block processing time.

