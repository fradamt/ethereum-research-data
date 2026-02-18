---
source: magicians
topic_id: 16664
title: "RIP-7560: Native Account Abstraction"
author: alex-forshtat-tbk
date: "2023-11-16"
category: RIPs
tags: [account-abstraction, eip, rip]
url: https://ethereum-magicians.org/t/rip-7560-native-account-abstraction/16664
views: 15729
likes: 42
posts_count: 36
---

# RIP-7560: Native Account Abstraction

An account abstraction proposal that introduces consensus-layer protocol changes, instead of relying on higher-layer infrastructure.

Combining the EIP-2938 and ERC-4337 into a comprehensive Native Account Abstraction proposal.

We propose splitting the Ethereum transaction scope into multiple steps: validations, execution,

and post-transaction logic.

Transaction validity is determined by the result of the validation steps of a transaction.

https://github.com/ethereum/RIPs/pull/3

## Replies

**cejay** (2023-11-16):

Wow! That’s awesome!

and what does ‘EIP-9999’ refer to in the markdown file?

---

**pantaovay** (2023-11-16):

This is really nice, stays compatible with 4337, optimizes Gas, and solves the problem of Bundler being private now, which is very significant for account abstraction adoption!

---

**ankurdubey521** (2023-11-17):

Why is unused gas a concern specifically for AA transactions and not regular EOA transactions?

---

**Ivshti** (2023-11-17):

Because of the separate validation and execution stages for AA transactions, it’s harder for the block builders to account for an unused gas discrepancy.

It’s described here https://github.com/ethereum/RIPs/blob/e3bead34f1bcf1aa37fd51923ad99a77b801775c/RIPS/rip-7560.md#unused-gas-penalty-charge

---

**Ivshti** (2023-11-17):

Generally this RIP is amazing but the elephant in the room is the upcoming/placeholder EIP-9999, would be really fantastic to see what it refers to.

Otherwise great job!

My main comment would be about the version parameter in the validation function. I think it makes way more sense for upgrading to simply change the signature of the function either by changing the parameters or append a _v* to the function name. The rationale for this is that it allows wallet implementation with fallback handlers and modules to update in an easier way.

At the risk of sounding like an optimizooor, it’s unfair to expect wallet implementations to implement full delegatecall upgradability cause it adds one mandatory SLOAD to each transaction.

---

**makemake** (2023-11-17):

IMO, this adds lots of complexity to the core protocol for something that can be done outside of it.

There’s the issue of multiple competing AA standards, with none having widespread use. If AA ends up being enshrined, it should look like what the leading AA standard looks like. Changing how AA works after a hard fork enabling it would be a massive PITA for everyone and would only slow progress.

---

**PixelCircuits** (2023-11-17):

IMO, the amount of complexity that this adds to the core protocol makes it not worth it. AA is continuing to evolve (for example intent based AA like UniswapX, [ERC-7521](https://ethereum-magicians.org/t/erc-7521-generalized-intents-for-smart-contract-wallets/15840/8), etc) and this would lock things into only the current solution.

Also, does this remove support for signature aggregation? I thought that was one of the biggest selling points of ERC-4337 since it gives huge cost savings to optimistic rollups.

---

**PixelCircuits** (2023-11-17):

I also don’t see how the “unused gas” griefing vector described can’t also be done with an EOA transaction. Is there a better description of the attack somewhere that explains how it’s unique to user ops?

---

**sk1122** (2023-11-20):

what’s the estimated timeline for EIP-9999? it contains some important things regarding this RIP, but overall a good proposal, is backwards compatible, enshrines most of the stuff

---

**alex-forshtat-tbk** (2023-11-20):

[@cejay](/u/cejay) [@Ivshti](/u/ivshti) [@sk1122](/u/sk1122)

The EIP-9999 was just a temporary placeholder for the [“ERC-7562: Account Abstraction Validation Scope Rules”](https://github.com/ethereum/ERCs/pull/105) document before it had an assigned number. I apologise for any confusion.

[@pantaovay](/u/pantaovay) thank you very much!

[@Ivshti](/u/ivshti)

Re: “changing the signature of the function instead of a version parameter”, we had an intention to make sure that we are only creating a single set of ‘special’ method IDs. However, if the method signature were to change with every revision of this RIP, their method IDs would change as well.

[@makemake](/u/makemake) [@PixelCircuits](/u/pixelcircuits)

This complexity is one of the reasons this proposal has been labeled as a “Rollup Improvement Proposal”, so hopefully it would not lead to locking things into a single solution too much.

Re: Signature Aggregation, it will not be removed from Native Account Abstraction but it is not part of this RIP, which is complex enough. “Native Account Abstraction Signature Aggregation” will probably be a separate RIP document in the near future.

---

**alex-forshtat-tbk** (2023-11-20):

> I also don’t see how the “unused gas” griefing vector described can’t also be done with an EOA transaction. Is there a better description of the attack somewhere that explains how it’s unique to user ops?

The issue of unused gas is only relevant for Type 4 Transactions because they can have their execution behaviour influenced by transactions that are coming **after them** in a block. This does not seem to be a problem unless the transaction suddenly starts using more gas than it used before.

Here is an example of how this could be turned into an attack on the block builder.

Here, Transaction #4 has a gas limit of 10’000’000. However, it only used 50’000 gas so there is a lot of available gas space in a block.

However, once Transaction #6 is included in a block and its validation phase flips some flag, Transaction #4 starts consuming the entire 10’000’000 gas.

[![Unused Gas Attack Block overview (1)](https://ethereum-magicians.org/uploads/default/optimized/2X/2/260174f697ca8c6fe7f5e5e3c69628323d970753_2_462x500.png)Unused Gas Attack Block overview (1)1460×1580 112 KB](https://ethereum-magicians.org/uploads/default/260174f697ca8c6fe7f5e5e3c69628323d970753)

---

**PixelCircuits** (2023-11-20):

So does the unused gas penalty go away after [ERC-7562](https://github.com/ethereum/ERCs/pull/105)?

---

**alex-forshtat-tbk** (2023-11-21):

> So does the unused gas penalty go away after ERC-7562 ?

Unfortunately, there seems to be no way to prevent the “flickering” gas usage by transactions with validation rules alone.

The “waste gas flag” storage can be read during execution phase of any transaction, and the “validation rules” are not meant to be applied during the execution phase.

---

**dror** (2023-11-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pixelcircuits/48/10513_2.png) PixelCircuits:

> IMO, the amount of complexity that this adds to the core protocol makes it not worth it

TL;DR: that’s the cost of account abstraction.

The complexity doesn’t come from the protocol itself (eip-7562 or ERC-4337) - It comes from the fact we want to use general-purpose EVM code for validation, which makes one transaction depend on external data - shared with other transactions, or with the external world.

With EOA, the validation is hard-coded into the protocol and depends only on the state of the account itself.

This means that a previously validated transaction can only be invalidated by issuing another transaction with the same sender (and nonce) to replace it.

With account abstraction (ANY implementation - 7560, 4337, 2938, and even 3078) we must have a mechanism to ensure the same isolation, otherwise, maliciously crafted transactions can cause mass invalidation: transactions that are accepted and propagated into the mempool, which later becomes invalid and thus draw resources from all nodes without a cost.

Removing this complexity exposes block-builders to DoS attacks, or requires removing the general EVM-code usage (the essence of account abstraction)

---

**PixelCircuits** (2023-11-22):

I’m not against complexity, just complexity at the core protocol level. At least ERC-4337 is opt-in and I can ignore it if I think there is too much risk or chose an alternate smart contract based AA solution. With this proposal, if something goes wrong for builders (some new DoS vector is found and exploited) or some bug is found, it would take down the whole network, including users who never cared about ERC-4337 style AA.

To me, it feels like trying to embed an OS into the bare metal. The bug surface area is too large and it would alienate others who want to use a different OS.

---

**yoavw** (2023-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ankurdubey521/48/10943_2.png) ankurdubey521:

> Why is unused gas a concern specifically for AA transactions and not regular EOA transactions?

Pasting the reply I sent you in 4337 Mafia on telegram in case others also wonder:

It protects the builder against a DoS vector, also applicable to 4337 bundlers (which is why the next EntryPoint version will have this as well).

Consider a builder trying to construct a block containing many AA transactions.  It creates a batch of AA transactions (equivalent to a 4337 bundle) where all the validations will be executed, followed by all the executions.  To work efficiently and not have to validate transactions sequentially, it wants to create the largest possible batch, validating all the transactions in parallel against the same state.  Otherwise it can’t parallelize because transactions can invalidate each other, which makes it vulnerable to DoS by many mutually-exclusive transactions where one transaction’s execution invalidates another’s validation.

An attacker could send transactions that have a high callGasLimit which they actually use when simulated separately, but that changes its behavior to use almost no gas when it detects that another transaction’s validation has been executed.  Suppose the batch has `[tx1,tx2]`.  `tx2.validation` sets `tx2.sender.flag=1`, and `tx1.execution` does `return (tx2.sender.flag==1 || waste5Mgas())`. It is allowed to access `tx2.sender.flag` because it happens during execution rather than validation.  The builder created the batch, thinking tx1 will use 5M gas and fill up the rest of the block, but due to the above behavior, 5M gas worth of of blockspace is not utilized.  The builder now has to append more transactions sequentially (not parallelized), simulating each of them against the state after all the others in order to know how much gas it really uses.

By penalizing unreasonably high unused gas, we make this attack less scalable.

---

**yoavw** (2023-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> Generally this RIP is amazing but the elephant in the room is the upcoming/placeholder EIP-9999, would be really fantastic to see what it refers to.

It’s [ERC-7562](https://github.com/ethereum/ERCs/pull/105/files).  We extracted the ERC-4337 validation rules to a separate (and hopefully more readable) ERC since they’re identical in both systems.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> Otherwise great job!

Thanks!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> My main comment would be about the version parameter in the validation function

I see Alex already replied this, but I’ll add that it was requested by one of the L2s.  They wanted to be able to add future extensions (maybe even specific to their own network) without having to redeploy or update accounts.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> At the risk of sounding like an optimizooor, it’s unfair to expect wallet implementations to implement full delegatecall upgradability cause it adds one mandatory SLOAD to each transaction.

I think making accounts upgradable offers security and usability benefits, well worth the SLOAD.  But we’re also looking for ways to make it cheaper.  For example, [EIP-7557](https://github.com/ethereum/EIPs/pull/7968/files) could make it as cheap as 32 gas for a widely used account while also making the protocol fairer.  Support EIP-7557 ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**yoavw** (2023-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/makemake/48/13855_2.png) makemake:

> IMO, this adds lots of complexity to the core protocol for something that can be done outside of it.

To put this in context, the RIP is meant for rollups that already added, or are considering adding the complexity of native AA.  Some already have, and some are planning to.  The purpose of this RIP is to standardize it for those who do, and avoiding fragmentation of the wallet ecosystem (wallets supporting only one chain, which is currently the case in chains that added their own form of native AA).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/makemake/48/13855_2.png) makemake:

> If AA ends up being enshrined, it should look like what the leading AA standard looks like.

and that’s precisely what this RIP does.  ERC-4337 has been gaining [some traction](https://dune.com/niftytable/account-abstraction), and has been used to add native AA in nonstandard ways by two L2 chains.  RIP-7560 is an enshrined version of ERC-4337, optimized for rollups.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pixelcircuits/48/10513_2.png) PixelCircuits:

> and this would lock things into only the current solution.

It shouldn’t.  That’s why we separated RIP-7560 and ERC-7562.  The mempool validation rules are incompatible with some forms of intents, but RIP-7560 isn’t.  Intent systems could benefit from RIP-7560 while being incompatible with the ERC-7562 mempool and using a separate intent-solvers network.  It’s one of the design goals.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pixelcircuits/48/10513_2.png) PixelCircuits:

> does this remove support for signature aggregation?

No.  But aggregation will be a separate RIP, to be published soon.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pixelcircuits/48/10513_2.png) PixelCircuits:

> To me, it feels like trying to embed an OS into the bare metal. The bug surface area is too large and it would alienate others who want to use a different OS.

It’s meant for chains that choose to embed this into their “OS”.  For example, Starknet and zkSync already embedded a similar native AA system (both are based on ERC-4337 with some mods).  You’re right that there is no way for you to opt out of it on these chains, whereas on a chain that doesn’t implement native AA, you can choose whether to use ERC-4337 or not.  L2 chains sometimes choose to be more opinionated about their OS for the sake of optimizing their UX and efficiency.  However, the Ethereum ecosystem offers enough choice of L2s so you can opt out by using a different one.  Some may choose to implement it early, some may be more conservative and wait.

---

**EGreg** (2023-12-24):

Will this lead to a precompiled contract for secp256r1 curve support, so we can finally implement wallets that integrate with the built-in private key encryption used in operating systems and secure enclaves?

https://github.com/ethereum/RIPs/pull/5



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ulerdogan/48/9227_2.png)

      [EIP-7212: Precompiled for secp256r1 Curve Support](https://ethereum-magicians.org/t/eip-7212-precompiled-for-secp256r1-curve-support/14789/69) [RIPs](/c/rips/58)




> EIP Update:
> As discussed in the RollCall#0 and RollCall#1, the final decision is that it would be more beneficial and quick to continue the proposal as a RIP. Thus, willing rollups will be allowed to complete their implementation around the standardization created with RIP.
> In this regard, a copy of the EIP with RIP naming has been merged into the RIP repo in the Last Call.
> https://github.com/ethereum/RIPs/pull/5
> The RIP specification will be finalized by determ…

---

**yoavw** (2023-12-24):

You’re talking about RIP-7212 (for which the answer is yes). But this thread is about RIP-7560.


*(15 more replies not shown)*
