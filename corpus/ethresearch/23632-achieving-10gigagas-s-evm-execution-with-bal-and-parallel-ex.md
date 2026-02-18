---
source: ethresearch
topic_id: 23632
title: Achieving 10GigaGas/s EVM Execution with BAL and Parallel Execution
author: Po
date: "2025-12-10"
category: Execution Layer Research
tags: [scaling]
url: https://ethresear.ch/t/achieving-10gigagas-s-evm-execution-with-bal-and-parallel-execution/23632
views: 390
likes: 11
posts_count: 6
---

# Achieving 10GigaGas/s EVM Execution with BAL and Parallel Execution

**By [Po](https://x.com/sanemindpeace), [Qi Zhou](https://x.com/qc_qizhou)**

> Special thanks to Toni and Dragan for feedback and review!

## Abstract

Ethereum is scaling L1 by gradually raising the block gas limit. However, increasing the gas limit substantially higher (e.g., [the 100× increase proposed by Dankrad](https://eips.ethereum.org/EIPS/eip-7938)) quickly hits hard limits—disk I/O and CPU execution speed. Prewarming and [EIP-7928 block-level access lists (BAL)](https://eips.ethereum.org/EIPS/eip-7928) remove most I/O read stalls, shifting the primary bottleneck to execution itself. Meanwhile, most clients still execute transactions sequentially, fundamentally capping throughput.

BAL ([an idea our team also explored two years earlier](https://docs.google.com/document/d/1FoW_iuIPoYAjxy-AUGr_vRbIK_Zon3XDAb6heS_GWL0/edit?usp=sharing)) unlocks perfect parallel execution, yet its performance ceiling remains unclear. To address this question, we built a pure-execution environment with:

- preloaded state, simulating an environment where relevant accounts, storage slots, and contract code are pre-resolved via BAL hints;
- pre-recovered tx sender, leveraging parallel sender recovery already implemented in most clients;
- omission of state-root computation, whose cost can be amortized for larger blocks.

Using this environment, we benchmarked per-transaction parallel execution with BAL. Our results show pure-execution throughput exceeding **10 GigaGas/s** on a modern 16-core commodity PC, whereas the current Reth client achieves only about 1.2 GigaGas/s under the same conditions. This indicates that EVM execution can scale an order of magnitude beyond current client baselines once the aforementioned bottlenecks are fully addressed.

---

# Where We Are Today

Ethereum is increasing its gas limit from 45 M to 60 M in the Fusaka upgrade. Suppose the gas limit were scaled by 100x, the resulting block would contain roughly 4.5 G gas. To keep validation time under three seconds, validators would therefore require at least 1.5 GigaGas/s of execution throughput. However, [Base’s public benchmarks](https://base.github.io/benchmark/#/latest) show that modern clients on commodity hardware reach a maximum of only about 600 MGas/s. This limitation is primarily due to sequential execution: although multi-core CPUs are available, existing clients process transactions serially, leaving most cores underutilized.

| Tx payload | Geth MGas/s | Reth MGas/s |
| --- | --- | --- |
| base-mainnet-simulation | 316.4 | 591.6 |

The gap between current performance (~0.6 GGas/s) and what 100× scaling requires (~1.5 GGas/s) is still substantial — which motivates our push toward fully parallel EVM execution.

---

# How We Did It

To study the ultimate parallel execution performance that BAL brings, we constructed a **pure-execution environment** by removing all unrelated non-execution parts, enabling us to measure the true upper bound of BAL-powered parallelism. Leveraging Rust’s no-GC design, fine-grained control over multi-thread scheduling, and Reth’s high performance, we modified the Reth client and used revm as the EVM execution engine for this experiment.

### Simplification for Pure Execution Emulation

- The entire chain state is loaded into memory beforehand (as we can batch I/O given BAL’s read locations).
- All transactions come with the sender already recovered (sender recovery can be fully parallelized ahead of time).
- No state root calculation and database commits are performed after execution (it’s a bottleneck, but not the main focus of this study).

### Engineering Work & Setup

- Modified the Reth client to support dumping full execution dependencies, including blocks, BALs, the last 256 block hashes, and pre-block states resolved from BAL read-set hints.
- Added an adaptor for Revm to load blockEnv, state, and txEnv, and to create a separate EVM instance per transaction.
- Parallelism granularity = per-transaction.
- Hardware: AMD Ryzen 9 5950X (16 cores), 128 GB RAM.
- Dataset: 2000 mainnet blocks (#23600500–23602500).
- Metric: Gas per second = total gas used / pure-execution emulation time.

Benchmark suite available here:

![:backhand_index_pointing_right:](https://ethresear.ch/images/emoji/facebook_messenger/backhand_index_pointing_right.png?v=14) https://github.com/dajuguan/evm-benchmark

---

# Results

Our evaluation began by aligning sequential performance for revm and then progressively introducing parallel execution. Analysis of parallel scaling revealed that the latency of the longest-running transactions forms the critical path that limits overall speedup. To alleviate this constraint, we simulated larger block gas limits, which unlocked substantial parallelism with BAL. With 16 threads and 1G block gas limit, pure-execution throughput reached **~14 GGas/s**.

## Baseline Alignment with Sequential Execution

We first attempted to reproduce Reth’s benchmark results. In a sequential run on mainnet data with the KZG setup preloaded, pure execution reached 1,212 MGas/s.

This sequential result serves as our reference point for all following experiments.

---

## Parallel Execution and Its Critical-Path Bottlenecks

To evaluate both the actual speedup and the effect of Amdahl’s law on transaction-level parallelism, we conducted per-transaction parallel execution experiments to quantify the impact of the longest-running transactions on the achievable speedup.

Detailed results are shown below (where “longest txs latency” is the total execution time of the longest-running transactions in each block):

| Threads | Throughput (MGas/s) | Longest TXs Latency | Total     Time |
| --- | --- | --- | --- |
| 1 | 1,258 | 6.06s | 33.47s |
| 2 | 2,460 | 6.04s | 17.12s |
| 4 | 3,753 | 6.10s | 10.71s |
| 8 | 4,824 | 6.00s | 8.73s |
| 16 | 5,084 | 6.04s | 8.29s |

Overall, the scaling results align closely with Amdahl’s law: although throughput increases with more threads, block execution time is constrained by the longest transaction, which accounts for about 70% of total execution time under 16 threads, capping the achievable speedup at roughly 5× instead of the ideal 16× for a 16-core machine. **This indicates that scalability is determined by per-block critical paths rather than raw compute capacity.**

This critical-path limitation can be mitigated by reducing the dominance of the longest transaction, for example, through [EIP-7825: transaction gas limit cap](https://eips.ethereum.org/EIPS/eip-7825) or by increasing block gas limit—the approach explored in this article.

---

## 7928 + Mega Blocks = Massive Parallelism

Since per-block critical paths limit concurrency, we experimented with higher-gas “mega blocks” to increase parallelism. To simulate this, we executed the transactions of multiple consecutive mainnet blocks, namely a mega block or a batch, in parallel, and then committed the state (noop in the experiment) only after all transactions in the batch had completed. This effectively aggregates multiple blocks into a single large execution unit.

### Parallelism Analysis Under Mega-Block Workloads

We first evaluated a batch of 50 blocks, simulating an average block gas usage of 1,053 M, across different thread counts. Full results are shown below:

| Threads | Throughput (MGas/s) | Longest TXs Latency | Total Time |
| --- | --- | --- | --- |
| 1 | 1,440 | 0.50s | 29.26s |
| 2 | 2,793 | 0.50s | 15.08s |
| 4 | 5,167 | 0.52s | 8.15s |
| 8 | 9,095 | 0.54s | 4.63s |
| 16 | 14,001 | 0.59s | 3.01s |

With such large blocks, the longest running transactions no longer dominate the critical path—they contribute less than 20% of total execution time under 16 threads. Throughput scales almost linearly with thread count: with 16 threads, we achieve 14 GGas/s, roughly a 10× speedup over sequential execution and close to ideal linear scaling. This is extremely encouraging. In our experiments, the one major remaining critical path is the `point_evaluation` precompile, which is not trivially parallelizable.

### Throughput Under Different Block Gas Usage

To evaluate how parallel execution scales with increasing block gas usage, we executed batches of consecutive blocks while varying the block batch size—the number of blocks grouped into a single mega block—thereby simulating different effective block gas usage.

| Threads | Block Batch Size | Avg. Block Gas (M) | Throughput (MGas/s) |
| --- | --- | --- | --- |
| 16 | 1 | 21 | 5,084 |
| 16 | 2 | 42 | 6,641 |
| 16 | 5 | 105 | 8,814 |
| 16 | 10 | 210 | 10,228 |
| 16 | 25 | 526 | 12,152 |
| 16 | 50 | 1,053 | 14,001 |
| 16 | 100 | 2,106 | 14,887 |
| 16 | 200 | 4,212 | 15,298 |

As the block gas usage increases, throughput continues to rise, but the incremental parallelism gains shrink from ~30% down to ~3% for each doubling of block gas. Once the batch size exceeds ~50 blocks (≈1,053M block gas), further increases in block gas yield only marginal additional throughput.

---

# Outlook

Our experiments show that combining **EIP-7928 with mega blocks** enables transaction execution to scale exceptionally well, achieving **14 GigaGas/s of pure-execution throughput** on a modern 16-core commodity processor. However, several open questions remain:

### 1. Sender Recovery

We excluded sender recovery from the pure-execution benchmark. In our experiment, enabling it cuts throughput by roughly 2/3, dropping to about 5 GigaGas/s under the mega-block configuration (1,053 M block gas).

Possible mitigation: GPU-accelerated sender recovery.

### 2. Gas Pricing Model

The `point_evaluation` precompile and sender recovery for 7702 transactions exhibit low gas-per-time efficiency. Their gas pricing may need to be revisited in the EIP-7928 era.

### 3. Transaction Gas Limit

Higher block gas limits may require retaining the current [transaction gas limit cap](https://eips.ethereum.org/EIPS/eip-7825) to maintain high parallelism.

### 4. Accelerating BAL Construction

Builder performance is expected to become the dominant bottleneck. Improving BAL building is essential to keep up with pure-execution throughput.

### 5. Optimizing State Commit

State commit is another major bottleneck. Speeding up state-root computation and optimizing trie commit are necessary to sustain high-throughput execution.

# Otherworks

We also explored different task scheduling strategies, e.g., prioritizing heavy-gas transactions by sorting them by gas used or gas limit, alongside the simple ordered-list scheduler (OLS), where transactions stay in natural block order, and each new transaction is assigned to the first available core. When applied to mainnet data, however, prioritizing heavy-gas transactions yielded only marginal performance improvements and did not significantly affect overall throughput.

## Throughput Under Different Scheduling Strategies

To evaluate the impact on overall throughput, we compared scheduling heavy-gas transactions first (by gas used or gas limit) against the OLS.

- results on normal blocks:

| Threads (Scheduler) | Throughput (MGas/s) | Longest Txs Latency | Total Time |
| --- | --- | --- | --- |
| 2 (gas used) | 2,726 | 5.70s | 15.45s |
| 2 (gas limit) | 2,728 | 5.68s | 15.44s |
| 2 (OLS) | 2,460 | 6.04s | 17.12s |
| 4 (gas used) | 4,401 | 6.09s | 9.57s |
| 4 (gas limit) | 4,321 | 6.18s | 9.75s |
| 4 (OLS) | 3,753 | 6.10s | 10.71s |
| 8 (gas used) | 5,455 | 6.15s | 7.72s |
| 8 (gas limit) | 5,426 | 6.13s | 7.76s |
| 8 (OLS) | 4,824 | 6.00s | 8.73s |
| 16 (gas used) | 5,643 | 6.03s | 7.47s |
| 16 (gas limit) | 5,531 | 6.05s | 7.62s |
| 16 (OLS) | 5,084 | 6.04s | 8.28s |

- results on mega blocks with 1053M average block gas:

| Threads (Scheduler) | Throughput (MGas/s) | Longest Txs Latency | Total Time |
| --- | --- | --- | --- |
| 2 (gas limit) | 2,732 | 0.53s | 15.42s |
| 2 (OLS) | 2,793 | 0.50s | 15.08s |
| 4 (gas limit) | 5,114 | 0.54s | 8.24s |
| 4 (OLS) | 5,167 | 0.52s | 8.15s |
| 8 (gas limit) | 9,082 | 0.57s | 4.64s |
| 8 (OLS) | 9,095 | 0.54s | 4.63s |
| 16 (gas limit) | 14,181 | 0.63s | 2.97s |
| 16 (OLS) | 14,001 | 0.59s | 3.01s |

[Toni’s analysis](https://ethresear.ch/t/modeling-the-worst-case-parallel-execution-under-eip-7928/23418/4) suggests that prioritizing heavy-gas transactions could outperform OLS by 20–80% in worst-case scenarios. In practice, however, using real mainnet data (representing the average case), the improvement is only around 10%, and scheduling by gas limit, gas used, or OLS shows minimal difference. On mega blocks, OLS performs nearly identically to gas-limit scheduling. These observations indicate that transaction scheduling is not the primary bottleneck; rather, the inherent distribution of transactions on mainnet forms the critical path.

## Replies

**bhartnett** (2025-12-10):

Interesting to see that using gasLimit for scheduling performs similar to gasUsed in these benchmarks. To use gasUsed for scheduling in practice we would need to increase the size of the BAL but since gasLimit is already available in each transaction, it sounds like using gasLimit scheduling might be a reasonable option for clients.

---

**unbalancedparenthese** (2025-12-10):

great work. we will try to replicate this with our execution client Ethrex ([GitHub - lambdaclass/ethrex: Minimalist, fast and modular implementation of the Ethereum protocol in Rust. L1 and L2 execution client.](https://github.com/lambdaclass/ethrex/)) and post our results.

---

**Nero_eth** (2025-12-11):

You’d do even better when you schedule by size of BAL filtered by tx, or by trying to guess the gas used from the balance diff and the gas price. The worst-case always stays the same though, and if all clients optimize using the same strategy, it’s easy to trigger a (collective) worst-case. Not saying this is necessarily bad. It might still be worth optimize for the avg, and since the worst-case doesn’t get worse while optimizing by doing reordering, it’s something we might see in clients - assuming clever ordering is practically worth it.

---

**ahamlat** (2025-12-11):

Great findings. Achieving almost linear scaling with thread count is very interesting. Apart from the longest transaction, have you found other wasted time related to executing in parallel ?

![](https://ethresear.ch/user_avatar/ethresear.ch/po/48/19766_2.png) Po:

> Meanwhile, current clients still execute transactions sequentially, fundamentally capping throughput.

Besu is actually doing optimistic parallel transaction processing, each thread receives a transaction a starts executing it in an optimistic way, based on OLS. I think other ELs are doing similar work.

It is interesting to see the results related to prioritizing heavy-gas transactions, we discussed this solution in the team but haven’t tried it. Even if it doesn’t improve, it is definitely worth trying it.

---

**Po** (2025-12-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/ahamlat/48/14781_2.png) ahamlat:

> Great findings. Achieving almost linear scaling with thread count is very interesting. Apart from the longest transaction, have you found other wasted time related to executing in parallel ?

Great work — changed to *most* clients. In our experiments, we found that `point_evaluation` is another time-consuming critical path. I expect other gas-heavy precompiles, such as `ecPairing` and `BLS12_PAIRING_CHECK`, will also become bottlenecks.

