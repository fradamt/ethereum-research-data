---
source: ethresearch
topic_id: 7321
title: Looking for ZK-ZK rollup proposals for headers
author: ciwobof900
date: "2020-04-25"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/looking-for-zk-zk-rollup-proposals-for-headers/7321
views: 1564
likes: 0
posts_count: 2
---

# Looking for ZK-ZK rollup proposals for headers

Is there a detailed ETH Research proposal or EIP proposal on how to rollup Ethereum block headers into a single block to avoid clients having to download the entire chain?

## Replies

**lithp** (2020-08-22):

No, this does not currently exist. Starkware might be working on something like this? I’m not sure. I’m not very familiar with the current state of the art re rollups, but any scheme which tries to do this will need to encode the entire EVM into their proving system, which I believe is beyond current capabilities.

