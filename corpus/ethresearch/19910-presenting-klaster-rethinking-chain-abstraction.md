---
source: ethresearch
topic_id: 19910
title: Presenting Klaster - rethinking chain abstraction
author: fichiokaku
date: "2024-06-26"
category: Applications
tags: [account-abstraction, layer-2]
url: https://ethresear.ch/t/presenting-klaster-rethinking-chain-abstraction/19910
views: 3616
likes: 4
posts_count: 3
---

# Presenting Klaster - rethinking chain abstraction

# Introduction

We are witnessing an ever-growing list of new chains popping out, and attracting a high level of activity and transactions. Ethereum is also scaling nicely, and with the EIP-4844 it’s becoming increasingly cheaper to onboard as a user and start interacting with chains.

This introduces fragmentation, which in our opinion is here to stay especially in a world where there will be hundreds of chains, users will demand fragmentation to be solved for. If we build solutions that kind of aggregate different assets in some sort of “centralized” service only to make all chains look like one and make it easy to move across chains, then we haven’t accomplished much.

We propose a solution which abstracts away chains and solves for fragmentation by introducing **Klaster** - a network of nodes placed between the users and chains. This layer wraps multiple blockchain networks and makes it easy for users to execute complex transaction flows spanning across one or more chains - all of that approved by the single off-chain signature.

By introducing the Klaster Nodes as a generic execution network, and defining how cross-chain transactions are being bundled and approved, we hope to set the standard for building chain abstracted applications. This goes beyond just a simple balance abstraction - spend your funds from one chain by interacting on another chain. It provides a “full” chain abstraction by allowing any arbitrary flow to be defined and executed.

# TL;DR

Klaster Protocol aims to position itself as a chain abstraction framework which allows dApps or Wallets to build complex cross-chain transaction bundles and let the users sign only once to execute these bundles across one or more blockchain networks.

We introduce two key concepts:

- iTx bundles: series of (possibly dependent) transactions spanning across many chains
- Transaction Commitment Layer: network of nodes providing execution guarantees and offering orchestrated iTx execution across many blockchain networks

Klaster Protocol leans on Smart Accounts and ERC-4337 EntryPoint and by introducing the economic incentives provides a reliable network of Klaster Nodes which anyone can use to build truly chain abstracted dApps while not sacrificing on the security, or taking the control from the user.

# Klaster

Klaster provides an infrastructure for building chain abstracted apps. Klaster does this by introducing a network of Nodes, which act as a **Transaction Commitment Layer**. This layer is placed between the dApp and multiple blockchain networks, It talks to the outside world (users, dApps) via **interchain transactions (iTx)**.

Developers can use these primitives to:

- Build chain abstracted dApps (no switch network button)
- Define complex flows involving multiple chains without having to think of the specifics of how the flow will get executed
- Automate the execution of the dependent actions spanning across many chains
- Onboard the users from different chains and ecosystems into their dApp with a single user signature

Users on the other hand:

- Can interact with chain abstracted dApps using any wallet they prefer
- Don’t have to care of where their funds are, the dApp will be able to spend their funds from other chains with a single user signature
- Don’t have to “lock” their funds in order for the dApp to consume their funds
- Can use any asset on any chain to pay for gas cost of the full iTx execution involving many transactions on different chains

## Core concepts

At its core, Klaster leans on its unique approach of **separating transaction signing from

the transaction execution**.

If we think about how the EOA is executing a transaction on an EVM - it’s all bundled in the same operation - sign & execute happening simultaneously with the user having one EOA wallet popup and interacting with the chain/RPC.

A more advanced approach can be seen with the Account Abstraction (ERC-4337), where users can approve their UserOp and then hand it over to the Bundler for execution. This approach is still bounded to one single chain - the one where the user’s smart account is deployed.

Klaster Model breaks the boundaries of a single chain, and allows an account owner to approve a complex series of (possibly dependent) UserOps targeting different blockchain networks - with a single off-chain signature! This signature is then provided to the Klaster Node (what would be a bundler in AA), for orchestrating an execution across all the different chains.

[![photo_2024-06-26_14-25-17](https://ethresear.ch/uploads/default/optimized/3X/7/5/755b51c20b470de874fc70cf3589d99577681458_2_690x388.jpeg)photo_2024-06-26_14-25-171280×720 49.9 KB](https://ethresear.ch/uploads/default/755b51c20b470de874fc70cf3589d99577681458)

As seen from the illustration above, if the user wanted to bridge funds and then swap on the destination chain, they would usually execute two transactions, on two different applications (Bridge app & then DEX app), while also having to pay for gas fees on two different chains.

By splitting the signature from the execution, Klaster is able to convert two actions into one **iTx bundle** and then execute them through the Klaster Node. Klaster node will figure out the ordering of transactions, and execute them as user intended, while also covering for execution fees.

## Interchain Transaction (iTx bundle)

**Interchain Transaction (iTx)** is the fundamental working unit used within the Klaster protocol. It’s a bundle of one or more blockchain transactions spanning across one or more blockchain networks. It fully describes what the user or the dApp is trying to achieve. One iTx, consisting of two transactions, might be: “bridge assets from chain A using some 3rd party bridge to chain B, and then swap bridged assets for something else on chain B”.

From the Klaster Protocol perspective, one iTx bundle is actually a Merkle Tree of all the UserOps as leaves, and is defined by its Merkle Root hash (iTx hash): **one iTx bundle = one unique iTx hash**.

Any on-chain interaction on any blockchain network can be converted to the UserOp and placed as a part of a bigger iTx Merkle Tree - meaning the iTx tree approach can be used to basically define any complex operation spanning across multiple blockchain networks provided that there’s at least some liquidity services connecting the chains.

[![photo_2024-06-26_14-27-23](https://ethresear.ch/uploads/default/optimized/3X/2/a/2a26e4bc6a55b451b319a567816c3f9fd11c8b5a_2_690x388.jpeg)photo_2024-06-26_14-27-231280×720 50.5 KB](https://ethresear.ch/uploads/default/2a26e4bc6a55b451b319a567816c3f9fd11c8b5a)

Transaction Commitment Layer takes unsigned iTx requests, and **commits** to execute them in the specific time frame - and therefore provides a reliable execution layer capable of executing the parts of the iTx on different blockchain networks. This involves strategically determining the optimal order for executing the individual transactions within the bundle. For instance, if a transaction on Polygon relies on assets being transferred from Ethereum first, the node will ensure that the Ethereum transfer is finalized before proceeding with the Polygon transaction.

## High Level Protocol Overview

[![photo_2024-06-26_14-28-18](https://ethresear.ch/uploads/default/optimized/3X/4/4/44e74558671473aa21b67bb54151e8dea1ce9070_2_690x388.jpeg)photo_2024-06-26_14-28-181280×720 55.8 KB](https://ethresear.ch/uploads/default/44e74558671473aa21b67bb54151e8dea1ce9070)

The following steps are involved for the user/dApp to interact with the Klaster Protocol:

1. dApp defines a list of operations to be executed across one or many chains and bundle them together into the iTx
2. dApp asks the Klaster Network for a quote (fee) for executing an iTx
3. dApp receives back the iTx with included fee amount and cryptographic execution guarantees given by the Klaster Network
4. User signs the iTx by signing its root iTx hash and then broadcasts the signed iTx back to the Klaster Network

Once the Klaster Network receives the signed iTx, it will charge the user upfront by pulling the fee amount as defined in the quote, and it will start processing the transactions from the iTx bundle, executing them on the different blockchain networks in the correct order. The specifics of how the fee is being calculated and charged upfront is outlined in the technical breakdown section.

## Chain Abstraction vs Balance Abstraction (AAVE example)

While balance abstraction is a great step forward in solving for liquidity fragmentation, it’s not covering all bases. Let’s say we want to build a chain abstracted version of AAVE, where users can interact with the dApp not only by having the “balance” abstracted away (supply assets from one chain to AAVE deployed on another chain), but also having an **AAVE “position” abstracted** away which is a more dApp specific use-case.

For example, a user might have 100 USDC supplied on AAVE on Optimism, but they want to switch the position to Base, and supply USDC there, because of better rates. Or there’s a bot that wants to do this periodically, in the user’s name and with the user’s approval.

Right now, the user would have to unwind their position, find a bridge to use, move liquidity to Base and then resupply the USDC. This involves signing multiple transactions and switching between multiple frontends and blockchain networks / RPCs, not to mention also having some gas dust on these chains to be able to execute transactions in the first place. We believe this is unsustainable and there has to be a way of “standardizing” these interactions & making life easier on the user facing side.

By using Klaster protocol, this complicated “position” rebalancing operation can be converted to one simple iTx bundle containing three UserOps:

- [Optimism] UserOp1: unwinds AAVE USDC position on Optimism
- [Optimism] UserOp2: bridges 100 USDC to Base using some third party bridge (across bridge, for example)
- [Base] UserOp3: supplies 100 USDC on AAVE

[![photo_2024-06-26_14-35-03](https://ethresear.ch/uploads/default/optimized/3X/a/a/aaccd85ed18ac9bacdc8cfe3806eb872019b0363_2_690x390.jpeg)photo_2024-06-26_14-35-031276×722 56.8 KB](https://ethresear.ch/uploads/default/aaccd85ed18ac9bacdc8cfe3806eb872019b0363)

The only thing the user would have to do from their side is provide one signature for the iTx and the balance reposition would be handled by the Klaster Protocol automatically. No gas required on the destination chain. No different apps involved. One simple signature. And we bet that if the developers are provided with tools like Klaster, many more other interesting use-cases might emerge other than the one we’re describing here.

# Technical Breakdown (I want to know more)

## Smart Accounts - iTx Module

Using an iTx bundle in combination with Smart Contract Accounts allows for one very powerful feature to be implemented - and is there to help on the UX side: **single signature iTx approvals**.

Smart Account modular architecture allows for building a standardized ERC-7579 module which “understands” iTx bundles and can be installed on top of existing smart account wallets or used to initialize new wallets as the UserOp model allows for providing the wallet initialization data as a UserOp parameter.

A smart account owner can approve the whole iTx bundle of many chain transactions by only **signing once** - one off-chain signature of the iTx Merkle Root hash can be used to approve for executing all the transactions across many chains.

As mentioned earlier, the tree is defined by its Merkle root hash - iTx hash. The smart contract owner signs the iTx hash with a signer. This typically is an EOA which is a common owner of all the smart accounts across different chains where the assets are being bridged and consumed, and by providing one signature, all of these operations are immediately executable.

If the user doesn’t have a smart contract account on one or more blockchain networks - the accounts can be “lazy deployed” for the user - meaning, the iTx bundle can contain an operation which bridges some amount of funds to the “not yet created” account as the address of the smart account can be precomputed.

By having the iTx validation module as a standardized module - Klaster protocol remains neutral & unopiniated - it can work with different smart account providers.

## Klaster Fees & Node Selection

The Klaster Transaction Commitment Layer consists of many Klaster Nodes - all of them being equal. Every Node is defined by its wallet address, and in order for nodes to join the network, they have to stake capital - this is how the nodes provide uptime & execution guarantees.

Klaster Nodes are taking care of the following:

1. Estimating iTx fees & responding to quote requests
2. Committing to iTx execution (or rejecting the request)
3. Executing fully signed iTx (if previously committed to execution)

### Estimating iTx fees & responding to quote requests

When the user or the dApp asks the protocol for quotes, every node will estimate the total cost of executing the iTx on different chains. The node adds its own fee on top of the total cost, including the **success execution tip** (more on this in the “optimistic execution” chapter) and responds back with the full cost the user will have to pay in order for the node to do the job.

### Committing to iTx execution (or rejecting the request)

The user or the dApp chooses the best received quote by taking into account the total execution cost offered by each of the nodes, and their reputation. The dApp then connects directly with the selected node, and asks for a commitment - a guarantee from the node that they are going to execute the iTx in full, provided that the user pays for what the node asks for.

The node commits to the iTx execution by

1. Prepending the payment tx* in the list of the transactions in the iTx bundle
2. Signing the root iTx hash with its own private key - essentially binding itself to the execution of the iTx

**A payment transaction generated and prepended by the node transfers some liquid asset from the user’s account to the node wallet address. The asset is selected by the user and the amount is calculated by the node to cover for all the execution costs + the node fee. This means that the user can pay for the execution on any chain and in any asset supported by the node.*

### Executing fully signed iTx (if previously committed to execution)

Once the dApp receives the iTx which includes the payment transaction and the node commitment, the user is finally prompted to approve the full iTx bundle by signing the root iTx hash - essentially approving the execution of all the transactions contained in the bundle. The iTx bundle, whose root iTx hash has been signed by both the node (commitment) & user (execution approval) is sent to back the selected node which:

1. Verifies the iTx bundle integrity (calculates & verifies merkle root)
2. Verifies the commitment signature (make sure the node really did commit to this iTx)
3. Verifies the user signature
4. Collects the payment from the user (the first transaction in the iTx bundle)
5. Once the payment is complete, proceeds to execute the rest of the operations by performing the optimistic execution algorithm

If the node fails to execute the iTx bundle, the user can use the node commitment (node iTx signature) to initiate a slashing request and prove on-chain that the node actually promised to execute the iTx but failed to do so in a given timeframe.

## Meta Paymaster and Multichain Gas Refunds

For the node to be fully operational, they have to own the native coin balance on their wallet address for every chain they support - in order to be able to pay for gas and execute UserOps as a part of iTx bundle. By accepting the upfront payment from the user in one token and one chain, and then executing the transactions and subsidizing gas on one or more chains, Klaster Node acts in a way as a Meta Paymaster.

The node executes UserOps contained in the iTx by routing them through the official ERC-4337 EntryPoint on different chains, and after receiving post-operation execution callbacks with the actual gas consumption data, the node will execute refunds for every processed UserOp, that is if actual UserOp cost (including the Klaster Node fee) was less than the maximum UserOp that was prepaid by the user. The process is illustrated below:

[![klaster-meta-paymaster-latest](https://ethresear.ch/uploads/default/optimized/3X/9/c/9ca11c122eee71670ddf3e95a2ecee88cf427bcb_2_569x500.png)klaster-meta-paymaster-latest943×828 47 KB](https://ethresear.ch/uploads/default/9ca11c122eee71670ddf3e95a2ecee88cf427bcb)

By relying on the official ERC-4337 EntryPoint for UserOp routing, the Klaster Protocol is staying compliant with the AA space, since most of the AA wallets today choose to trust and give control to one EntryPoint contract. Any existing AA wallet could technically activate the Klaster iTx module and gain cross-chain capabilities.

## Optimistic iTx Execution

Klaster Node is incentivized to execute UserOps from a given iTx bundle in the right order of events, without the user having to explicitly provide the order of events.

The right order of events is implicitly deduced by the Klaster Node, by repeatedly simulating every UserOp, between the timestamp deadlines set by the user when defining UserOp, and waiting for the simulation to yield 0 *REVERT* opcodes in the simulated execution breakdown. Once this happens, Klaster Node “knows” all the preconditions have been met (whatever they may be) and will proceed to execute the UserOp as this maxmizes the profits for the Klaster Node.

In our AAVE example from above, Klaster Node will wait for the bridge action to complete without having to be aware of which bridge is being used and what the estimated bridge time to destination might be. It’s not even aware of the context of any UserOp or the potential dependencies between those. The execution flow would look like this:

1. The Node executes the Payment UserOp (at index 0 in the list of UserOps). That way the Node charges for the full execution of all the other UserOps upfront and can proceed with the next steps
2. The Node “sees” that out of three UserOps (unwind, bridge, supply), the only one with 0 REVERTs is the unwind operation, and it proceeds to execute the UserOp successfully (on Optimism)
3. Afterward, another operation that yields 0 REVERTs is the bridge operation as the funds are now there to be bridged (unwinded position), so it proceeds to execute bridge action (on Optimism)
4. Finally, once the funds arrive at the user’s dest chain smart account (whenever that may be, depending on the 3rd party bridge being used), the supply operation is executed which marks the full iTx execution as complete.

[![photo_2024-06-26_14-45-59](https://ethresear.ch/uploads/default/optimized/3X/b/b/bb781b0246065508b7a832ee5060408e61d20a87_2_690x388.jpeg)photo_2024-06-26_14-45-591280×720 33.2 KB](https://ethresear.ch/uploads/default/bb781b0246065508b7a832ee5060408e61d20a87)

By having this generic approach of not being aware of the context, iTx bundles can express pretty much any complex cross-chain flow. To incentivize the node to wait for the simulation success (0 REVERTs), but then also to execute the UserOp **as soon as 0 REVERT is detected,** Klaster fee will include the **diminishing success tip**. This fee can be collected by the Node only if the UserOp was executed with 0 REVERT status and the tip is fading to 0 as the UserOp execution moment is closing to the upper bound execution timestamp.

*It is still possible for some of the UserOps to fail, for example, 3rd party bridge not working properly. In that case - the node has fulfilled its obligation, as it’s recorded on-chain that the node “attempted” to execute the UserOp, although the funds haven’t reached the destination chain. In that case, the node is protected from slashing, while the user experienced a partially executed iTx. The funds are still owned by the user, and have remained on their wallet on one of the chains where the UserOp failed.*

# Integration

dApp/Wallet developers will soon have access to the SDK, which in turn will allow for building chain abstracted applications much more efficiently, while staying neutral and not locking the developer to having to use any specific technology.

The developers are free to use any bridges or 3rd party services as a part of the iTx bundle - depending on the level of security/speed they require, and to rely on different AA wallet providers as the smart account wallets used behind the scenes.

On the user side, they have to sign once, and see their cross-chain intent being executed step by step without having to do any other action or even own gas funds on any of the chains they interact with.

This is how we see it developed further and how dApps might integrate the SDK in order to provide cross-chain experience to the end user:

[![photo_2024-06-18_13-18-43](https://ethresear.ch/uploads/default/optimized/3X/6/5/65e8e1fa54439727f6d9a820b1d86e740f228025_2_690x315.jpeg)photo_2024-06-18_13-18-43900×411 58.2 KB](https://ethresear.ch/uploads/default/65e8e1fa54439727f6d9a820b1d86e740f228025)

# Demo & Use Cases

At the moment, we’re building a chain abstracted AAVE dApp - to showcase what the protocol can do in terms of UX improvements.

The frontend will only contain two buttons: “supply” & “borrow” without specifying the chains. When executing borrow or supply, user’s funds will be routed to any chain where the AAVE market’s rates are most favorable, regardless of the fact which chain the user’s funds are on.

If the user wants to rebalance the existing position, again, it’s a one-click interaction for the user, but in the background, iTx is being executed by the Klaster Nodes.

Some other interesting use cases:

- streamlined checkout flows
- easier onboarding to the SocialFi L2/L3 apps, as Klaster protocol works with AA by default, and many of these apps choose to have embedded wallets generated for the users behind the scenes
- building chain abstracted flavors of dapps that are natively multichain (DEXs, lending markets, NFT marketplaces)
- single-chain dApps can use the Klaster Stack to streamline onboarding flows, attracting users from various chains. With Klaster Stack, users can interact with the dApp in just one click, regardless of their original blockchain

# FAQ

**Q: Is Klaster a Blockchain Network?**

A: No.

**Q: What’s the current development status?**

A: Centralized Klaster Node including the SDK and the docs is in the testing phase and will be launched very soon. The decentralization phase including the slashing and multichain staking which in turn makes the network more reliable will most likely be rolled out later this year.

**Q: What are the dangers of using Klaster Protocol?**

A: Dangers are mostly related to the impaired UX.

For example, malicous Klaster Node can refuse to process an iTx bundle in full - they only execute the Payment UserOp part of the iTx bundle. The user can still replay their UserOps manually and achieve the same effect but will have to pay for gas execution themselves. Nodes on the other hand get slashed in the decentralized model because the user can submit a proof of Node commiting to execute the iTx but failing to do so in a given timeframe - which is fully verifiable on-chain. As the AA wallets are used behind the scenes, the user is in full control of their funds, and the security is reduced to security of bridges used as an intermediary steps to move assets between chains. Klaster’s iTx-enabled AA wallet module is pending audits and the reports will be shared soon.

**Q: Can I run my own node, and what are the advantages of running a node?**

A: Klaster Protocol will host its own public node, with the implementation publicly available for everyone to take a look and verify the inner workings of the Node itself. While the initial version of the protocol is not decentralized in a sense of having a p2p networking implemented between public Klaster nodes, anyone can still choose to run their own Klaster Node either for their own purposes (only handling one single dApp) or even providing this node for others to connect to.

New chains can spin up their own Klaster node to easily onboard users from other chains.

Klaster Node if operational earns a % of the total gas processed and is another revenue stream for Node operators. To set up a node, one needs to have a wallet connected to the node, and funded with native coin on every chain which the Node operator decides to support.

**Q: How does Klaster compare to other chain abstraction solutions?**

A: For a start, we think we have a unique approach here in being highly focused on the UX part. We’re trying to stay as generic and as neutral as possible, and we’ve developed something that can be used today to fix the UX in some ways. Comparing to some other approaches we see being built in this space, Klaster’s main difference is that Klaster doesn’t work with liquidity nor does it require the Node operators to provide liquidity - meaning it’s easier to run the network and gain an initial base of Node operators. It doesn’t try to be “one solution fits all” which hides away blockchains completely, but rather a framework where, given the fact that the cross-chain action details are known upfront - it enables developers to easily define and build the action, and for the user to sign once and see the effects happening on different chains.

**Q: Where does Klaster Protocol fit in the CAKE framework?**

A: According to the CAKE Layer definitions, we’d say Klaster comes somewhere in the Settlement Layer (Execution part).

**Q: Is Klaster Protocol a bridge?**

A: Not really. Klaster Protocol can *wrap* bridges and other services to create a true cross-chain experience by having bridge action only there as a one step of the more comple iTx interaction.

**Q: I want to know more about the slashing process. Why do the Nodes have to stake capital, and how does slashing work?**

A: Klaster Nodes have to execute iTx bundles if they previously “promised” to the user they will do so. There has to be a way of punishing the Node for not doing their job - or even worse, collecting the fee payment from the user but never executing their desired intent. To make this possible, Klaster Nodes have to stake capital in order to be accepted by the network and allowed to execute iTx bundles on user’s behalf.

Every UserOp contains lower and upper bound timestamps, and the interval between these are when the UserOp is considered valid and can be executed on-chain. When the Node builds a full iTx tree, and signs the root iTx hash with their private key - we say the Node is “commited” to the iTx. The user has received the full quote including the Node commitment, and can use this commitment to initiate a slashing procedure if the nonce of the user’s smart account was not increased by one in the given timeframe, on any chain where their UserOp was **not executed**.

**Q: Is Klaster Protocol actually an Intent Solver network?**

A: Not really. Intents mean the user describes the end-result state and *someone somehow* finds the solution to the steps (txs) required to achieve the desired outcome. Klaster takes a completely opposite approach. The design space of the intent solvers is just too big and solving for all cases using intents is simply too complicated. We say - let’s make the system more exact, in a sense that, we assume that the developers of either dApps or wallets will always know upfront what exactly they want to achieve - and then let’s give them tools and means of how to express this interaction (iTx bundle) while making it easy for users to approve and execute these iTx bundles.

Klaster Protocol though is a great tool for Intent Solvers to express & execute their “paths of execution” once they solve for some specific user’s request.

**Q: What’s the role of AA Wallets in the Klaster Protocol?**

A: AA Wallet is the only viable option for Klaster Protocol to work. Since we need to be able to have the user authorize many actions with only one signature - the only possibility for this to work is to actually use programmable smart contract wallets.

**Q: How is the Node protected from users? How are the users protected from the Node?**

A: The Node charges for its service fee plus all the other execution gas costs upfront. This way, the node might overcharge for the gas spendings, but the user will still get charged fairly if the actual gas spent was lower than what the node calculated. The Node will not commit to execute the iTx if the iTx looks risky - too short timespans for the UserOp execution, or the UserOp execution window which starts far away in the future (gas price spike risks).

The user is protected from the Node by being the only owner of the AA Wallet which used to execute iTx steps. Even if the Klaster Network dies completely, the user can still access and manage funds. The Klaster Node can only do what the user explicitly signs & approves.

**Q: Does the user need to own the funds on the AA Wallet to interact with the Klaster Protocol in the first place?**

A: Unfortunately yes. If the user’s coming with an EOA wallet and assets are held by this EOA, the user will have to execute at least one EOA transaction and move funds from this wallet to an iTx enabled AA wallet to be able to use Klaster for chain abstraction / gas abstraction purposes. Luckily, the EIP-7702 which is confirmed will improve this flow substantially.

## Replies

**EugeRe** (2024-06-26):

That’s a nice work [@fichiokaku](/u/fichiokaku) ! I am building over the same concept of chain abstraction from a different perspective on my blogpost. Happy to share ideas.

---

**fichiokaku** (2024-06-27):

Thanks, [@EugeRe](/u/eugere) ! Reached out to you via DM.

By the way, there were some more questions regarding the node risks and how does the node know how much to ask for the upfront payment from the user considering the fact that gas spikes might happen before the node starts executing the bundle.

Thanks to the EIP-1559, we know that the gas price can increase 12.5% per block at most, so the node can take this into account and hedge against the risk by asking more for an upfront payment and then executing the refunds at the moment of execution.

In the end, the node only has to execute what they chose to commit to, and different node implementations might choose different levels of risk.

The other thing worth mentioning is the expansion of Klaster Protocol on the non-EVM stack. Provided that the non-EVM chain has a support for public key recovery from secp256k1 ECDSA signatures, we can integrate the chain and allow for transacting on the non-EVM chain by paying for gas from an EVM chain, or any other use case!

