---
source: ethresearch
topic_id: 16512
title: An appchain-based approach to Eth Rollups with Ethlets
author: jinghiskwon
date: "2023-08-30"
category: Layer 2
tags: []
url: https://ethresear.ch/t/an-appchain-based-approach-to-eth-rollups-with-ethlets/16512
views: 1180
likes: 1
posts_count: 2
---

# An appchain-based approach to Eth Rollups with Ethlets

I am new here, but I’ve been contributing to the Cosmos ecosystem for a few years now and now one of the team members at Saga. One of the things our team has been focused on this year is bringing the Cosmos appchain tech stack to complement Ethereum scalability.

I wanted to post this here to gather some feedback on our idea and see if there’s complementary technology solutions or other research we can leverage to make our product better.

We just announced Ethlets today [here](https://medium.com/sagaxyz/improving-ethereum-scalability-with-saga-ethlets-236685a51e8c). TL;DR version of the article below…

**Every Ethlet begins as a Chainlet**

Saga is a chain that launches other chains (an L1 to launch other L1s). The Saga Mainnet automatically and permissionlessly launches fully decentralized PoS appchains called Chainlets. Each Chainlet is fully secured by Saga Mainnet validators using Cross-Chain Validation (i.e., validators are shared across many chains). Every Chainlet is EVM compatible.

**When the developer is ready, they can convert a Chainlet into an Ethlet**

Converting a Chainlet into an Ethlet is an easy process (submitting a transaction on Saga mainnet). Upon conversion, Ethlets begin submitting state hash into the Ethereum blockchain once an epoch (about a day). Ethlets inherits Ethereum Security through an optimistic fraud proof (either optimistic ZK or interactive proof) mechanism.

**We believe Saga Ethlets combine the best qualities from every scaling solution into an easy-to-use product**

Saga Ethlets are the most affordable solution compared to alternative scaling strategies

- Fraud proofs are only generated and run optimistically, enabling lower costs and speedups
- Self-contained DA — do not need to pay Ethereum for DA
- State commitments to Ethereum only happen once per epoch
- Ethlets feature commodity pricing through our Chainlet auction mechanism

Saga Ethlets have the best security tradeoffs

- Prior to the challenge period, there is still significant economic security with Saga staked
- After the challenge period, the Ethlet inherits full Ethereum security
- Most secure because it does not rely on single sequencers
- No need for external auditors — Due to PoS, there is always an automatic set of auditors (other validators) who verify state hashes

Saga Ethlets have instant finality and therefore fast bridging. As long as the bridge operators and the counterparty chain trust Saga security, the bridges can have instant finality. Finally, Saga Ethlets are incredibly easy to provision with one-click deployment.

To summarize: we would love to get some feedback on this idea. I believe there are significant synergies with combining Cosmos and Ethereum research and development into scalability solutions. For one, our Chainlets and Ethlets will be fully IBC compatible at day-1. We would love to discuss!

## Replies

**maniou-T** (2023-09-04):

I like the idea that combining the Cosmos Lisk technology stack with the scalability of Ethereum is a compelling technological prospect. I look forward to seeing the further development of this project.Thank you for sharing this inspiring vision!

