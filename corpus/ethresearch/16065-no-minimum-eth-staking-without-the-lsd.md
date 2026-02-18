---
source: ethresearch
topic_id: 16065
title: No minimum ETH Staking without the LSD
author: natemiller
date: "2023-07-07"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/no-minimum-eth-staking-without-the-lsd/16065
views: 2512
likes: 1
posts_count: 2
---

# No minimum ETH Staking without the LSD

Existing ETH staking-as-a-service providers typically require users to deposit a full balance of 32 ETH or deposit funds into [inherently centralized liquid staking derivative](https://notes.ethereum.org/@djrtwo/risks-of-lsd) (LSD) protocols. However, relying on a third party in LSD protocols introduces certain counterparty risks, including the potential centralization of node operators, the vulnerability of validator signing keys to ransom attacks, and the management of stake balances leading to potential ETH being stuck or lost. Furthermore, the concentration of ETH within these centralized entities amplifies the potential impact of exploited risks.

More significantly, as additional opportunities in the Ethereum ecosystem grow, such as Eigenlayer. Single purpose LSDs are too inflexible to provide the optionality that ETH stakers have and will continue to have. It will be important to have a UI that allows users to natively choose where they want their staked ETH to go. By removing the middleman, this direct staking process opens up possibilities for stakers to earn additional rewards and maximize their returns.

For these reasons we’re building Casimir SelfStake to empower stakers with greater control over their assets and the ability to tap into emerging opportunities within the Ethereum ecosystem.

Casimir SelfStake offers a different approach where stakers can directly deposit any amount of ETH to highly capable Ethereum operators through a factory smart contract model. This approach minimizes counterparty risk for users and enhances the decentralization of Ethereum staking. Validators’ duties are carried out by openly registered and collateralized operators using distributed validator technology (DVT). Trustless key management is achieved through zero-coordination distributed key generation (DKG). Automated actions, such as compounding stake or handling a slash, are executed by a decentralized oracle network (DON). Furthermore, the user experience is improved through the use of account abstraction to wrap staking contract actions.

We’re looking for feedback, discussion, and mentorship from the broader community on this project. We believe this methodology can help enable a more decentralized and trustless approach to Ethereum staking without sacrificing scalability, usability, or staking yield.

You can follow our work here: [GitHub - consensusnetworks/casimir: 🌊 Decentralized staking and asset management](https://github.com/consensusnetworks/casimir)

## Replies

**chloefeal** (2025-01-02):

Thank you [@natemiller](/u/natemiller) for your hard working on Casimir SelfStake. This direct staking process opens up possibilities for stakers to earn additional rewards and maximize their returns, and in my opinion, the most important thing is the concentration of ETH within these centralized entities amplifies the potential impact of exploited risks.

