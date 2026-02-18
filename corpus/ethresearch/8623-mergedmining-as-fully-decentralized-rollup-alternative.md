---
source: ethresearch
topic_id: 8623
title: MergedMining as fully decentralized rollup alternative
author: kladkogex
date: "2021-02-03"
category: Consensus
tags: []
url: https://ethresear.ch/t/mergedmining-as-fully-decentralized-rollup-alternative/8623
views: 1372
likes: 1
posts_count: 3
---

# MergedMining as fully decentralized rollup alternative

**TL;DR**

A merged mined chain can be used as a fully decentralized rollup alternative to achieve 1000 tps, while using the current ETH1, and 100K+ tps using ETH2 data chains.

**Description**

Here is how this would work:

1. To participate in the network, a node would register in a smart contract on the main net.
2. There would be a single, randomly selected proposer for each epoch (block range)
3. Transactions would use aggregated BLS signatures instead of ECDSA, otherwise, the merged mined chain would be identical to ETH1.
4. Each proposer would submit a block by

- submitting block body as calldata, and
- submitting the state root to the ForkTree smart contract.

The block would aggregate all transaction BLS sigs into a single BLS sig. A fund transfer transaction would then take as little as 10 bytes or 160 gas (100 times less compared to what it takes now)

1. The fork choice used by the ForkTree contract would be simply the longest chain.
2. To exit, one would simply burn the funds on the merge mined chain and submit the receipt against a finalized root on in the ForkTree smart contract

Advantages:

- full ETH compatibility
- immediate exit
- no need to wait for 7 days as in optimistic rollup
- fully decentralized - no single operator
- security: identical to the main net!
- Satoshi Nakamoto saw merged mining as a way to scale blockchain!

Future:  one could use each of ETH2 data chains as data storage for merge mined chains. This could bring TPS to 100,000+!!!

## Replies

**blazejkrzak** (2021-02-18):

I am curious about 100,000 tps +.

Those digits are very optimistic, and I doubt it even if you had possibility to do this within a block, networking in shared tx.pool is not so fast.

Having 1k tps on our test network with executable beacon chain was possible, but filling tx pool with such insane amounts was demanding. We had to use chainhammer and design another library chaindriller to fill txpool

---

**mariano54** (2021-02-18):

You still need to do a bls pairing for each message if you’re verifying an aggregate signature. I’m assuming the messages are different? If so, doing 1k bls pairings per second seems like a lot. (to keep up with), and definitely a lot to sync up

