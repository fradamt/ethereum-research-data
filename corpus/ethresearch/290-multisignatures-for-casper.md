---
source: ethresearch
topic_id: 290
title: Multisignatures for Casper
author: kladkogex
date: "2017-12-05"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/multisignatures-for-casper/290
views: 1229
likes: 0
posts_count: 3
---

# Multisignatures for Casper

I wonder if you guys considered using a multisignature/aggregated  signature scheme (such as Boneh-Lynn-Shamir) to combibe Casper validator votes -  - this could improve verification times and decrease storage requirements …

## Replies

**AlexeyAkhunov** (2017-12-06):

If the account abstraction ends up being implemented, it should be possible to use multisignature in the Casper contract, I suspect

---

**vbuterin** (2017-12-07):

Correct. And account abstraction already is implemented in the current Casper PoCs.

Edit: sorry, misread what you meant. Multisignatures **for security purposes** are totally possible because a user can specify whatever signature scheme they want. Multisignatures **for signature aggregation purposes** are not really feasible because (i) they conflict with the goal of signature abstraction, and (ii) there’s little point because it still takes O(N) effort to process rewards for validators.

Though what we **can** do to make life easier for light nodes is have them randomly sample a set of voters, and only ask for and verify votes from them. Another thing you can do is use BLS signatures internally inside a stake pool.

