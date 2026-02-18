---
source: ethresearch
topic_id: 4187
title: Network-adjusted timestamps
author: vbuterin
date: "2018-11-08"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/network-adjusted-timestamps/4187
views: 13392
likes: 7
posts_count: 7
---

# Network-adjusted timestamps

One common criticism of many proof of stake algorithms is that they place a large dependence on the requirement that nodes’ local blocks must be roughly synchronized. In practice, this assumption seems to be roughly satisfied even in the current Ethereum PoW network, but this is often accomplished by the [relatively centralized NTP protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol).

This post describes one way to eliminate NTP. For illustration, we will use the [beacon chain network simulator](https://github.com/ethereum/research/tree/master/clock_disparity), specifically the `lmd_node.py` and `lmd_test.py` files. First of all, here is a dry run of the protocol with no modifications, network latency ~= 2/3 slot length, clock disparity ~= 1/3 slot length:

[![Figure_1-14](https://ethresear.ch/uploads/default/original/2X/7/7199f3f82c65c55299a67afff7759eb1dfcf658d.png)Figure_1-14640×480 5.23 KB](https://ethresear.ch/uploads/default/7199f3f82c65c55299a67afff7759eb1dfcf658d)

The execution is by no means perfect, but it is fairly orderly. Now, let’s crank up clock disparity to ~30x slot length.

[![Figure_1-15](https://ethresear.ch/uploads/default/original/2X/b/b20fc5ca0665fa905aef3b8900b67644401848c9.png)Figure_1-15640×480 21.6 KB](https://ethresear.ch/uploads/default/b20fc5ca0665fa905aef3b8900b67644401848c9)

The chain runs, and blocks even get justified, a true testament to the sheer power of LMD GHOST, but nothing gets finalized.

Now, we will adopt the following mechanism. When a node receives a message from another node, it calculates the implied timestamp of that node: for example, if genesis time is 1500000000, slot length is 8 seconds, and it receives a block with slot number 10, it takes an implied timestamp of 1500000080. A node can compute the median implied timestamp of all nodes based on their latest messages, and simply adopt it:

[![Figure_1-16](https://ethresear.ch/uploads/default/original/2X/1/1a570c852d66e919c133eafa600ecbeae6ed505f.png)Figure_1-16640×480 5.79 KB](https://ethresear.ch/uploads/default/1a570c852d66e919c133eafa600ecbeae6ed505f)

The timestamps of the nodes differ by an amount roughly equal to network latency.

Another rule that has similar consequences is adopting the implied timestamp of any new block that becomes the head; this is equivalent to replacing all references to clock time with a rule “build or accept a block using the slot after the head 8 seconds after receiving the head, using the slot two after the head 16 seconds after receiving the head, etc”.

However such rules are dangerous because they remove all pressure to converge on the “real time”, making rewards unpredictable and the `block.timestamp` opcode unpredictable. Fortunately, we can compromise, instead of the median taking the 67th percentile of the nodes’ implied timestamps (in the direction closer to one’s own timestamp). This rule gives less perfect results, though the results are still impressive:

[![Figure_1-18](https://ethresear.ch/uploads/default/original/2X/7/7eaeae6d0aedf50027fd193fafd6d777bae74fab.png)Figure_1-18640×480 10.3 KB](https://ethresear.ch/uploads/default/7eaeae6d0aedf50027fd193fafd6d777bae74fab)

Now we go up to the 83rd percentile:

[![Figure_1-19](https://ethresear.ch/uploads/default/original/2X/a/a0ea51eb6ba1103d9c5fc59e51621e90d45afc2b.png)Figure_1-19640×480 14.4 KB](https://ethresear.ch/uploads/default/a0ea51eb6ba1103d9c5fc59e51621e90d45afc2b)

Note that in practice, percentiles above the 75th are not recommended, as a relatively small portion of attackers could then “veto” any drifts away from a node’s local clock.

Another alternative is an adjusting-percentage rule: to make shifts up to 10 minutes away from a node’s local clock, we follow the majority, to shift 20 minutes we require 55% agreement between latest observed implied timestamps, to shift 40 minutes we require 60%, and so forth until the maximum a node can shift is 10240 minutes ~= 7 days.

This technique could be applied generically to reduce the level of reliance on local clocks in proof of stake algorithms.

## Replies

**ittaia** (2018-11-09):

Nice! BTW section 7 of this paper https://eprint.iacr.org/2018/1028.pdf addresses a similar question of decentralized clock synchronization against a malicious adversary. It can be piggybacked on many existing protocols and blends well with multi-sigs, etc

---

**vbuterin** (2018-11-09):

Thanks for the link!

> Whether we can design synchronous protocols with gradual deterioration without using proof-of-work is an interesting open question

Does LMD GHOST (the fork choice rule used in the simulations above) not provide this property?

---

**ChengWang** (2018-11-09):

As far as I see, the implied timestamp of a node is an interpolation of local clocks of all nodes and message delays this node receives. The first part of the interpolation could help ease the disparities of local clocks of different nodes. However, the disparities of message delays are hard to eliminate due to the different roles of different nodes.

Another disadvantage is that the implied timestamp seems to be after real time in general if assuming that the mean of local clocks is equal to real time. This difference to real-time might cause inconvenience to coding and introduce bugs.

---

**vbuterin** (2018-11-10):

This algorithm explicitly does not attempt to account for network delays.

I don’t think we need to; we only need clock accuracy on the order of one slot duration, and network delays are much less than that.

---

**ChengWang** (2018-11-10):

It’s not network delays, but message delays. In order to trust message (therefore timestamp) received from nodes, it’s better to use messages from validators. However, these messages from validators might be relayed to a specific node, not being sent directly. In a decentralized P2P network, the message delays are significant to one slot duration in my opinion.

---

**vbuterin** (2018-11-11):

> In a decentralized P2P network, the message delays are significant to one slot duration in my opinion.

A slot duration is 8 seconds; delays in the current ethereum network are at most ~1-2 seconds. So it’s certainly significant, but even if this problem is left unsolved, clock disparity + latency will still altogether be much less than one slot.

