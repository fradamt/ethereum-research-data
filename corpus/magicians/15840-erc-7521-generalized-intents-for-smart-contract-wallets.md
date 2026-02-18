---
source: magicians
topic_id: 15840
title: "ERC-7521: Generalized Intents for Smart Contract Wallets"
author: PixelCircuits
date: "2023-09-19"
category: ERCs
tags: [erc, wallet, account-abstraction, intents]
url: https://ethereum-magicians.org/t/erc-7521-generalized-intents-for-smart-contract-wallets/15840
views: 4662
likes: 7
posts_count: 13
---

# ERC-7521: Generalized Intents for Smart Contract Wallets

Discussion thread for [ERC-7521: Generalized Intents for Smart Contract Wallets](https://github.com/ethereum/EIPs/pull/7739).

https://github.com/ethereum/EIPs/pull/7739

The purpose of this ERC is to provide a single common interface for intent-based projects in the Ethereum ecosystem, unlocking future-proof access to the evolving intent landscape for developers and securing composability in the longer-term.

## Replies

**PixelCircuits** (2023-09-19):

A more detailed rationale is outlined in this [blog post](https://blog.essential.builders/introducing-erc-7521-generalized-intents). Any discussion related to this ERC can be facilitated below.

---

**JXRow** (2023-09-20):

It is complex, how is the gas cost?

---

**PixelCircuits** (2023-09-20):

It depends on how complex the intent is and gas usage is more efficient when lots of intents are included in the same solution. We’re currently working on gas optimizations, but we’re aiming to make it not much more expensive than ERC-4337. We should also be able to take advantage of EIP-1153 once it goes live.

---

**paul0x741** (2023-09-20):

Thanks for your work on this! I just have a couple questions to clarify after reading through the proposal.

1. How would you let solvers submit additional data like for example if a standard requires proof of some computation or proof that some conditionals had been met with private data? Or basically if a standard would want some extra data for validation on the intent solution, can the context be used for this (not sure)?
2. Do you guys have any thoughts on proving an optimal solution was submitted?
3. Any thoughts on intent privacy and how this standard would evolve for that?
4. If the intent entry point needs to be upgraded is there an easier way to upgrade for all standards and AA wallets instead of manual updates?
5. Is it possible for different solvers to cooperate on different segments of an intent? For example, if they are specialized in different things like bridging, swapping, resolving external data dependencies etc.

---

**PixelCircuits** (2023-09-20):

1. Good question! This would be a design problem for the intent standard to develop. One possible solution could be to create two new intent standards, lets call them “Data Blob Standard” and a “ZK Proof Check Standard”. The “Data Blob Standard” would simply be an arbitrary bytes dump that is intended to be placed just before another intent segment that would like to consume that data. the “ZK Proof Check Standard” could then check that the segment processed before it is of the standard “Data Blob” and use its’ data as a provided ZK proof. I’ve actually gone ahead and added an issue to the reference implementation for the EntryPoint to gracefully interpret an intent with no set standardId or sender as a data blob.
2. It’s difficult to do this on-chain, but we imagine dutch auction style flows to achieve similar results. For example, a basic trade intent that releases more and more ETH over time in order to get the DAI they want. Another controversial way to do it would be a private mempool, but could also be done decentralized using something like flashbots SUAVE.
3. Haven’t thought too deep about privacy, but I imagine that’s something that needs to be done on the mempool off-chain side of things. Again, projects like SUAVE could help.
4. All the standards would have to be redeployed for the new EntryPoint contract, yes. The reason the registration process is so strict was to avoid any possible exploits from registering a contract as an “Intent Standard” that really isn’t. I can’t actually think of any exploits right now, but early in the spec construction, there was some cause for concern with overlap in function names and an old requirement that the smart contract wallet had to give super permissions to calls coming from the EntryPoint (no longer the case). If we think this is being too cautious, we can remove it. Making the smart contract wallet store the EntryPoint in storage is really just a gas optimization thing. We could add EntryPoint to the signed intent itself, but it would add calldata and still require the setting and clearing of  the EntryPoint in the wallets storage as it needs to persist for the rest of the transaction in future function calls on the wallet. Transient data (EIP-1153) could help here though.
5. Haven’t thought too much into that. I think this is out of scope for the spec, but it might be possible on the mempool layer where partial solutions would be gossiped instead of individual intents. Of course, this would require a trusted relayer, or possibly use something like SUAVE for more decentralization.

---

**fmc** (2023-10-26):

Hey,

Solid proposal and interesting adoption of EP idea to intents space.

1. > Instead of smart contract wallets having to constantly upgrade to provide support for new intent standards as they pop up

Is it still the case with Modular Smart Accounts? Installing a new module to support new intent standard would be easy process, much easier than upgrading a wallet

---

**PixelCircuits** (2023-10-26):

Modular Smart Accounts will be helpful for smaller things like adding signature schemes, but it would still be a burden to users to have to make sure their wallet has all appropriate modules installed (and the correct version of the modules) before every action. Consider the scenario where a user wants to sign two intents that require different versions of the same module. The user would potentially have to go back and forth uninstalling and installing different modules before each intent, and you couldn’t overlap intents that have incompatible requirements.

I would also say that there is slightly better security in electing code to run once via ERC-7521 rather than having it become a permanent part of your wallet. In ERC-7521, if a bug is identified later down the road, only wallets that have unsolved intent floating in the mempool would be effected.

---

**cleanunicorn** (2023-12-19):

I recently penned an in-depth analysis on Intents.

This is for those who want a detailed look at the arguments supporting and opposing the proposal. I appreciate everyone who added to the discussion thread. Your insights were very helpful in my research.

https://www.edenblock.com/post/the-next-blockchain-bull-run-user-intents-paving-the-way-for-mass-adoption

---

**while1** (2024-02-21):

Thanks for putting together this proposal. It will definitely help with UX and adoption. A few questions:

- How does the proposal plan to handle fee payment? Intents, in its generic form, may include many types of operations. Some of them can be simply automation tasks that the end users would like to achieve. Such tasks may not have much MEV value to extract and solvers likely may not have incentive to process these intents.
- How do you plan to mitigate the potential state discrepancy between simulation and execution? In ERC-4337, it applied fairly restrictive standards in terms of storage access, which I think, would ban a ton of operations. In fact, if a smart contract wallet user wants the solver to open up a Uniswap V3 position on his/her behalf, it would not be possible using ERC-4337, because the position open would entail the access of non-owner storage slot.

---

**PixelCircuits** (2024-02-22):

The fee incentive can be resolved in many different ways and is out of scope for ERC-7521. Some ideas include using a reverse dutch auction model where an intent releases some amount of some token, which increases over time. The hope being that the competition forces solvers to solve as soon as the release makes it profitable to do so, or else lose it to another solver. Another idea is that an intent can specify an oracle they trust to price how much they need to compensate the solver upon solving.

This mitigation is no different than what MEV searchers deal with today. Solvers (the submitters of intents to the entrypoint) are expected to be as sophisticated as current MEV searchers. They’ll want to not only simulate their solutions, but submit them to block builders (the typical PBS process) with very specific requirements like potentially being top of block.

---

**Karotoka** (2024-03-17):

This proposal is a very useful standardization for intents as interest in them and implementations of them grow.

One addition that I think would be useful is a set of optional functions that would allow the creator of the intent (or the front end putting it together) to exclude specific addresses from either being Solvers of that intent or included in `intentData`.

This would be useful because the requestor of the intent does not have any control over the identity of the solver or the solution that the solver proposes in `intentData. This means that a naïve requestor could end up either being solved by a prohibited person (e.g. an OFAC listed person) or swapped through a nefarious pool, unknowingly exposing the requestor to legal liability or prosecution.

Such a function should not be imposed on the user but it may be prove useful for potential builders to keep their users safe if they so choose.

---

**PixelCircuits** (2024-03-17):

Ah yes, great idea! Restricting the solver (either whitelisting or blacklisting) can be done as an intent standard (outside the scope of the entrypoint itself).

Unfortunately, it is much harder to guarantee certain contracts are not touched during execution. An intent standard could look through all the intents on the solution and see what intent standards they use and their senders, but there are just too many ways to obscure an eventual call to a blacklisted contract (wrapper contracts, etc.) A more sophisticated solution would have to be implemented.

I can think of the following few options:

1. Create an intent standard that only allows for a whitelisted solver or certain contracts the solver can use that are known to not touch the blacklisted contracts. The downside is that this exclude your intent from benefiting from coincidence of wants with other intents and limits a solvers complexity.
2. Create an intent standard that whitelists a set of solvers that are trusted to stay away from blacklisted contracts. A slashing mechanism could be put in place to increase trust where the touching of a blacklisted contract could be zk proven after the fact. In the future with real time zk proofs, a solver may be able to zk prove their solutions execution will never touch a blacklisted contract in the middle of it executing on the EVM, but we’re a long way away from real time zk proofs right now.

