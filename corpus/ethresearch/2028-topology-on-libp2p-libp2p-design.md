---
source: ethresearch
topic_id: 2028
title: Topology on libp2p ( libp2p design )
author: ghasshee
date: "2018-05-18"
category: Meta-innovation
tags: [p2p]
url: https://ethresear.ch/t/topology-on-libp2p-libp2p-design/2028
views: 2730
likes: 12
posts_count: 7
---

# Topology on libp2p ( libp2p design )

Is there any place for discussion or fundamental base knowledge for

topology on libp2p, or could I open it here?

Casper protocol seems to have update system of ‘validator topology’.

And my question is that does libp2p which is more underlying layer have a similar system ?

## Replies

**vbuterin** (2018-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/ghasshee/48/3904_2.png) ghasshee:

> Casper protocol seems to have update system of ‘validator topology’.

Casper does not make any assumptions about network topology; it assumes a gossip network just like PoW. It’s sharding that has stronger network topology assumptions for scalability reasons.

---

**hwwhww** (2018-05-20):

Regarding (i) sharding topology and (ii) main chain transport layer on libp2p, here’s the new GH issue: https://github.com/libp2p/libp2p/issues/33

---

**jamesray1** (2018-05-20):

Thanks for the link Hsiao-Wei!

---

**jamesray1** (2018-05-20):

PS until we have a separate category for P2P, it’s probably best to categorize P2P posts under sharding (or Casper if it’s specific to that). I know Casper FFG alpha uses Kademlia and bootstrapping nodes, but I don’t know much more about their specific P2P implementation.

---

**ghasshee** (2018-05-21):

My purpose is a bit different, maybe as [@vbuterin](/u/vbuterin) implied by the term ‘gossip’;

I would like to research the way of updating the whole network topology as there are no stable neighbors.

( I took casper as sharding, as [@vbuterin](/u/vbuterin) mentioned. )

---

**jamesray1** (2018-07-05):

I have been reading up on [gossipsub](https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/README.md) for developing it for rust-libp2p, and suggest that you check that out.

