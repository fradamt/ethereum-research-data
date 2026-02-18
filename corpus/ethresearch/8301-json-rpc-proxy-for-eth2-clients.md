---
source: ethresearch
topic_id: 8301
title: JSON-RPC proxy for ETH2 clients
author: kladkogex
date: "2020-12-02"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/json-rpc-proxy-for-eth2-clients/8301
views: 1619
likes: 0
posts_count: 2
---

# JSON-RPC proxy for ETH2 clients

Having today’s slashing on ETH2, I want to mention that it is pretty trivial for a validator to create an internal filtering network proxy to drop double-proposals.

All you need is to write a proxy server, that excepts proposals over JSON-RPC and drops the doubles using LevelDB as a proposal store.

Literally one day of work and one page of code that can potentially save you lots of money …

## Replies

**alonmuroch** (2020-12-02):

Every validator should have an up to date slashing protection db. btw you don’t need full history, we’ve implemented minimal slashing protection by tracking highest source/ target (recently merged to Prysm’s slasher)

