---
source: ethresearch
topic_id: 22099
title: Staircase Attack-II in Ethereum PoS
author: mart1i1n
date: "2025-04-07"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/staircase-attack-ii-in-ethereum-pos/22099
views: 580
likes: 10
posts_count: 13
---

# Staircase Attack-II in Ethereum PoS

## Staircase attack

[Staircase attack](https://www.usenix.org/system/files/usenixsecurity24-zhang-mingfei.pdf) is a recent attack on the attestation incentives. Staircase attack aims to make honest validators suffer from penalties even if they strictly follow the protocol in a synchronous network after Capella upgrade. In staircase attacks, Byzantine validators withhold their attestations to prevent the canonical chain from justifying the last checkpoint. As illustrated in Figure 1, in epoch e, the Byzantine validators withhold their attestations to prevent the honest validators from justifying the checkpoint cp_0. The attestations from Byzantine validators are included in a withheld block b_1, a block proposed by a Byzantine validator. Before the middle of epoch e+1, all honest validators extend the chain led by block b_0. After the middle of epoch e+1, the withheld block b_1 is released. The last justified checkpoint is updated as only the withheld chain includes two-thirds of attestations for checkpoint block cp_0. The chain led by cp_1 is filtered in HLMD-GHOST and the chain led by b_1 becomes the canonical chain. In this attack, the attestations from honest validators in the first half of epoch e+1 are discarded, as the chain they vote for is not later finalized. These honest validators suffer from penalties according to the protocol. It was shown that by controlling 29.6% of the total stake, the attack can be conducted in every epoch so eventually all honest validators suffer from no incentive rewards. The attack was mitigated via the Deneb upgrade.

[![Figure 1. Staircase Attack](https://ethresear.ch/uploads/default/optimized/3X/1/2/1248dd2290d23f8bb6388d2b70a24c44abb07d41_2_690x392.png)Figure 1. Staircase Attack1156×658 72.2 KB](https://ethresear.ch/uploads/default/1248dd2290d23f8bb6388d2b70a24c44abb07d41)

## Staircase Attack-II

We find a new variant of the staircase attack and we called it staircase attack-II, as shown in Figure 2. Similar to the staircase attack, Staircase Attack-II requires the proposer in the first slot of an epoch to be Byzantine. Additionally, staircase attack-II assumes that the proposer in the first slot of epoch 1 is also Byzantine.

[![Figure 2. Staircase Attack-II](https://ethresear.ch/uploads/default/optimized/3X/4/7/47014757c4e592c562fb360fce1f552aa8a28348_2_410x500.png)Figure 2. Staircase Attack-II628×764 77.3 KB](https://ethresear.ch/uploads/default/47014757c4e592c562fb360fce1f552aa8a28348)

As shown in Figure 2, at the beginning of epoch 0, the adversary delays its block b_0 in slot 0 for four seconds. Therefore, the target of attestations from honest validators in slot 0, i.e., block b, is different from the target of attestations in slots 1-31, i.e., block b_0. In addition, all attestations from the adversary are delayed forever. Accordingly, the number of attestations from honest validators with the same target and source can not reach 2n/3. Block b_0, which is supposed to be justified in epoch 0, cannot be justified by the attestations from honest validators. In contrast, the adversary can justify the block in slot 0 by releasing its last block in epoch 0, i.e., block b_{31}. This block includes the attestations from the adversary, so the number of attestations exceeds two-thirds. The adversary delays the block for two epochs. As a result, the block in slot 0 can be justified at the end of epoch 2. In epoch 1, the adversary conducts the same strategies. Particularly, the adversary delays the block b_{32} for four seconds and delays all attestations from the adversary. Therefore, the honest validators can not justify the block in epoch 1. After block b_{31} is released in epoch 2, block b_0 is justified. As the chain from honest validators does not justify any new block, the chain led by b_{31} is the new canonical chain. All attestations included in the chain from honest validators are discarded.

## Analysis

Our staircase attack-II shares the same feature as the staircase attack: Byzantine validators receive rewards but honest validators suffer from penalties, although honest validators strictly follow the specification of the protocol. Therefore, this attack falls into metric III in our criteria. The probability of launching the attack is 1/9, as we require the proposer in the first slot to be Byzantine. Unlike the staircase attack, staircase attack-II cannot be continuously launched. However, if the adversary controls 33% stake and launches the attack whenever the attack can be launched, \textit{all} honest validators will suffer from penalties for the corresponding epochs.

## Replies

**potuz** (2025-04-08):

Can you explain how block 0 is canonical if the block is not attested? does the adversary have > 50% or are you assuming only 33%? Is the assumption that the attacker also controls slot 1 in addition to 0 and 31?

---

**mart1i1n** (2025-04-08):

Consider the honest reorg mechanism makes the attack description not very readable, so we do not include the strategy here. Briefly speaking, adversary attest in slot 0 can prevent its block being reorged by honest validators. We assume the adversary controls 1/3 of total stakes.

---

**potuz** (2025-04-08):

This contradicts the fact that attestations from the adversary are delayed forever

---

**mart1i1n** (2025-04-08):

It does not matter, the attestations from slot 1 to slot 31 are enough for this attack.

---

**potuz** (2025-04-08):

Ok, so the adversary releases attestations for block 0 and not the rest.

At any rate, I don’t understand what does this have to do with the block being there or not? what changes if block 0 is released early or not? What you describe seems to be the standard scenario in which an attacker can withold justification and can release it at any time. Same for b32, why does the adversary need to delay this block? what does it have to do with the attack that these blocks have few attestations during a single slot?

---

**mart1i1n** (2025-04-08):

We have described in detail in our previous paper, [staircase attack](https://www.usenix.org/system/files/usenixsecurity24-zhang-mingfei.pdf). Briefly speaking, by using such a strategy, the target of attestations from honest validators in slot 0 is different from the target of attestations from honest validators in slots 1-31. Thus, we can split the attestations from honest validators into two parts. No part includes enough attestations for justification. As a result, the honest attestations alone can not justify the checkpoint unless the adversary releases its attestation.

---

**kladkogex** (2025-04-08):

Good paper!

Please also take a look at this

A single kamikaze validator can make chaos in the entire system



    ![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png)

      [Kamikaze Attacks on ETH2](https://ethresear.ch/t/kamikaze-attacks-on-eth2/14351)




> There is one type of an attack on ETH PoS, where attacker is willing to sacrifice 32 ETH slashed to potentially have a much larger gain.
> If an attacker shorts a significant amount of ETH, then the potential gain from even temporarily disruption of the network can outweigh the 32 ETH loss.
> I do not know if the current ETH clients have been tested against attacks like that.
> The simplest attack involves the malicious proposer creating a large number of non-unique but valid block proposals, and d…

Unfortunately Ethereum Foundation has never announced any bounty on security vulnerabilities

---

**potuz** (2025-04-09):

I still don’t understand this only applies to slot 0, and even the full committee of slot 0 cannot have enough to justify anything, regardless of splitting.

---

**mart1i1n** (2025-04-10):

Assume the honest validators control 67% of the stake and the adversary controls 33% of the stake. If the adversary does not delay its block in slot 0 and the adversary withholds all its attestations, the attestations from honest validators can still justify epoch 0 since the number of attestations from honest validators is 67% of total attestations, greater than 2/3. If the adversary delays its block in slot 0, the target of attestations from honest validators in slot 0 is different from the target of attestations from honest validators in slots 1-31. Therefore, the number of honest attestations in slots 1-31 is 67\%\times 31/32<2/3, so the attestations from honest validators can not justify epoch 0.

---

**kladkogex** (2025-04-11):

Well it is even simpler -

Here is how a single validator can bring the entire network down

1. Stake 32 ETH
2. Collect IP addresses of nodes that form the network
3. Wait until it is your time to propose.
4. Form a unique different proposal for each node in the network and submit it to the node
5. The network will die because there will be total chaos and no winning branch.

Our team can bring the entire ETH mainnet down with this. I wonder if we do it, can we get retroactively funded by ETH foundation.

What I find incredible about ETH foundation, is that they never issue security bounties and never respond to any security vulnerability reports. They ignore you,  because any kind of criticism is perceived as a threat.

And then they start banning you from things like Devcon

---

**mart1i1n** (2025-05-21):

We simulated an attack on a local testnet with 256 validators. The adversary controls the first 85 validators (approximately 33%). For this simulation, the honest reorg mechanism was disabled.

Validator 55, controlled by the adversary, was scheduled to propose a block at slot 256, the first slot of epoch 8.

```shell
time="2025-05-20 15:20:33" level=info msg="Validator activated" index=55 prefix=client pubkey=0xac9f4df3f20a status=ACTIVE validatorIndex=55
time="2025-05-20 16:11:49" level=info msg="Duties schedule" attesterCount=3 attesterPubkeys=[0xae00fc3de831 0x86a73886aa01 0x815042c33c1a] prefix=client proposerPubkey=0xac9f4df3f20a slot=256 slotInEpoch=0
```

The adversary delayed the block proposal from validator 55 by 8 seconds. The block was expected at 16:11:49 but was instead proposed at 16:11:57.

```shell
time="2025-05-20 16:11:57" level=info msg="Submitted new block" attestationCount=1 blockNumber=256 blockRoot=0xae296447eb6a depositCount=0 fork=deneb gasUtilized=0 graffiti="" parentHash=0x2e56275d9f36 payloadHash=0x06ed388336c0 prefix=client pubkey=0xac9f4df3f20a slot=256 txCount=0 withdrawalCount=0
```

Due to this delay, honest validators attesting in slot 256 did not see the new block (256). Consequently, they used its parent, block 255 (root: `0x076884eadb9f`), as their target checkpoint for epoch 8.

```shell
time="2025-05-20 16:11:37" level=info msg="Submitted new block" attestationCount=1 blockNumber=255 blockRoot=0x076884eadb9f depositCount=0 fork=deneb gasUtilized=0 graffiti="" parentHash=0xabaec725e1b9 payloadHash=0x2e56275d9f36 prefix=client pubkey=0xa4e2f5a41959 slot=255 txCount=0 withdrawalCount=0
time="2025-05-20 16:11:57" level=info msg="Submitted new attestations" blockRoot=0x076884eadb9f committeeIndices=[0] prefix=client pubkeys=[0xb404c5cda4da] slot=256 sourceEpoch=7 sourceRoot=0x4c92b34576aa targetEpoch=8 targetRoot=0x076884eadb9f
```

Once block 256 was eventually proposed, validators attesting in the subsequent slot (257) began using block 256 (root: `0xae296447eb6a`) as their target checkpoint for epoch 8.

```shell
time="2025-05-20 16:12:09" level=info msg="Submitted new attestations" blockRoot=0xf8d3ec318a3e committeeIndices=[0] prefix=client pubkeys=[0x8f1ef3639aea] slot=257 sourceEpoch=7 sourceRoot=0x4c92b34576aa targetEpoch=8 targetRoot=0xae296447eb6a
```

We can use a figure to illustrate this:

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/3/137d63860848d70ff1e1e5eb97eea0150754583f_2_429x500.png)image455×530 38.8 KB](https://ethresear.ch/uploads/default/137d63860848d70ff1e1e5eb97eea0150754583f)

This delay successfully split the attestations for epoch 8: some referenced block 255 as the target checkpoint, while others referenced block 256. With the adversary controlling 33% of the stake, neither set of attestations could reach the required 2/3 majority for justification.

---

**mart1i1n** (2025-05-21):

We have also found a more powerful attack that manipulates RANDAO to create the canonical chain that only includes adversary blocks, thus causing a liveness problem. See [Liveness attack](https://ethresear.ch/t/liveness-attack-in-ethereum-pos-protocol-using-randao-manipulation/22241).

