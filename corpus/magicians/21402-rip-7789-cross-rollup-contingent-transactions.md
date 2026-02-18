---
source: magicians
topic_id: 21402
title: "RIP-7789: Cross Rollup Contingent Transactions"
author: shakeshack
date: "2024-10-18"
category: RIPs
tags: []
url: https://ethereum-magicians.org/t/rip-7789-cross-rollup-contingent-transactions/21402
views: 434
likes: 3
posts_count: 1
---

# RIP-7789: Cross Rollup Contingent Transactions

This proposal introduces a method to make cross-rollup transactions contingent on the shared Layer 1 (L1) history of communicating Layer 2 (L2) rollups.

Specifically, a contingency DAG is created across rollups for cross rollup transactions that is utilized to enforce a number of safety invariants.

1. Future to past communication is not allowed.
2. Communicating across L1 histories is not allowed.
3. A reorg of the originating chain from which a contingency link is created must also mean a reorg of the contingent chain.
4. A message originating from a source chain prior to reorg must not be replayable on the dependent destination chain after both chains reorg.

L2s are recommended to both track and align their L1 origins to enable faster cross L2 communication.

See the PR below for more information.

https://github.com/ethereum/RIPs/pull/40

An alternative link is provided to the markdown file w/ working image links as well.



      [github.com/polymerdao/RIPs](https://github.com/polymerdao/RIPs/blob/bo/cross-contigency/RIPS/rip-7789.md)





####

  [bo](https://github.com/polymerdao/RIPs/blob/bo/cross-contigency/RIPS/rip-7789.md)



```md
---
rip: 7789
title: Cross Rollup Contingent Transactions
description: Proposal to make cross-rollup transactions contingent on the shared L1 history across rollups.
author: Bo Du (@notbdu), Devain Pal Bansal (@dpbpolymer), Ian Norden (@i-norden)
discussions-to: https://ethereum-magicians.org/t/rip-7789-cross-rollup-contingent-transactions/21402
status: Draft
type: Standards Track
category: Core
created: 2024-10-16
---

## Abstract

This specification proposes a method to make cross-rollup transactions contingent on the shared Layer 1 (L1) history of communicating Layer 2 (L2) rollups.

The aim is to highlight the importance of L2’s tracking their L1 origins and the role it plays in the finality of a rollup. By introducing L1 origin tracking as a requirement, we define how it is utilized to establish ordering guarantees between rollups before they reach their safe or finalized stages. This enhances the reliability of cross-rollup interactions by accounting for the shared L1 context between rollups pre-finality.

## Motivation

```

  This file has been truncated. [show original](https://github.com/polymerdao/RIPs/blob/bo/cross-contigency/RIPS/rip-7789.md)
