---
source: magicians
topic_id: 10263
title: NFT "leader-follower" Protocol
author: SpiderAres
date: "2022-08-05"
category: EIPs
tags: [nft, erc-721, multi-chain]
url: https://ethereum-magicians.org/t/nft-leader-follower-protocol/10263
views: 1516
likes: 4
posts_count: 7
---

# NFT "leader-follower" Protocol

## Abstract

This proposal can be regarded as an **UPGRADED VERSION** of the ERC-721 protocol, which aims to realize the convenient and continuous infinite synthesis and iteration of multi-chain NFT assets. This NFT protocol will empower cross-chain NFT assets to combine arbitrarily, combine transactions, and publish on multiple chains.

## Motivation

Now, an important factor that restricts the diversification of the gamefi track and NFT marketplace is the “ecological fragmentation”. It is true that the existence of cross-chain bridges has played a certain positive incentive for NFT cross-chain transactions and the interoperability of various public chain ecosystems, but at present, it can only do some transaction optimization for a single NFT asset.

With the goal of promoting interoperability across the blockchain industry and the concept of multi-chain coexistence, we have pioneered the EIP-xxxx protocol proposal. This proposal allows NFTs to be combined and traded across chains, and allows NFTs to be upgraded and iterated, which we also refer to figuratively as a “leader-follower” protocol relationship (as explained in ‘feature 1)’ below). This protocol will primarily apply to the further development of the Gamefi project.

## Features Introduction

**1) Cross-chain combination**

This proposal makes it possible to combine NFT assets across different chains. That is, on the basis of ensuring that the original chain of each NFT is not transferred, the cross-chain combination is carried out. By abstracting the core parameters of the NFT, we will release a unified standard protocol interface so that each cross-chain NFT asset can be successfully combined across different chains.

> Example
> A multi-chain gamefi project released the same game version on the Ethereum main network and the Avalanche network respectively. The project chose to release its limited 10,000 NFT hero characters (called NFT-A) on Ethereum, while releasing NFT accessories that can be assembled on NFT-A on the Avalanche network, such as clothing (called NFT-B), weapons (called NFT-C), ornaments (called NFT-D), etc.
> If user Mora buys heroes and accessories on two public chains, she can freely combine and assemble without swapping NFTs across two different chains.

---

**2) NFT Portfolio Trading**

With the combination of cross-chain (or same-chain) NFTs, the proposal allows the combination of integrated NFTs (i.e., NFT Portfolio) to be traded and transferred in “packages” in a combined and convenient manner, which will greatly improve the ease of trading and save on transaction Gas fees.

> Example
> Following the Example in (1) above, when user Mora assembles the NFT integration package (NFT pro) according to his preference and then shelves it on the NFT market, user Bob finds NFT pro very rare and wants to buy it. User Mora can then directly trade NFT pro with user Bob, without the need to split NFT pro and then each NFT group block for separate transactions.

---

**3) Programmable NFT**

Based on the above-mentioned cross-chain combination and packaged transactions, we will also provide an open NFT free writing interface. Chain Games project parties can customize this protocol according to the actual situation of their own projects.

> Example
> A MOBA chain game project party plans to release different special activity tasks on the two public chains, players can complete the game tasks on the two public chains and obtain NFT rewards, and all the obtained NFT rewards can realize the function of cross-chain combination and packaged trading.

---

**4) Continuous Iteration of NFT**

We will give NFT further room for creation & improvement. This protocol can allow NFTs to be adjusted and modified by parameter factors as external conditions change. Not only can it be adjusted on the basis of the original parameters, but also new parameter designs can be supplemented for NFT.

> Example
> A MOBA chain game project side has released an unevolved initial NFT hero. Players Mora in the purchase of the NFT hero, and continue to train the NFT hero and let it participate in the competition to quickly upgrade, the NFT hero can be accumulated with the experience value to continue to improve the level of evolution. At this time the NFT hero’s values (such as: force value, defense value, blast rate, etc.) will be increased.
> In addition, if players Mora want to design their own new NFT hero skin, you can create your own on top of this NFT and define the relevant parameters to achieve personalized customization of the NFT.

## Discussion points

1. ERC is an improved protocol for Ethereum. The realization of cross-chain functions with high probability requires the help of a centralized system.
2. After the user combines and assembles the NFTs on each public chain, if the main NFT-A is upgraded, can the secondary NFT-B, NFT-C, etc. be upgraded together (that is, will the secondary NFT parameters change due to changes in the primary NFT parameters? )

## Replies

**abcoathup** (2022-08-05):

You may want to consider alternative naming such as parent/child; see: [Master/slave (technology) - Wikipedia](https://en.wikipedia.org/wiki/Master/slave_(technology))

---

**riksucks** (2022-08-06):

So, from what I understand, some sort of representation is needed in this said protocol, to denote NFTs from multiple chain into one “combination”

So I believe that each smart contract in each chain will maintain the same set of combinations and when transfers or upgrades happen, each smart contract from each chain does the necessary upgrade/transfer

---

**SpiderAres** (2022-08-07):

Great, thx a lot sir ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12)

---

**SpiderAres** (2022-08-08):

**Several problems and supplements to the protocol layer**:

Q1: Which chain will this cross-chain combined NFT contract be deployed on? An NFT contract always needs to be deployed on a certain chain.

> Idea: Can be the chain where the main NFT of this combined NFT was created.

---

Q2. How can this cross-chain combined NFT transaction be realized?

> Idea: Via sidechain/relay technology.

---

Q3. How to realize cross-chain combination?

> Idea: Can be split into 2 protocols:
>
>
> Protocol 1: Programmable NFT combination protocol of the same chain
> Protocol 2: NFT protocol for cross-chain combination
> In this way, each protocol only considers and solves a separate problem. Protocol 1 solves the problem of combinatorial programming between NFTs; Protocol 2 solves the problem of combination of cross-chain NFTs.

---

**anett** (2022-08-09):

Trying to understand your idea, so you want to build cross-chain protocol layer. So something like OpenSea but support more chains or something like NFT game with cross chain support, maybe like Enjin whom founders co-authored ERC-1155. Maybe peak into NFT projects on different chains and you may find a way how to combine more NFT projects into one and create perfect solution for your ideas ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Edit: I think this proposal extends your ideas data-wise [Minimalistic on-chain cross-game NFT attributes](https://ethereum-magicians.org/t/minimalistic-on-chain-cross-game-nft-attributes/7823)

---

**SpiderAres** (2022-08-16):

With the help of community partners, this proposal idea can be solved by ERC-998 combined with cross-chain protocol. Next, our team will focus more on the implementation of the front-end, and realize the ideas into applications, so that everyone can produce NFT collections across different chains, and trade the NFT collections package. ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

