---
source: magicians
topic_id: 14705
title: Compute Units Estimation
author: a10zn8
date: "2023-06-16"
category: Magicians > Primordial Soup
tags: [json-rpc]
url: https://ethereum-magicians.org/t/compute-units-estimation/14705
views: 551
likes: 0
posts_count: 1
---

# Compute Units Estimation

Greetings everyone,

I’m currently involved in a project, the primary goal of which is to create a system capable of estimating the relative complexity of each JSON-RPC method. We’re building this in the context of our work on [drpc.org](http://drpc.org), where we’re creating a community of node runners to run a decentralized rpc provider service.

One of the more intriguing challenges we’re grappling with is the construction of a fair model to estimate the cost of calls. To give you an example, the ‘eth_blockNumber’ method is relatively inexpensive, costing about 10 compute units (CUs). The ‘eth_getBalance’ method is slightly more expensive at 11 CUs, while ‘eth_call’ is even more so, with a cost of 21 CUs. The list goes on.

So, how do we create a comprehensive model that ensures a fair and accurate estimation of call costs? I am eager to hear your insights and look forward to the exchange of ideas.

### First iteration

In order to establish a baseline for this research, I adopted the following methodology: I selected two distinct Ethereum nodes, Erigon and Nethermind, and tested almost each JSON-RPC method’s performance under varying rps pressures.

So, here’s what I did: I tested the performance of two Ethereum nodes, Erigon and Nethermind, under different rates of requests per second (RPS). I added missing methods to Ethspam (here’s the link: https://github.com/p2p-org/ethspam) and used a load test tool I wrote called Ether Bench (link: https://github.com/p2p-org/ether-bench).

The tests provided a lot of data. The main objective was to create a robust model capable of providing fair estimations comparable to existing Compute Unit (CU) estimations from various public providers. I mainly looked at three things:

1. How long do requests take at 100 RPS
2. The maximum RPS where every request is successful
3. The average response size

I turned these numbers into a scale from 0 to 1 and used them in this formula:

`0.5 * latency + 0.3 * (1-throughput) + 0.2 * size`

Based on that formula and multiple measurement results, I came to our current cu estimation, which can be found here - [Docs: RPC & Chain Methods Documentation | dRPC](https://docs.drpc.org/pricing/compute-units)

### Questions

Now, I need your help. My formula is a guess, and I think we can make it better.

Are there more details we should add? Have you worked on something similar? How would you solve this?

I’m excited to hear your ideas.
