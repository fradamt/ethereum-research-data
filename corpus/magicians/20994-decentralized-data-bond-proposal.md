---
source: magicians
topic_id: 20994
title: Decentralized Data Bond Proposal
author: danilowhk
date: "2024-09-08"
category: ERCs
tags: [data]
url: https://ethereum-magicians.org/t/decentralized-data-bond-proposal/20994
views: 132
likes: 6
posts_count: 4
---

# Decentralized Data Bond Proposal

# Decentralized Data Bonds Standard

**Introduction:** I believe that data will become the next big asset class in the coming decades. As this transformation occurs, financial instruments will be built around it, such as ETFs, bonds, and much more.

**Why Decentralized Data Bonds?**

1. Democratization of Data Ownership: Data is perhaps the most inclusive asset class in the world. Anyone with internet access can generate valuable data. By building a permissionless and decentralized solution, we empower individuals to reclaim ownership of their data.
2. Collective Bargaining Power: Individual data points often hold limited value, but collectively, they become immensely valuable. Our standard allows users to pool their data, increasing their bargaining power and potential returns.

**How It Works**

1. Data Pools / Bonds: Users can contribute their data to specific pools or bonds. Each bond represents a collection of similar or complementary data types.
2. Verifiable Data Generation: Privately generate proofs for data with protocols such as:

Multiparty Computation (MPC) TLS
3. TLS Proxy
4. Trusted Execution Environments (TEE)
5. Tokenization: Contributors to a bond receive transferable tokens representing their share of the data pool. These tokens serve as both proof of contribution and a means to receive rewards.
6. Data Utilization: Companies, DAOs, and decentralized protocols can purchase or subscribe to access the aggregated data. Every time the data is accessed or purchased, token holders receive a yield proportional to their contribution.
7. Governance: Token holders have voting rights on decisions related to their specific data bond, such as pricing, access controls, and data usage policies.

**Example: Social Media Data Pool for LLM Training**

Imagine a Decentralized Data Bond called “Social Bond” where users can contribute their Reddit and Twitter data:

1. Users connect their Reddit and Twitter accounts to the platform.
2. The platform uses MPC-TLS to securely gather social verifiable data
3. Contributors receive “Social Bond” tokens proportional to the quality and quantity of their data.
4. An AI company developing a new language model purchases access to this data pool for training purposes.
5. The revenue from this purchase is distributed to token holders based on their contribution.
6. Token holders can vote on data usage policies, such as restricting access to non-commercial research only.

The proposed architecture consists of several key components:

1. Smart Contracts: Manage token issuance, data access rights, and reward distribution.
2. Decentralized Storage: Utilize solutions like IPFS or Filecoin to store encrypted data off-chain.
3. Prover Layer: MPC-TLS, TLS Proxy, TEE

**Challenges**

Design a secure architecture where none of the parties involved, besides the data owner and the buyer, can access the stored data.

**Next Steps**

1. Architect the standard
2. Validate with security researchers
3. Build the first open-source proof of concept

I am very happy to share my first ever ERC proposal, and hopefully we can bring a new standard to Ethereum that allows users to leverage and take back ownership of their own data.

## Replies

**lmtrarbach** (2024-09-10):

Hey! I will love to participate on that.  I have been working for a long time on the Digital Product Passport concept , you can read on github as DigitalProductPassport.

I think this is a scenario that would get a huge impact of this proposal.

Please let me know how can i help and participate.

---

**danilowhk** (2024-09-11):

For sure, the idea of this thread is for open discussion, will share my initial thoughts soon

---

**ownerlessinc** (2024-09-25):

This idea brings up several fascinating and complex questions, and I’m particularly intrigued when it comes to how the smart contract layer manages data sharing and security.

- How are the protocols (MPC-TLS, TEE, etc.) integrated into smart contracts to ensure trustless verification of data?
- Can these technologies fully guarantee that no one (including miners or validators) can intercept or manipulate the data before it reaches the intended pool? Can this be achieved by a fashion ECDSA signature?
- What level of transparency will users have regarding how their data is processed and validated? Who will decide this model or who will be entitled to determine types of models for different publics?
- The previous questions follows to this one: What mechanisms ensure the fair distribution of tokens based on the quality and quantity of data? How is “quality” defined and measured in a decentralized system? Will it be through the buyer’s feedback?
- How to address the risks of data “inflation” or manipulation where users try to game the system by contributing less valuable or even false data?
- How do you see the governance model structured?
- How can token holders ensure that their data is used ethically, and how can they enforce restrictions (e.g., non-commercial use) on data buyers?
- Will there be a transparent system for tracking how many times the data has been accessed and how much revenue is generated from these accesses? What stops a data buyer from re-selling it?
- Is the data buyable by everyone? Or there might be special terms allowing the monopolization by large buyers?
- How can we guarantee that the encryption standards are robust enough to prevent unauthorized access, both at rest (on decentralized storage) and in transit?
- There is also risks in using off-chain storage that could lead to vulnerabilities in terms of data retrieval, degradation, or corruption. How can this problem be addressed?
- Will smart contracts have to handle constant checks for encrypted access? Assuming the data provided by a pool is constantly increasing, we’d need different accesses to account for different buyers. Assuming the data size increases in both terms of quantity and quality, there is a need to increase the charge for the access. Do you have any idea how to manage and charge via smart contracts the access to this data pool? Do you think this can actually be achieved in a decentralized and seamless manner?
- Just to simplify what I asked above in other words: How will smart contracts calculate yield based on varying data contributions, given that data quality may be subjective or context-dependent?

I hope that these questions can spark deeper awareness around the complexities of decentralized data ownership and encourage collaboration among developers, researchers, and the community to co-create robust solutions for a more secure and equitable data-driven future.

I’m thankful that [@danilowhk](/u/danilowhk) is bringing this innovative concept to the table, as it opens up critical discussions and opportunities for collaboration in what I believe is the forefront of data sovereignty in machine learning.

