---
source: ethresearch
topic_id: 7714
title: Trustless staking pools - POC
author: alonmuroch
date: "2020-07-19"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/trustless-staking-pools-poc/7714
views: 1300
likes: 4
posts_count: 1
---

# Trustless staking pools - POC

A POC and better defined operations for a trustless staking pool based on previous posts:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png)

      [Abstract trustless pool with participant rotation](https://ethresear.ch/t/abstract-trustless-pool-with-participant-rotation/7332) [Economics](/c/proof-of-stake/caspers-economic-incentive-structures/11)




> For an overview of trustless pools, click here
> An extension to the described above is a protocol that enables an abstraction of the pool participants where a large set of participants pool is divided into committees for a defined time period, when that period finishes all participants are rotated to a different pool randomly.
> Very similar to committee selection on the beacon-chain.
> An overview will look like:
>
>
> At every epoch E_i, from a large set of participants, divide all into fixed sized…



    ![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png)

      [Trustless staking pools with a consensus layer and slashed pool participant replacement](https://ethresear.ch/t/trustless-staking-pools-with-a-consensus-layer-and-slashed-pool-participant-replacement/7198) [Economics](/c/proof-of-stake/caspers-economic-incentive-structures/11)




> I’ve seen a few talks about decentralised, trustless pools including one made by Carl Beekhuizen & Dankrad Feist (Devon 5). I wanted to describe a more detailed system of how this might look like in a real-world application.
> This is also my first post on ethresear.ch so that’s exciting!
> introduction
> The need behind staking pools is simple, as ETH price goes up so does the cost of becoming a validator. Many won’t be able to put 32 ETH when ETH is $500 or $1000.
> This will encourage centralized…

The [go-minimal-pool](https://github.com/bloxapp/eth2-staking-pools-research/tree/master/go_minimal_pool) project establishes a minimal POC for creating validator pools, jointly signing attestations and rotating participants between pool for randomness security.

For the full research and POC project:

https://github.com/bloxapp/eth2-staking-pools-research
