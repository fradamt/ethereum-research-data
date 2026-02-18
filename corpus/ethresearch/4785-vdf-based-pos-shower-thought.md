---
source: ethresearch
topic_id: 4785
title: VDF Based POS (Shower Thought)
author: machinehum
date: "2019-01-10"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/vdf-based-pos-shower-thought/4785
views: 2555
likes: 1
posts_count: 9
---

# VDF Based POS (Shower Thought)

I was thinking about a different approaches to POS and came up with something (maybe) interesting last night. All stuff about using VDFs for RNG has got me thinking about their utility recently.

If you have N validators which each have

1. Staked some amount of eth (min staking required)
2. A VDF

Where the VDF takes time t to evaluate (requires asic) and time << t to validate (Does not require asic), where the block time \approx t.

At the beginning of the block creation session…

1. Each Validator gathers up transactions from non-validator nodes, forming their own blocks. Previous block hash must be included in this block.
2. These blocks are then hashed/signed with the validator key and then run through the VDF.
3. The VDF outputs are then all collected by all validators, VDF outputs are arranged into a big block sorted by order with the previous block hash. Blocks are verified. Consensus is reached. Validators ensure no illegal transactions are present.
4. Slashing conditions apply. Validators are paid out based on their staked eth.
5. GOTO step 1

It’s similar to POW, but instead of the resource being power it’s time. In order to fabricate a blockchain of higher merit you would need time T to build from block height B.

T = t * B

For a 51% attack you need 51% of all the validators eth, if you were to pull it of the chain would probably just fork your wealth away.

Anyways, just a shower thought… might be interesting to some people, might not be. Digging the Tex formatting in this forum ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

## Replies

**JustinDrake** (2019-01-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/machinehum/48/3086_2.png) machinehum:

> Where the VDF takes time t to evaluate […] where the block time \approx t.

![](https://ethresear.ch/user_avatar/ethresear.ch/machinehum/48/3086_2.png) machinehum:

> In order to fabricate a blockchain of higher merit you would need time T to build from block height B.

While VDFs are good to guarantee that some minimum amount of time has elapsed, they are not so good as a direct clocking mechanism. The reason is that an attacker could build an ASIC that is A times faster than the commodity hardware available to honest players, where A is small but still greater than 1.

---

**dlubarov** (2019-01-10):

Your idea sounds similar to Solana’s proof of history concept, except that Solana’s delay function is a simple iterated hash, presumably because there were no good VDF candidates at the time.

I agree with Justin. It’s interesting but I never really understood the appeal of it. What benefit(s) do you see?

---

**machinehum** (2019-01-10):

Right, but if an attacker made a VDF that was marginally faster than honest players it wouldn’t really matter. They would just produce their personal block a little faster.

If an attacker made a VDF that was 2t that means the block time would be 2t, however the attacker would also need 51% (or some high amount) of eth to make the longest chain with the most wealth. Players with the slower VDFs would not be able to produce their blocks in time to be included in the big block.

Slower honest players would have the most wealth and the chain would basically fork itself.

Mr. fast VDF is more then welcome to validate on the “longest chain” but it’s basically an orphan.

---

**machinehum** (2019-01-10):

It’s similar to POW where the older the block, the more final it becomes.

---

**dlubarov** (2019-01-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/machinehum/48/3086_2.png) machinehum:

> the attacker would also need 51% (or some high amount) of eth to make the longest chain with the most wealth

Hm what would the fork choice rule be? If one fork had a longer VDF length, and the other had more staker participation, which would the network prefer? For comparison Solana uses BFT consensus, so their fork choice rule requires 2/3 voter approval.

It seems like VDFs only add security of an honest (and online) party controls the fastest ASIC. If an attacker’s ASIC was slightly faster, forks would take longer to build, but given enough time they could still build arbitrarily long forks which pass the VDF length test.

I’m not saying the scheme would be insecure, just not sure if it would be more secure than a traditional PoS chain using Nakamoto consensus, like Cardano.

---

**machinehum** (2019-01-10):

Fork choice would be some hybrid of the longest chain and most wealth. If there’s a super long chain with hardly any validators and eth then that’s not good. If there’s a chain that’s 100x less blocks and most of the wealth that’s not good either. So it would just be some formula for fork choice that included block height and wealth.

Chain security would be compromised if an attacker had the most wealth and the fastest ASIC. At which point it’s possible to fork away the wealth.

You don’t want to have an ASIC n times faster because then honest players wont be able to produce their blocks fast enough, and won’t be able to fit their blocks into the big blocks in time. At which point the network would just fork and you would loose your money.

Is it not possible to just generate a fake Cardano chain longer than the mainnet chain? I know it’s impossible with POW because you would need to redo all the work.

Edit: I don’t know much about Ouroboros

---

**manfr3d** (2020-04-13):

Hi guys, any comments on my VDF&VRF based PoS?

- Winner-takes-all is avoid by exponential VDF steps that adjust using average block time.
- VRF (ie. bijective signing) and current stake is used to generate pseudo-random seeds for each miner to calculate their current block VDF steps to compute. Basically is a Synthetic Proof-of-Work, because we are simulating Random Clocks.

Thanks!

Draft:



      [github.com/jose-blockchain/vixify](https://github.com/jose-blockchain/vixify/blob/master/README.md)





####

  [master](https://github.com/jose-blockchain/vixify/blob/master/README.md)



```md
![Vixify Logo](https://i.ibb.co/TgqJpvx/logo2-color-transp.png "Vixify Logo")

# Vixify Blockchain

A modern pure Proof-of-Stake blockchain based on a verifiable delay functions (VDF) and a verifiable random function (VRF). Implements a synthetic Proof-of-Work using the VDF and VRF based on coin stakes and non-parallelizable mining.

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Summary

Vixify is a blockchain adopting a pure Proof-of-Stake consensus protocol based on a verifiable random function (VRF) and a verifiable delay function (VDF) that has the following properties: a) all addresses with a positive stake can participate in consensus; b) is fair regarding the stake and the distribution of rewards; b) is tolerant to several classic attacks such as Sybil attacks, "Nothing-at-stake" attacks and "Winner-takes-all" attacks.

## Blockchain Features

Vixify Blockchain has the following features:

* Proof-of-Stake - only stakeholders can participate in consensus and recieve rewards.
* Energy-efficient Single-thread Mining - Using a VDF allow the blockchain with blocks mined on a single-thread by each stakeholder. Under certain chip technologies the design if secure (for example, no miner has a chip technology that is x3 or x4 faster than the current state of the art in commercial chips).
* Secure - Using a verifiable random function (VRF) allows next-block miner to be unpredictable, discouraging attacks on stakeholders nodes.
* Catastrophic Failure-tolerant - supports catastrophic >50% stake failure or network fragmentation, unlike PBFT Proof-of-Stake blockchains that stop working under catastrophic conditions.
```

  This file has been truncated. [show original](https://github.com/jose-blockchain/vixify/blob/master/README.md)










Very basic Proof of Concept (with pseudo-VDF):


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/jose-blockchain/vixify/tree/master/hello-vixify)





###



A prototype of Proof-of-Stake blockchain based on VDFs and VRFs, design to be a "plug-n-play" replacement of Proof-of-Work protocols.  - jose-blockchain/vixify










Consensus:

[![vixify-README-md at master · manfr3d-vixify 13-04-2020 17-38-38](https://ethresear.ch/uploads/default/optimized/2X/7/74c26969d2dc98b4ec0d7dc581cc676bdb4b410c_2_598x500.png)vixify-README-md at master · manfr3d-vixify 13-04-2020 17-38-381894×1582 545 KB](https://ethresear.ch/uploads/default/74c26969d2dc98b4ec0d7dc581cc676bdb4b410c)

Winner-takes-all Protection draft:

```
difficulty = slow-moving variable self-regulated by average block time (for example, miners can move this deterministically by 1% each block up or down).
minerStake = current block # of coins stake of the miner address holding the coins
stake = minerStake / totalCoins
slot = int(round(1/stake))
miner_vrf_seed = vrf_sign( prev_block_hash, miner_private_key ).    # VRF is just a deterministic signature, bijective.
random.set_seed(miner_vrf_seed)
slotRange = [1:slot+1] # the range of possible integer slots for a given miner holding stake on a given address.
slotNumber = random.random_integer_on_range(slotRange) # slotNumber = a deterministic slot number based for address or miner holding stake on a given blocknumber.
vdfSteps = 2 ^ ( difficulty * slotNumber )   # this number is like the average mining time of traditional PoW.
```

---

**machinehum** (2020-04-13):

Seems similar to what I was proposing. I still think it’s a half decent idea.

