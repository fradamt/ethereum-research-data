---
source: ethresearch
topic_id: 6002
title: Great paper analyzing gas pricing
author: virgil
date: "2019-08-20"
category: Economics
tags: []
url: https://ethresear.ch/t/great-paper-analyzing-gas-pricing/6002
views: 1047
likes: 0
posts_count: 2
---

# Great paper analyzing gas pricing

![image](https://static.arxiv.org/static/browse/0.2.7/images/icons/favicon.ico)
      [arXiv.org](https://arxiv.org/abs/1905.00553)


    ![image]()

###

Ethereum's Gas mechanism attempts to set transaction fees in accordance with
the computational cost of transaction execution: a cost borne by default by
every node on the network to ensure correct smart contract execution. Gas
encourages users to...








The most notable things to me from this are:

- Several opcodes are currently vastly underpriced in gas.  Particularly,

SDIV
- SLOAD
- BALANCE
- SGT
- BLOCKHASH is also mentioned but that gas fee went up in Constantinople.  It may still need to be increased further.

Nodes with beefy RAM seem to have significant competitive advantages over more consumer grade nodes (16GB).

There’s likely some database optimizations we could make in LEVELDB to improve performance and rreduce variability—particularly on lower-end machines.

It may be sensible for client operators to publish suggested specs for minimal hardware.

Verifiable computing methods will definitely help.

## Replies

**jgm** (2019-08-20):

I’d like to see similar tests carried out against other client software (notably geth and parity) before any conclusions were drawn against the data.

