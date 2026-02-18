---
source: ethresearch
topic_id: 21431
title: Key Management for Autonomous AI Agents with Crypto Wallets
author: jieyilong
date: "2025-01-12"
category: Cryptography > Multiparty Computation
tags: []
url: https://ethresear.ch/t/key-management-for-autonomous-ai-agents-with-crypto-wallets/21431
views: 1490
likes: 3
posts_count: 5
---

# Key Management for Autonomous AI Agents with Crypto Wallets

Autonomous AI Agents equipped with crypto wallets are attracting growing attention due to their capability to interact directly with blockchains and smart contracts. These agents can perform a variety of tasks, including sending and receiving tokens, calling smart contracts, and even writing and deploying smart contracts on-chain. Unlike traditional systems, these autonomous AI agents are proactive, capable of making independent decisions without direct human intervention. An example is an autonomous crypto trading agent which leverages sophisticated deep learning algorithms to execute trades by interacting with on-chain DEXes. In this scenario, a user might provide the agent with an initial fund and delegate trading decisions entirely to the agent, aiming for long-term profitability. This hands-off approach, powered by the agent’s ability to analyze market trends and execute trades autonomously, exemplifies the transformative potential of combining AI and crypto in decentralized finance (DeFi) and beyond.

To enable these promising capabilities, an AI Agent needs to possess a private key to initiate blockchain transactions. If the agent runs in a local device, such as a smartphone or a laptop, managing the private key becomes relatively straightforward. However, AI Agents often require substantial computational resources — for example, to run advanced large language models (LLMs) — making this simple design impractical for many use cases. To help address this challenge, below we informally define the problem:

**Problem definition**: A user seeks to deploy an autonomous AI Agent that proactively acts on their behalf. The user provides the Agent with a private key which enables direct or indirect access to valuable on-chain crypto assets. Due to the significant computational demands of the Agent — such as running advanced deep learning models or performing resource-intensive tasks — it may need to operate in a potentially adversarial environment, such as a remote server. The challenge is to design a system such that, even in the event of a server compromise, the crypto assets accessible through the private key remain secure.

Below we sketch a few possible approaches to tackle to the above problem:

1. TEE based: The first approach involves the user securely storing the Agent’s private key within a Trusted Execution Environment (TEE) and executing the entire AI Agent code inside the TEE. Provided the TEE remains uncompromised, adversaries would be unable to either alter the Agent’s code or extract the private key. However, while TEEs are designed to be secure, they could still be susceptible to sophisticated attacks targeting specific vulnerabilities in their implementation. Additionally, the use of TEEs may introduce performance overhead, as running code within the protected environment can be slower compared to execution outside of it.
2. iO based: Indistinguishable Obfuscation is a powerful cryptographic tool. As Vitalik discussed in this article, one direct application of iO is to hide the private key in the AI Agent code. The primary advantage of iO lies in its ability to ensure that, even if the key is included in the obfuscated code, adversaries should be unable to extract it, even when the code is executed on a remote server. However, iO is still in a nascent stage, both in terms of theoretical development and practical implementation. Current constructions of iO are highly resource-intensive, requiring significant computational overhead and large memory footprints, making them impractical for many real-world applications.
3. MPC based: A more practical approach is to leverage cryptographic tools such as multi-party computation (MPC) and threshold signature scheme (TSS). In this setup, multiple instances of the AI Agent code are run in parallel across several worker nodes. In this setup, we run multiple instances of the AI Agent code in parallel with multiple worker nodes. The user splits the private key into multiple shares, and securely sends each share to a different worker node, ensuring that no single node possesses the entire key. To interact with the blockchain, the worker nodes execute a consensus algorithm to propose and agree on specific actions. Once consensus is achieved for a particular transaction, the nodes collaboratively execute an MPC-based threshold signature protocol to jointly sign the transaction. Crucially, this process allows the signature to be generated without reconstructing the private key in its entirety. This ensures that even if an adversary compromises some worker nodes, the private key remains protected, provided a majority of the nodes remain secure. Although this approach requires the additional overhead of running multiple instances of the AI Agent, it significantly enhances security while allowing the Agent to operate safely in untrusted environments.

[![Screenshot 2025-01-12 at 11.16.29 PM](https://ethresear.ch/uploads/default/optimized/3X/6/6/66efe792083477f5e4323ab56028bf92f737c590_2_553x500.png)Screenshot 2025-01-12 at 11.16.29 PM1246×1126 31.5 KB](https://ethresear.ch/uploads/default/66efe792083477f5e4323ab56028bf92f737c590)

1. SNARK based: In this approach, we run a SNARK prover along with the Agent in the powerful server. Meanwhile, we run the corresponding SNARK verifier in a local personal device (smartphone, laptop, etc.). The local personal device also possesses the private key. The user first generates a cryptographic commitment to the AI Agent code and publish it on the blockchain. Then, each time the server generates a transaction requiring the signature of the private key, the local device uses the SNARK verifier to ensure that the transaction is generated by the committed Agent code. If the SNARK verification succeeds, the local device signs the transaction with the private key and submits the signed transaction to the blockchain. Unlike the MPC-based approach, this method eliminates the need to run multiple copies of the AI Agent code. However, despite recent advancements in zkML, generating SNARK proofs for cutting-edge deep learning models remains highly challenging due to the computational complexity involved. Nonetheless, if the Agent code is relatively simple or if the SNARK proof is required only for specific parts of the Agent’s logic, this approach becomes a practical and efficient solution.

[![Screenshot 2025-01-12 at 11.03.19 PM](https://ethresear.ch/uploads/default/optimized/3X/f/e/fe53c23a02a27e2b5e850812444f5ff8e098ef37_2_324x500.png)Screenshot 2025-01-12 at 11.03.19 PM820×1262 22.6 KB](https://ethresear.ch/uploads/default/fe53c23a02a27e2b5e850812444f5ff8e098ef37)

The above outlines several potential solutions we are exploring to address the AI Agent key management challenge. We welcome any feedback or suggestions to refine and improve these approaches!

## Replies

**SanLeo461** (2025-01-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/jieyilong/48/1899_2.png) jieyilong:

> SNARK based: In this approach, we run a SNARK prover along with the Agent in the powerful server. Meanwhile, we run the corresponding SNARK verifier in a local personal device (smartphone, laptop, etc.). The local personal device also possesses the private key. The user first generates a cryptographic commitment to the AI Agent code and publish it on the blockchain. Then, each time the server generates a transaction requiring the signature of the private key, the local device uses the SNARK verifier to ensure that the transaction is generated by the committed Agent code. If the SNARK verification succeeds, the local device signs the transaction with the private key and submits the signed transaction to the blockchain. Unlike the MPC-based approach, this method eliminates the need to run multiple copies of the AI Agent code. However, despite recent advancements in zkML, generating SNARK proofs for cutting-edge deep learning models remains highly challenging due to the computational complexity involved. Nonetheless, if the Agent code is relatively simple or if the SNARK proof is required only for specific parts of the Agent’s logic, this approach becomes a practical and efficient solution.

Instead of relying on another point of failure within the local device signing the transactions, why not do away with the private key in this scenario, and have a smart contract wallet which verifies the SNARK on-chain and execute the transaction if everything is correct.

Leveraging the idea of verifying AI outputs with SNARKs is another possible approach:

**Cryptoeconomic based**: In this approach, we use a cryptoeconomic scheme to verify the actions of an agent. For example using EigenLayer, an EigenLayer validator running a custom agent will calculate the output and commit it to the chain, validators have bonds which can be slashed if they misbehave. We can add a time delay to the agents actions and either introduce a slashing penalty for either an honest majority disagreeing with the output of another validator, or if someone else submits a SNARK disproving their committed answer.

Crucially these approaches based on smart contracts instead of private keys allow proper decentralization and redundancy so that agents can continue working in adversarial environments.

---

**jieyilong** (2025-01-20):

> and have a smart contract wallet which verifies the SNARK on-chain and execute the transaction if everything is correct.

Yes that’s definitely an improvement we can consider.

> Cryptoeconomic based

That’s an interesting direction as well.

---

**mayorcoded** (2025-01-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/jieyilong/48/1899_2.png) jieyilong:

> it may need to operate in a potentially adversarial environment, such as a remote server

First, I must say I find the overall problem definition very interesting.

However, I would like to add that if the agent already runs in an adversarial environment like a remote server, it might be simpler to use already existing battle-tested cloud security solutions.

For example, if the agent runs on a remote server on AWS, the solution could take advantage of AWS services such as the Secrets Manager and Key Management System to securely manage how the agent signs and execute transactions on-behalf of the user. These services also provide fine-grained access control policies that can be used by the user to grant permission to the agent, and even restrict the activities of the agent to certain geographical locations and 3rd-party services.

Additionally and probably more importantly, these services never allow agents have access to the user’s private keys, the agent rather interacts with the services to sign transactions via some API. In the event of a compromise of these services, the private keys are encrypted and will be useless to the bad actor.

Although my suggestion takes a rather orthodox approach to designing the solution, I just thought it’s simpler and cheaper to use existing solutions if the agent runs on a remote server.

---

**ElusAegis** (2025-02-16):

Thank you for raising this topic! It’s a very interesting discussion. However, I think it’s useful to approach it from a slightly different angle. While private keys are indeed a fundamental primitive for authentication today, they might be overkill for AI agents if our real goal is simply to verify correct algorithmic execution rather than to maintain strict secret storage in adversarial environments.

## Redundancy of Private-Key–Based Schemes for AI Agents

Private keys are optimal for authenticating a “black box” (e.g., a human or an external entity) where the only assumption we can make is that the black box can preserve secret storage. Authentication signatures produced by these keys are succinct and provide strong cryptographic guarantees that a message originates from the trusted secret holder.

However, for AI agents whose behaviour follows a deterministic algorithm, relying on secret-based authentication introduces unnecessary constraints. Instead, we can focus on generating a proof that the agent’s decisions were computed using the correct algorithm or model, removing the need to manage and hide a private key.

## Verification of AI Agents: Standard Approach

The original post already outlined two well-known approaches, but their role slightly shifts when the focus is purely on verification rather than securing a secret:

- TEE Attestation
A Trusted Execution Environment (TEE) can provide a constant-sized attestation that the intended code ran unmodified. Removing private key requirements eliminates the need for secret storage and only requiring it to preserving integrity. It’s then worth noting that TEEs offer stronger guarantees for computation integrity than privacy. If an adversary can compromise computation integrity, they can extract the secret, but not vice versa. This idea has been implemented by Phala network as far as I can tell.
- SNARK Proofs
SNARKs such as Groth16 produce constant-size, verifiable proofs of correct execution. However, as correctly outlined, their computational overhead remains a significant challenge for models of reasonable size. While several optimizations have been proposed, SNARKs nonetheless provide an elegant alternative to secret-based authentication by allowing any observer to verify the correctness of a computation without requiring private keys. This has already been proposed by ERC-7007: “Verifiable AI-Generated Content Token” and is actively explored by many protocols.

However, these are general-purpose verification techniques applicable to any computation. Since AI agents typically run structured models (e.g., Transformers, Neural Networks), we can leverage their unique properties to achieve verification at a fraction of the cost of fully generic solutions.

## Verification of AI Agents: Alternative Approaches

Some approaches we could consider:

- Split-Model Architectures
A smaller verifier can check that the AI model (or a portion of it) was used and that its results adhere to the intended functionality.
- Backdoor/Embedded Checks
Models can incorporate cryptographic traps or embedded verification mechanisms to confirm authenticity, leveraging properties unique to neural networks and transformers. I am working on a preprint for this approach and hope to share it soon.

## Toward Verifiable AI Agents

The final challenge is replacing private keys in blockchain environments, but this may be very feasible. With Ethereum’s account abstraction, as well as work by Ritual of creating a framework for attestable ML data on chain, we could soon authorize transactions based on AI-verifiable proofs instead of secret-based signatures. This would allow an untrusted host to run a model and publish actions on-chain, while a verifier—potentially a smart contract—could check that the transaction originated from the expected model, enabling verifiable AI agent execution.

