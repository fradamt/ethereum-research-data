---
source: ethresearch
topic_id: 10252
title: Eth2.0 Question. How to reduce storage bloat?
author: sinsinpurin
date: "2021-08-03"
category: Sharding
tags: []
url: https://ethresear.ch/t/eth2-0-question-how-to-reduce-storage-bloat/10252
views: 3136
likes: 3
posts_count: 5
---

# Eth2.0 Question. How to reduce storage bloat?

I’m a student currently working on the problem of storage bloat in blockchain.

I have a question.

- How to reduce storage bloat in Eth2.0?

Now, Eth1.0’s full node stored about 900GB. It will increase more.

In my research, I found super full node and single shard node.

Super full node store beacon chain data and all shard chain data.Super full node need high internet transmission speed and large SSD. On the other hand, single shard node store single shard data. So single shard node will don’t have to large SSD than super full node. But if node shuffle shard, i think ,single shard node would need to download large amounts of data about 1 shard.

So I think it’s going to be difficult to join the network immediately.

- Is my understanding correct?
- Do you see the data bloat of the superfluous nodes as a problem?
- Can you tell us about any storage issues ethereum developer are currently facing?

I’d appreciate it if you could answer my questions.![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

## Replies

**MicahZoltu** (2021-08-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/sinsinpurin/48/6344_2.png) sinsinpurin:

> Eth1.0’s full node stored about 900GB. It will increase more

A full node isn’t 900GB, that sounds like an archive node which is a very different thing that the vast majority of people do not need.

---

**adlerjohn** (2021-08-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> A full node isn’t 900GB

That is correct, it is only 899.9 GB ([source](https://etherscan.io/chartsync/chaindefault)).

[![full node 900](https://ethresear.ch/uploads/default/optimized/2X/4/42188122fbe9aa894f1d8c7a2f86c5b025cc4063_2_690x278.png)full node 9001353×546 26.7 KB](https://ethresear.ch/uploads/default/42188122fbe9aa894f1d8c7a2f86c5b025cc4063)

---

**MicahZoltu** (2021-08-03):

There are lots of possible sync settings, I’m curious what settings are being used for whatever is drawing that chart?  Modern fast syncs I believe are way below 900GB in disk space.

I don’t know if Geth has something like this, but I have always liked Nethermind’s chart showing different configuration options:

https://docs.nethermind.io/nethermind/ethereum-client/sync-modes

[![image](https://ethresear.ch/uploads/default/optimized/2X/1/189f9775e953a6a605303b603fdaa75249429771_2_502x500.png)image749×746 54.7 KB](https://ethresear.ch/uploads/default/189f9775e953a6a605303b603fdaa75249429771)

---

**norswap** (2021-08-04):

From [the command line options](https://geth.ethereum.org/docs/interface/command-line-options):

> --syncmode value       Blockchain sync mode (“fast”, “full”, “snap” or “light”) (default: snap)

You can find the description of the various modes [here](https://blog.ethereum.org/2021/03/03/geth-v1-10-0/#snap-sync).

I did try a sync last month and in snap sync 300GB were not enough. I wouldn’t be surprise if the 900GB figure is right.

