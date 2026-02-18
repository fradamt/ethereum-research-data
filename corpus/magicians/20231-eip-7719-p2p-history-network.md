---
source: magicians
topic_id: 20231
title: "EIP-7719: P2P History Network"
author: KolbyML
date: "2024-06-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7719-p2p-history-network/20231
views: 388
likes: 0
posts_count: 1
---

# EIP-7719: P2P History Network

Draft*

This EIP formalizes the usage of Portal’s History network for inclusion in Ethereum. The network lookups are based off blockhash.

Link to EIP PR

https://github.com/ethereum/EIPs/pull/8630

Link to formal spec:



      [github.com/ethereum/portal-network-specs](https://github.com/ethereum/portal-network-specs/blob/master/history/history-network.md)





####

  [master](https://github.com/ethereum/portal-network-specs/blob/master/history/history-network.md)



```md
# Execution Chain History Network

This document is the specification for the sub-protocol that supports on-demand availability of Ethereum execution chain history data.

## Overview

The chain history network is a [Kademlia](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) DHT that uses the [Portal Wire Protocol](../portal-wire-protocol.md) to establish an overlay network on top of the [Discovery v5](https://github.com/ethereum/devp2p/blob/master/discv5/discv5-wire.md) protocol.

Execution chain history data consists of historical block headers, block bodies (transactions, ommers and withdrawals) and block receipts.

In addition, the chain history network provides block number to historical block header lookups.

### Data

#### Types

- Block headers
- Block bodies
    - Transactions
    - Ommers
```

  This file has been truncated. [show original](https://github.com/ethereum/portal-network-specs/blob/master/history/history-network.md)
