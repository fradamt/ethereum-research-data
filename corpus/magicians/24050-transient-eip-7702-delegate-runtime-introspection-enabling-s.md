---
source: magicians
topic_id: 24050
title: Transient EIP‑7702 Delegate Runtime Introspection – Enabling Safer, Smarter Wallet Innovation
author: 0xth0mas
date: "2025-05-05"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/transient-eip-7702-delegate-runtime-introspection-enabling-safer-smarter-wallet-innovation/24050
views: 384
likes: 21
posts_count: 20
---

# Transient EIP‑7702 Delegate Runtime Introspection – Enabling Safer, Smarter Wallet Innovation

**![:star2:](https://ethereum-magicians.org/images/emoji/twitter/star2.png?v=12) [ERC‑XXXX] Transient EIP‑7702 Delegate Runtime Introspection – Enabling Safer, Smarter Wallet Innovation**

With EIP‑7702, we’re stepping into an exciting new chapter for Ethereum wallets. By allowing EOAs to temporarily attach contract logic per-transaction, 7702 opens the door to a new class of user experiences—flexible, programmable, and gas-efficient—without giving up EOA simplicity.

This is more than an upgrade; it’s a foundational shift in what a wallet can be.

But to fully unlock the promise of this model—modular wallets, delegate-driven apps, context-aware smart contracts—we need the ability to understand and verify what’s happening inside a delegated call.

Introducing: `callContext7702()`

This proposal defines a minimal, low-gas interface that gives any contract clear visibility into a wallet’s delegate call state.

---

**![:wrench:](https://ethereum-magicians.org/images/emoji/twitter/wrench.png?v=12) The Core Interface**

At the heart of this ERC is a single view function:

```solidity
function callContext7702() external view returns (CallContext7702 memory context);

struct CallContext7702 {
    bool    isDelegatedCodeActive;
    uint256 callDepth;
    address invoker;
    uint256 opType;
}
```

This lets smart contracts or tools answer questions like:

- Am I talking to a delegate, or a plain EOA?
- Who invoked the delegate code if it is active?
- Are we inside a recursive delegate context?
- What type of operation is being performed?
This unlocks composability and security at the same time, without relying on heuristics or external assumptions.

---

**![:brain:](https://ethereum-magicians.org/images/emoji/twitter/brain.png?v=12) Semantics via opType**

One useful aspect of this approach is the ability to include a semantic opType, which allows protocols to interpret the kind of delegate operation being performed and apply relevant policies or safeguards.

```solidity
uint8 constant OP_NONE                   = 0;
uint8 constant OP_TOKEN_TRANSFER_SINGLE  = 1;
uint8 constant OP_TOKEN_TRANSFER_BATCH   = 2;
uint8 constant OP_EXEC_SINGLE            = 3;
uint8 constant OP_EXEC_BATCH             = 4;
uint8 constant OP_UNKNOWN                = 5;
```

This paves the way for use cases like:

- Approving only certain op types via governance oracles
- Attaching intent metadata to a wallet transaction
- Implementing composable, multi-step workflows without breaking protocol invariants

---

**![:hammer_and_wrench:](https://ethereum-magicians.org/images/emoji/twitter/hammer_and_wrench.png?v=12) How It Works (Lightweight + Safe)**

We designed the system to be both robust and extremely simple to implement.

The reference implementation has a single modifier to provide delegates with introspection context:

```solidity
modifier delegateCodeEntered(uint8 opType) {
    uint256 contextToRestore = _delegateCodeEnteredBefore(opType);
    _;
    _delegateCodeEnteredAfter(contextToRestore);
}
```

This pattern ensures that introspection is:

- Stateless
- Nesting-aware
- Invisible to the wallet’s long-term state

---

**![:mag:](https://ethereum-magicians.org/images/emoji/twitter/mag.png?v=12) Safe Introspection From Consumers**

For contracts or apps that want to inspect a wallet’s delegate status safely the reference implementation contains helper functions to inspect an address for its current EIP-7702 state.

The example below uses the helper functions to check if a wallet has a delegate attached, if the attached delegate is allowed to interact with the contract, and the operation type if the call is being made through the delegate implementation.

```solidity
(bool isDelegate, address delegate) = _check7702(wallet);
if (isDelegate) {
    require(_allowedDelegates[delegate], “Unauthorized delegate implementation”);
    (bool error, CallContext7702 memory ctx) = _safeCallContext7702(wallet);
    require(!error && (!ctx. isDelegatedCodeActive
 || ctx.opType == OP_EXEC_SINGLE), "Unauthorized delegate op");
}
```

---

**![:earth_africa:](https://ethereum-magicians.org/images/emoji/twitter/earth_africa.png?v=12) Why This Matters**

By making introspection simple, reliable, and standardized, this ERC enables:

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Secure modular wallets — where functionality can be dynamically added without sacrificing protocol assurances

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Delegate-aware DeFi — allowing lending, swaps, or governance to enforce op-type constraints

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Trust-minimized integrations — where protocols can validate execution context, not just permissions

![:white_check_mark:](https://ethereum-magicians.org/images/emoji/twitter/white_check_mark.png?v=12) Composable protocols — that build on each other with full visibility into wallet behavior

We’re not just plugging a hole—we’re creating an interface that expands what’s possible across the wallet stack.

---

**![:lock:](https://ethereum-magicians.org/images/emoji/twitter/lock.png?v=12) Designed for Safety**

- Uses transient storage to avoid collision or contamination
- Nested calls are tracked via callDepth, providing reentrancy awareness
- Introspection is opt-in and observable, but not enforceable unless the delegate is trusted—you control your threat model

---

**![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=12) Let’s Build the Future of Wallets**

EIP‑7702 gives us the freedom to move beyond the binary choice of EOA vs contract account. But with that flexibility, we need the right guardrails and observability.

This ERC is our proposal for that layer. It’s minimal. It’s modular. And it’s designed to empower developers, protocols, and wallets to innovate safely.

![:blue_book:](https://ethereum-magicians.org/images/emoji/twitter/blue_book.png?v=12) Proposed ERC available [here](https://gist.github.com/nathanglb/0cf1c8dd60f3fcb5d6f39633aeae6736). We’d love your feedback, edge cases, and implementation ideas.

## Replies

**mitche50** (2025-05-05):

Introspection is paramount for safety in a trustless environment. Any addition to this I’m in favor for ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**PopPunkOnChain** (2025-05-05):

Easy introspection for apps/protocols. This seems like a no brainer to me.

---

**WOK** (2025-05-05):

Seem like a well thought out approach. Very useful IMO.

---

**matt** (2025-05-05):

I don’t fully understand this proposal. Is this something the delegated code should implement so the user can have modules for their wallet? Is it even possible to return the call depth?

---

**0xth0mas** (2025-05-05):

Yes, this is a proposed standard for delegate code to inform contracts they are interacting with about what is taking place. Contracts would need to be able to trust the delegate is being honest so a protocol implementing such a mechanism would need to whitelist delegate implementations that are trustworthy.

The call depth in this proposal is call depth within the delegate since a delegate could reenter itself.

---

**storm33** (2025-05-05):

Surprised this wasn’t included out of the box. Must have!

---

**dror** (2025-05-06):

I really don’t understand the purpose of this ERC

on-chain, an EIP-7702 account is just like any other SCA (smart contract account).

An SCA doesn’t have any standard API to expose its internals.

This of a DEX or Token call from a Safe:

The fact the safe needs a multisig doesn’t change the way the token behaves when the safe  performs a “transfer”.

A 7702 account is just the same. The target contract (token, DEX, etc) shouldn’t make any assumptions - only use the account address (`msg.sender `)

SCA - whether it is a Safe, an ERC-4337 account, an EIP-7702 differ in their gas payments, security and upgrade mechanism - nothing of this is exposed to the target contract they call, or should matter.

---

**0xth0mas** (2025-05-06):

It does matter because a normal SCA has deterministic behavior based on its implementation. An EOA with a 7702 delegate attached may be interacting with an another account through a direct call OR by a call through their attached delegate, which makes a difference in certain applications. Having an introspection standard makes this information available to any protocol that it matters to.

---

**mitche50** (2025-05-06):

An SCA is immutable, it has deterministic outcomes and code paths.

7702 has delegates that can change, meaning the same address can have completely different functionality based on what delegate is attached or what action they’re taking.

In a trustless environment, this is a necessity to build resilient protocols.

---

**WOK** (2025-05-06):

Certainly we should not just make assumptions about how 7702 delegates operate, but that is not what this proposal is suggesting. In a whitelisted environment, the interface give protocol developers useful context on the delegate. The need for whitelists is noted in the security considerations section of the draft ERC.

---

**dror** (2025-05-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mitche50/48/10359_2.png) mitche50:

> An SCA is immutable, it has deterministic outcomes and code paths.
>
>
> 7702 has delegates that can change,

An SCA in most cases, is a proxy contract. its behavior thus depend on the current account state. You can’t expect SCAs to provide on-chain the information which implementation they currently use (and with modular account it is even far more complex)

Likewise, an EIP-7702 account depends on the current account state to define its current implementation.

I can see no difference - in either case, you can’t assume the behavior to stay intact, and the account owner can modify it at will.

The difference with 7702, is that you assumed you know its behevior (as an EOA) and that was changed - but you can’t assume you know to what it changed.

e.g. you can’t even assume that a given delegate will give you consistent behaviour - since a user might install an ERC-1967 proxy account as a delegate: the delegate code is now fixed, but the actual implementation can be modified, even within a single transaction.

Giving an API to return the current delegate gives an application the impression it knows how the account behaves, or on what change the account’s behevior will change - which is wrong.

---

**0xth0mas** (2025-05-07):

You absolutely can determine the behavior of a SCA by requiring the SCA to have a certain codehash that does not allow for SCA user upgrades or requiring it to have been deployed through a certain account factory.

The key difference between non-7702 SCAs and 7702 SCAs is that a protocol that needs awareness of execution context cannot currently determine if the call is an internal call from the delegate or if it’s the outermost call of a transaction from the EOA.

This ERC specifically calls out that a protocol would need to have trusted delegate implementations to know that the introspection data is accurate.

---

**nathanglb** (2025-05-07):

https://www.certik.com/resources/blog/37VGpYOcYgHPbNh534k46X-pectras-eip-7702-redefining-trust-assumptions-of-externally-owned-accounts

EIP-7702 breaks some trust assumptions held by some pre-existing smart contracts.  Focusing on one specific pattern where tx.origin is compared with msg.sender to know if a smart contract with code is in the loop when calling a contract:

" Crucially, this means an EOA, identified by its address, can now execute complex smart contract logic as itself (**msg.sender** will be the EOA’s address), even when called deeper within a transaction’s call stack, not just at the top level.

This change breaks a fundamental invariant that many developers, consciously or unconsciously, rely upon: **tx.origin == msg.sender** is no longer a guarantee that the current execution context is the first frame initiated directly by an EOA without any intermediate contract calls within the same transaction."

With 7702 delegate introspection, a contract seeking to implement this “No Smart Contracts” access control can first determine if a delegate is attached or not.  If a delegate is attached, it can then check the delegate implementation address against a whitelist of known/trusted 7702 delegate implementations that implement the runtime introspection specification.  It can then query the 7702 delegate runtime state to make an informed decision to allow the call if the delegate’s code is not active, or possibly if the call depth is 1 and the execution mode is EXEC_SINGLE.

---

**nathanglb** (2025-05-07):

You can whitelist delegate implementations that you trust to interact with your protocols, and block unknown untrusted delegates.  Obviously you can’t trust a 1967 style proxy delegate implementation, so it would just get blocked.

Lets examine the implications of a 1967 delegate proxy though.  If the user can be phished or otherwise tricked into signing an upgrade to malicious code, the user can get drained very easily.  Upgradeable 7702 delegates are extremely risky for users.

---

**rookmate** (2025-05-26):

Adding runtime introspection via `callContext7702()` feels like a smart step toward safer wallet programmability. Curious to see how protocols will start using `opType` to enforce operation-specific behaviors!

---

**hellohanchen** (2025-06-23):

Wouldn’t a malicious EIP-7702 account just return fake data through `callContext7702()`?

---

**0xth0mas** (2025-06-23):

A malicious 7702 implementation certainly could but we can already inspect what the implementation address is, the point of this ERC is obtaining valuable execution data from accounts that have a trusted delegate attached.

This example checks if there is a delegate attached, if the attached delegate is allowed, if the account is interacting directly or through the delegate and if through the delegate what kind of operation it is.

```auto
(bool isDelegate, address delegate) = _check7702(wallet);
if (isDelegate) {
    require(_allowedDelegates[delegate], “Unauthorized delegate implementation”);
    (bool error, CallContext7702 memory ctx) = _safeCallContext7702(wallet);
    require(!error && (!ctx.isDelegatedCodeActive
 || ctx.opType == OP_EXEC_SINGLE), "Unauthorized delegate op");
}
```

---

**hellohanchen** (2025-06-23):

Even if the account is not malicious, such ABI interface can introduce compatibility issue.

My personal preference is just leverage off-chain validation. If an EOA is delegated to a well-known SCA, then its behavior is totally predictable.

For EIP-7702, it is kinda important that each delegated SCA is either

- publicly auditable OR
- trusted by the wallet/dapp (like an allowlist)

---

**0xth0mas** (2025-06-23):

EOAs can change their delegate at the start of a transaction that is executed after it is validated offchain.

I agree that the delegated SCA should be trusted through allowlist. You have to take that enforcement onchain in many cases as well and unlike traditional SCAs - you have two distinct execution paths with 7702. `msg.sender` could be from the EOA making a direct call to your contract or it could be a call from the EOA’s attached delegate.

