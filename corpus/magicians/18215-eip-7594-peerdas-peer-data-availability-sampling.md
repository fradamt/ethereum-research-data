---
source: magicians
topic_id: 18215
title: "EIP-7594: PeerDAS - Peer Data Availability Sampling"
author: hwwang
date: "2024-01-19"
category: EIPs > EIPs networking
tags: []
url: https://ethereum-magicians.org/t/eip-7594-peerdas-peer-data-availability-sampling/18215
views: 2349
likes: 6
posts_count: 3
---

# EIP-7594: PeerDAS - Peer Data Availability Sampling

Discussion topic for EIP-7594

- EIP draft: Add EIP: PeerDAS - Peer Data Availability Sampling by hwwhww · Pull Request #8105 · ethereum/EIPs · GitHub
- WIP CL specs: https://github.com/ethereum/consensus-specs/pull/3574
- Francesco’s explainer: From 4844 to Danksharding: a path to scaling Ethereum DA - Networking - Ethereum Research

## Replies

**SamWilsn** (2026-01-19):

Someone opened [a bug](https://github.com/ethereum/EIPs/issues/10498#issue-3498426513) instead of commenting here:

> In the Security Considerations section of EIP-7594, the first row shows 10^{38.36} (>1) as an upper bound on attack success probability, impossible for a probability and contradicts the narrative that probabilities “drop to a negligible amount.” Almost certainly a missing negative sign (should likely be 10^{-38.36}).

---

**SamWilsn** (2026-01-19):

Someone else opened [a bug](https://github.com/ethereum/EIPs/issues/10456):

> While reading EIP-7594 (PeerDAS), it’s not clear how many columns exist in the extended blob matrix. The document states that nodes sample 1/8 of the total data but does not explicitly indicate the total number of columns.
>
>
> The number 128 appears repeatedly in different discussion threads, but it’s unclear if this is the total number of columns or how it should adapt. Another detail is about storing and serving one extra data column for each new 32 ETH attached — the EIP doesn’t mention this either. Column count is expected to grow with validator size.
>
>
> Thanks.
>
>
> CC: @djrtwo, @fradamt

