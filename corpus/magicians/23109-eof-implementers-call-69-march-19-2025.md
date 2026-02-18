---
source: magicians
topic_id: 23109
title: EOF Implementers Call #69 | March 19, 2025
author: system
date: "2025-03-10"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eof-implementers-call-69-march-19-2025/23109
views: 98
likes: 0
posts_count: 4
---

# EOF Implementers Call #69 | March 19, 2025

# EOF Implementers Call #69

- Date and time in UTC in format March 19, 2025, 15:00 UTC with link to savvytime.com or timeanddate.com. E.g. Mar 19, 2025, 15:00 UTC
- Duration: 60
- Zoom: Launch Meeting - Zoom
- Other optional resources

# Agenda

- Testing Update
- Client and Compiler Update
- EOF-devnet-1 changes
- EOF-devnet-2 changes

Other comments and resources

[GitHub Issue](https://github.com/ethereum/pm/issues/1361)

## Replies

**benaadams** (2025-03-19):

Please add to agenda for Devnet-1

- EIP-7830: 64kB Contracts EIP-7830: Contract size limit increase for EOF
- EIP-5920: PAY EIP-5920: PAY opcode

---

**shemnon** (2025-03-19):

Agenda —

- Testing

EOF Testing Roadmap.

Client Updates

EOF devnet 1

- TXCREATE and initcode transaction
- PAY opcode?
- contract size update?

EOF devnet 2

- Symbolic Introspection (EXTCODEADDRESS, EXTCODETYPE)

---

**shemnon** (2025-03-19):

Notes

Testing

- Mario just got back from vacation

Not reviewing PRs in draft, take them out of draft if you want a review

question about blockchain engine tests - Will they give us any signal?

- These are tests using hive instead of other APIs.  Using the engine API.  Same tests as state tests and blockchain tests.  Different consumption route.
- Clients may skip as right now it will give no extra signal.  All tests are just EVM, unlike payload arguments and stuff like consolidations/withdrawals.

EOF Testing Roadmap

- when do we want certain testing deadlines?

Mario:

need to finish the EOF tracker.

tracker is the list of tess from legacy tests.

need to review all ported tests
need code coverage metics in eels, possibly other clients

- at least line coverage, maybe branch and path coverage too

ASAP?  by when?
hive discussion

- should be able to spin up hive as we have a live devnet.  It’s all the same code paths.

Coverage discussion

- Why EELS?  Readable instead of optimized, makes missed cases more obvious when run against coverage tools
- clients may be informative by EELS should provide most signal
- evmone is at 100% line coverage from EEST

Pavel: Old tests repo has no relevant tests that are not already in EEST.  Only fuzzer generated tess and out-of-date tests
Will provide reports in next call
Clients: please have code coverage reports for next week.

- client updates

Nethermind: passing all current tests devnet-0
- Besu: devnet-1 initial implementation, waiting on EEST for devnet-1
- evmone: preparing devnet-1 changes. some but not all done.
- EELS:  no updates, not based on current head.  Guru is the expert.
- Erigon: reported passsing eest test devnet 0
- Solidity:

prototype compiler was released
- optimizer not turned on, will work on that later

No Reth, Geth, Vyper reports.

Devnet 1

- TXCREATE and initcode

addresses many complaints about EOF
- generally in a good place

evmone will help provide EEST tests

- stack order done, data 0x04 → 0xff

PAY Opcode

- Proposed to add to devnet 1
- Fixes some issues noted in eth-magicians and twitter.
- Just a trimmed down call opcode, implementation wise
- Besu and nethermind support
- was nice to have in legacy, needed in EOF because of gas introspection changes
- Maybe move to glamsterdam?
- There are other reentrancy solutions, but sometimes we want it.
- Discussion about inclusion.
- What are alternative re-entrency solutions?  TSTORE/TLOAD, SSTORE/SLOAD (both expensive). checks-effects-interaction (gold standard)
- Target devnet 2 - testing burden is the real cost.

Contract size update

- two competing proposals - 7830 and 7907
- Need ACD presentation on these two before consideration can be done.

variable costs may present security problems
- In OZ codesize > 0 is a common test, so clients would need to cache sizes
- EOF Code sections could help with statelessness
- No broad support for either devnet or devnet 2

