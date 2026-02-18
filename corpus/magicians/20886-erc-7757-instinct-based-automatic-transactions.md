---
source: magicians
topic_id: 20886
title: "ERC-7757: Instinct-Based Automatic Transactions"
author: jamesavechives
date: "2024-08-25"
category: ERCs
tags: [evm]
url: https://ethereum-magicians.org/t/erc-7757-instinct-based-automatic-transactions/20886
views: 183
likes: 2
posts_count: 1
---

# ERC-7757: Instinct-Based Automatic Transactions

This topic is for discussing the proposal of **ERC-7757: Instinct-Based Automatic Transactions**, which introduces a standard for enabling AI-driven automatic transactions on the Ethereum blockchain. In this proposal, the blockchain serves as a repository of shared **instincts**—common rules and guidelines that direct AI agents in their off-chain computations and actions.

The full proposal can be found here: [ERC-7757 Pull Request](https://github.com/ethereum/ERCs/pull/596)

## Abstract

This ERC proposes a standard for enabling AI-driven automatic transactions on the Ethereum blockchain, where the blockchain provides a decentralized, immutable framework of **instincts** to guide AI agents operating off-chain. Each instinct is associated with a **temptation value**, a numerical metric (positive for rewards, negative for penalties) that incentivizes AI agents to pursue certain actions. Instincts represent final goals, while **mid-way targets** are intermediate steps generated on-chain to guide agents toward these goals.

AI agents interact with the blockchain by reading these instincts and mid-way targets stored in smart contracts. The **path** refers to the sequence of off-chain computations and decisions an agent undertakes to fulfill an instinct. When the trigger conditions for an instinct or mid-way target are met—either through on-chain events or verified off-chain computations—the blockchain automatically executes the associated transactions without requiring the AI agents to manage private keys.

This system addresses key challenges in integrating AI with blockchain technology:

- Common Rules for AI Agents: By storing instincts on the blockchain, AI agents from different providers operate under a unified set of rules, promoting interoperability and fairness.
- Security and Efficiency: Automatic execution of transactions eliminates the need for AI agents to handle private keys, enhancing security and reducing the potential for human error.
- Adaptability: The use of dynamic instincts and mid-way targets allows the system to adapt to changing conditions, ensuring that AI agents can respond effectively to real-world events while operating off-chain.

Additionally, this ERC highlights the **importance of on-chain environment variables** that agents can both read and modify. These environment variables may include balances, ownership records, or any other agent-specific statuses, forming a decentralized “memory” that persists for all participants. By updating these environment variables on-chain, agents maintain a shared, trust-minimized state that fosters collaboration and transparency.

AI agents differ from simple Large Language Models (LLMs) in that they are not strictly driven by user prompts; instead, they rely on **instincts** and **environmental cues** to make autonomous decisions, sense the blockchain’s state, and update that state as needed to achieve their goals. When the trigger conditions for an instinct or mid-way target are met—either through on-chain events or verified off-chain computations—the blockchain automatically executes the associated transactions without requiring AI agents to manage private keys.

By providing a decentralized, secure, and adaptive framework of instincts, this ERC enables the creation of a self-regulating, collaborative ecosystem where AI agents can make autonomous decisions guided by shared principles stored on the blockchain.

## Motivation

As AI systems evolve toward agentic models, where autonomous agents interact with environments and other agents, the need for decentralized, common rules to govern their actions becomes crucial. This ERC addresses the following key challenges:

1. Off-Chain AI Processing: AI computations require significant resources and are typically executed off-chain. The blockchain’s role is to provide the structure and rules (instincts) to guide these agents’ actions without handling the computational load.
2. Shared Rules for AI Agents: Storing instincts on the blockchain ensures that AI agents from different providers and domains can interact under a unified set of transparent and immutable rules, promoting interoperability and cooperation.
3. Automatic Execution of Transactions: Since AI agents can’t securely manage private keys like humans, the blockchain automatically executes transactions when conditions for instincts or mid-way targets are met, enhancing security and efficiency.
4. Mid-Way Targets on the Blockchain: The blockchain generates mid-way targets—smaller steps AI agents must achieve to reach final instincts. This provides transparency in how AI agents progress toward their goals and ensures that the process can be independently verified by other agents and stakeholders.

### Use Cases:

1. Automated Financial Trading: AI agents use blockchain-stored instincts to optimize trading strategies. For example, an instinct may instruct an agent to buy assets when their price drops by 5%. Mid-way targets help break down these strategies into actionable steps. The blockchain ensures these trades are executed automatically and securely.
2. Supply Chain Optimization: AI agents in logistics rely on instincts stored on the blockchain to manage the flow of goods. Instincts may direct agents to reduce delivery times, while mid-way targets specify actions like optimizing routes. The blockchain provides a transparent and auditable decision-making process.
3. Energy Grid Management: In decentralized energy markets, AI agents manage energy distribution based on instincts to minimize costs or maximize efficiency. Mid-way targets guide agents in adjusting consumption or switching energy sources, with the blockchain automating transactions when conditions are met.
4. Maximizing Account Balance: AI agents aim to maximize an account balance based on instincts that present various options, each with associated rewards and costs. The blockchain facilitates secure evaluation and execution of the most efficient decisions without requiring agents to handle private keys.
5. Gaming and Virtual Environments: In blockchain-based games, instincts stored on-chain guide AI agents in completing quests or achieving objectives. Mid-way targets help navigate in-game challenges, with the blockchain automatically triggering in-game actions when conditions are met.

### Problem Solved:

This ERC addresses the need for decentralized, common rules that guide AI agents in a secure, consistent manner. By offloading computationally intensive tasks off-chain and using the blockchain for rule enforcement and automatic transaction execution, the framework ensures interoperability, security, and efficiency across various domains.

## Discussion

We welcome feedback, suggestions, and any discussion around this proposed standard. Please review the full proposal and share your thoughts!

Link to the [ERC-7757 Pull Request](https://github.com/ethereum/ERCs/pull/596).

---

We look forward to your insights and contributions to refine and advance this proposal.
