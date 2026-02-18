---
source: magicians
topic_id: 25933
title: "EIP-8058: Contract Bytecode Deduplication Discount"
author: CPerezz
date: "2025-10-23"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-8058-contract-bytecode-deduplication-discount/25933
views: 113
likes: 0
posts_count: 3
---

# EIP-8058: Contract Bytecode Deduplication Discount

Discussion topic for EIP-8058 https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8058.md

> This proposal introduces a gas discount for contract deployments when the bytecode being deployed already exists in the state. By leveraging EIP-2930 access lists, any contract address included in the access list automatically contributes its code hash to a deduplication check. When the deployed bytecode matches an existing code hash from the access list, the deployment avoids paying GAS_CODE_DEPOSIT * L costs since clients already store the bytecode and only need to link the new account to the existing code hash.
>
>
> This EIP becomes particularly relevant with the adoption of EIP-8037, which increases GAS_CODE_DEPOSIT from 200 to 1,900 gas per byte. Under EIP-8037, deploying a 24kB contract would cost approximately 46.6M gas for code deposit alone, making the deduplication discount economically significant for applications that deploy identical bytecode multiple times.

#### Update Log

- 2025/10/23: initial draft https://github.com/ethereum/EIPs/pull/10585

## Replies

**ADMlN** (2026-01-08):

> Sequential transaction execution ensures that a deployment storing new code makes it visible to later transactions in the same block

Is this EIP built on the assumption that transaction execution will forever be sequential? Will it be problematic to have this EIP in a world where we want to parallelize all tx executions of a given block?

---

**CPerezz** (2026-01-19):

This only affects the odd case where 2 txs are submitted within a block and one references in the AL the contract that another deploys within the same block.

But that’s right that this should probably be correctly specified. Otherwise it could lead to consensus issues.

Will PR! Thanks for the comment!!!

