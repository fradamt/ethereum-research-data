---
source: magicians
topic_id: 1733
title: EVM Evolution Notes (Council of Prague)
author: expede
date: "2018-10-29"
category: Protocol Calls & happenings > Council Sessions
tags: [evm, council-of-prague, evm-evolution, ring]
url: https://ethereum-magicians.org/t/evm-evolution-notes-council-of-prague/1733
views: 905
likes: 1
posts_count: 1
---

# EVM Evolution Notes (Council of Prague)

# Council of Prague — EVM Evolution Notes

## General Discussion

- Lots of client and VM implementations actively being worked on
- All agree EVM design could use an update
- Some effort happening to explore storage becoming a key-value store
- Current EVM (partly) avoids being a bottleneck by using precompiles

Min performance requirement: finish on a reasonable machine under the blocktime

Client diversity lost due to the Shanghai attacks

- Had 5-7 clients prior

Polkadot has differentiation between consensus mining nodes vs follow-along clients
Roadmap? RChain-like features?

- As far as we can tell, there is no official EVM 1.x roadmap
- RChain (or similar) features unlikely at this point

Greg wants a formally verified VM stack

- Brooke:
- Seems uncontentious

Richer semantics at the VM layer

- Most present think that it would be great
- One dissenting voice, who wants to keep it feeling like being on the metal

## Work Left on Static Jumps and SIMD

(EIPs 615 & 616)

- C++ implementation exists
- Demitry(?) or someone else has to to write tests

## Gas Limit

- General desire to increase the gas cap
- Some thoughts on
- Could use money as a limit

If someone wants to spend thousands of dollars to run a long computation
- May hurt clients and low-power hardware
- Really just needs to complete before block time

## Yul

- Doesn’t have dynamic jumps
- Doesn’t have function pointers
- I mean, it’s meant to be higher level than the EVM bytecode

## Precompiles

- Resounding desire to not need precompiles
- Why precompiles rather than opcodes?

Only have 256 opcodes in a byte

Could have 2-byte opcodes, but adds complexity

Apparently Yoichi (not present) wants the VM to be kept very simple

Parity exploring lower level multi-sig

- Precomple vs EVM debate

## Performance

- Can’t emulate a 6502 on the EVM

Orders of magnitude too complex for current VM
- It’s VMs all the way down

## eWASM

- eWASM harder to tune for our use case
- LLVM (ie: ewasm) is complex, so if vulnerability found, it would take a while to fix

## Wish List

- Batch transactions
- ERC20-compatible Ether

Privileded token representing Ether

Arbitrary mod operations

- Scale gas by modulous number
- Dynamic jumps make this hard
- Reset mod flag manually

Gas model (quadratic) leads to unreasonable cost

- Perhaps should be exponential or other “brick wall”
- Or just keep a certain amount of memory available
- Change gas to reflect performance gains

Opcode to copy chunks of memory (`MEMCOPY`)

- Currently have to loop

Masking operations would be nice
