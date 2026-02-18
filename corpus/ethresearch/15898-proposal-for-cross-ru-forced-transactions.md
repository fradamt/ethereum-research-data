---
source: ethresearch
topic_id: 15898
title: Proposal for Cross RU forced transactions
author: kelemeno
date: "2023-06-16"
category: Sharding
tags: [zk-roll-up, cross-shard]
url: https://ethresear.ch/t/proposal-for-cross-ru-forced-transactions/15898
views: 1296
likes: 0
posts_count: 1
---

# Proposal for Cross RU forced transactions

## Introduction

Cross-rollup interoperability is a crucial part of scaling. In particular cross RU asynchronous atomicity, i.e. forced transactions would provide the best achievable interoperability between RUs, given that synchronicity is not possible. L2s do not solve the problem, as forced txs have to go through L1, and the L1 will be bottlenecked by execution. L3s partially ease this problem, as forcing txs on an L2 will be much cheaper than on L1, so L3s are a good intermediate solution. Unfortunately, the L2 execution is still a bottleneck.

The path for cross rollup messaging is state proof bridges, as described for example [here](https://era.zksync.io/docs/dev/fundamentals/hyperscaling.html) or [here](https://vitalik.ca/general/2022/09/17/layer_3.html). Ideally, we would make these state proof bridges forcible. Otherwise, users would have to post multiple txs to multiple RUs or trust external relayers to finish their txs. Atomicity is also advantageous for smart contracts and their developers, trust assumptions are greatly reduced.

The way to do this is to utilise the DA layer, as described [here in Celestia](https://arxiv.org/abs/1905.09274): X-RU txs can be recorded and read from the DA layer. By adding ZKPs (like [Sovereign Labs](https://github.com/Sovereign-Labs/sovereign/blob/main/core/specs/overview.md)), the RUs can prove both that the txs that are sent are valid and that they are consumed in the receiving RU.

Ethereum already has plans to add a [DA layer](https://twitter.com/VitalikButerin/status/1588669782471368704/photo/1). This does not yet enable the last component of the Celestia vision: scalable X-RU forced transactions. To make this work securely and with the best possible interoperability, we need a new architecture in the current rollup-centric roadmap. This architecture needs to combine the DA layer, the shared proof, the state of the RUs, the X-RU txs, and the consensus mechanism that secures it, all in a scalable way.

## Motivation

Why do we need cheap forced transactions?

- First and foremost cheap forced txs are a security question, as if a user has some a small amount of funds in an L2, but can only access it via expensive forced tx via L1, then this will not be worth it for them. So the user effectively lost their funds.
- The alternative approach to forced transactions is Censorship Resistance of L2s. This is a good intermediate step, it would mean making the L2’s sequencer set and the locked stake large. With this approach, we can trust some of the L2 sequencers to not censor our tx. However, this is expensive as it requires lots of capital and multiple sequencers. It also penalises new rollups, it will be hard for them to boot up a trusted sequencer set.
- Finally in this context, forced transactions are equivalent to atomicity, a tx on one chain implies a tx on another chain. The RUs are not fragmented anymore. So we can say that this is also a UX problem for the users. With cross rollup forced transactions in the future, the UX of bridging will be great: cheap, fast, atomic, secure.

Full post here: [Cross Rollup Forced Transactions - Introduction - HackMD](https://hackmd.io/@kalmanlajko/BkmTTADai#Introduction)
