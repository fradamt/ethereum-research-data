---
source: magicians
topic_id: 5302
title: "EIP-XXXX: SSTORE revert gas refund"
author: k06a
date: "2021-02-08"
category: EIPs
tags: [opcodes]
url: https://ethereum-magicians.org/t/eip-xxxx-sstore-revert-gas-refund/5302
views: 999
likes: 1
posts_count: 1
---

# EIP-XXXX: SSTORE revert gas refund

# Simple Summary

What’s the reason behind no gas refund for the cases when storage was not changed? For example, storage can be initialised, then erased and due subcall revert gas refund will not happened while storage remain unchanged. This makes transactions cost more than expected.

```auto
SSTORE(ptr, 1)
SSTORE(ptr, 0)
REVERT(0, 0)
```

What do you think about creating EIP to keep gas refund or even apply immediately right after internal revert?
