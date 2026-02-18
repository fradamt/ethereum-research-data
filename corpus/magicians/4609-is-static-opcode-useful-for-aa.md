---
source: magicians
topic_id: 4609
title: IS_STATIC opcode (useful for AA)
author: vbuterin
date: "2020-09-13"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/is-static-opcode-useful-for-aa/4609
views: 2251
likes: 0
posts_count: 2
---

# IS_STATIC opcode (useful for AA)

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2975)














####


      `master` ← `vbuterin-patch-2`




          opened 01:36AM - 13 Sep 20 UTC



          [![](https://avatars.githubusercontent.com/u/2230894?v=4)
            vbuterin](https://github.com/vbuterin)



          [+39
            -0](https://github.com/ethereum/EIPs/pull/2975/files)







Add a `IS_STATIC (0x4A)` opcode that pushes `1` if the current context is static[…](https://github.com/ethereum/EIPs/pull/2975) (ie. the execution is in a `STATICCALL` or a descendant thereof, so state-changing operations are not possible), and `0` if it is not.












Returns whether or not the execution is in a static context.

## Replies

**chfast** (2020-09-20):

Easy to implement in projects I maintain.

