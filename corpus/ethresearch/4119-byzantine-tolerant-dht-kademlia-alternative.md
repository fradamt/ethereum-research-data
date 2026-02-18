---
source: ethresearch
topic_id: 4119
title: Byzantine tolerant DHT/Kademlia alternative
author: MihailoBjelic
date: "2018-11-04"
category: Security
tags: []
url: https://ethresear.ch/t/byzantine-tolerant-dht-kademlia-alternative/4119
views: 2846
likes: 2
posts_count: 3
---

# Byzantine tolerant DHT/Kademlia alternative

Stumbled upon this paper today (Raul Kripalani from Protocol Labs shared it on Twitter).

It’s basically a BFT alternative to DHT-based p2p protocols.

It consists of two components: 1) attack-resilient gossip-based protocol and 2) the component that extracts uniformly random node samples from the stream of node IDs gossiped by the protocol.

The authors show that an attacker cannot create a partition between correct nodes, and prove that each node’s sample converges to an independent uniform one over time (no such properties were proven for a gossip protocol in the past).

I’m not a p2p expert and I don’t have time to check the paper in depth now, but it surely looks interesting, so I’m dropping it here hoping that it will be useful to someone, someday… ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)


      [cs.technion.ac.il](https://www.cs.technion.ac.il/~gabik/publications/Brahms-COMNET.pdf)


    https://www.cs.technion.ac.il/~gabik/publications/Brahms-COMNET.pdf

###

1473.64 KB

## Replies

**jannikluhn** (2018-11-05):

I agree, looks pretty nice! Please go here for sharding specific discussion about this: https://github.com/ethresearch/p2p/issues/3

---

**MihailoBjelic** (2018-11-05):

Oh, cool, thanks for opening the discussion! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

I’m sorry if this can’t be used for sharding (if it’s impossible to query for metadata) but anyway, GossipSub sounds like a good solution to me (again, I’m not an expert ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)).

