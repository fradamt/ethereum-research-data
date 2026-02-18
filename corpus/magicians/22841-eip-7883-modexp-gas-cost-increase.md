---
source: magicians
topic_id: 22841
title: "EIP-7883: ModExp Gas Cost Increase"
author: benaadams
date: "2025-02-12"
category: EIPs > EIPs core
tags: [core-eips]
url: https://ethereum-magicians.org/t/eip-7883-modexp-gas-cost-increase/22841
views: 268
likes: 1
posts_count: 9
---

# EIP-7883: ModExp Gas Cost Increase

Discussion topic for https://eips.ethereum.org/EIPS/eip-7883

## Replies

**wjmelements** (2025-02-13):

That link is 404 Not Found

---

**shemnon** (2025-02-13):

PR - [Add EIP: ModExp Gas Cost Increase by marcindsobczak · Pull Request #9356 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9356/files)

The link will work one day.

---

**jochem-brouwer** (2025-05-10):

For transparency of this EIP (and process), where can we find the benchmarks such that it can be reproduced that the precompile is underpriced and we thus need a raise?

---

**jochem-brouwer** (2025-05-13):

Since [EIP-7823: Set upper bounds for MODEXP](https://eips.ethereum.org/EIPS/eip-7823) will limit the inputs (to max 1024 bytes length) does this impact the relevant benchmarks which lead to the repricing for this EIP? If the decrease in performance was only noticeable at >> 1024 bytes length then this EIP in combination with 7823 might not be necessary? Would also like to see these benchmarks to see on which inputs these benchmarks ran on. Thanks ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**chfast** (2025-05-29):

I’ve benchmarked [evmone](https://github.com/ethereum/evmone) with [GMP](https://gmplib.org/) as the modexp precompile implementation. All numbers are for x86-64-v3 CPU with 4.0GHz frequency.

The inputs having the lowest gas rate are from the edge of the minimal cost of 500 gas.

| mod len (bytes) | exp len (bytes) | gas rate (Mgas/s) |
| --- | --- | --- |
| 8 | 110 | 65.37 |
| 16 | 40 | 109.51 |
| 24 | 22 | 147.00 |
| 32 | 12 | 165.08 |

The below chart gives the overview of the bigger picture with the series of fixed mod lens:

- 32 bytes (lowers)
- 64 bytes
- 1024 bytes (highest)

[![EIP7883 gas rate of GMP modexp](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4014fffb27a2a84ab001ffe540ad86709460226f_2_690x427.png)EIP7883 gas rate of GMP modexp2016×1248 119 KB](https://ethereum-magicians.org/uploads/default/4014fffb27a2a84ab001ffe540ad86709460226f)

In this context the formula works good for in long ranges (the curves flatten). The cheapest usage range (within 32 bytes of all arguments) is also [the most common one](https://github.com/hugo-dc/modexp_analysis/blob/master/modexp.ipynb).

We plan to introduce a in-house implementation of the modexp precompile to evmone. It may help with the performance in the low ranges but nothing is promised.

---

**chfast** (2025-06-02):

Pointing the execution around the minimal cost of 500 gas still gives some badly performing inputs.

I.e. the a short mod/base length we pick the longest exponent giving the cost of ~500 gas.

The worst is the single word (8 byte) long mod.

The rough performance estimation is ~30 Mgas/s for Geth ~40 Mgas/s for Besu.



      [github.com/ethereum/execution-spec-tests](https://github.com/ethereum/execution-spec-tests/pull/1701#issuecomment-2931341464)














#### Comment by
         -


      `main` ← `ipsilon:bench/modexp`







# Benchmark results

## Geth

```
evm statetest --bench fixtures/state_test[…](https://github.com/ethereum/execution-spec-tests/pull/1701)s/zkevm/worst_compute/worst_modexp.json
{"stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b"}
{"stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b"}
{"stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b"}
{"stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b"}
[
  {
    "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Prague-state_test-worst_16b]",
    "pass": true,
    "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
    "fork": "Prague",
    "benchStats": {
      "time": 1896936828,
      "allocs": 7733204,
      "bytesAllocated": 369552608,
      "gasUsed": 72000000
    }
  },
  {
    "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Prague-state_test-worst_24b]",
    "pass": true,
    "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
    "fork": "Prague",
    "benchStats": {
      "time": 1544172220,
      "allocs": 6300260,
      "bytesAllocated": 352070248,
      "gasUsed": 72000000
    }
  },
  {
    "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Prague-state_test-worst_32b]",
    "pass": true,
    "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
    "fork": "Prague",
    "benchStats": {
      "time": 1070321751,
      "allocs": 2734510,
      "bytesAllocated": 169097072,
      "gasUsed": 72000000
    }
  },
  {
    "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Prague-state_test-worst_8b]",
    "pass": true,
    "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
    "fork": "Prague",
    "benchStats": {
      "time": 3480719806,
      "allocs": 9704896,
      "bytesAllocated": 394419552,
      "gasUsed": 72000000
    }
  }
]
```

## Besu

```
besu-evm state-test fixtures/state_tests/zkevm/worst_compute/worst_modexp.json
{"output":"","gasUsed":"0x44aa200","time":1709787127,"Mgps":"42.111","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Prague-state_test-worst_16b]","fork":"Prague","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
{"output":"","gasUsed":"0x44aa200","time":1014152314,"Mgps":"70.995","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Prague-state_test-worst_24b]","fork":"Prague","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
{"output":"","gasUsed":"0x44aa200","time":699856359,"Mgps":"102.878","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Prague-state_test-worst_32b]","fork":"Prague","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
{"output":"","gasUsed":"0x44aa200","time":2901106964,"Mgps":"24.818","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Prague-state_test-worst_8b]","fork":"Prague","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
```

---

**chfast** (2025-06-03):

In the [EIP Test Cases](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7883.md#test-cases) the benchmarks for the short base/mod lengths are not exactly the worst cases.

They should be updated to the ones having the longest exponent for a given short mod within the fixed gas cost budget.

Specifically, test cases `marcin-{1,2,3}-exp-heavy` should be modified in the following way:

- increase the exp length to the maximum within ~500 gas cost,
- set base different than mod; currently base equals mod which gives 0; it looks like some implementation (e.g. Besu) exploit the fact of multiplying by 0,
- set the mod to an even number,
- trim the trailing zeros of the input; in the proposal below we set the mod to 0xffff..ff00.

Proposed test cases replacements and additions:

```auto
pawel-1-exp-heavy:
0x000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000700000000000000000000000000000000000000000000000000000000000000008ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
pawel-2-exp-heavy:
0x000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000280000000000000000000000000000000000000000000000000000000000000010ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
pawel-3-exp-heavy:
0x000000000000000000000000000000000000000000000000000000000000001800000000000000000000000000000000000000000000000000000000000000150000000000000000000000000000000000000000000000000000000000000018ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
pawel-4-exp-heavy:
0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000020ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
```

Comparison between `marcin-...` and `pawel-...` variants (the lower Mgps the better):

- Geth

```
    [
      {
        "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-marcin-1-exp-heavy]",
        "pass": true,
        "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
        "fork": "Osaka",
        "benchStats": {
          "time": 1696246946,
          "allocs": 4916707,
          "bytesAllocated": 227783496,
          "gasUsed": 72000000
        }
      },
      {
        "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-pawel-1-exp-heavy]",
        "pass": true,
        "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
        "fork": "Osaka",
        "benchStats": {
          "time": 2312206593,
          "allocs": 6673111,
          "bytesAllocated": 262594608,
          "gasUsed": 72000000
        }
      },
      {
        "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-marcin-2-exp-heavy]",
        "pass": true,
        "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
        "fork": "Osaka",
        "benchStats": {
          "time": 1668483227,
          "allocs": 3053372,
          "bytesAllocated": 175740232,
          "gasUsed": 72000000
        }
      },
      {
        "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-pawel-2-exp-heavy]",
        "pass": true,
        "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
        "fork": "Osaka",
        "benchStats": {
          "time": 1634767138,
          "allocs": 6907475,
          "bytesAllocated": 323495592,
          "gasUsed": 72000000
        }
      },
      {
        "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-marcin-3-exp-heavy]",
        "pass": true,
        "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
        "fork": "Osaka",
        "benchStats": {
          "time": 1238461037,
          "allocs": 3273356,
          "bytesAllocated": 217249888,
          "gasUsed": 72000000
        }
      },
      {
        "name": "tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-pawel-3-exp-heavy]",
        "pass": true,
        "stateRoot": "0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b",
        "fork": "Osaka",
        "benchStats": {
          "time": 1604264770,
          "allocs": 6662585,
          "bytesAllocated": 366018400,
          "gasUsed": 72000000
        }
      }
    ]

```
- Besu

```
  {"output":"","gasUsed":"0x44aa200","time":300591521,"Mgps":"239.528","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-marcin-1-exp-heavy]","fork":"Osaka","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
  {"output":"","gasUsed":"0x44aa200","time":1799100921,"Mgps":"40.020","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-pawel-1-exp-heavy]","fork":"Osaka","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
  {"output":"","gasUsed":"0x44aa200","time":108400040,"Mgps":"664.206","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-marcin-2-exp-heavy]","fork":"Osaka","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
  {"output":"","gasUsed":"0x44aa200","time":1168371163,"Mgps":"61.624","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-pawel-2-exp-heavy]","fork":"Osaka","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
  {"output":"","gasUsed":"0x44aa200","time":132789271,"Mgps":"542.212","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-marcin-3-exp-heavy]","fork":"Osaka","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}
  {"output":"","gasUsed":"0x44aa200","time":976736105,"Mgps":"73.715","test":"tests/zkevm/test_worst_compute.py::test_worst_modexp[fork_Osaka-state_test-pawel-3-exp-heavy]","fork":"Osaka","d":0,"g":0,"v":0,"stateRoot":"0x1d3c59311b602ed6cdbb8766efb327a88c7764cb788f2ffbe9deef6b8d61ff7b","postLogsHash":"0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347","pass":true,"error":"Out of gas"}

```

---

**chfast** (2025-06-03):

Based on the above, I’ve proposed the following spec update: [Update EIP-7883: Assume minimal base/mod length of 32 by chfast · Pull Request #9855 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9855).

