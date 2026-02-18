---
source: ethresearch
topic_id: 20981
title: "AI-Powered Ethereum: From Rules-Based Smart Contracts to AI-Powered Smart Contracts"
author: punk3700
date: "2024-11-14"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/ai-powered-ethereum-from-rules-based-smart-contracts-to-ai-powered-smart-contracts/20981
views: 393
likes: 0
posts_count: 1
---

# AI-Powered Ethereum: From Rules-Based Smart Contracts to AI-Powered Smart Contracts

*Hi! We just released a whitepaper on adding onchain LLM to smart contracts. Any feedback is much appreciated. We have also implemented it already. You can play around with it at [eternalai.org](http://eternalai.org)*

# AI-Powered Ethereum

## From Rules-Based Smart Contracts to AI-Powered Smart Contracts

**Abstract.** One of the most fascinating aspects of Ethereum is its ability to create decentralized systems based on a set of smart contracts that can operate without human intervention. However, these smart contracts are still limited by their reliance on pre-programmed rules and logic. By integrating AI, we can begin to create systems that are not only decentralized but also autonomous, adaptive, and self-aware. This raises a range of interesting questions about the combined potential of blockchain technology and the role of AI in decentralized systems. To explore these questions, we propose the development of an AI Kernel that can be used to build AI-powered smart contracts on Ethereum. Eternal AI presents the architecture of the AI Kernel and examines the implications of integrating AI into smart contracts.

# 1. Truly Smart Contracts

Let’s take a step back and think about what we’re trying to achieve with smart contracts. We want to create systems that are not only decentralized but also autonomous, able to make decisions and respond to changing circumstances.

But if we look at the current state of dapps, we’re still a long way from achieving that vision. Most dapps today are simply rule-based programs coded in smart contracts with no ability to integrate AI capabilities. They’re like rigid machines, unable to adapt or learn from their environment.

Meanwhile, in the Web2 world, we’re seeing a proliferation of AI-powered applications capable of making decisions in real-time. So, what’s holding us back from bringing this same level of sophistication to decentralized applications?

To address this challenge, we need to rethink the way we approach decentralized software development. We need to create a framework that allows developers to incorporate AI capabilities into their smart contracts, enabling the creation of truly smart contracts that can adapt and evolve over time.

We propose to achieve this by developing an AI Kernel for Ethereum.

# 2. A New Programming Model

Consider a smart contract that manages a decentralized fantasy sports league. The contract needs to determine the winner of a matchup between two teams.

## Rule-Based Approach

With a traditional rule-based approach, the contract might use a complex set of if-else statements to analyze each player’s performance and determine the matchup’s winner.

[![](https://ethresear.ch/uploads/default/optimized/3X/7/d/7d170c152ba23645d0972c413a844be7acfb7204_2_624x256.jpeg)1598×654 85.3 KB](https://ethresear.ch/uploads/default/7d170c152ba23645d0972c413a844be7acfb7204)

Figure 1. Rule-based smart contract.

This approach would be rigid and inflexible and unable to capture the game’s nuances and complexities.

## AI-Powered Approach

In contrast, the AI Kernel enables a new programming model that uses large language models (LLMs) to make decisions dynamically in real time. With the AI Kernel, the fantasy sports league contract could be written as providing a prompt to the LLM and receiving a structured response.

[![](https://ethresear.ch/uploads/default/optimized/3X/2/9/294993a536f3c8fa3c46bfa19ace693fdd42efe8_2_624x301.jpeg)1598×770 115 KB](https://ethresear.ch/uploads/default/294993a536f3c8fa3c46bfa19ace693fdd42efe8)

Figure 2. AI-powered smart contract.

In this example, the contract prompts the AI Kernel to analyze the two teams’ performance and determine the matchup winner. This approach allows for much more flexibility and dynamic decision-making. It could capture the nuances and complexities of the game in a way that a traditional rule-based approach would not.

# 3. AI Kernel Architecture

To build truly smart contracts and AI-powered dapps, we need a decentralized framework that can facilitate the integration of AI inference, AI models, and GPU resources. This is where the AI Kernel comes in – the central component of the AI-powered Ethereum.

[![](https://ethresear.ch/uploads/default/optimized/3X/6/e/6eb7da57185b5fcef0a29ac3798d87e42f708857_2_478x430.jpeg)1600×1441 140 KB](https://ethresear.ch/uploads/default/6eb7da57185b5fcef0a29ac3798d87e42f708857)

Figure 3. The AI Kernel architecture.

At a high level, the AI Kernel can be broken down into four main components. Let’s explore each of these in turn, and think about how they fit together to enable decentralized AI.

First, we have the User space – the domain where dapps operate. In this space, developers can build applications that interact with AI models, but they don’t have direct access to the underlying AI models or compute resources. Instead, they connect to the AI models via the Kernel space.

The Kernel space is where the magic happens. This component provides a simple programming interface for developers to interact with AI models, making it easier to build AI-powered dapps. Under the hood, the kernel space is divided into two sub-components: Decentralized Inference and Core AI Kernel. The Decentralized Inference provides a simple programming interface for developers to interact with AI models. At the same time, the Core AI Kernel takes care of the complex task of executing AI models on decentralized compute resources.

Next, we have the Model space – a domain dedicated to managing AI models. Here, we take existing open-source models like Llama and FLUX, and adjust them to work onchain, enabling decentralized inference. By making these models available onchain, we can create a shared resource that developers can tap into, without having to replicate effort or manage complex model deployments.

Finally, we have the Hardware space – the component that interacts with physical hardware, such as GPU nodes worldwide. This is where the compute resources are provisioned and the AI models are executed. By leveraging decentralized compute resources, we can create a scalable and flexible platform that can handle complex AI workloads.

# 4. User Space

Let’s consider the user’s journey to interacting with the AI Kernel. It starts with a prompt — a request for the AI Kernel to generate an output. This prompt can come from a regular user or smart contract accounts. The prompt is sent to the Decentralized Inference smart contract.

The prompt itself is a simple data structure consisting of four fields:

- The account: either a regular user account or a smart contract account
- The topic: one of the many unique contexts between the account and the AI Kernel
- The input: a question or a message to elicit an AI-generated output
- The extra piece of context (optional)

[![](https://ethresear.ch/uploads/default/optimized/3X/1/b/1b40db0cb07ca808f6a97707905bd2415f1b5766_2_624x277.png)1600×712 66.5 KB](https://ethresear.ch/uploads/default/1b40db0cb07ca808f6a97707905bd2415f1b5766)

Figure 4. A chain of prompts for a specific account and topic.

The topic is an interesting concept – it’s a unique context that’s shared between the account and the AI Kernel. This context is crucial for the AI Kernel to generate a meaningful output, and it’s something that evolves over time. The Context Manager smart contract is responsible for constructing and updating this context, based on the previous prompts, the input, and any extra context provided.

Once the prompt is submitted, the AI Kernel generates an output, and the Context Manager updates the prompt context with the new output. The prompt data is stored onchain, meaning anyone can verify the output by rerunning the prompt. This transparency is a key feature of the AI Kernel, which sets it apart from traditional AI systems.

Developers have a choice regarding storing the prompt data — they can either store it directly on its native blockchain or store a hash that points to the raw data on an external decentralized storage network like Filecoin. This flexibility is important, as it allows developers to balance the trade-offs between cost, scalability, and security.

Overall, the User Space is designed to provide a simple and intuitive interface for users to interact with the AI Kernel. By abstracting away the complexity of the underlying AI models and compute resources, we can create a seamless experience that allows users to focus on what matters - generating insights and solving problems.

# 5. Kernel Space

The AI Kernel is the heart of our decentralized AI architecture. It is designed to be modular and flexible. At its core, the AI Kernel consists of a set of smart contracts that work together to manage resources and facilitate communication between different parts of the protocol.

[![](https://ethresear.ch/uploads/default/optimized/3X/9/2/92e714e8e34cbdb94d71ef227ee07fecc1247439_2_480x290.jpeg)1600×968 85.4 KB](https://ethresear.ch/uploads/default/92e714e8e34cbdb94d71ef227ee07fecc1247439)

Figure 5. The core smart contracts of the AI Kernel.

Let’s take a look at the five main smart contracts that make up the AI Kernel.

First, the Decentralized Inference contract provides a standardized interface for dapps to interact with the AI Kernel. This contract offers a set of “inference calls” that allow developers to tap into the AI Kernel’s capabilities in a simple and intuitive way.

Next, we have the Prompt Scheduler contract, which is responsible for distributing GPU time and resources among all prompts in a fair and efficient manner. This is a critical component of the AI Kernel, ensuring that all prompts can be handled efficiently and simultaneously. The Prompt Scheduler uses various scheduling algorithms, such as round-robin and fee-based, to manage the flow of prompts and ensure that the system remains responsive and scalable.

The GPU Management contract is another key component of the AI Kernel. This contract manages the staking, status, and configurations of GPU nodes, which are the workhorses of the decentralized AI system. By providing a standardized interface for managing GPU nodes, we can ensure that the system remains flexible and scalable.

The Model File System contract provides access to stored models on various file systems, such as Filecoin and Arweave. This contract abstracts the details of different file systems, providing a consistent model I/O interface to GPU nodes. This allows developers to focus on building their dapps without worrying about the underlying complexities of model storage and retrieval.

Finally, the Context Manager contract organizes and makes various user contexts accessible to GPU nodes. This contract is critical for ensuring the AI Kernel can provide personalized and context-dependent responses to user queries.

These five smart contracts form the core of the AI Kernel, working together to provide a decentralized and scalable AI system that can support a wide range of applications.

# 6. Model Space

The Model Space is a critical component of the AI Kernel, where we adapt popular open-source AI models to the blockchain environment. At its core, the Model Space consists of two key components: AI Models and AI Model Drivers.

The AI Models are well-known open-source models like Llama, FLUX, and Hermes. These models have been widely adopted in the AI community and provide a solid foundation for our decentralized AI system.

However, these models were not designed with the blockchain in mind, which is where the AI Model Drivers come in. These drivers play a crucial role in adapting the models to the blockchain environment, ensuring they can operate effectively in a decentralized setting.

One key challenge in adapting AI models to the blockchain is ensuring deterministic. In other words, we must ensure that the models produce the same results given the same input. This is critical for maintaining the integrity of the decentralized AI system, and the AI Model Drivers are designed to handle it.

Another important aspect of adapting AI models to the blockchain is quantization. By reducing the precision of model weights and activations, we can improve performance and reduce storage requirements. This is especially important in a decentralized setting, where storage and computational resources may be limited.

The AI Model Drivers are designed to be modular and extensible, allowing new models to be integrated into the AI Kernel easily. This means that developers can simply plug in new models as they become available without worrying about the underlying complexities of the blockchain environment via a standardized interface.

# 7. Hardware Space

The Hardware Space is where the actual computation happens in the AI Kernel. At its core, this space consists of GPU nodes that serve as the atomic compute unit of the system. These nodes are responsible for taking user prompts, running inference, and returning outputs.

But what makes these GPU nodes tick? The answer lies in the GPU Management smart contract, which plays a critical role in managing the nodes and ensuring that they’re qualified to work. To participate in the system, nodes must stake EAI, which provides a level of accountability and ensures that nodes are invested in the success of the AI Kernel.

In addition to managing nodes, the GPU Management contract also tracks hardware configurations, such as GPU device models. This information is used by the Prompt Scheduler contract to assign prompts to nodes for processing.

But how do nodes get incentivized to participate in the system? That’s where the Proof-of-Compute mechanism comes in. This novel approach to node participation rewards nodes for generating outputs for prompts. The first node to generate an output for a prompt is rewarded with EAI, creating a built-in incentive mechanism that encourages nodes to support the AI Kernel.

Think of it like gold mining. Miners expend resources to add gold to circulation, and in return, they’re rewarded with a piece of that gold. In our case, GPU nodes expend resources (electricity and GPU time) to process prompts, and in return, they’re rewarded with EAI. This mechanism creates a self-sustaining ecosystem where nodes are incentivized to participate and support the AI Kernel.

Eventually, as the system matures, the reward mechanism will transition to prompt fees, making it completely inflation-free. This approach ensures that the AI Kernel’s ecosystem is sustainable and self-sufficient, with nodes incentivized to participate and users paying for value-added services.

# 8. Proof-of-Compute

Traditional consensus algorithms like Proof-of-Work (PoW) have been criticized for their lack of real-world utility. In contrast, our AI Kernel runs on a novel consensus algorithm called Proof-of-Compute (PoC), which challenges this paradigm by repurposing the computational energy expended in the network.

Instead of solely solving a complex mathematical puzzle, GPU nodes in the PoC network perform meaningful computations on prompts requested by real users and real dapps. This generates valuable outputs for them, creating a self-sustaining ecosystem where nodes are incentivized to participate, and users receive tangible benefits.

So, how does Proof-of-Compute work? The process is straightforward:

First, users or dapps submit a prompt to the Decentralized Inference smart contract. This prompt can be anything from a simple question to a complex AI task.

Next, the Prompt Scheduler smart contract randomly assigns the prompt to a subset of available GPU nodes managed by the GPU Management smart contract. This ensures a decentralized and resilient computation process where no single node has too much control.

Once assigned, the GPU nodes process the prompt and generate outputs, competing to be the first to return a valid result. This competition incentivizes nodes to invest in computational resources and participate honestly in the network.

The first GPU node to return a valid output receives a reward comprising the prompt fee and the block reward. This reward mechanism incentivizes nodes to participate in the network and maintain its integrity.

But what about malicious behavior? To address this, other GPU nodes verify the output for accuracy, detecting and penalizing malicious behavior. This validation and penalty mechanism ensures the integrity of the computation process and maintains trust within the network.

By combining these elements, Proof-of-Compute creates a novel consensus algorithm that not only secures the network but also provides tangible benefits to users. It’s a new blockchain consensus paradigm that prioritizes utility and efficiency over mere security.

[![](https://ethresear.ch/uploads/default/optimized/3X/7/1/71d94a277ec8d80dc8fc554a62b17eebba218205_2_624x436.png)1600×1118 124 KB](https://ethresear.ch/uploads/default/71d94a277ec8d80dc8fc554a62b17eebba218205)

Figure 6. Proof-of-Compute

# 9. AI-Powered Decentralized Applications

As we integrate the AI Kernel into Ethereum, a new paradigm for decentralized applications begins to take shape. No longer limited by rigid, rule-based programming constraints, developers can now create dapps capable of adapting, learning, and evolving over time.

## Onchain Conversational AI Agents

With just a few lines of code, you can build an autonomous agent on top of the AI Kernel and earn passive income by charging a service fee when someone uses your agent.

[![](https://ethresear.ch/uploads/default/optimized/3X/6/3/637ed842df63c9071312905a4b1c344002439a6d_2_624x196.png)1518×478 58.7 KB](https://ethresear.ch/uploads/default/637ed842df63c9071312905a4b1c344002439a6d)

Figure 7. Onchain AI agent.

When someone chats with your agent, simply call the AI Kernel.

[![](https://ethresear.ch/uploads/default/optimized/3X/d/3/d3b780212fa26ca57d8c452931a0b5c7597f4f21_2_624x196.png)1600×504 107 KB](https://ethresear.ch/uploads/default/d3b780212fa26ca57d8c452931a0b5c7597f4f21)

Figure 8. Conversational onchain AI agent.

## AI-Powered Crypto Wallet

In this example, we’re building an AI-powered wallet. Before sending the funds to an address, the wallet will call the suspiciousTransaction function.

[![](https://ethresear.ch/uploads/default/optimized/3X/e/b/eb462ae970d3c066fb40b8c20e8946f4e139c6f5_2_624x344.jpeg)1600×883 178 KB](https://ethresear.ch/uploads/default/eb462ae970d3c066fb40b8c20e8946f4e139c6f5)

Figure 9. AI-powered crypto wallet.

By providing the AI Kernel with a rich context of transaction history, the model can learn to identify potential red flags such as:

- Large or unusual transaction amounts
- Unusual frequencies within a short period
- Transactions that are not consistent with the user’s typical wallet behavior
- Transactions to known flagged addresses

## AI-Powered Oracles

In this example, we’re building an AI-powered oracle for BTC prices.

[![](https://ethresear.ch/uploads/default/optimized/3X/a/b/abf968b8b5d9d498e7a1c1871849c14f6bceb4d7_2_624x364.png)1430×834 98.2 KB](https://ethresear.ch/uploads/default/abf968b8b5d9d498e7a1c1871849c14f6bceb4d7)

Figure 10. AI-powered oracles.

By providing the AI Kernel with a rich context of BTC price feeds added continuously by Oracle feeders, the AI Kernel can learn to return the current BTC price by aggregating the fed prices and determining the most accurate value.

## AI-Powered DAOs

In this example, we’re building an AI-powered DAO.

[![](https://ethresear.ch/uploads/default/optimized/3X/e/6/e6ac324c400a255838f8ad60293bc3f329eb9b33_2_624x347.jpeg)1600×889 180 KB](https://ethresear.ch/uploads/default/e6ac324c400a255838f8ad60293bc3f329eb9b33)

Figure 11. AI-powered DAOs.

By feeding the AI Kernel a continuously updated context of proposal result history, the AI Kernel can develop an understanding of successful and unsuccessful proposals. This enables it to assess and predict the viability of new proposals and make informed decisions on whether to approve or reject a proposal.

## AI-Powered Wallet Credit Scores

In this example, we’re building an AI-powered Wallet Credit Scoring system.

[![](https://ethresear.ch/uploads/default/optimized/3X/7/c/7c956f1f8bb8ceb00ed8cbd56f9f175c620cbe02_2_624x328.jpeg)1600×841 164 KB](https://ethresear.ch/uploads/default/7c956f1f8bb8ceb00ed8cbd56f9f175c620cbe02)

Figure 12. AI-powered credit scoring.

By providing the AI kernel with a comprehensive context of a given address’s transaction history, including details such as transaction amounts, contract interactions (e.g., swaps, lending, borrowing), and other relevant data, the model can learn to accurately assess the address’s creditworthiness and provide a corresponding credit score.

## AI-Powered ENS

In this example, we’re building an AI-powered ENS generator.

[![](https://ethresear.ch/uploads/default/optimized/3X/e/2/e2baa9e8e7f688d9aaac20bacb4f678077297ffe_2_624x371.jpeg)1600×952 133 KB](https://ethresear.ch/uploads/default/e2baa9e8e7f688d9aaac20bacb4f678077297ffe)

Figure 13. AI-powered ENS.

The model can generate an available ENS domain that best fits the given description. If a suggested domain has already been taken, it will continue to retry until it finds a suitable one.

# 10. Conclusion

The integration of AI and blockchain technology represents a significant paradigm shift in the way we approach decentralized systems. Our work on the AI Kernel provides a framework for executing AI computations on the blockchain, opening up new possibilities for decentralized applications.

As AI is such an important technology and is growing into every fabric of our lives, the success of decentralized AI will depend on our ability to design systems that are not only technically robust but also socially and philosophically sound. This requires a deep understanding of the complex relationships between technology, society, and the individual.

Ultimately, our work on the AI Kernel is a starting point for a broader conversation about the future of AI-powered decentralized systems and their potential to reshape our world.
