---
source: ethresearch
topic_id: 16480
title: Efficient Stateless Ethereum Execution
author: sogolmalek
date: "2023-08-25"
category: Execution Layer Research
tags: [zk-roll-up, stateless]
url: https://ethresear.ch/t/efficient-stateless-ethereum-execution/16480
views: 2499
likes: 7
posts_count: 2
---

# Efficient Stateless Ethereum Execution

**Motivation:**

**TL;DR:** Light clients struggle to efficiently access and validate data on the mainnet due to challenges in obtaining concise witness proofs. Verkle trees help lightweight clients transition between blocks but can’t prove new state accuracy. Stateless clients lack state data for actions beyond transitioning. The Portal Network doesn’t fully address these issues. Our solution adds entities to the stateless verifier LC on the Portal Network with a cache to store important state fragments. We distribute the latest state using zero-knowledge proofs and propose a chase mechanism for efficient data retrieval. This addresses challenges in accessing state data for tasks like gas estimation and enhances lightweight client efficiency.

**Project Description:**

Light clients struggle to efficiently access and validate data. Currently, light clients, which rely on simplified verification, face challenges in accessing and validating the mainnet state due to the absence of concise witness proofs. These clients need to confirm blocks without having access to the full state.

Verkle trees allow very lightweight clients to consume proofs from other networks to transition from the last block to the new block. However, they cannot prove the accuracy of the new state root. If a stateless client discards all its stored information, it can still confirm the accuracy of new state roots. By doing so, a stateless client can still send transactions but cannot calculate gas estimates, perform ETH calls, or read Ethereum’s state since it no longer maintains any state data. The client is limited to actions that involve transitioning from one state to the next state root, without any specific state-related functions.

This is where the Portal Network comes into play. While it allows the reading of random state data, it doesn’t fully mitigate the core issue. The underlying challenge persists—efficiently accessing state data remains crucial for various tasks, including gas estimation. Additionally, Verkle trees, despite their benefits, don’t inherently solve problems like federated access to the state.

To bridge this gap, an innovative solution comes in the form of the Portal Network introducing a stateless verifier LC (Lightweight Client) with a partial state caching mechanism to enhance the efficiency of accessing specific segments of the state. It achieves this by storing frequently accessed or important state fragments in a cache, enabling clients to retrieve them more quickly than repeatedly traversing Verkle trees.

**Our proposal of partial state caching complements has following value propositions:**

- Improved Retrieval for Stateless Clients:
Stateless clients lack the ability to store the full state and rely on external means to access data. By using partial state caching, we offer an efficient method for these clients to access vital state fragments, reducing their reliance on complex Verkle tree processes.
- Less Data Transfer and Computation:
Stateless clients struggle with data transfer and computation. Partial state caching lets them access pre-cached data, lessening the need for extensive data transfers and computational work, in line with the efficiency objectives of stateless clients.

-Decentralized, Trustless Verification:

Stateless clients aim for trustless Ethereum network interaction. Through partial state caching, clients can independently verify cached state fragment validity using zk proofs, preserving trustlessness by eliminating dependence on a central source.

-Swift Data Retrieval:  Cached state fragments are readily available, bypassing the need to rebuild or navigate the Verkle tree for each request. This rapid access to cached data results in quicker retrieval times compared to direct tree fetching, especially for frequently needed data.

- Reduced Network Latency:
Cached fragments can be fetched locally, reducing the reliance on multiple network interactions for Verkle tree traversal. This minimizes network delay and enhances responsiveness.
- Efficient Resource Use:
Cached fragments reduce computational load during Verkle tree traversals, particularly for complex state structures. This optimizes computing resource utilization.
- Consistency and Validity:
The partial state caching mechanism ensures consensus-validated data, preventing caching of compromised or invalid data. This boosts integrity and data retrieval reliability.

-Optimized State Access:

Partial state caching can prioritize frequently accessed state fragments, catering to stateless clients’ needs for specific data subsets. This speeds up necessary information access, elevating overall efficiency.

- Improved Security and Reliability:
Stateless clients face security risks with third-party state data. Incorporating cryptographic proofs and cached state fragments empowers clients to autonomously verify data integrity, boosting security and reliability in Ethereum network interactions.

Ps. I’ve added an [issue](https://github.com/sogolmalek/EIP-x/issues/5) in my GitHub to propose an initial draft of the Cashe mechanism design.

## Replies

**sogolmalek** (2023-09-11):

Discussion:

The ability to verify a transaction’s execution with only the post-execution state and the last state (pre-execution state) depends on what we want to verify and the specific details you require for validation. Lets break down what we can prove and what we can not prove with lightclients only having previous state and post state:

What We Can Prove:

1. Balances and State Changes: we can prove that the transaction correctly changed the account balances and storage values from the last state to the post-execution state. This includes checking that the sender’s balance decreased by the correct amount, and the recipient’s balance increased as expected.
2. Transaction Hash and Signature: We can verify that the transaction hash in the block matches the one provided in the transaction, and we can validate the transaction’s digital signature using the sender’s public key.

What We Cannot Prove:

1. Contract Code Execution: We cannot directly prove that the contract method produced the expected output, consumed the expected amount of gas, or adhered to the contract’s internal logic without retaining the contract code. This limitation means you won’t be able to fully verify the correctness of contract execution, especially for complex smart contracts.
2. Interaction with Other Contracts: If the transaction interacts with other contracts, we cannot fully validate those interactions, including the inputs and outputs of those interactions, without retaining the contract code for those other contracts.

While we can verify some aspects of a transaction’s execution with only the last state and the post-execution state (e.g., balances and basic transaction integrity), verifying more complex interactions and contract logic would require retaining the contract code. The proposal of partial state caching can be valuable for improving retrieval efficiency and reducing reliance on complex tree processes, but it may not fully address the need for contract code to verify all aspects of execution and interactions with other contracts.

Implementing partial state caching as a proposal should not inherently break the concept of statelessness for light clients in the context of having only the post-execution state and the last state. Statelessness in Ethereum refers to clients, typically light clients, that do not store the entire state but rather access it as needed.

Partial state caching can be seen as a means to enhance the efficiency of stateless clients by allowing them to access specific state fragments more efficiently. However, it does not fundamentally change the stateless nature of these clients. Instead, it provides a mechanism to reduce the complexity and resource requirements associated with verifying transactions and smart contract interactions.

With partial state caching, a light client can still operate in a stateless manner by relying on external sources to access vital state fragments (the last state and the post-execution state) temporarily during transaction verification. This allows the client to verify transactions more efficiently without having to maintain a full state database.

By selectively caching relevant contract data during transaction execution, the light client can validate interactions with other contracts more effectively without retaining the entire contract codebase. This approach allows for a balance between efficient validation and the need for selective contract data access. This approach can reduce the gas fee bounded by state access and contract storage.

Partial caching can help address the challenge of validating interactions with other contracts when we  have a portion of the contract code included in a recent block.

1. Selective Caching:

When a transaction interacts with another contract, the light client can selectively cache the contract code, storage, and state related to the contract being interacted with.
2. This selective caching should occur dynamically based on the contracts accessed during transaction execution. Only cache what is needed for the specific interactions within the transaction.
3. Cache Smart Contract Data:

Store relevant contract code, storage values, and any state changes introduced by the contract’s methods during the transaction’s execution.
4. This data should be cached temporarily and used for validation during and immediately after the transaction’s processing.
5. Transaction Validation:

During validation, the light client can compare the expected inputs and outputs of the contract interactions with the actual data cached during execution.
6. It can verify that the inputs to the contract methods match the transaction’s input data and that the outputs produced by the contract match the expected results.
7. Ensure that gas consumption is consistent with expectations.
8. Dependency Handling:

If the contract being interacted with depends on other contracts, cache data for those dependent contracts as well.
9. Continue to selectively cache data for dependent contracts, allowing for a more complete validation of contract interactions.
10. Trust Considerations:

Maintain trust in the RPC node providing the cached data, as it is essential for the integrity of the validation process.
11. Ensure that the cached data is provided by a trusted and reliable source to avoid potential manipulation.
12. Data Cleanup:

After the transaction’s validation and any necessary post-transaction processes, the cached data can be safely removed from the light client’s memory or database.

