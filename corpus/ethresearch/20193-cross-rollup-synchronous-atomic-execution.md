---
source: ethresearch
topic_id: 20193
title: Cross-rollup Synchronous Atomic Execution
author: HankyungKo
date: "2024-08-01"
category: Layer 2
tags: []
url: https://ethresear.ch/t/cross-rollup-synchronous-atomic-execution/20193
views: 2292
likes: 9
posts_count: 2
---

# Cross-rollup Synchronous Atomic Execution

- by Hankyung Ko(@HankyungKo) and Chanyang Ju(@wooju), Researcher at Radius . Thanks to Tariz and AJ for reviewing this post.
- Your feedback and opinions are highly valued.

*Radius has designed a synchronous atomic execution solution for cross-rollup composability. This development is driven by our commitment to support rollups seeking improved composability and enhanced user experience. We will enable rollups to create their own shared sequencing layer, offering this as a service to make it widely accessible. By doing so, we ensure that atomic execution of bundled transactions is coordinated effectively across participating rollups.*

# 1. Introduction

---

Synchronous atomic execution allows multiple transactions from different rollups to be executed simultaneously and atomically in an all-or-nothing manner, significantly reducing latency compared to sequential execution. A naive approach to executing multiple cross-rollup transactions require each transaction to be finalized sequentially on L1. For n transactions, the total latency would be n times the L1 finalization period. In contrast, **`synchronous atomic execution`** enables all transactions to be executed at the same time, significantly reducing latency.

While executing transactions simultaneously can reduce latency, it may raise concerns about security. For example, in a bundled transaction involving minting-and-burning across different rollups, there’s a risk that the burn could fail while the mint succeeds. To address this, we’ve designed our system to verify the atomicity of bundled transactions faster than the time it takes for block finalization. This approach ensures that security is maintained even with simultaneous execution. Our innovation improves composability across multiple rollups, providing a seamless, efficient, and secure user experience with real-time, all-or-nothing execution of cross-rollup transactions without delays.

To implement this convenient and secure solution, Radius introduces a shared sequencer for rollups to guarantee the atomic execution of bundled transactions. Users create bundled transactions that depend on transactions across multiple rollups, and the shared sequencer manages the sequencing of bundled transactions for successful execution.

> It’s important to note that this shared sequencer is not a single entity controlled by Radius, but rather a set formed by aggregating existing sequencers from each rollup. A leader is selected from this set through a predefined process (reference) to manage sequencing.
>
>
> To prevent potential power abuse by the shared sequencer, Radius employs decentralized sequencing techniques, including encrypted mempool (PVDE and SKDE). The shared sequencer has two main functions: determining transaction order and enforcing transaction reverts to maintain bundle atomicity.
>
>
> This article details on how our architecture addresses the second function, ensuring atomicity. Preventing potential abuse of the first function, transaction ordering, is also crucial. Radius addresses this concern through the encrypted mempool, ensuring that the shared sequencer cannot abuse its power regarding transaction ordering.

## 1) Requirements of the synchronous atomicity solution

- Convenience: Users can achieve greater benefits by utilizing atomic execution of cross-rollup bundled transactions, without compromising security.

Bundle transactions: Users can bundle and execute multiple transactions across different rollups as one.
- Atomic execution: The bundle transaction is guaranteed to execute simultaneously without failures. If a failure occurs, it is guaranteed to fail simultaneously.
- Fast execution for bundle while maintaining security: Transactions are guaranteed to be executed faster than sequential execution (where each transaction waits for the previous one to finish). This allows users to strategize their next transactions more quickly. Additionally, atomic execution is cryptographically verified before finalization, ensuring that the security of the transactions is maintained even though they are executed more quickly.

**`Security`**

- Minimized trust level: Aims to minimize the amount of trust users must place in key network participants like the shared sequencer and executors by:

Minimizing the number of parties that need to be trusted.
- Minimizing the duration for which trust is necessary.
- Ensuring early detection and verification of any malicious behavior by the shared sequencer and executors before blockchain finalization.

## 2) Main Idea

We propose an architecture for synchronous atomic execution using the `shared sequencer`, `data availability (DA)`, and a `verification layer`.

### Why shared sequencer?

- To satisfy the desired properties of convenience and security, it is necessary to handle bundled transactions across multiple rollups. Therefore, we propose a new entity called the shared sequencer, which is responsible for confirming the blocks of multiple rollups.
- The shared sequencer receives a cross-chain bundle and determines the block order for atomic execution.
- The shared sequencer is responsible to ensure the atomic execution of bundled transactions before confirming the block.

### New responsibility of the executor

- The executor, in agreement with the shared sequencer, has an added constraint: it must execute the transaction list committed by the shared sequencer.

[![SAE_figure1](https://ethresear.ch/uploads/default/optimized/3X/5/5/553162b8f7a0148ceedbd7bddbf19ce91d944f58_2_690x130.png)SAE_figure13188×602 134 KB](https://ethresear.ch/uploads/default/553162b8f7a0148ceedbd7bddbf19ce91d944f58)

[Figure 1] The definition of roles and responsibilities of shared sequencer and executors

### Conditions for synchronous atomicity

- Synchronous atomicity for bundle transaction is achieved if the following two conditions are independently verified:

All bundled transaction in the block committed by the shared sequencer should be atomic.
- The executor executes the same block as committed by the shared sequencer.

## 3) Our Contributions

- Designed a synchronous atomic execution solution:

Security requirements definition: We have defined the security requirements for each entity involved in synchronous atomic execution, ensuring that all components operate securely and reliably.
- Architecture design: We have designed a robust architecture that ensures security and efficiency. This architecture includes:

User’s bundle transaction: We defined the structure and format of bundle transactions that users can create. These bundled transactions enable users to execute multiple transactions across different rollups simultaneously, ensuring atomic execution.
- The bundler contract: We designed and implemented the bundler contract, which is responsible for handling and processing bundled transactions. This contract is called by the shared sequencer, and performs several critical functions:

Acts as a gateway smart contract for users to call the actual contracts they intend to execute.
- Allows the shared sequencer to enforce transaction reverts to guarantee the atomicity of the bundle transactions.
- Verifies the legitimacy of transactions initially created by the user.
- Charges transaction fees to users.

**Coordination process for the shared sequencer**:  We developed a coordination process for the shared sequencer, which includes interaction with the full nodes (simulators) of each rollup. This process ensures that the shared sequencer can effectively manage and sequence transaction across multiple rollups, guaranteeing atomic execution.
**Verification logic**: We defined the verification logic to ensure that all transactions within a bundle meet the defined security requirements before finalization.

**Demonstrated the feasibility of the architecture:**

- Implementation: We have implemented the entire architecture, demonstrating its feasibility and effectiveness. Our implementation includes all components of the synchronous atomic execution solution, from the user’s bundle transaction creation to the coordination process for the shared sequencer.

The user’s bundled transaction is signed using MetaMask.
- Implemented on two Polygon CDKs:

Each Polygon CDK has an API that responds to the shared sequencer’s simulation requests.
- Each Polygon CDK has a deployed Bundler contract.

**Demo**: The demo scenario involves transferring tokens from Rollup A to Rollup B. In this scenario, the bundled transaction consists of two operations: burning the wrapped token on Rollup A and mint it on Rollup B. This demonstrates the practical application of our solution. ([Check out our Demo here!](https://x.com/radius_xyz/status/1809120936270123468))

# 2. Definition

---

[![SAE_figure2](https://ethresear.ch/uploads/default/optimized/3X/0/b/0bec5c1463e929939d860e125c34e05cbc6b4c34_2_690x243.jpeg)SAE_figure23288×1158 246 KB](https://ethresear.ch/uploads/default/0bec5c1463e929939d860e125c34e05cbc6b4c34)

[Figure 2] Overview of transaction flow

> The proposed architecture is based on the following assumptions.
>
>
> Scenario
>
> Each Bundle Tx consists of two transactions: a Burn transaction and a Mint transaction of ERC20 contract (rToken), occurring on different chains (inspired by Hyperlane bridge scenario).
>
>
> Rollups
>
> Each rollup has a simulation API implemented.
> The Radius’ Bundler contract is deployed on each rollup.
> The ERC20 rToken contract is also implemented on each rollup.
> The execute function of the Radius’ Bundler contract is accessible only by whitelisted shared sequencers.
> The ERC20 contract (rToken) grants burn and mint access rights to the Radius’ Bundler contract.
>
>
> Incentives and Penalties (Future work)
>
> There are sufficient incentives for correct behavior and penalties for incorrect behavior for the shared sequencer and Executor.

## 1) Operational Roles and Security Requirements of Entities

In this section, we define the correct behavior and adversarial behavior of each entity in the architecture. The adversarial behaviors defined here will be analyzed in Section 4.

- User: The entity that generates cross-rollup bundled transactions and sends them to the shared sequencer for atomic execution.

Adversarial behaviors

Creates invalid Bundle Tx:

The value of the BURN Tx and the MINT Tx do not match.
- Insufficient account balance for the tokens intended to be burned.
- Lacks the ability to pay the gas fee required for executing the transaction on at least one chain.
- Incorrectly signs the Bundle Tx.

Calls the MINT function without the shared sequencer’s assistance:

- Attempts to execute the MINT Tx without creating a Bundle Tx.

**`Shared sequencer`:** The entity responsible for receiving bundled transactions from users, creating and submitting blocks for multiple rollups, and ensuring the atomic execution of bundled transactions.

- Adversarial behaviors

Calls bundler contract without user’s consent.
- Fails to verify whether the Bundle Tx is executed atomically across all rollups.
- Forces the valid Bundle Tx to revert unnecessarily.
- Sends a different transaction list to the executor than the one committed to the DA after confirming the block.

**`Executor`:** The entity specific to each rollup that executes the transaction list determined by the shared sequencer and uploads the resulting blocks to the Data Availability layer.

- Adversarial behaviors

Does not execute the transaction list as confirmed and provided by the shared sequencer.

**`Shared Prover`:** The entity that generates zero-knowledge proofs to validate the atomic execution of bundled transactions across different chains based on data from the Data Availability layer.

## 2) Additional Components

- Simulator: The simulator refers to the full node of each rollup that the shared sequencer communicates with to validate the atomicity of bundled transactions before committing the block. This entity could be the same as the executor mentioned above.
- Data Availability Layer (DA): The DA is a layer for storing data committed by the shared sequencer and executor to prove their honesty. The shared prover uses this information to verify the honesty of both entities.

Given a reliable DA, if the shared sequencer and executor each commit the minimum necessary information for the verification of synchronous atomicity to the DA, it can be quickly verified based on that information.

**`Verification layer`:** The verification layer is responsible for verifying the proofs generated by the shared prover and assisting with the appropriate actions if verification fails. This layer can either be part of the settlement layer or a dedicated layer focused solely on verification.

# 3. Synchronous atomic execution architecture

---

[![SAE_figure3](https://ethresear.ch/uploads/default/optimized/3X/e/a/ea8cbd6739d8f45ec741d82a13f6f55f94907b38_2_690x349.jpeg)SAE_figure31920×973 147 KB](https://ethresear.ch/uploads/default/ea8cbd6739d8f45ec741d82a13f6f55f94907b38)

[Figure 3] The process of synchronous atomic execution architecture

The architecture of Radius’s synchronous atomic execution ensures that bundled transactions are executed in an all-or-nothing manner within the same cycle, coordinated by the shared sequencer. Initially, the shared sequencer’s coordination is trusted optimistically, allowing each transaction to be executed independently on its respective rollup. Subsequently, the atomicity of these transactions is verified before the rollup blocks are finalized on L1.

It can be divided into three main components: **the bundler contract**, **the coordination process**, and **the verification process**. This section will describe each of these components in detail.

## 1) Smart Contract for Bundle Transaction (Radius’s Bundler contract)

[![SAE_figure2](https://ethresear.ch/uploads/default/optimized/3X/0/b/0bec5c1463e929939d860e125c34e05cbc6b4c34_2_690x243.jpeg)SAE_figure23288×1158 246 KB](https://ethresear.ch/uploads/default/0bec5c1463e929939d860e125c34e05cbc6b4c34)

[Figure 4] Overview of transaction flow

We introduce a new smart contract called `Radius’s bundler contract`, designed to handle and process the users’ bundled transactions. It acts as a gateway to execute the users’ intended contracts.

For example, as shown in the figure, suppose a user creates a bundled transaction that includes calling the Burn function of the rToken contract on Rollup A and the Mint function of the rToken contract on Rollup B. The shared sequencer receives this bundle and wraps it into a transaction that calls the Radius’s bundler contract. Each rollup then processes the transaction through a series of verification via the Radius contract, ultimately executing the user’s intended contract calls.

### Key features of the Bundler contract

- Acts as a gateway smart contract for users to call the actual contracts they intend to execute.
- Allows the shared sequencer to enforce transaction reverts to guarantee the atomicity of the bundle transactions.
- Verifies the legitimacy of transactions initially created by the user.
- Charges transaction fees to users.

### How is the Bundler contract implemented?

The Bundler contract includes the following functions:

- execute: Called by the shared sequencer, this function executes the user’s transaction after a series of verifications.
- deposit: Allows users to deposit transaction fees in advance.
- withdraw: Allows users to withdraw their deposited funds.
- addWhitelist: Adds a sequencer to the whitelist.
- removeWhitelist: Removes a specific sequencer from the whitelist

### How is the execute function implemented?

> The input parameters for the execute function are as follows:
>
>
> from: User address
> bundle_tx_list: Information of all transactions within the Bundle Tx
> index: Current transaction’s index within the bundle_tx_list
> bundle_tx_signature: User’s signature for the Bundle Tx
> revert_flag: Flag for enforcing revert
>
> The sequencer includes a “revert_flag” in the data, which is set by the sequencer to forcibly revert the user’s transaction. If this value is set to true, the Bundler contract will revert the user’s transaction. This mechanism is designed to ensure the atomicity of the transactions defined in the bundle, preventing the execution of the remaining transactions if even one included in the bundle fails to execute.

1. Access control:

Verify that the call is made by a shared sequencer listed in the whitelist.
2. Check revert_flag:

If revert_flag == true, forcibly reverts the transaction.
3. Verify user’s transaction:

Decode the transaction’s data field.
4. Ensure the user’s deposit is greater than the transaction fee.
5. Verify the user’s bundled transaction signature.
6. Check the Bundle Transaction validity

(In this scenario) Verify that the values to be minted and burned are identical.
7. Deduct transaction fee from user’s deposit (Exception handling required for early reverts):

Transfer the transaction fee to the shared sequencer from the contract’s deposited assets.
8. Deduct the transaction fee from the user’s deposit.
9. Execute user’s intended contract:

Call the contract that the user intended to execute.

## 2) Coordination process for the shared sequencer

Radius’s shared sequencing technique separates the roles of sequencing and execution. The shared sequencer is responsible for deciding the block that atomically executes the user’s bundle transactions, while the block is built by each rollup’s executor. Therefore, if it can be ensured that the shared sequencer has coordinated the atomic execution of the bundle transactions and the executor has executed the block as determined by the shared sequencer, synchronous atomic execution is achieved.

Coordination involves requesting simulations to the full nodes of each rollup for the respective transaction lists, collecting the simulated results, and, if some transactions within the bundle need to be reverted to maintain atomicity, forcibly reverting the remaining transactions to produce a transaction list that will be executed atomically. In other words, if the simulation results of the two transaction defined in the bundle are not the same (i.e., one is a revert and the other is a success), the transaction that yields a successful result is modified by setting its `revert_flag` to 1 to forcibly revert it. The transaction list is then updated with the modified transaction.

[![SAE_figure5](https://ethresear.ch/uploads/default/optimized/3X/4/d/4d77403de3cd9cacd9e96500481eda982fd6f53f_2_690x493.jpeg)SAE_figure51920×1374 138 KB](https://ethresear.ch/uploads/default/4d77403de3cd9cacd9e96500481eda982fd6f53f)

[Figure 5] Example of a Simulation Process

After finalizing the block, the shared sequencer commits to it. Later, the block information committed by the shared sequencer can be compared with the block executed by the executor to verify that the executor executed the block as agreed. The atomicity of the bundle transactions can be verified by examining the receipt committed by the executor after building the block, which shows the success status of each transaction and ensures that the shared sequencer did not forcibly revert all transactions. These two processes can be verified off-chain using ZKP systems such as RiscZero or SP1. This process is detailed in section 3.3.

## 3) Verification process for the shared prover

We design a zk prover called  “Shared Prover” which allows us to verify that the shared sequencer and executor acted in accordance with the protocol’s intentions. The shared prover generates proof for the **atomicity of the bundle transactions** and their **valid execution result** according to the commitment.

We leverage the DA layer to facilitate the sharing of the sequencer’s commitments and execution data across different chains. Utilizing the DA layer for data storage offers enhanced transparency and accessibility. Based on the DA (Data Availability) data, it can be confirmed that the user’s bundle transactions were executed atomically, and the validity of the execution result on different chains can be verified.

The shared sequencer communicates with simulators to finalize the the list of transactions to be performed while ensuring atomicity, and the executor processes this list and then it uploads the resulting data to the DA layer.

### Information stored in the DA

- Shared sequencer’s transactions list commitment
 To settle transaction list, shared sequencer commits the following data with signature to the DA:

chain ID
- block height
- transaction MPT root
- bundle transaction list

**Executed Block data**

After a block is executed on each chain, the entity who executed the block uploads the results to the DA.

### Atomicity proofs (Shared sequencer’s honesty)

The shared prover retrieves the block execution results stored in the DA by the executor. In the atomicity proof, the following aspects are verified using zero-knowledge proofs:

- All-or-Nothing execution

 The receipt status for the bundle transactions must have the same value.
 \text{assert!} (\text{receipt}(\text{tx}_A).\text{status} = \text{receipt}(\text{tx}_B).\text{status})

**Prevention of arbitrary manipulation of the shared sequencer’s revert flag**

- There is a potential attack where a valid bundled transaction is reverted entirely, collecting fees from the user without executing the transaction. To prevent this, the atomicity proof checks that not all revert flags for the transactions are set to 1.
- Therefore, revert flags cannot be set to 1 simultaneously.
 \text{assert!}(\text{tx}_A.\text{revert_flag} \times \text{tx}_B.\text{revert_flag} = 0)

### Proof of Rollup executor’s honesty

To verify that the executor has honestly executed the block according to the transaction list committed by the shared sequencer, the shared prover also includes the relationship between the values committed by the shared sequencer and the MPT root of the transactions uploaded by the executor.

# 4. Security analysis

---

- Individual Transaction Validity: The validity of individual transactions (e.g., insufficient user’s balance) is verified by the Bundler Contract, and transactions will fail if they do not pass this check.
- Bundle Transaction Validity: The validity of the bundled transaction (e.g., discrepancy between mint and burn amounts) is also verified by the Bundler Contract, and the bundle will fail if it does not pass this check.
- Atomicity of Successful Bundle Transactions: The shared sequencer is responsible for ensuring the atomicity of successfully executed bundled transactions. The honesty of the shared sequencer is verified by the shared prover and the verification layer.
- Honesty of the Executor: If the shared sequencer has legitimately determined and committed the blocks for each rollup, the honesty of the executor is verified by the shared prover and the verification layer.
- Prevention of Manipulation: Additionally, neither the shared prover nor the rollup executor can manipulate the user’s bundle transaction. The user’s signature prevents such tampering.
- Integrity of Proofs and Verification: The shared prover and the verification layer perform proofs and verification based on authenticated data available in the Data Availability (DA) layer. As a result, they cannot alter the proof content. The worst they can do is to withhold performance.

## Replies

**EugeRe** (2024-08-07):

Hey [@HankyungKo](/u/hankyungko) [@wooju](/u/wooju) this looks very nice! I would like to have a chat with you to anchor some ideas I have in mind, please also have a look at my past blog on [Self-Sovereign Identity and Account Abstraction for Privacy-Preserving cross chain user operations across roll ups](https://ethresear.ch/t/self-sovereign-identity-and-account-abstraction-for-privacy-preserving-cross-chain-user-operations-across-roll-ups/19599)

