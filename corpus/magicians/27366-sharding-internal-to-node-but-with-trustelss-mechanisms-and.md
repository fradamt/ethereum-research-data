---
source: magicians
topic_id: 27366
title: Sharding internal to node but with trustelss mechanisms and "coalition" from consensus mechanism
author: bipedaljoe
date: "2025-12-31"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/sharding-internal-to-node-but-with-trustelss-mechanisms-and-coalition-from-consensus-mechanism/27366
views: 17
likes: 0
posts_count: 1
---

# Sharding internal to node but with trustelss mechanisms and "coalition" from consensus mechanism

To me it has seemed sharding internal to node is superior to sharding in a centrally agreed on way, since nodes have different hardware and need to divide responsibility differently. There is a way to combine this idea with the sharding ideas from Vitalik Buterin (such as “stateless validation” and maybe a random extra audit like Gavin Wood does in Polkadot) and this is to let nodes internally use such mechanisms (if they want), but then you open an attack surface (which if node internally delegates by trust does not exist) as attackers can seek out and join node-as-a-team in ways that can attack the nodes. One work-around to this, could be… to use the social consensus mechanism all over again. With proof-of-stake for example, a team of 1024 people together running a node (partitioning into 1024 shards) could do delegated staking with a contract. They are elected as one validator, but they are a team in terms of the hardware their node runs on (which can be geographically distributed, just like in Vitalik Buterin’s sharding ideas). This type of idea seems to not be getting much recognition. I was banned from the Ethereum reddit for mentioning this approach to shard internal to validator. But it seems superior. If a node can manage the block alone, great. If they need to do 64 shards, let them. If they need 1024, let them. Apparently, this type of idea is taboo (why else ban for it) but it has been 11 years since Ethereum and it does not seem anyone has a good plan for scaling. And my https://doc.bitpeople.org needs someone to figure it out.

***Edit:** This can be conceptually understood as intra-validator sharding (Aptos, Sui, Ostraka) subordinating inter-validator sharding (NEAR, Ethereum). It thus combines the two dominant sharding ideas into one, and gets the best of both worlds (has exactly the rationale of both sides but in a combined model, gets the best of both). Thesis, anti-thesis, synthesis.*

[![Drawing-22.sketchpad (22)](https://ethereum-magicians.org/uploads/default/optimized/3X/8/b/8bf05099a3f40a2cc7d506578e38990d17b50dde_2_690x226.png)Drawing-22.sketchpad (22)1749×573 23.6 KB](https://ethereum-magicians.org/uploads/default/8bf05099a3f40a2cc7d506578e38990d17b50dde)
