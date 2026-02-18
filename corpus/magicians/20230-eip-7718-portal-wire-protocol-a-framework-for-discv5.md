---
source: magicians
topic_id: 20230
title: "EIP-7718: Portal Wire Protocol a framework for discv5"
author: KolbyML
date: "2024-06-06"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7718-portal-wire-protocol-a-framework-for-discv5/20230
views: 426
likes: 1
posts_count: 1
---

# EIP-7718: Portal Wire Protocol a framework for discv5

This Post is a draft, but the core subject matter is likely to remain unchanged

[Discv5 (Node Discovery Protocol v5)](https://github.com/ethereum/devp2p/blob/master/discv5/discv5.md) is a protocol used by the consensus later and soon to be used by the execution layer to find nodes on the network. Discv5 is an extendable protocol which allows building new protocols on top of it, utilizing `TalkRequests`, which is a message type of Discv5.

This EIP proposes a framework over Discv5 called the `Portal Wire Protocol`, a generic framework which allows building new DHT networks referred to as `Overlay Networks` these `Overlay Networks` inherit the performance optimizations of the base `Portal Wire` implementation, well also accelerating the development of new `Overlay Networks` networks. `Overlay Networks` each maintain their own Kademlia DHT routing table.

EIP Draft can be found here: [Add EIP: Portal Wire Protocol a framework for discv5 by KolbyML · Pull Request #8629 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8629)

More information can be found in this specification



      [github.com](https://github.com/ethereum/portal-network-specs/blob/master/portal-wire-protocol.md)





####



```md
# Portal Wire Protocol

The Portal wire protocol is the default p2p protocol by which Portal nodes communicate.

The different sub-protocols within the Portal network **MAY** use this wire protocol, but they **MUST** remain separated per network.

This is done at the [Node Discovery Protocol v5](https://github.com/ethereum/devp2p/blob/master/discv5/discv5-wire.md#talkreq-request-0x05) layer, by providing a different protocol byte string, per protocol, in the `TALKREQ` message.

The value for the protocol byte string in the `TALKREQ` message is specified as protocol identifier per network.

Each network using the wire protocol **MUST** specify which messages are supported.

Unsupported messages **SHOULD** receive a `TALKRESP` message with an empty payload.

## Protocol identifiers

All protocol identifiers consist of two bytes. The first byte is "`P`" (`0x50`), to indicate "the Portal network", the second byte is a specific network identifier.

### Mainnet identifiers
Currently defined mainnet protocol identifiers:
```

  This file has been truncated. [show original](https://github.com/ethereum/portal-network-specs/blob/master/portal-wire-protocol.md)
