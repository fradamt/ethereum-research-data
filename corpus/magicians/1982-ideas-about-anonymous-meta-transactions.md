---
source: magicians
topic_id: 1982
title: Ideas about anonymous meta transactions
author: suenchunhui
date: "2018-11-23"
category: Magicians > Primordial Soup
tags: [privacy, meta-magicians, meta-transactions]
url: https://ethereum-magicians.org/t/ideas-about-anonymous-meta-transactions/1982
views: 1107
likes: 1
posts_count: 3
---

# Ideas about anonymous meta transactions

I would like to seek opinions on good ideas for doing meta transactions while maintaining privacy on the identity of the user?

Main reason is to allow B2B activities where buyers, sellers and possibly financiers can move tokens around or interact with smart contracts, but do so using ephemeral addresses that are one-time use to protect privacy, and known only for the duration these parties are interacting with each other. This is particularly important because leakage of identity can create unfair advantage in an open buy/sell market.

How can we keep privacy, while bringing in the UX conveniences of meta-tx?

My current idea involves embedded meta methods directly into the ERC20 token, but i’m not sure if that’s a good approach?

## Replies

**pet3rpan** (2018-11-23):

You might benefit from watching the recent metacartel community call. We talked quite a bit about anonymous meta transactions https://www.youtube.com/watch?v=x8RPeH0OjCc

---

**suenchunhui** (2018-11-23):

hi [@pet3rpan](/u/pet3rpan), Thanks for the video link.

I’m not sure of the username of Ali who presented about anonymous meta tx, but I do have a question on that…

Does it mean that the technique have a similar semi-privacy guarantee to UTXOs in bitcoin? Since the origin address will be revealed during a coin transfer, so all spent transaction can be traced to form a transaction graph (but not future unspent ones)?

Its an interesting technique nonetheless.

