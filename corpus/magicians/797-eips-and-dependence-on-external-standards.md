---
source: magicians
topic_id: 797
title: EIPs and dependence on external standards
author: Recmo
date: "2018-07-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eips-and-dependence-on-external-standards/797
views: 775
likes: 5
posts_count: 2
---

# EIPs and dependence on external standards

Now that EIPs seem to be moving from proposing improvements to becoming a repository of standards, maybe we should be clear about which external (i.e. non-EIP) standards we build on.

Example: The many EIPs that specify contract interfaces all depend on the smart contract ABI. AFAIK the authoritative source for that is the Solidity documentation. This often goes unmentioned in the EIPs.

Here’s a list of external authoritative sources that EIPs depend on:

- The Yellow Paper
- JSON-RPC specification on the wiki
- Web3 specification on the wiki
- ABI specification in Solidity documentation
- Wherever the wire format of the Ethereum p2p protocol is defined.
- Various cryptographic primitives.
- (Please add any others you are aware of)

While it is not feasible to include everything, I think we can establish some goals here. Personally, I would like to see specifications like ABIv2, JSON-RPC, web3 and wire formats be included as an EIP.  Ideally the crypto primitives should also each have a short EIP containing literature references, test vectors and a (link to a) reference implementation.

Getting the EIP repo to fully specify Ethereum would be nice, but the Yellow Paper already covers most of this well (although it could be a bit more concrete and verbose in places).

At a minimum I would like to have a definite list of all the relevant Ethereum specific standards.

## Replies

**jpitts** (2018-07-23):

A few months ago I started documenting some of these here:

https://ethereum-magicians.org/t/standards-work-throughout-the-community/98

I agree, all standards that comprise the Ethereum system need to be called out, and formally brought through the improvement process.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> I would like to see specifications like ABIv2, JSON-RPC, web3 and wire formats be included as an EIP.  Ideally the crypto primitives should also each have a short EIP containing literature references, test vectors and a (link to a) reference implementation.

