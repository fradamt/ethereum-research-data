---
source: ethresearch
topic_id: 20560
title: Can Ethereum Distribution System reduce disk space usage & enable object passing?
author: peersky
date: "2024-10-04"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/can-ethereum-distribution-system-reduce-disk-space-usage-enable-object-passing/20560
views: 235
likes: 0
posts_count: 3
---

# Can Ethereum Distribution System reduce disk space usage & enable object passing?

Im looking for a developer community feedback for Ethereum Distribution System project: a generalized, semver enabled fully-on chain distribution system (generalized factory)

Please reach back in thread or leave comments in discussion tab on github! ![:handshake:](https://ethresear.ch/images/emoji/facebook_messenger/handshake.png?v=14)



      [github.com](https://github.com/peeramid-labs/eds)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/2/1/2111073e9b47bb8519e80ed41057a4c607c5bc38_2_690x344.png)



###



Ethereum Distribution System










**TLDR, hypotesis I want to validate:**

### Hypotesis 1

The current landscape of smart contract distribution on the Ethereum network is fragmented and inefficient.

Mostly, projects generate numerous deployment artifacts that **cannot be optimized in database**(?) because of built metadata affects code hashes.

This practice results in a increase in blockchain size for node operators, far beyond what is necessary.

This likely is much below what storage / tx takes, however, contrary to tx data, bytecode is not something nodes can prune, meaning in the long run it may become more actual?

I am not familiar with how execution clients store contract bytecode, but I doubt they split metadata objects in separate table, and even if, the smart contract devs are not incentivised to re-use heavily and likely anyway produce overhead number of artefacts

### Hypotesis 2

Newer ecosystems such as Sui claim competitive advantage over Ethereum, for example, for being able to pass objects between contracts.

From my understanding, the EVM is eventually right concept because it allows to build similar abstraction model on top, as it is just a computer architecture.

With stateless Distributions proposed in EDS, **it is possible to write software that will enable functionality similar as Sui proposes** on inside evm. ( e.g,: Two applications distributed trough same distribution / distributor do not need for user explicit `approval`s as they are by design distributed together. )

### Hypotesis 3

Distributions that are stateless chunks of code, in principle could be used to provision execution layer migration scripts for the whole protocol.

EIP 7702 discussion is exemplary for this, it’s a breaking change for many security assertions.

It could be presented as “Ethereum 3.0”, a network within a network, where upon fork day, Beacon chain promises to migrate all of infrastructure that community added and then do user states (assets) migration ad-hoc whenever users reach out to designated migration contract.

### Open questions

How dumb am I ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) any of these hypothesises can hold their truth?

Can bytecode size on Ethereum become a problem in foreseeable future?

I’ve encapsulated proposal to enshrine use of bytecode hashes in [ERC7744](https://eips.ethereum.org/EIPS/eip-7744) however If this proves to be very helpful, perhaps it’s worth to move in EIPs?

If EDS proves to have positive perception, this implies that there will be extensive use of proxies instead of new deployments, perhaps an EIP needed to bake native proxy support for this (even if not, proxies are very popular) ?

## Replies

**defitricks** (2024-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/peersky/48/10864_2.png) peersky:

> Can bytecode size on Ethereum become a problem in foreseeable future?

Yes, bytecode size on Ethereum could become a problem in the foreseeable future. As smart contract deployments increase, bytecode cannot be pruned by nodes like transaction data, leading to inefficiencies in storage. The Ethereum Distribution System (EDS) proposal aims to address this by optimizing code distribution and encouraging proxy use, potentially alleviating some of the bytecode bloat. However, without such solutions, the growing bytecode footprint may become a more significant issue for Ethereum node operators

---

**peersky** (2024-12-11):

I created [EIP-7784: GETCONTRACT opcode](https://eips.ethereum.org/EIPS/eip-7784) to address this

