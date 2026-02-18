---
source: ethresearch
topic_id: 3141
title: Example of Garbage/gas collection for 0x
author: kaibakker
date: "2018-08-29"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/example-of-garbage-gas-collection-for-0x/3141
views: 1080
likes: 0
posts_count: 1
---

# Example of Garbage/gas collection for 0x

I considered garbage collection (gas collection) for 0x, these can be generalized to other contracts. Here are my thoughts:

Garbage collection can be used to subsidize certain parties or functionality, by freeing up data and allowing functions to have a net negative gas fee. Pseudocode example:

free(Order[] orders) {

order for each orders

require(order.expiresAt < now)

delete transactions [keccak(order)]

}

Profit: 9000 gas per order.

For 0x it might be interesting to allow the relayer to call free. The average fee per executed order is around 90000 gas. Gas collection Offers a 10% discount as a subsidy for relayers.

Are there other examples of projects using garbage collection as a subsidy?
