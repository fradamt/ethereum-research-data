---
source: ethresearch
topic_id: 7874
title: To what extend does Ethereum benefit from Kademlia?
author: newptcai
date: "2020-08-19"
category: Consensus
tags: []
url: https://ethresear.ch/t/to-what-extend-does-ethereum-benefit-from-kademlia/7874
views: 3944
likes: 5
posts_count: 7
---

# To what extend does Ethereum benefit from Kademlia?

I have looked into [Kademlia](https://en.wikipedia.org/wiki/Kademlia) a few years ago. It is one of the [Distributed Hash Table](https://en.wikipedia.org/wiki/Distributed_hash_table) algorithms/networks. Basically, the idea is that in a P2P network, it is infeasible for each node to know the network addresses of *all* other nodes. So instead each node just remembers a logarithmic number of other nodes called neighbors. And Kademlia guarantees that within logarithmic number of queries (exchange of messages between nodes), a node can find the actually address of a node with given ID in the network. This works quite well with [BitTorrent](https://stackoverflow.com/questions/1332107/how-does-dht-in-torrents-work).

However, as far as I understand, Ethereum is still a Proof-of-Work network and new transactions and new blocks are just flooded to the whole network. So I do not see how Kademlia can help here.

In the proposed Proof-of-Stake [Gasper protocol](https://ethresear.ch/t/confusion-about-the-definition-of-safety-in-the-gasper-protocol/7861), all messages are also simply flooded to the whole network, so I also do not see the point of using Kademlia.

So what is the reason to use Kademlia in Ethereum? Wouldn’t a network that each node simply selects a random number of other nodes to connect works equally well?

## Replies

**barryWhiteHat** (2020-08-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/newptcai/48/5106_2.png) newptcai:

> In the proposed Proof-of-Stake Gasper protocol , all messages are also simply flooded to the whole network, so I also do not see the point of using Kademlia.

IIUC ethereum uses Kademlia to pass historic data round. For example transactions that were in previous blocks. So new txs go to everyone and history state can be looked up by Kademlia methods.

I’m not an expert in this area but that i what i think happens.

---

**newptcai** (2020-08-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> IIUC ethereum uses Kademlia to pass historic data round.

Can you give me some references? Thanks.

---

**barryWhiteHat** (2020-08-20):

http://www.cs.bu.edu/~goldbe/projects/eclipseEth.pdf I am wrong. Correct answer here ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Its node discovery that uses Kademlia.

---

**mjackisch** (2020-08-20):

A question that kept me up at night, since I studied Kademlia this spring. I would argue, for the blockchain to function, Kademlia is not needed, yet it helps with being surrounded by very active peers and potentially prevents some p2p-sybil attacks. It is also used in [Swarm](https://swarm-guide.readthedocs.io/en/latest/architecture.html).

There are some good discussions about Kademlia in Ethereum in the following paper, also mentioned by the post before me: [Low-Resource Eclipse Attackson Ethereum’s Peer-to-Peer Network](https://eprint.iacr.org/2018/236.pdf).

Excerpt:

> Ethereum  inherits  most  of  the  complicated  artifacts  of the  Kademlia  protocol,  even  though  it  rarely  uses  the key property for which Kademlia was designed

---

**lithp** (2020-08-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/newptcai/48/5106_2.png) newptcai:

> So what is the reason to use Kademlia in Ethereum? Wouldn’t a network that each node simply selects a random number of other nodes to connect works equally well?

As others have mentioned, Ethereum currently uses a slightly-simplified version of Kademlia for peer discovery. It doesn’t store any data in Kademlia, it just keeps track of which peers are currently in the network. This allows it to select some random nodes and try to connect to them, as you suggest ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> IIUC ethereum uses Kademlia to pass historic data round

This is not currently true, but the #eth1x-research team [is currently looking into things](https://ethresear.ch/t/state-network-use-cases/7634) which look kind of like Kademlia for storing historical state. Currently it’s kind of a shame that we do the maximally-inefficient thing where all data is stored in every node.

---

**newptcai** (2020-08-29):

I read in this paper

> Countermeasure 1 is live as of geth 1.8.0.
> There is now a configurable upper bound on incoming
> connections, which defaults to  1/3 maxpeers = 8.

This is very strange. Since the total number of incoming and outgoing connections must be the same, the above stated 1/3 limitation means that there are going to be many nodes that cannot reach maximum number of peers.

