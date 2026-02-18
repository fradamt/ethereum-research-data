---
source: magicians
topic_id: 11535
title: How ethererum transaction works?
author: Shweta-hlf
date: "2022-10-31"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/how-ethererum-transaction-works/11535
views: 635
likes: 0
posts_count: 3
---

# How ethererum transaction works?

HI team,

I am new to ethereum.can you pls give answers of below points.

How fast transactions are accepted by the blockchain’s network

- How much bandwidth it uses,
- How much blockchain data needs to be stored and in what way the data must be stored.
- Important metrices:

numbers of blocks are added to the blockchain,
- block and transaction sizes,
- transaction rates

Also,

'- How does blockchain respond to increasing number of nodes

- How does blockchain respond to increased number of transactions for one specific node.
Thanks

## Replies

**Ariiellus** (2022-10-31):

Hi!

- Tx in Ethereum are accepted every ~12s in what is called slot, and every 32 slots form an epoch. They achieve Finality after 2 epochs
- Recommended hardware requirements to run a Full node is 25 MBit/s bandwidth. This will be lower after the implementation of EIP-4844 (blob transactions)
- Ethereum stores and manages data using a trie. There three types of the trie in the Ethereum Blockchain:

State Trie
- Storage Trie
- And Transaction Trie

Important metrices: https://beaconcha.in/

- After The Merge a block or “slots” is added every ~12s
- Each slot can store up to 256 bits (32 bytes ).
- 21000 is the minimum amount of gas an operation on Ethereum will use.

The most “tangible” answer is that Gas prices will rise due to supply and demand law.  https://etherscan.io/gastracker

---

**Shweta-hlf** (2022-11-01):

Thanks a lot for your reply!!

How ethereum respond to increasing number of nodes

How does Ethereum respond to increased number of transactions for one specific node.

