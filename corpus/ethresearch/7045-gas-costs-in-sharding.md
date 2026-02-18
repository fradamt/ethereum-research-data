---
source: ethresearch
topic_id: 7045
title: Gas costs in Sharding
author: kashishkhullar
date: "2020-02-29"
category: Sharding
tags: []
url: https://ethresear.ch/t/gas-costs-in-sharding/7045
views: 1064
likes: 0
posts_count: 1
---

# Gas costs in Sharding

In inter-shard communication receipts from one shard is sent to another shard as a confirmation of processing a transaction in the first shard. The other shard accepts the receipts or “consumes it” to make changes to the account of the person of other shard.

How much gas is used by the inter shard communication for consuming receipts? First in the shard where the sender is, and second where the receiver, thus can we say that the intershard transaction are using double the gas than intrashard communication.
