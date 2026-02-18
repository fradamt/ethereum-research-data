---
source: magicians
topic_id: 22678
title: "ERC-7868: Verifiable Cross Rollup Links"
author: shakeshack
date: "2025-01-27"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7868-verifiable-cross-rollup-links/22678
views: 87
likes: 0
posts_count: 1
---

# ERC-7868: Verifiable Cross Rollup Links

Cross rollup traffic should ultimately be secured by the L1. EIP-7868 propoose a standard around how different rollup frameworks can identify cross rollup dependencies enabling settlement time validation of cross rollup txs.

The end goal is to make both the L1 and its L2s one homogenous economic zone security wise.



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/863)














####


      `ethereum:master` ← `polymerdao:bo/xrollup-links`




          opened 01:08AM - 24 Jan 25 UTC



          [![notbdu](https://avatars.githubusercontent.com/u/8580333?v=4)
            notbdu](https://github.com/notbdu)



          [+117
            -0](https://github.com/ethereum/ERCs/pull/863/files)







This ERC proposes a specification for verifiable cross rollup links to enable se[…](https://github.com/ethereum/ERCs/pull/863)ttlement time verification of cross rollup transactions across different rollup frameworks.

The goal is to enable rollups of any framework to join a cluster and have cross rollup communication within that cluster secured by the L1.
