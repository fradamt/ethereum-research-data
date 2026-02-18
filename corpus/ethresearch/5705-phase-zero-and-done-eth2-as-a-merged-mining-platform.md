---
source: ethresearch
topic_id: 5705
title: "Phase Zero and Done: eth2 as a merged mining platform"
author: atoulme
date: "2019-07-05"
category: Sharding
tags: []
url: https://ethresear.ch/t/phase-zero-and-done-eth2-as-a-merged-mining-platform/5705
views: 3007
likes: 5
posts_count: 5
---

# Phase Zero and Done: eth2 as a merged mining platform

# Origin

ETHv2 phase zero is now around the corner, with a spec freeze, implementers busying themselves with the networking and productization of the clients, and a flurry of activity looking towards the horizon.

This post is related to “Phase One and Done”, and meant as a simplification of the ecosystem to see if we could find utility in phase zero.

Phase zero sets up the beacon chain. It is used to create a peer-to-peer network infrastructure of beacon nodes, to which validators connect to, providing votes for blocks.

This is a bare bones architecture for proof of stake.

We have seen [merged mining](https://tlu.tarilabs.com/merged-mining/merged-mining-scene/MergedMiningIntroduction.html#what-is-merged-mining) being explored and discussed in particular in this [paper](https://arxiv.org/abs/1904.06441).

Phase zero has little intrinsic value by itself as of now, so there is a chance it will take time for it to catch on.

Interestingly, some of the folks on the research team have looked at making it useful by [providing finality to the ETH 1 chain](https://medium.com/@ralexstokes/the-finality-gadget-2bf608529e50).

This post is a generalization of that approach to any chain or sidechain that would like to use ETHv2 to provide security through PoS and finality through beacon chain finality.

# Proposal

## Propose blocks containing 32 bytes hashes

We propose to allow a mechanism by which beacon chain blocks may embed a number of hashes provided. If you want to add a hash to a block, you’ll need to sign and propose a block on your turn with the hash in it.

## Potentially pay for proposing those blocks

We may request that whoever proposes a block with such additional data adds the hash of a transaction of a payment to an ETH1 contract showing that they properly paid for their block proposal, and signs the block with the key of the originator of the transaction.

Maybe. We could also make it free for a while, but it’d be good to give money to those brave stakers, eventually.

# Benefits

Well, it gets a bunch of folks running beacon chain nodes. It gets money in the staker pockets.

And it allows scaling by having multiple chains use PoS as a security mechanism.

## Replies

**adlerjohn** (2019-07-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/atoulme/48/1534_2.png) atoulme:

> We have seen merged mining  being explored and discussed in particular in this paper .

As the primary author on that paper, allow me to make some nitpicks. The paper presents a scheme for *merged consensus*, not merged mining/staking. Unlike merged mining, merged consensus is a consensus protocol that can be introspected entirely on-chain (with some optimism and synchrony assumptions). This allows for permissionless trust-minimized side chains.

This intuition can be found in my post on [Minimal Viable Merged Consensus](https://ethresear.ch/t/minimal-viable-merged-consensus/5617), namely

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png)[Minimal Viable Merged Consensus](https://ethresear.ch/t/minimal-viable-merged-consensus/5617/1)

> This scheme can be thought of as an optimistic execution engine on top of ordered data. The main chain (Ethereum) block producers are only responsible for consensus on ordering transaction data and processing proofs of incorrect execution.

It’s important that the side chain’s consensus protocol’s safety be guaranteed modulo trivial assumptions, otherwise you’d be scaling throughput at the cost of funds being easily stolen. You can’t get this guarantee with merged mining/staking, so that avenue of scaling is largely a dead end. (Merged mining only provides security against external attackers, not state safety.)

---

**atoulme** (2019-07-07):

Hello John,

Thanks for the clarifications. I am so happy to see your response here. Thanks for the nitpicks, and sorry I mischaracterized your paper.

I’ll refine my thinking a bit. There is indeed no silver bullet, and you should not rely on merge mining as a way to secure a chain without other means. The chain still needs to provide its own security.

However, having a merge mining mechanism provides finality and the ability to peg chains to each other so it becomes easier to create bridges. One such recent effort was started with Syscoin for example, currently against Eth 1.x: https://github.com/syscoin/sysethereum-docs

We can make it easier to transact value this way.

Separately from this bridge mechanism, Syscoin has its own consensus algorithm *and* merge mines with bitcoin (https://syscoin.org/about/). So there is value for them for example to support Ethereum merge mining.

More in line with your thinking, the Plasma group has been working towards the “general purpose plasma” idea that, as I understand it, allows to introspect the plasma transaction. You know more than me on this though.

---

**vbuterin** (2019-07-09):

> We propose to allow a mechanism by which beacon chain blocks may embed a number of hashes provided. If you want to add a hash to a block, you’ll need to sign and propose a block on your turn with the hash in it.

Is the idea that validators would vote on whether or not those blocks are available? If so, how is this different from phase 1?

---

**atoulme** (2019-07-17):

Right, the validators would send block hashes as part of their attestations. Is this exactly phase 1? I confess I didn’t read phase 1 much yet.

