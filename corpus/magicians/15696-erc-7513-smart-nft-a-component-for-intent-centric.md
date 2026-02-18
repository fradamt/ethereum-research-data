---
source: magicians
topic_id: 15696
title: "ERC-7513: Smart NFT - A Component for Intent-Centric"
author: MJ_Tseng
date: "2023-09-06"
category: ERCs
tags: [nft, erc-721, erc1155]
url: https://ethereum-magicians.org/t/erc-7513-smart-nft-a-component-for-intent-centric/15696
views: 2061
likes: 7
posts_count: 4
---

# ERC-7513: Smart NFT - A Component for Intent-Centric

Smart NFT is the fusion of Smart Contract and NFT. An NFT with the logic of a Smart Contract can be executed, enabling on-chain interactions. Transitioning from an NFT to a Smart NFT is akin to going from a regular landline telephone to a smartphone, opening up broader and more intelligent possibilities for NFTs.

EIP: [ERCs/ERCS/erc-7513.md at erc-7513 · TsengMJ/ERCs · GitHub](https://github.com/TsengMJ/ERCs/blob/erc-7513/ERCS/erc-7513.md)

PR: [Add ERC: Smart NFT - A Component for Intent-Centric by TsengMJ · Pull Request #73 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/73)

## Replies

**0xmu** (2023-09-25):

Love this idea to explore the function modularization through NFT.

When you mention Intent Abstraction, are you referring that the solver to fetch and concatenate appropriate modules with high security and execute them?

(and maybe whats the relationship of this idea and 6551?)

---

**MJ_Tseng** (2023-09-26):

Yes, we believe that complex interaction processes can be abstracted into reusable functional modules. This is the foundation for efficient and secure implementation in an intent-centric manner.

While we are all NFT-bound, what EIP-6551 achieves is providing an associated contract address for NFTs to store assets. On the other hand, this EIP aims to package code that can perform specific functions into NFTs. Before this, there wasn’t a secure on-chain way to trade code or transfer contract permissions. With this EIP, it’s possible to achieve this through NFTs on any NFT marketplace.

---

**cleanunicorn** (2023-12-19):

I recently wrote a detailed study on Intents.

This is for those who seek a thorough understanding of the reasons for and against the proposal.

https://www.edenblock.com/post/the-next-blockchain-bull-run-user-intents-paving-the-way-for-mass-adoption

