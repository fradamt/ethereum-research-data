---
source: magicians
topic_id: 8979
title: "EIP-5003, AUTH_USURP: Publishing code at an EOA address"
author: danfinlay
date: "2022-04-20"
category: EIPs > EIPs core
tags: [evm, opcodes, eoav2]
url: https://ethereum-magicians.org/t/eip-5003-auth-usurp-publishing-code-at-an-eoa-address/8979
views: 3518
likes: 13
posts_count: 7
---

# EIP-5003, AUTH_USURP: Publishing code at an EOA address

[EIP PR link](https://github.com/ethereum/EIPs/pull/5003)

Body below:

---

## eip: 5003
title: Replace Externally Owned Accounts with AUTHUSURP
description: Allow migrating away from ECDSA by deploying code in place of an externally owned account.
author: Dan Finlay (), Sam Wilson ()
discussions-to:
status: Draft
type: Standards Track
category: Core
created: 2022-03-26
requires: 3074, 3607

## Abstract

This EIP introduces a new opcode, `AUTHUSURP`, which deploys code at an EIP-3074 authorized address. For externally owned accounts (EOAs), together with EIP-3607, this effectively revokes the original signing key’s authority.

## Motivation

EOAs currently hold a significant amount of user-controlled value on Ethereum blockchains, but are limited by the protocol in a variety of critical ways. These accounts do not support rotating keys for security, batching to save gas, or sponsored transactions to reduce the need to hold ether yourself. There are countless other benefits that come from having a contract account or account abstraction, like choosing one’s own authentication algorithm, setting spending limits, enabling social recovery, allowing key rotation, arbitrarily and transitively delegating capabilities, and just about anything else we can imagine.

New users have access to these benefits using smart contract wallets, and new contracts can adopt recent standards to enable app-layer account abstraction (like EIP-4337), but these would neglect the vast majority of existing Ethereum users’ accounts. These users exist today, and they also need a path to achieving their security goals.

Those added benefits would mostly come along with EIP-3074 itself, but with one significant shortcoming: the original signing key has ultimate authority for the account. While an EOA could delegate its authority to some *additional* contract, the key itself would linger, continuing to provide an attack vector, and a constantly horrifying question lingering: have I been leaked? In other words, EIP-3074 can only grant authority to additional actors, but never revoke it.

Today’s EOAs have no option to rotate their keys. A leaked private key (either through phishing, or accidental access) cannot be revoked. A prudent user concerned about their key security might migrate to a new secret recovery phrase but at best this requires a transaction per asset (making it extremely expensive), and at worst, some powers (like hard-coded owners in a smart contract) might not be transferable at all.

We know that EOAs cannot provide ideal user experience or safety, and there is a desire in the community to change the norm to contract-based accounts, but if that transition is designed without regard for the vast majority of users today—for whom Ethereum has always meant EOAs—we will be continually struggling against the need to support both of these userbases. This EIP provides a path not to enshrine EOAs, but to provide a migration path off of them, once and for all.

This proposal combines well with, but is distinct from, EIP-3074, which provides opcodes that could enable any externally owned account (EOA) to delegate its signing authority to an arbitrary smart contract. It allows an EOA to authorize a contract account to act on its behalf *without forgoing its own powers*, while this EIP provides a final migration path off the EOA’s original signing key.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

### Conventions

- top - N - the Nth most recently pushed value on the EVM stack, where top - 0 is the most recent.
- invalid execution - execution that is invalid and must exit the current execution frame immediately, consuming all remaining gas (in the same way as a stack underflow or invalid jump).
- empty account - account where its balance is 0, its nonce is 0, and it has no code.

### AUTHUSURP (0xf8)

A new opcode `AUTHUSURP` shall be created at `0xf8`. It shall take two stack elements and return one stack element.

#### Input

| Stack | Value |
| --- | --- |
| top - 0 | offset |
| top - 1 | length |

#### Output

| Stack | Value |
| --- | --- |
| top - 0 | address |

#### Behavior

`AUTHUSURP` behaves identically to `CREATE` (`0xf0`), except as described below:

- If authorized (as defined in EIP-3074) is unset, execution is invalid.
- If authorized points to an empty account, then static_gas remains 32,000. Otherwise, static_gas shall be 7,000.
- AUTHUSURP does not check the nonce of the authorized account.
- The initcode runs at the address authorized.
- If the initcode returns no bytes, its execution frame must be reverted, and AUTHUSURP returns zero.
- After executing the initcode, but before the returned code is deployed, if the account’s code is non-empty, the initcode’s execution frame must be reverted, and AUTHUSURP returns zero.
- The code is deployed into the account with the address authorized.

## Rationale

The rationale fleshes out the specification by describing what motivated the design and why particular design decisions were made. It should describe alternate designs that were considered and related work, e.g. how the feature is supported in other languages.

## Backwards Compatibility

All EIPs that introduce backwards incompatibilities must include a section describing these incompatibilities and their severity. The EIP must explain how the author proposes to deal with these incompatibilities. EIP submissions without a sufficient backwards compatibility treatise may be rejected outright.

## Test Cases

Test cases for an implementation are mandatory for EIPs that are affecting consensus changes.  If the test suite is too large to reasonably be included inline, then consider adding it as one or more files in `../assets/eip-####/`.

## Reference Implementation

An optional section that contains a reference/example implementation that people can use to assist in understanding or implementing this specification.  If the implementation is too large to reasonably be included inline, then consider adding it as one or more files in `../assets/eip-####/`.

## Security Considerations

All EIPs must contain a section that discusses the security implications/considerations relevant to the proposed change. Include information that might be important for security discussions, surfaces risks and can be used throughout the life cycle of the proposal. E.g. include security-relevant design decisions, concerns, important discussions, implementation-specific guidance and pitfalls, an outline of threats and risks and how they are being addressed. EIP submissions missing the “Security Considerations” section will be rejected. An EIP cannot proceed to status “Final” without a Security Considerations discussion deemed sufficient by the reviewers.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**rmeissner** (2022-06-27):

Did you think about if this EIP should touch the ecrecover opcode to check if a specific address contains code.

Not saying that this is something that should be done. I would just be interested in if this was evaluated to get around some of the side effects of this EIP

---

**PaulRBerg** (2023-10-13):

I would smile upon this EIP being implemented. It would solve the problem of EOA liability.

Imagine you have a contract that gives some admin permission to an EOA, permission which cannot be revoked at the contract level (the developer forgot to implement this). Now, further imagine that the EOA owner wishes to relinquish their admin powers due to e.g. a desire to decentralize the contract, or regulatory concerns.

There’s currently no way for the EOA owner to do this. More generally, “proof of lack of knowledge” is impossible. But EIP-5003 would enable EOAs to effectively rage-quit their account by publishing a dummy contract that does nothing.

---

**danfinlay** (2023-10-26):

I’ve heard this included in proposals similar to this one. My personal suspicion is that while modifying ECRecover could preserve compatibility with some contracts that were not designed for an AA world, it could introduce some new issues (for example, in 4337, a Paymaster isn’t allowed to call an external contract, but it can ecrecover, and that rule would complicate this guarantee).

By not providing that change, I think we would establish a strong incentive for contracts to use `msg.sender` as an authorization system rather than custom internal `ecrecover` type logic.

---

**wjmelements** (2024-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> while this EIP provides a final migration path off the EOA’s original signing key.

This doesn’t seem to be in the spec. I don’t think it is explicitly defined that `ORIGIN` cannot have code.

Also, does 3074 `AUTH` require that the signing account does not have code?

---

**wjmelements** (2024-04-29):

> This means that, for example, the private key will always have access to the permit function on token contracts. This can—and should—be mitigated by modifying the ecrecover pre-compiled contract.

I disagree. `ecrecover` can have valid uses besides `permit` even after usurp. Contracts using ecrecover can check `EXTCODESIZE` if it applies to their use-case. Instead, the usurped account should divest itself of all ERC-2612 tokens if `ecrecover` is deemed a risk.

---

**matt** (2024-04-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> This doesn’t seem to be in the spec. I don’t think it is explicitly defined that ORIGIN cannot have code.

Yes, under “behavior” you can see that `AUTH` must throw if the account code size is not zero.

