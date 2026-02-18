---
source: ethresearch
topic_id: 7739
title: Onboarding to L2 without ever directly touching L1
author: siliconMan
date: "2020-07-22"
category: Layer 2
tags: []
url: https://ethresear.ch/t/onboarding-to-l2-without-ever-directly-touching-l1/7739
views: 3537
likes: 3
posts_count: 7
---

# Onboarding to L2 without ever directly touching L1

L2 mass adoption seems to be hindered by the entrance fees/delays and the resulting chicken/egg challenges.

Is it possible for users to flow into an L2 system such as Loopring or zk-Sync without ever submitting an Ethereum mainnet transaction?  In other words, if you have the private keys for an L1 address, is that sufficient to operate within the L2 framework, or must there be an initial mainnet transaction to “open an account” and link the mainnet address to the L2 counterpart?

If users can onboard funds directly to L2 from a credit card or bank account (i.e. something like Coinbase), it seems inevitable that the current base layer becomes a simple data availability layer, behind the scenes.  Am I stating the obvious or missing something?

If this is possible, Eth 1.x is already vastly superior to the para-chain model of Polkadot.

## Replies

**barryWhiteHat** (2020-07-22):

You will have to make the public key available during account create. But this can be done by someone else.

For example if i want to send funds to you who do not have an account. I can include a higher fee for my send so that it incentivizes the coordinator to create that account for you so that they can process the transaction and get the fee.

---

**siliconMan** (2020-07-22):

Thank you, so once generalized smart contracts are available on L2 and there is mobility between L2 networks, is there any reason why people would continue to transact on Mainnet?  I can only think of these:

(1) legacy usage with soon-antiquated contracts

(2) create new L2 systems

(3) in an emergency to recover funds from a broken L2

(4) long-term storage of value for large amounts

(5) moving legacy or large funds to L2

(6) staking on ETH2

It seems like an important discussion because – if this is the new model – then future onramps should be built to move mainstreet into L2 with Ethereum quietly at the bottom of the pyramid.  The whole notion of “gas” disappears to the regular user as they will only be paying L2 fees.

I just discovered your other thread where you are promoting standardization to allow mobility between L2s.   I hope the ETH foundation leadership will clarify the roadmap along these lines so developers can plan accordingly, and branding can be optimised.   I think most people have the model upside down and think that Ethereum is at the top of the pyramid…as the gateway, with the L2s underneath.   At least that was my paradigm until now.

It also tells me that ETH 1.5 is the end-game.   What would be the point of sharding execution if it’s all happening on L2?  The contract execution of ETH2 could happen within the Beacon chain, since it would primarily be just managing L2s and the data shards.

Actually, is it even necessary to merge ETH1 with ETH2, or could the L2 networks inter-operate with both until an effective shutdown of ETH1 some 5 years down the road?  It would never be completely shutdown, but the ice-age would smoothly slow it down along with the issuance.

Edit: one more thought.  If the L2s can operate on both ETH1 and ETH2 simultaneously, a two-way bridge is opened for the two versions of ETH, as any DEX can exchange the two forms at near parity.

---

**cfoster0** (2020-07-31):

AFAICT, there are real efficiency gains to be had with Phase 2 Execution Environments. For instance, rather than paying for EVM gas execution of a ZK rollup on shard 0 (as you’d need in phase 1.5), you could use a special, precompile EE that handles them. And you can run a bunch of them in parallel since that EE should be available to all shards.

---

**barryWhiteHat** (2020-07-31):

Phase 1 also helps by giving use huge amount of data availability bandwidth. With rollups we have to put alot of data on chain and this is the limiting factor. With eth2 phase 1 the limit on how much data we can publish rises alot.

---

**adlerjohn** (2020-07-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/cfoster0/48/5077_2.png) cfoster0:

> Phase 2 Execution Environments

EEs are “postponed indefinitely.”

![](https://ethresear.ch/user_avatar/ethresear.ch/cfoster0/48/5077_2.png) cfoster0:

> a special, precompile EE

That’s not how EEs work. EEs can’t have special metering. Which isn’t actually relevant since EEs are no longer a planned feature.

---

**cfoster0** (2020-07-31):

Since when are EEs no longer a planned feature? Both Etherhub and the Phase 2 wiki talk about them extensively. I know the EWASM team is exploring the idea of Eth1x64, but I haven’t seen anything abandoning the idea of EEs. Only suggestion I could find was a Twitter thread with Vitalik discussing the possibility that we might find down the line that we don’t need more than one shard with execution capacity.

I know these specs change fast but I haven’t heard of this changing.

https://docs.ethhub.io/ethereum-roadmap/ethereum-2.0/eth-2.0-phases/


      ![](https://ethresear.ch/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/UzysWse1Th240HELswKqVA)



    ![](https://ethresear.ch/uploads/default/optimized/3X/c/d/cd231863ebeb783c60343a8e1e943178c5cb44c7_2_690x362.jpeg)

###












    ![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/f04885/48.png)

      [Eth1x64 Variant 1 “Apostille”](https://ethresear.ch/t/eth1x64-variant-1-apostille/7365) [Sharded Execution](/c/sharded-execution/35)




> Co-written by Alex Beregszaszi (@axic) and Sina Mahmoodi (@sinamahmoodi), with the involvement of other Ewasm team members. Thanks to Guillaume Ballet (@gballet) and Danny Ryan (@djrtwo) for valuable feedback.
> This post will provide a high-level overview. For a more detailed semi-specified version refer to the repository, which additionally includes example contracts.
> This post goes into one variant of the Eth1x64 experiment. To recap, Eth1x64 builds on Phase 1.5 and explores the “put Eth1 on …

https://mobile.twitter.com/muellerberndt/status/1279011030128001029

