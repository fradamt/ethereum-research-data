---
source: magicians
topic_id: 23606
title: EOF Implementors Call, # 72, April 30, 2025
author: system
date: "2025-04-18"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eof-implementors-call-72-april-30-2025/23606
views: 63
likes: 1
posts_count: 2
---

# EOF Implementors Call, # 72, April 30, 2025

# EOF Implementors Call, # 72, April 30, 2025

- Apr 30, 2025, 14:00 UTC

# Agenda

- Testing
- Client Updates

EELS
- Geth
- Besu
- Reth
- Erigon
- EthereumJS
- Nethermind
- Evmone
- Solidity
- Vyper

Spec changes / updates

- EOF Bootstrapping  / To: nil
- EOF opcodes outside a container

Current / Next Tesnet
Other Issues

zoom: [Launch Meeting - Zoom](https://us02web.zoom.us/j/88940506383?pwd=aTdsbHVyMTNDSUFHYmhTWlI2ZEVldz09)

Facilitator emails (comma-separated): [danno.ferrin@gmail.com](mailto:danno.ferrin@gmail.com)

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : EOF Implementors Call
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : false
- display zoom link in invite : true

[GitHub Issue](https://github.com/ethereum/pm/issues/1489)

## Replies

**shemnon** (2025-04-18):

The two spec change topics represent potential additions to EOF, once utility and security are established.

# Allowing to:nil in Initcode Transacitons

This is the remaining question from meeting 71’s discussion on bootstrapping EOF contracts: should we allow ‘to:nil’ handling as seen in Frontier series transactions.

The [previous bootsrapping pre-read](https://notes.ethereum.org/@ipsilon/EOF-bootstrapping) listed sis options. Two prior bootstrap options are withdrawn in eof-devnet-1: (a) the predeploy contract due to technical details and ACD process concerns with the removeal of EIP-7666 from Fusaka scope and (b) EIP-7698 overloading of Frontier, access list, and fee market transactions.

The plan of record is to expose `TXCREATE` as an opcode outside the EOF container and allow non-container code to thus deploy EOF contracts into account code storage. This reflects what the [initial batch of eof-devnet-1 tests uses](https://github.com/ethereum/execution-spec-tests/releases/tag/v4.3.0).

Whether there are going to be “standard” `TXCREATE` contracts is an ERC question, as they ERC contracts can be deployed via existing toehold contracts enumerated in [RIP-7640](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7740.md) (Deterministic Deployment Proxy, Safe Singleton Factory, CreateX,  and the Create2 Deployer) and keep the same address in chains that support RIP-7640.

A lot of the discussion time was spent on address derivation for the options where `to:nil` is allowed in InitcodeTransacitons.  The tension was between two issues relating to adding the sender address to the address derivation: safety and cross-chain utility.  If the address is not added then a contract creation tx can be front run. However, if the contract does not rely on the creating address nor on other variable or side effects that could be changed (such as available ether) then the front-running is idempotent. This ability to be moved between callers is also how it gains the ability to be cross-chain safe, as long as the chain-id and sender address is not in the derivation then those can be changed in a transaction and it can be re-signed by another EOA on another chain.

Options to consider are

- Status Quo: no to:nil in Initcode Transactions
- Accepting the Security risk
- Providing configurability to optionally add sender restriction to the call (either via calldata encoding or anoter transaciton type)

# Adding EOF opcodes outside the EOF container

Another possible addition is to expose opcodes introduced for the benefit of EOF outside of the container. This is particularly relevant for the `PAY` opcode.  The facilitator in meeting 71 asked for those who would use these opcodes outside of an EOF container to comment in the relevant eth-magicians threads.  Those are:

- PAY opcode -  EIP-5920: PAY opcode
- RETURNDATALOAD, EXTCALL, EXTDELEGATECALL, EXTSTATICCALL opcodes - EIP-7069: Revamped CALL instructions

Collecively or individually, RETURNDATALOAD indificually and the EXT*CALL set are viable subsets.

`EXTCODETYPE` opcode - [EIP-7761: EXTCODETYPE instruction](https://ethereum-magicians.org/t/eip-7761-is-contract-instruction/20936)
`EXTCODEADDESS` opcode - [EIP-7880: EOF - EXTCODEADDRESS instruction](https://ethereum-magicians.org/t/eip-7880-eof-extcodeaddress-instruction/22845)

Opcodes with immediate arguments (such s RJUMP) and opcodes referring to the container itself (such as DATALOAD) are not good candidates for exposing outside the container.

