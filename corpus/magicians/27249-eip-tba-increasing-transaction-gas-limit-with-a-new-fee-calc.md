---
source: magicians
topic_id: 27249
title: "EIP-TBA: Increasing Transaction Gas Limit with a New Fee Calculation Rule"
author: Helkomine
date: "2025-12-20"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-tba-increasing-transaction-gas-limit-with-a-new-fee-calculation-rule/27249
views: 82
likes: 2
posts_count: 1
---

# EIP-TBA: Increasing Transaction Gas Limit with a New Fee Calculation Rule

Note: Have not created PR yet, as it is advised to get recommendations.

**Requirements**

[EIP-1559](https://eips.ethereum.org/EIPS/eip-1559), [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718), [EIP-3529](https://eips.ethereum.org/EIPS/eip-3529), [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702), [EIP-7825](https://eips.ethereum.org/EIPS/eip-7825)

**Simple Summary**

Allows transactions to specify gas limits larger than the maximum `uint24` value.

**Abstract**

Introduces a new fee calculation rule for large-sized transactions. The scope of application is restricted to specific transaction formats.

**Motivation**

[EIP-7825](https://eips.ethereum.org/EIPS/eip-7825) introduced a rigid hard cap on gas at 16,777,216 (2²⁴). This limitation prevents the construction of meta-transactions and the deployment of large-sized contracts. By introducing a softer fee calculation rule, we avoid future development barriers while still effectively mitigating DoS attacks.

**Specification**

**Parameters**

| Parameters | Value |
| --- | --- |
| COMPRESSION_RATIO | 2 |
| THRESHOLD_GAS_LIMIT | 45,000,000 |
| BLOCK_GAS_LIMIT | 60,000,000 |
| GAS_USED | unset |
| GAS_USED_IN_TX | unset |
| GAS_LIMIT | unset |
| EXECUTION_GAS_LIMIT | unset |
| GLOBAL_REFUND_GAS | unset |

**Validation Rules**

For [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718) transaction formats with `TransactionType` equal to `0x02` and `0x04`, if `GAS_LIMIT` is a `uint32`, the effective `EXECUTION_GAS_LIMIT` is determined as follows, where `/` denotes integer division rounded down:

```auto
if GAS_LIMIT <= THRESHOLD_GAS_LIMIT:
    EXECUTION_GAS_LIMIT = GAS_LIMIT
else:
    EXECUTION_GAS_LIMIT = THRESHOLD_GAS_LIMIT + (GAS_LIMIT - THRESHOLD_GAS_LIMIT) / COMPRESSION_RATIO
```

A transaction is considered invalid if `GAS_LIMIT > BLOCK_GAS_LIMIT`.

Execution follows [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) and [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702), except gas accounting uses `EXECUTION_GAS_LIMIT`, and `GAS_USED` is computed as follows:

```auto
if GLOBAL_REFUND_GAS <= GAS_USED_IN_TX / 5:
    GAS_USED = GAS_LIMIT - GLOBAL_REFUND_GAS
else:
    GAS_USED = GAS_LIMIT - GAS_USED_IN_TX / 5
```

**Rationale**

**Gas Used Equals the Specified Gas Limit**

This fee model is inspired by [Monad’s](https://docs.monad.xyz/developer-essentials/gas-pricing#gas-limit-not-gas-used) gas accounting approach, where the entire specified gas limit is consumed. This design mitigates DoS attacks that exploit extremely high gas limits with very low actual execution costs. It allows large transactions to be included in blocks while still pricing them appropriately based on the risk they introduce.

**Reasonable Scope of Application**

This EIP limits its application to type 2 and type 4 transaction formats, as the author believes these formats have the highest demand for large gas usage, while also encouraging reduced reliance on legacy formats. In the future, this rule may be extended to other formats based on real-world usage patterns.

**Explanation of Tuning Parameters**

The `COMPRESSION_RATIO` parameter increases the effective cost of gas above the defined threshold, compensating for the risk of excessive block space occupation. Gas refunds remain permitted because they return gas that was previously overcharged. Furthermore, [EIP-3529](https://eips.ethereum.org/EIPS/eip-3529) caps refunds at no more than 20% of the gas used, so this design does not introduce new attack vectors beyond those already known.

**Backwards Compatibility**

This EIP requires a hard fork, as it introduces changes to the gas fee calculation rules.

**Security Considerations**

**Reasonable Gas Limit Specification**

Because gas usage is derived from the specified gas limit, wallet interfaces must exercise extreme caution when suggesting gas limits exceeding those defined in [EIP-7825](https://eips.ethereum.org/EIPS/eip-7825).

**Parameter Tuning and Client Improvements**

In the short term, the parameters of this EIP can be adjusted to better reflect real-world conditions. In the long term, clients must be improved to handle heavier workloads resulting from transactions with very large gas limits.

**Test Cases**

The following is a list of gas usage values for transactions based on their specified gas limits:

| GAS_LIMIT | GLOBAL_REFUND_GAS | GAS_USED_IN_TX | EXECUTION_GAS_LIMIT | GAS_USED |
| --- | --- | --- | --- | --- |
| 1,500,000 | 0 | 1,000,000 | 0 | 1,000,000 |
| 2,000,000 | 0 | 2,000,000 | 0 | 2,000,000 |
| 4,000,000 | 300,000 | 2,000,000 | 0 | 1,700,000 |
| 5,000,000 | 1,200,000 | 4,000,000 | 0 | 3,200,000 |
| 18,000,000 | 0 | 18,000,000 | 18,000,000 | 18,000,000 |
| 20,000,000 | 0 | 4,000,000 | 20,000,000 | 20,000,000 |
| 24,000,000 | 2,000,000 | 23,000,000 | 24,000,000 | 22,000,000 |
| 30,000,000 | 10,000,000 | 25,000,000 | 30,000,000 | 25,000,000 |
| 48,000,000 | 0 | 40,000,000 | 46,500,000 | 48,000,000 |
| 54,000,000 | 9,000,000 | 48,000,000 | 49,500,000 | 45,000,000 |
| 60,000,000 | 30,000,000 | 50,000,000 | 52,500,000 | 50,000,000 |
