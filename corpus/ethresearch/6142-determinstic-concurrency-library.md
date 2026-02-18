---
source: ethresearch
topic_id: 6142
title: Determinstic Concurrency library
author: laurentyzhang
date: "2019-09-15"
category: Architecture
tags: []
url: https://ethresear.ch/t/determinstic-concurrency-library/6142
views: 1346
likes: 1
posts_count: 3
---

# Determinstic Concurrency library

We are currently adding concurrency support to EVM. We have designed a generic wrapper called VM container, not just for EVM, but all kinds of VMs, the library is mostly dealing with these VM container to achieve VM agnosticism.

The library supports server cluster as well, so you can run parallel smart contracts on multiple servers.

Now we have a STM for managing state consistency, A versioned storage access interface, using standard stateDB interface, but re-implemented it completely, two types of concurrent containers,  locking and deferred functions.

We used the library to rewrite a part of CryptoKitties and got ~9x on a 16c machine, Will rewrite the whole program in next couple months. Targeting at 100x with a few more servers.

What other functionalities do we need to add ? Any thought?

Laurent

## Replies

**adlerjohn** (2019-09-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/laurentyzhang/48/5537_2.png) laurentyzhang:

> What other functionalities do we need to add ?

Open sourcing the code?

---

**laurentyzhang** (2019-09-17):

Will do in the future, the biggest problem we are facing right now is the latency of the distributed locking part, currently using rlock(redis based), but it is too slow, 0.1ms was the best we could get, any recommendations ?

