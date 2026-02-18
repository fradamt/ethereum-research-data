---
source: ethresearch
topic_id: 1020
title: What R&D topics are there that, if implemented, would introduce backwards incompatible changes for clients?
author: jamesray1
date: "2018-02-08"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/what-r-d-topics-are-there-that-if-implemented-would-introduce-backwards-incompatible-changes-for-clients/1020
views: 2426
likes: 2
posts_count: 5
---

# What R&D topics are there that, if implemented, would introduce backwards incompatible changes for clients?

What comes to mind is sharding, statelessness, full Casper, eWASM and STARKs. I still need to read up on STARKs. What else should I get a good understanding of? I’m planning on developing a stateless sharding implementation on top of eWASM.

## Replies

**kladkogex** (2018-02-08):

I have a feeling that Casper can affect backward compatibility too in some sense. The new Casper fork choice rule specified in the Casper whitepaper says that everything is determined by the justified checkpoints, not PoW. PoW becomes a thing which validators take into account when validators  vote for checkpoints. The final judgement re: the winning chain comes from longest justified checkpoint. Theoretically there could be (very rare) cases where there would be two competing chains A and B having slightly different PoW, and where PoW fork choice rule would chose A and  Casper would chose B.

If there are clients that continue using PoW as the fork choice rule and ignoring the Casper, then in some cases there could be discrepancies in interpretation of what the winning  chain is.  My understanding though is that these discrepancies would be rare and could resolve over time.

Casper whitepaper initially used the PoW fork choice rule, but then switched to the longest justified checkpoint rule.  There is a discussion in the paper stating  the PoW choice rule could lead to a validator deadlock in some rare cases …

---

**jamesray1** (2018-02-08):

Fair point, Casper FFG could also be backwards incompatible.

---

**jamesray1** (2018-02-08):

I guess that getting round to reading through this would be a start: [Are there any ideas that's potentially more useful than implementing sharding?](https://ethresear.ch/t/are-there-any-ideas-thats-potentially-more-useful-than-implementing-sharding/334/14).

---

**jamesray1** (2018-02-08):

Is there anything else that would require a major rewrite of a client?

I want to determine whether I should focus on developing a stateless sharding client e.g. with Nimbus, or learn more about our contribute to any such research topics that would require a major change in implementation.

https://docs.google.com/document/d/14u65XVNLOd83cq3t7wNC9UPweZ6kPWvmXwRTWWn0diQ/edit?usp=drivesdk&ouid=108926235437139442541

