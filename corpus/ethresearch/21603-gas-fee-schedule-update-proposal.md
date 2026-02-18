---
source: ethresearch
topic_id: 21603
title: Gas Fee Schedule update proposal
author: JacekGlen
date: "2025-01-27"
category: EVM
tags: []
url: https://ethresear.ch/t/gas-fee-schedule-update-proposal/21603
views: 345
likes: 2
posts_count: 3
---

# Gas Fee Schedule update proposal

Based on our [research](https://github.com/imapp-pl/gas-cost-estimator), we have devised a proposal to radically update the existing gas cost schedule. The exact proposal is available here: https://github.com/imapp-pl/gas-cost-estimator/blob/bf31b21917e399aa51bc20cec651f4d420f9191b/docs/gas-schedule-proposal.md#radical-gas-schedule-proposal.

We are working on EIP which includes those changes, but here is the place to gather some thoughts and feedback on the proposal.

## Replies

**JacekGlen** (2025-03-05):

The [EIP-7901](https://github.com/ethereum/EIPs/pull/9454) has been added. This has several changes compared to the original proposal, notably:

- no changes to LOG*
- added SLOAD, STORE
- extended security analysis
- incorporated other similar projects to the final proposal
- analysis of EIP-7667 impact

---

**JacekGlen** (2025-05-01):

Update: the EIP number has changed to [EIP-7904](https://github.com/ethereum/EIPs/pull/9454)

