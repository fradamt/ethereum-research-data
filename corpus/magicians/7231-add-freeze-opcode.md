---
source: magicians
topic_id: 7231
title: Add FREEZE opcode
author: rmeissner
date: "2021-10-08"
category: EIPs
tags: [opcodes]
url: https://ethereum-magicians.org/t/add-freeze-opcode/7231
views: 1504
likes: 1
posts_count: 9
---

# Add FREEZE opcode

I would like to propose to add an opcode to freeze the storage of the current contract in the current call stack. This would be useful to ensure that no state changes can occur after a certain opcode. This could potentially even be validated with static analysis which would be helpful for [EIP-3074: AUTH and AUTHCALL opcodes](https://ethereum-magicians.org/t/eip-3074-auth-and-authcall-opcodes/4880) and [ERC 4337: Account Abstraction via Entry Point Contract specification - #10 by vbuterin](https://ethereum-magicians.org/t/erc-4337-account-abstraction-via-entry-point-contract-specification/7160/10) especially in combination with [EIP-2937: SET_INDESTRUCTIBLE opcode - #12 by nikolai](https://ethereum-magicians.org/t/eip-2937-set-indestructible-opcode/4571/12).

The mentioned EIPs limit the use of delegate calls as they can introduce unexpected state changes. By freezing the contract storage it would be possible to eliminate this uncertainty. The scope of the freeze should only be the contract that is calling the opcode.

Is anyone else interested in such an opcode or does anyone see anything that would speak against such an opcode?

## Replies

**rmeissner** (2021-10-08):

Other use cases could be wallet contracts, such as DSProxy, InstaDapp or the Gnosis Safe, which make use of delegatecalls to allow complex interactions with other cobtracts. These interactions normally don’t require state changes on the contracts that performs the delegatecall. Preventing state changes would make these contracts significantly more secure.

It could also be useful for reentrancy guards. The commonly used approach that makes use of storage can currently not securely be used in conjunction with delegatecalls.

---

**poma** (2021-10-10):

If the only usecase is for delegatecall, maybe we should instead do something like `StaticDelegateCall` opcode (similar to `CALL`/`STATICCALL` logic).

Note that this currently can be emulated (kind of) by doing a `staticcall` to a special contract method that does the `delegatecall`

---

**rmeissner** (2021-10-11):

> do something like StaticDelegateCall opcode

This is fundamentally different to the FREEZE logic as it would prevent all stage changes, not only for the calling contract.

Having a separate opcode to freeze storage of a specific contract is more flexible and the use with delegatecall is just the most obvious one. I outline this use case before in a different post [Add opcode to access storage trie root hash for account](https://ethereum-magicians.org/t/add-opcode-to-access-storage-trie-root-hash-for-account/6142#verification-1)

---

**poma** (2021-10-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> only for the calling contract.

In that case this opcode is dangerous, as it might introduce a false sense of safety. If any other contact trusts the current one, bad things can happen. For example if current contract owns some ERC20 tokens, a delegatecall will be able to transfer them even with FREEZE active.

---

**rmeissner** (2021-10-11):

> a delegatecall will be able to transfer them even with FREEZE active.

I see your point, but this would be possible even with a call (unless you fully freeze all state).

I think what I am rather looking for is a delegate call without the state access, something like an impersonate call. But I would think that this is even more dangerous.

In general these options should allow you to scope the risk. I don’t think any user would actually look for the opcode inside a contract. Currently delegatecalls are a all or nothing feature. If they could be better tweeked they could be more securely used in different contexts, which should allow to also minimize the code stored on-chain.

---

**nikolai** (2021-10-12):

Relevant: [Reentry is impossible to prevent when delegate calling · Issue #3 · nmushegian/wand · GitHub](https://github.com/nmushegian/wand/issues/3)

Throwing my support behind this, between this an SET_INDESTRUCTIBLE we can really level up the EVM. Hard to justify not having this *given that* we already have STATICCALL

---

**rmeissner** (2021-10-28):

I will be working on a reference implementation for this, to collect more data and get more people onboard.

---

**dror** (2021-10-30):

There are different attributes for “freeze”, each used in different cases:

- recurse current contract, next-to-call contract (depth=1), any depth
- block storage change
- block balance change
- logs
- selfdestruct

So my proposal is make FREEZE have “attributes” parameter, which define what will be frozen.

- The current STATICCALL is thus a special case of freeze(depth=1, storage, balance,logs) followed by “call”
- The proposed “SET_INDESTRUCTIBLE” is thus freeze(selfdestruct, depth=0)

All “undefined”  bits are required to be zero, so that future  EIP can define more attributes to freeze.

