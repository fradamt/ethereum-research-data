---
source: magicians
topic_id: 5006
title: High-Level Overview of the Diamond Contract Pattern
author: mudgen
date: "2020-12-07"
category: Magicians > Primordial Soup
tags: [upgradeable-contract]
url: https://ethereum-magicians.org/t/high-level-overview-of-the-diamond-contract-pattern/5006
views: 708
likes: 2
posts_count: 1
---

# High-Level Overview of the Diamond Contract Pattern

Here is a good overview of [EIP-2535 Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535) and the diamond contract pattern:


      ![image](https://docs.aavegotchi.com/~gitbook/image?url=https%3A%2F%2F3848023912-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252F-MNmb4TW2v3QC3cEgBAP%252Fsites%252Fsite_qCYIv%252Ficon%252FfquVRXPsE3AcGW6cP7Y6%252FArtboard_1_copy_7with_texture_pfp.png%3Falt%3Dmedia%26token%3D0941cbd6-e40a-41a6-b89d-a544f4f505d9&width=48&height=48&sign=d8e56ded&sv=2)

      [docs.aavegotchi.com](https://docs.aavegotchi.com/overview/diamond-standard)



    ![image](https://docs.aavegotchi.com/~gitbook/image?url=https%3A%2F%2F3848023912-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Forganizations%252F-MNmb4TW2v3QC3cEgBAP%252Fsites%252Fsite_qCYIv%252Fsocialpreview%252FAzNi9tMJkBlwmQcz9cA9%252FAAVEGOTCHi_HEADER_FULL_CAST_1920px.png%3Falt%3Dmedia%26token%3D14cbe39f-4f2b-46d5-bf43-1b9fd8ba23bc&width=1200&height=630&sign=89c2619d&sv=2)

###



High-level overview of EIP-2535 Diamonds










> The diamond pattern is a code implementation and organization strategy. The diamond pattern makes it possible to implement a lot of contract functionality that is compartmented into separate areas of functionality, but still using the same Ethereum address. The code is further simplified and saves gas because state variables are shared between facets.

> The diamond pattern is a contract that uses a fallback function to delegate function calls to multiple other contracts called facets. Conceptually a diamond can be thought of as a contract that gets its external functions from other contracts. A diamond has four standard functions (called the loupe) that report what functions and facets a diamond has. A diamond has a DiamondCut event that reports all functions/facets that are added/replaced/removed on a diamond, making upgrades on diamonds transparent.

> Diamonds are not limited by the maximum contract size which is 24KB.

> Facets can be deployed once and reused by any number of diamonds.

> Diamonds can be upgradeable or immutable. They can be upgradeable and at a later date become immutable. Diamonds support fine-grained upgrades which means it is possible to add/replace/remove only the parts desired. Everything does not have to be redeployed in order to make a change. A diamond does not solve all upgrade issues and problems but makes some things easier and better.

See [the standard](https://eips.ethereum.org/EIPS/eip-2535) and the [standard’s reference section](https://eips.ethereum.org/EIPS/eip-2535#learning--references) for more information about diamonds.
