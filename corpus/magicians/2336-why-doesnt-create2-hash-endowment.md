---
source: magicians
topic_id: 2336
title: Why doesn't CREATE2 hash endowment?
author: jochem-brouwer
date: "2019-01-04"
category: Uncategorized
tags: [opcodes, questions]
url: https://ethereum-magicians.org/t/why-doesnt-create2-hash-endowment/2336
views: 929
likes: 0
posts_count: 2
---

# Why doesn't CREATE2 hash endowment?

CREATE2 is useful for state channels so a user is certain that at some point a specific contract can exist at an address which can be calculated beforehand. That this address is created from hashing the current address calling CREATE2, a salt and the deploy bytecode seems logical to me. However, in a constructor (and even when calling the CREATE2 opcode) we can send value together with the deployment bytecode. What was the design choice not to hash the call value?

## Replies

**fare** (2021-01-03):

When that matters, can’t the init code (which is hashed) use VALUE to check the endowment as part of the init code?

