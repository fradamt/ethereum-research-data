---
source: ethresearch
topic_id: 23651
title: "TrustMesh: Consensus as Emergence, Security from Behavior"
author: YanAnghelp
date: "2025-12-14"
category: Meta-innovation
tags: [consensus]
url: https://ethresear.ch/t/trustmesh-consensus-as-emergence-security-from-behavior/23651
views: 118
likes: 0
posts_count: 5
---

# TrustMesh: Consensus as Emergence, Security from Behavior

## Overview

TrustMesh is a consensus architecture based on emergent dynamics. Its goal is to allow the entire network to eventually converge on a single proposal within each Round. Any node may propose, and through local interactions and dynamical convergence, the network selects a unique proposal. Throughout the process, no node needs knowledge of any global view; blocks do not reference one another, and nodes react purely based on local information.

The current Proof of Concept (PoC) demonstrates that even under adversarial conditions with randomly assigned reputations, the system still exhibits clear attractors and reliably converges. The PoC implementation is available here: [TrustMesh](https://github.com/BinGo-Lab-Team/TrustMesh)

## Core Concepts

### Round

A *Round* is the basic unit of a complete consensus process in TrustMesh. TrustMesh intentionally does **not** prescribe how rounds must be advanced. (In the PoC, rounds are driven by fixed time windows for observability.)

If strong consistency is not required, rounds may execute in parallel. Each round ultimately produces **valid history** (i.e., consensus results that are never pruned or discarded). In this semantic model, there are no forks that require resolution or pruning.

### Reputation

Reputation is the core concept of TrustMesh, and the security of the system directly depends on it. Reputation is stored in each node’s **Locally Observed Reputation Table (LORT)** and must be bound to **verifiable identities** (e.g., public keys). Although the term “reputation” is used, it does not represent subjective prestige. To prevent reputation from degenerating into global authority, TrustMesh enforces the following design constraints:

1. Local Privacy
A node’s reputation table must not be shared, broadcast, copied, or exported to any external party.
2. Observation-Only Derivation
All reputation values must be derived solely from behaviors directly observed by the node itself, rather than imported from third-party recommendations or external reputation feeds.
3. Purpose-Driven Rule Construction
Reputation update rules must be defined according to the concrete purpose and service model of the network.

## Consensus Process

### 1. Proposal Generation

At the beginning of each round, nodes construct and broadcast proposals. Nodes do not score their own proposals, as self-scoring provides no meaningful information and introduces attack surfaces. However, the system requires an initial perturbation; otherwise, all proposal scores would remain zero.

Receiving nodes may therefore apply a configurable *base score*, conceptually equivalent to assuming that the proposer assigns an initial score to its own proposal. (In the PoC, this is simplified by letting proposers self-score and self-sign with an immutable value; this can be losslessly mapped back to a base-score mechanism.)

Every node may produce a valid proposal in every round. TrustMesh fully removes the distinction between leaders and voters: all nodes possess both the right to propose and the right to score proposals.

### 2. Proposal Reception & Scoring

Upon receiving a proposal, a node examines its signature set and applies **reputation-weight dilution** to each scoring signature based on its local reputation table (unknown nodes have zero weight). The sum of all diluted scores constitutes the node’s *local score* for that proposal at that moment.

This scoring process relies exclusively on local information and does not require any global view.

In the current PoC, linear weighting is used. Consider the following local reputation table:

| Name | Reputation | Score |
| --- | --- | --- |
| NodeA | 2677 | 500 |
| NodeB | 7906 | 1000 |
| NodeC | 3845 | 490 |

The total reputation is:

```auto
2677 + 7906 + 3845 = 14428
```

The resulting weights and weighted contributions are:

| Name | Weight | Weighted Score |
| --- | --- | --- |
| NodeA | 2677 / 14428 ≈ 0.19 | 500 × 0.19 = 95 |
| NodeB | 7906 / 14428 ≈ 0.55 | 1000 × 0.55 = 550 |
| NodeC | 3845 / 14428 ≈ 0.27 | 490 × 0.27 = 132.3 |

The resulting local score is:

```auto
95 + 550 + 132.3 = 777.3
```

The node then adds its own score signature to the proposal and broadcasts it. Other nodes repeat the same process independently.

In the PoC scoring model, local proposal scores are theoretically **monotonic non-decreasing**. Missing signatures contribute zero. Scores must be non-negative. For the same proposal, a node only accepts score updates that are greater than or equal to its previous score; lower scores are treated as outdated and ignored. Under these rules, signature set growth and updates can only increase or preserve local scores.

### 3. Final Synchronization & Termination

Once the network is already highly converged and only minor perspective divergence remains (in the PoC, this is determined by a fixed time window), the proposal with the highest local score is selected as the *Winner* and stored. This is the simplest termination behavior.

Some nodes may still select a different Winner due to local perspective variance. A final synchronization mechanism can eliminate this residual divergence. To better observe natural convergence, this mechanism is not implemented in the PoC and is provided for theoretical reference only.

In final synchronization, each node broadcasts exactly one local Winner and ceases scoring. Nodes collect Winner announcements from peers and rank them using local weights, excluding their own previously selected Winner from the ranking. If the top-ranked Winner changes, an updated announcement is broadcast. Once the ranking stabilizes, the top-ranked proposal is finalized and stored.

## Experimental Results

The following figure shows PoC results under random reputation, 30 nodes, 60-second rounds, and an average of 8 neighbors, across 31 rounds. Each node submits one proposal per round, and reputations are re-randomized at the start of every round.

![performance graph](https://ethresear.ch/uploads/default/original/3X/4/0/40d83e73a23593847d4e71999f0456736a9e7457.svg)

1. On average, 26.61 out of 30 nodes (88.7%) converged on the same proposal.
This was achieved using only local information, without synchronized voting or global chain structures.
2. In all rounds, the Winner’s supporters outnumbered all other proposals combined.
This indicates strong amplification of advantage and majority dominance.
3. Even when multiple proposals coexisted, the final Winner maintained overwhelming dominance.
Minority clusters form only local stable points and do not disrupt global convergence.
4. Earlier experiments with 21 nodes showed lower convergence probabilities under identical parameters.
This suggests that TrustMesh may exhibit increasing stability as network size grows.

## FAQ

### Q: Is TrustMesh similar to RAG-style consensus systems?

**A: No. TrustMesh differs fundamentally from RAG, IOTA, and similar systems.**

RAG and most DAG-based systems aim for approximate correctness and probabilistic optimality. They allow many parallel candidate branches, but ultimately must resolve and discard a significant portion of them, incurring real network cost.

In TrustMesh, **each Round is a complete and independently valid consensus process**. Parallel execution does not create prunable forks; every round produces usable consensus results.

### Q: Can attackers accumulate reputation via Sybil identities and later “burn” it to attack?

**A: TrustMesh mitigates this from two directions.**

**First, reputation growth is strongly bound to real effort.**

Reputation is purely local; nodes cannot observe or control any global reputation value. To become highly reputable across many nodes, an actor must engage in long-term, sustained, and genuine interactions with many independent peers. Sybil identities cannot rapidly inflate reputation via self-assertion or internal loops. Reputation decay mechanisms (e.g., time-based decay for inactivity) may further limit long-term Sybil farming.

**Second, reputation influence is intentionally weakened rather than amplified.**

Reputation participates only as normalized weight. As a node’s local reputation table grows, the marginal influence of any single high-reputation node is increasingly diluted. Unlike stake, reputation grants no direct leadership or decision authority; it merely accelerates convergence and suppresses Sybil noise.

**Thus, reputation in TrustMesh is difficult to accumulate and impossible to convert into one-shot attack power.**

### Q: How does TrustMesh handle double-spending?

**A: This work focuses on non-consistent consensus systems rather than monetary ledgers.**

In scenarios such as notarization, execution result selection, or parameter agreement, duplicate inclusion across rounds is harmless and deduplicable, so double-spending does not arise.

In principle, TrustMesh could enforce strong consistency via additional validity checks, but this would require global ordering or arbitration, destroying parallelism and is therefore out of scope.

For monetary systems, a single linear history remains an efficient and reasonable design. Any attempt to parallelize transaction state ultimately reintroduces expensive global consensus via arbitration or trusted timestamps. Strong consistency is a scarce and costly resource and should be minimized and decoupled from non-consistent execution layers.

### Q: Can TrustMesh rapidly punish malicious behavior?

**A: Yes—more flexibly than stake-based systems.**

Because reputation is not bound to money, its reduction rules can be far more sensitive.

For cryptographically provable misbehavior (e.g., double proposals within the same round), nodes may broadcast evidence. Peers independently verify the evidence and locally reduce the offender’s reputation. No global slashing, synchronized punishment, or system rollback is required, preserving parallelism and forward progress.

## Call for Participation

If you believe TrustMesh is worth further investigation, please help improve it.

This includes critical feedback, theoretical challenges, experimental reproduction, code contributions, or simply sharing the idea with others.

TrustMesh is still exploratory, and its development depends on rigorous discussion and collective effort.

E-mail: [yangzhixun-@outlook.com](mailto:yangzhixun-@outlook.com)

Github repo: [GitHub - BinGo-Lab-Team/TrustMesh: TrustMesh: Consensus as Emergence, Security from Behavior](https://github.com/BinGo-Lab-Team/TrustMesh)

## Replies

**MicahZoltu** (2025-12-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> ### Q: Can attackers accumulate reputation via Sybil identities and later “burn” it to attack?
>
>
>
> A: TrustMesh mitigates this from two directions.
>
>
> First, reputation growth is strongly bound to real effort.
> Reputation is purely local; nodes cannot observe or control any global reputation value. To become highly reputable across many nodes, an actor must engage in long-term, sustained, and genuine interactions with many independent peers. Sybil identities cannot rapidly inflate reputation via self-assertion or internal loops. Reputation decay mechanisms (e.g., time-based decay for inactivity) may further limit long-term Sybil farming.
>
>
> Second, reputation influence is intentionally weakened rather than amplified.
> Reputation participates only as normalized weight. As a node’s local reputation table grows, the marginal influence of any single high-reputation node is increasingly diluted. Unlike stake, reputation grants no direct leadership or decision authority; it merely accelerates convergence and suppresses Sybil noise.
>
>
> Thus, reputation in TrustMesh is difficult to accumulate and impossible to convert into one-shot attack power.

This is the right question, but the answer doesn’t appear to correctly address it.  There doesn’t seem to be anything stopping an attacker from creating a large number of honest behaving nodes, farming reputation for an extended period, and then leveraging that to do bad things.  Either you need the network to not be able to do bad things, or you need a way to punish an attacker after the fact if they do a bad thing.

The second part of your answer seems to hint that there is nothing an attacker can actually do other than grief, but if that is the case it should be explicitly stated.  Can you show that if an attacker gains super-majority of reputation they cannot do anything particularly bad beyond just delaying consensus?  How much can they delay?  If an attacker can fully eclipses a node, what bad thing can they do?  I assume censor at least, but what else?

---

**YanAnghelp** (2025-12-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The second part of your answer seems to hint that there is nothing an attacker can actually do other than grief, but if that is the case it should be explicitly stated. Can you show that if an attacker gains super-majority of reputation they cannot do anything particularly bad beyond just delaying consensus? How much can they delay? If an attacker can fully eclipses a node, what bad thing can they do? I assume censor at least, but what else?

**Regarding the first part:** this type of attack exists in any open network. It cannot be fully eliminated; the only realistic objective is to raise its cost. In TrustMesh, the cost of reputation accumulation is intentionally high. Because reputation is purely local and observation-derived, an attacker must engage in long-term, sustained, and genuinely useful interactions with many independent nodes in order to become a high-reputation node in their local views.

Punishment is also intentionally local. Since reputation exists only in each node’s local reputation table, penalties are decided independently by each node. An attacker can only directly affect nodes that actually recognize and interact with them. Once a node observes malicious behavior, it can locally reduce the attacker’s reputation without requiring global coordination or slashing.

**Regarding the second part:** if an attacker controls the high-reputation nodes across the entire network, then they can influence proposal selection or deliberately obstruct convergence, causing a round to converge on attacker-preferred proposals or fail to converge at all. TrustMesh does not claim safety under such conditions, just as no consensus system remains secure under adversarial super-majority control.

If the attacker controls only locally concentrated high-reputation nodes, the impact remains local. They may eclipse or mislead subsets of nodes, causing those nodes to diverge from the main network and temporarily fall out of sync. For this reason, TrustMesh fundamentally relies on network connectivity: broader and more diverse connectivity limits the extent to which local reputation dominance can propagate into global influence.

---

**MicahZoltu** (2025-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> the cost of reputation accumulation is intentionally high

Do you have calculations that support the claim that the cost to raise trust is *meaningfully* high?  With things like Ethereum, you have a calculable amount of stake that can be burnt if someone tries to attack the network, and while you are correct that not all attacks can be prevented, at least a lower bound on how much those attacks will cost can be asserted.

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> they can influence proposal selection or deliberately obstruct convergence, causing a round to converge on attacker-preferred proposals or fail to converge at all

Do you have some worst case examples of how such things would affect an end-user or how an attacker could profit?  Is this just a transient loss in finality and censorship for the duration of the attack?

Do all attacks require *burning* reputation, or are there a class of attacks (often there are in reputation systems) where an attacker can accumulate a bunch of reputation, then do bad things, but avoid losing that accumulated reputation due to the attack?  (e.g., attack isn’t noticeable or attributable).

---

**YanAnghelp** (2025-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Do you have calculations that support the claim that the cost to raise trust is meaningfully high? With things like Ethereum, you have a calculable amount of stake that can be burnt if someone tries to attack the network, and while you are correct that not all attacks can be prevented, at least a lower bound on how much those attacks will cost can be asserted.

In a local-consensus system like TrustMesh, the cost of an attack is inherently difficult to quantify precisely, because each node maintains its own perspective and trust evaluation. There is no single global metric that can be universally priced or slashed.

A useful analogy is BitTorrent’s tit-for-tat mechanism: reputation is derived from direct, observed interactions between peers, rather than from an externally verifiable stake. Because trust is based on firsthand behavior, it is not something that can be cheaply fabricated or globally asserted.

More concrete cost estimates therefore depend on the specific reputation rules implemented by each node. Those rules determine how quickly trust can be accumulated or lost, but that is an engineering-level design choice rather than a fixed protocol constant.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Do you have some worst case examples of how such things would affect an end-user or how an attacker could profit? Is this just a transient loss in finality and censorship for the duration of the attack?

Regarding the first question, the worst-case scenario would be one in which an attacker successfully captures the view of all nodes.   In that case, the winning proposals would be entirely controlled by the attacker, representing a total breakdown of honest influence.

A more realistic and weaker adversarial scenario is one where the attacker becomes a high-reputation node in the views of a majority of participants.   Under such conditions, the attacker could bias the selection of winning proposals to extract block rewards, or deliberately slow down convergence by disrupting the scoring dynamics, thereby delaying finality.

From an end-user perspective, the most visible effect in such scenarios would be significantly slower finality.  Additionally, if the round progression mechanism is poorly designed, different nodes may temporarily select different winning proposals, leading to inconsistent local outcomes across the network.

However, even in this scenario, it remains difficult for the attacker to completely destroy finality.   As long as honest nodes remain mutually connected, proposal scores among honest participants continue to increase monotonically, and the gap between competing proposals continues to widen over time.   This makes permanent stagnation hard to sustain.

Once the attack subsides, the network is expected to gradually self-heal: honest connectivity reasserts itself, local views realign, and a healthy topology eventually re-emerges without requiring explicit coordination or intervention.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Do all attacks require burning reputation, or are there a class of attacks (often there are in reputation systems) where an attacker can accumulate a bunch of reputation, then do bad things, but avoid losing that accumulated reputation due to the attack? (e.g., attack isn’t noticeable or attributable).

Whether all attacks necessarily burn reputation is a very important question.  My honest answer is: it is uncertain.  In TrustMesh, reputation rules are explicitly designed to follow the objectives of the network rather than being fixed protocol constants, which means that this class of vulnerability cannot be categorically ruled out.

In practical engineering terms, two aspects need to be distinguished.  First, low-visibility attacks are likely to exist and are fundamentally unavoidable.  For example, an attacker may subtly bias consensus by assigning slightly higher scores to certain proposals.  In a system like TrustMesh, which is intentionally noisy and decentralized, it is impossible to precisely detect such marginal bias.  Instead, the system relies on the scale of reputation tables and diversity of local views to dilute these effects until they become negligible.

Second, TrustMesh was designed from the outset with the assumption that not all misbehavior can be cleanly attributed to a specific node.  As a result, an implicit design principle is that all meaningful information must be verifiably attributable to an identifiable origin.  Information whose origin cannot be verified is treated as spam, and information originating from unknown or untrusted parties may be selectively ignored.

This design choice does not eliminate all forms of abuse—denial-of-service attacks, in particular, remain difficult to prevent—but it limits the ability of attackers to accumulate influence through unattributable or unaccountable actions.

