---
source: ethresearch
topic_id: 4749
title: Bitwise LMD GHOST
author: vbuterin
date: "2019-01-04"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/bitwise-lmd-ghost/4749
views: 7947
likes: 8
posts_count: 10
---

# Bitwise LMD GHOST

Prerequisite: https://vitalik.ca/general/2018/12/05/cbc_casper.html

I propose a version of the LMD GHOST fork choice rule and an algorithm that makes it easy to tell whether or not a given block is valid under the CBC validity condition of “a block B with parent P is valid if all the evidence included in the state of B points to P being the correct result of the LMD GHOST fork choice rule”. This is a step toward making CBC practically implementable.

In general, GHOST-style fork choice rules follow the same pattern: start with some block H, then let C_1... C_n be the children of H. If the list of children is empty, just return H, if there’s one child then set H to that child and repeat, and if there is more than one child, choose the child that has the strongest support (this could be latest message count, proof of work, or one of many other metrics).

I propose a modification that makes forks always binary (that is, any H has at most two children): if a given block H has multiple children, then arrange the children into a virtual tree where we are deciding bit-by-bit on the hash of the child. For example, if H has three children C_1, C_2, C_3 with hashes 010..., 011... and 101..., then the tree looks as follows:

![image](https://ethresear.ch/uploads/default/original/3X/5/6/5699a9129c4b3aea49932739dd5b177683fd5b79.svg)

Note that this means that if any of the three children has more support than the other two combined (ie. at least 51%), then it will win in the GHOST fork choice as before, but if none of the three strongly dominate then the result could be different, for example if C_1 has score 4, C_2 has score 3 and C_3 has score 5, then under simple LMD GHOST C_3 would win, but in modified GHOST C_1 would win.

Conjecture: this difference does not actually matter much in real life, and does not make any attacks easier, because any attack that takes advantage of the new structure where C_1 and C_2 support each other could have also succeeded in a three-way fork where H had two regular children D and C_3, where C_1 and C_2 were children of D.

Now, let’s see what this enables. We assume that the blockchain state keeps track of the following data structure: for each validator, what is the height up to which the block that their latest attestation pointed to agrees with the current chain? We store this as a number: `256 * actual_shared_height + number_of_common_bits`, where `number_of_common_bits` is the number of initial bits in common between the hash of the chain’s actual next block and the hash of the ancestor of the message signed by the validator at the lowest height that is not shared with the chain. That is, if the actual chain has head B_1 and a validator’s latest message is B_2, and B_1 and B_2 have common ancestors up to height n, and at height n+1 the ancestors of B_1 and B_2 agree in their first k bits, then the “virtual agreement height” stored is n * 256 + k.

We also maintain a mapping: virtual height → how many validators whose latest message agrees up to this virtual height. We store it in a sum tree, so we can now determine in O(log(n)) time how many validators agree with the main block up to at least some given virtual height (we call this agreeing[h]). To determine if a block is valid, we now need only verify one property: that there is no virtual height h where agreeing[h+1] < (agreeing[h] - at[h]) * \frac{1}{2}, where at[h] is the set of validators that agree up to exactly h and whose latest signed message is of a block at exactly that height. If it is the case that there is no such h, then the current block’s parent actually is the LMD GHOST evaluation of the messages the block knows about.

Because agreeing[h] declines monotonically (as it represents how many validators agree up to at least that point), we can do this in O(log^2(n)) time: binary-search the max height h where at least half of all validators agree, verify that agreeing[h+1] \ge (agreeing[h] - at[h]) * \frac{1}{2}, then binary-search the max height h where at least a quarter of all validators agree, and so forth until you reach the head.

Notice that the fact that each node in the virtual tree can only have at most two children is necessary for this technique to work, as it ensures that verifying that agreeing does not “step down too quickly” is necessary and sufficient for verifying bitwise GHOST compliance.

## Replies

**naterush** (2019-01-04):

This is extremely cool - and is very reasonable from a specification-complexity standpoint as well!

To make sure I understand, this proposal adds the following two maps to the state:

1. A map from Validator → Virtual Height. I’ll call this agrees\_to, where agrees\_to[v] is, as you say, the virtual height up to which the block that v's latest attestation pointed to agrees with the current chain.
2. A map from Virtual Height → Weight. This is the agreeing map, where agreeing[h] is sum of the weights of the validators v where agrees\_to[v] \geq h.

> We store it in a sum tree

Quick questions here. Can you elaborate on how the sum tree is used to create this map, and how it is updated when a new attestation is made? Probably very simple, but I’ve never seen sum trees used before ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

A good goal in the next few weeks would be to specify the beacon-chain block structure, and this forkchoice rule, entirely in the language of the CBC framework. It’s a good excuse to check out the beacon-chain spec as well - so I’m happy to work on this!

---

**vbuterin** (2019-01-04):

> To make sure I understand, this proposal adds the following two maps to the state:

Yep! Though I think you also need a third map, at[block\_hash], which stores how many validators’ latest messages signed exactly some block hash.

> Quick questions here. Can you elaborate on how the sum tree is used to create this map,

Generically, suppose you have a set of indices, 0....n-1, with some value v[i] stored at each index. We store this as an array, A = 0.....2n-1, where A[n+i] = v[i]. Set A[i] = A[i*2] + A[i*2+1] for i < n, up to A[1] which is the sum of the entire list \sum_{i=0}^{n-1} v[i]. When any v[i] is updated, update the A[i] values upstream from it (log(n) operations required).

To compute a partial sum \sum_{i=0}^{k-1} v[i], we convert it into a sum of 2^i-sized sums, each of which is a single entry in A[i]. Specifically, for every 1 bit at position i in the binary representation of k, take A[floor(\frac{n+k}{2^i}-1)], so for v[11] with n = 16, where 11 = 2^3 + 2^1 + 2^0, take A[floor(\frac{16+11}{1}-1)] + A[floor(\frac{16+11}{2}-1)] + A[floor(\frac{16+11}{8}-1)], or A[26] + A[12] + A[2]. We can see A[12] = A[24] + A[25] and A[2] = A[4] + A[5] = \sum_8^{11} A[i] = \sum_{16}^{23} A[i], so this set of A values covers the sum of the entire subset of v that we want.

---

**naterush** (2019-01-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Because agreeing[h] declines monotonically (as it represents how many validators agree up to at least that point), we can do this in O(log^2(n)) time: binary-search the max height h where at least half of all validators agree, verify that agreeing[h+1] \ge (agreeing[h] - at[h]) * \frac{1}{2}, then binary-search the max height h where at least a quarter of all validators agree, and so forth until you reach the head.

In case it’s useful for anyone else (as it took me a second to convince myself) - here’s the argument for why this validity check ensures there is no height h where agreeing[h+1] < (agreeing[h] - at[h]) * \frac{1}{2}. Let’s call this invalidity condition **(1)**.

Assume the validity check passes, but there are some heights where **(1)** occurs. Let h be the lowest of such heights. Let x be the “current set of validators” under consideration at the step that considers h in the validity check (x is at first 1, then \frac{1}{2}, then \frac{1}{4}, etc). Thus, as agreeing[h+1] < (agreeing[h] - at[h]) * \frac{1}{2}, clearly h is the largest height such that at least \frac{x}{2} agrees. But as the validity check passes, we have that agreeing[h+1] \ge (agreeing[h] - at[h]) * \frac{1}{2}. However, this is clearly a contradiction with **(1)**. Thus, no such height h can exist where agreeing[h+1] < (agreeing[h] - at[h]) * \frac{1}{2}.

---

**AgeManning** (2019-02-18):

Curious about the conjecture.

Let’s consider the same scenario mentioned, C_2 has score 3 and C_3 has score 5 and I hold 4 votes and want to manipulate the fork. Under regular GHOST, there is no way for me to construct a block to be chosen as the head, as C_3 will always win (I would need to also manipulate the 3 votes from C_2 and construct D as is mentioned). In modified GHOST it seems I can take the head of the chain with only my 4 votes by constructing C_1 without the need of manipulating C_3.

Does this not decrease the number of validators required to manipulate the fork-choice compared to regular GHOST?

---

**vbuterin** (2019-02-19):

In “regular GHOST” there is always the potential scenario where C_1 and C_2 are children of some common parent C_{1,2} which competes with C_3; in that case, an attacker would face the same scenario as they do in the LMD GHOST situation described in the post.

So bitwise LMD GHOST doesn’t bring any *fundamentally* new possibilities into the attack space.

---

**nrryuya** (2019-03-23):

Thanks for this interesting idea! Here is my concern.

> Conjecture: this difference does not actually matter much in real life

I think the “modified GHOST” require a larger threshold for clique oracle (and hence it takes a longer time to finality) than the “regular GHOST” because the modified LMD GHOST is only “majority driven” i.e. a block need to be supported by more than the majority to be finalized.

For a majority driven fork-choice, the threshold of the ratio of a clique to the validator sets (by weight) is 1/2 + t - e where t is the equivocation fault threshold and e is the ratio of the observed equivocating validators.

For plausible liveness, t need to be lower than 1/4.

The “regular GHOST” is “max driven” i.e. the greatest set of validators agreeing on a block is sufficient for the block to be finalized. In this case, the threshold of a clique is 1/2 + t/2 - e and for plausible liveness t < 1/3.

(The original definitions of “majority driven” and “max driven” are introduced by Nate in [the draft of section 7](https://github.com/cbc-casper/cbc-casper-paper/pull/13) of the CBC paper. The compiled version is [here](https://drive.google.com/file/d/1lGg0RDZ7BW7DnuJKP_YWaYe5VN2TPEw2).)

---

**vbuterin** (2019-03-23):

I’m not sure why the max driven vs majority driven distinction leads to that consequence. In the case where there are two children of some block, they seem identical, and in the case where there are more than two children, that’s just splitting the attacker so it’s not beneficial to them (but also don’t harmful because attackers don’t have to split).

---

**nrryuya** (2019-03-23):

I’m sorry I was misunderstanding a bit about bitwise-tree ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12). The modified GHOST is still max driven (i.e. a block is finalized if the validators locked on that block is larger than the validators who are not locked on that block).

> I’m not sure why the max driven vs majority driven distinction leads to that consequence

Basically, because a max driven fork-choice requires fewer validators locked on that block.

The threshold is for `(honest agreeing) > (honest disagreeing) + (potential equivocation)`,

W(V) > W(\mathcal{V} \setminus V \setminus E(\sigma)) + (t - F(\sigma)) \\
\iff 2 * W(V) > W(\mathcal{V}) + t - 2 * F(\sigma) \\
\iff W(V) > W(\mathcal{V})/2 + t/2 - F(\sigma)

---

**adiasg** (2019-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/nrryuya/48/1552_2.png) nrryuya:

> For plausible liveness, t need to be lower than 1/4.

Background reasoning: Plausible liveness is achieved when the set of honest validators can possibly satisfy the threshold. So, threshold weight should be lower than (or equal to) weight of honest validators: \frac{1}{2} + t - e \leq 1 - t - e \implies t \leq \frac{1}{4}.

Similar reasoning for the “regular GHOST” case.

