---
source: ethresearch
topic_id: 6810
title: Preventing pooled mining by VRF-based mining
author: SebastianElvis
date: "2020-01-19"
category: Mining
tags: []
url: https://ethresear.ch/t/preventing-pooled-mining-by-vrf-based-mining/6810
views: 2270
likes: 2
posts_count: 5
---

# Preventing pooled mining by VRF-based mining

Hi everyone,

We’d like to introduce VRF-based mining, a surprisingly simple and effective way of making pooled mining impossible. Instead of using hash functions, we use Verifiable Random Functions (VRFs) for proof-of-work-based consensus. As VRF binds the authorship with hashes, a pool operator should reveal his private key to outsource the mining process to miners, and miners can easily steal cryptocurrency in the pool operator’s wallet anonymously.

Please find the details here https://hackmd.io/@ZcwjuAe3RUCFVPrXtvriPQ/S1YM1KZWI

This idea is co-developed by Runchao Han (me) and Haoyu Lin ([@haoyuathz](/u/haoyuathz)). We thank Jiangshan Yu and Omer Shlomovits for their valuable feedback.

## Replies

**SebastianElvis** (2020-01-20):

A known issue (credit to [@ChengWang](/u/chengwang)): The miner should keep the secret key in memory all the time in order to mine. This may give opportunities for attackers to steal the secret key.

For example, the mining software has a bug, and the attacker can exploit this bug to access the memory space of the process of the mining software.

A possible solution is to use Oblivious RAM (ORAM), but maybe there are more elegant ways?

---

**Mikerah** (2020-01-21):

Another possible solution would be to use hardware or software enclaves to guard secrets in memory.

---

**SebastianElvis** (2020-01-21):

Correct, using enclaves can be a good solution. Here the enclave should just protect read operations on the secret key, so it is unnecessary to be general-purpose (like SGX). Maybe this simplifies the design of ASIC specialised for VRF-based mining?

---

**Mikerah** (2020-01-22):

I’m not an enclave expert but it does seem like you get simplification in the ASIC design if your enclave is only for managing private keys, instead of a general purpose enclave.

