---
source: ethresearch
topic_id: 23920
title: Reducing BAL Size with 10 GigaGas/s EVM Throughput in the Presence of I/O
author: Po
date: "2026-01-22"
category: Execution Layer Research
tags: [scaling]
url: https://ethresear.ch/t/reducing-bal-size-with-10-gigagas-s-evm-throughput-in-the-presence-of-i-o/23920
views: 88
likes: 2
posts_count: 1
---

# Reducing BAL Size with 10 GigaGas/s EVM Throughput in the Presence of I/O

**By [Po](https://x.com/sanemindpeace), [Qi Zhou](https://x.com/qc_qizhou)**

TL;DR

- We evaluate three BAL designs—full BAL, batched I/O BAL, and parallel I/O BAL—with different trade-offs between execution throughput and BAL size.
- We examine how closely the lowest-overhead design, parallel I/O BAL, can approach the throughput of Full BAL.
- Parallel I/O BAL achieves ~10.8 GGas/s versus ~13.9 GGas/s for full BAL, providing 78% of the throughput with only 33% of the full BAL size.

Block-level access lists ([BAL](https://eips.ethereum.org/EIPS/eip-7928)) enable paralism including parallel I/O and parallel execution, by explicitly encoding all accounts and storage accessed during block execution in the block space, along with their post-execution values. In [our previous article](https://ethresear.ch/t/achieving-10gigagas-s-evm-execution-with-bal-and-parallel-execution/23632), we studied the parallel execution performance of full BAL, which includes post-transaction state diffs and pre-block read keys and values. On a 16-core commodity machine, we achieved approximately 15 GGas/s pure parallel execution throughput in a mega-block setting.

However, this study omits two dominant constraints: I/O and large BAL overheads. In a non-prewarming scenario, I/O accounts for roughly 70% of total block processing time. Although BAL enables parallel disk reads, the effectiveness of BAL-enabled parallel I/O might depend on how much read information is embedded in the BAL itself. More detailed read hints may increase I/O parallelism, but they also inflate BAL size, directly impacting network bandwidth and storage costs. As a result, BAL admits several design variants, each representing a different trade-off between achievable parallism and BAL size. Based on the precision of read hints, the main designs are: full BAL, batched I/O BAL, and parallel I/O BAL.

| Name | Details | Parallel Execution | Parallel I/O | BAL Size (RLP-encoded)* |
| --- | --- | --- | --- | --- |
| Full BAL | Post-transaction state diffs & pre-block read keys and values | Per-transaction | Per-hint (for verification only) | 213 kb |
| Batched I/O BAL | Post-transaction state diffs & pre-block read keys | Per-transaction | Per-hint | 110 kb |
| Parallel I/O BAL | Post-transaction state diffs | Per-transaction | Per-transaction | 71 kb (lowest, 33% of Full BAL, 64% of Batched I/O BAL) |

> *Sampled from blocks #23,770,000–23,771,999

Ideally, we would like to maximize throughput while minimizing BAL size. While full BAL delivers the highest performance, it also incurs the largest overhead. This raises a key question: **to what extent can the lowest-overhead design—parallel I/O BAL—approach the throughput of full BAL?** Addressing this question is the central goal of this work.

To answer it, we constructed an execution environment that explicitly includes state loading via I/O reads, with the following setup:

- A flat database for accounts, storage, and contract code, as used in Reth
- Pre-recovered transaction senders, leveraging sender recovery parallelism already implemented in most clients
- Omission of state root computation and state trie commits, whose costs can be amortized for large blocks and are not the focus of this study

Using this setup, we benchmarked per-transaction parallel execution (including parallel I/O and parallel execution) with different BAL designs. The results show that **parallel I/O BAL still acheives ~10.8 GGas/s** on a 16-core commodity machine under mega-block setting, which is comparable to ~13.9 GGas/s with full BAL. This demonstrates that, **relative to full BAL, parallel I/O BAL achieves 78% of the throughput of full BAL with only 33% of its BAL size, offering a practical trade-off between throughput and BAL size overhead**.

# The I/O Bottleneck in Ethereum Execution

Ethereum is continuing to scale L1. The Fusaka upgrade increased the gas limit from 45M to 60M, and Glamsterdam is expected to raise it further. [Our previous research](https://ethresear.ch/t/achieving-10gigagas-s-evm-execution-with-bal-and-parallel-execution/23632) showed that BAL can improve execution throughput by an order of magnitude, providing a solid foundation for higher gas limits.

Despite these gains, I/O remains a major bottleneck in today’s block processing pipeline. In a non-prewarming setup, I/O accounts for roughly 70% of total execution time. Taking Reth as an example:

- Single-threaded execution with I/O (using MDBX) achieves only ~350 MGas/s
- With prewarming, I/O overhead drops to ~20%, and throughput improves to ~700 MGas/s

Although prewarming helps, substantial headroom remains. The fundamental limitation for I/O lies in sequential I/O access patterns. Although modern NVMe SSDs support deep I/O queues (typically up to 64), most Ethereum clients still perform state reads sequentially and fail to fully exploit the available I/O parallelism.

BAL addresses this limitation by enabling parallel I/O, but it does so at a cost. Post-transaction state diffs are essential for parallel execution—our prior work showed they enable a 10× speedup over sequential execution. However, **read values and read hints can together be comparable in size to state diffs**, while the performance benefit they provide relative to this additional network and storage overhead is less clear.

This raises an important design question: if near-optimal performance can be achieved without including read values—or even read hints—BAL size could be reduced significantly, lowering network and storage costs without sacrificing throughput. To test this hypothesis, we focus on parallel I/O BAL, which includes only post-transaction state diffs and performs state reads on demand during execution.

# Experimental Methodology

To evaluate the ultimate performance limits enabled by parallel I/O BAL, we constructed a simplified execution environment by removing the aforementioned unrelated parts. This allows us to measure the true upper bound of BAL-powered parallelism.

Leveraging reth’s high-performance execution engine and RocksDB’s multi-threaded read capabilities, we modified the reth client to dump execution dependencies (including blocks, BALs, and the last 256 block hashes), use REVM as the EVM execution engine, and introduce a RocksDB-based state provider for account, code, and storage access.

## Simplification for I/O Execution Emulation

- All transactions come with the sender already recovered (sender recovery can be fully parallelized ahead of time).
- No state root computation or trie commits are performed after execution (only flat state commits), as these costs are orthogonal to the focus of this study.

## Engineering Work & Setup

- Modified the Reth client to support dumping full execution dependencies, including blocks, BALs, the last 256 block hashes.
- Added a rocksdb state provider for Revm to load account, code and storage state

Reth’s MDBX binding was initially tested but showed degraded performance under multi-threading; RocksDB was adopted instead, with a migration tool to convert MDBX databases to RocksDB
- For parallel I/O, a shared cache layer is used to avoid redundant reads across transactions

Dropped the page cache before each experiment
Parallelism granularity = per-transaction
Hardware:

- AMD Ryzen 9 5950X (16 physical cores, or 32 with hyper-threading)
- 128 GB RAM
- 7TB RAID-0 NVMe SSD (~960k random read IOPS for 4k blocks, 3.7GB/s bandwith)

Dataset: 2000 mainnet blocks (#23770000–23771999).
Metric: Gas per second = total gas used / execution with I/O time.

Benchmark suite available here:

![:backhand_index_pointing_right:](https://ethresear.ch/images/emoji/facebook_messenger/backhand_index_pointing_right.png?v=14) [GitHub - dajuguan/evm-benchmark](https://github.com/dajuguan/evm-benchmark#execution-with-io)

# Results

We first evaluated Ethereum mainnet blocks under parallel I/O and parallel execution with different thread counts given parallel I/O BAL. The results reveal a clear **critical path dominated by the longest-running transactions**. To mitigate this, we simulated larger block gas limits, which unlock substantially more parallelism when using BAL.

With 16 threads and a 1G-gas block, **parallel I/O BAL achieves a throughput of ~10.8 GGas/s**, approaching **78% of the ~13.8 GGas/s achieved by full BAL**. Crucially, this performance comes with an average BAL size of only ~71 KB, representing a **~67% reduction compared to full BAL**.

## Critical Path Analysis in Parallel I/O and Parallel Execution

To evaluate both the actual speedup and the effect of Amdahl’s law on transaction-level parallelism, we conducted per-transaction parallel execution experiments to quantify the impact of the longest-running transactions on the achievable speedup.

Detailed results are shown below (where “longest txs latency” is the total execution with I/O time of the longest-running transactions in each block):

| Threads | Throughput (MGas/s) | Longest TXs Latency | Total     Time |
| --- | --- | --- | --- |
| 1 | 740 | 6.85s | 60.62s |
| 2 | 1,447 | 6.75s | 31.00s |
| 4 | 2,167 | 8.11s | 20.70s |
| 8 | 2,994 | 9.02s | 14.98s |
| 16 | 3,220 | 8.92s | 13.93s |
| 32 | 3,253 | 9.57s | 13.79s |

Overall, the results closely follow Amdahl’s law. Although throughput increases with more threads, total execution time is constrained by the longest transaction. Under 16 threads, the longest transactions account for ~75% of total execution time, limiting speedup to ~4× rather than the ideal 16×.

To overcome this limitation, we tried to increase the block gas limit.

> When thread count exceeds physical cores (e.g 32 threads on 16 cores), performance no longer improves. While I/O itself can scale beyond physical cores, this is likely limited by RocksDB cache lookups (indexes, bloom filters, data blocks) and CPU-intensive value encoding/decoding.

## Mega Blocks Enable Massive Parallelism

To overcome per-block critical path limits, we experimented with higher-gas “mega blocks” as in our previous work to increase parallelism. To simulate this, we executed the transactions of multiple consecutive mainnet blocks, namely a mega block or a batch, in parallel, and then committed the state to database only after all transactions in the batch had completed. This effectively aggregates multiple blocks into a single large execution unit.

We evaluated a batch of 50 blocks, simulating an average block gas usage of 1,121 M, across different thread counts. Full results are shown below:

| Threads | Throughput (MGas/s) | Longest TXs Latency | Total Time |
| --- | --- | --- | --- |
| 1 | 943 | 0.53s | 47.55s |
| 2 | 1,857 | 0.53s | 24.16s |
| 4 | 3,505 | 0.56s | 12.80s |
| 8 | 6,524 | 0.57s | 6.88s |
| 16 | 10,842 | 0.61s | 4.13s |
| 32 | 10,794 | 1.07s | 4.14s |

With mega blocks, the longest running transactions no longer dominate the critical path—they contribute less than 15% of total execution time under 16 threads. Throughput scales almost linearly with thread count, reaching ~10.8 GGas/s—78% of full BAL performance—while maintaining a 67% reduction in BAL size of full BAL.

| BAL Design | RLP-Encoded BAL Size | Throughput with 16 threads |
| --- | --- | --- |
| Full BAL | 213 KB | 13,881 Mgas/s |
| Parallel I/O BAL | 71 KB (33% of 213 KB) | 10,842 Mgas/s |

# Conclusion

This study demonstrates that parallel I/O BAL approaches the performance of full BAL while substantially reducing BAL size. In mega-block settings, parallel I/O BAL sustains approximately 10.8 GGas/s (~78% of full BAL throughput), while reducing BAL size overhead to about 33% of that of full BAL. This makes parallel I/O BAL a practical and efficient design choice, balancing throughput against network and storage overhead.

Overall, these results establish a practical upper bound for parallel I/O BAL-powered parallel execution and provide actionable insights for Ethereum client optimizations and future L1 scaling efforts.

# Other works

In addition to execution benchmarks, we compared RocksDB and MDBX under synthetic random-read workloads and EVM execution, and examined the trade-offs between parallel I/O BAL and batched I/O BAL across different block gas limits.

## MDBX vs. RocksDB Random Read Benchmark

We first benchmarked raw random-read performance for MDBX and RocksDB on the same hardware used in prior experiments, varying the number of reader threads to assess scalability. The database configuration was as follows:

| Item | Value |
| --- | --- |
| Key size | 16 bytes |
| Value size | 32 bytes |
| Entries | 1.6 billion |
| RocksDB size | 85 GB |
| MDBX size | 125 GB |

Detailed results:

| Threads | Database | IOPS | Avg Latency (µs) | CPU Usage (%) |
| --- | --- | --- | --- | --- |
| 2 | RocksDB | 12K | 160 | 1.1 |
| 2 | MDBX | 21K | 85 | 0.8 |
| 4 | RocksDB | 30K | 130 | 2.2 |
| 4 | MDBX | 48K | 84 | 1.3 |
| 8 | RocksDB | 85K | 92 | 4.5 |
| 8 | MDBX | 97K | 83 | 2.5 |
| 16 | RocksDB | 180K | 90 | 8 |
| 16 | MDBX | 180K | 86 | 6 |
| 32 | RocksDB | 320K | 110 | 24 |
| 32 | MDBX | 360K | 90 | 13 |

Both RocksDB and MDBX scale throughput nearly linearly with thread count, even beyond the 16 physical cores. Once thread counts exceed 8, the differences in IOPS and latency between the two databases become minimal.

Benchmark suite availiable at: [GitHub - dajuguan/ioarena: Embedded storage benchmarking tool for libmdbx, rocksdb, lmdb, etc.](https://github.com/dajuguan/ioarena)

## MDBX vs. RocksDB EVM Execution Benchmark with Parallel I/O Setup

We then evaluated EVM execution throughput with parallel I/O using MDBX and compared it against RocksDB, under a block gas usage of 1,121 M. Detailed results:

| Threads | Database | Throughput (MGas/s) |
| --- | --- | --- |
| 8 | MDBX | 2,369 |
| 8 | RocksDB | 6,524 |
| 16 | MDBX | 3,705 |
| 16 | RocksDB | 10,842 |
| 32 | MDBX | 5,748 |
| 48 | MDBX | 6,662 |
| 64 | MDBX | 6,525 |

Despite similar raw I/O performance, execution throughput with MDBX is significantly lower. This discrepancy is likely due to the current usage of reth’s MDBX binding, which does not fully exploit the underlying I/O parallelism. In particular, proper management of shared readers across threads could improve performance, but we have not yet found an effective approach.

## Parallel I/O vs. Batched I/O across Gas Limits

The previous analysis primarily focused on parallel I/O, where state is fetched on demand during execution. However, batched I/O may offer advantages in scenarios where some transactions are highly I/O-intensive and can better exploit I/O parallelism beyond the number of physical CPU cores.

To evaluate this trade-off, we compared parallel I/O BAL and batched I/O BAL across different I/O load pattern, and measured how execution throughput scales under the two BAL designs.

### Average I/O Load Analysis with Mainnet data

We begin with the average-case analysis, where storage reads account for only a fraction of the instructions executed within each transaction—a setting that closely reflects typical mainnet workloads. The following table summarizes the throughput results under different BAL designs, thread counts, and block gas usage.

| I/O Type | Threads | Block Batch Size | Avg. Block Gas (M) | Throughput (MGas/s) |
| --- | --- | --- | --- | --- |
| Batched | 16 | 1 | 22 | 3,587 |
| Batched | 32 | 1 | 22 | 3,333 |
| Parallel | 16 | 1 | 22 | 2,893 |
| Batched | 16 | 10 | 224 | 7,221 |
| Batched | 32 | 10 | 224 | 6,725 |
| Parallel | 16 | 10 | 224 | 6,842 |
| Batched | 16 | 50 | 1,121 | 10,159 |
| Batched | 32 | 50 | 1,121 | 10,259 |
| Parallel | 16 | 50 | 1,121 | 10,842 |
| Batched | 16 | 100 | 2,243 | 11,129 |
| Batched | 32 | 100 | 2,243 | 11,266 |
| Parallel | 16 | 100 | 2,243 | 11,292 |

As block gas usage increases, throughput continues to increase for both designs. However, **the relative advantage of batched I/O BAL decreases steadily, from roughly 20% at small block sizes to nearly zero at large block sizes**.

In addition, increasing the threads beyond 16 to 32 for batched I/O BAL provides little performance benefit, indicating that the workload becomes CPU-bound rather than I/O-bound. This behavior is likely due to RocksDB cache lookups and CPU-intensive value encoding/decoding, which limit further I/O scaling.

| BAL Design | RLP-Encoded BAL Size |
| --- | --- |
| Batched I/O BAL (with reads) | 110 KB |
| Parallel I/O BAL (without reads) | 71 KB (35% smaller) |

Crucially, the average RLP-encoded BAL size for batched I/O is approximately 35% larger than that of parallel I/O. Given that large blocks expose excution bottlenecks beyond I/O reads alone, this additional network and storage overhead makes **parallel I/O the more attractive BAL design choice overall**. Detailed BAL size measurements are also available in the [above benchmark suite](https://github.com/dajuguan/evm-benchmark#bal-size-measurement).

### Worst-Case I/O Load Analysis with Simulated Data

To complement the average-case results, we now consider the worst-case I/O load scenario, where disk reads dominate transaction execution.

To simulate this setting, we construct synthetic transactions that maximize storage access pressure. Specifically, we generate transactions whose opcode stream is filled with calls to a contract performing repeated `SLOAD(x)` operations, where `x` is the hash of a random value. Without BAL-provided read locations, such transactions must execute the `SLOAD` opcodes sequentially to fetch storage state, representing a worst-case I/O-bound workload.

Given the current per-transaction gas limit of 16 million gas, and a per-slot state read cost of approximately:

- 2000 gas for SLOAD, plus ~39 gas for keccak hash overhead,

a single transaction can perform at most:\frac{16{,}000{,}000}{2039} \approx 7{,}845

distinct storage reads. Using this configuration, we simulate worst-case I/O-load transactions with the mainnet database.

The resulting performance comparison between batched and parallel I/O designs is shown below:

| I/O Type | Threads | Total Execution Time (ms) | Avg. Block Gas (M) | Throughput (MGas/s) |
| --- | --- | --- | --- | --- |
| Batched | 16 | 14.4 | 64 | 4,571 |
| Batched | 32 | 11.2 | 64 | 5,818 |
| Batched | 48 | 10.7 | 64 | 6,400 |
| Batched | 64 | 10.7 | 64 | 5,333 |
| Parallel | 4 | 82.5 | 64 | 780 |
| Batched | 16 | 42.6 | 640 | 11,034 |
| Batched | 32 | 58.2 | 640 | 12,307 |
| Batched | 32 | 60.3 | 640 | 10,158 |
| Parallel | 16 | 82.2 | 640 | 7,804 |

Under a lower block gas usage (64M gas), batched I/O BAL achieves its best throughput at 48 threads, reaching nearly **8× the throughput of parallel I/O BAL**. This confirms that explicit I/O batching is highly effective when storage reads dominate execution.

However, it is important to interpret these results in an end-to-end execution context. Even in the worst-case I/O load scenario, the total execution time for parallel I/O BAL remains well below the current attestation deadline (~3 seconds). Moreover, as theres are no state changes in this case, parallel execution excludes merklization and state commit costs, which together account for nearly 50% of total execution time in realistic parallel execution pipelines.

In the 10× gas-usage mega-block setting (640 M gas), the performance gap narrows further: batched I/O BAL outperforms parallel I/O BAL by only **~1.6×**, while both remain comfortably within validation time constraints.

| I/O Type | Avg. Block Gas (M) | Optimal Throughput (MGas/s) | RLP-Encoded BAL Size |
| --- | --- | --- | --- |
| Batched | 64 | 6,400 | 251 kb |
| Parallel | 64 | 6,400 | 0 kb |
| Batched | 640 | 15,238 | 2,511 kb |
| Parallel | 640 | 6,153 | 0 kb |

Taken together, under worst-case I/O-heavy workloads, we observe the following:

- Under current mainnet gas limits:

Batched-I/O BAL achieves up to an 8× throughput improvement over parallel-I/O BAL. However, when considering end-to-end block processing time, I/O reads are not the dominant bottleneck in this regime.

**Under 10× gas limits:**

- The performance advantage of batched-I/O BAL narrows significantly, delivering 1.6× throughput over parallel-I/O BAL, while incurring an additional ~2.5 MiB BAL size overhead, which is non-negligible.

These results reinforce a key insight: although batched-I/O BAL delivers the best performance under pathological, I/O-saturated workloads, **parallel-I/O BAL remains sufficiently robust even in worst-case scenarios—without incurring the additional BAL size overhead introduced by batching.**

Benchmark suite available here:

![:backhand_index_pointing_right:](https://ethresear.ch/images/emoji/facebook_messenger/backhand_index_pointing_right.png?v=14) [GitHub - dajuguan/evm-benchmark](https://github.com/dajuguan/evm-benchmark?tab=readme-ov-file#execute-with-worst-io-load-case)
