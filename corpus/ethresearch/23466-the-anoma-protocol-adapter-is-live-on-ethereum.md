---
source: ethresearch
topic_id: 23466
title: The Anoma protocol adapter is live on Ethereum
author: cwgoes
date: "2025-11-18"
category: Architecture
tags: []
url: https://ethresear.ch/t/the-anoma-protocol-adapter-is-live-on-ethereum/23466
views: 547
likes: 10
posts_count: 1
---

# The Anoma protocol adapter is live on Ethereum

#### Summary

- We’ve just deployed the Anoma Protocol Adapter to the Ethereum main chain (contract address).
- The protocol adapter implements the Anoma state model, which we call the Anoma Resource Machine (ARM), such that Anoma transactions can be executed (settled) on Ethereum. You can see an example transaction here.
- With this deployment, developers can now write Anoma applications which leverage the principal affordances of the resource machine – native intents and privacy – and use those applications on Ethereum.
- This deployment of the resource machine leverages RISC0’s zkVM, and applications can be written in Rust.
- The protocol adapter and RISC0 resource machine have been audited by Informal Systems and Nethermind. You can find the audit reports here.
- The protocol adapter itself is fully open-source and deployment is permissionless, so developers can also deploy the protocol adapter contracts to other EVM chains, making them compatible with Anoma applications.

#### What’s the Anoma Resource Machine?

The Anoma Resource Machine (ARM) defines Anoma’s state model and transaction semantics. An analogy may be helpful: the resource machine is roughly to Anoma as the EVM is to Ethereum. The design of the resource machine, however, is quite different.

The EVM bundles together three distinct design choices: an instruction set for performing computation (ADD, MUL, etc.), a state architecture (contracts with independent storage), and a message-passing execution model (execution starts in a contract and moves when a message call is performed). The resource machine, by contrast, specifies only a state architecture.

The resource machine’s state architecture is – as suggested by the name – based on units of state called *resources*. Compared to smart contracts, resources are simpler, smaller, and immutable. Ethereum applications typically use only a small number of mutable smart contracts, but Anoma applications may use millions of immutable resources. While smart contracts specify how state transitions are *computed*, resources only specify how state transitions are *verified* – they can be computed in any way which results in a valid transition. This means that applications written for the resource machine are intent-centric by default, since solvers or other off-chain parties can compute transitions in any way which will satisfy the requirements of the resources involved.

Smart contracts are mutable: once you deploy a smart contract, it can be called many times, and each time you call it, the state may change. By contrast, resources are immutable: a given resource can be created and consumed only once. Mutable-like behavior can be obtained with a sequence of resources that share some common identity. Resource creation and consumption is tracked using commitments and nullifiers: when a resource is created, the resource’s commitment is added to a commitment tree, and when a resource is consumed, the resource’s nullifier is added to a nullifier set. Transactions check that no resource is consumed twice by checking that any nullifiers revealed are not already present in the nullifier set.

This aspect of the state model is inspired by the commitment/nullifier system originally pioneered by the Zerocash paper and Zcash, and allows resource machine transactions to be privacy-preserving. More fine-grained programmable privacy can be obtained by splitting state into different resources with different rules for which parties must be able to read which resource (enforced with verifiable encryption).

A more comprehensive design overview can be found in [this paper](https://zenodo.org/records/10689620).

#### What does the resource machine bring to Ethereum?

With the Anoma protocol adapter, developers can use the resource machine abstractions to write Anoma applications benefiting from native intents and privacy, and use those applications with existing state and infrastructure in the Ethereum ecosystem. The Ethereum community has demonstrated a clear [commitment to privacy](https://vitalik.eth.limo/general/2025/04/14/privacy.html), but the design of the EVM itself is incompatible with privacy, and refactors substantial enough to make it compatible would require that applications be re-written anyways.

The resource machine is not a roll-up or a layer two, although those sorts of constructions could potentially be built *using* it. Rather, it’s a different state architecture built to be compatible with intents and privacy by default. Migrating applications to new state architectures takes a long time, so we build the protocol adapter in a way which allows developers to write applications that interoperate across both resource machine and EVM state (using forwarder contracts).

The combination of the resource machine and the existing Ethereum ecosystem makes many new applications possible. Here are just a few I’d be excited to try out:

- A privacy-preserving trading application which stores user tokens as resources (shielded), but leverages Uniswap pool liquidity for swaps, so that users can gain privacy without compromising on liquidity.
- A privacy-preserving version of Gitcoin (we call this idea Public Signal), which allows users to craft conditional commitments to support projects if certain conditions are met, where those conditions are kept private.
- A dark pool for structured financial products, where collateral is kept locked in resources, released only under specified conditions. Think: Hyperliquid without public liquidation thresholds and with real Ethereum security.

We’re working ourselves on AnomaPay, an application that aims to bring easy-to-use privacy-preserving payments to Ethereum and any EVM chain where the protocol adapter is deployed. You can expect more news on AnomaPay soon!

Thanks for reading!
