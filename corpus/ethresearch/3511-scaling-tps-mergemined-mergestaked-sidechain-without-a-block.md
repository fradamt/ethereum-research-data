---
source: ethresearch
topic_id: 3511
title: "Scaling tps: Mergemined/Mergestaked sidechain without a blocksize limit"
author: olivierjanss
date: "2018-09-24"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/scaling-tps-mergemined-mergestaked-sidechain-without-a-blocksize-limit/3511
views: 1239
likes: 4
posts_count: 5
---

# Scaling tps: Mergemined/Mergestaked sidechain without a blocksize limit

A couple of days ago I tweeted: “Lightning/Plasma alternative: Has anyone considered just creating a mergemined sidechain without a blocksize limit? Lock coins from main chain to sidechain, miners get tx fees and specialize in large scale nodes. POW/S=The real power, and mergemining is vastly underestimated/used”.

I think mergemining or “mergestaking” has huge untapped potential for scaling Ethereum (and beyond). Paul Sztorc reacted to my tweet and said this:

"We will release both BTC and BCH versions of a largeblock sidechain softfork pretty soon. First testnet release almost ready.”

He also made an interesting youtube video,explaining the concept:

Has anyone explored the concept yet?

## Replies

**vbuterin** (2018-09-24):

I think we tend to dislike mergemining and mergestaking because it either massively increases the load required by miner/validator nodes or harms security. That is, if *almost everyone* participates in the drivechain it gets security but then the resource requirements for participation go waaay up, so it’s similar to just increasing blocksize of the base chain, and if few people participate then the amount of resources needed to 51% attack it are fairly small.

Now technically you could have many drivechains with an 8M gas limit and randomly sample PoS validators for each one, so that an attacker cannot target a specific chain to attack with a small number of validators, but then that does get pretty close to what sharding is ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**MihailoBjelic** (2018-09-24):

I never understood the potential of mergemining, indeed. AFAIK, it’s just the same miners mining multiple chains? I don’t see how that has potential for scaling, it’s better even to simply increase the block size of one chain and make them all mine on that one (no overhead as with multiple chains)? Am I missing something?

I even tried to watch this 2-hour video ![:scream:](https://ethresear.ch/images/emoji/facebook_messenger/scream.png?v=9), but as far as I can see this gentleman is just showing screenshots of other people’s tweets and keeps saying they’re wrong and wondering how can they be so wrong? ![:grin:](https://ethresear.ch/images/emoji/facebook_messenger/grin.png?v=9)

As [@vbuterin](/u/vbuterin) said, Eth 2.0 sharding-like constructions are the only scalable way to “mergemine” multiple chains without sacrificing safety (or at least we’re not aware of any other).

---

**kladkogex** (2018-09-24):

I do not think you need to use mergemining with Ethereum. Mergemining is used for networks that do not have smart contracts. For ETH you simply insert the Merkle root of the sidechain into a smart contract of the main chain, it is equivalent to mergemining.

You can not simply raise the block size to achieve scalability - it wont work.  The block size needs to propagate the network - if you increase the blocksize you will need to increase the time between subsequent blocks.

---

**MihailoBjelic** (2018-09-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> You can not simply raise the block size to achieve scalability - it wont work. The block size needs to propagate the network - if you increase the blocksize you will need to increase the time between subsequent blocks.

Sure. I was just comparing block size increase (as a naive and trivially simple approach to scaling) with mergemining (at least mergmining as I understand it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)), pointing out that you can achieve more with the former (cumulatively the same amount of data in blocks, but much less overhead).

