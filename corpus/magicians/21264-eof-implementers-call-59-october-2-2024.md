---
source: magicians
topic_id: 21264
title: EOF Implementers call #59, October 2 2024
author: abcoathup
date: "2024-10-04"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-59-october-2-2024/21264
views: 49
likes: 0
posts_count: 1
---

# EOF Implementers call #59, October 2 2024

#### Agenda

[EOF Implementers Call #59 · Issue #1162 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1162)

#### Notes

Notes by [@shemnon](/u/shemnon) *[Copied from [ethereum/pm](https://github.com/ethereum/pm/issues/1162#issuecomment-2388989786)]*

- Current release tests (EOF on top of prague) are broken

Besu had a 7702 bug, all non-7702 tests are fine.
- Next release will be released after devnet 4 is released
- PR reviews are mostly caught up
- Testing focus is on devnet 4 for the next week

Compiler

- Vyper create from blueprint needs a re-work for EOF.

Create form EXT Contract would have helped.
- Cannot blueprint off of any contract in EOF like you could in legacy
- A factory deployer would be good, delegate call into a contract that EOF creates. As opposed to an initcode only contract

Osaka Migration

- Clients need to target Osaka for EOF activation
- Tests need to target Osaka, including moving tests in source tree
- We have 6 more months to reifine the spec

We can look into HASCODE
- We can reconsider EXT*CALL return code numbers
- cleanup: EOFCREATE stack order
- cleanup: Remove hashing of container in EOFCREATE
- cleanup: Rename RETURNCONTRACT to RETURNCODE

Open questions

- Implications of gas introspection: regarding a gas to eth EIP.

Next Meeting:

- Rename RETURNCONTRACT → RETURNCODE
- HASCODE / ERC-721 solution
- EXT*CALL return code, keep or revise?
- EOFCRAE stack order
- remove container hashing in EOFCREATE

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/2/2304dcb4aa8307250d51ea404fc67cf2e93fc7f3.jpeg)](https://www.youtube.com/watch?v=TjZv8DMZka4)
