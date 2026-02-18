---
source: magicians
topic_id: 25693
title: "EIP-8038: State-access gas cost update"
author: misilva73
date: "2025-10-07"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8038-state-access-gas-cost-update/25693
views: 140
likes: 1
posts_count: 3
---

# EIP-8038: State-access gas cost update

Discussion topic for [EIP-8038](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8038.md); [Web](https://eips.ethereum.org/EIPS/eip-8038);

#### Abstract

This EIP updates the gas cost of state-access operations to reflect Ethereum’s larger state and the consequent slowdown of these operations. It raises the base costs for `GAS_STORAGE_UPDATE`, `GAS_COLD_SLOAD`, and `GAS_COLD_ACCOUNT_ACCESS` and updates the access cost for `EXTCODESIZE` and `EXTCODECOPY`. The design coordinates with EIP-8032: before EIP-8032, parameters assume worst-case contract size; after EIP-8032, they assume worst-case up to `ACTIVATION_THRESHOLD`, with additional depth-based scaling beyond.

## Replies

**sbacha** (2025-10-10):

what are the potential metric targets for benchmarking across clients, what should we see pre a d post ideally?

---

**misilva73** (2025-10-13):

One of the goals would be to have [these statefull tests](https://github.com/ethereum/execution-specs/blob/forks/osaka/tests/eest/benchmark/test_worst_stateful_opcodes.py) performing at the same million gas per second target (or close enough), accounting for the added cost of state creation. Of course, SSTORE will not have the same million gas per second performance as SLOAD since it also includes a state creation cost component.

Also, state access operations should be harmonized with other compute operations. So [these tests](https://github.com/ethereum/execution-specs/blob/forks/osaka/tests/eest/benchmark/test_worst_compute.py) should also have similar million gas per second performances.

