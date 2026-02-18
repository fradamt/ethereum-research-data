---
source: magicians
topic_id: 4456
title: "EIP: PubRef - Script OP Code For Public Data References"
author: rook
date: "2020-07-28"
category: EIPs
tags: [opcodes]
url: https://ethereum-magicians.org/t/eip-pubref-script-op-code-for-public-data-references/4456
views: 583
likes: 0
posts_count: 1
---

# EIP: PubRef - Script OP Code For Public Data References

Imagine an immutable stack-based language where every push operation is executed contributing more to an ever growing global-stack. This stack can be pruned down for relevance, and then exposed to future scripts which can then reference any previous value used by any previous operation.

Having a global shared stack would allow scripts to be less redundant as they could refer to what has already happened.  In effect, this is a form of running code-book compression of key material.

I will be happy to write up an EIP if you guys are interested blockcahin pointers.  For now a i have BIP:


      [github.com](https://github.com/TheRook/bip-pubref/blob/master/bip-PubRef.mediawiki)




####

```mediawiki

  BIP: PubRef
  Layer: Consensus (soft fork)
  Title: PubRef - Script OP Code For Public Data References
  Author: Michael Brooks
  Comments-Summary: No comments yet.
  Comments-URI: https://github.com/bitcoin/bips/wiki/Comments:BIP-0323
  Status: Draft
  Type: Standards Track
  Created: 2019-07-23
  License: CC0-1.0

== Abstract ==

This BIP describes how a new OP code can be used to construct smaller, more compact transactions.  With a public reference (PubRef), a newly created transaction can reuse elements of a previously confirmed transaction by representing this information with a smaller numeric offset or “pointer”.

== Motivation ==

Giving scripts the ability to refer to data on the blockchain will reduce transaction sizes because key material does not have to be repeated in every Script. Users of the network are rewarded with smaller transaction sizes, and miners are able to fit more transactions into new blocks.  Pointers are a common feature and it felt like this was missing from Bitcoin Script.
```

  This file has been truncated. [show original](https://github.com/TheRook/bip-pubref/blob/master/bip-PubRef.mediawiki)
