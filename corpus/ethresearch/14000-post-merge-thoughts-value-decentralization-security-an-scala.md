---
source: ethresearch
topic_id: 14000
title: "Post-merge thoughts : value, decentralization, security an scalability"
author: Michael2Crypt
date: "2022-10-22"
category: Architecture
tags: []
url: https://ethresear.ch/t/post-merge-thoughts-value-decentralization-security-an-scalability/14000
views: 1816
likes: 0
posts_count: 2
---

# Post-merge thoughts : value, decentralization, security an scalability

It is more and more acknowledged that the best situation for Ethereum utility and value is the following positioning :

[![triangle2](https://ethresear.ch/uploads/default/optimized/2X/9/9f34974478a500182462fbfd7c1ec72cc3faf0d0_2_690x466.jpeg)triangle2714×483 37.2 KB](https://ethresear.ch/uploads/default/9f34974478a500182462fbfd7c1ec72cc3faf0d0)

**Decentralization +++** : very good level of decentralization

**Security +++** : very good level of security

**Scalability =** : not so good scalability, because improving scalability is reducing decentralization and / or security ([Blockchain trilemma, CAP Theorem](https://www.gemini.com/cryptopedia/blockchain-trilemma-decentralization-scalability-definition)). As a result, scalability is devoted to L2 and L3 layers.

Currently, Ethereum is more or less here :

[![triangle3](https://ethresear.ch/uploads/default/optimized/2X/2/2fa25a27944eef7c1c8c4619a3b701157f360fcd_2_690x466.jpeg)triangle3714×483 31.8 KB](https://ethresear.ch/uploads/default/2fa25a27944eef7c1c8c4619a3b701157f360fcd)

**Decentralization +** : currently, the vast majority of Ethereum nodes are running on AWS, as much as 90 % according to [cointelegraph](https://coinmarketcap.com/alexandria/article/disappointing-coinbase-and-lido-dominate-ethereum-staking-rewards-after-the-merge). Most nodes are managed by a few actors : Lido, Coinbase, …

**Security ++** : the technical level of security seems very good, but with such centralization of nodes, there are security and censorship risks. For example, due to the fact that most nodes are running in the US on AWS, the SEC claims is has a jurisdiction on all Ethereum transactions :

*ETH contributions were validated by a network of nodes on the Ethereum blockchain, which are clustered more densely in the United States than in any other country. As a result, those transactions took place in the United States.*  [Coinmarketcap](https://coinmarketcap.com/alexandria/article/sec-argues-u-s-has-jurisdiction-for-ethereum-blockchain-in-new-court-filing)

As a result of the SEC jurisdiction claims, there will be more pressure to censor transactions.

**Scalability =** : the blockchain is pretty fast, even if the number of transactions is limited.

[![triangle4](https://ethresear.ch/uploads/default/optimized/2X/f/fefdaa389f50796dd1e3ee512322d3cf5165d309_2_690x466.jpeg)triangle4714×483 35.3 KB](https://ethresear.ch/uploads/default/fefdaa389f50796dd1e3ee512322d3cf5165d309)

A few thoughts and suggestions :

A priority should be to increase decentralization : solo validation should be the norm, it is currently the exception. If you look at the Ethereum website and look for information to run a node, you get here : [How to Run an Ethereum Node](https://ethereum.org/en/run-a-node/) You have a link to a website called dappnode, with a shop https://www.dappnode.io/collections/frontpage

There is little information, is this an independent project, how reliable is it, is it really non custodial … ?

If you look further, you learn that you can delegate the everyday management of a node with a “staking as a service” provider :  [Staking as a service | ethereum.org](https://ethereum.org/en/staking/saas/) According to the page, the only open source and audited provider is BloxStaking. Yet, it has very little popularity, with less than 1000 subscribers on their youtube channel.

Once again, how reliable is it, is it really non custodial … ?

Currently, running a node is too complex and too demanding. As a result, Eth users turn to Lido, Coinbase and other big actors. And **even these big actors are afraid not to be able to run nodes properly** in an efficient way, that’s why they turn to AWS.

Currently, Ethereum is mostly running inside Amazon highly specialized cloud factories.

To improve decentralization, a few ideas :

- building official and user friendly tools and clients, that would enable Eth users to engage easily into solo staking
- making node installation easier for smaller cloud providers, in order to reduce AWS dominance. Make sure non custodial solutions are possible and easy to implement.
- reducing scalability by slowing the blockchain : there is no need to have a block every 13 seconds. 30 - 45 seconds would be enough, and it would enable slower computers, slower internet connections, increase the tolerance to computers which are offline, … Once again, scalability is a thing that L2 and L3 have to manage, L1 has to focus on decentralization and security.
- reconsidering slashing : solo validators are not supposed to be node experts, they have their lives, jobs and occupations. They fear to lose their capital if there is a slashing. With a slower blockchain, it would be possible to just blacklist bad actors, and to implement more security procedures during the production of the bloc, making slashing unnecessary.

To increase scalability, more tools are needed to build L2 and L3 layers more easily. There are currently only a few actors providing L2 layers, while an intense competition is needed to reach mass and fast transactions with zero fee. There should be official and open source solutions for people and firms who would like to run a L2 or a L3 layer.

Security is also security of funds, financial and fiscal security. I made a [topic a few months ago about these aspects](https://ethresear.ch/t/please-separate-staking-revenue-from-staking-capital/12345). In particular, validators should have the option of collecting the income of staking on a separate Ethereum address of their choice.

## Replies

**MicahZoltu** (2022-10-23):

You should change “decentralization” to “censorship resistance” in your triangle.  Decentralization is one means of censorship resistance, but it isn’t a goal in itself.

Also, while the end-game of the current roadmap may be a focus on decentralization and security, the path we are currently on takes us *away* from decentralization in an attempt to become more scalable, with plans to "eventually fix the decentralization/censorship resistance problems that we create along the way.

