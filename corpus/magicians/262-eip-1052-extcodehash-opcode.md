---
source: magicians
topic_id: 262
title: "EIP-1052: 'EXTCODEHASH' opcode"
author: Arachnid
date: "2018-05-02"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1052-extcodehash-opcode/262
views: 6189
likes: 6
posts_count: 11
---

# EIP-1052: 'EXTCODEHASH' opcode

I’ve written an EIP proposing a new ‘EXTCODEHASH’ opcode [here](http://eips.ethereum.org/EIPS/eip-1052). Feedback appreciated!

## Replies

**holiman** (2018-05-03):

I think that one has been suggested before, and I’m all for it.

---

**fubuloubu** (2018-05-03):

I think this is a no brainier.

Would it be a constant gas operation?

---

**veox** (2018-05-17):

Sounds quite useful!

Need clarification in EIP: what should happen if the argument taken from the stack (assumed to be address):

- is over (or: is not exactly) 20 bytes long? EDIT: Perhaps: "same answer as for BALANCE"?
- is a precompile address (a non-bytecode one like 0x01..0x04)? EDIT: Perhaps: "if it does have EVM bytecode in the state, then a hash of that; if nothing, then 0x, i.e. nothing, - not a hash of 0x"?

---

**veox** (2018-05-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> I think that one has been suggested before

For ref: AFAIU it was [issue 139](https://github.com/ethereum/EIPs/issues/139).

---

**chfast** (2018-07-17):

Update: https://github.com/ethereum/EIPs/pull/1226

---

**karalabe** (2018-07-19):

The `0x3d` opcode slot is already taken by `RETURNDATASIZE` (and `0x3e` is taken by `RETURNDATACOPY`). Please bump the opcode number to `0x3f`.

---

**fulldecent** (2019-01-26):

Posting here for completeness:

---

Here is my issue with EIP-1052 (the version as of [80b8f80](https://github.com/ethereum/EIPs/commit/80b8f8071076537d99888064c63636a07b40b627)).

I believe this test case:

> “The EXTCODEHASH of an precompiled contract is either c5d246… or 0.”

is ambiguous and could lead to multiple, conflicting implementations. That of course would lead to a network split and cost billions of dollars.

The solution is to provide more explicit test cases, one that returns c5d246… and one that returns 0.

---

This issue may be resolved and it is also discussed here [EIP-1052 failed to go through the workflow · Issue #1699 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/1699#issuecomment-457867195) but I am cross posting here and sorry I should have posted here first then crossposted elsewhere.

---

**ajsutton** (2019-01-27):

This is covered by the ethereum reference tests for EXTCODEHASH, specifically https://github.com/ethereum/tests/blob/develop/src/GeneralStateTestsFiller/stExtCodeHash/extCodeHashDynamicArgumentFiller.json (and probably others) which checks both precompile 0x01 and 0x02 where 0x01 does not exist in state and 0x02 does.  Basically precompiles have no code and whether they are present or not is determined by whether they exist in the actual world state or not like any other contract.

---

**howardpen9** (2020-09-11):

Nice, interesting.

But why `EXTCODECOPY`  ( `0x3c` ) opcode, but this is expensive is mor expensive!

---

**CryptoKiddies** (2022-03-10):

Great feature for validating code integrity. Its usage does force redesigns for factory-spawned or standardized contracts when immutable vars are in use, given that their initialized values end up in the deployed bytecode.

