---
source: magicians
topic_id: 4385
title: Improving Network Resilience Despite a Supermajority Client
author: matt
date: "2020-06-26"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/improving-network-resilience-despite-a-supermajority-client/4385
views: 739
likes: 3
posts_count: 1
---

# Improving Network Resilience Despite a Supermajority Client

*TLDR: If Geth had multiple implementations of consensus critical code paths (e.g. EVM, state root calculation, etc) that were chosen randomly for use during each block, we could force* diversity into an environment that wants to run a single client.

–

There was a great discussion in [ACD 90](https://github.com/ethereum/pm/issues/189) regarding the burnout client developers face due to the unending protocol upgrades and maintenance tasks. It was noted that client diversity helps reduce this to a degree, because in a world with many clients, one failing would not lead to a catastrophic failure where the majority of the network follows an invalid fork.

Geth currently accounts for [76% of all mainnet clients](https://www.ethernodes.org/). There are numerous different ways to understand why that is the case and how to best address it. I’ll leave that for another discussion. My assumption is that this is the world we live in *now* and we will likely *continue* to live in a world with a single supermajority client for some time – so how can we build a more resilient network?

A supermajority client implies the need for 100% correctness of its consensus critical code paths. In other words, the supermajority client must be fault tolerant to maintain correctness and availability. Traditionally, non-byzantine fault tolerance is achieved via replication, redundancy, and/or diversity. In terms of achieving fault tolerance in software, only the latter is really applicable because i) code is deterministic, so running identical implementations will lead to identical results and ii) redundancy is already addressed in the consensus protocol.

Fault tolerant software is [not a new concept](https://dl.acm.org/doi/pdf/10.1145/356678.356681) and has been explored in many industries where high-availability is paramount. I think there is a lot of potential for integrating some of their paradigms into our client development. For example, suppose Geth dynamically loaded three different EVM implementations (via EVMC) and randomly chose a new implementation each time an interpreter was constructed. Given the distribution of Geth clients, now for a catastrophic failure to occur 2/3 of the implementations would need to incur a fault for the same input.

I’m curious to hear others’ thoughts on this, especially regarding feasibility. Not only would it be an enormous undertaking, it would slow down development by a factor of 2-3x, and require a significant growth in headcount on the Geth team. The positive aspect is that we can improve the diversity of the network *ourselves* without needing to convince hobbyist and companies to choose less popular implementations.
