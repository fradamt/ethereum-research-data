---
source: ethresearch
topic_id: 20413
title: "Resolving the Dichotomy: DeFi Compliance under Zero Knowledge"
author: Therecanbeonlyone
date: "2024-09-11"
category: Decentralized exchanges
tags: [transaction-privacy, zk-id, cryptoeconomic-tool-set]
url: https://ethresear.ch/t/resolving-the-dichotomy-defi-compliance-under-zero-knowledge/20413
views: 585
likes: 0
posts_count: 2
---

# Resolving the Dichotomy: DeFi Compliance under Zero Knowledge

This is a summary and enumeration of relevant research questions based on the recent [EEA Article by the same title as this post](https://entethalliance.org/2024-08-20-resolving-the-dichotomy-defi-compliance-under-zero-knowledge/).

**Bulleted Summary**

- DeFi protocols face a compliance challenge due to the type of assets traded and their often decentralized governance.
- A solution is leveraging blockchain-native compliance mechanisms, specifically smart contracts, and onchain verifiable zero-knowledge proofs.
- This approach ensures regulatory compliance, weighted risk management, and required transaction reporting while preserving user privacy.
- The framework attaches Compliance-Relevant Auxiliary Information (CRAI) to onchain transactions, enabling real-time compliance monitoring/verification, in a privacy-preserving way using zero-knowledge proofs.
- The framework also specifies compliance-safe DeFi interaction patterns involving using smart contract wallets, DeFi compliance contracts, a compliance smart contract system, and zero-knowledge proofs to enforce compliance rules specified in the compliance smart contract system that defines compliance policies, attestation providers, and compliant assets.
- The framework offers benefits like regulatory compliance, risk management, privacy protection, security, versatility, transparency, and accountability.
- By adopting such a framework, DeFi protocols could navigate the regulatory landscape while maintaining their core principles.
- Some of this solution already exists (compliance smart contract system, compliant assets, etc.) and need to be further expanded (smart contract wallets, compliance wrapper contracts, DeFi-specific custom hooks, etc.)

Below is a list of open research questions in no particular order:

- What are the potential challenges and limitations of implementing this framework in existing DeFi protocols?
- How can the framework’s privacy features be further enhanced to accommodate complex compliance scenarios with many compliance assertions as zkps e.g. using proof aggregation and proof recursion?
- How can the framework be extended to support a broader range of compliance requirements beyond KYC/AML e.g. incorporated DAOs, Power-of-Attorney?
- What are the potential governance challenges associated with managing and updating compliance policies within the framework?
- How can the framework’s transparency and accountability features be leveraged to further enhance DeFi e.g. custom hooks?
- How can the framework be adapted to different regulatory environments and jurisdictions?
- What are the economic implications of implementing this framework for DeFi users and protocols?

Given that part of the framework already exists, this post is to stimulate further discussion on the framework itself, and its suggested open research questions.

Looking forward to the feedback from the Ethereum research community.

## Replies

**jonhubby** (2025-07-22):

Thanks for sharing this detailed summary. The approach of using zero-knowledge proofs with smart contract systems for compliance is promising. I’m particularly interested in how proof aggregation and recursion could help scale complex compliance assertions efficiently. Curious to see more discussion on cross-jurisdictional adaptability too, seems like a key challenge.

