---
source: ethresearch
topic_id: 7271
title: PoS based on Synthetic PoW using VDF and VRF
author: manfr3d
date: "2020-04-13"
category: Proof-of-Stake
tags: [proofs-of-sequential-work]
url: https://ethresear.ch/t/pos-based-on-synthetic-pow-using-vdf-and-vrf/7271
views: 2938
likes: 4
posts_count: 5
---

# PoS based on Synthetic PoW using VDF and VRF

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

## Replies

**SebastianElvis** (2020-05-22):

If I understand correctly, what this protocol aims to achieve is to make mining non-parallelisable. To this end, you replace PoW mining with VDF puzzles. Then this leads to the winner-take-all problem. To avoid winner-take-all, you introduce difficulty adjustment for each miner. If a miner mines too fast, then makes his VDF puzzle harder as punishment. However, miners can use multiple addresses to avoid this. To make such behaviour non-profitable, you introduce staking.

I can think of two attacks, which seem to be fundamental and unsolvable.

The first one is that, given parameters for PoW/PoS/VDF, the adversary can always find an optimal strategy on how many accounts to use and how many stakes each account holds, such that he can earn extra profit. In other words, the adversary can launch more fine-grained sybil attacks. Staking can only reduce the factor that the adversary can earn in extra, but cannot prevent sybil attacks completely.

This requires very careful design of parameters, with game-theoretic analysis as theoretical foundation. Also, replacing staking with contribution (i.e., the number of blocks a miner mines in the last x blocks) can be better here. Coins (stakes) are transferable, but contribution cannot.

The second one is that, the adversary (with a single account) can mine lots of blocks at the same height within the same time compared to mine a single block. The adversary can choose different sets of transactions, so have lots of merkle roots. Then, he can run VDF over different `prev_hash || merkle_root` in parallel, and find lots of blocks at the same height. As mining multiple blocks is no harder than mining a single one, everyone can mine blocks at the same height in parallel. Would this end up with lots of parallel chains? Or would this lead to network partitioning?

In short, the input of VDF should be deterministic and each key pairs can only mine a single block. All mutable things in VDF’s input should be ruled out. This is hard. Even if you just use prev_hash as input of VDF the adversary can do that in the VRF phase.

---

**manfr3d** (2020-05-22):

Thanks for your response, it is difficult to find some still interested in this problem. I believe your points are covered by the protocol. Let me recap.

**Parallelizable:** I am working on a parallelizable version with shards, I believe is parallelizable, but this is the single version.

**Winner-takes-all:** initially we assume that the linear so, for example, 10 random linear slots a VDF miner with a 50% (2x) advantage can outrun half of the slots or miners. So we have exponential slots. For example, with a 3x exponential, first slots mines 100ms, 2dn slot 300ms, 3rd slot 900ms, etc. in this example we can avoid winner-takes all for miners with hardware or optimization up to a 66% better than other miners.

**Sybil Attacks**: 1st attack. Given the fact that the pseudo-randomization of VDF steps is based on the stake it has on the account, is design to distribute rewards fairly with a low error, lets say ±2%. Then is always less expensive to consolidate the stake into one single account than splitting into many and do many VDF minings. If we account the extra electricity for extra VDF threads, we can say that it is superlinear because always

NetRewards(S0 + S1) >= NetRewards(S0) + NetRewards(S1)

**Nothing-at-stake**: 2dn Attack. The VRF seed that is used in combination with your private key and your stake to generate the pseudo-random slot is only based on the previous block hash that you don’t control. Then you can’t control the current seed and you can’t control the future seed because the VDF proof output (nonce on PoW) is also deterministic so you cannot run multiple VDF on the same block with the same stake and account. If you want to move the stake into a new account, even if you choose a specific account address, a specific stake you move, you include the Tx on the current block and know you can win because you have a big stake, the VDF proof you cannot control it and then you cannot control the next block hash depending on the VDF proof/nonce. If there is any doubt on miners moving stake around before mining, I don’t think it is needed, but we can include a lock mechanism so staked coins cannot be moved around for N blocks before they can be staked (like BFT blockchains have). So, is positive in our design, only one keypair/account can mine a single block because we use their stake also as input. I mean, the only way to be the proposer is to mine VDF in parallel on each account with positive stake, try to mine on account with zero stake and then moving stake will invalidate all the VDF mining done. Even if the attack a super computer (quantum?) and can cover a significant fraction of the VDFs mining for other possible accounts or futures, he cannot predict who is going to win because he doesn’t has the private keys of the competitors, and if he tries to affect the future by moving his stake then he will be changing his future outcomes.

I hope the explanation was clear, because the mining power now is translated to Random Clocks based on Stake, the only way to increase your mining power and reduce the random clock should be to by more stake. Maybe there is a more specific attack you can find.

Thanks.

---

**SebastianElvis** (2020-05-22):

Thanks for your detailed response.

> Winner-takes-all:  initially we assume that the linear so, for example, 10 random linear slots a VDF miner with a 50% (2x) advantage can outrun half of the slots or miners. So we have exponential slots. For example, with a 3x exponential, first slots mines 100ms, 2dn slot 300ms, 3rd slot 900ms, etc. in this example we can avoid winner-takes all for miners with hardware or optimization up to a 66% better than other miners.

So you mean if the miner mines too fast, his difficulty will increase quadratically or even exponentially? This seems to be a more harsh and fine-grained difficulty adjustment. The final objective is that, the mining speed of each account is equal, am I right?

> Sybil Attacks : 1st attack. Given the fact that the pseudo-randomization of VDF steps is based on the stake it has on the account, is design to distribute rewards fairly with a low error, lets say ±2%. Then is always less expensive to consolidate the stake into one single account than splitting into many and do many VDF minings. If we account the extra electricity for extra VDF threads, we can say that it is superlinear because always

Do you have the concrete function between difficulty and {stake, mining speed}? You are right on the objective of making splitting coins into multiple accounts no more profitable than using a single account.

My point is that, given any stake-difficulty function, there exists a strategy of allocating stakes into multiple accounts such that the adversary can get more reward than using a single account.

Now the mining difficulty is related to two parameters, stake and mining speed.

The difficulty adjustment towards the mining speed delays at least for one block.

What the adversary can do is to: 1) have a powerful hardware, 2) have some stake on account A, 3) mine in the name of account A, 4) difficulty of account A rises, 5) transfer stake to another account B, 6) mine in the name of account B, …

> Nothing-at-stake : 2dn Attack. The VRF seed that is used in combination with your private key and your stake to generate the pseudo-random slot is only based on the previous block hash that you don’t control. Then you can’t control the current seed and you can’t control the future seed because the VDF proof output (nonce on PoW) is also deterministic so you cannot run multiple VDF on the same block with the same stake and account. If you want to move the stake into a new account, even if you choose a specific account address, a specific stake you move, you include the Tx on the current block and know you can win because you have a big stake, the VDF proof you cannot control it and then you cannot control the next block hash depending on the VDF proof/nonce. If there is any doubt on miners moving stake around before mining, I don’t think it is needed, but we can include a lock mechanism so staked coins cannot be moved around for N blocks before they can be staked (like BFT blockchains have). So, is positive in our design, only one keypair/account can mine a single block because we use their stake also as input. I mean, the only way to be the proposer is to mine VDF in parallel on each account with positive stake, try to mine on account with zero stake and then moving stake will invalidate all the VDF mining done. Even if the attack a super computer (quantum?) and can cover a significant fraction of the VDFs mining for other possible accounts or futures, he cannot predict who is going to win because he doesn’t has the private keys of the competitors, and if he tries to affect the future by moving his stake then he will be changing his future outcomes.

I agree with that it’s hard to control the VDF output. What I mean is that, the merkle root is partly controllable. The memory pool is very big.  The adversary can choose different sets of transactions to mine on, leading to different merkle root hashes. Then, he can enumerate lots of legal VDF inputs, and mine on these VDF instances concurrently.

---

**manfr3d** (2020-05-23):

> So you mean if the miner mines too fast, his difficulty will increase quadratically or even exponentially? This seems to be a more harsh and fine-grained difficulty adjustment. The final objective is that, the mining speed of each account is equal, am I right?

According to its stake has a slot range 1…S, then based on the prev block hash and its private key has a random slot in the range. The slot is multiplied by a quantum to scale up for desired block time. For winner-takes-all protection each slot is not linear but exponential. Base on average block time the exponential base is dynamically increased or decreased **affecting all miners**. If a miner has better hardware or software then it will reduced average block time and the consensus is to increment the exponential base, same in the other direction. This was as soon as hardware or software advantage is used to jump to a smaller slot in a few blocks the VDF mining is more difficult for all and is more difficult to jump to smaller slots.

> Do you have the concrete function between difficulty and {stake, mining speed}? You are right on the objective of making splitting coins into multiple accounts no more profitable than using a single account.
> My point is that, given any stake-difficulty function, there exists a strategy of allocating stakes into multiple accounts such that the adversary can get more reward than using a single account.

My initial version is: if stakeFraction if miner between 0 and 1, then the slot range is [1/stakeFraction] + 1

The idea is obviously, I believe is correct, to make the most profitable strategy to mine with all the stake together on the same account.

> Now the mining difficulty is related to two parameters, stake and mining speed.
> The difficulty adjustment towards the mining speed delays at least for one block.
> What the adversary can do is to: 1) have a powerful hardware, 2) have some stake on account A, 3) mine in the name of account A, 4) difficulty of account A rises, 5) transfer stake to another account B, 6) mine in the name of account B, …

As I explained before, the increase in difficulty affect the exponential base and affects all accounts mining, then is the same if you move the stake to another account.

> I agree with that it’s hard to control the VDF output. What I mean is that, the merkle root is partly controllable. The memory pool is very big. The adversary can choose different sets of transactions to mine on, leading to different merkle root hashes. Then, he can enumerate lots of legal VDF inputs, and mine on these VDF instances concurrently.

Now the Merkle Root is part of the VDF input, then the byzantine miner can do VDF mining with many parallel inputs. But will finish all threads at the same time because the random slot depends only on the VRF seed. Once it finishes all parallel VDFs have many VDF outputs and can a) choose one to publish, or b) try do to some Selfish Mining and start many next block parallel VDF for each VDF of the previous block. Because being a winner depends on the number of VDF Steps (random slot) based on the prev block hash and the private key, I agree there is some possibility of an attack but the attack is mitigated (I hope!) do to the following reasons:

1. We can avoid Merkle Root when computing the VDF input, then the Merkle Root is only affecting the block hash. Then the Selfish Mining attack must compute 2 blocks VDF before any other miners found a solution for the first block.

Comment: Thinking more, I think this makes the attack more easy, so is better to leave the Merkle Root as part of the VDF input.

1. In Bitcoin fork of the same height are equivalent there is no way to choose, is arbitrary. Describing their Selfish mining attack for Bitcoin (https://www.cs.cornell.edu/~ie53/publications/btcProcFC.pdf) the proposed to randomize that. In Vixify, because the slots are already random if the Byzantine Selfish Miner takes to much time another miner with a smaller slot can appear and reorganize the blockchain. Also, because all miners know when they see a proposed block if they have a better a lot than the proposed, they can continue mining and reorganized the last blocks when they claim their fork. We can do that for less than K blocks of difference the blockchain can be recognized favoring the slot winner, and for more than K blocks of difference in the chain we can favor the longer chain.
2. The dynamic exponential base feedback based on average block time will also help mitigate this problem because as soon as the attacker published smaller times the system will make it more difficult also for the attacker.

> (Selfish mining paper) Currently, when there are two branches of equal length, the choice
> of each miner is arbitrary, effectively determined by the network topology and
> latency. Our change explicitly randomizes this arbitrary choice, and therefore
> does not introduce new vulnerabilities.

