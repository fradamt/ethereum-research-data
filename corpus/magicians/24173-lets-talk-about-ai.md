---
source: magicians
topic_id: 24173
title: Lets talk about AI
author: kladkogex
date: "2025-05-14"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/lets-talk-about-ai/24173
views: 94
likes: 2
posts_count: 3
---

# Lets talk about AI

Hey!

The AI revolution is here — and we need:

- A bold vision for AI
- Something truly valuable to users, not just empty hype built around buzzwords like “blockchain” and “AI”

The first and most critical step is identifying a **real, significant user problem** that AI can solve.

In my view, **the problem is security**. We need to build a **self-defending blockchain** — a safe, welcoming environment for users that shuts out bad actors, including threats like North Korean hacks.

Once we identify **“self-defending blockchain”** as our goal, the next question is: *Can we build it using open-source AI?* The answer is a **resounding yes**.

---

### Two Critical Points of Defense in a Self-Defending Blockchain:

#### Point 1: Smart Contract Deployment

Valuable smart contracts are deployed **very rarely**. People usually deploy standards like ERC-20 or Uniswap once and then use them for years. That makes **contract deployment** a perfect time for the decentralized network to take time and significant computational power **analyze the smart contract and its source code using AI**.

The network can require developers to submit the **source code, test code, and test results**, ensuring the contract is properly tested.

The AI can then analyze the contract over several days and assign it a **security rating from 0 to 100**, or more intuitively: **green, yellow, or red**.

Similarly, **user addresses** can be rated for security based on factors like account age, transaction history, prior interactions, and fund flows.

#### Point 2: Smart Contract Execution

Typically, users submit transactions through wallets like Metamask — either to a smart contract or directly to another address.

Here, **AI will require a human-readable description** of the transaction, explaining what it does. The AI will **pre-execute the transaction** and engage the user in a real-time conversation, ensuring the user **truly understands what the transaction does**, where funds are going, and what risks are involved.

This conversation will use the **contract security analysis** from Point 1.

---

### Where Does the AI Run?

**a)** Community can develop **base models** for Points 1 and 2.

These models must be fast enough to run on **ETH nodes**. For contract deployment, longer runtimes (days) are acceptable. Each AI inference must be **replicated on multiple randomly chosen nodes**, and a **2/3 supermajority** will determine the consensus result.

**b)** For more advanced analysis, the network can introduce an **open auction model**, allowing **anyone in the world** to participate in the evaluation.

The contract or transaction submitter can **choose to pay** for the best answers, selected by them. High-value use cases will naturally opt for **higher-quality models**, even at a premium.

### Summary: MVP for Self-Defending AI

1. Security analysis at smart contract submission
2. Conversational AI at transaction submission — using the analysis to help users understand and avoid malicious actions

These two components must be **compatible with Ethereum ecosystem tools and APIs** to provide seamless, AI-enhanced protection.

## Replies

**HenryRoo** (2025-08-20):

It’s also worth noting that the real challenge lies in the AI systems themselves (LLM). We often don’t know where the LLM you’re using actually pulls its data from or what assumptions underlie the conclusions and outputs it generates. Despite the massive adoption, todays LLMs are far from perfect they can produce hallucinations, or even invent entirely new information as you know and I many times faced with this. And what happened if it appears during an audit/security analysis?

AI Agents are indeed powerful they can autonomously act on a defined set of inputs and even learn from them. That’s an exciting and important development. But I think we should look a bit deeper. Right now, AI feels like finance **before 2009** - closed, opaque, and without alternatives. Just as Bitcoin made financial systems more transparent and decentralized, projects like LazAI and others AI oriented protocols are doing the same for data in AI. They aim to make AI data transparent, verifiable, and decentralized, fundamentally changing the market.

In practice, this means an AI agent shouldn’t rely on opaque black-box models prone to noise or self-invention. Instead, it should be structured on top of **decentralized, tokenized data (Data Tokens)** that provide provenance, auditability, and stability while still leveraging AI components so it doesn’t degrade into a simple “if-else” script.

---

**haxolabs** (2025-08-21):

Security is the right place to focus. But we agree with the concern that opaque, black-box LLMs introduce their own risks. If a model hallucinates during contract analysis, it can create false trust, which is arguably more dangerous than no analysis at all.

The path forward feels like a layered approach:

- Deterministic checks where possible (formal verification, reproducible proofs).
- AI augmentation for interpretation and user communication, but with guardrails.
- Decentralized or verifiable data sources so the “reasoning substrate” is auditable, not opaque.

The key will be designing systems that balance trust, latency, and usability. A self-defending blockchain is possible, but it will not come from AI alone. It will come from AI embedded in resilient infrastructure.

