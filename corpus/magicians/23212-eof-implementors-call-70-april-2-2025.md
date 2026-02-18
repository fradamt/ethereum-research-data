---
source: magicians
topic_id: 23212
title: EOF Implementors Call #70 | April 2, 2025
author: system
date: "2025-03-20"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eof-implementors-call-70-april-2-2025/23212
views: 120
likes: 0
posts_count: 4
---

# EOF Implementors Call #70 | April 2, 2025

# EOF Implementors Call #70 | April 2, 2025

- April 3, 2025, 15:00 UTC  -  Apr 2, 2025, 14:00 UTC
- Duration in minutes : 60
- Recurring meeting : true
- Call series : EOF Implementors Call
- Occurrence rate : bi-weekly

# Agenda

Standing Agenda Framework

- Testing
- Client Updates
- Current/Next Testnet
- Spec changes/updates

Facilitator email: [danno.ferrin@gmail.com](mailto:danno.ferrin@gmail.com)

Facilitator telegram: shemnon

Edit to trigger bot

[GitHub Issue](https://github.com/ethereum/pm/issues/1397)

## Replies

**shemnon** (2025-04-02):

# Agenda

- Testing

Cutting final eof-devnet-0 tests
- Status of eof-devnet-1 tests
- Client request: code coverage report

Client and Compiler Updates

- Besu
- Erigon
- EthereumJS
- Evmone
- Geth
- Nethermind
- Reth
- Solidity
- Vyper

EOF devnet 1

- Status of client impleemntations
- TXCREATE and initcode transaction
- EOF Creator Contract Precompile/Predeploy

EOF devnet 2

- PAY opcode - EOF only?
- Symbolic Introspection (EXTCODEADDRESS, EXTCODETYPE)
- Metadata Section

Post-EOF denvet-2

- contract size update?
- Anything else in fusaka wishlist?
- CALL_GAS_SPLIT ethereum/EIPs#9558

---

**shemnon** (2025-04-02):

# Notes

- Testing

Finishing up devnet-0 PRs

new testing scenarios
- Will cut at or around prague releases?

TXCREATE Tests in progress

- A lot are migrated EOFCREATE
- 7623 has some testing impacts

All other tests are container format changes

- ex: 0x04 → 0xff tests underway
- Some new scenarios that may need to be considered, such as headers checking 0x05 and 0x06 need to include 0x04 now

TXCREATE lacks contract address bytecode in the testnet yet - Will dive in later
Client request: code coverage report

- CI generated coverage would be great

Have some level of eof-devnet-1 tests next week

Client and Compiler Updates

- Besu

devnet-1 implemented, except creator contract
- PAY opcode has a PR

Erigon

- Started fuzzing

EthereumJS

Evmone

- eof-devnet-1 changes ready, except creator contract
- PAY opcode not started

Geth

Nethermind

- Implemented PAY opcode for devnet-2
- No devnet-1 work yet, waiting on creator contract status, will proceed without it for now
- Will work off of a devnet-1 branch

Reth

- No updates, not started working on devnet-1

Solidity

Vyper

EELS

- Working on TXCREATE
- eips/osaka/eip-7692 - been rebased

Should we differentiate devnet-1 and devnet-2 tests?

- Possibly too much effort?

PAY outside of EOF containers?

- But it increases scope, for testing and security, and old CALL* paths

EOF devnet 1

- Status of client implementations

Implementation is mixed, blocking somewhat on EEST tests.

EOF Creator Contract Precompile/Predeploy

- If it’s a precompile we cannot EXTDELEGATECALL it without a rule exception
- Precompile also has to do “sub calls” - which is not like any other precompile
- Predeploy is better
- Do clients have code that code that can update state as part of a transition?

Is the DAO transition code generic enough?

Need to brace for pushback, but adding bytecode to the state is the cleanest approach
Could be a special transaction, on “magic” approved list (may be too complicated)
May be simplest to just have it be a system contract that executes first at the transition.

TXCREATE and initcode transaction

- Need to add to the TXFuzzer

Questions about container spec changes?

- Goal is the container is frozen to breaking changes after devnet-1
- Ipsilon needs to start tooling outreach in earnest then.

EOF devnet 2

- PAY opcode

EOF only? TBD, EOF requires it, non-container merely benefits from it
- Some clients have PRs ready
- Should we allow PAY in a static context?

Value == 0 will have no state change
- Recipient is same as sender will have no state change
- But logging may still happen when that EIP happens

Banning in a static context is cleanest, transferring value is the *intent* of PAY, not so much with zero value `CALL` / `EXTCALL`
What happens in a fail case?

- Not enough balance to send
- Fault?  Consume all gas?  Return error code?

Error code, consistent with value-bearing CALL / EXTCALL - return code 1
- Would be return code 0 outside a container, argument against non-container PAY access

Currently no return value, needs it.

Post-EOF denvet-2

- CALL_GAS_SPLIT ethereum/EIPs#9558

alternative is to add fraction to every EXT*CALL
- ben - not ideal, but better than gas introspection
- Add a max limit
- Add ‘magic’ symbolic values.

---

**shemnon** (2025-04-04):

Youtube Video: https://youtu.be/IdJeNWi4RWo

