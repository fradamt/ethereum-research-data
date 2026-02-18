---
source: magicians
topic_id: 6538
title: We should be moving beyond EOAs, not enshrining them even further (EIP 3074-related)
author: vbuterin
date: "2021-06-24"
category: EIPs
tags: [account-abstraction, signatures, eip-3074]
url: https://ethereum-magicians.org/t/we-should-be-moving-beyond-eoas-not-enshrining-them-even-further-eip-3074-related/6538
views: 4935
likes: 8
posts_count: 8
---

# We should be moving beyond EOAs, not enshrining them even further (EIP 3074-related)

A long term goal in Ethereum is **account abstraction (AA)**: making it so that users can use smart contract wallets to store their funds with the same convenience as EOAs, so that we no longer need externally owned accounts (EOAs). Smart contract wallets have the following benefits:

1. They can encode more complex access policies (eg. multisig, social recovery) that provide users increased security
2. They provide a natural upgrade path to other signature schemes that may have better properties (eg. Schnorr or BLS for much better threshold-sig-friendliness)
3. They provide a natural upgrade path to quantum resistance: once AA is implemented, full quantum resistance would not require any execution-layer EVM changes, instead, users could just upgrade their wallets to quantum-safe alternatives on their own
4. They allow user accounts to perform many operations in one transaction atomically, increasing safety and convenience and reducing gas costs

[EIP 3074](https://eips.ethereum.org/EIPS/eip-3074) accomplishes **[4]**, but it does NOT accomplish **[1, 2, 3]**. Hence, **EIP 3074 does not accomplish account abstraction (though as a short-term fix to [4], it or [something like it](https://ethereum-magicians.org/t/a-case-for-a-simpler-alternative-to-eip-3074/6493) can still be quite valuable)**. Currently, my favorite proposal for AA involves doing it outside the consensus layer [via alternate mempools](https://notes.ethereum.org/@vbuterin/alt_abstraction), to reduce load on consensus client developers who already need to work hard on testing, the merge, statelessness, optimization, etc, though we could decide on other approaches in the future as well. Nevertheless, **if something like EIP 3074 is rolled out, it would be nice if it was forward-compatible with future AA goals.**

## Post-AA cleanup of EOAs

**If AA is rolled out, eventually we would want to remove EOAs as a category, to reduce client complexity**. This can be done by making a hard fork that edits all existing and new EOAs in-place, replacing them with smart contract wallets that have the same functionality (but also an upgrade feature, so users can upgrade their accounts to a different scheme while keeping the same address).

Currently, there are no obstacles to doing this; the only issue is that there would need to be an irregular precompile that can create EOA-based wallets at addresses derived by hashing their public key. **But EIP 3074’s `AUTH` + `AUTHCALL` mechanism increases this complexity.**

`AUTH` + `AUTHCALL` is an opcode that initiates a call from another address. Hence, in a post-EOA world, it could conceivably be replaced with a call to the wallet contract that asks the wallet contract to make the desired operation. However, there is a problem: the authorization is disconnected from the call itself. Hence, the smart contract wallet would have to have additional functionality, a “authorize deputy” function that would allow a specific address to call it without a signature and have those calls immediately forwarded. `AUTH` would then become a call that calls this authorize-deputy mechanic, though even this doesn’t replicate the exact functionality because `AUTH` as specified is call-scoped, and any in-EVM storage that could store the deputy is persistent.

**All in all, a post-EIP-3074 post-AA world seems like it would carry a large amount of technical debt.**

## Ideas to improve this

1. Make AUTH and AUTHCALL precompiles instead of opcodes. This way, they could later be replaced with pieces of code, avoiding EVM opcode technical debt.
2. Implement Yoav’s alternative EIP 3074, which avoids the AUTH mechanism and makes a series of calls from the EOA directly. This simplifies the logic, as such an AUTHORIZED_MULTI_CALL EIP could in a post-AA world just be replaced with a series of calls to the wallet contract.
3. Give the AUTH and AUTHCALL opcodes/precompiles a pre-determined fixed lifetime (eg. 2 years), clearly signaling to wallet developers that these are temporary measures and at some point applications will need to switch over to a different system.

## Replies

**yoavw** (2021-06-24):

That’s a great frame for thinking about the problem.  Whatever we do, should be a step towards native AA.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> This can be done by making a hard fork that edits all existing and new EOAs in-place, replacing them with smart contract wallets that have the same functionality (but also an upgrade feature, so users can upgrade their accounts to a different scheme while keeping the same address).

This is exactly what Optimism does with [OVM_ProxyEOA](https://github.com/ethereum-optimism/optimism/blob/develop/packages/contracts/contracts/optimistic-ethereum/OVM/predeploys/OVM_ProxyEOA.sol) which currently delegates to [OVM_ECDSAContractAccount](https://github.com/ethereum-optimism/optimism/blob/develop/packages/contracts/contracts/optimistic-ethereum/OVM/predeploys/OVM_ECDSAContractAccount.sol) but supports `upgrade(address _implementation)`.  OVM creates these proxies [on demand](https://github.com/ethereum-optimism/optimism/blob/e6e85a6220de0c4e1d28749bc4b1d27d4dd7e4c1/packages/contracts/contracts/optimistic-ethereum/OVM/predeploys/OVM_SequencerEntrypoint.sol#L57) when the first transaction is made by EOA.  We could use a variation of that.

---

**matt** (2021-06-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> EIP 3074 accomplishes [4], but it does NOT accomplish [1, 2, 3]

I think EIP-3074 actually does accomplish **1**. To have a multisig, you could write an invoker that allows you to submit an artificial signature (hand picked r, s, v values), the members of the multisig, and the required threshold. The invoker would then not allow calls that use that artificial signature unless it is able to validate a multi-signature from the listed members.

Social recovery works similarly, except it doesn’t even need to be registered on chain. A user could sign a EIP-3074 authorization over `N` addresses and a threshold. The signature could be given to each member for safe keeping. If the user loses their private key, they could request that the members sign a EIP-3074 authorization to give control of the EOA to a new account the original owner controls. The multi-sig would be assembled and submitted on-chain with the original EIP-3074 authorization. The invoker could verify the threshold was met and allow the action to be executed.

The drawback to EIP-3074 access control policies is that you can’t revoke control of an EOA address from the private key. It can always circumvent the invoker.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> This can be done by making a hard fork that edits all existing and new EOAs in-place, replacing them with smart contract wallets that have the same functionality (but also an upgrade feature, so users can upgrade their accounts to a different scheme while keeping the same address).
>
>
> Currently, there are no obstacles to doing this; the only issue is that there would need to be an irregular precompile that can create EOA-based wallets at addresses derived by hashing their public key. But EIP 3074’s AUTH + AUTHCALL mechanism increases this complexity.

There are two approaches to resolving these obstacles. The first involves a modification of `AUTH` at the time of the AA fork and an additional `AUTH2` opcode. The second involves only a modification of `AUTH` in the current proposal.

#### Modifying AUTH during the AA fork

If we leave `AUTH` as it is now, we can in the future modify its behavior during the AA fork. The goal would be to disable secp256k1 ECDSA signatures for EOA smart contract wallets that have been upgraded. To do this, `AUTH` accepts the same stack operands and would continue to recover the signer of the EIP-3074 authorization. Before setting the `authorized` context variable to the recovered address, `AUTH` would call out to the recovered address using a standardized call interface to determine if contract allows authorizations via secp256k1 ECDSA signatures. If it does, it returns `true`. If it doesn’t, `false`. `AUTH` verifies the call returns `true` and then sets `authorized` to the recovered address. Otherwise, it fails.

To allow new cryptographic schemes to use EIP-3074 invokers, a new opcode `AUTH2` would have to be introduced. Instead of performing any signature recovery (it doesn’t know what scheme was used), it just accepts the `commit`, the signature payload, and the authorizing address. `AUTH2` would then call into the provided address to allow that contract to determine if the provided signature is valid. If the call returns `true`, `AUTH2` would set the authorizing address as `authorized`.

#### Modifying AUTH now

The above proposal would require invokers to be redeployed to support the `AUTH2` opcode. We could front run this by already defining `AUTH` to be the same as `AUTH2` was defined above. This would cause EIP-3074 transaction flows to be more expensive today, but would allow us to avoid redeploying invokers in the future. To simplify things further until the AA fork, we could assume that `AUTH` recovers the signer as normal and ensures it’s equal to address passed to it. After the AA fork, it could call provided address to perform the recovery and validation.

(Thanks [@SamWilsn](/u/samwilsn) for helping come up with these)

---

**vbuterin** (2021-06-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> To have a multisig, you could write an invoker that allows you to submit an artificial signature (hand picked r, s, v values), the members of the multisig, and the required threshold.

But then that EOA would still have a single key controlling it, no?

Or are you proposing one of those single-signature EOAs where the address is derived from a random signature of a message authorizing an invoker, so no one knows the private key? If so, then sure, though it is a fairly hacky way of achieving the goal…

---

**SamWilsn** (2021-06-25):

An idea I’ve been formulating slowly is that the `AUTH` vs. `AUTHCALL` split is actually where the strength of 3074 lies.

We could have any number of `AUTH`-like methods that all work with the `AUTHCALL` opcode. We’ve seen `AUTH` with the traditional ECDSA signature, and now `AUTH2` with the more flexible signature-in-memory approach, but there’s also [IMPERSONATECALL](https://eips.ethereum.org/EIPS/eip-2997) which could be implemented as another `AUTH`-style instruction, but the authorize would be much cheaper than an ecrecover.

Synthetic EOAs are a pretty hacky tool, but when the alternative is a `CREATE2` shell contract…

---

**vbuterin** (2021-06-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> To have a multisig, you could write an invoker that allows you to submit an artificial signature (hand picked r, s, v values), the members of the multisig, and the required threshold.

Actually, I forgot to mention an even bigger issue with this scheme: it still requires some contract other than your multisig to hold ETH, so you’d need a forwarding mechanism and something that manages the complexity of ETH in two different accounts. So as a multisig wallet, it’s not really better than existing multisig smart contracts.

---

**matt** (2021-07-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Actually, I forgot to mention an even bigger issue with this scheme: it still requires some contract other than your multisig to hold ETH, so you’d need a forwarding mechanism and something that manages the complexity of ETH in two different accounts. So as a multisig wallet, it’s not really better than existing multisig smart contracts.

This is true in the current proposal, but I think I think there is a pretty clear path to allowing balance spends from EOAs during execution – if we make same some of the assumptions as AA, just charge enough to cover potentially invalided txs. In that case, it should be equivalent to smart contract multisigs today and when we have AA it will be able to also pay for its own gas. It’s definitely not a major selling point to 3074 though ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I also tried to flesh out this vision for an EOA migration to smart contract wallets: [Validation Focused Smart Contract Wallets](https://ethereum-magicians.org/t/validation-focused-smart-contract-wallets/6603)

---

**eawosika** (2024-12-04):

https://research.2077.xyz/charting-ethereums-account-abstraction-roadmap-eip-3074-eip-5806-eip-7702

A deep dive on account abstraction-related proposals that also includes a section on EIP-3074. Provides important context re: the difficulty of gaining broad acceptance for EIP-3074 and the subsequent adoption of EIP-7702.

