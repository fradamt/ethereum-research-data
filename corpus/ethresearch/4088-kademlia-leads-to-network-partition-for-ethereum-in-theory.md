---
source: ethresearch
topic_id: 4088
title: Kademlia leads to network partition for Ethereum in theory
author: ChengWang
date: "2018-11-02"
category: Security
tags: []
url: https://ethresear.ch/t/kademlia-leads-to-network-partition-for-ethereum-in-theory/4088
views: 2943
likes: 3
posts_count: 9
---

# Kademlia leads to network partition for Ethereum in theory

Hello guys! As far as I know, Ethereum uses a variant of Kademlia protocol. The distance of two node is based on the common prefixes of node ids (hashed actually).

In this way, the whole space of node ids are divided into two branches, one branch ids starting with 0 and another branch ids starting with 1. In theory, the nodes in branch 0 have near neighbors only from branch 0 and nodes in branch 1 have near neighbors from branch 1. Therefore, there is no neighbor connections between branch 0 and branch 1. In practice, bootstrap nodes could ease this problem.

I found this issue when I was designing my own blockchain algorithm/protocol. My fix is pretty simple as well, replacing xor metric by hamming distance, i.e. changing from `distance = id1 xor id2` to `distance = sum bits of(id1 xor id2)`. With hamming distance, the network has the same diameter as xor metric, but not partitioned.

Hope that I did not misunderstand Ethereum’s discovery protocol ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) Looking forward to discussions.

## Replies

**jannikluhn** (2018-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/chengwang/48/2628_2.png) ChengWang:

> In theory, the nodes in branch 0 have near neighbors only from branch 0 and nodes in branch 1 have near neighbors from branch 1

It is not correct that nodes only connect to other nodes “in the same branch”. There is more “space” in each node’s peer table for nodes that are closer, but this doesn’t mean that there are no nodes at all from the other branch.

---

**ChengWang** (2018-11-03):

> Blockquote
> It is not correct that nodes only connect to other nodes “in the same branch”. There is more “space” in each node’s peer table for nodes that are closer, but this doesn’t mean that there are no nodes at all from the other branch.

Branch 0 and branch 1 each has around half of the nodes in the network.

According to XOR metrics, the distance of two nodes from these two different branches is always larger than Pow(2,255), while the distance of two nodes from one same branch is always less than Pow(2,255). Therefore, closer neighbors are always from the same branch.

Of course,  a node in branch 0 will store nodes from branch 1 in it’s peer table, but those nodes are not as closer as nodes from branch 0

---

**jannikluhn** (2018-11-03):

This is all true, I’m not sure if I understand the problem. Maybe the misunderstanding is that nodes connect only to the closest nodes they know about? This is not the case, closeness is only relevant for populating the table from which peers are then selected randomly.

---

**ChengWang** (2018-11-03):

The table for nodes in branch 0 has very few nodes from branch 1, actually just one bucket in the table has nodes from branch 1. Even if peers are randomly selected, the probability of nodes from branch 1 are less likely to be selected (1 / 256). So nodes in branch 0 are still more likely to connect to nodes in branch 0. There is still the partition problem.

Thanks for pointing out random selection. I thought that only neighbors are used for connections.

---

**jannikluhn** (2018-11-03):

Only the first few buckets actually contain nodes in practice, the rest is empty because there are so few nodes that close to any given address. So the probability should be much larger than `1 / 256` when picking uniformly, but, you’re right, it’s probably less than `1 / 2` (I don’t know exact numbers unfortunately). One could account for that by adjusting the probabilities to select peers in a way that ensures a equal distribution. I don’t think clients do this and I’m not sure if it would make a noticeable difference, but it would be possible.

---

**ChengWang** (2018-11-03):

Replacing xor metrics with hamming distance could fix this issue. Network with hamming distance is more symmetric

---

**Levalicious** (2018-11-04):

The problem with replacing the xor metric with something else is that one loses Kademlia’s advantages; that is, the ability to know where to send a message for a node one isn’t connected to, knowing only their address, and without flooding the entire network. (To be honest, I don’t know if ethereum even takes advantage of this. If anyone can enlighten me that would be appreciated.)

Also, assuming I’m understanding the Kademlia paper correctly, the bucket that another node (node B) would “most easily fall into” would automatically make it closer to the other nodes it shares that bucket with. As such, it would be “easier” for B’s buckets to receive other peers, ones automatically farther from it, not the ones that node A groups it with in A’s personal routing table.

---

**ChengWang** (2018-11-04):

If we replace the xor metric with distance function that follows triangle inequality, it’s still be able to locate another node B by sending requests iteratively to k closer nodes to B. The only disadvantage is that these k closer nodes do not automatically fall into any bucket, so there is a cost to find these k closer nodes to B, but the cost is totally tolerable for hundreds of peers.

As far as I know, indeed, Ethereum does not need to locate node in its discovery protocol. The goal of discovery protocol in Ethereum is to make sure the network is randomly and evenly connected.

