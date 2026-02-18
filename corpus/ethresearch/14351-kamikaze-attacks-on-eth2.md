---
source: ethresearch
topic_id: 14351
title: Kamikaze Attacks on ETH2
author: kladkogex
date: "2022-12-03"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/kamikaze-attacks-on-eth2/14351
views: 2953
likes: 0
posts_count: 3
---

# Kamikaze Attacks on ETH2

There is one type of an attack on ETH PoS, where attacker is willing to sacrifice 32 ETH slashed to potentially have a much larger gain.

If an attacker shorts a significant amount of ETH, then the potential gain from even temporarily disruption of the network can outweigh the 32 ETH loss.

I do not know if the current ETH clients have been tested against attacks like that.

The simplest attack involves the malicious proposer creating a large number of non-unique but valid block proposals, and distributing them in such a way, that each client get a different proposal.

Then you essentially get a huge number of weak branches across the network where each client will have a different world view.

The clients should in theory adjust the fork choice rule once they become aware of another block version, but looking through the source code of some ETH clients I am not sure whether this case is well handled and the corresponding mechanisms are actually implemented.

For instance, the attacker can first release only a single unique block version,  then wait until a long branch X is built on top of this block, and then flood with more non-unique versions later.

It is not clear to me how the current ETH specification handles this case, and whether the branch X needs to be invalidated in the fork choice rule after slashing, or whether the branch will stay valid and only the proposer needs to be slashed.

## Replies

**krabbypatty** (2022-12-23):

I think that it is impossible for the attacker to propose conflicting blocks without the other nodes realizing. Since blocks are gossiped in a flood protocol, eventually nodes would realize that the attacker has proposed conflicting blocks and would get slashed for violating consensus rules.

Im guessing casper would slash the attacker but ghost would probably reorg first

---

**kladkogex** (2024-06-21):

The problem is that to slash the attacker the block chain needs to be alive, and the attack makes blockchain stuck.

