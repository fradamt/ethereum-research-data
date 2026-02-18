---
source: ethresearch
topic_id: 6925
title: Timeliness detectors and 51% attack recovery in blockchains
author: vbuterin
date: "2020-02-11"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/timeliness-detectors-and-51-attack-recovery-in-blockchains/6925
views: 12303
likes: 13
posts_count: 8
---

# Timeliness detectors and 51% attack recovery in blockchains

### Summary

I propose a construction, based on [Lamport’s 99% fault tolerant consensus](https://vitalik.ca/general/2018/08/07/99_fault_tolerant.html) ideas, that I call **timeliness detectors**. Timeliness detectors allows online clients (ie. clients, aka users, that are connected to other clients with latency \le \delta) to detect, with guarantees of correctness and agreement, whether or not blocks were published “on time”. In the event of a 51% attack, this allows at least the subset of clients that are online to come to agreement over (i) whether or not a “sufficiently bad” 51% attack happened, and (ii) what is the “correct” chain to converge on and potentially even (iii) which validators to “blame” for the attack. This reduces the ability of 51% attacks to cause chaos and speeds up recovery time from an attack, as well as increasing the chance that a successful attack costs money.

### Timeliness detectors

The most basic construction for a timeliness detector is as follows. For every block that a client receives, the client maintains a “is it timely?” predicate, which states whether or not the client thinks the block was received “on time”. The goal of this will be to try to distinguish the attacking chain from the “correct” chain in a 51% attack:

[![51attack](https://ethresear.ch/uploads/default/optimized/2X/9/9c5d77f7a9c1ef3e47798d0f782b00e9a3047f95_2_690x290.png)51attack701×295 10.3 KB](https://ethresear.ch/uploads/default/9c5d77f7a9c1ef3e47798d0f782b00e9a3047f95)

Our model will be simple: each block B has a self-declared timestamp t (in real protocols, the timestamp would often be implicit, eg. in the slot number). There is a commonly agreed synchrony bound \delta. The simplest possible timeliness detector is: if you receive B before time t + \delta, then you see the block as timely, and if you receive it after t + \delta, then you do not. But this fails to have agreement:

[![51attack2](https://ethresear.ch/uploads/default/original/2X/a/a66e0ef443633757dcb8f40e8cd67808be1599f6.png)51attack2482×262 3.52 KB](https://ethresear.ch/uploads/default/a66e0ef443633757dcb8f40e8cd67808be1599f6)

We solve the problem as follows. For each block, we randomly select a sample of N “attesters”, v_1 ... v_n. Each attester follows the rule: if they see a block B with a timestamp t along with signatures from k attesters before time t + (2k+1)\delta, they re-broadcast it along with their own signature. And the rule that a *client* follows is: if they see a block B with a timestamp t along with signatures from k attesters before time t + 2k\delta, they accept it as timely. If they see B but it never satisfies this condition, they see B as not timely.

Let us see what happens when even one client sees some block B as timely, though others may not see it as timely *at first* because of latency discrepancies. We will at first assume a single, honest, attester.

[![51attack3](https://ethresear.ch/uploads/default/original/2X/8/8ef25ee130544e06a5a0989a15a5a50c535bcda1.png)51attack3572×431 20.6 KB](https://ethresear.ch/uploads/default/8ef25ee130544e06a5a0989a15a5a50c535bcda1)

This diagram shows the basic principle behind what is going on. If a client sees a block before for deadline T, then (at least because they themselves can rebroadcast it) that block will get into the hands of an attester before the *attester deadline* T + \delta, and the attester will add their signature, and they will rebroadcast it before time T + \delta, guaranteeing that other nodes will see the block with the signature before time T + 2\delta. The key mechanic is this ability for one additional signature to delay the deadline.

Now, consider the case of n-1 dishonest attesters and one honest attester. If a client sees a timely block with k signatures, then there are two possibilities:

1. One of those k signatures is honest.
2. None of those k signatures are honest (so one attester who has not yet signed still remains)

In case (1), we know that the attester is honest, and so the attester broadcasted B with j \le k signatures before time T + (2j-1)\delta, which means that (by the synchrony assumption) every client saw that bundle before time T + 2j\delta, so every client accepted B as current.

In case (2), we know that the honest attester will see the bundle before time T + (2k+1)\delta, so they will rebroadcast it with their own signature, and every other client will see that expanded bundle before the k+1 signature deadline T + (2k+2)\delta.

So now we have a “timeliness detector” which a client can use to keep track of which blocks are on time and which blocks are not, and where all clients with latency \le \delta to attesters will agree on which blocks are timely.

### The Simplest Blockchain Architecture

Come up with any rule which determines who can propose and who attests to blocks at any slot. We can define a “99% fault tolerant blockchain” as follows: to determine the current state, just process all timely blocks in order of their self-declared timestamp.

This actually works (and provides resistance to both finality-reversion and censorship 51% attacks), and under its own assumptions gives a quite simple blockchain architecture! The only catch: it rests everything on the assumption that all clients will be online and the network will never be disrupted. Hence, for it to work safely, it would need to have a block time of perhaps a week or longer. This could actually be a reasonable architecture for an “auxiliary chain” that keeps track of validator deposits and withdrawals and slashings, for example, preventing long-run 51% attacks from censoring new validators coming in or censoring themselves getting slashed for misbehavior. But we don’t want this architecture for the main chain that all the activity is happening on.

### A more reasonable alternative

In this post, however, we will focus on architectures that satisfy a somewhat weaker set of security assumptions: they are fine if *either one* of two assumptions is true: (i) network latency is low, including network latency between validators and clients, and (ii) the majority of validators is honest. First, let us get back to the model where we have a blockchain with some fork choice rule, instead of just discrete blocks. We will go through examples for our two favorite finality-bearing fork choice rules, (i) FFG and (ii) LMD GHOST.

For FFG, we extend the fork choice rule as follows. Start from the genesis, and whenever you see a block with two child chains which are both finalized, pick the chain with the *lower-epoch timely finalized block*. From there, proceed as before. In general, there will only ever be two conflicting finalized chains in two cases: (i) a 33% attack, and (ii) many nodes going offline (or censoring) leading to a long-running inactivity leak.

Case (i):

[![51attack4](https://ethresear.ch/uploads/default/original/2X/1/192557548a219b3dcceaf32fd375cb06bde8385a.png)51attack4581×271 8.08 KB](https://ethresear.ch/uploads/default/192557548a219b3dcceaf32fd375cb06bde8385a)

Case (ii), option 1 (offline minority finalizing later):

[![51attack5](https://ethresear.ch/uploads/default/optimized/2X/a/a08acea159b8103dcdd8ac4be59a12481b61c306_2_690x276.png)51attack5726×291 9.95 KB](https://ethresear.ch/uploads/default/a08acea159b8103dcdd8ac4be59a12481b61c306)

Case (ii), option 2 (offline majority, later reappearing with finalized chain):

[![51attack6](https://ethresear.ch/uploads/default/optimized/2X/8/8bfc51a9550c5a40cd3022f5b97be37c46dbcee4_2_690x263.png)51attack6761×291 10.2 KB](https://ethresear.ch/uploads/default/8bfc51a9550c5a40cd3022f5b97be37c46dbcee4)

Hence, in all cases, we can prevent 51% attacks from breaking finality, at least past a certain point in time (T + 2k\delta, the time bound after which if a client has not accepted a block as timely then we know that it will *never* accept it as timely). Note also that the above diagram is slightly misleading; what we care about is not the timelines of *the finalized block*, but rather the timeliness of a block *that includes evidence* that proves that the block is finalized.

For clients that are offline sometimes, this does not change anything as long as there is no 51% attack: if the chain is not under attack, then blocks in the canonical chain will be timely, and so finalized blocks will always be timely.

The main case where this may lead to added risk is the case of clients that have high latency *but are unaware that they have high latency*; they could see timely blocks as non-timely or non-timely blocks as timely. The goal of this mechanism is that if the non-timeliness-dependent fork choice and the timeliness-dependent fork choice disagree, the user should be notified of this, so they would socially verify what is going on; they should not be instructed to blindly accept the timeliness-dependent fork choice as canonical.

### Dealing with censorship

We can also use timeliness detectors to automatically detect and block censorship. This is easy: if a block B with self-declared time t is timely, then any chain that does not include that block (either as an ancestor or as an uncle) before time t + (2k+2)\delta is automatically ruled non-canonical. This ensures that a chain that censors blocks for longer than (2k+2)\delta will automatically be rejected by clients.

[![51attack7](https://ethresear.ch/uploads/default/original/2X/1/1b6ca873b13b928529b1441ae9b222a118c3e1bb.png)51attack7561×131 2.44 KB](https://ethresear.ch/uploads/default/1b6ca873b13b928529b1441ae9b222a118c3e1bb)

The main benefit of using timeliness detectors here is that it creates consensus on when there is “too much” censorship, avoiding the risk of “edge attacks” that are deliberately designed to appear “sufficiently bad” to some users but not others, thereby causing the community to waste time and energy with arguments about whether or not to fork away the censoring chain (instead, most users would in all cases agree on the correct course of action).

Note that this requires an uncle inclusion mechanism, which eg. eth2 does not have. Additionally, it requires a mechanism by which transactions inside of uncles get executed, so that the censorship resistance extends to transactions and not just the raw bodies of blocks. This [requires care](https://ethresear.ch/t/stateless-ees-and-delayed-block-inclusion/6839) to work well with stateless clients.

One additional nitpick is that care is required to handle the possibility of many blocks being published and gaining timeliness status and needing to be included as uncles at the same time. This could happen either due to delayed publication or due to a single proposer maliciously publishing many blocks in the same slot. The former can be dealt with via a modified rule that blocks must include *either* all timely blocks that are older than (2k+2)\delta *or* the maximum allowed number (eg. 4) of uncles. The latter can be dealt with with a rule that if one block from a particular slot is included, all other blocks from that slot can be validly ignored.

Note that in the Casper CBC framework, censorship prevention and de-prioritization of chains containing non-timely or censoring blocks by itself suffices to provide the same finality guarantees as we saw for the FFG framework above.

### Challenges / todos

1. (Non-technical) Come up with the best way to explain to users what happened in the event that timeliness-aware and non-timeliness-aware fork choice rules disagree, and how they should respond to the situation.
2. Analyze the behavior of the system in cases where latency is sometimes above \delta, or latency is always potentially above \delta but we have assumptions that eg. some fixed fraction of attesters is honest, or other hybrid assumptions. See if there are ways to modify the rules to improve performance in those scenarios.
3. Analyze ways to achieve these properties without including a new class of attestation; instead, reuse existing attestations (eg. the attestations that validators make every epoch in FFG)
4. Determine if there are small modifications to “simple” longest-chain-based fork choice rules that allow them to benefit from timeliness detectors to gain a kind of finality.

## Replies

**dankrad** (2020-02-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> then (at least because they themselves can rebroadcast it) that block will get into the hands of an attester before the attester deadline T+δT + \delta

Should this be T + 2 \delta?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Hence, in all cases, we can prevent 51% attacks from breaking finality, at least past a certain point in time ( T+2kδT + 2k\delta , the time bound after which if a client has not accepted a block as timely then we know that it will never accept it as timely).

What you’re saying is also, if both chains are published at the same time, there’s really nothing we can do in terms of choosing the right one. I guess in that case we just display the message “consensus failure” to the user and wait for social recovery?

---

**vbuterin** (2020-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Should this be

Thanks! Will fix.

> What you’re saying is also, if both chains are published at the same time, there’s really nothing we can do in terms of choosing the right one. I guess in that case we just display the message “consensus failure” to the user and wait for social recovery?

If we want to, we can force a choice, eg. “pick the chain with more signatures”. So then a finalized block could for a short time be reverted with an attack that slashes \ge \frac{1}{3} of validators; “true finality” would come 2k\delta after finality.

---

**dankrad** (2020-02-13):

Anyway, I’m very excited about this direction. When I first read this I thought it can’t be possible to do this automatically, but it turns out you actually can! Wow!

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Analyze the behavior of the system in cases where latency is sometimes above δ\delta , or latency is always potentially above δ\delta but we have assumptions that eg. some fixed fraction of attesters is honest, or other hybrid assumptions. See if there are ways to modify the rules to improve performance in those scenarios.

So the latency above delta would only matter if there is an attack, right? If there’s only one chain, we will always accept it, whether it’s delayed or not. However, if we see two chains, we have three possibilities:

1. Both are timely. Synchronous attack. Here it’s best to just stop
2. One is timely, one is not – notify the user, and present the timely chain as likely correct one and default option
3. Neither is timely – again, can’t do anything and best to just stop.

---

**vbuterin** (2020-02-13):

> So the latency above delta would only matter if there is an attack, right? If there’s only one chain, we will always accept it, whether it’s delayed or not. However, if we see two chains, we have three possibilities:

Correct.

---

**terence** (2020-02-13):

Nice write up! This is interesting. How much of this do you think is applicable for the current eth2 landscape? Do you see eth2 phase 1 incorporate some of the mentioned techniques?

---

**vbuterin** (2020-02-13):

I definitely think it’s applicable! I personally definitely hope we can move in this direction, though I think to get there there are some shorter-term things we need to do:

1. Have a clearer understanding of recourse from 51% attacks in general. Particularly, what happens if an invalid sharded block gets included in a chain? Do we abandon that entire chain? Do we do some kind of in-state rollback (effectively turning the chain into a rollup)? Do we remove that possibility entirely by adopting a “phase 1 and done” shards-are-data-only mentality and move all of the EE work into layer-2 rollups, and use something like Kate commitment-based data availability checks (and maybe STARKed Merkle roots later) to verify data availability of blocks?
2. Have an uncle inclusion mechanism, and a clear understanding of how uncles get executed (note that if we do the “phase 1 and done” approach, then this is much less of a problem)
3. Have a better strategy for dealing with attacks where large portions of validators maliciously prevent committees from hitting quorum. Currently, we only deal with habitually offline validators; ideally we would require a validator to be part of 2/3+ of committees to stay in the quorum, so that we have a hard guarantee that quorums happen (and do some extra stuff to ensure that quorums happen on every shard).

---

**archieforuwu** (2024-12-26):

At the moment I’m not sure what δ is. Is it the max delay to reach all the network or just average delay between two nodes? In my reply I assume the first. (if it was the second we’d reject blocks broadcasted more than 1 hop away)

About timeliness detectors:

It’s more chances to block being accepted timely than otherwise (I think it can be close to 100%). If I send my block not at the deadline timestemp D to reach all the nodes but at D + δ/3*2, so it will be accepted by 33% of nodes, so 33% chance an attester to be there. And if the attester sends it now it will be accepted by all network as timely because he has whole δ of time. If he had only δ/2 of time then his signature would accepted as new by max at 38% of nodes and the block at 71% of nodes among which would be another attesters.

