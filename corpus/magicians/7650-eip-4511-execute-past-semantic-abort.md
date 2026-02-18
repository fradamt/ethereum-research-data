---
source: magicians
topic_id: 7650
title: "EIP-4511: Execute Past Semantic Abort"
author: tsutsu
date: "2021-12-01"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-4511-execute-past-semantic-abort/7650
views: 698
likes: 0
posts_count: 2
---

# EIP-4511: Execute Past Semantic Abort

Allow clients to defer detection and enforcement of EVM revert conditions like out-of-gas, stack-overflow, etc. from the interpretation-step where the condition first applies, to some time later in the same call frame.

By removing these checks from the hot loop of EVM bytecode interpretation, a number of currently-impractical interpreter optimization strategies — such as threaded-code interpretation, or bytecode JIT — become practical.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4511)














####


      `master` ← `tsutsu:eip-execute-past-semantic-abort`




          opened 11:42PM - 30 Nov 21 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/8/8c26ca96aed5eaa39d9d4e8c833375294dc40bae.jpeg)
            tsutsu](https://github.com/tsutsu)



          [+116
            -0](https://github.com/ethereum/EIPs/pull/4511/files)







Proposes a "declared explicit intent to not standardize" a certain type of execu[…](https://github.com/ethereum/EIPs/pull/4511)tion tracing, in order to leave EVM implementations free to optimize how often they detect certain error conditions.

## Replies

**matt** (2021-12-06):

Hi [@tsutsu](/u/tsutsu) – not super familiar with these optimization strategies, but I don’t understand why threaded-code interpretation is impractical? [evmone](https://github.com/ethereum/evmone) uses indirect call threading rather efficiently. There was also a [JIT project](https://github.com/ethereum/evmjit) a while back.

