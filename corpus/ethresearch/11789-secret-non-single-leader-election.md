---
source: ethresearch
topic_id: 11789
title: Secret non-single leader election
author: vbuterin
date: "2022-01-16"
category: Proof-of-Stake
tags: [single-secret-leader-election]
url: https://ethresear.ch/t/secret-non-single-leader-election/11789
views: 11467
likes: 24
posts_count: 9
---

# Secret non-single leader election

## Single and non-single proposer selection: introduction  and context

Ethereum’s current approach to proof of stake works by picking a *single* validator using a publicly computable random function to be the proposer for each slot. This is in contrast to PoW, where instead every validator has an *independent random chance* of being a valid proposer at any given time.

Ethereum’s single-proposer approach always picks exactly one proposer, whereas the PoW-style approach gives a [Poisson distribution](https://en.wikipedia.org/wiki/Poisson_distribution), and so often selects multiple proposers at the same time (in which case, the proposer with the better internet connection gets an unfair advantage). However, the single-proposer approach makes the proposer publicly known ahead of time, making them vulnerable to DoS attacks.

[Single secret leader election](https://eprint.iacr.org/2020/025.pdf) (see: [Whisk](https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763)) aims to get the best of both worlds: select a single proposer using a cryptographic procedure that ensures that only the proposer knows when they are selected. Each validator submits a commitment to a secret, and then the commitments are repeatedly blinded and re-shuffled. When it comes time to choose a proposer, a random commitment is publicly chosen, but because of the blinding only the proposer knows that the commitment corresponds to *them*.

This post explores an alternative based on protocol engineering rather than cryptography: **what if we remove the requirement to have a *single* chosen leader? What if we go back to giving each validator an independent random chance of being a valid proposer, but actually try to handle conflicts fairly?**

## A concrete proposal

Suppose that there are N active validators. Each validator has a \frac{5}{N} chance of being a valid proposer at any given slot. One simple way of implementing this is to require that the hash of the [randao reveal](https://github.com/ethereum/annotated-spec/blob/3855127b22e989b52371188c830b1a4769eca762/phase0/beacon-chain.md#aside-randao-seeds-and-committee-generation) of the block must be less than \frac{2^{256} * 5}{N}. The randao reveal has the property that there is only one possible valid value that any validator can generate in any slot, but this value can only be calculated ahead of time by the validator themselves. This is ideal: it means that only the validator themselves can know ahead of time whether or not they are a valid proposer at a given slot.

The above parameters create a [Poisson distribution](https://en.wikipedia.org/wiki/Poisson_distribution) with \lambda=5. During each slot, there is a 1 - e^{-5} \approx 99.3\% chance of having at least one proposer. However, there is also a \approx 96\% chance that there will be more than one proposer. How could we fairly, and safely, deal with this situation?

Fairness alone is easy to solve: if there are multiple proposers, they all propose, and the one with the lowest randao reveal hash wins. But is this safe?

### Easy case: all valid proposers honest or offline

[![Proposals.drawio (1)](https://ethresear.ch/uploads/default/original/2X/b/b3420004bc8aa82362cd6a131c657b262d68c03c.png)Proposals.drawio (1)371×356 13.4 KB](https://ethresear.ch/uploads/default/b3420004bc8aa82362cd6a131c657b262d68c03c)

All proposers propose at time T, and all proposals reach all attesters before T + 4. Attesters all vote for the proposer with the lowest randao reveal, and so there is one leading proposer with a large fork choice advantage over the others.

### Medium case: the lowest-hash proposer is honest, some other proposers are dishonest

[![Proposals.drawio (2)](https://ethresear.ch/uploads/default/original/2X/b/b6d867cde50d76cf985ae553f056842904f39fdc.png)Proposals.drawio (2)326×266 7.52 KB](https://ethresear.ch/uploads/default/b6d867cde50d76cf985ae553f056842904f39fdc)

The lowest-hash proposer proposes at time T, and their proposal reaches all attesters before T + 4. Some attesters see other proposals as well, others don’t. However, they still all vote for the same lowest-hash proposer, and so there is one leading proposer with a large fork choice advantage over the others.

### Hard case: the lowest-hash proposer is dishonest

[![Proposals.drawio (3)](https://ethresear.ch/uploads/default/original/2X/a/a68907a150ca732dc0478d17b96df34c38a55517.png)Proposals.drawio (3)326×266 7.49 KB](https://ethresear.ch/uploads/default/a68907a150ca732dc0478d17b96df34c38a55517)

The lowest-hash proposer P_1 proposes at time T+3.5; some attesters see it before T+4 and others do not. The network is split between attesters voting for P_1 and attesters voting for some other P_2 (or occasionally an empty slot).

This is the same situation as what happens in the status quo, and so far we’ve established that it happens with *only the same probability* as in the status quo (and not a higher probability because of multiple proposers). The question, however, is: **is recovery harder**?

Recovery in the status quo happens through [proposer boosting](https://notes.ethereum.org/@vbuterin/lmd_ghost_mitigation). We assume that the chain continues to be potentially chaotic for one or more slots until there is a slot with an honest proposer. At that point, the honest proposer produces a block, and we give that block an extra bonus to their fork choice score, enough to override a large portion of the attesters. The attesters for that next slot, when computing the fork choice, only take into account attestations that they received before the start of that slot, plus the proposer boost, and so there is one single actor that “pushes” the fork choice split to one side or the other.

Can we replicate proposer boosting in the multi-proposer case? It seems that we can: **we only apply the proposer boost to the lowest-hash proposal**. The attestations are published at time T+4, which is also the attesters’ deadline for receiving proposals. Hence, they know about all of the proposals that they will consider, and so they can figure out which one has the lowest hash and apply the proposer boost to it. If the lowest-hash proposer is honest, this will work for the same reasons why proposer boosting works in the status quo.

[![Proposals.drawio (4)](https://ethresear.ch/uploads/default/original/2X/a/ac2dcfee44f52fa40345a4d2599550ff963f6e15.png)Proposals.drawio (4)596×264 15.9 KB](https://ethresear.ch/uploads/default/ac2dcfee44f52fa40345a4d2599550ff963f6e15)

The main difference is that if the lowest-hash proposer is malicious, then attesters may have a 2x larger disagreement in their fork choice views: instead of some attesters seeing the boost and others seeing no boost, some see a boost in one direction and others see a boost in the other direction. **This may reduce the maximum safe size of a boost by up to 2x and should be studied more, but is not a fatal flaw**.

### Extending to PBS

One small change to the [current PBS proposal](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980) seems to be required. In the current proposal, the proposer boost of a builder is larger than the entire attestation committee. This would be risky in a multiple-proposer-per-slot world for a similar reason to what is identified above: if a builder builds on a block B_1, but there is a proposer with a lower-hash randao that has not yet published, then they could release B_2 and steal the MEV from B_1. The fix is to make the builder’s proposer boost smaller, so that the builder B_1 would only publish after attestations on top of B_1 have been made and those attestations would ensure that it beats B_2 in the fork choice and B_2's proposer boost would not overrule them.

## Replies

**JustinDrake** (2022-01-17):

Secret elections with multiple proposers per slot allow for “time buying” MEV attacks. An attacker (e.g. a pool) which controls two proposers in the same slot can publish two proposals:

1. a “safe” proposal which is published early enough to reach most attesters in time
2. a “risky” proposal which is published after the safe proposal

The risky proposal is at a greater risk of not reaching most attesters in time (and therefore not make it on-chain) but has more MEV than the safe proposal (from the extra time “bought”).

Notice that the attacker benefits from the possibility of extracting more MEV via the risky proposal in addition to the fallback provided by the safe proposal.

Such time buying strategies have two negative externalities:

1. validator centralisation because of the incentive to have multiple proposers per slot
2. builder centralisation because of the incentive to build multiple blocks per slot

---

**ittaia** (2022-01-27):

1. If you really want strong MEV protection you may need to look at MPC/Blinder etc…
2. For a lightweight solution, using a bit of synchrony:
A. Proposers commit by sending the hash of their proposal (or via VDF if you have one)
B. Then a randomness beacon (threshold signature on block number for example or VDF) outputs a fresh public value
C. Then each proposer can use the beacon value and her commitment and compute a VRF rank (say deterministic signature on commit+public rand or the reveal proof of the VDF and hash of public randomness)
D. If your VRF has low rank then you try to propose (if more time passes more try)
E. The validators wait and then attest to the lowest rank VRF for which they have data availability of the proposal (attests only once like FFG)

Maybe minor diff is here you do not know ahead of time if you are going to win, only after you commit and then see the public rand, may be an advantage for MEV?

---

**bowaggoner** (2022-02-04):

- What about the case where there is only one valid proposer, and they are dishonest? Does an issue arise when some attesters think there were zero valid proposers and other attesters think there was one? [Edit 2023-02-05: this may be what was referenced by “or occasionally an empty slot”.]
- Would it be possible, with some more work, to select exactly 5 valid proposers every round, rather than just 5 in expectation? I don’t see the Poisson distribution as a positive. Just as a naive proof of concept, there should be a decent algorithm to fairly map a list of potential proposers and a random seed to a choice of exactly 5 valid proposers.
- What about sybils? Do I have a higher chance of winning in this system from splitting into two identities? (That wouldn’t be terrible, it’s better than encouraging pooling.) This is additional to JustinDrake’s point.

Apologies if the questions are naive, I may not have all the background.

---

**Sh4d0wBlade** (2023-01-20):

Do you figure out the answers to your questions? I have the same with yours.

---

**casparschwa** (2023-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Secret elections with multiple proposers per slot allow for “time buying” MEV attacks.

Note that the status quo already suffers from the possibility of time-buying attacks. A block proposer can show up late and still become canonical.

I agree that controlling multiple proposers is beneficial in that you can propose a safe block. However, this is only true if the adversary controls the proposals with the two lowest hash values of their randao reveals.

My point is that time-buying makes sense in the status quo as well as in this scheme. The adversary just needs to carefully tune their block release time such that a majority of attesters hears their block in time. Simply add a little safety margin in your release strategy, i.e. don’t try to target 50%+1, but say 60% of attesters hearing the adversarie’s block in time. So in theory the extra proposal in this scheme buys you the ability to be slightly more risky with your release strategy of the second block, but this should be a fraction of a second. In short, practically I do not think an extra proposal in this scheme will add much to the expected payoff, since the timing of releasing the “risky” block will only be marginally later than the optimal release time when the proposer only controls a single block.

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> What about the case where there is only one valid proposer, and they are dishonest? Does an issue arise when some attesters think there were zero valid proposers and other attesters think there was one?

I’d think that this scenario would be treated as in the status quo: Attesters that see the dishonest proposal in time will vote for it, the remaining attesters will vote for whatever they consider as head of the chain without the dishonest block in their view (presumably the preceeding block). The next block proposer would extend the chain by building on the dishonest proposal (as they will have had 8 more secs to hear the dishonest proposal + the fact that the dishonest proposal inherits the fork choice weight of the preceeding block as they are not competing).

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> What about sybils? Do I have a higher chance of winning in this system from splitting into two identities? (That wouldn’t be terrible, it’s better than encouraging pooling.) This is additional to JustinDrake’s point.

Not sure what the questions is, but running multiple validators is obviously beneficial in the status quo as well as in this scheme. If you mean p2p nodes, then you can buy yourself even more time by releasing your late block from several p2p nodes with different locations across the network. This will speed up the propagation of the late block meaning that you can release it even later while a majority of attesters still hears the block in time.

---

**llllvvuu** (2023-02-06):

What are the motivations for this? Better liveness? Anything else?

---

**casparschwa** (2023-02-06):

It is an alternative idea to another proposal (Whisk). Both try to protect proposers from DoS attacks as explained by Vitalik:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> However, the single-proposer approach makes the proposer publicly known ahead of time, making them vulnerable to DoS attacks.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Single secret leader election  (see: Whisk ) aims to get the best of both worlds: select a single proposer using a cryptographic procedure that ensures that only the proposer knows when they are selected.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This post explores an alternative based on protocol engineering rather than cryptography

---

**ethDreamer** (2023-05-24):

Without PBS there’s a worse attack than this if you have two proposers in the same slot:

1. Send block with higher RANDAO to relay, sign, and broadcast
2. Relay reveals transactions
3. Steal MEV from relay, and publish in the block with lower RANDAO

