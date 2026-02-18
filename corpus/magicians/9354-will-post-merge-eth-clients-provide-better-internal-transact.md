---
source: magicians
topic_id: 9354
title: Will post-merge ETH clients provide better internal transaction inspection?
author: cyrus
date: "2022-05-23"
category: Working Groups > The Merge
tags: []
url: https://ethereum-magicians.org/t/will-post-merge-eth-clients-provide-better-internal-transaction-inspection/9354
views: 669
likes: 0
posts_count: 3
---

# Will post-merge ETH clients provide better internal transaction inspection?

I’m working with some extremely old contracts that have no event emissions, so I run daemons that watch for changes there instead.

If there are txs to my contracts I can detect potential changes; I grab the latest block and look at the hydrated tx list for “to” values matching my contracts.

Unfortunately I can’t easily detect *internal* transactions that alter the state of my contact. To my knowledge there is no easy way to do this; neither the “to” nor “from” values are addresses I can predict.

Will eth 2 clients and their http/ws endpoints allow easier “watching” of contracts in this manner? i.e. for changes in smart contract state, no matter the source, initial tx target or manner?

## Replies

**wminshew** (2022-05-24):

v keen for the answer to your question, but in the meantime perhaps this is something a subgraph with [callHandlers](https://thegraph.com/docs/en/developer/create-subgraph-hosted/#call-handlers) could help with?

---

**daniellehrner** (2022-05-27):

Most clients offer API endpoints to create the traces, with all of the details, of a transaction. For Hyperledger Besu you can find some examples of these traces in the docs: [Trace types](https://besu.hyperledger.org/en/stable/Reference/Trace-Types/#trace)

If you search for tracing you should find the same for other clients.

