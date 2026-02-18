---
source: magicians
topic_id: 1658
title: Mosaic to scale dapps asynchronously on-chain
author: schemar
date: "2018-10-24"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/mosaic-to-scale-dapps-asynchronously-on-chain/1658
views: 582
likes: 2
posts_count: 1
---

# Mosaic to scale dapps asynchronously on-chain

Dear Magicians,

we are implementing a BFT scaling solution for dapps that runs on-chain and we are looking for your feedback and questions.

We extend the state and transaction space by adding auxiliary systems (side-chains) and only committing roots back to Ethereum.

In very simple terms think of it as a combination of Casper FFG and sidechains.

One difference to Plasma is that we have an open set of validators that is staked on Ethereum. That set of validators observes the side-chain and commits state roots. Furthermore, the asynchronous nature does not put a time constraint on a mass-exit.

One difference to Ethereum v2 (shasper) is that we can add an arbitrary number of side chains. In future work it can be extended to a second order depth of finalization. Mosaic would run on Ethereum v2 as well, of course.

**You can find the current draft of the paper here:**



      [raw.githubusercontent.com](https://raw.githubusercontent.com/OpenST/mosaic-contracts/develop/docs/mosaicv0.pdf)



    https://raw.githubusercontent.com/OpenST/mosaic-contracts/develop/docs/mosaicv0.pdf

###



1561.96 KB










**From the abstract:**

> Mosaic is a parallelization schema for decentralized applications. It introduces a set of Byzantine fault-tolerant consensus rules to compose heterogeneous blockchain systems into one another. Decentralized applications can use Mosaic to compute over a composed network of multiple blockchain systems in parallel.
>
>
> The Mosaic consensus rules are asynchronous and as a result the state transitions of the meta-blockchain can span an arbitrary time length and an arbitrary amount of computation. This includes the exit procedure.
>
>
> The computational effort required by the origin blockchain to (challenge and) commit a meta-block is constant in the computation executed and scales linearly in the number of validators.

We are very interested in critical feedback and questions.

One open topic, which we also haven’t solved yet, is the proving of an invalid state transition in the case when more than 2/3 of the validators collude.

The source code is work-in-progress and lives here: [GitHub - OpenST/mosaic-contracts: Mosaic-0: Gateways and anchors on top of Ethereum to scale DApps](https://github.com/openstfoundation/mosaic-contracts)

If you want, you can also ask your questions on https://discuss.openst.org
