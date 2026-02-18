---
source: magicians
topic_id: 26450
title: "EIP-8075: Adaptive state cost to cap growth & scale L1"
author: aelowsson
date: "2025-11-06"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-8075-adaptive-state-cost-to-cap-growth-scale-l1/26450
views: 88
likes: 0
posts_count: 1
---

# EIP-8075: Adaptive state cost to cap growth & scale L1

Discussion topic for EIP-8075; [PR](https://github.com/ethereum/EIPs/pull/10689)

#### Description

Track state bytes and target 250 MiB/day by dynamically adjusting the state gas cost. Exempt state from the gas limit to facilitate scaling.

#### Relevant resources

- EIP-8075 execution-spec.
- EIP-8037
- Discussion about EIP-8037 with relevant conversation starting here.
- Separate PR for repricing state gas with gas limit.

### Abstract

This EIP precisely caps state growth while at the same time facilitating between 50%-300% more non-state operations per block compared to when solely raising the state gas cost. The cap is achieved by tracking state creation and having a dedicated EIP-4844 style fee market mechanism set the cost, to target 250 MiB per day. To preserve the existing transaction format and EVM execution patterns, state is still priced in gas during transaction processing. The state creation gas cost is updated every block, adjusting slowly so that users can set reasonable gas limits. The byte-level harmonization of state creation operations provided by EIP-8037 are then still applied. To facilitate scaling, state creation and regular gas have separate limits, but a normalized aggregate gas is used when calculating the base fee.
