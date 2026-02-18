---
source: magicians
topic_id: 5496
title: Universal CREATE2 wrapper
author: fare
date: "2021-03-07"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/universal-create2-wrapper/5496
views: 690
likes: 0
posts_count: 2
---

# Universal CREATE2 wrapper

I have some use cases, including generalized state channels and verification challenges, where any of many users may want to create the contract to be verified, in the same spirit as Bitcoin MAST. CREATE2 *almost* gets us there, but annoyingly includes the creator address as part of the data getting hashes, which runs against the “the same contract binds everyone principle”. Lo and behold, this can be worked around by a contract that has this runtime code:

```auto
GETPC DUP1 CALLDATALOAD 32 CALLDATASIZE SUB DUP1 32 DUP5 CALLDATACOPY DUP3 CALLVALUE CREATE2 STOP
```

Now, I could create this contract on the Ethereum network, but wouldn’t it be nice if it had the very same address on every EVM network, so we could have universal MAST addresses? Well, that’s possible, thanks to presigned transactions: I generated an address, had it sign transactions to create the above contract with all possible values of gas on an geometric sequence of ratio sqrt(2), then threw the address away, so the same addresses can be used everywhere. It would be much nicer of course, if a precompiled contract did the same, but this is good enough for now.

[https://gitlab.com/mukn/glow/-/wikis/|Universal-CREATE2-wrapper](https://gitlab.com/mukn/glow/-/wikis/%7CUniversal-CREATE2-wrapper)

## Replies

**fare** (2023-02-28):

This is very useful for State Channels, wherein you know the terms of the contract, but don’t want to publish it in advance (for both scaling and privacy reasons), and especially do not know which of the participants will have to publish it because the other one fails to cooperate. Can we make it happen?

