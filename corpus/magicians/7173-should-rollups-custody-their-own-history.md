---
source: magicians
topic_id: 7173
title: Should rollups custody their own history?
author: samueldashadrach
date: "2021-09-30"
category: Uncategorized
tags: [ethereum-roadmap, layer-2]
url: https://ethereum-magicians.org/t/should-rollups-custody-their-own-history/7173
views: 1007
likes: 0
posts_count: 1
---

# Should rollups custody their own history?

Off-shoot from my earlier post requesting [tighter integration between rollups and shards](https://ethereum-magicians.org/t/rollup-centric-ethereum-with-sharding-or-rollup-centric-sharding/7159)

Here’s a simple (not necessarily best) way of doing this.

Validators follow the 64-shard spec as designed. 64 subnets exist and shard nodes exist for each subnet, same as always. Shard nodes defend security as they always do. Tight coupling exists, there is social pact to not accept chain if blocks from even one shard are unavailable.

However, rollup nodes also exist. Rollup nodes only store those L1 blocks which contain calldata required by the rollup. (Assume for now an L1 block either contains only calldata of one rollup, or other data, not a mix of both.) And they store headers of all other blocks. Each rollup also has its own topic for gossip network, call it a subnet - there is no restriction to how many subnets can be created. These subnets are not initially enshrined in ethereum protocol, though they use official source code.

A rollup node who wants to sync to one specific rollup can

- get full copy of blocks relevant to rollup from rollup node
- DAS with other shard nodes if they feel like
(ofcourse they can get these blocks from the shard nodes too - this is their choice)

Once rollup nodes for a specific rollup have become large in number, it might make sense for shard nodes to start dropping those blocks. A node who wishes to sync can now get those blocks from the rollup nodes instead of the shard nodes. Rollup nodes are now responsible for data availability of those blocks and consensus-critical. The point at which shard nodes decide rollup nodes are *enough in number* to make this switch is entirely up to the shard nodes.

Pros

1. Rollup nodes have more altruistic capacity because they care more about the blocks they store. This proposal takes advantage of this capacity.
2. Once a rollup has enough economic activity and enough altruistic capacity built (enough rollup nodes storing blocks for the rollup), it frees up the altruistic capacity of the shard nodes. For other shards or potentially even for new shards. Nodes can now more naturally load-balance and pick which blocks to store because blocks are now grouped semantically and based on economic value.
3. This opens up future possibility to make more changes than enshrine rollups - either in consensus or outside of it. For instance since rollups have their own subnets, it could at some point make sense for networking client to be forked off and worked on independently (like how execution and consensus clients are currently separated). It may also be easier to later make any consensus-level changes that benefit specific rollups if all this infrastructure exists.
4. Adding to previous point, modularity also good because it splits development work across teams.
5. Most importantly it allows a graceful transition into this, instead of the extremes of a) baking rollups into consensus right at the start b) never letting rollups have any control over the lower layers they build upon c) mandating hard fork as a way of enshrining rollup when it achieves “big boy” status. Nodes instead provide soft signalling by choosing to run nodes for rollups they care about. Group intelliegence for load balancing outside of in-protocol consensus.

Cons

1. Complexity++
2. Does not allow ethereum to easily transition to zero-governance.
