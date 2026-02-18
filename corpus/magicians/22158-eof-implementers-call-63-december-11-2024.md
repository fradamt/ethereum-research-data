---
source: magicians
topic_id: 22158
title: EOF implementers call #63, December 11 2024
author: abcoathup
date: "2024-12-11"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-63-december-11-2024/22158
views: 36
likes: 1
posts_count: 2
---

# EOF implementers call #63, December 11 2024

#### Agenda

[EOF Implementers Call #63 · Issue #1205 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1205)

#### Notes



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png)

      [EOF implementers call #63, December 11 2024](https://ethereum-magicians.org/t/eof-implementers-call-63-december-11-2024/22158/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Meeting Notes
>
>
> Clients and Compilers
>
> Solidity
>
> some functionality merged,
> updating solidity tests (proves correct compilation)
> working on stability next
>
>
> Frangio is working on a new EVM assembler for EOF and Legacy
>
> Do any assemblers output EOF as well? Other than YUL?
> EXCHANGE opcode textual representation, how?  [n, m-n] or [n, m]?
> (mixed prefs, closer to bytecode/Internal encoding vs user meaning)
> proposal will be made for review in 2 weeks
>
>
>
>
>
> Spec Changes
>
> Metadata
>
> Possibly change da…

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/2/2304dcb4aa8307250d51ea404fc67cf2e93fc7f3.jpeg)](https://www.youtube.com/watch?v=2Z5YPfOnb74)

## Replies

**shemnon** (2024-12-11):

# Meeting Notes

- Clients and Compilers

Solidity

some functionality merged,
- updating solidity tests (proves correct compilation)
- working on stability next

Frangio is working on a new EVM assembler for EOF and Legacy

- Do any assemblers output EOF as well? Other than YUL?
- EXCHANGE opcode textual representation, how?  [n, m-n] or [n, m]?
- (mixed prefs, closer to bytecode/Internal encoding vs user meaning)
- proposal will be made for review in 2 weeks

Spec Changes

- Metadata

Possibly change data to 0xff (and reserve 0x04)
- Not all containers use metadata in runtime containers

initcode only,
- tx data only
- Event during initcode

Keeping initcode separate from runtime code makes sourcify’s job harder

- metadata in tx only requires archive data of all deployment transactions

There is an appeal to unreadable code in runtime, but perhaps we need different conventions for compiler metadata
Mixing metadata with code produces runtime issues with indexes into the data and makes metadata discovery difficult.

Generic Contracts and Deterministic / Counterfactual Deployments

- There is a desire for contracts at the same address on multiple chains
- Ways it’s done

Nick’s method is used to create a single-use TX to make a fixed address (chain #0, high fees)
- CREATE2 deployer deployed w/ Nicks Method (most used factory)
- createx - GitHub - pcaversaccio/createx: Factory smart contract to make easier and safer usage of the `CREATE` and `CREATE2` EVM opcodes as well as of `CREATE3`-based (i.e. without an initcode factor) contract creations.

createx factory is not implementable in EOF right now.

- Will TXCREATE fix this? (eof/spec/eof_future_upgrades.md at main · ipsilon/eof · GitHub)

App devs use both salted create2 and nick’s method

- Nick’s method is hard on some other chains, no toehold.

Can only deploy code in containers, not arbitrary contracts
General question on how to get reliable addresses in Eth w/o “toehold process.”

Unsalted deployed - nonce derived address

- EOFCREATE and TXCREATE require a salt, no nonce.
- Could the factory maintain this?
- Possibly remove the “witness” from the address. (https://github.com/ipsilon/eof/issues/162)

Witnesses include: initcode, code address (sender or caller), initcode container index
- Removing the witness makes counterfactual addresses more difficult.

Time boxed at 15 minutes

Code Size EIP

- Needs to be accompanied by EOF changes to support > 64KiB containers / code / etc.

Testing

- Devnet 5 is the focus, no EOF work due to priority
- Fuzzing and Tracing overview

