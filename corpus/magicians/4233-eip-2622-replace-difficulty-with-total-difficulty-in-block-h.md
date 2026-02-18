---
source: magicians
topic_id: 4233
title: EIP-2622 Replace Difficulty with Total Difficulty in block headers
author: tkstanczak
date: "2020-04-29"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2622-replace-difficulty-with-total-difficulty-in-block-headers/4233
views: 513
likes: 3
posts_count: 1
---

# EIP-2622 Replace Difficulty with Total Difficulty in block headers

As in the topic - replace Difficulty with Total Difficulty in Block Headers.

This will help stateless clients (and any clients) to verify headers without full path to genesis.

This will help to pick best peers by quickly discarding fake total difficulty claims.

This will help with AddBlock messages validation.
