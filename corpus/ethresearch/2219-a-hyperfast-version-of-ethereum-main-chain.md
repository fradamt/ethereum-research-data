---
source: ethresearch
topic_id: 2219
title: A hyperfast version of Ethereum main chain
author: kladkogex
date: "2018-06-12"
category: Sharding
tags: []
url: https://ethresear.ch/t/a-hyperfast-version-of-ethereum-main-chain/2219
views: 1579
likes: 4
posts_count: 12
---

# A hyperfast version of Ethereum main chain

Here is an interesting thought regarding how to make ETH main chain way faster and blocks much much larger.

The idea is to make a block much faster so that it includes only PoW, the Merkle root of the previous block and a Merkle root of everything else.

In addition, the miner should include in the block a list of “fast IP addresses”, where one can get “everything else”.

The entire block will fit into a single IP packet, and will be under 500 bytes.

Then when a node receives a block, the node will first try downloading the block from one of the “fast” IP addresses, and then only resort to gossiping as the last resort. Things will become way faster.

A miner will build a block on top of a blockchain tip only if it has the full blocks for the entire branch of the tip.

Things will become way faster since it will be in the miners interest to deploy full blocks to hypefast CDNs.

It looks like the block witholding problem will be resolved automatically since a branch with withheld blocks will not be

followed by miners.

As a result, the block size and TPS may go up hundreds of times.

Looking for someone to tear it apart ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)

## Replies

**MicahZoltu** (2018-06-12):

A miner can include a transaction and then withhold details of that transaction from everyone else so no one can prove or disprove if the Merkle roots are valid.

---

**kladkogex** (2018-06-12):

But then only this miner will be adding to this tip , so ultimately I think if the miner controls less than 50% of the mining power she will lose …

---

**mmaist** (2018-06-12):

How are these “fast IP addresses” determined? If miners can just submit an arbitrary list of IP addresses every block they mine then it seems like they’d be able to manipulate the network fairly easily.

---

**kladkogex** (2018-06-12):

The miner publishes a block to a number of IP addresses (say CDN like AWS Cloudfront) and then includes these IP addresses

I guess it should be in the miner’s interest to distribute the block as fast as possible because the miner wants the block to be in the winning branch of the blockchain (otherwise the miner wont get the mining reward)

So it seems cryptoeconomically that the system should work well …

---

**dlubarov** (2018-06-12):

CDNs could help on the egress side – a miner with little egress bandwidth could just upload their blocks to one CDN server, and rely on the CDN to propagate the block quickly. It wouldn’t necessarily need protocol changes; the CDN service could just be a well-connected hub in the network.

But isn’t ingress just as much of a bottleneck? If a node can barely keep up with current ingress bandwidth due to poor last-mile connectivity, there’s not much that can be done about that other than raising the bar for running a node.

---

**jamesray1** (2018-06-13):

We want to to reduce energy consumption and improve security with PoS. Relying on lists of fast IP addresses adds a centralization tendency.

---

**fubuloubu** (2018-06-13):

Isn’t “fast IP addresses” essentially hyperlocal? You would talk to like the 25 closest peers who have the least latency, and that would be different depending on where you are. There might be a centralization tendancy because higher bandwidth devices would get chosen most.

However, another thought is that you want the lowest latency connection that gets you the most accurate picture of the network so you’re consistent with the network and can mine faster, this might involve getting devices much further away than the “fastest” peers.

---

**jamesray1** (2018-06-13):

An attacker could create 25 nodes, publish a list of them, and then eclipse attack a connecting peer to this list of nodes.

---

**kladkogex** (2018-06-13):

I[quote=“dlubarov, post:6, topic:2219”]

f a node can barely keep up with current ingress bandwidth due to poor last-mile connectivity, there’s not much that can be done about that other than raising the bar for running a node.

[/quote]

Daniel - interesting … Do you think that CDN vs p2p would decrease    the traffic? For p2p you have lots of hops between nodes, while for CDN it is just going to be one hop.

If an average ETH transaction is 200Bytes,  1000 transactions per second would only make it 200KB download (or 1.6MBit/Sec)

Agree ?))

---

**kladkogex** (2018-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> An attacker could create 25 nodes, publish a list of them, and then eclipse attack a connecting peer to this list of nodes.

This is true … But in this case they would need to include PoW so it would cost attacker lots of money to do it for a given block …

---

**kladkogex** (2018-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> sn’t “fast IP addresses” essentially hyperlocal?

I guess for a CDN these would be IP addresses of servers close to the core internet backbone but geographically distributed … A node would chose an IP address with the fastest connection and lowest latency …

