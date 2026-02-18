---
source: ethresearch
topic_id: 7195
title: The Eth1x64 experiment
author: axic
date: "2020-03-25"
category: The Merge
tags: [cross-shard]
url: https://ethresear.ch/t/the-eth1x64-experiment/7195
views: 4689
likes: 7
posts_count: 4
---

# The Eth1x64 experiment

# The Eth1x64 experiment

## Motivation

It has been mentioned multiple times in the past that one could just “put Eth1 on each shard” on Eth 2.0. The feasibility of this idea is yet to be proven.

Furthermore we think that this reduced design space aids a quicker turnaround and possibly the result can be reused for Phase 2 or it can reduce the to-be-explored design space.

## Goal

Design a cross-shard protocol between “Eth1 shards” with least invasive means to the EVM and current DApp best practices.

## Background

In Phase 0 [there is a process](https://github.com/ethereum/eth2.0-specs/blob/9f7a5491d749ced2f2fe9b44f2b467bb6db8c746/specs/phase0/deposit-contract.md) for “depositing” Ether from Eth1 as “Beacon Ether”, but no further integration with Eth1 is explained.

One potential way to integrate Eth1 more closely is explained by the [Phase 1.5](https://ethresear.ch/t/alternative-proposal-for-early-eth1-eth2-merge/6666) idea, to recap that briefly:

- Eth1 becomes Shard 0
- A list of Shard 0 validators is added to the beacon chain (eth1_friendly_validators) and Shard 0 validators are only chosen from this subset

Vitalik also posted a [larger diagram overviewing different areas of work on Ethereum](https://pbs.twimg.com/media/ETaj8ruWAAM1AdG?format=jpg&name=large).

Historically there has been a reluctance to introduce sizeable changes to the EVM. This has to be considered and attempt must be made to minimize changes.

## Synopsis

Take Phase 1.5 as the baseline, but extend it as:

- Each of the 64 shards contain “Eth1”
- Shard 0 contains the current Eth1 mainnet state, while other shards start with an empty state
- Change eth1_friendly_validators so that each shard has its own list

Furthermore:

- Consider current Eth1 (“Istanbul”), but assume “stateless ethereum” (e.g. block witnesses) and ignore “account abstraction” and EIP-1559
- Consider Ether on each shard to be the same token as “Beacon Ether”
- Shard validators are paid via the coinbase inside the shard and not via “Beacon Ether”

Planned features (in the following order):

1. Cross-shard Ether transfer
2. Cross-shard contract calls
3. Moving Beacon Ether from the beacon chain into shards other than the 0 shard
4. Moving Ether out of other shards than the 0 shard

Important to note that during 1) and 2) the existence of “Beacon Ether” is ignored.

## Future work

Introduce account abstraction and Webassembly into the design, which leads into Phase 2.

---

Any feedback is appreciated. The Ewasm team will explore this and report our findings.

## Replies

**jpitts** (2020-04-05):

[@benjaminion](/u/benjaminion) has comments about this proposal in his 3 April 2020 “What’s New in Eth2” update.

https://notes.ethereum.org/@ChihChengLiang/Sk8Zs--CQ/https%3A%2F%2Fhackmd.io%2F%40benjaminion%2Fwnie2_200403?type=book

---

**benjaminion** (2020-04-05):

Also see the [follow up conversation](https://twitter.com/alexberegszaszi/status/1246788852989255680) with [@axic](/u/axic) on twitter. My views on this are essentially non-technical, which is why I didn’t post them here ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=14)

---

**axic** (2020-05-07):

We have shared the first update here: [Eth1x64 Variant 1 “Apostille”](https://ethresear.ch/t/eth1x64-variant-1-apostille/7365)

