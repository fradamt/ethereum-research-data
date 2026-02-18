---
source: ethresearch
topic_id: 431
title: Log Type Parameters in the Validator Manager Contract (VMC)
author: ltfschoen
date: "2018-01-03"
category: Sharding
tags: []
url: https://ethresear.ch/t/log-type-parameters-in-the-validator-manager-contract-vmc/431
views: 1173
likes: 2
posts_count: 3
---

# Log Type Parameters in the Validator Manager Contract (VMC)

In the [VMC section of the Sharding Specification](https://github.com/ethereum/sharding/blob/develop/docs/doc.md#validator-manager-contract-vmc) it shows the Log Type syntax as `CollationAdded(indexed uint256 shard, `.

But is it meant to accept a `shard_id` rather than a `shard` for the first parameter?

## Replies

**mhchia** (2018-01-04):

Agree. IMO it refers to `shard_id`![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=9)

---

**vbuterin** (2018-01-04):

Yep, thanks for catching the error! Fixed.

