---
source: ethresearch
topic_id: 20992
title: On trustless cross-chain asset transfers
author: Ashy5000
date: "2024-11-15"
category: Layer 2
tags: []
url: https://ethresear.ch/t/on-trustless-cross-chain-asset-transfers/20992
views: 225
likes: 0
posts_count: 1
---

# On trustless cross-chain asset transfers

**On trustless cross-chain asset transfers.**

NOTE: Early development of this protocol has begun under the name Viaduct.

*Preface*

In the state of Ethereum today, layer 2 blockchains experience fragmentation between each other and with the Ethereum mainnet. One core piece of solving this problem and achieving effective interoperability is cross-chain asset transfers. Many bridges implement this functionality, but they do so in a way that, to some extent, relies on trust.

But, by using a signature-based transaction system, it is possible to trustlessly mirror token transfers across multiple networks. The only trust assumption is that **at least one** honest node exists and that the network can detect and relay transactions in a reasonably short period of time.

*Part I: Single-deployment*

The first step is to create a system that can reliably handle signature-based transfers on a single smart contract. The protocol splits these transfers into three parts: retrieval, signing, and execution.

The retrieval step calls `getValidHash()` on the protocol’s core smart contract. This method will, given a sender, recipient, value, and nonce, calculate and return the requested transfer’s hash.

Then comes the signing step. Once the contract finishes its calculations, the transaction sender can sign the resulting hash to approve the transaction. Signatures are valid for one transfer only. If the sender wishes to repeat a transaction, it can calculate a new hash and signature using a new nonce.

Finally, in the execution step, anyone with access to the transaction signature can call `objectiveTransfer()` on the core contract. After checking for double spending and signature correctness, the contract transfers the correct number of tokens from the sender to the recipient. Either the signer or a so-called relay node could initiate the `objectiveTransfer()` call. Note that relay nodes may introduce fees into the transfer process.

This system allows for token transfers via signatures and relays. At this point, this design replicates the benefits and drawbacks of a system like Uniswap’s Permit2.

*Part II: Cross-deployment*

The next step in creating a cross-chain trustless signature transfer system is enabling this protocol to function across multiple deployments or instances of the core contract, all on the same blockchain. While it might not seem relevant now, it forms an important piece in the infrastructure for cross-chain transfers.

Each deployment can keep track of a list of other deployments. It is not necessary for every deployment to be aware of all others. The only requirement is that there is a route, direct or indirect, between any two given instances. Then, whenever a deployment receives a valid objective transfer, it can initiate an identical transfer call on each of its peer chains. Those chains can independently verify that the call is correct before executing the transfer and recalculating balances appropriately.

Attempts to double-spend tokens on multiple instances at once will fail. Because each instance is on the same blockchain, signers can’t execute multiple transactions at once. This means that all deployments will remain in sync, blocking all double-spending attempts.

*Part III: Isolated cross-deployment*

Now, the core contract deployments or instances need a way to run a secure version of the protocol without communicating with one another. To enable cross-deployment transaction execution, there can be a permissionless relay node network that monitors onchain objective transfers and relays them to each deployment.

However, at this point there remains a critical flaw in the protocol. If the same sender initiates two transactions on two different deployments simultaneously, both sending over 50% of the sender’s balance to two different addresses, the sender can double-spend. Both deployments will reject the transaction they did not receive initially, and their account balances will differ.

To resolve the double-spending issue, the core contracts use a *challenge window* . Each window lasts w_f seconds long and consists of two periods: the proposal period and the challenge-only period, which last for w_p and w_c seconds, respectively. The core smart contract disables the `objectiveTransfer()` function during the challenge-only period.

When a signer submits an objective transfer, the contract checks it for double-spending and then stores it in the `challengeableTransfers` array. Note that the initial double-spending checks on `objectiveTransfer()` calls only check for double-spending against the address’ finalized balance. The protocol also checks for double-spending again when `cleanChallengeWindow()` is called [see below], where the total amount spent in all challangeable transfers are combined and *then* checked against the finalized balance.  The core contract can finalize the transfer once the active challenge period ends. Any address can call the `cleanChallengeWindow()` method, which will attempt to execute and delete all challengeable transfers that it can finalize. At this point, the transfer is complete.

Any address can call the `challengeAndRecord()` method on a core contract, which, given one or more transfers, will check them alongside all challengeable transfers for double-spending. If this process detects double-spending (the total amount of tokens transferred from one address in the challenge window period exceeds its balance), it will mark all challengeable transfers originating from double-spending addresses as problematic. During the `cleanChallengeWindow()` call, the core contract will delete but not execute problematic transactions.

These rules create a system that:

- Only needs one honest relay.
- Prevents double spending.
- Maintains consensus between deployments.

But at this point, the protocol isn’t very useful.

*Part IV: Cross-chain*

There’s a surprisingly small gap between Part III and a cross-chain token. Because the isolated cross-deployment solution doesn’t require contracts to interact with each other, each deployment doesn’t need any awareness of or connection to any other deployments. **They could be on entirely different blockchains, and the protocol would still function.** We could deploy one instance on each network we want to connect to. Then, when an address initiates a transfer on one chain, relays will replicate it on every other chain.

A trustless exchange contract repackages the protocol into a more familiar form, where EOA addresses can transfer assets from one chain to another. This works by utilizing the swapon-sync-swapoff model, which functions as follows:

1. Swap an ERC20 token on the source chain for the cross-chain token.
2. Wait for relays to sync cross-chain balances.
3. Swap the cross-chain token for an ERC20.

However, standard liquidity pools like Uniswap can’t swap ERC20 tokens for cross-chain tokens. Instead of relying on the traditional model, we must take an orderbook-like approach.

For sellers:

1. Deposit the ERC20 token into the exchange contract, specifying a price level for the trade.
2. Wait for a buyer to fulfill the order.

For buyers:

1. Fetch unfulfilled trades for the specified price level.
2. Create and sign transactions to transfer the cross-chain token to the appropriate sellers.
3. Send the transactions and signatures to the exchange contract, which will verify them.
4. The exchange contract executes cross-chain token transfers using objectiveTransfer() calls.
5. The exchange contract releases sellers’ deposited funds to the buyer.

This design allows for a standard asset bridging interface between blockchains.

*Conclusion*

This protocol enables trustless cross-chain asset transfers using a standardized interface. It would also be possible to expand the protocol to execute arbitrary transactions on an EVM instance. This expanded version of the protocol could be the first step in building a class of blockchain that integrates a vast array of networks into its fundamental design, enabling trustless interoperability between all Ethereum-based blockchains in existence. It would be similar to an L2 blockchain in the sense that transaction data is stored onto another blockchain, but different in the sense that it stores data on multiple blockchains all at once to enhance interoperability.

By itself, this system is not very scalable. High fees are expected as there are multiple transactions required per transfer. However, this issue can be mitigated by either only using L2 networks to store transfer data or building L3s on top of the protocol. Alternatively, transactions could be bundled and their Merkle root submitted onchain alongside a ZK proof in a manner similar to that of a zero-knowledge rollup. In this way, multiple objective transfers could be submitted in only a few transactions.

Finally, any and all feedback is welcome! The project is in its very early stages but I’ll attach the Github repository once I’ve made some more progress.
