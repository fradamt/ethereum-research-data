---
source: ethresearch
topic_id: 2407
title: Sharding Validator Privacy?
author: jarradhope
date: "2018-07-02"
category: Sharding
tags: []
url: https://ethresear.ch/t/sharding-validator-privacy/2407
views: 1239
likes: 1
posts_count: 3
---

# Sharding Validator Privacy?

Yesterday at the Sharding Workshop it was suggested to use a PubSub to manage shard coordination, with a potential candidate being something like gossipsub.

The question I wanted to ask with this approach is, have we considered how the network optimisation features of gossipsub impact a Validator’s privacy? and if that has any potential implications? and if the performance gains are justified?

If Quadratic Sharding and Moore’s law gets us all we need for transactions, maybe we can look at similar reasoning here?

(apologies if this isn’t the proper medium for discussion)

## Replies

**jannikluhn** (2018-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/jarradhope/48/219_2.png) jarradhope:

> The question I wanted to ask with this approach is, have we considered how the network optimisation features of gossipsub impact a Validator’s privacy?

There have been discussions on validator privacy in p2p in general, but as far as I know not for gossipsub in particular. To start some thoughts on that topic:

The main difference between floodsub and gossipsub is that in floodsub messages spread uniformly through the network whereas for gossipsub they preferably take certain routes. Therefore, the main question from a privacy point of view is if this fact can be used to identify the source of a message. I think the answer is yes because one can probably find the routes by connecting to a lot of nodes and comparing arrival times of messages. Once you know the paths (and are able to connect to nodes on them) you can do a binary search on them to find the source of a message (or rather, a set of messages you know belong to the same validator). The difference to similar attacks on a uniform network is that searching a path is much more efficient.

Maybe one can prevent this by randomly delaying messages so that arrival times become less insightful. The attack also depends on the time it takes to setup these routes and their lifetime: If the setup takes a long time, validators who quickly jump between networks essentially don’t participate in gossipsub at all, but do plain floodsub. If the lifetime is shorter than the time it takes to identify the paths, the attack also doesn’t work.

![](https://ethresear.ch/user_avatar/ethresear.ch/jarradhope/48/219_2.png) jarradhope:

> and if the performance gains are justified?

I’d also be interested to see some numbers on the performance.

---

**mhchia** (2018-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/jarradhope/48/219_2.png) jarradhope:

> have we considered how the network optimisation features of gossipsub impact a Validator’s privacy

If the network optimization means the one from floodsub(which floods messages to all its peers) to gossipsub(which send messages only to its “eager peers”), then they should impact a Validator’s privacy in the same way because nodes send the subscription message to its peers in pubsub system in both design. However, I think other sharding p2p designs should have the similar issue, as long as they use the same peer ID in the overlay network in different shards.

![](https://ethresear.ch/user_avatar/ethresear.ch/jarradhope/48/219_2.png) jarradhope:

> and if the performance gains are justified?

Sorry, for now we don’t have the numbers. If you mean the performance gain from floodsub to gossipsub, then it should be gains, in terms of reducing redundancy.

