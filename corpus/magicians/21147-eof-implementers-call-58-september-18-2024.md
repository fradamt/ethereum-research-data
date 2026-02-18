---
source: magicians
topic_id: 21147
title: EOF Implementers call #58, September 18 2024
author: abcoathup
date: "2024-09-20"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-58-september-18-2024/21147
views: 58
likes: 0
posts_count: 1
---

# EOF Implementers call #58, September 18 2024

#### Agenda

[EOF Implementers Call #58 · Issue #1146 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1146)

#### Notes

Notes by [@shemnon](/u/shemnon) *[Copied from [ethereum/pm](https://github.com/ethereum/pm/issues/1146#issuecomment-2358853729)]*

- Client Discussion
- Discussed Split

pt 2 should follow w/in 3-6 months
- mild preference for one merge, but not enough to block
- concern about scope creep and moving actual shipment to 1 year

Compiler Updates

- None

Specs

- Tracing

evmone will look into implementing, but may have changes to proposle

HASCODE/ISCONTRACT

- Discussed AA concern in discord

AA is concerned about the pattern where non-eoa accounts are barred, HASCODE could be used to perpetuate that and slow AA adoption
- Also, 721 could be solved better with ERC-165 interface
- counter: AA is slowed by lack of smart contract signatures
- counter: Banning EOAs possible w/o HASCODE
- No conclusion yet

Could pectra split allow it to be added in V1?

- Some preference to be in a follow-on fork, but preference may have been driven by time to gather data
- Split is because of EIP bloat, adding a new EIP would counter the solution
- At least 1 client wants to include it for V1

Absence could slow adoption of EOF (Any ERC-721/ERC-1155 or flashloan project for example)

There is concern that 721 and 1155 are badly designed, and so this pattern won’t re-occur. An update of 721 could provide the same protections and conform to modern practices.
AA accounts could implement 165, but then they would have to have the 721 callbacks active.
See note below about EXTDELEGATE and proxies

EXTCALL return codes

- intent
- 1 - gas was not burned as part of the violation

User reverts
- Some failures related to call process

2 - all gas consumed as part of the failure

- Out of gas
- RETURNDATA copy oob in legacy
- static call violation
- data stack overflow

No action today

Allow EXTDELEGATECALL to legacy

- This is another use case for HASCODE, to ensure EOF proxies won’t delegate to a legacy contract

This could be solved with a “handshake” method or a trial delegate call

Testing

- PRs will be reviewed
- 7702 testing

many clients were rejecting incorrectly
- execute mode in EEST can address this problem - uses JSON-RPC only to interact with node

Bikeshedding

- Can we rename types to stack-io in the spec? types was not terribly clear.

stack-io
- section-info or section-spec
- code-info
- signature(s)

Standing agenda should move testing to the first items
