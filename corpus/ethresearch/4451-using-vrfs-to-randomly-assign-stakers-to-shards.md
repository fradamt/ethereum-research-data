---
source: ethresearch
topic_id: 4451
title: Using VRFs to randomly assign stakers to shards
author: poemm
date: "2018-12-03"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/using-vrfs-to-randomly-assign-stakers-to-shards/4451
views: 4134
likes: 1
posts_count: 3
---

# Using VRFs to randomly assign stakers to shards

Below is a copy of [this brief document](http://paul.oemm.org/eth/VRF_Based_Random_Next_Shard_Mechanism.pdf) and an image.

**ABSTRACT.** We sketch a mechanism which randomly assigns each staker to their next shard by using their Verifiable Random Function (VRF). We sketch proofs for unpredictability, liveness, and biasability. Many details and optimizations are omitted in favor or conciseness and simplicity.

**Definition** (Sketch.) *VRF-based random next-shard mechanism*.

- A staker’s VRF output determines their next shard, time at that shard, etc. When a staker must move to their next shard, they compute their VRF on an input x based on the previous n VRF outputs from stakers who just moved. (Say x is the xor of the previous n VRF outputs.)
- A new staker deposits a stake (say 32 Eth) and a public key which corresponds to their VRF. New stakers must wait n VRF outputs from when they deposit before computing their first VRF output. For security, this first VRF output is not used as input to other staker’s VRFs.

**Theorem.** Assume that there is an honest majority of stakers. Then a VRF-based random next-shard mechanism gives unpredictability and liveness, but not unbiasability.

Proof. (Sketch.)

- Unpredictability is achieved by having n large enough that there is a high probability that at least one in every n consecutive VRF evaluations is by an honest member.
- Liveness is achieved by participation of the honest majority.
- Unbiasability is not achieved because a staker can choose to withhold their VRF output.

**Remarks.**

- Bias from withholding a VRF output is local – withholding only helps one (or few) stakers under the attacker’s control. This withholding can cost their stake, so it is not worth it unless they are close to attacking a specific shard and lucky enough to be sent to that shard.
- Unbiasability may be achieved(!) with a VDF (verifiable delay function) producing the input to each VRF.
- The honest majority assumption can be relaxed to a lower percent.
- There may be an unequal number of stakers in each shard. But if the VRFs provide uniform randomness, and there are many stakers, then there is high probability that the shards have a nearly equal number of stakers.
- A beacon chain can be used to record each VRF output, along with any new staker’s stake.
- VRFs are already used by Algorand and Ouroboros blockchains, but they don’t have shards (yet) and have different VRF inputs and different output meaning. This mechanism is novel because inputs and outputs are local to each staker.

[![drawing](https://ethresear.ch/uploads/default/optimized/2X/9/96c95d25fd32207d5f7d5cb594826a4c79e39036_2_690x231.png)drawing1875×628 99.6 KB](https://ethresear.ch/uploads/default/96c95d25fd32207d5f7d5cb594826a4c79e39036)

## Replies

**dlubarov** (2018-12-04):

Nice writeup Paul! I would just add that if a staker wishes to withdraw, they should be required to remain for at least one full “shift” following their request. Otherwise, a staker who is targeting a particular shard could do “better than random” by withdrawing whenever they’re about to be assigned to a different shard.

I think of VRF-based randomness as being very similar to RANDAO, except that determinism removes the need for commitments. So if we want to reduce biasability, we can use similar techniques:

1. Batch k VRFs together, and use the result for the next k blocks
2. The subcommittee scheme you proposed
3. Avalanche RANDAO

We’re planning to use #1 for our project. Its biasability is worse than #2 and #3, but it’s still very low if we use a large batch size, and we prefer to avoid public key encryption.

---

**poemm** (2018-12-05):

Daniel, thank you for your nice response. Agreed that a departing staker should signal that early.

One point I want to emphasize: This mechanism uses *local* randomness, avoiding *global* randomness which has more incentive for bias. So this mechanism reduces bias in some sense.

Great observation that this mechanism can be restated using commit-reveal, allowing similar bias-reduction techniques to be applied – batching, subcommittees, avalanche, VDFs, etc.

BTW Another such technique to reduce bias in commit-reveal follows. (Maybe it deserves it’s own post.)

**Definition.** *Reveal-forcing filter.*

Consider a commit-reveal procedure, each committee member commits to their secret s_i\in \mathbb{Z} by publishing value g^{s_i}, where g generates cyclic group G of order p. At reveal-time, each member can reveal their secret in order. Each member’s contribution to randomness is the output of a n-linear map e:G^n\to G_T, where G_T is also a cyclic group of order p, and e is defined as follows.

- case n=1: The contribution of the i^{\text{th}} member is g^{s_{i-1}s_{i}} which can be computed if s_{i-1} is revealed using (g^{s_{i}})^{s_{i-1}}.
- case n=2: The contribution of the i^{\text{th}} member is e(g,g)^{s_{i-2}s_{i-1}s_{i}} which can be computed by from s_{i-1} with pairing e(g^{s_{i-2}},g^{s_{i}})^{s_{i-1}}. Similarly, from s_{i-2}.
- case n=m: The contribution of the i^{\text{th}} member is e(g,g,...,g)^{s_{i-m+1}s_{i-m+2}\cdots s_i} which can be computed using any s_k by m-linear map e(g^{s_{i-m+1}},g^{s_{i-m+2}},...,g^{s_{k-1}},g^{s_{k+1}},...,g^{s_{i}})^{s_k}.

**Remark.** Only *ONE* honest member is needed in each neighborhood. But this increases look-ahead, so perhaps it should only be used for the last revealers in current randao.

