---
source: magicians
topic_id: 4825
title: "EIP-3041: Add basefee to eth_getBlockByHash"
author: abdelhamidbakhta
date: "2020-10-13"
category: EIPs
tags: [json-rpc, eip-1559]
url: https://ethereum-magicians.org/t/eip-3041-add-basefee-to-eth-getblockbyhash/4825
views: 2418
likes: 0
posts_count: 4
---

# EIP-3041: Add basefee to eth_getBlockByHash

https://github.com/ethereum/EIPs/pull/3041

[EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) introduces a base fee per gas in protocol.

This value is maintained under consensus as a new field in the block header structure.

This change should be reflected in RPC methods that return block header information.

## Replies

**ryanschneider** (2020-10-19):

Hi,

Just curious, what’s the rationale for a separate EIP per RPC (e.g. 3044,45,46 and this one)?

---

**timbeiko** (2020-10-23):

I believe [@MicahZoltu](/u/micahzoltu) suggested this approach.

---

**MicahZoltu** (2020-10-24):

Small EIPs go through the EIP process smoother as you don’t end up with contention on one piece blocking all of the others.  Also, from a communication standpoint there are benefits to having each “thing” have its own number.  A client may implement EIP-3044 but not implement EIP-3045 and being able to express that simply is valuable.  If it was all one EIP, then you would have to say “I partially implement EIP-3044” and then go on to specify which parts you implement or which parts you don’t using words.

