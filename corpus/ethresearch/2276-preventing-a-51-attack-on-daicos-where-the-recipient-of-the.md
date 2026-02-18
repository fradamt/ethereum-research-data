---
source: ethresearch
topic_id: 2276
title: Preventing a 51% attack on DAICOs where the recipient of the funds can be changed?
author: jtremback
date: "2018-06-18"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/preventing-a-51-attack-on-daicos-where-the-recipient-of-the-funds-can-be-changed/2276
views: 1493
likes: 1
posts_count: 1
---

# Preventing a 51% attack on DAICOs where the recipient of the funds can be changed?

I would like to see DAICOs where the recipient of the raised funds can be changed by the token holders. This allows the token holders to replace developers without a refund. A refund would kind of blow the group apart and creates a coordination problem in establishing a new developer group for the token network.

However, changing the recipient address was specifically avoided in the original DAICO design to prevent 51% attacks.

I would like to propose a mitigation of 51% attacks, without the complicated and recursive nature of [DAO splits](https://github.com/slockit/DAO/wiki/How-to-split-the-DAO). It’s late, so maybe this has obvious problems I’m missing.

### Developer replacement or refund

In addition to simply voting “I want to change the developer to this address”, you can also vote “I want a refund if the developer is changed to this address” (this is a personal refund). This way, during a 51% attack that the 49% are aware of, they can exit if the attack is completed.
