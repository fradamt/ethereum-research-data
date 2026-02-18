---
source: ethresearch
topic_id: 1720
title: Torus-shaped sharding network
author: jannikluhn
date: "2018-04-13"
category: Sharding
tags: [p2p]
url: https://ethresear.ch/t/torus-shaped-sharding-network/1720
views: 6313
likes: 10
posts_count: 9
---

# Torus-shaped sharding network

#### Tl;dr:

Instead of using one network per shard, use a single network, but limit propagation of messages between nodes interested in different shards.

#### Problem

A single p2p network in which all messages are broadcasted to everyone is obviously unsuitable for sharding, as it’s opposed to the goal of distributing workload. However, the alternative of having one network per shard has the disadvantage that notaries, whenever they are assigned to a shard, need to connect to a new network. At least with the current devp2p protocol, this takes a long time and thus lower bounds the period length as well as the lookahead length. libp2p might bring improvements here, but this is untested and reconnecting won’t be free either.

In order to connect to a new shard network more quickly, notaries might rely on bootstrapping nodes. This is dangerous though as those would be an easy target for DoS attacks that could temporarily stop notarization for a specific shard.

A separate issue may be that the behavior of rapidly reconnecting to new networks whenever a new period starts is a way to identify notaries, making them a target for DoS attacks aiming to, for instance, censor certain proposals.

As a result of above points, notaries benefit from being constantly well connected to all shard networks. This is a centralization risk as participating in many networks is quite costly bandwidth-wise, likely requiring notaries to be run in data centers.

#### Proposed solution

A solution to these problems could look like this: Use a single network in which nodes are placed on the surface of a torus. A node’s ID defines the “poloidal” (red circle in the Wikipedia illustration below), the shard id the “toroidal” angle. All messages are transmitted as usual in the poloidal direction as the nodes on the ring care about the same shard. In the toroidal direction however, only messages of interest to notaries are relayed (mainly new collations, but not, for instance, transactions). In addition, those toroidal messages are transmitted only across a certain number of shards (say, 5).

[![image](https://ethresear.ch/uploads/default/optimized/2X/e/e3471d1a35550fcec2f426983e330c8687da5c20_2_666x500.png)Toroidal_coord.png1024×768 121 KB](https://ethresear.ch/uploads/default/e3471d1a35550fcec2f426983e330c8687da5c20)

#### Discussion

Compared to the naive single network approach, this type of network has the advantage of only increasing the bandwidth requirements of each node by a little (essentially, only by some collations of neighboring shards which neither have to be validated nor stored permanently). Compared to the one-network-per-shard apprach, this allows notaries to require less reconnections as it’s possible to be close to a shard (instead of either being connected or not) and being close leads to receiving collations (albeit with higher latency).

Another tweak one could add is making the notary sampling mechanism give “hints” for future samples: Notaries could get bits of information like “if I get sampled at all then I get sampled for some shard in the range 25 to 45”, possibly narrowing it down over time. This would allow notaries to make sure that they are propably close to the right shard prior to actually being sampled.

## Replies

**prestonvanloon** (2018-04-13):

In this paradigm, nodes interested in a single shard n will accept connections from peers interested in shard n as well as peers interested in shard (n-1)\mod100 and (n+1) \mod 100? Then that node would act as a relay to propagate messages that aren’t relevant to their shard n? Wouldn’t that increase overall bandwidth for these nodes with no incentive to act as a relay?

I’m also thinking about a scenario when a given node wants to connect to 20 nodes on distinct shards and I think that this node will have a hard time maintaining these connections since it will be mostly or entirely leaching messages without offering any new messages. This would happen when a node has only distinct shard connections and none of those connections act as a relay for other shards.

---

**jannikluhn** (2018-04-13):

> Wouldn’t that increase overall bandwidth for these nodes with no incentive to act as a relay?

Yes, but we can assume nodes to be somewhat altruistic (or rather interested in a healthy network).

Even in the current Ethereum network there is no incentive to relay other nodes’ transactions, but they still do it.

> I’m also thinking about a scenario when a given node wants to connect to 20 nodes on distinct
> shards and I think that this node will have a hard time maintaining these connections since it
> will be mostly or entirely leaching messages without offering any new messages.

Good point. Can you by chance point me to resources how reputation is handled in today’s network?  I

couldn’t find anything on that. In particular, is leaching actually reducing reputation or just

straight up “lying” to one’s peers?  I’m asking because for instance just syncing a chain is

leaching as well, but obviously not punished. Asking for collations could be treated similarly.

What one could do is challenge such nodes. This doesn’t make them more useful but at least ensures

that they are connected to other shards as well and probably are doing something useful for the

network (being notaries). That would remove the notary stealthness property unfortunately. A challenge could look like this: “You’re saying you’re connected to shard 24, 44, 64, …, please provide the collation in the latest period of shard 26 (or a proof of custody)”.

---

**fubuloubu** (2018-04-13):

I had a thought in a similar vein, but instead of creating a new post I figured I would respond to this one.

There is already a massively scalable infrastructure we can copy for managing broadcasting infrastructure at scale in a high-usage network: cellular networks. It allows the network to “shard” itself into different cell towers with different coverage, and varies the operating frequencies optimally to maintain the coverage without interference. Each tower has a maximum amount of channels it can support, but at scale the network is obviously able to handle billions of devices.

I took a survey course in grad school on cell networks, I think I can probably drag up some research papers if anyone is interested in that parallel and using it to design Ethereum’s sharding updates.

---

**prestonvanloon** (2018-04-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Even in the current Ethereum network there is no incentive to relay other nodes’ transactions, but they still do it.

I think clients do (or should do) detect leaching peers and disconnect them. This is an incentive to relay messages otherwise no one will relay to you.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Can you by chance point me to resources how reputation is handled in today’s network?

I’m actually not certain where this is done. I learned it from offline discussions with Peter and Felix in Taipei. I think this is the code handling “idle” (what I call leeching) peers [go-ethereum/eth/downloader/peer.go at 7aad81f8815084c8ed032705fbaf6d3710e518cf · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/blob/7aad81f8815084c8ed032705fbaf6d3710e518cf/eth/downloader/peer.go).

I *think* there is also some mechanism for rejecting peers that are consistently sending bad data or on the wrong chain, but I don’t know where that is off the top of my head.

Peer reputation is important to consider since clients default to 25 max peers (at least for go-ethereum) so clients want to ensure that these are quality peers. If some percentage of these peers are on shards that are not interesting to the client, then those peers may be considered quality peers. However, we do allow this type of leeching activity with light clients. Perhaps there is another layer of light client communication protocol that notaries can use?

---

**FrankSzendzielarz** (2018-04-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> need to connect to a new network. At least with the current devp2p protocol, this takes a long time

Hello Jannik. Please could you clarify this quote for me? I am a little uncertain what mechanism you have in mind there. As I understand it, even now, nodes will need to support multiple discovery protocols (v4, v5), so it is conceivable that while *connections* between nodes form the toroid, notaries may use a peer discovery mechanism to cast a wide net, so to speak. Then, if I am not mistaken, ‘joining’ a network is just a question of running the rlpx handshake.

Also, bootnodes aren’t really 100% necessary to join a network if the peer discovery mechanism allows nodes to cache previously discovered, reliable nodes with significant uptime.

---

**jannikluhn** (2018-04-15):

> I think I can probably drag up some research papers if anyone is interested in that parallel and
> using it to design Ethereum’s sharding updates.

Sounds interesting! The most fundamental difference is probably that cellular networks are centralized and we’re p2p, and my guess is that this changes a lot. But would still love to read a nice introduction/review/overview paper on that topic if you could link to one!

> Please could you clarify this quote for me?

Not really, unfortunately ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12) All I’ve heard is that “connecting to a network takes time”, and so I tried to find a way to avoid it. It’s possible that we won’t have these issues with a global peer discovery mechanism, I don’t know. I’m also not sure if global peer scales well enough (after all we’re trying to increase the network size by 100).

> Also, bootnodes aren’t really 100% necessary to join a network if the peer discovery mechanism
> allows nodes to cache previously discovered, reliable nodes with significant uptime.

I guess that depends on the frequency at which a notary is sampled (or rather the time a notary is selected for the same shard again). We don’t really have an estimate on that quantity yet as far as I know, so it’s hard to make predictions. By the way, it doesn’t really matter if they are called bootnodes or nodes with significant uptime, the point is that they are few and easy to identify, so single-points-of-failure. But with a global peer discovery this is probably not an issues at all.

---

**jamesray1** (2018-04-17):

Hmm yeah, I think we should incentivize acting as a relay e.g. with [Incentivizing a Robust P2P Network/Relay Layer](https://ethresear.ch/t/incentivizing-a-robust-p2p-network-relay-layer/1438/19). But with such incentives, I think this model is worth further consideration vs 100 separate P2P networks.

---

**jamesray1** (2018-07-11):

Starting development of gossipsub after doing a lot of reading. Note that a node doesn’t have to broadcast a message to all peers in the network, as is the case in gossipsub. A node can connect to a limited set of peers, and messages are propagated via a mesh network. For more details on gossipsub, see [specs/pubsub/gossipsub at master · libp2p/specs · GitHub](https://github.com/libp2p/specs/tree/master/pubsub/gossipsub).

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> However, the alternative of having one network per shard has the disadvantage that notaries, whenever they are assigned to a shard, need to connect to a new network. At least with the current devp2p protocol, this takes a long time and thus lower bounds the period length as well as the lookahead length. libp2p might bring improvements here, but this is untested and reconnecting won’t be free either.

Would be good to experiment with both approaches and compare. [Floodsub is already implemented for libp2p implementations and gossipsub is implemented with Go](https://github.com/libp2p/specs/tree/master/pubsub).

One issue with gossipsub as currently designed is that the initial parameter for the maximum number of nodes is 10,000. More details on this is at [Maximum number of nodes in a gossipsub network. · Issue #86 · libp2p/go-libp2p-pubsub · GitHub](https://github.com/libp2p/go-floodsub/issues/86).

