---
source: magicians
topic_id: 4424
title: Eth1 architecture working group
author: AlexeyAkhunov
date: "2020-07-16"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eth1-architecture-working-group/4424
views: 949
likes: 10
posts_count: 1
---

# Eth1 architecture working group

I would like to launch a working group on Eth1 implementation architecture.

**Why?**

It has been recognised that a lot of Eth1 implementations tend to become more monolithic over time, with optimisations cutting across various components. This makes it harder to study the architecture of such implementation (because it usually means studying a lot of code), and limits the extent to which implementers can specialise in specific components.

**Work**

The work that this working group would be doing at first would mostly be modelling and technical writing. would love to see modelling happening in a “guided discovery” mode, and I can be one of the guides. Other guides could be people who know details of a specific implementation but never had a chance to generalise and deepen their knowledge.

**Outputs**

Outputs will be models of various things like p2p peers, header chains, block chains, state, evm, things inbetween EVM and state etc. And hopefully these models can be used to construct a reference architecture with some form of spec, which will also define common terminology. To recap, I see 4 types of output:

1. models of entities for the architecture
2. reference architecture, which is collection of entities and data flow requirements/interfaces between them
3. terminology for the entities
4. specification describing the reference architecture
