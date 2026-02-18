---
source: magicians
topic_id: 3752
title: Running a Parity Archive node
author: tjayrush
date: "2019-11-03"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/running-a-parity-archive-node/3752
views: 1277
likes: 2
posts_count: 3
---

# Running a Parity Archive node

About two years ago I set up two Parity archive nodes on custom-built Linux boxes with internal 4TB SSD hard drives (don’t ask – I have a reason). Currently, they are both at 94% full with about 220 GB of free space, and I’m looking for any ideas of where to go from here.

Is anyone out there running Parity archive nodes? Are you anticipating it outgrowing a 4TB drive? Are you running the nodes locally? Are you running them on a datacenter? How much is it costing you? I can’t find an internal SSD any larger than 4TB – is an internal drive needed? I’m pretty sure an SSD is needed - is that still true?

Any help or advice from people running archive nodes would be appreciated. I’ll collect together and write up a Medium post if I get some useful information.

## Replies

**richardpringle** (2020-02-18):

Hey [@tjayrush](/u/tjayrush), I’m interested in hearing more about your use case and why you require a full archive node. As far as SSDs go, I’m running a couple non-archiving nodes with several days with of history before pruning and they require SSDs just to keep in sync. I’m running the nodes in the cloud though and it cost a fortune.

I think what most people are doing that have “archival” use cases is indexing the new data as it comes in into a database. There are several different strategies on that front.

If you could share a little more about your use case (the queries you are running, not necessarily why you are running them), then I might be able to help.

---

**tjayrush** (2020-02-25):

I solved my issue with the SSD disc size. I added a second 4TB drive to each node (I now have two nodes with 8TB drives each). The person who set it up for me used Raid 0. Works well.

As far as why I’m running an archive node, it’s a long story. I’m trying to understand what would be needed to make a single user’s data fully available to them without a third party involved at all – in other words – any user should be able to get any data they want from ONLY the node. I don’t technically need an archive node (but I do need a --tracing node). I used the historical balances/data state to ‘debug’ my work. Without an archive node, if there’s a bug somewhere in my code (which scans accounts for a list of historical transactions), I can’t really tell where the error is unless I ‘reconcile’ at the end of each transaction. Once my code works, I really don’t need the archive node.

The project is called TrueBlocks (http://trueblocks.io).

