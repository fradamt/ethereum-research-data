---
source: ethresearch
topic_id: 23850
title: Data-driven analysis on EIP-7907
author: CPerezz
date: "2026-01-13"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/data-driven-analysis-on-eip-7907/23850
views: 263
likes: 6
posts_count: 6
---

# Data-driven analysis on EIP-7907

*The following report, aims to be a collection of data that will hopefully be a resource that will help ACD to take a decision over EIP-7907.

Also, this hopefully sets a new methodology of backing up EIPs or proposals with as much data as possible, which can definitely help taking better and more informed decisions when scoping forks.*

*I want to thank [@rjl493456442](/u/rjl493456442)  for [his PR adding metrics](https://github.com/ethereum/go-ethereum/pull/33442) in Geth and his advice and support during the benchmark collection which has been extremely helpful. And which I’d like to standarize eventually across all clients such that we can compare data easily and collect data easily to inform our decisions on repricings and scaling.

Finally, it’s important to highlight that Geth is severely underperforming due to the totally disabled cache (which also affects pre-warming). Notice that in a real-world scenario, even this benchmarks would be better. The intention is getting the worst-possible case such that if we’re good under it, we can skip 7907 repricing straight away.*

---

Related Issue:** [EIP-7907](https://github.com/ethereum/EIPs/pull/7907)

**Date:** 2026-01-13

**Benchmark Environment:** Geth (dev mode) with mainnet-sized database (~24M blocks), **internal caches disabled**

**Test Configuration:** ~18,106 EXTCODESIZE operations per block (all different bytecode contracts), ~50M gas

**Hardware:** WD Black SN850X NVMe (8TB)

---

## Executive Summary

This report analyzes the performance of the `EXTCODESIZE` opcode when reading contracts of varying bytecode sizes (0.5KB to 64KB) **with Geth’s internal code cache disabled**. This represents the worst-case attack scenario where an attacker deploys thousands of unique contracts to force cold disk reads.

The iteration also has the lowest overhead possible leaveraging `CREATE2` deterministic address generation.

More information regarding this can be found in:

- feat: add extcodesize_setup scenario for deploying EXTCODESIZE benchmark contracts by CPerezz · Pull Request #161 · ethpandaops/spamoor · GitHub
- https://github.com/ethereum/execution-specs/pull/1961

### Key Findings

| Finding | Value |
| --- | --- |
| Code read time range | 107ms - 904ms (for ~18K code reads) |
| Per-call latency range | 5.9µs - 49.9µs |
| Code read time scaling | 8.5x growth (0.5KB → 64KB) |
| 64KB block execution time | ~1006ms |
| Code read % of block time | 51% (0.5KB) → 90% (64KB) |
| Geth efficiency vs raw NVMe | 24-51% |

### EIP-7907 Verdict

| Size | Block Time | % of 1s Budget | Verdict |
| --- | --- | --- | --- |
| 24KB (current) | 535ms | 54% | Safe |
| 32KB | 685ms | 69% | Safe |
| 64KB | 1006ms | ~100% | Viable at 60M gas |
| 128KB+ | Projected 1.5s+ | >100% | Might need gas repricing, We need more data after BALs + ePBS |

**Recommendation:** Proceed with 64KB as the new maximum contract size. Beyond 64KB would require new data collection once BALs and ePBS’s optimizations are landed in all clients.

If a repricing was required after the data collection mentioned above, such pricing would also require being able to benchmark the rest of the clients as well as looking to the rest of `EXTCODE*` opcodes.

---

## 1. Methodology & Benchmark Setup

### 1.1 Test Environment

| Parameter | Value |
| --- | --- |
| Geth version | v1.16.8-unstable (with lots of hacks) |
| Database | Mainnet synced (~24M blocks) |
| Geth cache | Disabled (forces disk reads) |
| Contract sizes tested | 0.5, 1, 2, 5, 10, 24, 32, 64 KB |
| EXTCODESIZE operations | ~18,106 per block |
| Gas per block | ~50M |
| Deployed contracts | 18,100+ unique contracts per size |
| Iterations per size | 8 |
| Hardware | WD Black SN850X NVMe 8TB |

### 1.2 Attack Scenario Design

This benchmark represents the **worst-case attack** against `EXTCODESIZE`:

- 18,100+ unique contracts deployed per size (forces code cache misses)
- Each block reads bytecode from all unique contracts exactly once
- Code cache hit rate: <2% (effectively disabled)
- OS page cache cleared between benchmark runs

### 1.3 Raw Disk Baseline (fio)

To establish theoretical maximum performance, we measured raw NVMe capabilities:

| Block Size | IOPS | Throughput | Avg Latency |
| --- | --- | --- | --- |
| 512B | 337K | 172 MB/s | 95 µs |
| 1KB | 320K | 328 MB/s | 100 µs |
| 4KB | 272K | 1.1 GB/s | 117 µs |
| 24KB | 171K | 4.2 GB/s | 185 µs |
| 32KB | 155K | 5.1 GB/s | 204 µs |
| 64KB | 85K | 5.6 GB/s | 366 µs |

---

## 2. Benchmark Results

### 2.1 Code Read Time vs Bytecode Size

[![7907_violin_code_read_time](https://ethresear.ch/uploads/default/optimized/3X/0/7/072434480e0d2b18c0621e1bdc91eeec4b0bcdc8_2_690x402.png)7907_violin_code_read_time1800×1050 91.5 KB](https://ethresear.ch/uploads/default/072434480e0d2b18c0621e1bdc91eeec4b0bcdc8)

[![7907_code_read_vs_size](https://ethresear.ch/uploads/default/optimized/3X/a/0/a0cc942cebfe6f0a903a5e3ad723be8615e93953_2_690x414.png)7907_code_read_vs_size1500×900 55 KB](https://ethresear.ch/uploads/default/a0cc942cebfe6f0a903a5e3ad723be8615e93953)

**Core Finding:** Code read time scales with bytecode size when cache is ineffective.

| Size | Code Read (ms) | Growth vs 0.5KB |
| --- | --- | --- |
| 0.5KB | 107ms | 1.0x (baseline) |
| 1KB | 135ms | 1.3x |
| 2KB | 142ms | 1.3x |
| 5KB | 145ms | 1.4x |
| 10KB | 161ms | 1.5x |
| 24KB | 428ms | 4.0x |
| 32KB | 584ms | 5.5x |
| 64KB | 904ms | 8.5x |

**Key insight:** Code read time grows 8.5x as bytecode size grows 128x. This is **sub-linear** scaling (not 1:1), but the absolute time impact is significant.

### 2.2 Bytes Read vs Code Read Time (Correlation)

[![7907_code_read_vs_total_bytes](https://ethresear.ch/uploads/default/optimized/3X/6/d/6d347f04cecfd73de4a686b72919e4e54e52b239_2_690x414.png)7907_code_read_vs_total_bytes1500×900 76 KB](https://ethresear.ch/uploads/default/6d347f04cecfd73de4a686b72919e4e54e52b239)

The strong positive correlation (R² ≈ 0.96) confirms that code read time scales with total bytes read when caches are ineffective.

### 2.3 Per-Call Latency

[![7907_per_call_latency](https://ethresear.ch/uploads/default/optimized/3X/8/d/8d07c15906fd07535fe278170e5c6ce5d8b46c62_2_690x414.png)7907_per_call_latency1500×900 59.1 KB](https://ethresear.ch/uploads/default/8d07c15906fd07535fe278170e5c6ce5d8b46c62)

Per-call latency grows with bytecode size:

| Size | Per-Call Latency | Growth |
| --- | --- | --- |
| 0.5KB | 5.9 µs | 1.0x |
| 1KB | 7.5 µs | 1.3x |
| 10KB | 8.9 µs | 1.5x |
| 24KB | 23.7 µs | 4.0x |
| 32KB | 32.3 µs | 5.5x |
| 64KB | 49.9 µs | 8.5x |

---

## 3. Execution Time Breakdown

### 3.1 Component Analysis

[![7907_time_breakdown_stacked](https://ethresear.ch/uploads/default/optimized/3X/c/f/cff7ee47015e5eb928bb11dfbdff1d4fb8da17ce_2_690x402.png)7907_time_breakdown_stacked1800×1050 69.2 KB](https://ethresear.ch/uploads/default/cff7ee47015e5eb928bb11dfbdff1d4fb8da17ce)

Code read becomes the **dominant factor** at larger bytecode sizes:

| Size | Code Read | Account Read | EVM Exec | DB Write | Other | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 0.5KB | 107ms (51%) | 54ms | 34ms | 12ms | 2ms | 209ms |
| 1KB | 135ms (57%) | 53ms | 37ms | 12ms | 1ms | 238ms |
| 10KB | 161ms (59%) | 53ms | 40ms | 12ms | 5ms | 271ms |
| 24KB | 428ms (80%) | 44ms | 46ms | 15ms | 2ms | 535ms |
| 32KB | 584ms (85%) | 38ms | 47ms | 13ms | 3ms | 685ms |
| 64KB | 904ms (90%) | 38ms | 51ms | 12ms | 1ms | 1006ms |

**Observation:** At 64KB, code read consumes 90% of block execution time. This is dramatically different from warm-cache scenarios where code read is only 8-10%.

---

## 4. Block Time Budget Analysis (EIP-7907 Focus)

### 4.1 Time vs Budget Target

[![7907_block_time_budget](https://ethresear.ch/uploads/default/optimized/3X/f/b/fbf1bba53d3c5db61e0abec242e9952c93115871_2_690x414.png)7907_block_time_budget1500×900 60.4 KB](https://ethresear.ch/uploads/default/fbf1bba53d3c5db61e0abec242e9952c93115871)

Using a 1-second target for block execution:

| Size | Block Time | % of 1s Budget | Status |
| --- | --- | --- | --- |
| 0.5KB | 209ms | 21% | Well under budget |
| 1KB | 238ms | 24% | Well under budget |
| 2KB | 248ms | 25% | Well under budget |
| 5KB | 252ms | 25% | Well under budget |
| 10KB | 271ms | 27% | Well under budget |
| 24KB | 535ms | 54% | Under budget |
| 32KB | 685ms | 69% | Under budget |
| 64KB | 1006ms | ~100% | At limit |

**Conclusion:** 64KB contracts are viable under worst-case attack conditions at 60M gas blocks. The ~1-second execution time is at the budget limit but acceptable. Note that this is a quite conservative limit considering ePBS & BALs will likely reshape what we consider a safe budget in the near future.

### 4.2 Gas Processing Rate (Mispricing Analysis)

[![7907_mgas_vs_size](https://ethresear.ch/uploads/default/optimized/3X/5/4/54e2fee8636976a611abbf93f88b3cd0e7436fd9_2_690x414.png)7907_mgas_vs_size1500×900 64.3 KB](https://ethresear.ch/uploads/default/54e2fee8636976a611abbf93f88b3cd0e7436fd9)

| Size | Gas Used | Block Time | Mgas/s |
| --- | --- | --- | --- |
| 0.5KB | 49.4M | 209ms | 236 |
| 1KB | 49.4M | 238ms | 208 |
| 10KB | 49.4M | 271ms | 182 |
| 24KB | 49.4M | 535ms | 92 |
| 32KB | 49.4M | 685ms | 72 |
| 64KB | 49.4M | 1006ms | 49 |

**Mispricing observed:** Same gas cost, but 5x different execution time (236 Mgas/s → 49 Mgas/s). This indicates that under worst-case conditions, larger contracts impose disproportionately higher cost on validators.

**Implication for 128KB+:** Beyond 64KB, a gas model adjustment would be needed—likely a base cost plus size-dependent component.

*Notice this is quite conservative. As in order to “halt” the network or “significantly hurt slow validators”, the setup required would be of hundreds of times the 18k unique contracts. Which incurrs on a massive costs (we can’t reuse them as they would be cached after the first block execution).*

---

## 5. Raw Disk Baseline (Geth vs NVMe Efficiency)

### 5.1 Efficiency Comparison

[![7907_geth_vs_nvme](https://ethresear.ch/uploads/default/optimized/3X/8/4/8431ab5073443e2403eec8cf385d5bb7dc88893c_2_690x295.png)7907_geth_vs_nvme2100×900 64.7 KB](https://ethresear.ch/uploads/default/8431ab5073443e2403eec8cf385d5bb7dc88893c)

| Size | Geth IOPS | Raw NVMe IOPS | Efficiency | Geth Throughput | Raw NVMe | Efficiency |
| --- | --- | --- | --- | --- | --- | --- |
| 0.5KB | 171K | 337K | 51% | 83 MB/s | 172 MB/s | 48% |
| 1KB | 142K | 320K | 44% | 139 MB/s | 328 MB/s | 42% |
| 24KB | 43K | 171K | 25% | 1.0 GB/s | 4.2 GB/s | 24% |
| 32KB | 31K | 155K | 20% | 979 MB/s | 5.1 GB/s | 19% |
| 64KB | 20K | 85K | 24% | 1.26 GB/s | 5.6 GB/s | 23% |

**Observation:** Geth achieves 20-51% of raw disk performance. The gap is likely due to:

- Pebble/LevelDB overhead (index traversal, bloom filters)
- Key hashing and lookup
- Value deserialization

---

## 6. Comparison with Warm Cache Scenario

### 6.1 Cached vs Uncached Performance

[![7907_cached_vs_uncached](https://ethresear.ch/uploads/default/optimized/3X/5/2/5243df8cd244c968dadac2cfc96d19dc6bb2f8c0_2_690x345.png)7907_cached_vs_uncached1800×900 64 KB](https://ethresear.ch/uploads/default/5243df8cd244c968dadac2cfc96d19dc6bb2f8c0)

| Size | Warm Cache | Cold Cache | Slowdown |
| --- | --- | --- | --- |
| 0.5KB | 5.3ms | 107ms | 21x |
| 1KB | 4.4ms | 135ms | 31x |
| 2KB | 4.5ms | 142ms | 32x |
| 5KB | 4.6ms | 145ms | 31x |
| 10KB | 4.7ms | 161ms | 34x |
| 24KB | 4.8ms | 428ms | 89x |
| 32KB | 4.9ms | 584ms | 119x |
| 64KB | 4.9ms | 904ms | 181x |

The “flat cost” finding from warm-cache benchmarks remains valid for normal operation. Cold cache conditions require extreme attack scenarios (18K+ unique contracts).

---

## 7. Implications for EIP-7907 & Recommendations

### 7.1 Summary of Findings

1. Code read time scales with size under attack conditions (8.5x from 0.5KB to 64KB)
2. 64KB is viable at 60M gas blocks—worst-case ~1s execution, within budget
3. This represents the absolute worst case—18K+ unique contracts is impractical to deploy and maintain (you need a new set for each block you want to run the attack).
4. Normal operation is unaffected—warm cache scenarios show flat ~5ms cost
5. Gas mispricing exists under attack (5x execution time variation for same gas)

### 7.2 EIP-7907 Recommendation

| Action | Recommendation |
| --- | --- |
| 64KB limit | Proceed - viable under worst-case attack. No need for the EIP |
| 128KB+ limit | Requires re-measuring with BALs + ePBS |

It seems we can just “keep it simple” and provide Smart Contract developers a nice upgrade on the codesize limit without any changes to the protocol besides the 64kB limit and the initcode size increase.

Once we have BALs and ePBS on a more ready state, **we will be in a position where data will guide us better towards a good decision on repricing/just proceed to 256kB.**

But it feels unnecessary to do a repricing now for something that doesn’t really need it even in it’s worst case.

### 7.3 Why 64KB is Acceptable

1. Attack impracticality: Deploying 18K+ unique 64KB contracts requires:

~13M gas per contract deployment (32K base + 64K × 200 gas/byte)
2. Hundreds of blocks just for setup
3. Significant ongoing cost to maintain attack surface
4. Block time within budget: Even worst-case ~1s is acceptable for 60M gas blocks
5. Cache effectiveness in practice: Real mainnet blocks reuse contracts; code cache hit rate is typically high
6. Sub-linear scaling: 8.5x time for 128x size growth indicates amortization still helps

## Replies

**rjl493456442** (2026-01-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> This represents the worst-case attack scenario where an attacker deploys thousands of unique contracts to force cold disk reads.

Given that the maximum gas limit per transaction is 16M and a block gas limit of 60M, a block can contain at least four transactions. In Geth, the required state (accounts, storage slots, and contract code) is internally prefetched alongside transaction execution. Under this setup, the time spent reading contract code should be lower than the reported ones in the writeup, in which the code cache is completely disabled.

---

**Po** (2026-01-15):

Great article. One concern, however: although the benchmark uses mainnet data, it primarily exercises the contract code database, which is relatively small (≈10 GB on PebbleDB) and can be fully covered by the OS page cache on typical machines. As a result, the reported per-call latency may largely reflect warm-cache behavior rather than true NVMe-backed random reads.

In addition, the reported per-call *average* latency under multi-threaded reads is likely influenced by IO-level parallelism and throughput amortization: while individual NVMe reads still incur ~70–100 µs of device latency, concurrent outstanding requests allow this cost to be overlapped, significantly lowering the observed average latency.

In practice, once account and storage lookups are included—where the working set is orders of magnitude larger and cache miss rates are higher—single-request and tail latencies on cache misses would be dominated by NVMe access, with device-level read latency typically in the 70–100 µs range. However, concurrent requests may yield much lower amortized averages, so the reported average latency may still match your observed results.

---

**CPerezz** (2026-01-15):

Hey thanks for the comments [@Po](/u/po)  !

1. As for OS page cache, they have been dropped in between each benchmark. So theoretically they should not be helping. Also, Geth was restarted between benchmarks too. So even with the cache disabled, we should get ridd of it.
2. I don’t see how you interpret warm-cache behaviour when the reads in Geth are >50% slower than in the NVME with fio. Maybe you can elaborate? Notice Geth should indeed be faster with the caches enabled as it would be able to prewarm.
3. Is there any way you envision to make this benchmark in even worse conditions for Geth? (ie. to get the worst possible case as I did now with no cache and 18k different-code contracts).
I ask because at the end this was my goal with this bench. It’s to mainly determine whether we need some type of repricing for EXTCODE* when we raise gas limits or not.
And in 1 week, this is as much as I was able to gather.

---

**Po** (2026-01-16):

1. For this comment, I actually meant Pebble’s internal cache, not Geth’s cache. You can tune Pebble’s cache size directly and make it smaller, for example:
 Cache:        pebble.NewCache(int64(cache * 1024 * 1024))
2. Regarding your interpretation:

 CPerezz:

> Observation: Geth achieves 20-51% of raw disk performance. The gap is likely due to:

 This is possibly correct. I’ve observed the same phenomenon with RocksDB as well, although I don’t fully understand the underlying mechanism yet
3. From my experience, cache size is the dominant factor affecting DB performance. See our latest research on how to tune the cache size Demystifying Blockchain KV Lookups: From O(log N) to O(1) Disk I/O . So my suggestion is:

Explicitly tune (reduce) Pebble’s cache size
4. Run another program that consumes most of the system memory, to ensure the effective cache available to the DB benchmark remains small. FYI, I’ve previously built a small Rust tool for this purpose: revm/bins/dbtool/src/cmd/cache_killer.rs at 3ec984266af98838967a88c2079bac2cebd7c48d · dajuguan/revm · GitHub

---

**CPerezz** (2026-01-16):

Ahhh thanks for the clarifications!

1. Yes, I did not touch Pebble’s cache. I thought that having no code cache at all in Geth and dropping the OS page cache between runs + restarting Pebble + Geth in between runs would be a good-enough representative worst case. More than that would be just unnecessarily pessimistic/bad (we would even had to decrease the limit lol).
2. I can’t think of anything else. Though this is a question for @rjl493456442 as this is not my area of expertise.
3. Yes. I agree on that. But as said on point 1, no node runs without cache. And even if it did, the attack setup makes it prohivitively expensive to do it for multiple blocks (you’d need 36.000 contracts of 64kB each with different bytecode) just to make this attack for 1 block.
So imagine more.. This is one of the reasons I did not disable even more stuff. Also, notice that Pebble won’t run with less than 16MB of cache.

