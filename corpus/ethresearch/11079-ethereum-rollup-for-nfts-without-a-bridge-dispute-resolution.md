---
source: ethresearch
topic_id: 11079
title: Ethereum rollup for NFTs without a bridge/dispute resolution contract
author: musalbas
date: "2021-10-22"
category: Layer 2
tags: []
url: https://ethresear.ch/t/ethereum-rollup-for-nfts-without-a-bridge-dispute-resolution-contract/11079
views: 4492
likes: 5
posts_count: 8
---

# Ethereum rollup for NFTs without a bridge/dispute resolution contract

One common misconception of rollups is that they all require an on-chain dispute resolution contract in the form of a light client implemented as a smart contract. This is only true if the rollup needs a two way bridge with some other chain (i.e. the Ethereum parent chain), which is not necessary for all use cases.

Consider a rollup for recording the ownership of NFTs. You can achieve all the same functionalities as a standard rollup (i.e. a trust-minimized bridge between the rollup and the main chain), without a dispute resolution on the Ethereum chain. Instead, you only need a one-way read-only bridge for the NFT rollup to read the Ethereum chain state.

Let’s assume a rollup for recording the ownership of NFTs, that uses Ethereum for data availability, but does not have a bridge/dispute resolution contract on the Ethereum chain. Now, let’s assume that an owner of an NFT on the rollup wants to use the NFT for some DeFi application on the Ethereum main chain or one of its rollups, e.g. use the NFT as collateral for a loan. How would they do this?

Owners of NFTs on the rollup can create a ‘wrapper NFT’ on the main Ethereum chain (or some rollup like Arbitrum connected to the Ethereum chain). The rollup’s state transition function would be designed such that whoever owns the wrapper NFT on Ethereum, also owns it on the rollup, because the rollup clients would also run Ethereum nodes.

The fraud proofs and validity proofs would be shared on the peer-to-peer layer of the rollup’s subnet, rather than posted on any chain, so the rollup’s light clients can still reject invalid blocks. This is similar to Mina validity proofs, or if you were to add fraud proofs to Bitcoin light clients - they don’t need to be posted to any on-chain dispute resolution layer.

To determine if a wrapper NFT is valid or not, you would need to follow the canonical rollup chain to check that the wrapper NFT was minted correctly. This means that a smart contract on Ethereum wouldn’t be able to check if the wrapper NFT was valid or not without a dispute resolution contract, but this doesn’t matter. The status quo is already that because anyone can obviously create a worthless NFT, you need to check the value of an NFT off-chain anyway before e.g. offering to lend someone funds collateralized by it. Checking whether the wrapper NFT is valid or not is a part of checking whether the NFT has value. Checking what the value of ETH itself within a DeFi protocol for example is a similar problem; protocols like Maker use external price oracles.

The key intuitive here is that: you need a two-way bridge and therefore on-chain dispute resolution, only if you want to move assets (e.g. ETH) ‘hosted’ on the Ethereum chain, but not necessarily vice verse (e.g. moving an NFT from the rollup to the Ethereum chain).

## Replies

**MicahZoltu** (2021-10-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> The fraud proofs and validity proofs would be shared on the peer-to-peer layer of the rollup’s subnet, rather than posted on any chain, so the rollup’s light clients can still reject invalid blocks.

This is the hard part I think.  How do you come to consensus on what the latest state is?  If you are a new participant in the network, the only way to get to the latest state is to re-execute everything from the beginning, and if two clients disagree on what the latest state is you don’t have a mechanism for recognizing and resolving that disagreement autonomously.

---

**adlerjohn** (2021-10-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> How do you come to consensus on what the latest state is?

[This paper](https://bitcoin.org/bitcoin.pdf) is a good introduction to how multiple nodes in a decentralized network can all agree on the same state.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> if two clients disagree on what the latest state

Transactions in a blockchain are executed deterministically. It’s not possible for two nodes that see the same transactions in the same order to disagree. The above-linked paper describes this as well.

---

**MicahZoltu** (2021-10-23):

That paper describes how to build a Proof of Work based blockchain.  In this case, you won’t have a proof of work chain so you won’t have a clear mechanism for coming to consensus.  If all transactions are submitted through L1, you can solve the ordering problem, but you still don’t have a mechanism for ensuring that everyone is in sync and a subtle bug didn’t result in a desync between peers.

You could setup a gossip network and have peers share the root of their latest state, but you have no sybil resistance so someone can lie about what they believe actual state is and force the network to deal with it.  The network cannot automatically recover when there is disagreement about current state, and new peers only option is to rebuild full state from scratch.  You can’t have light clients either.  When there is a divergence like this humans will need to investigate but since you don’t have Sybil resistance an attacker can just pretend like a bunch of peers ended up with a different state.

---

**musalbas** (2021-10-24):

As the rollup blocks are ordered (e.g. posted on a consensus and data availability layer), it’s not possible for correctly functioning full nodes for a rollup to disagree on what the latest state for the rollup is, after they re-execute everything, because the state machine is deterministic.

---

**MicahZoltu** (2021-10-24):

This is true only if there are no bugs in the state machine implementation that can cause divergence.  Ethereum has 4 clients, and they have had a number of bugs in the past that would cause them to disagree on state.  By having the state root be part of consensus, you ensure that everyone believes state is the same, and if someone doesn’t they can quickly notice.

At the most extreme, you have a solar flare that causes a client to have a state that differs from everyone else.  In order for the system to work properly, everyone needs to agree on both the state transition rules **and** the current state.  While you can certainly *hope* that everyone agrees on state, there is huge value in ensuring that at the consensus layer.

---

**musalbas** (2021-10-24):

If a node has a bug, then it’s not a correctly functioning node, and will hard fork from the network. This isn’t a problem specific to this proposal, but all blockchains in general. Adding the state root to the consensus won’t help you, because the buggy full nodes will still reject blocks they consider invalid and hard fork.

---

**MicahZoltu** (2021-10-24):

You’re correct, if your client has a bug you will fork from the network.  What is important here though is that with state being part of consensus you will *notice* when you fork away from the network because you’ll stop receiving new blocks.

With this proposal, when you fork away from the network you’ll continue processing transactions and over time your state will diverge from reality more and more and you won’t know it.  At some point in the future you’ll try to interact with another user such as by receiving a transfer from them, and you will not receive it according to your client.  Hopefully you notice this before you get ripped off by someone faking a transfer to you.

