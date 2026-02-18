---
source: magicians
topic_id: 22700
title: EOF implementers call #66, February 5, 2025
author: abcoathup
date: "2025-01-28"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-66-february-5-2025/22700
views: 73
likes: 1
posts_count: 2
---

# EOF implementers call #66, February 5, 2025

#### Agenda

[EOF Implementers Call #66 · Issue #1260 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1260)

## Replies

**shemnon** (2025-02-05):

## Agenda

- Testing Updates

General EEST updates (mario)
- Converting legacy tests to EEST (@chfast)

Client and Compiler Update

Non-specification Issues:

- Proposed testnet plan: Osaka Testnets Plan - HackMD

Specification Issues

- Osaka-1 cleanup items

Section Type Malleability ipsolon/eof#176
- Remaining List of items

Modify type section to have “additional stack” instead of total stack
- Change EOFCREATE stack order to match EXTCALL
- Any other stack arg re-ordering to align with legacy or other EOF ops
- Rename RETURNCONTRACT to RETURNCODE
- Change data section index from 0x04 to 0xff

Retire the 0x04 header ID.
- A more worked out example - Improve generic EOF header · Issue #181 · ipsilon/eof · GitHub

Change CREATE/CREATE2 to an exceptional halt when seeing EOF (was fails and returns 0)

TXCREATE [EIP-7873](https://github.com/ethereum/EIPs/pull/9299/files?short_path=f9e4aac#diff-f9e4aac074d7b4ec62e32d78d6107364f7e3470ba61809a24b26675b45bfe7f4)

- Q: Do we need to block DELEGATECALL?

Will impact generated address namespace

Q: Is address hashing OK with everyone?
Q: Is toehold contract OK wih everyone?
Q: What other toehold variants for the ERC?

Add Metadata Section [EIP-7834](https://eips.ethereum.org/EIPS/eip-7834)
Add EXTCODETYPE [EIP-7761](https://eips.ethereum.org/EIPS/eip-7761)
Add EXTCODEADDRESS opcode

## Notes

- Testing

Mario discssed Improve generic EOF header · Issue #181 · ipsilon/eof · GitHub

There are some validaiton tests that don’t work running live, due to size
- Markers will be added to mark some parameters as non-fillable
- Execute has a hive mode, mocks the CL

Pawel spoke about Converting legacy tests to EEST

- Tried to hand convert legacy tests

Months to a year if done by hand

Wrote python automated conversion wrapper
Some tests are obvious, some are obfuscarted
Discussed eof/statetest fixture

Client and compier updates

- Nethermind did some merges and are part of Danno’s fuzzing
- Solidity

merged some code relating to tests
- Release in the coming weeks to test the prototype
- Want to prepare a list of breaking changes for EOF
- Looking into low level bytecode optimizaitons,
- Look into using dupn/swapn to fix stack too deep
- roadmap Refine and Stabilize EOF Support · Issue #15310 · argotorg/solidity · GitHub

tesnet plan

- osaka-1 is where the bulk of the spec freezes, for tooling support.

Spec Issues

container heder codes

- large subcontainers?
- VLQ encoding?

Punch list discussion

- max stak height
- code section type malliability fix - require full stack range to be accessed

has impact on register conversion logic if not fixed
- easy to circumvent with deep swaps/dupn pop.

Punch list items will just be amendments to the existing EIPs.

TXCREATE

- Question to 0X - what is the ideal predeploied toehold

ERC factories

not guaranteed to be there.
- Tooling cannot assume
- Adds complexity
- Single toehold may be sufficient, keep the ERCs not “official”

EXTDELEGTECALL creates different namespace - feature, not a bug.

- Perhaps Mandatory delegatecall

