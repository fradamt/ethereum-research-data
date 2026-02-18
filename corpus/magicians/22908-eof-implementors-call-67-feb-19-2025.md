---
source: magicians
topic_id: 22908
title: EOF Implementors Call #67, Feb 19, 2025
author: shemnon
date: "2025-02-19"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eof-implementors-call-67-feb-19-2025/22908
views: 43
likes: 0
posts_count: 2
---

# EOF Implementors Call #67, Feb 19, 2025

#### Agenda

[EOF Implementers Call #67 · Issue #1277 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1277)

## Replies

**shemnon** (2025-02-19):

#### Agenda

- Testing Update

eof-devnet-0
- EEST

Client and Compiler Updates

Devnet-1

For tomorrow’s EOF call I feel we need to lock down eof-devnet-1 scope so we can start executing it.

I think we need to front load all breaking changes

Move TXCREATE into devnet-1 TXCREATE [EIP-7873](https://eips.ethereum.org/EIPS/eip-7873)

- This includes the Initcode transaction type
- This includes the toehold creator contract
- This includes removing EIP-7698 creation contract support

existing devnet-1 planned changes

- Alter EOFCREATE Hashing (Just ADDRESS + salt, same as TXCREATE)
- Change EOFCREATE stack order to match EXTCALL
- making 0x03 container sizes 4 bytes instead of 2
- Change data section to 0x04 to 0xff
- Change CREATE/CREATE2 behavior when seeing EOF, back to pectra behavior
- Rename RETURNCONTRACT to RETURNCODE
- extra stack in types instead of total height

Arrange audit for creator contract

Post Devnet-1 changes

- Metadata Section EIP-7834
- TXCODEADDRESS EIP-7761  and TXCODETYPE EIP-7880

Add EIPs to backlog

- EIP-5920 - PAY (needs new opcode #)

#### Notes

- Discussed proposal for devnet 1

 Nethermind is in favor, some concern with backwards incompatible changes but we are bringing them all in.
- evmone/ipsilon - sounds good, want to paus pose devnet-1 changes to later
- For testing, get evmone working with txcreate very fast, then EEST will be able to asses imact.
- We also need creator contract support.  We can punt initially by putting it in genesis,

We need state transition support to add the contract

we need to coordinate with peerdas for transaction type number, may be a conflict (EOF gets lower number is the initail proposal)

4 byte container size

- Geth: +1
- evmone: has concerns about consistency with he vision for the header parsing, but it’s already been altered as you need to know the parsing of each specific section

evmone will prototype and report back in 2 weeks.

wen eof-devnet-1?

- April 8th is ideal, depends on results of evmone explorations.

