---
source: magicians
topic_id: 3123
title: A cross-protocol, cross-implementation standard for server capacity management and flow control
author: FrankSzendzielarz
date: "2019-04-12"
category: Magicians > Primordial Soup
tags: [light-client, devp2p]
url: https://ethereum-magicians.org/t/a-cross-protocol-cross-implementation-standard-for-server-capacity-management-and-flow-control/3123
views: 1329
likes: 1
posts_count: 1
---

# A cross-protocol, cross-implementation standard for server capacity management and flow control

After reviewing PIP and LES flow control mechanisms and new proposals for managing server capacity, and after discussions with [@zsfelfoldi](/u/zsfelfoldi), I realized a number of things:

- The flow control mechanisms are essentially token bucket rate limiters, primarily aimed at managing burst demand, but not quota limits per absolute calendar period (eg: megabytes per day). The mechanisms are pretty narrow, allowing to manage demand in a limited way.
- The mechanisms expect clients to mirror the token-bucket state in order to avoid immediate disconnection. This is fragile under some circumstances and also draconian.
- It complicates implementation of light clients from scratch.
- Clients don’t need information on the token bucket state, they just need to know when their service is being throttled or limited (like http codes 503 and 429 : server overloaded and client sending too many requests, respectively)
- Clients may optionally receive hints about eviction rules and throttling rules.

A summary of a high level review is in the devp2p repo here [LES: client load management discussion · Issue #66 · ethereum/devp2p · GitHub](https://github.com/ethereum/devp2p/issues/66)

**I would like to propose that the flow control mechanisms and server capacity management methods be removed from and abstracted out from light client protocols and replaced with the following**:

- A common data structure that would describe various throttling and evicition policies.
- This would be used as a commonly recognized server configuration file format.
- It would be used as a message format for RPC admin calls.
- All of it or parts of it would be used as message bodies for flow control hints messages, which could be distributed as part of protocol-specific handshakes, and as a new server protocol/capability for informing clients of policy information.

So basically we’d have a common data format that would configure the server for different capacity-limiting policies, at a per-client level and for the whole server. Clients could optionally request information on throttling and eviction policies using a capacity-management specific protocol, a simple set of messages, that would allow clients to monitor token-bucket or quota status if they wanted to.

**A detailed proposal of exactly what format this could take is here** (at the time of writing the proposal is missing ‘burst depth’ as a config parameter): [LES: Server load management proposal - detail · Issue #74 · ethereum/devp2p · GitHub](https://github.com/ethereum/devp2p/issues/74)

This would help with a number of avenues:

- Converge PIP and LES: aside from flow control and some minor batching discrepancies, the CHT is the only significant difference. The consensus seems to be that LES should move to a non-cumulative CHT to assist with pruning. If so, with flow-control out, semantically there is not much to solve.
- Debatable still if this is the preferred direction, but there is some discussion about moving the PIP/LES capability into ETH/64. By abstracting out flow-control this helps with this endeavor.
- The same config format, message format and logic can be applied to Whisper (at a server level) , Swarm (light clients and server capacity management), Ethereum and across all implementations.
- The very same format can be used for consortium type trusted setups where the load management might be across a cluster or even applied at setups like Infura.
- The proposal includes client categorization (free, paid, banned, etc…). This helps pave the way for micropayment incentivization, allowing the common format to be an extension point to include actual ‘cost’ information.
