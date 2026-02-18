---
source: magicians
topic_id: 23386
title: EOF Implementors Call, #71, April 16, 2025
author: system
date: "2025-04-04"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eof-implementors-call-71-april-16-2025/23386
views: 82
likes: 0
posts_count: 2
---

# EOF Implementors Call, #71, April 16, 2025

# EOF Implementors Call, #71, April 16, 2025

- Apr 16, 2025, 14:00 UTC
- Duration in minutes : 60
- Recurring meeting : true
- Call series : EOF Implementors Call
- Occurrence rate : bi-weekly
- Already on Ethereum Calendar : true
- Need YouTube stream links : False

# Agenda

- Testing
- Client Updates

Nethermind
- Evmone
- Reth
- Geth
- EthereumJS
- EEST
- Besu
- Erigon
- Vyper
- Solidity

Spec changes / updaes

- EOF Bootstrapping EOF bootstrapping - HackMD

Current/Next Testnet
Other comments and resources

Zoom Link: [Launch Meeting - Zoom](https://us02web.zoom.us/j/88940506383?pwd=aTdsbHVyMTNDSUFHYmhTWlI2ZEVldz09)

Facilitator email: [danno.ferrin@gmail.com](mailto:danno.ferrin@gmail.com)

[GitHub Issue](https://github.com/ethereum/pm/issues/1429)

## Replies

**shemnon** (2025-04-16):

I like how the system keeps the posting in line with the Github issue ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15) [@nicocsgy](/u/nicocsgy)

# Call Notes

## Testing

- Planning a release soon for Pectra “final”

would like eof-devnet-1 release
- concerned about in-progress breaking changes from eof-devnet-0

missing coverage is OK
- should only be TXCREATE/EOF Bootstrapping and removing EIP-7698

Fuzzing

- start fuzzing next week

## Client/Compiler Updates

- Nethermind

Passing devnet-0 tests (tests v 2.2)
- merged to master
- devnet-1 being worked on

evmone

- Passing devnet-1 (because it’s filling the tests)

Reth

- 1 bug on devnet-0 fixed
- running sate tests
- running some devnet-1 tests

currently in TXCREATE

Geth

- no update

EthereumJS

- no update

EELS

- passing 2.3 devnet-0 tests
- PRs for TXCREATE pending resolution of bootstrapping discussion
- devnet-1 otherwise fine

Besu

- eof-devnet-1 fixing extdelegatecall bug and txcreate gas bugs
- PAY opcode - targeting devnet 2
- question on legacy support of compatible EOF opcodes

Erigon

- No Update
- racytech fork passed EOF-devnet-0 fuzzing

Vyper

- No updates

Solidity

- radak has PRs i queue
- working on pectra
- working on eofcreate in assembly
- assembly is complicated, crosses the line between custom container and assembly code

q: how are creation salts handled?

- right now user provided salt, used as-is
- No plans for a default solution

q: support new Foo{salt: salt}(input) - has legacy/eof semantic differences

- Won’t have a drop-in replacement
- frangio: not a good idea, we need to preserve semantics, need to hash with foo’s bytecode, as well as the input data hash.  Perhaps rawsalt is the unchanged salt, and salt has the initcode and input brought into the salt calculation. Just new Foo(input) not compiling is insufficient, the salt should include data hashed from input and initcode to match legacy security guarantees.
- piotr: the rawsalt hashing will be cheaper, there are cost implicaions with EOF.
- cameel: Daniel prefers rawsalt == salt, please come on our calls to discuss with daniel. We need a non-solidiy opinion on this.

## Spec Changes / Updates

### Legacy opcode support

- Is PAY legacy support

Danno’s proposal: wait for a request to be made in the appropriate EIP’s eth-magician threads
- PAY, however, uses EOF’s return code semantics and we would introduce that into legacy if we bring it over, or we would need to change the opcode for legacy
- In general, we need to keep the possible differences in behavior in legacy.
- Frangio thinks differing impls based on context is a bad idea, and that users will just need to keep in mind what is happening.
- What is the impact?  Clients is mostly small, EEST tests are larger
- Frangio - waiting for requests could be a while, bad for “outsiders” who don’t keep up.
- How do we know which ones?
- Not including is not an irrevokable decision, just costs time (on the order of a year)
- Possibly RETURNDATALOAD, and EXTCALL opcodes into legacy
- Time boxed  discussion, no decisions.

### EOF Bootstrapping

- Danno summarized the document
- Q: Why does option 4 and 6 limit it to one initcode?

felt cleaner
- not mandatory
- could be changed

Q: Address of 4?

- same as types 0, 1, 2 - nonce based

Note options 5 and 6 provide cross-chain address niceness.

- no dependency on nick’s method, with no nonces.
- also 5 and 6 do not include the address of the sender
- 5 and 6 can be front run, does not include address.
- including the sender means you cannot un-include this

option 7 propsoed: execute initcode as legacy and allow it to TXCREATE
Tension is address of sender vs. front-running capability.
If your contract doesn’t use sender or tx.origin, or the value, then frontrunning is a wierd suprise.  Contract creation that depends on externalities will be vulnerable
Main question: Stick with 3 for devnet-1?  Will it hurt adoption?  Can we add a variant of 4,5,6 in the future?
Temporary solution: 3 and 3 alone.
Meet in one week to discuss

- continue discussion Eth R&D evm channel on discord and in EIP-7873: EOF - TXCREATE and InitcodeTransaction type
- Will post better distillation of the issues in a follow on comment by AMER COB Wednesday.

## Current / Next Testnet

eof-devnet-1 tests will be release assuming TXCREATE is in legacy

## Other Items

no time.

