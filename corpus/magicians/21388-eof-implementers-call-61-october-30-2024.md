---
source: magicians
topic_id: 21388
title: EOF Implementers call #61, October 30 2024
author: abcoathup
date: "2024-10-17"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-61-october-30-2024/21388
views: 66
likes: 2
posts_count: 1
---

# EOF Implementers call #61, October 30 2024

#### Agenda

[EOF Implementers Call #61 · Issue #1184 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1184)

#### Notes

Notes by [@shemnon](/u/shemnon) *(Copied from [ethereum/pm](https://github.com/ethereum/pm/issues/1184#issuecomment-2447633714))*

- Clients

Nethermind -

merged osaka fixes,
- based off of prague / main

reth

- has osaka wired in,
- Fixed one bug with precompiles and EXTDELEGAGECALL

evmone transition to osaka is larger than expected

- Migrated all ethereum/tests state tests over to EEST
- EOF validation tests are not moved over yet
- Some evmone tests are not ported yet - EVMONE v13 tests

Besu

- osaka ready in main
- prague-3/4 - based on where main besu gets to

Spec Changes

- EXT*CALL

discuss after devcon

EOFCREATE hashing

- multiple initcode contexts are creaed
- Using container address only works for first level, not nested creates
- create transaction - sender has no code so container address won’t work
- Not always possible to point to a “physical address” of the container holding the initcode
- Maybe omit address, and still hash subcontainer when it cannot be proved, but computation time is different in two scenarios
- Goal is to reduce extra hashing
- Useful property is to prove code came from a specific code (not just address)
- Is it possible to defeat polymorphic code?
- Should auxdata be included?

Change max stack height - to be stack needed in addition to inputs

- makes the two fields (inputs / max stack) unrelated, rather than max >= inputs
- rename the field from max_stack_height to… max_stack_increase
- EEST has some auto-calculations we could leverage, client unit tests would incur ~4h work
- Quality of Life fix, can miss if we are shipping Q1, but if we had 6 more months would be worth looking into for devnet-1

Re-order EOFCREATE to match EVMCALL

- same QoL level of effort. Can miss, but if we have time worth adding.
- Feels “small”
- Valuable for tooling and developers manually debugging code, to not have to swap elements

Rename RETURNCONTRACT to RETURNCODE
Zero client impact, opcode stays the same
Documentation changes only
QoL for devnet-1
Please comment on EXTCODE* after devcon (//TODO add link)
EXTDATACOPY and EXTDATASIZE (//TODO add bug link)

- Target memory? SSTORE2 will use return buffer
- When SSTORE2 is used in this context really we are talking about just the read side, not write
- Question now is smart contract read methods equivelantly good.
- How does it handle legacy and delegate contracts? Read like EXTCODECOPY? Zeros? fault?
- Would EXTDATALOAD be needed too? (no EXTCODELOAD…)

DELEGATECALL to legacy

- If we fail we need to be able to detect legacy contracts safely and easily
- Could we further tweak SELFDESTRUCT to behave differently when a delegate of EOF?

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/2/2304dcb4aa8307250d51ea404fc67cf2e93fc7f3.jpeg)](https://www.youtube.com/watch?v=kBQoRdBg4Vg)
