---
source: ethresearch
topic_id: 1159
title: Are deposits going to be slashed across hard forks?
author: nootropicat
date: "2018-02-19"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/are-deposits-going-to-be-slashed-across-hard-forks/1159
views: 1207
likes: 2
posts_count: 3
---

# Are deposits going to be slashed across hard forks?

There’s no security reason to do so as forks would be permanently divergent. So all it would do is change a hard fork choice incentive from ‘what I prefer’ to ‘what I think the majority is going to prefer’ and (in practice) prevent the existence of a minority fork.

In addition it could potentially lead to a stall in the network at a (controversial) fork time as validators could prefer to pay an offline penalty just to see what fork the remaining majority chooses.

For these reasons I don’t think deposits should be slashed across hard forks. Are they going to?

## Replies

**vbuterin** (2018-02-20):

If we want to make hard forks “safe” then we could require hard forks to change the format of signatures or add a chain ID into signatures; this way it would be possible for validators to continue being validators of both chains after a fork takes place.

---

**MicahZoltu** (2018-02-21):

I think it is very important from a governance perspective to make sure that hard forking (rule changes) are always available and easy for all forks.  This is the final check/balance by a disenfranchised group against the majority and to only thing stopping a blockchain from turning into mob (majority) rule.

