---
source: ethresearch
topic_id: 2884
title: RAFT Leader Election and Casper
author: eolszewski
date: "2018-08-10"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/raft-leader-election-and-casper/2884
views: 1327
likes: 3
posts_count: 4
---

# RAFT Leader Election and Casper

What is the disadvantage to using RAFT leader election for the validator committee in Casper whereby validators are moved in and out of the committee one at a time versus swapping out the entire committee at regular intervals?

This would allow us to leverage a tried and tested approach to leader election and would allow for a constantly fluctuating pool of the validator committee members vs. locking up the collective in for a predetermined number of rounds. We could perform the same sort of operation on the current committee for deciding which member(s) will be being replaced by the new committee member(s).

## Replies

**kladkogex** (2018-08-11):

RAFT is a protocol that works under assumption that all servers in the cluster are not malicious. This is not the case for decentralized networks, where it is assumed that a minority of cluster members are malicious.

---

**0zAND1z** (2018-08-11):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> RAFT is a protocol that works under assumption that all servers in the cluster are not malicious.

That’s a good point  [@kladkogex](/u/kladkogex), assumption of node good withstanding in the network is not safe to assume.  You may check out the concept of **Node Trust Quotient** used in the link:  [Sentinel Scalability - KIP Technical Primer](https://kipfoundation.github.io/techprimer/4-Sentinel-Scalability.html).

The proposed system runs on TARA -  A modified version of Raft; and collects a set of information from hardware as well as dynamic statistics when required.

The math is not fully carved out yet, but I hope this adds value to the thread.

---

**kladkogex** (2018-08-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/0zand1z/48/9248_2.png) 0zAND1z:

> The math is not fully carved out yet, but I hope this adds value to the thread.

Once you start carving out the math you will encounter the Byzantine generals problem …

