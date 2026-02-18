---
source: magicians
topic_id: 23243
title: "EIP-7915: Adaptive mean reversion blob pricing"
author: aelowsson
date: "2025-03-24"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7915-adaptive-mean-reversion-blob-pricing/23243
views: 157
likes: 1
posts_count: 1
---

# EIP-7915: Adaptive mean reversion blob pricing

Discussion topic for [EIP-7915](https://github.com/ethereum/EIPs/blob/bc11ad22a1fa33eae7c471e4a65081a43d2ec7ba/EIPS/eip-7915.md); [PR](https://github.com/ethereum/EIPs/pull/9518).

## Abstract

Reworks the excess blob gas update in `calc_excess_blob_gas()` so that the blob base fee rises relatively more during high gas usage than it falls during low usage whenever the current fee is below the long-run average. This establishes a smoothly adapting, neutral lower bound for the base fee. The exponential moving average (EMA) is computed in the linear domain and stored as a header variable.

## Motivation

Demand for blobspace is fee-inelastic, leading to a blob base fee that may fluctuate excessively with minor shifts in aggregate demand. The lower end of the fee range of 1 wei is under current circumstances economically inconsequential, but can be reached after a period of blocks consuming fewer blobs than the target. During increases in demand, the existing fee mechanism requires sustained periods of near-full blocks to re-establish equilibrium. This exacerbates spikiness in resource consumption, which can hamper efficient scaling of throughput. Furthermore, users may intermittently need to compete in a first-price auction for inclusion, degrading UX. The appropriate fee range will inadvertently vary going forward due to changes in the ETH token price and circulating supply, as well as the protocol’s ability to scale throughput. To remain neutral and future-proof, the operational range should be established relative to the long-run average fee, smoothly adjusting equilibrium quantity of blobs consumed. Thus, this EIP introduces a new fee update mechanism that accounts for the long-run average fee when responding to shifts in demand. This allows the protocol to quickly converge to desirable equilibria while also remaining neutral and future-proof.

[![Figure 1](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5d46c4913cc26aaad437448fcf214740d8703ebd_2_670x500.png)Figure 12662×1984 262 KB](https://ethereum-magicians.org/uploads/default/5d46c4913cc26aaad437448fcf214740d8703ebd)

**Figure 1.** Response to various blob quantities for the proposed fee mechanism (green), the current mechanism (black), and a threshold mechanism (red). The mechanism smoothly converges to appropriate equilibria when demand shifts, establishing the fee relative to the long-run average base fee (at 4 gwei in this example). The fee adapts faster when converging toward the average from below than when diverging from it.
