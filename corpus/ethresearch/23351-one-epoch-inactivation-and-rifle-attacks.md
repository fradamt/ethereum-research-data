---
source: ethresearch
topic_id: 23351
title: One-epoch inactivation and Rifle attacks
author: Mediabs2022
date: "2025-10-27"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/one-epoch-inactivation-and-rifle-attacks/23351
views: 155
likes: 1
posts_count: 1
---

# One-epoch inactivation and Rifle attacks

# Three kinds of one-epoch inactivation attack

**One-epoch inactivation attack** is a method that can harm Ethereum liveness even under synchronous assumptions: it can render one epoch inactive by preventing the checkpoint justification update during the attacked epoch. We propose three variants of one-epoch inactivation attacks, each augmented with specific *sly* strategies. These extend and refine existing attacks (the ex-ante attack, the sandwich attack, and the 1/3-slot-withhold attack) so that—while preserving the original reorg or withholding effects—they achieve additionally liveness degradation or less Byzantine loss.

### 1. Sly-ex-ante attack

The sly-ex-ante attack occurs when slot t is the first slot of an epoch and the proposer at slot t is honest, while the proposers at slots t-2 and t-1 are Byzantine. The modified ex-ante reorg attack in [1] demonstrates how to bypass proposer boosting; our sly-ex-ante attack further optimizes the attacker’s strategy on that basis.

[![one-inactivaty-sly-ex-ante.png](https://ethresear.ch/uploads/default/optimized/3X/7/f/7f5a2dd00e0a2821ef42890edc6c895f0c67186c_2_690x310.png)one-inactivaty-sly-ex-ante.png1051×473 23.3 KB](https://ethresear.ch/uploads/default/7f5a2dd00e0a2821ef42890edc6c895f0c67186c)

The attack proceeds as follows (notation: blocks proposed in slot t-2, t-1, and t are denoted b_i, b_{i2}, and b_t, respectively):

1. Delayed release within slot t. The Byzantine proposers in slots t-2 and t-1 propose blocks b_i and b_{i2} but delay releasing these blocks and their corresponding attestations until slot t. Specifically, the Byzantine blocks or their votes in slots t-2, t-1, and t are released during the interval 8–12s into slot t (instead of the earlier 0–4s window). As a result, validators at the start of slot t+1 will observe the two attacker blocks and their attestations.
2. Byzantine voting target choice. Byzantine attestors present at slot t vote for b_{i2} (i.e., their target is b_{i2}) and delay broadcasting those votes so that they remain valid during the attack. Honest attestors at slot t still vote for b_t (i.e., their target is b_t).
3. HLMD GHOST weight calculus and canonical change. Under the HLMD GHOST rule, the attacker’s branch accumulates weight roughly equal to (1/32) \cdot (1/3) \cdot 3 \approx 1/32 (slightly less than that), which exceeds the honest branch weight near (2/3)\cdot(1/32) (slightly greater than that). Thus the canonical chain selection favors the attacker branch, causing subsequent proposers (including the proposer at slot t+1) to build on b_{i2}.
4. Epoch inactivity. In epoch e, all Byzantine attestors except those in slot t withhold their votes. Although the attacker injects approximately 1/32 \cdot 1/3 Byzantine votes targeting b_{i2} in epoch e, the total votes targeting b_{i2} still amount to roughly 31/32 \cdot 2/3 + 1/32 \cdot 1/3 < 2/3. Consequently, the checkpoint of epoch e cannot be justified; therefore, the attack both reverts the honest block b_t and renders epoch e inactive (no newly justified checkpoint).
5. Take use of a Deneb patch. This attack exploits the fact that—even if the attacker branch cannot justify cp_{e-1} at slot t, HLMD GHOST can still consider the attacker branch a candidate for the canonical chain. The attacker therefore gains a path for reorg despite the Deneb patch for [2] intended to mitigate related attacks.

### 2. Sly-sandwich attack

The sly-sandwich attack occurs when slot t is the first slot of an epoch, the proposer at slot t is honest, and proposers at slots t-1 and t+1 are Byzantine. Our sly-sandwich attack extends the sandwich reorg attack in [1] by adding *sly* timing and vote-routing strategies.

[![one-inactivaty-sly_sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/8/8/88183c4d28c038e0ee7aff1883eeee94dcd5467b_2_690x289.png)one-inactivaty-sly_sandwich.png965×405 16.2 KB](https://ethresear.ch/uploads/default/88183c4d28c038e0ee7aff1883eeee94dcd5467b)

Key elements of the sly-sandwich attack:

1. Delayed proposer block from slot t-1. The block b_i proposed at slot t-1 is withheld and released at slot t. Byzantine attestations for b_i may also be withheld and released after b_i is released, ensuring these attestations are counted as valid attack votes.
2. Canonical change with proposer boosting. After b_{i2} (the attacker-controlled block in the sandwich sequence) is released, the branch led by b_{i2} becomes the canonical chain (assisted by proposer boosting), and honest attestors in slots [t+1, t+31] will vote with b_i as target, while honest attestations from slot t are targeted at b_t.
3. Epoch inactivity. In epoch e, all Byzantine attestors except those in slot t withhold their votes. Although the attacker injects approximately 1/32 \cdot 1/3 Byzantine votes targeting b_{i} in epoch e, the total votes targeting b_{i} still amount to roughly 31/32 \cdot 2/3 + 1/32 \cdot 1/3 < 2/3. Consequently, the checkpoint of epoch e cannot be justified; therefore, the attack both reverts the honest block b_t and renders epoch e inactive.
4. Rifle-attack linkage (vote routing). We propose a linked sly strategy with the Rifle attack family: not all Byzantine votes for b_i in slots t-1 or t are broadcast to the whole network immediately. Instead, some votes are selectively delivered only to Byzantine proposers appearing later. This effectively concentrates weight on the attacker branch (slot t-1 or t Byzantine weight, approximate (1/32)\cdot(1/3), plus proposer boosting weight in slot t+1 of roughly 0.4\cdot(1/32)), which still exceeds the honest branch weight near (1/32)\cdot(2/3), enabling the attack to succeed.
5. Exploiting a Deneb patch. Similar to sly-ex-ante, sly-sandwich leverages the Deneb patch relaxation that may avoid pruning the attacker branch even when it cannot justify cp_{e-1} at slot t, leaving a vector for the attacker to become canonical.

### 3. Sly-1/3-slot-withhold attack

The sly-1/3-slot-withhold attack extends the warm-up attack described in [2]. This attack can cause one epoch to be inactive, but it cannot roll back honest blocks; therefore its immediate threat is less severe than the previous two variants. A single Byzantine proposer—if selected as the proposer of the first slot t in epoch e can execute this attack independently.

[![one-inactivaty-sly-4s-withhold.png](https://ethresear.ch/uploads/default/optimized/3X/e/3/e377fcc3036bf171480ba12897506bb3819e1c16_2_690x195.png)one-inactivaty-sly-4s-withhold.png930×263 16 KB](https://ethresear.ch/uploads/default/e377fcc3036bf171480ba12897506bb3819e1c16)

Attack description:

- A Byzantine proposer v_i proposes a block at slot t but withholds its broadcast for 4 seconds, releasing it later within the same slot. Consequently, approximately 1/32 of honest validators cast their votes targeting fb_{e-1} (the finalized-block target from the prior epoch), while other honest attestations target b_i. This split prevents epoch e from being justified.

We add the following *sly* refinements to the warm-up attack from [2]:

1. Partial vote broadcasting. During slot t Byzantine voters broadcast only about 20% of the slot’s Byzantine votes, which reduces the chance that b_i will be rolled back by honest reorg behavior.
2. Rifle-style vote routing. The remaining (non-broadcast) Byzantine votes are selectively delivered only to Byzantine proposers that appear later in epoch e, thereby increasing the attacker branch’s weight while minimizing the attackers’ exposure to slashing/punishment.

---

# Rifle attack

**Rifle attack** amplifies the impact of the three kinds of one-epoch inactivation attacks by composing them in a coordinated, multi-stage manner. By combining two-stage one-epoch inactivation attacks with Byzantine collusion primitives — specifically **one-way transfer** (unidirectional forwarding of attestations) and **delayed release** of attacker blocks — the attacker can roll back multiple honest blocks and repeatedly prevent checkpoint justification across several epochs.

## Overview

Rifle attack uses two core techniques:

- One-way transfer (unidirectional attestations): Byzantine attestors in earlier slots forward their attestations only to a designated later Byzantine proposer (rather than broadcasting them to the network). This concentrates weight on the attacker chain while keeping most honest validators unaware.
- Delayed release: The designated Byzantine proposer delays releasing their attack block until a carefully chosen slot t_{rel} in a later epoch, so that when it is finally released it has just enough weight (including forwarded Byzantine attestations) to justify a previous checkpoint on the attacker branch.

By selecting which slots/validators participate (e.g., the last Byzantine proposer in an epoch, or the penultimate Byzantine proposer), and by combining different one-epoch inactivation primitives (sly-ex-ante, sly-sandwich, sly-1/3-slot-withhold) in phase 1 and phase 2, the attacker derives a family of **Rifle attack strategies** that differ in which Byzantine votes and blocks are forwarded/delayed.

## Notation and timing constraint

- Let t denote the first slot of epoch e.
- Let t_j denote the slot of a selected (e.g., penultimate or last) Byzantine proposer in epoch e who will propose attack block b_j.
- Let t_k denote the slot in the later epoch (such as epoch e+2) of the Byzantine proposer v_k who will ultimately release a delayed block (or be the focal point of the next loop).
- Let t_{rel} denote the release slot (modulo 32 within the epoch) when the delayed attack block is broadcast.

## The concrete 6 strategies of Rifle attack

### Strategy 1

Byzantine validators at slots t-2, t-1, and t collude to launch a sly-ex-ante attack, causing the honest block b_t to be rolled back and resulting in an honest-vote loss at slot t (approximately 1/32 \times 2/3 of the total stake).

In addition, let t_j denote the slot of the penultimate Byzantine proposer in epoch e, who proposes block b_j. All Byzantine attestors in slots [t+1, t_j) of epoch e **unidirectionally transfer** their attestations to the penultimate Byzantine proposer v_j in the same epoch. After proposing the attack block b_j, v_j delays its release until t_{rel}.

Furthermore, Byzantine proposers at slots t+31 \sim t+33 collude to launch a sly-sandwich attack using a sly strategy—**only broadcasting the Byzantine votes at slot t+32**—thereby causing an honest-vote loss at slot t+32 (approximately 1/32 \times 2/3 of the total stake).

All Byzantine votes from epoch e slots [t_j, t+31], from all slots in epoch e+1 except slot t+32, and from epoch e+2 slots [t+64, t_k) are **unidirectionally transferred** to v_k, using a sly strategy that sets the source as b_{i2} and the target as b_j.

As a result, honest validators fail to justify any checkpoint in epochs e and e+1, while b_j can justify b_{i2} after t_{rel}. Therefore, the honest branch after t_j is pruned (indicated by red crosses in the figure). Attestations included in the honest branch are discarded.

[![Rifle-1-exante+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/7/1/71a992f639b8c9eb8bb83f51bdef2b5f596df8fb_2_690x183.png)Rifle-1-exante+sandwich.png2001×533 36.6 KB](https://ethresear.ch/uploads/default/71a992f639b8c9eb8bb83f51bdef2b5f596df8fb)

### Strategy 2

Byzantine validators at slots t-2, t-1, and t collude to launch a sly-ex-ante attack, causing the honest block b_t to be rolled back and resulting in an honest-vote loss at slot t (approximately 1/32 \times 2/3 of the total stake).

All Byzantine attestors in slots [t+1, t_j) of epoch e **unidirectionally transfer** their attestations to the last Byzantine proposer v_j in the same epoch. After proposing the attack block b_j, v_j delays its release until t_{rel}.

In epoch e+1, the Byzantine proposer at slot t+32 launches a sly-1/3-slot-withhold attack.

All Byzantine votes from epoch e slots [t_j, t+31], from all slots in epoch e+1, and from epoch e+2 slots [t+64, t_k) are **unidirectionally transferred** to v_k, using a sly strategy that sets the source as b_{i2} and the target as b_j.

As a result, honest validators fail to justify any checkpoint in epochs e and e+1, while b_j can justify b_{i2} after t_{rel}. Therefore, the honest branch after t_j is pruned (indicated by red crosses in the figure). Attestations included in the honest branch are discarded.

[![Rifle-2-exante+4swithhold.png](https://ethresear.ch/uploads/default/optimized/3X/8/7/875ba101401bdb0b3d36ed830305c9ee23c297be_2_690x151.png)Rifle-2-exante+4swithhold.png1832×402 41.7 KB](https://ethresear.ch/uploads/default/875ba101401bdb0b3d36ed830305c9ee23c297be)

### Strategy 3

Byzantine validators at slots t-1, t, and t+1 collude to launch a sly-sandwich attack, adopting a sly strategy — **only broadcasting the Byzantine votes at slot t-1**. This causes the honest block b_t to be rolled back and results in an honest-vote loss at slot t.

All Byzantine attestors in slots [t, t_j) of epoch e **unidirectionally transfer** their attestations to the penultimate Byzantine proposer v_j in the same epoch. After proposing the attack block b_j, v_j delays its release until t_{rel}.

Furthermore, Byzantine proposers at slots t+31 \sim t+33 collude to launch another sly-sandwich attack, using a sly strategy — **only broadcasting the Byzantine votes at slot t+32** — thereby causing an honest-vote loss at slot t+32.

All Byzantine votes from epoch e slots [t_j, t+31], from all slots in epoch e+1 except slot t+32, and from epoch e+2 slots [t+64, t_k) are **unidirectionally transferred** to v_k.

As a result, b_j can justify b_{l} after t_{rel}, and the honest branch following t_j is pruned, with all attestations included in it being discarded.

[![Pistol-3-sandwich+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/f/5/f529645c1532ed090bf9566cedc768a59ebf6b4e_2_690x163.png)Pistol-3-sandwich+sandwich.png1830×434 39 KB](https://ethresear.ch/uploads/default/f529645c1532ed090bf9566cedc768a59ebf6b4e)

### Strategy 4

Byzantine validators at slots t-1, t, and t+1 collude to launch a sly-sandwich attack, adopting a sly strategy — **only broadcasting the Byzantine votes at slot t-1**. This causes the honest block b_t to be rolled back and results in an honest-vote loss at slot t.

All Byzantine attestors in slots [t, t_j) of epoch e **unidirectionally transfer** their attestations to the penultimate Byzantine proposer v_j in the same epoch. After proposing the attack block b_j, v_j delays its release until t_{rel}.

In epoch e+1, the Byzantine proposer at slot t+32 launches a sly-1/3-slot-withhold attack, causing an honest-vote loss at that slot.

All Byzantine votes from epoch e slots [t_j, t+31], from all slots in epoch e+1, and from epoch e+2 slots [t+64, t_k) are **unidirectionally transferred** to v_k.

Therefore, b_j can justify b_{i} after t_{rel}, and the honest branch following t_j is pruned, with all attestations included in it being discarded.

[![Pistol-4-sandwich+4swithhold.png](https://ethresear.ch/uploads/default/optimized/3X/4/5/452849d76a86c9dde3b3f91739ed85ce4c538bb5_2_690x152.png)Pistol-4-sandwich+4swithhold.png1974×435 46.6 KB](https://ethresear.ch/uploads/default/452849d76a86c9dde3b3f91739ed85ce4c538bb5)

### Strategy 5

Byzantine validators at slot t launch a sly-1/3-slot-withhold attack, causing an honest-vote loss at slot t.

All Byzantine attestors in slots [t, t_j) of epoch e **unidirectionally transfer** their attestations to the penultimate Byzantine proposer v_j in the same epoch. After proposing the attack block b_j, v_j delays its release until t_{rel}.

Furthermore, Byzantine proposers at slots t+31 \sim t+33 collude to launch a sly-sandwich attack, adopting a sly strategy — **only broadcasting the Byzantine votes at slot t+32**.

All Byzantine votes from epoch e slots [t_j, t+31], from all slots in epoch e+1 except slot t+32, and from epoch e+2 slots [t+64, t_k) are **unidirectionally transferred** to v_k.

Therefore, b_j can justify b_{i} after t_{rel}, and the honest branch following t_j is pruned, with all attestations included in it being discarded.

[![Pistol-5-4swithhold+sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/9/5/956b627e3e7e64e8f10f4730652d4982b6e87090_2_690x189.png)Pistol-5-4swithhold+sandwich.png1735×477 41.7 KB](https://ethresear.ch/uploads/default/956b627e3e7e64e8f10f4730652d4982b6e87090)

### Strategy 6

Byzantine validators at slot t launch a sly-1/3-slot-withhold attack, causing an honest-vote loss at slot t.

All Byzantine attestors in slots [t, t_j) of epoch e **unidirectionally transfer** their attestations to the penultimate Byzantine proposer v_j in the same epoch. After proposing the attack block b_j, v_j delays its release until t_{rel}.

In epoch e+1, the Byzantine proposer at slot t+32 launches another sly-1/3-slot-withhold attack, causing an additional honest-vote loss at that slot.

All Byzantine votes from epoch e slots [t_j, t+31], from all slots in epoch e+1, and from epoch e+2 slots [t+64, t_k) are **unidirectionally transferred** to v_k.

The result of this attack is similar to the previous strategies — b_j can justify b_{i} after t_{rel}, and the honest branch following t_j is pruned, with all attestations included on it being discarded.

##

# Rifle attack-II

Rifle attack leverages a two-stage composition of the three one-epoch inactivation attacks, combined with collusion-based **unidirectional transfer** of attestations and **delayed-release** strategies among Byzantine validators, to realize block reorgs. From this construction we can readily conceive another class of attacks, which we call **Rifle attack-II**. The distinguishing feature of Rifle attack-II is that the delayed release of the attack block is deferred until *after* the one-epoch inactivation attack in the second phase; in other words, the collusion-driven delayed-release primitive is postponed by one inactivation-attack stage. This postponement likewise enables reorg attacks against the honest branch.

The six Rifle attack-II strategies are listed as follows:

### Strategy 7

By the same reasoning, and differing from Strategy 1 of the original Rifle attack, in this variant the Byzantine attestators in slots [t+1,\,t_j) unidirectionally transfer their attestations to the *last* Byzantine proposer v_j in epoch e+1. Validator v_j then proposes the attack block b_j and delays its release until slot t_{rel} of epoch e+2. All Byzantine votes in slots [t_j,\,t_k) are unidirectionally passed to v_k. Consequently, after t_{rel}, b_j can justify b_{l2}, causing the honest branch to be pruned.

[![1-exante-sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/4/5/453fb751d90a080423229a7ccfd2e098c2e76b5b_2_690x183.png)1-exante-sandwich.png1689×448 30.3 KB](https://ethresear.ch/uploads/default/453fb751d90a080423229a7ccfd2e098c2e76b5b)

### Strategy 8

Different from Strategy 2 of the Rifle attack, the Byzantine attestors in slots [t+1, t_j) **unidirectionally transfer** their attestations to the last Byzantine proposer v_j in epoch e+1. After proposing the attack block b_j, v_j delays its release until slot t_{rel} in epoch e+2.

All Byzantine votes from slots [t_j, t_k) are **unidirectionally transferred** to v_k. Therefore, after t_{rel}, b_j can justify b_l, resulting in the honest branch being pruned.

[![2-exante-4s.png](https://ethresear.ch/uploads/default/optimized/3X/a/9/a9c2e9483b9d3553429e52e646e1073e18de19f7_2_690x153.png)2-exante-4s.png1676×372 39.9 KB](https://ethresear.ch/uploads/default/a9c2e9483b9d3553429e52e646e1073e18de19f7)

### Strategy 9

Different from Strategy 3 of the Rifle attack, the Byzantine attestors in slots [t, t_j) **unidirectionally transfer** their attestations to the last Byzantine proposer v_j in epoch e+1. After proposing the attack block b_j, v_j delays its release until slot t_{rel} in epoch e+2.

All Byzantine votes from slots [t_j, t_k) are **unidirectionally transferred** to v_k. Therefore, after t_{rel}, b_j can justify b_l, resulting in the honest branch being pruned.

[![3-sandwich-sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/5/a/5a6c594459befce2726f1e16b9328daf67b5c267_2_690x163.png)3-sandwich-sandwich.png1678×398 39.2 KB](https://ethresear.ch/uploads/default/5a6c594459befce2726f1e16b9328daf67b5c267)

### Strategy 10

Different from Strategy 4 of the Rifle attack, the Byzantine attestors in slots [t, t_j) **unidirectionally transfer** their attestations to the last Byzantine proposer v_j in epoch e+1. After proposing the attack block b_j, v_j delays its release until slot t_{rel} in epoch e+2.

All Byzantine votes from slots [t_j, t_k) are **unidirectionally transferred** to v_k. Therefore, after t_{rel}, b_j can justify b_l, resulting in the honest branch being pruned.

[![4-sandwich-4s.png](https://ethresear.ch/uploads/default/optimized/3X/3/e/3eb8e20a036b7811e243e1b1f606f30ad5457ac3_2_690x154.png)4-sandwich-4s.png1672×374 38.8 KB](https://ethresear.ch/uploads/default/3eb8e20a036b7811e243e1b1f606f30ad5457ac3)

### Strategy 11

Different from Strategy 5 of the Rifle attack, the Byzantine attestors in slots [t, t_j) **unidirectionally transfer** their attestations to the last Byzantine proposer v_j in epoch e+1. After proposing the attack block b_j, v_j delays its release until slot t_{rel} in epoch e+2.

All Byzantine votes from slots [t_j, t_k) are **unidirectionally transferred** to v_k. Therefore, after t_{rel}, b_j can justify b_{l2}, resulting in the honest branch being pruned.

[![5-4s-sandwich.png](https://ethresear.ch/uploads/default/optimized/3X/4/a/4a5ee53b29d2356ea8e44ad0d79dd3f0b0018cc2_2_690x191.png)5-4s-sandwich.png1468×408 36.9 KB](https://ethresear.ch/uploads/default/4a5ee53b29d2356ea8e44ad0d79dd3f0b0018cc2)

### Strategy 12

Different from Strategy 6 of the Rifle attack, the Byzantine attestors in slots [t, t_j) **unidirectionally transfer** their attestations to the last Byzantine proposer v_j in epoch e+1. After proposing the attack block b_j, v_j delays its release until slot t_{rel} in epoch e+2.

All Byzantine votes from slots [t_j, t_k) are **unidirectionally transferred** to v_k. Therefore, after t_{rel}, b_j can justify b_l, resulting in the honest branch being pruned.

[![6-4s-4s.png](https://ethresear.ch/uploads/default/optimized/3X/c/f/cfb5d04d34012fd006e12d15b68a3aa74b5ab486_2_690x171.png)6-4s-4s.png1479×367 34.4 KB](https://ethresear.ch/uploads/default/cfb5d04d34012fd006e12d15b68a3aa74b5ab486)

---

## Discussion on the Delayed Release Time of the Attacker’s Block

For the 12 attack strategies of the two types of Rifle attacks mentioned above, the attacker can choose between two different attack modes, “single-shot Rifle” and “looping Rifle,” based on their attack objectives. The former seeks to cause the maximum honest incentive loss in a single attack; however, if multiple attacks are desired, a two-stage one-epoch inactivation attack must be repeated at the start of each attack. On the other hand, the latter dynamically adjusts the attack strategy to ensure that the attack cycle occurs while maximizing the attack’s intensity in each cycle. This approach aims to reduce the difficulty of the attack by leveraging accumulated advantages across multiple cycles.

### “Single-shot Rifle”

If executed only once, it is sufficient to release block b_j at the final slot of the last attack epoch to achieve maximal influence — just like epoch e+2 in the previous figures. At this point, strategy 6 of our Rifle attack is similar to Staircase Attack-II[3], and strategy 6 of our Rifle attack-II is similar to the modified staircase attack in [1]. Therefore, our “single-shot Rifle” can be viewed as an extension of the staircase attack: under the non-attack condition that the first slot t is held by an honest proposer, we add checks on the identities of the block proposers at slots t-2, t-1, and t+1 to produce 10 additional attack strategies, thereby increasing the probability that the attack occurs on time.

### “Looping Rifle”

If we want the Rifle attack and Rifle attack-II to repeat and maximize their impact, we must release b_j as late as possible, under the constraint:

1 \le t_{rel} \le \min \left( t_k,\; \frac{3t_k - 64}{2} \right)

Specifically, each epoch that updates the checkpoint’s justified state (releases the attack block) needs to satisfy the following conditions:

First, we need to confirm the selection of v_k in the epoch:

For Rifle attack:

- If the epoch is e+2, e+5, e+8, e+11, …, then the attack can be initiated without requiring the next epoch to suffer 1/32 honest vote loss. Therefore, v_k should be the last Byzantine proposer in the epoch.
- If the epoch is e+3, e+6, e+9, e+12, …, then it is necessary to ensure that the next epoch incurs 1/32 honest vote loss. Therefore, v_k should be selected as the 3rd last, 2nd last, or last Byzantine proposer in the epoch, depending on the occurrence conditions of the 3 different one-epoch inactivation attack strategies.

For Rifle attack-II:

- If the epoch is e+2, e+5, e+8, e+11, …, it is necessary to ensure that the next epoch incurs 1/32 honest vote loss. Therefore, v_k should be selected as the 3rd last, 2nd last, or last Byzantine proposer in the epoch, based on the occurrence conditions of the 3 different one-epoch inactivation attack strategies.
- If the epoch is e+4, e+7, e+10, e+13, …, then the attack can be initiated without requiring the next epoch to suffer 1/32 honest vote loss. Therefore, v_k should be selected as the last Byzantine proposer in that epoch.

Additionally, it is necessary to ensure that b_k can justify the epoch it was proposed in, and that it cannot be justified by honest votes alone. The following three conditions must be met (all time values are taken modulo 32):

1. The proportion of Byzantine votes in [0, t_k) plus the proportion of honest votes in [t_{rel}, t_k) must be \geq 2/3.
2. The proportion of honest votes in [t_{rel}, 31] must be < 2/3.
3. t_{rel} \leq t_k.

By satisfying these conditions, we obtain an approximate constraint for t_{rel}. Using this constraint for the delayed release of b_k, we can ensure that the attack cycle occurs without needing to repeat the two-stage one-epoch inactivation attack.

For example, for Rifle attack:

- If t_k in epoch e+2 = 31, then t_{rel} in epoch e+2 can be 14, meaning that b_j proposed in epoch e is released at slot 14 in epoch e+2, and the justified checkpoint is updated to cp_e.
- If t_k in epoch e+3 = 30, then t_{rel} in epoch e+3 can be 13, meaning that b_k proposed in epoch e+2 is released at slot 13 in epoch e+3, and the justified checkpoint is updated to cp_{e+2}.
- Based on the actual situation, perform a one-epoch inactivation attack to epoch e+4.
- If t_k in epoch e+5 = 29, then t_{rel} in epoch e+5 can be 11, meaning that b_k proposed in epoch e+3 is released at slot 11 in epoch e+5, and the justified checkpoint is updated to cp_{e+3}.
- If t_k in epoch e+6 = 30, then t_{rel} in epoch e+5 can be 13, meaning that b_k proposed in epoch e+5 is released at slot 13 in epoch e+6, and the justified checkpoint is updated to cp_{e+5}.
- Continue executing the looping Rifle attack according to this pattern…

For Rifle attack-II:

- If t_k in epoch e+2 = 31, then t_{rel} in epoch e+2 can be 14, meaning that b_j proposed in epoch e+1 is released at slot 14 in epoch e+2, and the justified checkpoint is updated to cp_{e+1}.
- Based on the actual situation, perform a one-epoch inactivation attack in epoch e+3.
- If t_k in epoch e+4 = 30, then t_{rel} in epoch e+4 can be 13, meaning that b_k proposed in epoch e+2 is released at slot 13 in epoch e+4, and the justified checkpoint is updated to cp_{e+2}.
- If t_k in epoch e+5 = 29, then t_{rel} in epoch e+5 can be 11, meaning that b_k proposed in epoch e+4 is released at slot 11 in epoch e+5, and the justified checkpoint is updated to cp_{e+4}.
- Based on the actual situation, perform a one-epoch inactivation attack in epoch e+6.
- If t_k in epoch e+7 = 30, then t_{rel} in epoch e+7 can be 13, meaning that b_k proposed in epoch e+5 is released at slot 13 in epoch e+7, and the justified checkpoint is updated to cp_{e+5}.
- Continue executing the looping Rifle attack-II according to this pattern…

---

# Scalable Delay Strategy

In fact, the 12 Rifle attack strategies we introduced above are merely the basic “take advantage of the situation” Rifle attacks. In real attack scenarios, whether in the “single-shot Rifle” or “looping Rifle,” within each layer of the loop, we can further leverage the three kinds of one-epoch inactivation attacks described above to create more epochs of inactivity, thus increasing the attack intensity. For example, for the 12 Rifle attack strategies mentioned above, if slot t+64 is a Byzantine proposer, or if slot t+64 is an honest proposer and both slots t+63 and t+62 are Byzantine proposers, or if slot t+64 is an honest proposer and both slots t+63 and t+65 are Byzantine proposers, a third-phase one-epoch inactivation attack can be triggered, resulting in inactivity in epoch e+2. This would allow the attack block b_j to be released at t_{rel} in epoch e+3, thereby causing an additional rollback of 1 epoch’s honest blocks and attestations.

Similarly, for the “looping Rifle” mode of the Rifle attack, if epoch e+6 meets the conditions for a one-epoch inactivation attack, the block b_k proposed by epoch e+5 can be delayed and released in epoch e+7 rather than epoch e+6, justifying cp_{e+5}. Similarly, for the “looping Rifle” mode of Rifle attack-II, if epoch e+8 satisfies the conditions for a **one-epoch inactivation attack**, the block b_k proposed by epoch e+7 can be delayed and released in epoch e+9 rather than epoch e+8, justifying cp_{e+7}.

Furthermore, we can extend the range of epochs covered by a single delay: if slot t+96 is a Byzantine proposer, or if slot t+96 is an honest proposer and both slots t+95 and t+94 are Byzantine proposers, or if slot t+96 is an honest proposer and both slots t+95 and t+97 are Byzantine proposers, block b_j can be delayed and released at t_{rel} in epoch e+4… Readers can extend this approach to generate infinite variations of more powerful Pistol attack strategies.

# References

We would like to especially thank all the authors for their efforts and contributions :

[[1] Zhang, Mingfei, et al. “Available Attestation: Towards a Reorg-Resilient Solution for Ethereum Proof-of-Stake.” Cryptology ePrint Archive (2025).](https://www.usenix.org/system/files/conference/usenixsecurity25/sec25cycle1-prepub-1204-zhang-mingfei.pdf)

[[2] Zhang, Mingfei, Rujia Li, and Sisi Duan. “Max attestation matters: Making honest parties lose their incentives in ethereum {PoS}.” 33rd USENIX Security Symposium (USENIX Security 24). 2024.](https://www.usenix.org/system/files/usenixsecurity24-zhang-mingfei.pdf)

[[3] Zhang, M. (2025, April 7). Staircase Attack-II in Ethereum PoS . Ethereum Research. https://ethresear.ch/t/staircase-attack-ii-in-ethereum-pos/22099](https://ethresear.ch/t/staircase-attack-ii-in-ethereum-pos/22099)

Figure 2 of [2] provides a formalized description of the Ethereum PoS protocol from the perspective of a validator, while Figure 3 of [2] explains the meanings of the legends used throughout that paper’s figures. For clarity of exposition, we adopt the formal description style of Figure 2 in [2] to present the Rifle attack, and we use the legend and visualization conventions of Figure 3 in [2] for our diagrams. Readers are encouraged to consult [1~3] directly for further details. Thanks again.
