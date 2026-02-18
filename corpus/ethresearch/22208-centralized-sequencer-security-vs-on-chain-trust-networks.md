---
source: ethresearch
topic_id: 22208
title: Centralized Sequencer Security vs. On-Chain Trust Networks
author: peersky
date: "2025-04-24"
category: Architecture
tags: []
url: https://ethresear.ch/t/centralized-sequencer-security-vs-on-chain-trust-networks/22208
views: 123
likes: 0
posts_count: 1
---

# Centralized Sequencer Security vs. On-Chain Trust Networks

*[Copy of this](https://ethereum-magicians.org/t/centralized-sequencer-security-vs-on-chain-trust-networks/23813) article exists on Magicians as I have no idea why would Eth need to have two different forum boards.*

Many security companies today are adopting a centralized, sequencer-based security approach for Layer 2 solutions. Some examples include:

- Forta: (An OpenZeppelin spinoff - hello to my ex-colleagues!) - Forta Firewall
- Ironblocks: Rollup Guard
- Blockaid: Incorporates similar concepts in its solutions.
- Countless startups are now emerging, building variations of this “AI security” model.

## Motivation

While many of these sequencer-based solutions are advertised primarily as “security,” I the motivation is twofold. Firstly, it’s an obvious path towards achieving **compliance**, which is often seen as a prerequisite for broader institutional adoption by end-users. The ability to enforce rules at a central point is arguably necessary if the Ethereum ecosystem aims for mainstream acceptance beyond its current niche. A clear application of this approach is providing a central actor to validate transaction inclusion in L2s, as exemplified by Zircuit’s [Sequencer-Level Security paper](https://www.zircuit.com/blog/the-sequencer-level-security-paper-is-out).

However, there’s a **darker side to this motivation** that security firms might not readily discuss: the security business in crypto has been exceptionally profitable, potentially *the* most profitable sector. Offering a centralized sequencer scanner as a service fits perfectly into this context. It relies on proprietary infrastructure built around a relatively simple concept, creating intellectual property that can be readily capitalized upon.

My concern is that even if this approach harms the long-term decentralization and core principles of Ethereum, these firms may pursue and lobby for it because their primary interest lies in USD revenue accumulating in fiat bank accounts, not necessarily the health of the ETH ecosystem.

*Hence, while input from “security experts” on this topic is welcome, I suggest taking it with a grain of salt, considering potential conflicts of interest.*

## Pros & Cons of Centralized Sequencing

- Pros:

Can prevent malicious transactions from appearing on-chain, potentially negating damage before it occurs.
- Relatively quick to implement for most rollup frameworks.
- Does not directly incur extra gas costs on-chain for the end-user.
- Does not require adjustments to existing smart contract code (on specifically designed rollups).
- Provides a clear business model for security firms collaborating with centralized sequencer operators and institutions.

**Cons:**

- It’s quick to implement partly because it often relies on traditional Web2 infrastructure (potentially less reliable, certainly less transparent).
- Introduces a central point of censorship (potentially enabling scenarios far removed from Web3 ideals, like selling a fiat bank account experience disguised as Web3).
- Weakens Ethereum’s key differentiator: if a central entity can override transactions, the “smart contracts are law” principle is compromised.
- Doesn’t inherently solve L1 compliance issues.
- Accounting for the scanner’s operational costs (often passed indirectly, perhaps via MEV, staking arrangements, or other fees) can be opaque and questionable.
- False positives can be exceptionally destructive. Even a mistaken flag from a wallet extension (like this example I encountered) gives developers an immediate taste of how easily they can be blocked from reaching users.
- Misses (malicious transactions that bypass the filter) can still cause critical damage, especially if not anticipated at the smart contract layer.

The definition of a “significant loss” or “malicious activity” is determined by the sequencer operator, not the user or asset owner. This leaves room for major hacks targeting new or unconventional asset types to slip through if they don’t fit the operator’s predefined criteria.
- I’d argue this situation might inadvertently benefit security firms; as the sums lost in hacks grow (like the recent ByBit case), the demand (in USD) for perceived “better” solutions increases, fueling a cycle of “re-inventions of the wheel” that prioritize central control.

## Alternative: Smart Contract-Based Networks of Trust

Examples of on-chain, smart contract-based compliance mechanisms that can work even on L1 exist today. Notable instances include Circle’s [USDC blacklist functionality](https://etherscan.io/token/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48#writeProxyContract) and Chainalysis’s implementation of the [OFAC sanctions list](https://etherscan.io/address/0x40c57923924b5c5c5455c48d93317139addac8fb). Security councils operating pause/emergency upgrade functions in DeFi protocols also fall into this category.

- Pros:

Transparent and Reliable: Operates on-chain, inheriting blockchain properties.
- Upholds Ethereum’s Core Value: Reinforces the principle that “smart contract code is law” (akin to Bitcoin’s “not your keys, not your coins,” Ethereum’s equivalent is the immutability and predictability of code).
- L1 Applicable: Can be implemented directly on Layer 1, without requiring L2 sequencer control.
- Enshrines L1 Usage: Drives demand for block space, potentially funding security through gas fees spent on valuable computation rather than just memecoins.
- Direct Cost Alignment: Transaction costs directly cover the smart contract execution expenses related to security/compliance.
- Accountable Revenue Distribution: Models like distributor contracts (e.g., in my EDS project) can use DLT to transparently account for oracle/security provider revenue.
- User-Defined Security: With proper design, can ensure that “significant loss” is defined by the asset owner’s configured policies via smart contracts, preventing unexpected large failures for specific assets.

**Cons:**

- Achieving preventative guarantees similar to centralized sequencers often requires security wrappers or modifications to existing smart contracts, adding complexity.
- Transparency is a double-edged sword: Attackers can also analyze the on-chain security logic.
- Requires substantial smart contract library development, facing the classic public goods funding problem. It’s unclear how to finance this foundational work.
- Increased gas costs, more cross-contract calls, and potentially larger deployment bytecode size.
- The current Solidity developer experience could certainly be improved to better handle the development of complex, secure systems.
- Less obvious direct business model for traditional security firms; potentially reduces the need for numerous jurisdiction-specific L2s (which could be seen as positive or negative depending on your perspective on L2 proliferation).

## Mitigating the Cons of On-Chain Trust

I argue that, with careful design and leveraging recent advancements, the “Cons” of the smart contract approach can be mitigated:

- Privacy: Technologies like Zama’s work on fhEVM enable Fully Homomorphic Encryption on-chain. This allows private logic for security oracles or compliance checks, mitigating the risk of attackers analyzing the defenses while maintaining verifiability.
- Implementation Complexity: My initiative on the Ethereum Distribution System (EDS) aims to enable “trusted networks” (conceptually similar to traditional VPNs but on-chain). Security wrappers could potentially be implemented more easily within these networks and might even work for existing codebases with minimal changes.
- Gas Costs: Increased gas costs resulting from valuable on-chain security can be viewed positively as healthy ecosystem demand for block space. I believe we should think in terms of “if applications need more gas for essential functions like security, Ethereum must evolve to provide it efficiently,” rather than avoiding on-chain solutions solely due to current gas limitations.
- Standardization & Trust: Software factories and trusted registries acting as on-chain gateways can help ensure that whatever logic a user interacts with corresponds to established compliance or security standards not just from institutional side, but also from user acceptance of such rules.
- Security Firm Role: Security firms can still play a vital role. They could build and manage sophisticated on-chain firewall contracts, offer L1 transaction signing services (perhaps enhanced by proposals like EIP-7702), and contribute expertise to the design and auditing of these trusted smart contract networks.

## The Path Forward & Funding Challenges

The public goods funding and sustainable business model aspect remains largely unresolved for the on-chain approach. I’ve implemented much of EDS myself using personal funds, driven by my belief in this direction. However, it’s a complex system and not yet ready for large-scale production use without broader ecosystem support. Acting mostly as a solitary researcher, bringing it to a production-ready state is challenging.

For instance, a proposal for [Safe DAO to support EDS development](https://forum.safe.global/t/support-eds-development-for-safe/6432/) has faced difficulties gaining traction. We also received rejections from Gitcoin OSS Tooling rounds and the Ethereum Foundation’s Ecosystem Support Program (ESP), with feedback sometimes citing metrics like low GitHub star counts – highlighting the hurdles in bootstrapping foundational infrastructure without initial backing.

Perhaps there are other promising approaches emerging? Could we potentially write sequencer-level or even beacon chain Rust contracts for compliance and security that maintain decentralization guarantees? I’m very open to discussing thoughts and alternative ideas on how we can build a more secure *and* decentralized future for Ethereum.
