---
source: magicians
topic_id: 7253
title: Split validating nodes and data nodes
author: jori
date: "2021-10-12"
category: Magicians > Primordial Soup
tags: [storage]
url: https://ethereum-magicians.org/t/split-validating-nodes-and-data-nodes/7253
views: 791
likes: 0
posts_count: 2
---

# Split validating nodes and data nodes

Solana has broken disk space scalability limitation to decentralization by storing data history on Arweave Blockchain. This has security concerns since they are introducing a third party risk within the security of their own network but it has solved the problem of disk space affecting scalability.

Algorand is trying to compete with Solana by increasing velocity and block space and their approach to the disk space problem is to compress history within their own nodes using ZK-Rollups technology.

These movements should make the Ethereum community think about alternatives to the disk space problem so Ethereum is not left behind on scalability.

This Ethereum Improvement Proposal is to split the nodes in validating nodes and data storage nodes within Ethereum Blockchain. Advantages:

-Block size and velocity can be increased because the limit of disk space is no longer an issue so Ethereum L1 can compete on scalability and velocity.

-Decentralization is not compromised but is increased since now the security of the network has more and different nodes.

-Security is also improved on future shards since shards nodes only validate, data is stored on cross shards data nodes.

-Security could also be improved by forcing a coordinated attack on both the validating nodes and the data nodes (where you not only need to stake but also provide disk capacity).

-If a bold approach to data nodes is followed, this opens the door for new utilities for Ether. Ethereum could become the most secure decentralized storage network and storing demand would increase Ether demand.

I did not find any discussion about this and I think It is a very important topic. Just wanted to open the discussion since I am not a technical guy.

## Replies

**greatfilter** (2021-11-22):

Eth nodes already distinguish between archive, full and lite clients. Full nodes store all the data needed to validate transactions and prune away state that is no longer relevant to future transactions. Lite nodes store only block headers and kinda operate in the way you are describing. The problem is that lite nodes cannot efficiently verify blocks because they must fetch data from remote sources which would add too much latency to the process.

