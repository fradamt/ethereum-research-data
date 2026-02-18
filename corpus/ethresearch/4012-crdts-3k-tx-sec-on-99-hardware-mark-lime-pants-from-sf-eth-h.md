---
source: ethresearch
topic_id: 4012
title: "CRDTs: 3K tx/sec on $99 hardware - Mark (lime pants) from SF Eth Hackathon chat w/ Vitalik"
author: amark
date: "2018-10-30"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/crdts-3k-tx-sec-on-99-hardware-mark-lime-pants-from-sf-eth-hackathon-chat-w-vitalik/4012
views: 1330
likes: 1
posts_count: 2
---

# CRDTs: 3K tx/sec on $99 hardware - Mark (lime pants) from SF Eth Hackathon chat w/ Vitalik

Vitalik told me to post here.

I don’t track blockchain/ethereum much, so pardon my non-jargon. I’m from the decentralization camp and run [GUN](https://github.com/amark/gun) which has D.Tube (3M/monthly uniques), Internet Archive (Wayback Machine parent, top 300 site globally), [Notabug.io](http://Notabug.io) (1K/daily uniques) using us to go P2P.

Vitalik and others asked for scaling solutions at the hackathon and just wanted to mention what we use in production - CRDTs (conflict free replicated data types), specifically state-based graph CRDTs (not append-only).

It has easily scaled up to 1000X BTC’s tx/sec **yesterday in production** (this isn’t theoretical) on $99 P2P hardware. Nobody at the conference seemed aware of it, so just thought I’d drop by and say hi and try out CRDTs, should be pretty easy for Ethereum to experiment with.

If you have any Qs shoot me an email (please don’t reply here, too hard to track). Cheers!

## Replies

**MihailoBjelic** (2018-10-30):

*This post is intended for the Ethresearch community, not the author himself*

CRDTs are a way to achieve **eventual** consistency in distributed systems (mostly databases). They’ve been around for some time, CouchDB, Riak and few other projects use them.

Some time ago, I thought if using something similar in Ethereum could help scale it, but couldn’t come up with anything that would make sense. IMHO, the main issues are that we have eventual consistency (not instant, similar to Bitcoin’s eventual finality in a way), there is no leader (a complete paradigm-shift) and we need to have clear rules for conflicts resolution (I don’t know if such rules could be constructed in this case).

Any thoughts? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

