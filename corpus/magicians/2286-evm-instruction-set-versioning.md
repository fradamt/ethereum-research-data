---
source: magicians
topic_id: 2286
title: EVM instruction set versioning
author: androlo
date: "2018-12-25"
category: EIPs
tags: [evm, versioning]
url: https://ethereum-magicians.org/t/evm-instruction-set-versioning/2286
views: 2837
likes: 10
posts_count: 11
---

# EVM instruction set versioning

---

## eip:
title: EVM version instruction
author: Andreas Olofsson <@androlo>
discussions-to:
status: Draft
type: Standards Track
category: Core
created: -

**This is currently a bit of a pick-and-choose proposal, which is why it has not yet been submitted as a proper EIP.**

## Simple Summary

This document proposes that the ABI of contract code is extended to include an EVM (instruction set) target version number, or ID, that allows the EVM to pick the correct instruction set when executing contracts.

## Abstract

This document is a proposal to add support for multiple EVM instruction set versions, and for manually specifying the desired target in code. A version number would be added to the EVM instruction set, which would be updated for every change that would break (i.e. alter the behavior of) contracts that are already deployed. The old instruction set would still remain after a version update, making it possible to pick which one to use. Additionally, a new instruction would be added to reserve a certain opcode for safe ABI formatting and for making it possible to view the target version of a contract from code.

## Motivation

It is vital that the EVM can undergo changes without making previously deployed contracts break. New instructions and new functionality can sometimes be added without breaking old code, but sometimes that is not possible - like when opcodes has to be remapped or removed.

We are already dealing with these kinds of issues; for example, `CALLCODE` is still around despite having been replaced by `DELEGATECALL` - which was assigned its own new opcode - and the other call instructions still has the return position and size parameters in its parameter list even though they were made obsolete by the new returndata system. Ideally, one could think, the current `DELEGATECALL` instruction should instead have been re-mapped to `CALLCODE`, and the other call instructions would be changed to new versions that does not have the redundant parameters.

The changes proposed here would address all the issues above and any similar issues that may arise in the future.

## Specification

### Instruction

#### Name/Mnemonic

`TARGET`

#### Opcode

TBD

#### Parameters

`address` - the address of the target account.

#### Result

Pushes the target version ID of the account with address ‘`address`’ onto the stack.

### ABI update

Contract code (init and body sections) must be preceded by 2 bytes - the `TARGET` opcode followed by a 1 byte target ID.

### EVM version ID

Target IDs starts at 1 and is incremented by 1 when an update is made.

If an account is not a contract account the instruction could either return 0 or cause the EVM to revert (TBD).

#### Changes to CREATE

Contracts that are already deployed and therefore does not start with the `TARGET` opcode would be assigned a target ID of 1.

To ensure that future contracts conform to the new standard, contract creation has to be modified. During creation, the EVM must revert if:

- the contract initialization code does not have a target set.
- the contract runtime code does not have a target set.
- either of the target IDs are invalid.

## Rationale

The reason for adding version to the first byte of the code is to make it easy for the EVM to find and to use it. The EVM routine for getting and checking the target ID would be trivial.

A one-byte target ID should be plenty, given that most updates are backwards compatible and therefore they do not require a version change.

The ability to view the target of another contract may become very useful. Old contracts will inevitabely become less and less safe as the EVM evolves - particularly if proposals like [EIP 615](https://eips.ethereum.org/EIPS/eip-615) are implemented. This proposal would make it possible for contract writers to avoid calling contracts that are potentially less safe.

#### Some possible changes

The reason for not adding the target ID as a separate field is to avoid complicating the account data-structure, although doing that may actually be more practical. If that is the case then a lot of these suggestions could be scrapped.

Obviously, the big job here would be to change the EVM to allow multiple instruction sets to be chosen from. The purpose of the instruction is mainly to reserve a certain opcode for target version, which would make the starting sequence distinguishable from other code, i.e. it would always be possible to tell whether code is on the new ABI format or not. If the target version is instead stored in its own field, that would remove most of the motivation for this instruction.

In the above case, the ABI could instead be modified to have only the version number byte in front of the code when CREATE is called. The version number would then be stripped out by the EVM and added to the reserved field before the code is actually run. A drawback to this is that it would be more difficult to check that the input is well formed.

## Backwards Compatibility

Adding this instruction in accordance with the spec would not cause backwards compatibility issues.

## Test Cases

None.

## Implementation

For EVM designers to decide.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**boris** (2018-12-31):

This is interesting and might also be important for different networks that use the EVM. Makes me think of chainID https://chainid.network

---

**veox** (2019-03-17):

Possibly related discussion: [Immutables, invariants, and upgradability](https://ethereum-magicians.org/t/immutables-invariants-and-upgradability/2440/7?u=veox) (comments).

---

**jpitts** (2019-03-18):

I assume that, even though “instruction set” is used in the description, this EVM versioning scheme would advance with any forking EVM change e.g. gas cost changes in EIP-150 included in the v4 Tangerine Whistle protocol release.

In the context of my proposed set of [protocol versions](https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921), what are the points at which the EVM has advanced its “MAJOR” version (provided the EVM has its own schedule, but released with protocol upgrades)?

Also, is it even possible to have “MINOR” updates to the EVM specification? Perhaps this occurs when multiple clients fix the same bug?

Here is my take:

v1 EVM - v1 Protocol - Frontier

v2 EVM - v4 Protocol - Tangerine Whistle

v3 EVM - v5 Protocol - Spurious Dragon

v4 EVM - v6 Protocol - Byzantium

v5 EVM - v7 Protocol - St. Petersburg


      [gist.github.com](https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921)




####

##### ethereum-protocol-versions.md

```
# Ethereum Protocol - Series 0.x

| Version and Code Name | Block No. | Released | Incl EIPs | Specs | Impls |
|-----------------------|-----------|----------|-----------|-------|-------|
| v1 - Frontier | 1 | 07/30/2015 | | | [Geth v1.0.0](https://github.com/ethereum/go-ethereum/releases/tag/v1.0.0) |
| v1.1 - Frontier Thawing | 200000 | 09/07/2015 | | | [Geth v1.0.1.1](https://github.com/ethereum/go-ethereum/releases/tag/v1.0.1.1) |
| v2 - Homestead | 1150000 | 03/14/2016  | [EIP-2](https://eips.ethereum.org/EIPS/eip-2)
 [EIP-7](https://eips.ethereum.org/EIPS/eip-7)
 [EIP-8](https://eips.ethereum.org/EIPS/eip-8) | [HFM-606](https://eips.ethereum.org/EIPS/eip-606) | [Geth v1.3.4](https://github.com/ethereum/go-ethereum/releases/tag/v1.3.4) |
| v3-rc1 - DAO Wars | aborted | aborted |  |  | [Geth v1.4.8](https://github.com/ethereum/go-ethereum/releases/tag/v1.4.8) |
| v3 - DAO Fork | 1920000 | 07/20/2016 |  | [HFM-779](https://eips.ethereum.org/EIPS/eip-779) | [Geth v1.4.10](https://github.com/ethereum/go-ethereum/releases/tag/v1.4.10) |
| v4 - Tangerine Whistle | 2463000 | 10/18/2016 | [EIP-150](https://eips.ethereum.org/EIPS/eip-150) | [HFM-608](https://eips.ethereum.org/EIPS/eip-608) | [Geth v1.4.18](https://github.com/ethereum/go-ethereum/releases/tag/v1.4.18) |
```

This file has been truncated. [show original](https://gist.github.com/jpitts/4c541a4efa2f8872ce9acf63da5c4921)

---

**lrettig** (2019-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> In the context of my proposed set of protocol versions, what are the points at which the EVM has advanced its “MAJOR” version (provided the EVM has its own schedule, but released with protocol upgrades)?

I have a different take on this. All EVM upgrades thus far have been fully backwards-compatible, and without breaking changes (I think). So there has been no new major version. I’d argue that we’re still on 0.x and that Ewasm (or whatever gets rolled out with Eth2) would be a 1.x. Then again, EVM and Ewasm are different VMs and therefore maybe we should use orthogonal/unrelated numbering schemes for the different VMs.

Linking two related threads here from Ewasm:

- Behaviour on a combined EVM+ewasm chain
- Use invalid opcode as part of the eWASM magic

Note that in Ewasm-land we’ve discussed adding a contract or VM code to the account trie, rather than modifying contract bytecode (an account with no such field is interpreted as a legacy contract running “EVM0” or whatever version we’re on now). The advantage here is that it may be a little easier for the client to select a VM without needing to “peek” at the bytecode first, and it avoids issues (discussed in the first Ewasm thread I linked) in porting code across chains or adding new VMs in the future which may interpret opcodes differently. It also raises questions (also discussed in that thread) about how a contract targeting one VM creates contracts targeting another VM.

---

**lrettig** (2019-03-18):

Copying in some related links from another thread:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png)
    [EIP-615: Subroutines and Static Jumps for the EVM](https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm/2728/87) [EIPs](/c/eips/5)



> The links in above copy-paste (in order of appearance):
>
> Immutables, invariants, and upgradability
> EVM instruction set versioning
> https://github.com/ethereum/EIPs/pull/1712
> https://github.com/sorpaas/EIPs/issues/4
> https://github.com/ethereum/EIPs/issues/154
> https://github.com/ethereum/EIPs/pull/1707



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png)
    [EIP-615: Subroutines and Static Jumps for the EVM](https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm/2728/89) [EIPs](/c/eips/5)



> And https://github.com/ethereum/EIPs/issues/178.
> So yes, a number of proposals for EVM versioning have been made. None of them reached a proper EIP draft.
> I also believe this is prerequisite for static jumps.

---

**jpitts** (2019-03-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> All EVM upgrades thus far have been fully backwards-compatible, and without breaking changes (I think). So there has been no new major version.

That is a very good point!

The current EVM can be positioned as 0.x, and all changes are MINOR as backwards compatibility is maintained. Perhaps the proposed EIP-615 AKA “EVM 1.5” actually is not v1.5, but v0.6.

v0.1 EVM - v1 Protocol - Frontier

v0.2 EVM - v4 Protocol - Tangerine Whistle

v0.3 EVM - v5 Protocol - Spurious Dragon

v0.4 EVM - v6 Protocol - Byzantium

v0.5 EVM - v7 Protocol - St. Petersburg

v0.6 EVM - v8 Protocol - St. Gregory? ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)  (could include EIP-615)

The upcoming “Ethereum 1.x” changes required for mainnet sustainability perhaps would still keep the EVM in 0.x, as smart contracts are not backwards incompatible as much as they are not financially sustainable due to the proposed changes. But would the incorporation eWASM into the protocol even bring the EVM itself to 1.x?

What actually brings the EVM out of beta?

I would argue that as sidechains and even major blockchains are using the EVM w/ serious money flowing over it, and a sustainable funding model is reached for the project, it is time to hatch the EVM out of beta with fanfare.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> I’d argue that we’re still on 0.x and that Ewasm (or whatever gets rolled out with Eth2) would be a 1.x. Then again, EVM and Ewasm are different VMs and therefore maybe we should use orthogonal/unrelated numbering schemes for the different VMs.

I do think EVM should be on its own versioning scheme, allowing for it to continue  alongside eWASM which would have its own balancing act between the EVM and WASM specifications (if I am understanding it correctly).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Note that in Ewasm-land we’ve discussed adding a contract or VM code to the account trie, rather than modifying contract bytecode (an account with no such field is interpreted as a legacy contract running “EVM0” or whatever version we’re on now).

This tells me that proper versioning is even more critical so that client makers, devs, and dev tooling makers can start to be in sync about what will happen when the smart contract is executed.

---

**gcolvin** (2019-03-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> I do think EVM should be on its own versioning scheme, allowing for it to continue alongside eWASM which would have its own balancing act between the EVM and WASM specifications (if I am understanding it correctly).

That came up recently.  EIP-615 won’t start out as breaking change, but might become one, and I’m not wanting to solve the versioning problem in general before moving ahead.  [Discussion here](https://ethereum-magicians.org/t/eip-615-subroutines-and-static-jumps-for-the-evm/2728/91), including list of 7 or 8 active versioning proposals.

Wasm could be a completely separate VM, or could be integrated more or less tightly to the EVM,  (e.g. as literally the assembly language that the EVM compiles to).  But we’ll need an EIP for eWasm to discuss this in much detail.

---

**gcolvin** (2019-03-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> v0.6 EVM - v8 Protocol - St. Gregory?

No. Please no.

(Post must be least 20 characters, so type …)

---

**jpitts** (2019-03-20):

Don’t worry Greg, this network upgrade will be called Instanbul ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**shemnon** (2019-05-26):

So is this the best thread to discuss on-chain EVM versioning?

On the AllCoreDevs call #62 EVM versioning was put forth as a possible way to re-introduce EIP-1283, the one pulled from Constantinople, if I understand it correctly the version bit would apply to EVM semantics as well as EVM instructions.

One thing I haven’t seen discussed is the scope of the versioning.  If Contract A6 is under version 6 of the EVM and calls contract B5 that has no version information set, and hence defaults to v5, under what terms are the EVM executing B5’s methods?

If it is under the terms of A6 then the I think the EIP-1283 bug still exists, because a new exploit contract could be deployed under the new gas metering rules, which could call a vulnerable contract and the versioning rules would not protect that contract’s EVM environment.

One alternative is to have each contract executed under the terms it was deployed under.  This is more work for EVM implementors because they would have  to keep different EVM versions running in the same call stack.

One brutal solution would be to only allow contracts to call other contracts of the same EVM generation.  This would in essence fork the ecosystem on chain, and IMHO is a very bad solution.

