---
source: ethresearch
topic_id: 4986
title: State of networks research/SD-WAN for blockchains
author: stephanthecynic
date: "2019-02-12"
category: Applications
tags: []
url: https://ethresear.ch/t/state-of-networks-research-sd-wan-for-blockchains/4986
views: 1359
likes: 1
posts_count: 1
---

# State of networks research/SD-WAN for blockchains

I have been looking into BloXroute and feel an idea such as that makes sense. Traditional internet performance has been a result of both better compression tech as well as a lot of behind the scenes networking tech - CDNs, leased lines, MPLS. The latest in the space is SDWANs of course. Better networking can bring down worst-case latencies for packet propagation across the network. I am not convinced though that decentralized protocols should rely on a service provided solely by AWS or Akamai or even BloXroute (which is basically just a centralized company renting machines at AWS and could completely screw fork rates at will by suddenly introducing propagation delays once block times have been reduced).

The defacto protocol used today is gossip. While I understand the importance of the topology being structureless in providing redundancy and robustness, it surely does compromise on performance and leaves networking to chance and uncertainty. As an example, a study found that most Bitcoin miners ran on 13 ISPs (0.026 percent of all ISPs). Similarly, studies have shown that eclipse attacks on miners cost next to nothing. So despite gossip giving us a (false?) belief of redundancy, miners continue to be vulnerable to partitioning (after all submarine cables are owned by a handful of companies).

Inspired by the discussion at [1] and computational sharding, I was wondering if it makes sense to look at networking too from a crypto-economic perspective. This could possibly provide benefits in terms of both security as well as performance. Just as validators in Casper, a select set of nodes chosen via a RNG could be responsible for forming a high-performance global multicast group. The number of nodes chosen every interval could factor in the required level of redundancy (as suggested by [@phil](/u/phil) in [1], they could even be in competition for rewards).

[1] [Incentivizing a Robust P2P Network/Relay Layer](https://ethresear.ch/t/incentivizing-a-robust-p2p-network-relay-layer/1438)
