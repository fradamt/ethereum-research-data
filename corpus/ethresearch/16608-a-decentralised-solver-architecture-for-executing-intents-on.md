---
source: ethresearch
topic_id: 16608
title: A decentralised solver architecture for executing intents on EVM blockchain
author: rishotics
date: "2023-09-13"
category: Economics
tags: [account-abstraction]
url: https://ethresear.ch/t/a-decentralised-solver-architecture-for-executing-intents-on-evm-blockchain/16608
views: 12404
likes: 48
posts_count: 22
---

# A decentralised solver architecture for executing intents on EVM blockchain

by [@nlok5923](/u/nlok5923) [@hawk](/u/hawk)

*Special thanks to [Alex](https://twitter.com/alexanderchopan) for the helpful discussions and feedback that were instrumental in making this article possible.*

### TL;DR

- Blockchain user intentions, or ‘intents,’ lack a standardised framework for efficient solver collaboration in Ethereum
- This article introduces Abstracted Transaction Objects (ATOs) to capture operation-specific information and optimise user intents.
- A trusted driver manages ATO bundles and broadcasts them to a diverse solver network, each specialised in different domains.
- Solvers generate scores based on user-specified or operation-specific fields, and the winning solution is determined by Degree of Expectation (DoE), a quantitative measure.
- Collaboration among multiple solvers ensures optimal solutions, censorship resistance, and system availability, driven by reputation scores.
- Solver incentives include transaction fees, prepaid balances, and an intent execution module integrated into smart contract wallets for streamlined transactions and automated solver rewards.

---

## Current Scenario

In the blockchain realm, user intentions, referred to as ‘intents,’ take on diverse forms, including DSL expressions, natural language, actions, conditions, and restrictions. An intent captures how users envision specific transaction actions. For instance, a common example is choosing ‘Same day delivery’ for an Amazon order. The incorporation of Account Abstraction([ERC 4337](https://eips.ethereum.org/EIPS/eip-4337)) extends the range of these expressive possibilities.

At present, there is no established architecture for solvers in the Ethereum ecosystem to collaborate and coordinate their efforts. The existing solver ecosystem operates in isolation, resulting in limited solver visibility and complicating the user’s process of discovering suitable solvers for their intent fulfilment.

The MEV extraction thats taking place in the DeFi protocols is increasing and with flashbots new solution SUAVE does provide a way to mitigate this but those approaches are quite farsighted and depends on adoption. This leaves the users in the light of increasing loss of funds in the form of MEV. The MEV captures can be further be reduced by leveraging solver collaboration and facilitating data sharing among solvers which would introduce counter party discovery and could lead to potential coincident of wants.

Ethereum, as a stateful blockchain employing a Virtual Machine (VM), faces a key impediment to implementing this architecture within the EVM. This obstacle lies in the transaction construction process. In the Ethereum ecosystem, transactions adhere to a deterministic approach, capturing only a limited set of information required to effect a state change. This design resists further optimization. In contrast, Intents aim to capture users’ desires, subsequently translating them into optimized transactions by solvers, thereby offering greater flexibility and value to users.

In order to align Intents with the EVM, we are introducing a novel structure known as **Abstracted Transaction Objects (ATOs)**. ATOs exclusively capture information relevant to a specific operation. Solvers leverage this information to construct optimized transactions tailored to the operation’s requirements.

### Tentative ATO structure

```auto
{
"operation": ENUM,
"fieldsToOptimize": hex,
"fieldsToOptimizeSchema": string,
"chainId": number,
"payload": hex,
"payloadSchema": string
}
```

The fieldToOptimize field contains the fields for an operation which are necessary for score optimization in an encoded form. Score converts the solution of a solver into quantitative value which can be used by the driver to evaluate and compare the solutions received from different solvers. fieldToOptimizeSchema contains the schema followed for decoding the fieldToOptimize field. chainId is the chain Id of the chain on which the user want to executes the intent. payload is the extra information apart from fieldToOptimize to convert that ATO into a valid transaction by the solver in an encoded format. payloadSchema contains the schema followed for encoding the payload field. The Intent(I) captured at application level can be composed of n ATO’s, which might correspond to same operation more than once. Theoretically n can go till \infty but in practical case scenarios it would be some definitive number.

I = [ATO_{1}+ATO_{2}+........+ATO_{n}]  \;\;n \in[1,\infty)

These ATO’s can be presented in the form of a private manner where information is hidden and executed in such a way that the user doesn’t reveal any information to the public blockchain.

## Managing Abstracted Transaction Objects (ATOs): The Role of the Driver in Intent-Driven Architecture

[![efw](https://ethresear.ch/uploads/default/optimized/2X/b/ba098e6ab88b189d168b9c41de99e9a1f0adcaaa_2_690x348.png)efw3812×1924 143 KB](https://ethresear.ch/uploads/default/ba098e6ab88b189d168b9c41de99e9a1f0adcaaa)

The driver plays a pivotal role within the infrastructure, serving as a trusted party with several key responsibilities:

1. ATO Broadcasting: The driver is tasked with broadcasting Abstracted Transaction Objects (ATOs) to the mempool, where all the solvers can initiate their execution processes to find optimal solutions.
2. Simulation and Verification: It receives solutions from all the solvers, conducts off-chain simulations to ensure their validity and security, and subsequently posts the winning solution.
3. Aggregation of Solutions: For a given Intent, the driver aggregates solutions from different ATOs, combining them into a unified execution plan for final implementation.

### ATO Bundling and broadcasting

[![ATO ordering and bundling](https://ethresear.ch/uploads/default/optimized/2X/8/89b372db426bbc2f37e7d607a52c493325b52500_2_690x397.jpeg)ATO ordering and bundling1600×921 96.6 KB](https://ethresear.ch/uploads/default/89b372db426bbc2f37e7d607a52c493325b52500)

The driver efficiently manages bundles of Abstracted Transaction Objects (ATOs) with each bundle focusing on resolving a single user intent. In the case where the intent corresponds to a single action, the driver can also receive a single ATO.

Upon receiving these bundles, the driver undertakes the following tasks:

**Parallel Ordering:**

The driver performs parallel ordering of ATO bundles, to start extracting and bundling ATOs to broadcast.

**Bundling ATOs:**

It bundles the first ATO from each bundle based on their operation type. For example, if there are four bundles of ATOs, two of which have a swap operation as their first ATO, and the other two have a bridge operation as their first ATO, the driver will broadcast two bundles, one for the swap operation and one for the bridge operation, to their respective solvers. This organised approach streamlines the ATO distribution process to the solver network.

For the first ATO in each bundle, no new state information is required, as the solver can utilize the current blockchain state to find the optimal solution for that specific ATO.

The driver follows a structured process. For the initial ATO’s of the bundle, it doesn’t require additional state information, and the solver can proceed with the available blockchain state.

However, for subsequent ATOs in the bundle, the driver collects the corresponding solutions from all the previous ATOs before bundling the next set of ATOs. This ensures that the solver has updated state information before solving the new ATO, as some fields may depend on the information from preceding ATOs.

In essence, the driver maintains a continuous cycle for every non-initial ATO. Before broadcasting it, the driver ensures it has the winning solutions for all preceding ATOs, facilitating an organised and synchronised approach to solving user intents.

## How the Solver Network Enhances the Intent-Driven Architecture?

A solver is a participant within the context of this system. It operates within a solver network, a collective repository of diverse solvers, each specialising in distinct domains. Individuals with these pre-requisites can be a solver:

- Valid ethereum address: Individuals with valid wallet addresses can partake in this ecosystem by registering themselves as solvers through a dedicated smart contract.
- Domain Experts: These solvers are equipped with specialised code tailored to solve specific types of ATO for a particular operation (swap, bridge, stake etc). For example a solver specialising in derivative trading
- Win the DAO voting process: Remarkably, the selection process for solvers extends to decentralised autonomous organisations (DAOs), where members can exercise their voting rights to determine the inclusion of a solver.

This collaborative approach ensures a diverse and expert-driven solver network, enriching the architecture’s capabilities.

While drivers facilitate the routing of client-originated ATOs to their designated solvers, a vital consideration arises in the design of solver networks. Entrusting a solitary solver with the complete authority to address all ATOs introduces several challenges:

- Optimal Solution Exploration: The absence of competition within a single solver’s domain can compromise the attainment of the best solution for an ATO. Solver networks mitigate this concern by fostering an environment where multiple solvers contribute their expertise, enabling diverse approaches to be explored and the most effective solutions to be identified.
- Censorship Resistance: The potential for a singular solver to enact censorship and selectively decline certain users’ ATOs is a concerning aspect. Solver networks circumvent this issue by distributing ATOs across various solvers, promoting fair and equitable execution without the risk of undue censorship.
- Enhanced Availability: Relying solely on a single solver presents a vulnerability; if that solver becomes unavailable, the entire protocol grinds to a halt. Solver networks avert this predicament by distributing tasks across a multitude of solvers, ensuring that the system remains operational even if certain solvers experience downtime.

### Mempool

Including multiple solvers in the system proves to be a sensible approach, capable of handling the diverse stream of ATOs originating from the driver. These solvers collectively form a solver network, collaborating to decipher ATOs and achieve the best possible solutions, an effort that earns them well-deserved rewards. Within this framework, ATOs find their home in a shared mempool, accessible to all participating solvers. Further we are planning for solver to have their own local mempools and in future we would try to enable user to directly sent their ATOs to one of the solver and from the local offchain mempools the solver which doesn’t posses expertise in solving the ATO which they have received they can share those ATO’s with their neighbour solver having expertise in solving that. Additionally their would be an auction period setup by driver by that auction period it’s the responsibility of solver to return the solution for that particular ATO failing to do so might lead to the failing of ATO solution acceptance.

## Degree of Expectation: A Quantitative Approach for Optimising Intents

The solver optimises ATOs based on user-specified or operation-specific fields represented by a set of qualities T for a particular ATO, the optimisable fields could be swap rates, percentage yield, contained in the ATO’s fieldsToOptimize field. Optimising this fields enables solvers to evaluate their solution and provide a score for their solutions, which the driver validates to prevent potential malicious score calculations by solvers.

T \subset set\;of\;user\;defined\;optimizable\;fields

d: number\;of\;default\;fields\;to\;optimise

of_{i}: optimisableField_{i} \;\;\forall \;\; i \in [1, n(T)+d] \; \;\;n(T): cardinality \;\;of\;\;set \;\;T

fieldsToOptimize: abi.encode(of_{1}, of_{2}.....of_{n(T)+d})

f_{i}:optimisableField_{i} \rightarrow fieldValues_{i} \;\; \;\;\forall \;\; i \in [1,n(T)+d]

A function f_{i} takes in optimisableField_{i} and returns a quantitative representation of the optimisation achieved for the overall ATO. The specific function for mapping the qualitative nature of these optimisableField to fieldValues will be determined through community and solver discussions and these fields may encompass various aspects such as bridge reputation and DEX slippage. If a field is not explicitly mentioned, it is excluded from the optimisation problem.

In situations where no optimisable field is explicitly stated in the Intent, default fields that can be optimised would be considered. These default fields are determined through community and solver consensus when enabling support for a new operation into the protocol

All the solvers calculate the same expression and then optimise over it. There will be a function which will represent the ***‘Degree of Expectation’ (DoE)*** which the solver is trying to optimise in **T (auction time)** time for which the ATO is valid to the solver. The DoE only contains the value which maximise the user’s expectation explicitly

DoE_{operation}\propto \frac{fieldValues_{positiveQuality}}{fieldValues_{negativeQuality}}

fieldValues_{positiveQuality}: represents the numerical Values (values received on optimising the optimisableField) of the ATO which are directly proportional to the DoE of the operation. For example this can be reputation of the bridge in a bridging operation. Basically it is the quantised representation of the fields of ATO which upon optimising providing surplus value to the user.

fieldValues_{negativeQuality}: represents the numerical values of the ATO which are inversely proportional to the DoE of the operation. for example: swapping with a fairly large slippage. Similarly it is the quantised representation of the fields of ATO which upon optimising in positive manner could results in user losses.

For  a particular ATO_{i} where ATO_{i} \in [ATO_{1}, ATO_{n}] we have solutions getting from all the solvers from [solver_{1},solver_{m}] and we represent it in the form of DoE of the solver_{j} for the$ATO_{i}$ as DoE_{solver_{j}}^{ATO_{i}}

In a more simplified way we can express it as:

DoE_{solver_{j}}^{ATO_{i}}: Degree\;\;of \;\;expectation \;\;for\;\; a \;\;particular\;\; ATO_{i} \;\;provider\;\; by\;\; solver_{j}

For a particular ATO_{i} we get all the DoEs possible from the solvers and the winning DoE for a particular ATO is defined as the maximum of all these values:

DoE^{ATO_{i}} = \max (DoE_{solver_{1}}^{ATO_{i}}, DoE_{solver_{2}}^{ATO_{i}},.......,  DoE_{solver_{m}}^{ATO_{i}})

Solver which will provide max DoE for it’s ATO would be declared as winning solver and solution corresponding to that ATO would be accepted in the final transaction bundle.

### Greedy vs DP approach

If we take the summation of all winning solutions of all the ATO_{i} forming an Intent I to calculate the Total Degree of Expectation(TDoE) of the intent we get this expression:

TDoE=\sum_{i=0}^{n} DoE^{ATO_{i}}

Currently, We are taking a greedy approach to solve the problem. In the current approach we are focused on optimising the DoE for the current ATO, For now we are not considering the implications of previous DoE over the current DoE calculations with respect to optimisations. For now we are just using the previous ATO solution to complete the current ATO’s optimisation problem.

We can understand this problem with an example:

Intent: I have 10 USDC on polygon use that and quickly give me max USDT on Gnosis.

The above example results in the formation of two ATO first would be for bridging USDC token from polygon to Gnosis quickly and another would be for swapping USDC token to USDT on Gnosis for best rates

With the current infra we are thinking that the bridge solver would solve the first ATO and come up with the solution for bridging tokens with fastest bridge but that bridge may not be providing tokens on destination chain with best rates. Although the swapping on the destination chain would occur with lowest slippage (a.k.a best rates) considering the ATO.

This in general is a relatively hard problem and at we will be first going with the greedy approach for implementation.

## Solution Simulation and Agreement

Before accepting any solution, it falls upon the Driver to simulate the solution, ensuring it aligns with the score commitment shared by the solver. It’s essential to note that both the driver and the solver operate with a shared scoring mechanism. This mutual understanding mandates the solver to initially evaluate the solution on their end. This assessment is based on the optimisation techniques employed by the solver and the state information provided by the driver. Once satisfied with the results, the solver then commits the score, along with the solution, to the driver.

Interestingly, the onus of score computation lies solely with the solver. The rationale behind this approach is to prevent overwhelming the driver with the responsibility of evaluating each ATO. Upon receipt of the solution, the driver embarks on simulating the highest-scoring solution, referencing the previous state data. If this simulation resonates with the score initially shared by the solver, the solution is heralded as the winning one. Furthermore, the solver responsible for that winning solution is subsequently marked as the beneficiary of the incentives amassed post-solving that particular intent of which that ATO was part of.

However, discrepancies might arise. If the driver’s simulation yields a score that doesn’t match the solver’s commitment, penalties will be levied on the solver who provided the solution. The driver will then proceed to simulate the next highest-scoring solution. This process of simulation and score verification continues until the driver identifies a solution that matches the originally committed score.

## Solution Acceptance and aggregation

Upon receipt of ATO bundles, the driver is tasked with appending specific tags to each ATO prior to broadcasting them to the solver. These tags play a pivotal role, enabling the driver to later discern the linkage of each ATO to its corresponding intent and its order within the bundle. Specifically, ATOs can be traced using tags like ***(bundleHash, bundleOrder).***

Here, the ***bundleHash*** represents the bundle to which the ATO belongs, while the ***bundleOrder*** indicates the ATO’s position within that bundle.

These tags subsequently guide the driver in collating all the ATO solutions into their respective bundles. Once aggregated, the driver then returns these consolidated solutions to the client, presenting them as resolutions for their specific intents.

Additionally, the solvers are held in check through a reputation score, maintained and updated on-chain via the protocol contract. This score undergoes revision with each victorious solution provided by a solver. Not only does this reputation score aid the driver in the incentivisation process for solvers, but it also serves as a performance benchmark. Should a solver’s reputation plummet below a set threshold, they risk expulsion from the system.

## Solver Incentivisation: Rewarding solver for their computation

We are exploring various strategies for solver incentivisation and have identified several potential approaches. We remain open to dialogue and welcome suggestions for alternative methods. Here are some of the methods we’re considering:

**Transaction Fee Model**

Drawing inspiration from platforms like CowSwap, this method involves providing users with an estimated transaction fee (likely determined and returned by the Driver). Based on this estimate, we can then deduct the requisite fees from the user’s initiated operation.

**Prepaid Balance System**

Envisioned as a “gas tank”, this approach allows users to deposit funds in advance, effectively prepaying for access to our infrastructure. As users initiate operations, the associated fees for solving their intents are automatically deducted from this pre-deposited balance.

**Intent Execution Module**

We propose the integration of a specialised module within the SCW. In this setup, when a user submits an intent to the driver RPC, they receive a unique hash. This hash serves as a reference linking to the addresses of the winning solvers. For on-chain execution of the intent, users must invoke the module’s function, inputting the relevant hash. The module then liaises with the driver to obtain a fee quotation. Once determined, the fee, aligning with the provided quote, is dispatched to the driver via module for distribution. Following successful fee transfer, the driver then supplies the module with the calldata for the bundled transaction for facilitating the execution.

## MSCA: Module facilitating payments and executions

We are in the development phase of a specialised [4337 compatible module](https://ethereum-magicians.org/t/erc-6900-modular-smart-contract-accounts-and-plugins/13885) designed to enhance smart contract wallets by introducing the capability of intent-based transaction execution. Many companies like [Rhinestone](https://docs.rhinestone.wtf/), [Safe](https://safe.mirror.xyz/t76RZPgEKdRmWNIbEzi75onWPeZrBrwbLRejuj-iPpQ), [Biconomy](https://www.biconomy.io/smart-accounts) etc. are designing modular smart contract wallets, and the goal will be to make it compatible with their architecture. This module is envisioned to streamline the process of executing user intents, calldata retrieval while also seamlessly integrating a mechanism for solver incentivisation. Here’s a breakdown of the pivotal roles and functionalities the module aims to offer:

1. Module Activation:

Upon activation, the module will signal that the associated smart contract wallet is now equipped to support intent-based transaction execution. This declaration serves as a green flag for external entities, ensuring compatibility and readiness for intent-based interactions.
2. Quotation and Fee Handling:

The module will incorporate predefined methods that facilitate the retrieval of fee quotations necessary for intent resolution. Before the intent’s execution, module will automatically deduct the quoted fee from the smart contract wallet’s balance. Subsequently, this amount will be channeled to designated driver contracts, serving as an incentive for solvers.
3. Intent Execution:

One of the core functionalities of the module is to actualise the execution of user intents. This encompasses processing the intent, converting it into actionable transactions, and ensuring their proper execution using the method exposed by the module.
4. CallData Retrieval:

To ensure the accurate and complete realisation of user intents, the module will possess the capability to gather the necessary calldata for the user intent from the driver.

# Conclusion

In this exploration of our intent-based architecture, we have examined various components, including the solver network, mempool, the representation of intents as ATO, and the nuances of solver incentivisation, among others. While we have mapped out certain aspects, there are still elements, such as the mechanisms for incentivisation and solution evaluation, where the finer details are under deliberation.

In future, the proposed solution can be integrated in various ways, contingent upon the ATO generation method. At the heart of our infrastructure lies the ambition to aggregate diverse constructs—be it liquidity, tokens, or data—across multiple domains. By integrating a wide range of solvers, we aim to handle an expansive variety of operations, ensuring a seamless and efficient experience for the end-user.

One should take into account that this document might potentially possess some inaccuracies, as its main purpose lies in community feedback.

*Feel free to reach-out to us on telegram @creator5923 and @**rishotics** for further discussion*

## Replies

**sk1122** (2023-09-14):

Nice approach!

Who is the driver here? From the points, its seem that driver can slash/penalize solvers for wrong answers, but it also seems like a centralized piece of tech, could you elaborate more on that?

Auction is very necessary for any kind of decentralization of intents, how are you going to approach this, will this be on some EVM blockchain or totally happening inside the driver?

---

**ankurdubey521** (2023-09-14):

This is really interesting, I had a few questions:

1. Which entity is responsible for converting the User Intents to ATOs? What happens if this entity is malicious and generates invalid ATOs.
2. While calculating the DoE, it looks like all fields are currently given equal weightage. If this is correct, than this would assume that all fields are normalised, which might not hold in practice. Also, some fields may be more important than others - for example the user may care about the reputation of the bridge used, but not as much as the slippage.
3. How does the system account for the possibility of multiple pathways to resolve an intent?  Say for a cross chain swap depending on the liquidity distribution, bridging->swapping could be more optimal than swapping->bridging. These two pathways would have their ATOs swapped, in this case how would the DoE^{ATO_i} calculate behave?

---

**nlok5923** (2023-09-14):

Hi [@sk1122](/u/sk1122),

In the very initial iteration, we planned to proceed with the driver approach, as it’s a proven method used by few of the protocols for managing order flows. Essentially, the Driver would function as a DAO-governed entity for off-chain management of ATOs, Additionally, serving as the trusted entity for verifying and validating solutions.

Now, onto the second query. I completely agree that an auction-based mechanism for task completions would be beneficial. We drew inspiration from SUAVE’s preference management mechanism, where executors bid to complete user preferences. This concept will likely be incorporated in future iterations. However, for this very first iteration, our goal is to abstract away the complexities of the mechanism from the solver’s end, keeping it as simple as possible to lower barriers to participation in the network.

---

**chiragagrawal9200** (2023-09-14):

This is a very good research! The topics covered here are very good and explained in a very simple way.

---

**rishotics** (2023-09-14):

can be taken care by the client. One possible approach we experimented at ETH Paris was using LLMs which can be fine tuned for a set of N actions. Additionally you can attach a Snark proof to the ATO generation.

1. Weight will only be given to the fields which are being expressed by the user. So a rough expression might be:

DoE_{operation}= \sum w_{positiveQuality}. fieldValues_{positiveQuality} - w_{negativeQuality}. fieldValues_{negativeQuality} + default

where  \;\;w\in\{0,1\}

The exact expression for DoE calculation will be highly dependent upon the operation.

1. Some thoughts have been mentioned some thoughts above: link. The global maximum for a particular Intent is dependant on the feedback the ATO generation receives from solvers for a particular intent. Currently these components are not connected and independent so might not get the maximum DoE but will get a local maxima.

---

**ankurdubey521** (2023-09-14):

Thanks for the explanation! Do you think representing the ATOs as a DAG with edge weights \propto \dfrac{1}{DoE_i} then applying a shortest path algo could be a potential solution?

---

**jacobdcastro** (2023-09-14):

This seems super promising! Thanks for all the thought you’ve put into this, and accelerating the EVM intent space. I have a few questions:

1. The driver seems a bit opinionated and centralized. What exactly is it? Can anyone build a driver implementation with different ordering algos?
2. How does the driver’s role differ from SUAVE’s MEVM smart contract mechanisms?
3. How do solvers guarantee block inclusion for the client? Will txns be routed through MEV-boost, or through private order flow?
4. How do you plan on deciding which solver reward mechanic to use? Is there a way to implement many reward solutions here, and/or allow solvers to create/enforce their own reward mechanisms depending on order type specialty?

---

**paul0x741** (2023-09-14):

Thanks for publishing this research! I have a couple questions:

1. One thing I’m thinking about is how expressive an intent can be on conditional criteria for example can they express preferences on mempool data? Would the driver need to wait for that data to be finalized? How would that affect the DOE calculation?
2. If a solver has access to private orderflow and can get better execution how would the driver verify that?
3. You say that this yields enhanced availability of solvers but what about the driver?
4. How does the Intent Execution Module work, does the user need to manually verify the solution for onchain execution?

---

**rishotics** (2023-09-14):

Thats an interesting anology! If I get it then each node will be a state s_{k} starting from s_{i} till final state s_{f} where an ATO_{k} can lead a state change from s_{k} \rightarrow s_{k+1}.

[![Screenshot 2023-09-15 at 12.47.33 AM](https://ethresear.ch/uploads/default/optimized/2X/4/415386814c7e2710f8ac49a3bfaa70665f79c817_2_309x375.png)Screenshot 2023-09-15 at 12.47.33 AM578×701 17 KB](https://ethresear.ch/uploads/default/415386814c7e2710f8ac49a3bfaa70665f79c817)

One issue might be the discovery of the entire state graph for optimising, as a particular state can lead to multiple states. But if the state graph is known then we can choose the shortest path for a potential solution.

---

**nlok5923** (2023-09-15):

Thanks for contributing [@jacobdcastro](/u/jacobdcastro)

> The driver seems a bit opinionated and centralized. What exactly is it? Can anyone build a driver implementation with different ordering algos?

The driver in this architecture is managed and governed by the solver DAO. We retained the driver for the initial iteration of this architecture to place a stronger emphasis on the solvers’ end of the structure. Certainly, our roadmap includes plans to make it increasingly permissionless and decentralized. We are indeed considering the possibility that, in the future, anyone could code their own logic for ATO distribution among solvers. Since an intent comprises multiple ATOs, the routing and distribution of these ATOs also present an optimization challenge. Better approaches from the community could enable quicker resolution of the ATOs.

> How does the driver’s role differ from SUAVE’s MEVM smart contract mechanisms?

In SUAVE’s MEVM, smart contracts are primarily used to construct builders, relays, and searchers. These entities mainly deal with building blocks and identifying MEV opportunities from the order flow, which, in the case of SUAVE, are user preferences. In the context of SUAVE, the driver functions more as a mempool management entity where user preferences are received. Executors (as solvers here) can then listen to these preferences and solve them.

> How do solvers guarantee block inclusion for the client? Will txns be routed through MEV-boost, or through private order flow?

Solvers operate at a layer above the order flow layer of the EVM. Their primary task is to determine the best route for the user’s optimizable ATO. Once the path is identified, it is sent and executed from the user’s wallet as a UserOperation.

> How do you plan on deciding which solver reward mechanic to use? Is there a way to implement many reward solutions here, and/or allow solvers to create/enforce their own reward mechanisms depending on order type specialty?

For now, the reward mechanism we are considering is largely based on the type of ATO a solver addresses. However, we are definitely open to discussions and suggestions regarding the implementation of a flexible solver oriented rewards mechanism.

---

**nlok5923** (2023-09-15):

Thanks [@paul0x741](/u/paul0x741) for the contribution

Here are the answers to your recent queries.

> One thing I’m thinking about is how expressive an intent can be on conditional criteria for example can they express preferences on mempool data? Would the driver need to wait for that data to be finalized? How would that affect the DOE calculation?

For sure, in the future, we might have intentions that prioritize preferences based on mempool. We could perhaps draw inspiration from SUAVE MEVM contracts in this regard. However, these preferences are more logical when managed by developers on behalf of the users. In our current architecture, we are focusing more on user-oriented preferences, ones that could potentially offer greater value around specific operations. For instance, if a user wants to execute a swap operation, they could specify preferences such as low slippage, faster execution, and interaction with trusted contracts, encompassing both on-chain and off-chain preferences.

Regarding the second part, we mentioned in the ATO ordering section that the driver would propagate ATO bundles in phases. Once a solution for a specific phase is determined, the updated state information will be included with the next set of ATO bundles, allowing solvers to work with the refreshed state…

> If a solver has access to private orderflow and can get better execution how would the driver verify that?

The primary value proposition of solvers collaborating is to achieve the most optimized solution possible and to support the resolution of multiple different types of operations, as an intent might encompass several operations. Thus, users will benefit the most from this infrastructure when the driver manages the order flow.

> You say that this yields enhanced availability of solvers but what about the driver?

In the initial iteration, the driver will be governed by the DAO. However, we eventually plan to decentralize the driver. In the future, we aim to release an extension for the solvers that will handle the validation, verification, and management of ATOs. This can be likened to running a ethereum client, as a client operates both the consensus and execution clients.

> How does the Intent Execution Module work, does the user need to manually verify the solution for onchain execution?

The Intent Execution Module will serve as an extension to the user’s smart contract wallet, enabling support for intent execution. Its primary function is to facilitate fee payments and execute calldata received for a specific intent. The solution will be verified by the driver entity, and we are planning introduce an API (via driver) through which dApps can display the execution steps for the user’s resolved intent.

---

**Bbasche** (2023-09-15):

Hey guys, thanks for this, super interesting area of investigation and great questions raised - particularly around solver incentivization and proving optimality.

Two questions I had

1. Can you ELI5 why the driver needs to be enshrined with a particular DAO? I understand the idea of progressively decentralizing it etc but I want to understand why ATOs necessitate a DAO for this system role in this design whereas the userOps they are somewhat analogous to (and definitely adjacent to as you described) do not as far as I can tell? Why not a design explicitly around multiple drivers, or a network of drivers with reputations that could be managed by arbitrary actors like DAOs or other designs as we have in AA-land ? You did allude to this down road in the post but why not from start is what first comes to mind for me.
2. I forgot the second question by the end of that so I’ll come back later if I remember it

Thanks!

---

**nlok5923** (2023-09-16):

Thanks for the contribution [@Bbasche](/u/bbasche)

> Can you ELI5 why the driver needs to be enshrined with a particular DAO? I understand the idea of progressively decentralizing it etc but I want to understand why ATOs necessitate a DAO for this system role in this design whereas the userOps they are somewhat analogous to (and definitely adjacent to as you described) do not as far as I can tell? Why not a design explicitly around multiple drivers, or a network of drivers with reputations that could be managed by arbitrary actors like DAOs or other designs as we have in AA-land ? You did allude to this down road in the post but why not from start is what first comes to mind for me.

For the very first iteration of this network we are more focused on building a robust network of solvers that could help facilitate optimized and faster resolving of intents into optimized executable paths. Having a network of drivers does helps in delegating loads and maintaining consensus in validation and verification stage of solutions. But we wanted to work on it phase by phase so for the first phase building a network of solvers and enabling a communication layer between driver and solver network is what we are thinking to focus on. Once the architecture is functional We could move to the next phase of development which could surely involve building a network of drivers.

Considering AA, The phases of development are quite similar. As for the first phase of functional AA we had separate teams providing their own bundlers and other services and with the next sets of development phases we are seeing development towards an alternate mempool for UserOps where all bundler would listen and fetch userOp to bundle and broadcast.

Please do let us know your feedbacks we are open to discussion.

---

**nlok5923** (2023-09-19):

Firstly, we want to extend our gratitude to the community for the insightful feedback and challenging questions. Below, we address the major points raised:

1. The Role of the Driver:

- The driver currently works in harmony with DAO in our architecture, acting as a coordinator and aggregator of ATOs. However, we should note that while its operation looks centralize, it doesn’t centralize control or introduce a single point of failure. We’re actively exploring ways to decentralize this piece, including introducing multiple driver implementations with varying ordering algorithms. In a gist, anyone should be able to build and propose a driver implementation, promoting decentralization and reducing potential biases.
- The driver’s role in our design differs from SUAVE’s MEVM primarily in its ATO ordering and managment. Whereas SUAVE MEVM offering a totally different approach of enabling user to build their own searches, relayer, builders. Our infrastructure would lie one layer above SUAVE infrastructure

1. Solver Network and Incentivization:

- Our approach does lean on solvers being competitive and incentivized correctly. We’re still iterating on incentive model to attract more people to build solvers for this network.
- The Degree of Expectation (DoE) was indeed designed to be a representation of solver’s solution. We’re in the process of introducing some weighted parameters to ensure that it can be tuned to users’ specific preferences.

1. Expressiveness of Intents:

- Intents are designed to be as expressive as possible. While our current focus is on optimizing the DoE for immediate user intents, we acknowledge that more dynamic and conditional intents (like those based on mempool data) can introduce complexity. We are iterating on ATO design to enable it to capture as much preferences as possible for a particular operation.

1. Execution and Verification:

- Although we would be having certain validity checks at Driver end to verify the solution authenticity before providing it to the user. Apart from Driver check we a devising a model in which user would be able to see the execution steps before actually executing the intent.

1. Availability and Redundancy:

- Multiple solvers working as a part of network would enable max uptime and expand avenues for solving multiple different types of intents.

1. Decentralization and DAO Involvement:

- DAO involvement provides a layer of community governance over critical system components (in context of our architecture Driver). However, we understand the concerns about starting the infra with a DAO-centric approach. Our vision is to evolve towards a network of drivers managed by various entities, not limited to DAOs. Starting with DAO involvement ensures community participation from the outset, but we’re flexible in adapting our approach based on practical implications and feedback.

To conclude, we’re at a nascent stage, and there’s much to refine. The intent-driven approach is UX friendly, but its success hinges on the collaboration of the community, users, and developers. We welcome continuous feedback and collaboration as we iterate on this architecture.

Once again, Really appreciate valuable insights, and we look forward to further discussions and collaborations.

---

**0xTaker** (2023-09-22):

Thought I’d chime in and reply here after having a good read of this - for one, really enjoyed it! There’s a couple things I think that still are up in the air for me.

**The ATO Schema:**

It’s good that ATOs are more loose than that of UserOps, Transaction Objects etc.

- Does additional validation occur for each operation type? For example, to make sure that I’ve staked ETH with the Lido contract to get stETH as opposed to having swapped for it on a DEX?
- With an external constraint system and the ATO schema, it would be possible to forge ATOs. What protections would be in place to protect against DoS on the solvers?
- Am I correct in that an unsolved ATO is one where payload and payloadSchema is unset / set to their default values and a solved ATO is one where they are set?
- How would constraints / validity conditions / counterfactuals be encoded? Would this be using a very large negative weighting?

**The Driver:**

From reading, it seems like the driver holds a number of responsibilities for this system to function:

- Receiving the client’s ATO
- Bundling of ATOs
- Sending of ATOs to a designated solver or designed solvers
- Sending of solved ATOs back to the client

I do have some questions regarding this related to censorship:

- How is censorship by the driver managed? How does the driver ensure itself try to prevent censoring a client’s ATO or solver’s solved ATO back to the client? Is this from alignment with the DAO’s intentions that it ultimately leads to more ATO uptake?
- In the scenario that a collective of solvers behind a driver does choose to censor a specific segment of ATOs or clients, what would you envision the switching cost be to another driver? Is a solver network specific to a single driver and thus a switch to another driver potentially worsen solution quality?

---

**nlok5923** (2023-09-23):

Thanks for the contribution [@0xTaker](/u/0xtaker)

> Does additional validation occur for each operation type? For example, to make sure that I’ve staked ETH with the Lido contract to get stETH as opposed to having swapped for it on a DEX?

The validation totally depends on the operation type and the operation type would always be fixed for a particular ATO. For your example, the operation type for the ATO could always be STAKE or SWAP.

> With an external constraint system and the ATO schema, it would be possible to forge ATOs. What protections would be in place to protect against DoS on the solvers?

Yes, for sure it is possible to forge ATO’s with external constraint system but the DoS won’t be beneficial. As before the solver starts working on the ATO the user would have to pay the fees upfront for solving those ATOs. So even if the user starts forging ATO’s just to DoS the solvers. The attack vector would be very expensive for them.

> Am I correct in that an unsolved ATO is one where payload and payloadSchema is unset / set to their default values and a solved ATO is one where they are set?

Yes, exactly

> How would constraints / validity conditions / counterfactuals be encoded? Would this be using a very large negative weighting?

We are planning to enforce constraints / validity condition / counterfactuals on ATO via trusted Driver for the very first iteration.

(if I understood correctly) yes it would apply very large negative weighting to the solutions which fails constraints / validity conditions / counterfactuals.

**The Driver:**

> From reading, it seems like the driver holds a number of responsibilities for this system to function:

- Receiving the client’s ATO
- Bundling of ATOs
- Sending of ATOs to a designated solver or designed solvers
- Sending of solved ATOs back to the client

Yes we gave it a thought after hearing some feedbacks and for the next iteration we are working on delegating several responsibilities out of driver to smart contract to make system more permissionless and transparent.

I do have some questions regarding this related to censorship:

> How is censorship by the driver managed? How does the driver ensure itself try to prevent censoring a client’s ATO or solver’s solved ATO back to the client? Is this from alignment with the DAO’s intentions that it ultimately leads to more ATO uptake?

Yes, we planned DAO would lead the charge towards Driver but for sure your query is totally valid we are working on delegating out the pieces which could lead to censorship to work with harmony in user and DAO.

> In the scenario that a collective of solvers behind a driver does choose to censor a specific segment of ATOs or clients, what would you envision the switching cost be to another driver? Is a solver network specific to a single driver and thus a switch to another driver potentially worsen solution quality?

I think the above answer answers the first few parts of this question. For the other parts, The solver network won’t be specific to Driver it just a routing entity that is responsible for routing the ATO’s to the solver network. We want Driver should be composable such that any party could spin up their Driver with their own custom routing logic for ATO’s and integrate it with the system. Also, we do forsee having driver’s custody owned to users could lead to potential censorship issues.

Thanks for the amazing feedback this was definitely helpful and would help us to make this system far more robust and secure.

---

**nlok5923** (2023-09-30):

Thanks for the contribution [@xmrjun](/u/xmrjun) absolutely we are working towards the community feedback and certain points of centralization in our current iteration of infrastructure.

We would be updating the post with potential solutions soon.

---

**nlok5923** (2023-10-11):

Hi everyone,

Thank you for your valuable feedback.

Upon analyzing the feedback, we noticed that a recurring concern was the centralization of the Driver in our infrastructure, which could lead to potential centralization issues.

We have taken this feedback and developed an approach to decentralize the Driver component within our infrastructure.

Decentralizing driver by making it a component of solver client. And we are calling that component as Router.

[![Approach towards Driver Decentralization](https://ethresear.ch/uploads/default/optimized/2X/0/028861cb1fcebfccf389424f9759ce889e82fdd3_2_690x413.jpeg)Approach towards Driver Decentralization2386×1430 193 KB](https://ethresear.ch/uploads/default/028861cb1fcebfccf389424f9759ce889e82fdd3)

### Thoughts on Driver Decentralisation

We are thinking of an approach where driver roles have been delegated to solver clients themselves. Basically, the solver client now would have two components.

- Router Component: The Router component would be performing all the duties of the Driver. which includes ATO’s routing, solution simulation, winner selection and solution aggregation
- Solver Component: The Solver component would be the component where solvers could embed their solving algorithms. The solver components would act as an interface for solvers where they just have to plug their own solver implementation (can be in the form of API integration, SDKs etc.). Through the interface itself, the solvers would be receiving ATO for solving.

### ATO Routing

Clients can send their intents (ATO bundles) to any of the solver client RPCs. Once sent the ATOs would land into solver offchain mempool. From thier the Router component of the solver client would route the ATOs to other solvers. (for example sending swap ATOs to swap solvers, bridge ATOs to bridge solvers etc).

### Winner Selection and Solution Aggregation

Once the ATOs are solved by different solver clients. The solved ATOs would be routed back to the origin solver which received those ATOs and the origin solver would now decide the winning solver based on the solution efficiency and at least it would aggregate the winning solution and return it back to the users.

Further, we are planning to operate the Router component inside a trusted execution environment so as to eliminate any inference from the solver component of the client. We don’t want the solver component to have access to the solutions the Router component would receive for a particular ATO so as to avoid solver cheating.

In Addition to that, we plan to employ winning solver deciding and ATO sharing capabilities in a trusted manner within the solver client. As it might be the case if the Router component is kept open within the Solver client the solvers might tweak it and make it not to share the ATO with another solver to solve or could modify it to always declare their own solver solution as the winning solution for a particular ATO.

## Why this is better than our first approach ?

In our previous proposal Driver worked as a DAO-owned trusted entity. It’s the sole entity which was getting order flow (in the form of ATOs) from user, broadcasting ATOs to solver and for deciding the winning solver for a particular ATO. Which conveyed the fact that owning a Driver means owning the whole network. But in the current approach, we delegated the Driver task to the Router component of each solver client.

| Task | DAO-owned Driver Approach | Router component in each solver client |
| --- | --- | --- |
| Broadcasting ATOs to solve | The driver had the ownership of all the order flows (user intents) Driver would receive the orderflows first and then it would broadcast it to solvers for solving. | Any user can send his intent to any solver client. And the solver client would have to share the ATO’s with each other via trusted Router component. |
| Winning solver declaration | Driver had the sole control for deciding the winner solver for a particular ATO. | With Router component we are planning to employ a voting based mechanism to decide the winning solver for a particular ATO. |
| Availability bottleneck | Driver has to be up all the time in case the driver went down the whole solver network would stop working. | Solver network would remain avalaible till the last know solver client up for work. |

## How will the solver run the router?

Solver doesn’t have to worry about the complexities of the Router component. They just have to integrate their APIs, SDK etc. into the client solver component and that’s it. Once integration is done the solvers would just have to spin up the client.

Looking forward towards feedback on this revised approach.

Thanks!

---

**pixelcircuits** (2023-10-13):

I’m curious if you’ve thought about issues with solutions that only work at a specific block height, but quickly become invalid. Basically, how can you guarantee a solution valid at block n, will still be valid by the time the client submits their tx at block n+1?

---

**ankurdubey521** (2023-11-15):

> we are planning to operate the Router component inside a trusted execution environment so as to eliminate any inference from the solver component of the client.

how do you guarantee that every node ensures that the solver component is unable to access information meant to the router component, given that all information is received over a network interface?

Additionally, what incentive does a node have to “not” try and intercept the solutions from other solvers? As a node runner in the network, I could simply choose to not run the router in an isolated component and claim the fee for the solutions myself.

I also had an unrelated question: In the original post, the first step is to send a raw intent to the “constraint system” which is responsible for breaking down the intent into ATOs that are then further processed by the driver/router. How does this constraint system work?


*(1 more replies not shown)*
