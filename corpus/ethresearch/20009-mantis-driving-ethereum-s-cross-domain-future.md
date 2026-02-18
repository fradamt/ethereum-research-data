---
source: ethresearch
topic_id: 20009
title: "Mantis: Driving Ethereum’s Cross-Domain Future"
author: 0xBrainjar2
date: "2024-07-08"
category: Applications
tags: []
url: https://ethresear.ch/t/mantis-driving-ethereum-s-cross-domain-future/20009
views: 2146
likes: 1
posts_count: 1
---

# Mantis: Driving Ethereum’s Cross-Domain Future

Author: [0xbrainjar](https://x.com/0xbrainjar)

Reviewers: [Sydney Sweck](https://x.com/ComposableSyd) & [Bruno Mazorra](https://x.com/0xBrMazoRoig)

# Summary

Recently, Composable [launched its IBC Ethereum mainnet connection](https://twitter.com/Picasso_Network/status/1775512007963500772). The [IBC Protocol](https://www.ibcprotocol.dev/) is emerging as the gold standard for cross-chain communication, as we have previously explored in our comparison analysis [here](https://medium.com/@Picasso_Network/ibc-as-the-end-game-of-bridging-a-comparison-analysis-on-trust-dcc01e0d9377). IBC’s trust levels parallel that of ZK bridging, which is limited to the Ethereum ecosystem and its layer 2s. Originally, the IBC Protocol was also limited to one ecosystem: the Interchain, which includes Cosmos SDK chains and the Cosmos Hub. However, IBC has now been expanded outside of the Interchain/Cosmos ecosystem for the first time by Composable’s Picasso Network.

IBC Ethereum a significant milestone, marking the first time that trust-minimized bridging is available between Ethereum and other IBC-enabled chains including the Cosmos hub, Cosmos SDK chains, Polkadot and Kusama parachains, Solana, and more ecosystems soon. Moreover, this was a huge technological feat, given that this connection required architecting a light client on Ethereum. While various projects were exploring the concept of Ethereum light clients at the time, there were no light clients fully available on Ethereum when we began development.

Now, Composable is in the process of launching a product that aims to bring more utility to cross-domain Ethereum operations: Multi-chain Agnostic Trust-minimized Intent Settlement, or Mantis. This framework serves as a vertically integrated intent pipeline, complete with expression, execution, and settlement. Ultimately, Mantis strives to establish a decentralized market for cross-domain intent expression through a permissionless solver network and intent-settlement framework. Through Ethereum IBC and now Mantis, Ethereum will be optimally positioned to continue in its role as the leading hub of DeFi; new cross-chain use cases to and from Ethereum will be generated, enabling the flow of new liquidity and users to Ethereum, with all of the complexities abstracted away to improve the user experience.

The present article thus summarizes Mantis from our recently-published Mantis Whitepaper and Litepaper. Moreover, this post details how Mantis can benefit Ethereum and other IBC-enabled ecosystems.

# About Mantis

## The Industry Need

Mantis is a relevant protocol within the present DeFi space for a number of reasons, as it aims to fulfill a number of challenges currently facing the space:

- Optimizing UX and Execution: There has always been a need in the space to optimize both user experience (UX) and execution. If this is accomplished, capital efficiency and value accrual can be maximized for all participants.
- Combatting Centralization Trends: In the multi-chain bridging space, there has been an increased reliance upon centralized structures. Unfortunately, there has been a lack of decentralized solutions that rival the speed and cost of centralized structures.
- Facilitating Trust-Minimized Interoperability: Many bridging structures in place today require putting trust in third-party intermediaries, making them vulnerable to attack. However, new technologies are being introduced with the launch of trust-minimized bridging structures like the IBC Protocol, which powers the Picasso Network. These developments enable generalized message passing and synchronization of protocols and applications across multiple blockchain ecosystems.
- Delivering Intent-Centricity: Intents are another new area of development in the DeFi space that are positioned to further assist in resolving user experience and execution issues. However, many intents solutions are not cross-chain interoperable, and are not vertically integrated with execution and settlement solutions, rendering them unable to accrue value from pay for orderflow.

With Mantis, Composable addresses these present unmet needs in the DeFi space. Overall, our thesis is that cross-domain interoperability widens the intent solution space. We hypothesize that this increased choice in solutions results in value in the form of better user outcomes.

## Architecture

Mantis accomplishes its functionalities via the Mantis protocol and rollup, a cross-domain auction mechanism, as well as their synergies with the Inter-Blockchain Communication (IBC) Protocol and the Picasso Network. Moreover, a commitment mechanism between chains allows conditions in the other parts of the architecture to be carried out cross-domain.

### The Mantis Protocol & Rollup

The Mantis protocol facilitates optimal execution of cross-domain intents via a competition of solvers. Users sign intents, which are contained on a private rollup mempool. Solvers are staked agents that can a) observe the transactions on the mempool and b) post solutions in the auctioneer contract. The auctioneer contract scores the solutions in terms of users utility maximization. The winner of the auction is responsible for settling the outcome of the intent to the solution settlement contracts in the final chain expressed by the intent.

The Mantis protocol lives on the Mantis Solana Virtual Machine (SVM) rollup. This rollup serves as a coordination and settlement layer for cross-domain intents, in addition providing a framework for cross-domain block proposals and credible commitments. The rollup further allows for assets to be staked and restaked to provide crypto-economic security along the proof-of-stake model. This includes staking both the native token of Solana (SOL) as well as liquid staked token versions of SOL. These assets are staked into the bridge contract of the rollup, which then sends them to the proper place for staking or restaking.

The Mantis rollup also provides developers with a simplified mechanism for designing cross-domain decentralized applications (cdApps), which are defined by their inclusion of scoring, solvers, solution settlement, and cross-domain integrity proofs. An SDK is provided to further enhance the development and integration process.

### Cross-Domain Auctions

Mantis plans to introduce cross-domain combinatorial auctions, with the goal of accomplishing the following:

- Optimized cross-domain MEV extraction*
- Cross-domain intent solution atomic settlement
- Efficient blockspace allocation
- Increased distribution of revenue to validators selling items separately

*We would like to take a moment here to reflect on MEV and our goals surrounding this concept. MEV is an evolving term with a number of interpretations. Initially MEV stood for miner extractable value, representing the maximum profit an agent (miner or validator) in proof-of-work blockchain systems could incur from its monopolistic rights over transaction inclusion. With the advent of proof-of-stake systems, MEV has become more often described as maximal extractible value, as miners are largely obsolete. Maximal extractible value still refers to the value that agents derive from strategically reordering and including transactions, but now these agents are frequently searchers.

A number of negative ramifications have been reported from these MEV extraction mechanisms. Thus, Flashbots introduced MEV-geth to Ethereum, which implemented a centralized combinatorial auction where searchers can express complex preferences in bundles. Then, this auction system was decentralized by MEV-Boost, allowing anyone to propose their block by bidding at auction. With the introduction of proposer-builder separation, validators on Ethereum now derive value from their monopolistic power over their slots.

As one can see, value from rearranging and including/excluding transactions can now be carried out by a number of parties in a number of manners. In addition to the extraction by validators, miners, and searchers, builders can also derive profits and users themselves can derive financial benefits from these mechanisms by using protocols such as Flashbots Protect, MEV blocker and Cow Protocol . Therefore, it becomes difficult to define exactly what value accrual mechanisms can be considered MEV.

Another complicating factor in the definition of MEV is that some of the aforementioned value accrual mechanisms have an inverse relationship. Most importantly, there is tension between the profits made by validators and other sellers from MEV and the overall welfare of the system (i.e. total value accrued to all users of the system, including end users, solvers, searchers, stakers, etc.). When overall profits to sellers are maximized, overall welfare goes down.

Thus, the goal of Mantis is not necessarily to maximize MEV extraction. Rather, the goal is to maximize overall welfare.One way in which we hope to achieve this is via our mechanisms designed to allocate blockspace efficiently to the users valuing it the most, such as our cross-domain auctions.

Initially, these auctions will be just-in-time to allow builders to express atomically. For two domains, this will involve two simultaneous English auctions with a unique combinatorial block take-it-or-leave it offer. Buyers can place send blocks with bids for the independent blocks and combinatorial blocks. The problems with this approach are the risk of double-signing and the high level of trust placed in the relay.

Therefore, Mantis aims to later introduce a future combinatorial blockspace market, where the rights to future blockspace on multiple domains can be bought and sold. The new crypto-economic primitive of restaking (such as that being facilitated by the Picasso Network) enables block proposers to issue credible commitments about future block construction. These are promises to build blocks in accordance with specific conditions laid out by execution ticket holders if certain payment thresholds are met. Tickets exist outside of a domain’s consensus protocol and will be exchanged via a combinatorial batch auction where buyers express combinatorial valuations over the tickets and sellers express reserve prices. Then, tickets can be traded or sold in a secondary market. This aims to decrease the monopoly of block sellers while increasing market efficiency.

### The IBC Protocol

The [IBC Protocol](https://www.ibcprotocol.dev/) facilitates communication between different blockchain ecosystems. [Compared to other cross-chain communication protocols](https://medium.com/picasso-network/why-ibc-everywhere-is-the-key-to-cross-chain-defi-041bed829acd), the benefits of IBC are that it is [trustless](https://medium.com/@Picasso_Network/ibc-as-the-end-game-of-bridging-a-comparison-analysis-on-trust-dcc01e0d9377), secure, censorship-resistant, permissionless, fast, cost-effective, and natively interoperable. For these reasons, Mantis has opted to use IBC as its mechanism for cross-chain communication.

Composable has expanded the reach of the IBC so that it not only connects the [Cosmos Hub](https://hub.cosmos.network/) and [Cosmos SDK](https://v1.cosmos.network/sdk) chains that it originally linked, but also interoperates with [Polkadot](https://polkadot.network/) and [Kusama](https://kusama.network/) parachains, [Ethereum](https://ethereum.org/en/), and [Solana](https://solana.com/). Creating these novel connections required a significant amount of technical development, given that many blockchains lack different components needed for IBC-compatibility.

In the case of Ethereum, the following components needed to be architected in order to enable IBC-compatibility:

- ZK Circuit: This program is able to output a proof given a set of inputs. This proof can then be easily verified to ensure that each computational step that was run inside the circuit was done so correctly. In Picasso’s solution, the ZK circuit connects SNARK ED-25519 signatures to a prover. ED-25519 is a digital signature algorithm (DSA) that offers small key and signature sizes and fast computation being impervious to many common attacks to other DSAs.
- Tendermint Light Client on Ethereum: We constructed a Tendermint light client on Ethereum, which lives as an Ethereum smart contract and is able to communicate over IBC with the light client on Picasso.
- Ethereum Light Client on the Picasso Chain: We also created a CosmWasm contract in the Wasm client of the Picasso Cosmos SDK chain to complete the Ethereum IBC connection.
- IBC Stack on Ethereum: We created a modified IBC stack for Ethereum that consists of Solidity smart contracts on Ethereum. Through this IBC stack, all BC components can operate on Ethereum, facilitating Ethereum’s interoperability with IBC.
- Hyperspace Relayer: The Composable Foundation’s Hyperspace relayer connects the two light clients involved in Ethereum IBC by transferring IBC packets between them. Hyperspace is the first event-driven, chain-agnostic IBC relayer that is based on ibc-rs (the Rust implementation of IBC). Hyperspace can thus relay packets between any IBC-enabled chains.
- Prover: This entity interacts with the relayer and proves to the verifier that something is true without revealing other information. On Picasso, what is being proved is various transactions sent between Ethereum and IBC. In particular, this prover is a rapid SNARK prover living on the Picasso Cosmos SDK chain.
- Verifier: Verifiers receive a proof from provers and validate this claim. This prover-verifier relationship results in the production of zero-knowledge proofs, as Ethereum explains here.

### The Picasso Network & Its Restaking Pool

The [Picasso Network](https://picasso.xyz/) aims to deliver ecosystem-agnosticism to DeFi. It executes on this vision via the Picasso Layer 1, a Cosmos SDK blockchain that acts as an IBC hub between Cosmos and non-Cosmos IBC-enabled chains.

Picasso is the first censorship-resistant, natively-secured cross-ecosystem interoperability solution. The Picasso Network further emphasizes trust-minimization by drawing on the trustless IBC protocol. While a multisig is initially being used for upgradability of IBC contracts on Picasso, the end goal is to transition to decentralized governance.

Picasso is a critical component of Mantis as it allows the Mantis framework to be cross-chain capable over IBC. Specifically, Mantis transactions are grouped into IBC bundles for shipment based on domain. These bundles are then sent from the Mantis rollup over Picasso IBC and out to relevant blockchains for settlement.

Moreover, a restaking pool on Picasso coordinates the agents that have a combination of stake in different chains. Commitments formed between these actors draw upon this restaking pool.

## Development Roadmap

The development for Mantis will be carried out in the following steps:

1. Enabling cross-domain swaps: integrating with IBC bridges and automated market makers across different chains to facilitate seamless asset swaps
2. Setting up the foundational architecture: establishing a robust framework that includes the initial design of the Mantis architecture and the development of standards for scoring mechanisms and IBC for intent-based mechanisms
3. Implementing cross-domain intent-based mechanisms: developing application programming interfaces (APIs) and software development kits (SDKs) that enable users to create and manage cross-domain intents, along with implementing an open-source solver that solves these intents
4. Enriching the restaking layer: building out the restaking layer of Mantis to have additional functionality (simultaneously to step 3)
5. Creating cross-domain MEV auctions: developing an auction system that efficiently allocates blockspace (simultaneously to step 3)
6. Deploying block proposal commitments: enhancing the infrastructure for block proposals and establishing a credible commitment mechanism across domains, including robust fraud-proof mechanisms to maintain trust and security.
7. Completing public launch and scaling: focusing on officially releasing all functionalities and documentation for Mantis

# Benefits to Ethereum

Mantis supports Ethereum’s continued role as a leader in DeFi as the space becomes increasingly cross-chain. Composable has already connected Ethereum to the IBC, and therefore, to our trust-minimized bridge. This connection will drive new usership and liquidity to Ethereum from Solana, Cosmos, Polkadot, and Kusama. It will also enable the development of new use cases for ETH outside of Ethereum and on these other networks. Through such new use cases in new locations, DeFi users who do not currently hold ETH will likely be incentivized to do so, and existing users may be incentivized to hold more ETH. Thus, the Ethereum network is positioned to expand its reach even further into the cross-domain DeFi landscape, helping the ecosystem to maintain its reputation as a leader in the space.

Another benefit Mantis aims to deliver is chain abstraction. Mantis provides a mechanism for Ethereum and other domains to easily be participants in cross-chain DeFi without the blockchain, its layer 2s, or any protocols in the ecosystem needing to make significant modifications. Now that Ethereum is integrated with IBC, its innumerable DeFi protocols and applications can be leveraged from within Mantis. A user simply puts their intent for a transaction into the Mantis user interface, and the rest is handled for them. For example, A user may be looking to swap ETH for USDC. Once they input this intent, Solvers on Mantis compete to come up with the best execution route. For the sake of this example, perhaps the best price for this swap is through an ETH-USDC pool on Uniswap. The solver who has proposed the best settlement route wins the rights to settle the solution, routing the funds through Uniswap for the swap, and then back to the user. Once the transaction is settled as specified, the solver is rewarded. In this manner, all parties benefit: new traffic is routed through Uniswap in this example (or more generally, any other protocol or protocols providing best execution), the user has a streamlined experience with optimized settlement, and the solver is rewarded for their role.

# Conclusion

Mantis provides the architecture needed for IBC-enabled chains like Ethereum to easily participate in the cross-domain future. This will help Ethereum continue its role at the forefront of DeFi as the industry continues to embrace multi-domain operations.

# References & More About Composable

Composable is dedicated to improving DeFi’s accessibility, quality, transparency, efficiency, and security. Our ultimate vision is for the Composable ecosystem to become an execution hub for chain-agnostic transactions. We are actualizing our mission by working to unite the DeFi space, building an ecosystem and a range of infrastructure to support trustless cross-chain operations.

- Mantis Whitepaper
- Mantis Litepaper
- Mantis app
- Composable website
- Composable X/twitter
- Composable Discord
- Composable Telegram
- Composable GitHub
