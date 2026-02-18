---
source: magicians
topic_id: 22466
title: EOF implementers call #65, January 22, 2025
author: abcoathup
date: "2025-01-09"
category: Protocol Calls & happenings
tags: [eof]
url: https://ethereum-magicians.org/t/eof-implementers-call-65-january-22-2025/22466
views: 77
likes: 1
posts_count: 2
---

# EOF implementers call #65, January 22, 2025

#### Agenda

[EOF Implementers Call #65 · Issue #1243 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1243)

#### Notes



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png)

      [EOF implementers call #65, January 22, 2025](https://ethereum-magicians.org/t/eof-implementers-call-64-january-22-2025/22466/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Meeting Notes
> Testing Update
>
> EEST
>
> All lingering PRs are merged
> We should wait for Devent 6 to settle before re-filling
> EOFWRAP relies on evmone which is not yet on pectra-5. Will be turned off until evmone is ready (some 7702 edge cases)
> Devnet 6 is a tiny change
>
>
> Fuzzing findings
>
> No new findings
> Fuzzing fails if clients are not on the same pectra devnet level
> Relies on new fields
> Tracing should support new tracing field RIP-7756
>
> PC zero to container is critical
> Function depth is currently…

#### Recording

  [![image](https://img.youtube.com/vi/5ywv6QpS2sE/maxresdefault.jpg)](https://www.youtube.com/watch?v=5ywv6QpS2sE)

## Replies

**shemnon** (2025-01-22):

Meeting Notes

# Testing Update

- EEST

All lingering PRs are merged
- We should wait for Devent 6 to settle before re-filling
- EOFWRAP relies on evmone which is not yet on pectra-5. Will be turned off until evmone is ready (some 7702 edge cases)
- Devnet 6 is a tiny change

[Fuzzing findings](https://github.com/shemnon/execution-spec-tests/blob/shemnon/eof-fuzz/src/ethereum_fuzzer_differential/__init__.py)

- No new findings
- Fuzzing fails if clients are not on the same pectra devnet level
- Relies on new fields
- Tracing should support new tracing field RIP-7756

PC zero to container is critical
- Function depth is currently needed

Clients need to target Getting up to Pectra Devnet 5/6 (whatever the last devnet becomes)

# Client & Compiler Update

- Nethermind, Besu, evmone, revm, erigon, all no changes
- Solidity - not much change, merged the base needed and testing.

Planning for Q1/Q2
- Deciding which optimizations to do

Vyper

- Not much change
- PyVM EOF support?

unknown, Mario will ask snake charmers
- Separate from EELS

# Spec And Other Issues

- EOF Metadata Section

An update after doing a spike for EIP-7834 (metadata section) in evmone and EEST. Ref.

Multiple optional sections makes things complicated.
- Very different from other sections, needs new code paths
- No suggestions for improvements, meets it’s goals

EEST Tests

- could automatically add metadata to standard tests, or a subset

Probably via a marker

Design wise more optional sections make parsing more complex

instead of a full re-filling.

- If we are sure it can be osaka we could make it mandatory

[EOFCREATE / TXCREATE potential features and scenarios](https://notes.ethereum.org/@ipsilon/SyrzctZSJg)- an opinion and/or counter proposals.

andCross-chain addresses (deterministic, counterfactual, and nonceless)

- Pitor reviewed doc

Scenario 1b is the preferred solution

EOFCREATE - sender+salt
- TXCREATE - sender + salt
- Predeploy (fka ISC) to load bootstrap contracts.
- Drop EIP-7720 (EOF create tx)

Discussion talked about pre-reployed contracts
This makes TXCREATE more palitable
New TXCREATE EIP

- Includes 2 toehold contracts - salt only and salt+=CALLER
- Maybe an address-based nonce-toehold as part of EIP and not ERC

We need a plan B for not having TXCREATE
RIP-7740 - [RIPs/RIPS/rip-7740.md at master · ethereum/RIPs · GitHub](https://github.com/ethereum/RIPs/blob/master/RIPS/rip-7740.md) - Preinstall deterministic deployment factories
Pre-ERC - EOF deterministic deployment contracts [ethereum/ERCs@master…shemnon:ERCs:eof/txcreate-factories](https://github.com/ethereum/ERCs/compare/master...shemnon:ERCs:eof/txcreate-factories)

~~Start work on Osaka-1 spec changes~~ out of time

# Other

