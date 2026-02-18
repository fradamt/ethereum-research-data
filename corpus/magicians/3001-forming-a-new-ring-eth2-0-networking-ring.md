---
source: magicians
topic_id: 3001
title: "Forming a new Ring: ETH2.0 Networking Ring"
author: mikerah
date: "2019-03-26"
category: Magicians > Primordial Soup
tags: [consensus-layer, networking]
url: https://ethereum-magicians.org/t/forming-a-new-ring-eth2-0-networking-ring/3001
views: 1186
likes: 6
posts_count: 4
---

# Forming a new Ring: ETH2.0 Networking Ring

Hey,

We are finally announcing an ETH2.0 Networking Ring. We will be working on standards and requirements around the needs of ETH2.0. With the transition to Proof of Stake and the addition of sharding, we expect a new set of networking challenges. The focus of this Ring is to help with that and make ETH2.0 a reality.

You can read more here: [ETH2.0 Networking Ring · ethereum-magicians/scrolls Wiki · GitHub](https://github.com/ethereum-magicians/scrolls/wiki/ETH2.0-Networking-Ring) .

cc’ing [@atoulme](/u/atoulme) [@zscole](/u/zscole)

## Replies

**zscole** (2019-03-26):

Sweet! Definitely interested in helping push the ball forward on these initiatives. As you know, we’re currently working on implementing [Hobbits](https://github.com/Whiteblock/hobbits) in Artemis and Lodestar, but what should be our next steps?

---

**mikerah** (2019-03-27):

Here’s a rough sketch of what we need to do in the long-term:

1. Finalize Wire Protocol. We are currently using hobbits for testing and Matt Slipper has a PR with a more complete wire protocol for those with complete libp2p implementations.
2. Start modifying the beacon chain wire protocol in order to take into account shards in Phase 1.
3. Figure out networking for light clients. We can look to how current light clients in PoS networks like Cosmos handle this.
4. Figure out networking privacy. I am currently working on this with another researcher and have been onboarding him to our efforts. He should be able to contribute soon.

---

**atoulme** (2019-04-12):

Happy to participate. I will be at the core dev meeting in Berlin next week. I will present hobbits there.

