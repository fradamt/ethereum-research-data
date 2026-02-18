---
source: ethresearch
topic_id: 22847
title: Ethereum Bytecode and Code Chunk Analysis
author: weiihann
date: "2025-07-31"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/ethereum-bytecode-and-code-chunk-analysis/22847
views: 153
likes: 1
posts_count: 1
---

# Ethereum Bytecode and Code Chunk Analysis

# Ethereum Bytecode and Code Chunk Analysis

Code chunking is a strategy for breaking up bytecode into smaller chunks, which helps reduce witness size. However, this approach is only effective if a relatively small portion of the bytecode is accessed during execution. This analysis explores byte and chunk access patterns to evaluate the utility of code chunking.

## Methodology

The complete repository which includes the data collection and analysis code can be found [here](https://github.com/weiihann/chunk-analysis).

## Analysis

### Key Dataset Statistics

- Block range: 15537394 (The Merge)–22000000
- Block Count: 100898 (spreaded evenly across the block range)
- Total contract interactions: 19,934,701
- Min. unique contracts interacted with per block: 1
- Median unique contracts interacted with per block: 187
- Max. unique contracts interacted with per block: 659
- Total unique contracts interacted with: 1,220,017

[![](https://ethresear.ch/uploads/default/optimized/3X/1/d/1de579983fbbf29903c7dda65bd4177c9a49f7a1_2_690x410.png)987×587 30 KB](https://ethresear.ch/uploads/default/1de579983fbbf29903c7dda65bd4177c9a49f7a1)

---

### Bytes Access Patterns

This section examines the proportion of bytecode accessed during contract execution:

```auto
Bytes Accessed Ratio = bytes accessed / total bytecode size
```

[![](https://ethresear.ch/uploads/default/original/3X/d/8/d85759435c15d8c35d983753e63ec9795327f3d7.png)626×472 25 KB](https://ethresear.ch/uploads/default/d85759435c15d8c35d983753e63ec9795327f3d7)

[![](https://ethresear.ch/uploads/default/optimized/3X/c/4/c464eac2d7b57a71705caf790e4651e836c2ef3b_2_534x500.png)627×586 29.7 KB](https://ethresear.ch/uploads/default/c464eac2d7b57a71705caf790e4651e836c2ef3b)

**Core Finding:** On average, only **22.8%** of the contract bytecode was accessed in a block.

**Detailed Insights:**

- Median proportion accessed: 17.1%
- By contract size:

Tiny (

**Interpretation:** For contracts larger than 1 KiB, only a small fraction of the bytecode is accessed. Contracts under 1 KiB tend to have more of their bytecode accessed. This is expected, as small contracts usually contain fewer functions that are repeatedly invoked.

---

### Chunk Access Patterns

Referencing [EIP-2926](https://eips.ethereum.org/EIPS/eip-2926) as a code chunking solution, we split the contract bytecode into 31-byte chunks and assess the proportion of 31-byte chunks accessed:

```auto
Total number of chunks = bytecode size / 31
Chunks Accessed Ratio = chunks accessed / total number of chunks
```

[![](https://ethresear.ch/uploads/default/original/3X/5/0/50b6212aa5735925dc70f0330ef1acefb17e11db.png)616×472 21.5 KB](https://ethresear.ch/uploads/default/50b6212aa5735925dc70f0330ef1acefb17e11db)

[![](https://ethresear.ch/uploads/default/optimized/3X/c/8/c81a885260e330ff816c8e4df225825caac1c28e_2_534x500.png)627×586 29 KB](https://ethresear.ch/uploads/default/c81a885260e330ff816c8e4df225825caac1c28e)

**Core Finding:** On average, only **29.6%** of 32-byte chunks were accessed in a block.

**Detailed Insights:**

- Median proportion accessed: 24.7%
- By contract size:

Tiny (

**Interpretation:** The results are similar to the bytes accessed ratio. Chunk access is also low for contracts over 1 KiB. However, the overall chunk accessed ratios are slightly higher than byte accessed ratios, suggesting that not all bytes in the accessed chunks were used.

---

### Chunks Efficiency

In this section, we explore how efficient chunks are, i.e., how many bytes in the chunks are actually used:

```auto
Chunks Efficiency = bytes accessed / (chunks accessed * 31)
```

[![](https://ethresear.ch/uploads/default/original/3X/9/d/9dbf725fc7192e3df32bfca11e3bdff653584351.png)626×472 24.3 KB](https://ethresear.ch/uploads/default/9dbf725fc7192e3df32bfca11e3bdff653584351)

[![](https://ethresear.ch/uploads/default/optimized/3X/4/1/41c30674476f93146fd3bd4c72da93fae0c78d1a_2_534x500.png)627×586 31.8 KB](https://ethresear.ch/uploads/default/41c30674476f93146fd3bd4c72da93fae0c78d1a)

**Core Finding:** On average, **68.9%** of the bytes in the 31-byte chunks were accessed. That’s roughly 21 bytes in every 31-byte chunks on average.

This indicates that more than half of the bytes in 31-byte chunks were accessed. To maximize chunk efficiency, we may consider smaller chunk sizes (e.g., 16-byte chunks). However, this comes at the cost of increased hashing overhead.

---

### Code-Access Instructions

This section evaluates the impact of opcodes that access the entire code, namely:

- EXTCODESIZE
- EXTCODECOPY
- CODECOPY
- CODESIZE

When one of these opcodes is executed, it requires access to all of the bytes in the bytecode. In the past sections of evaluating the access ratios, we exclude them from the results. Here, we assess how including them changes the access ratios. We split them into two categories:

1. Code Size (EXTCODESIZE, CODESIZE)
2. Code Copy (EXTCODECOPY, CODECOPY)

The reason for the 2 categories is because [EIP2926](https://eips.ethereum.org/EIPS/eip-2926) adds the code size in the account field. Therefore, once it’s implemented, code size opcodes will no longer require access to the entire bytecode.

[![](https://ethresear.ch/uploads/default/optimized/3X/0/0/006f9dcaccb388b65372d3831da30d0576ce80ab_2_690x341.png)1187×587 31.8 KB](https://ethresear.ch/uploads/default/006f9dcaccb388b65372d3831da30d0576ce80ab)

In total, **46.6%** of contracts per block contain either the code size or code copy opcodes. Among these, **40.7%** contain code size opcodes, while only **10.6%** contain the code copy opcodes.

[![download (9)](https://ethresear.ch/uploads/default/optimized/3X/f/c/fc0a573d5a6733a1c76fb928f3b57f8075b2044d_2_529x500.png)download (9)620×586 31.7 KB](https://ethresear.ch/uploads/default/fc0a573d5a6733a1c76fb928f3b57f8075b2044d)

[![download (10)](https://ethresear.ch/uploads/default/optimized/3X/e/5/e5a41ec5a665c6904de29134e4aa74e5daa8932e_2_529x500.png)download (10)620×586 32.4 KB](https://ethresear.ch/uploads/default/e5a41ec5a665c6904de29134e4aa74e5daa8932e)

[![download (11)](https://ethresear.ch/uploads/default/optimized/3X/f/2/f2525b3c10034ead7cf3a294472e14f61a1a0d23_2_529x500.png)download (11)620×586 31.8 KB](https://ethresear.ch/uploads/default/f2525b3c10034ead7cf3a294472e14f61a1a0d23)

[![download (12)](https://ethresear.ch/uploads/default/optimized/3X/1/7/1792fae8f7d607e409b07a73cfbbd70c9ecb8ff2_2_529x500.png)download (12)620×586 32.2 KB](https://ethresear.ch/uploads/default/1792fae8f7d607e409b07a73cfbbd70c9ecb8ff2)

**Avg Bytes Access Ratio**

- Original: 22.8%
- With Code Size: 54.0% (+31.2%)
- With Code Copy: 31.5% (+8.7%)

**Avg Chunks Access Ratio**

- Original: 29.6%
- With Code Size: 57.8% (+28.2%)
- With Code Copy: 37.6% (+8.0%)

After including the code-access instructions, we do see a moderate increase in the access ratios. However, it’s mostly due to code size opcodes. As mentioned before, the addition of code size in the account field would make code copy opcodes the only instructions to access the entire bytecode. Since the amount of code copy instructions is significantly lesser, the overall access ratios are lower.

---

## Is Code Chunking A Viable Solution?

Referencing [EIP-2926](https://eips.ethereum.org/EIPS/eip-2926), the main point of code chunking is to reduce witness size, as the current status quo requires the whole bytecode to be used in the code proof.

Our analysis has shown that not all of the bytes in a contract’s bytecode are used. In fact, only a relatively small proportion of the bytes and chunks are used. Based on the current access patterns, if we were to implement code chunking, we would significantly reduce the amount of actual bytes used included in the code witness.

The addition of code size in the account field in EIP2926 would effectively make code copy opcodes the only instructions that requires accessing the entire bytecode. In addition, as shown in our findings, the amount of code copy opcodes is significantly less than the code size. Therefore, we would further reduce the average code witness size based on the current access pattern.

One additional exploration that we can conduct is to determine the optimal chunk size. In EIP-2926, it uses 31-byte chunks. We may want to explore smaller chunk sizes, such as 16-byte, to maximize the number of bytes utilized per chunk. However, this comes at a cost of additional hash overhead. Therefore, we need to experiment with different chunk sizes to find the optimal balance.
