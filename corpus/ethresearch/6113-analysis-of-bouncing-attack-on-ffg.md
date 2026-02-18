---
source: ethresearch
topic_id: 6113
title: Analysis of bouncing attack on FFG
author: nrryuya
date: "2019-09-08"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/analysis-of-bouncing-attack-on-ffg/6113
views: 6916
likes: 3
posts_count: 1
---

# Analysis of bouncing attack on FFG

## TL;DR

In this post, I dig into the bouncing attack on Casper FFG, which is already known to potentially make a permanent liveness failure of FFG. I present specific cases where this attack can happen. Also, I describe how the choice of the fork-choice rule relates to this attack.

Prerequisites:

- Casper FFG paper

## Background: Bouncing attack

In Casper FFG, the fork-choice rule must start from the latest justified checkpoint.

Alistair Stewart [found](https://ethresear.ch/t/beacon-chain-casper-mini-spec/2760/19) that this introduces an attack vector where the attacker leverages the inconsistency between the latest justified checkpoint and the fork-choice due to accidental or adversarial network failure.

[![image](https://ethresear.ch/uploads/default/optimized/2X/0/08bd315f46dba836786e05b46898c27aa4586c8e_2_690x380.png)image961×530 43.4 KB](https://ethresear.ch/uploads/default/08bd315f46dba836786e05b46898c27aa4586c8e)

Because of this, FFG cannot have liveness in eventually/partially synchronous model regardless of the choice of the fork-choice.

Then, looking deeper than the traditional network model in distributed systems, in what situation this attack happens in practice?

## Setup

The protocol we discuss is as follows:

- Casper FFG, slot, epoch, and attestation-committee a la ETH2.0 are adopted
- The number of the total validators is n, assume static validator set & homogeneous weight (stake) for simplicity
- The attacker controls t

## Bouncing condition

First, we discuss bouncing condition i.e. a condition in which an attacker can do a bouncing attack even in fully synchronous network.

Bouncing condition: there exists a latest justified checkpoint C and *justifiable* checkpoint C' such that (i) C' is *later* than and (ii) conflicting with C.

- Justifiable: 2n/3 - t_C \le \mathrm{FFGVotes}(C')  \mathrm{Epoch}(C)

This condition is sufficient to start bouncing attack; because if it is satisfied,

- Honest validators votes for a checkpoint C'', which is a descendant of C
- C'' becomes justifiable
- The attacker justifies C' before C'' is justified (This is where the rushing requirement for the attacker comes in)

In practice, the attacker publishes a block which contains the votes for C'

C' and C'' makes the bouncing condition satisfied again

[![image](https://ethresear.ch/uploads/default/optimized/2X/9/9530525f4da2a10b490be284b0e4acb9b1eacfd9_2_517x351.png)image746×507 15 KB](https://ethresear.ch/uploads/default/9530525f4da2a10b490be284b0e4acb9b1eacfd9)

#### How the bouncing condition is satisfied?

Since C is justified, at least the majority of the honest validators voted for C in \mathrm{Epoch}(C).

Also, since C' is justifiable, at least the majority of the honest validators voted for C' in \mathrm{Epoch}(C'). (The proof is omitted for simplicity.)

Therefore, for the bouncing condition to be satisfied, the fork-choice must have switched from the chain of C to the chain of C'.

Below, we describe scenarios where the fork-choice switches and the condition is satisfied by ~2 epochs of network failure.

## Case 1: Switch by saving (only in LMD)

In LMD GHOST, the attacker’s votes from an epoch earlier than \mathrm{Epoch}(C) can make the switch.

One example is a case where the attacker saved votes up and then published it.

[![image](https://ethresear.ch/uploads/default/optimized/2X/b/bcd31a7a4a61977bd58176a689eaf798d9d9bf71_2_690x378.png)image869×477 36.4 KB](https://ethresear.ch/uploads/default/bcd31a7a4a61977bd58176a689eaf798d9d9bf71)

The exact condition that this happens are:

- There is a justifiable (but not justified) checkpoint C, and there is no later justified checkpoint
- There is a checkpoint C' later than and conflicting with C
- C' is forked off in an epoch earlier than \mathrm{Epoch}(C)
- The attacker saved up t' votes in an epoch earlier than \mathrm{Epoch}(C)
- In \mathrm{Epoch}(C), the votes are sufficiently split such that 2n/3 - t' \le \mathrm{FFGVotes}(C) \lt n/2

For such a case to be possible,  t' > n/6

In simple terms, if the justification is delayed until the attacker succeeds to save up some votes and then in a later epoch the votes are sufficiently split, the attacker can start the bouncing attack.

Compared to the [decoy-flip-flopping](https://ethresear.ch/t/decoy-flip-flop-attack-on-lmd-ghost/6001) where the attacker also needs to succeed in saving, this is much stronger and easier to do successfully.

In FMD GHOST, which modified LMD GHOST so that only votes from the previous/current epoch are counted, this strategy does not work because the saved t' votes cannot affect the fork-choice.

## Case 2: Switch by biased message delay

Here, we consider a case where the network delay is biased (by accident or the attacker) for votes for C and the fork-choice switches.

[![image](https://ethresear.ch/uploads/default/optimized/2X/8/899807c683a5dac3147d8af2a67bd0087dcd0867_2_690x347.png)image852×429 36.2 KB](https://ethresear.ch/uploads/default/899807c683a5dac3147d8af2a67bd0087dcd0867)

The exact condition that this happens are:

- There is a justifiable or justified checkpoint C, and there is no later justified checkpoint
- There is a checkpoint C' later than and conflicting with C
- Some of the votes for C is delayed so that for honest voters, (i) C is seen not to be justified yet and (ii) C' wins the fork-choice

The necessary length of the delay depends on the slot allocation of the next epoch; the earlier slot the validators voted for C and the attacker are allocated to, the quicker the fork-choice switches

In the above example, where there is no fork earlier than \mathrm{Epoch}(C), there is no difference between LMD and FMD.

However, when the fork is from an earlier slot and most of the validators voted for the same chain as the previous epoch, there is a case where the attack succeeds in FMD but not in LMD.

[![image](https://ethresear.ch/uploads/default/original/2X/8/8482d9e3e5aa698217c086e6559e8cfa0a6ec41f.png)image670×461 27.5 KB](https://ethresear.ch/uploads/default/8482d9e3e5aa698217c086e6559e8cfa0a6ec41f)

## Implications

- A bouncing attack happens with ~2 epochs of network failure
- A bouncing attack works for every fork-choice in FFG, but fork-choice rules have their strengths and weaknesses

We cannot conclude LMD vs FMD regarding bouncing attack since we have little knowledge about how these cases happen
