---
source: ethresearch
topic_id: 3467
title: Transaction throughput under Shasper
author: econoar
date: "2018-09-21"
category: Sharding
tags: []
url: https://ethresear.ch/t/transaction-throughput-under-shasper/3467
views: 2001
likes: 9
posts_count: 3
---

# Transaction throughput under Shasper

Hi all,

I’ve been diving into the Shasper spec and have been crunching some numbers on what it will mean for network throughput. I’m looking for some input on my calculations as well as a question I have on block gas limit.

Here is what I have right now. Everything on the “current chain” section are real numbers with no assumptions.

| Value | Current Chain | Shasper |
| --- | --- | --- |
| shards | 1 | 1024 |
| block(slot) time | 14.5 | 8 |
| blocks/minute | 4.1 | 7680 |
| blocks/day | 5,959 | 11,059,200 |
| blocks/year | 2,174,896 | 4,036,608,000 |
| ​ | ​ | ​ |
| block gas limit | 8,000,000 | 8,000,000* |
| daily gas cap | 47,668,965,517 | 88,473,600,000,000 |
| avg gas/tx | 76,364 | 76,364 |
| ​ | ​ | ​ |
| tx/day cap | 624,237 | 1,158,582,857 |
| tx/min | 434 | 804,571 |
| tx/sec | 7.2 | 13,410 |

My main question revolves around block gas limit. What are the thoughts on how much this can increase under Shasper? I’m currently keeping the assumption at the same limit but assume this can go way up.

Any feedback is appreciated!

## Replies

**vbuterin** (2018-09-21):

I’d say keep it at 8M. Realistically, it will go up because of EWASM but then the costs of many operations will also go up, so you’ll be able to do more computation within a block in some cases and the same amount in other cases (and still other things will get more expensive, particularly mass storage access).

---

**econoar** (2018-09-22):

What are your thoughts on accounting for cross shard tx in this? Should I just assume x% of tx will be cross shard? 30k gas for those?

