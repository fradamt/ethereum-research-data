---
source: magicians
topic_id: 26023
title: "EIP-8070: Sparse Blobpool"
author: raul
date: "2025-10-30"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8070-sparse-blobpool/26023
views: 118
likes: 1
posts_count: 3
---

# EIP-8070: Sparse Blobpool

> Discussion topic for EIP-8070 [PR]

## Description

Introduce custody-aligned sampling in the EL blobpool to vacate bandwidth.

## Abstract

This proposal introduces the sparse blobpool, a construction that brings cell-level, custody-aligned sampling in the Execution Layer (EL). For every new type 3 (blob-carrying) transaction, an EL node fetches full blob payloads only with probability p = 0.15, and otherwise it merely samples the blobs, using the same custody assignment as its Consensus Layer (CL) counterpart. For full nodes, this means downloading as little as 1/8 of the data (8 out of 128 cells), so that the average bandwidth consumption compared to the (current) full blobpool is 0.15 + 0.85/8 ~ 0.25, a ~4x reduction. The choice of p = 0.15 balances reducing bandwidth consumption with guaranteeing the full propagation of txs, by ensuring that for each blob tx there exists a large connected backbone of nodes that have the full blob payload. At an individual node level, p = 0.15 translates to 98.6% probability of least 3/50 neighbours holding the full blob payload, only 0.03% chance of total unavailability. The sampling performed with probability 1 - p = 0.85 enables streamlined data availability checks during block validation, as well as enhancing the availability of the data.

## Replies

**ADMlN** (2026-01-08):

Thanks for adding the rationale for why normative peer scoring is not a good idea. I remember that in the GossipSub paper a ‘covert flash attack’ was described, in which malicious nodes spend some time being honest to increase their peer score and then in a coordinated way one day all at once stop their message distribution / behave maliciously. I agree that adding sampling noise and actively trying to get random new peer connections (to avoid eclipse attacks) is the safest way forward

---

**kedihacker** (2026-01-13):

I don’t get how extra noise adds any security. Peers can act normally to eclipse a node then not serve more than 50 percent of a blob to block da.

