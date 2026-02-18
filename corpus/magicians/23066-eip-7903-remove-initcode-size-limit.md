---
source: magicians
topic_id: 23066
title: "EIP-7903: Remove Initcode Size Limit"
author: charles-cooper
date: "2025-03-05"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7903-remove-initcode-size-limit/23066
views: 249
likes: 4
posts_count: 7
---

# EIP-7903: Remove Initcode Size Limit

discussion topic for [Add EIP: Remove Initcode Size Limit by charles-cooper · Pull Request #9452 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9452)

## Replies

**sbacha** (2025-03-08):

Is Pectra off the table for this?

![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

---

**charles-cooper** (2025-03-14):

benchmarks (tl;dr: jumpdest analysis shows a strong linear correlation to initcodesize, at sizes ranging from 128 bytes to 15MB):


      ![image](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/charles-cooper/eip-3860-benchmarks/tree/master/benchmark_results)





###



jumpdest analysis benchmarks. Contribute to charles-cooper/eip-3860-benchmarks development by creating an account on GitHub.

---

**chfast** (2025-04-26):

It is not explicitly mentioned in the benchmark summary what implementation is measured, but I’m guessing this is the C++ code in the same repo. I believe this would be more meaningful if existing implementations (e.g. geth, revm, nethermind). Also the benchmarks don’t necessarily target the worst cases. Depending on the implementation, the worst cases is some combination of `PUSH1`, `PUSH2` and `JUMPDEST`.

---

**chfast** (2025-04-26):

This must be coordinated with [EIP-7825](https://eips.ethereum.org/EIPS/eip-7825) (discussed in [Eip 7825: Transaction Gas Limit Cap](https://ethereum-magicians.org/t/eip-7825-transaction-gas-limit-cap/21848)) which is going to put its own limits on the both initcode and deploy code sizes.

---

**charles-cooper** (2025-04-27):

Can you specify what the worst case is? Happy to accept a pull request if some important case has been missed.

---

**jochem-brouwer** (2025-11-27):

As [@chfast](/u/chfast) mentioned this might need an update due to [EIP-7825: Transaction Gas Limit Cap](https://eips.ethereum.org/EIPS/eip-7825) introduced in Fusaka. This limits the gas limit per tx to 16777216. When deploying contracts, 200 gas per byte has to be paid for the deployment costs (and this does not cover extra costs like tx intrinsic costs, memory expansion costs, etc.). So this already puts a hard limit of maximum code size of 16777216 // 200 = 83886 bytes per transaction. Note that Pectra also got [EIP-7623](https://eips.ethereum.org/EIPS/eip-7623) (Increase calldata cost) which makes the initcode more expensive, which would also interact with the goal here.

If EIP-7907 would go live in this draft form: [EIPs/EIPS/eip-7907.md at a053474ee1e38b8eaa5058c6a3a5d51098599725 · charles-cooper/EIPs · GitHub](https://github.com/charles-cooper/EIPs/blob/a053474ee1e38b8eaa5058c6a3a5d51098599725/EIPS/eip-7907.md) (which increases initcodesize limit to 128 KiB and the max code size to 64 KiB), would this be sufficient? Would the 128 KiB initcode size and the max code size of 64 KiB (for now) be enough to also take into account the highest bytes to deploy with EIP-7825 is 83_886 bytes?

My personal line of thought would go like this: EIP-7825 puts a hard limit on code size currently. It is possible to deploy ~3-4 maximally sized contracts (of 24 KiB) after Fusaka. It is likely that if one wants to deploy 2 or more contracts then one is hindered by the initcode. I am then wondering: because of this new tx gas limit in EIP-7825 it is already somewhat clear that for multi-contract setups one should likely send multiple txs for this (this is now baked into the protocol). Is this EIP-7903 then still necessary in Glamsterdam (or a later fork?). And what if EIP-7907 would get shipped as the draft above in Glamsterdam (max code size 64 KiB and initcode size 128 KiB), would this then also alter the necessity of EIP-7903 in Glamsterdam?

