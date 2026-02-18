---
source: magicians
topic_id: 6828
title: Eth2.0 How to reduce storage bloat?
author: sinsinpurin
date: "2021-08-10"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eth2-0-how-to-reduce-storage-bloat/6828
views: 502
likes: 0
posts_count: 2
---

# Eth2.0 How to reduce storage bloat?

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

I’d appreciate it if you could answer my questions.![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

## Replies

**matt** (2021-08-11):

You already [posted this](https://ethresear.ch/t/eth2-0-question-how-to-reduce-storage-bloat/10252) on ethresearch, is there a reason for cross posting?

