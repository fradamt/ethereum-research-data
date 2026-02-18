---
source: ethresearch
topic_id: 427
title: Enhance privacy and scaling
author: ihlec
date: "2018-01-03"
category: Privacy
tags: []
url: https://ethresear.ch/t/enhance-privacy-and-scaling/427
views: 2055
likes: 1
posts_count: 2
---

# Enhance privacy and scaling

Could we allow miners to substitute specific transactions, by combining the transaction IDs.

This could happen in a simple revocable mathematical way, to allow for validation from other nodes.

This way we achieve greater efficiency on heavily used addresses. (Exchanges or Mixing Services)

Substitution will get more powerful, the more pending transaction we have.

Example: (A to B; B to C) => A to C

## Replies

**vbuterin** (2018-01-04):

This could potentially work for simple transactions, but would be complex to implement, and would have no effect for more complex transactions. The place where these kinds of optimizations can happen more naturally is inside of state channel systems, which can also provide increased privacy if done well. I’d recommend researching state channels more, eg. here: http://www.jeffcoleman.ca/state-channels/

