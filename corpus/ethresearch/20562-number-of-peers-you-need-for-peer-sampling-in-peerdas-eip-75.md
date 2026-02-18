---
source: ethresearch
topic_id: 20562
title: Number of peers you need for peer sampling in PeerDAS (EIP-7594)
author: pop
date: "2024-10-04"
category: Networking
tags: [data-availability, p2p, scaling]
url: https://ethresear.ch/t/number-of-peers-you-need-for-peer-sampling-in-peerdas-eip-7594/20562
views: 424
likes: 4
posts_count: 3
---

# Number of peers you need for peer sampling in PeerDAS (EIP-7594)

*Authors: [pop](https://github.com/ppopth)*

*This post is based on the [current spec](https://github.com/ethereum/consensus-specs/tree/cb03c8/specs/_features/eip7594) of PeerDAS*

*Edited after [@leobago](/u/leobago)’s comment*

This post will tell you the expected number of peers each node must connect to in order to cover all the columns to do peer sampling successfully.

# Simulation

In PeerDAS, at the time of writing, the number of peers you are expected to connect to is solely calculated by `CUSTODY_REQUIREMENT` and `DATA_COLUMN_SIDECAR_SUBNET_COUNT`. We write the following simulation to count how many peers you need to connect.

```auto
import math
import random

def peer_count(N, C):
    num_trials = 1000
    counts = []
    for trial in range(num_trials):
        covered = set()
        count = 0
        while len(covered) != N:
            selected = set(random.sample(range(N), C))
            if len(selected.difference(covered)) > 0:
                covered = covered.union(selected)
                count += 1
        counts.append(count)
    return sum(counts)/len(counts)
```

where N and C are `DATA_COLUMN_SIDECAR_SUBNET_COUNT` and `CUSTODY_REQUIREMENT`, respectively.

What this function does is to simulate the node discovery mechanism. What it does in the real world is that the node will discover new peers and find out what subnets the peer is taking custody of. It will continue discovering new peers until all the subnets are covered by those peers. What’s important is that the node will not keep a peer that doesn’t add any more coverage to the subnets. So when N=32 and C=1, `peer_count` will be exactly 32.

The set of subnets each peer is supposed to custody is determined by its Peer ID. However, in our simulation, such set is just randomized, which shouldn’t be different from the real world.

In order to get the expected number, we run 1,000 simulations and get only the mean.

# Result

Trivially, if we fix C and make only N variable, `peer_count` will increase as N increases since, when there are more subnets to cover, the more peers you should have. And, if we fix N and make only C variable, `peer_count` will decrease as C increases since, when each peer custodies more, the number of peers you should have should be lower. Even if it’s trivial, we did the simulation for completeness.

[![](https://ethresear.ch/uploads/default/original/3X/1/a/1a677c4dba26c4037a17dbfa45eb905dfc3bc7dc.png)640×480 16.9 KB](https://ethresear.ch/uploads/default/1a677c4dba26c4037a17dbfa45eb905dfc3bc7dc)

[![](https://ethresear.ch/uploads/default/original/3X/d/9/d9676408f1dc84808f466a8bdade7988481bb8ce.png)640×480 17.1 KB](https://ethresear.ch/uploads/default/d9676408f1dc84808f466a8bdade7988481bb8ce)

You can see that with N=128 and C=16, you need 25.9 peers on average (so it’s far different from N/C=8).

Now, let’s consider an interesting non-trivial scenario, if the ratio (N/C) remains unchanged, do you think `peer_count` will remain unchanged? That is, do you think `peer_count(64, 8)` and `peer_count(128, 16)` will be the same? The answer is no. As shown below, the higher N is, the higher `peer_count` is.

[![Figure_3](https://ethresear.ch/uploads/default/original/3X/1/7/179da7b41d4f73f39fb90c2fc5cbdc65d32e41f0.png)Figure_3640×480 16.4 KB](https://ethresear.ch/uploads/default/179da7b41d4f73f39fb90c2fc5cbdc65d32e41f0)

So the expected number of peers you will have cannot be easily calculated with N and C. You need to do the simulation to tune the parameters.

## Replies

**leobago** (2024-10-05):

Nice analysis Pop.

This is good news; the numbers remain very low, mostly under 50 peers, when current CL clients run with over 80 peers today. See details in our blog [post](https://migalabs.io/blog/post/ethereum-hardware-resource-analysis-update).

One thing that I don’t understand in your simulation results is why the spike at C=2 when N=128. I understand that if a peer does not add anything to the custody set, it will not keep it, so I expect that every peer brings at least one more column with him. Therefore, I don’t see why you need 335 peers, with 128 should be enough, right? Am I missing something?

---

**pop** (2024-10-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/leobago/48/18496_2.png) leobago:

> I understand that if a peer does not add anything to the custody set, it will not keep it, so I expect that every peer brings at least one more column with him.

Oh shit, that makes sense. I will change the `peer_count` function and redo the work. I threw the peers away only if its whole custody set has been seen by some other peer. In fact I should throw it as well when it has been covered by all the peers. Thanks.

EDITED: Now the original post has been edited.

