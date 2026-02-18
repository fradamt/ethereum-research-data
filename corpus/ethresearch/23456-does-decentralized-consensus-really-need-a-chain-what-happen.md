---
source: ethresearch
topic_id: 23456
title: Does decentralized consensus really need a chain? What happens if emergence replaces history?
author: YanAnghelp
date: "2025-11-17"
category: Consensus
tags: [consensus]
url: https://ethresear.ch/t/does-decentralized-consensus-really-need-a-chain-what-happens-if-emergence-replaces-history/23456
views: 348
likes: 20
posts_count: 17
---

# Does decentralized consensus really need a chain? What happens if emergence replaces history?

For about fifteen years, nearly every decentralized consensus protocol—whether PoW, PoS, or DAG variants—has implicitly relied on the same core assumption:

> That achieving consensus requires all nodes to share a single, global, ordered history of blocks.

This linear history makes verification simple, but it also introduces structural constraints: global synchronization, replay overhead, finality coupling, and increasing centralization pressure as the network grows.

At some point I started asking a very simple but uncomfortable question:

> Is this assumption a mathematical necessity… or just an engineering tradition?
> Does decentralized consensus really need a chain?

---

## ✦ A hypothetical alternative

Suppose we abandon the requirement for shared historical ordering, and instead allow:

- Each proposal (block/message) to exist independently
- No parent references, no global ordering
- Nodes propagate proposals according to local trust
- Consensus emerges from network topology, not chain structure

If this were possible, we would need to ask:

- Would such a system still converge?
- Could finality be emergent rather than sequential?
- Would full nodes still need to store history at all?
- Would high-latency environments (e.g. interplanetary networks) remain viable?
- If consensus weight derives from behavior rather than capital, would we see less centralization?

---

## ✦ A working hypothesis: the L.O.P. Principles

To explore this direction, I defined a minimal set of constraints for a purely local trust model, called the **L.O.P. Principles** (Locally / Observed / Principles):

> 1. Trust is strictly local and must never be globally shared
> 2. Trust must be derived only from directly observed behavior
> 3. Trust rules must be defined according to the network’s purpose

These rules look trivial at first—but their consequences are not.

> They prohibit global trust synchronization
> They eliminate the idea of a “single reputation state”
> And they force every node to determine trust boundaries independently

In such a world, consensus is no longer a product of shared history.

It becomes a property of **network topology + local trust + emergent convergence**.

---

## ✦ Unresolved questions (and why I am posting here)

To be absolutely clear: I **do not yet know** whether this direction is viable.

I would specifically love to hear criticism, references, or proof-based counterarguments to questions like:

- Has this direction been explored—and disproven—before?
- Is there a theoretical impossibility result that makes “historyless consensus” unattainable?
- Could local trust models lead to permanent partitioning?
- Can topology collapse be formalized as finality?
- Are there applicable results from CRDTs, epidemic consensus, or multi-agent systems?
- Does this violate any classical impossibility results (FLP, CAP, etc)?
- Is there any known way to prove (or disprove) convergence in such a model?

I am explicitly hoping someone will tell me why this cannot work, if that is indeed the case.

---

## ✦ What this is not

- Not a token launch
- Not fundraising
- Not a product
- Not a whitepaper announcement
- Not an “X is better than blockchain” argument

Right now this is simply a conceptual question, one that I think deserves public scrutiny:

> If a chain is not strictly necessary, then perhaps we have not yet explored the full space of consensus designs.

---

## ✦ Repository (empty for now, for future work)

I have created an empty GitHub repository **only as a placeholder** for future drafts, experiments, or specifications:

![:backhand_index_pointing_right:](https://ethresear.ch/images/emoji/facebook_messenger/backhand_index_pointing_right.png?v=14) [GitHub - BinGo-Lab-Team/TrustMesh: Consensus without chains — an orderless, history-free, reputation-driven framework with infinite parallelism.](https://github.com/BinGo-Lab-Team/TrustMesh)

There is currently **no documentation, no code, and no implementation**.

If anyone finds this direction interesting, feel free to Watch the repository, but please don’t expect anything yet.

---

## ✦ Open-ended closing questions

If consensus can emerge without shared history:

- Do we need to redefine what “consensus” means?
- Is blockchain just one special case of a larger design space?
- Could Web3 eventually shift from ordered history → stable trust states?

**If the answer is “yes”, then perhaps we haven’t reached the boundary of decentralized consensus at all.**

## Replies

**MicahZoltu** (2025-11-17):

IOTA has been trying to solve this problem for something like 10 years, and while they always make big claims to having solved it despite al of the “experts” telling them that they haven’t, so far they have yet to turn off their centralized piece that is still required to keep it running.

The core of the problem is that there is no true “local”.  Alice can transact in Brazil at the exact same time as transacting in China and if those two transactions are mutually exclusive (e.g., they both spend the same money) then you need some mechanism for deciding which of them comes “first” (and thus gets included) and which comes “second”.

From the point of view of someone in Brazil, the Brazilian transaction arrived first.  From the point of view of someone in China, the Chinese transaction arrived first.

---

**boris-kolar** (2025-11-17):

Strictly speaking, to prevent double spending, it’s not necessary to decide which transaction came first. We could reject both transactions if they appear within a short time frame.

---

**MicahZoltu** (2025-11-17):

That is an interesting idea I hadn’t considered, I will need to think on it more.

You still would need to wait for “finality” though, where you wait to see if there is a conflicting signature in the prescribed time.  You also would need to deal with edge cases where the second signature arrives right on the border of what is allowed, so half of the world see it as double-spend, the other half see it as properly spaced sequential spend.

---

**thegaram33** (2025-11-17):

Participants in any high-stakes system (e.g. payment network) must agree on the following:

1. What are the transactions that happened?
2. Given a set of conflicting transactions, which one (if any) do we accept as valid?

Sounds like you want to relax (1). But isn’t (1) a prerequisite of (2)? It is hard to imagine that a system without some kind of global consensus could solve both.

That said, having a global linear ledger (i.e. a total ordering of all transactions) is not necessarily required; we only need to order conflicting transactions, not independent ones.

---

**YanAnghelp** (2025-11-17):

You’re absolutely right that some form of finality is still required. However, the key difference in TrustMesh is that finality doesn’t depend on probabilistic confirmation or multi-round voting. Instead, it emerges naturally from the collapse of the trust topology. In practice, the finality window depends almost entirely on the number of propagation hops—not on the total network size or validator count.

Given modern network conditions, low latency, and nodes proactively maintaining peer connections, the variance introduced by hop-based delay is negligible. This means that what is normally considered a disadvantage (waiting for finality) actually becomes an advantage: the network can operate with a fully fixed block interval without needing synchronized rounds or probabilistic safety.

As for the consensus process itself, the design works like this: in each round, every node may publish a proposal containing a signature tree. Other nodes score proposals based on the signatures they recognize, using their local reputation tables, then append their own signature and continue propagation. After a few iterations, one proposal becomes the dominant attractor in the topology. It consistently ranks first in all healthy nodes, which effectively establishes consensus.

One more thing I want to highlight: using a monetary blockchain as the mental model for this kind of network is actually misleading. Bitcoin and similar systems assume that all state must be linearly chained forever, but many real-world applications don’t require continuous history at all. Once you stop treating continuity as a hard requirement, you’ll find that a very different—and often much more efficient—design space becomes possible.

---

**YanAnghelp** (2025-11-17):

Bitcoin already demonstrates that you don’t need every node to see every transaction in order to resolve conflicts. No node has a complete mempool, yet double-spends are still handled purely through propagation and competition.

Fundamentally, a system only needs to satisfy two conditions:

1. Each proposal must be internally consistent and not conflict with confirmed history
2. Eventually, only one proposal will be accepted network-wide

This does *not* require all nodes to have a global view of all transactions, and it doesn’t require a globally linear history either. As long as the propagation and resolution process leads to a single dominant proposal, consensus can still be achieved—even outside of monetary networks.

---

**MicahZoltu** (2025-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> Other nodes score proposals based on the signatures they recognize, using their local reputation tables

This is the very hard problem that you need to solve.  Imagine some actor wants to build reputation over time.  They can sybil attack and pretend to be 1000, or 1,000,000 different nodes and they can do whatever is necessary to pump their reputation.  Once they have pumped their reputation sufficiently high, they can then “burn” that reputation to double spend.

The traditional way to address the sybil problem and profitable attack problem is via some sort of staking mechanism so if a double spend is detected the attacker can be slashed and we can at least ensure they lose a lot of money.  However, once you build such a system you may find that you are back to a linear blockchain as that is much easier to implement slashing on than a tree.

---

**YanAnghelp** (2025-11-18):

Thanks — this is the right question, and I agree it’s the core challenge.

The key difference is that in TrustMesh, reputation is not a global shared variable.

Under the L.O.P. axioms, reputation is:

- Local
- Non-exportable
- Observation-based
- Decaying

That means an attacker cannot “pump” global reputation — they must independently earn trust from each observer. Even if they control 1,000,000 identities, they do not automatically accumulate 1,000,000× reputation, because every node evaluates them independently.

Sybil behavior simply results in wasted effort, not global influence.

TrustMesh does not require slashing because it does not store “reputation” as a globally agreed-upon value. There is nothing to slash — only local trust to revoke.

In other words: PoS protects a shared ledger. TrustMesh avoids the need for a shared ledger in the first place.

---

**YanAnghelp** (2025-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> Thanks — this is the right question, and I agree it’s the core challenge.
>
>
> The key difference is that in TrustMesh, reputation is not a global shared variable.
> Under the L.O.P. axioms, reputation is:
>
>
> Local
> Non-exportable
> Observation-based
> Decaying
>
>
> That means an attacker cannot “pump” global reputation — they must independently earn trust from each observer. Even if they control 1,000,000 identities, they do not automatically accumulate 1,000,000× reputation, because every node evaluates them independently.
>
>
> Sybil behavior simply results in wasted effort, not global influence.
>
>
> TrustMesh does not require slashing because it does not store “reputation” as a globally agreed-upon value. There is nothing to slash — only local trust to revoke.
>
>
> In other words: PoS protects a shared ledger. TrustMesh avoids the need for a shared ledger in the first place.

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> 1. Trust is strictly local and must never be globally shared
> 2. Trust must be derived only from directly observed behavior
> 3. Trust rules must be defined according to the network’s purpose

The third axiom of L.O.P. inherently requires that any attack must be accompanied by sustained positive contributions to the network. Economically, this is far more secure than Proof-of-Stake, because it prevents adversaries from temporarily acquiring influence through mechanisms such as loans. Furthermore, once malicious behavior is detected, any node that observes or receives cryptographic evidence can immediately reduce the offender’s reputation and reject any future requests from that identity.

In addition, we can impose an upper bound on each node’s reputation and allow it to decay over time, completely eliminating the possibility of “whale” nodes.

---

**thegaram33** (2025-11-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> Bitcoin already demonstrates that you don’t need every node to see every transaction in order to resolve conflicts. No node has a complete mempool, yet double-spends are still handled purely through propagation and competition.

Correct me if I’m wrong, but Bitcoin prevents double-spends via reaching consensus on the linear ledger of transactions. Nodes can apply different strategies to exclude double-spending transactions from the mempool, but it’s all a heuristic with no strong guarantees.

---

**YanAnghelp** (2025-11-18):

Just to clarify — TrustMesh doesn’t forbid chains. Chains are still necessary for monetary systems because balance history must remain traceable. What TrustMesh does is make chains optional instead of mandatory.

The only consensus guarantee is that each round produces one accepted proposal. Whether those proposals reference a parent (i.e. form a chain) depends on the application.

Using your example: if Alice has 10 tokens and submits two valid spends at once, a proposal that includes both is locally invalid and will be rejected immediately. If the two spends land in separate proposals, both are temporarily valid—just like forks in Bitcoin. Only one proposal will eventually win, and anything building on the losing one becomes invalid.

So it’s the same model as Bitcoin: conflicts are allowed to exist briefly, but only one path becomes canonical. The difference is simply that TrustMesh resolves this via reputation/emergence instead of PoW/PoS.

Chains are still possible when needed—they’re just not the foundation of consensus anymore.

---

**AhmadNajari** (2026-01-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/boris-kolar/48/8610_2.png) boris-kolar:

> Strictly speaking, to prevent double spending, it’s not necessary to decide which transaction came first. We could reject both transactions if they appear within a short time frame.

**This is a sharp and important point that cuts to the core of the problem. You’re right: strict global ordering is a *solution* to double-spending, but not the only possible one. The ‘reject both’ approach essentially trades a strong consistency guarantee for eventual consistency with a strong safety rule.**

**However, in a trustless, Byzantine environment, this creates a new vulnerability: it opens the door to a systematic Denial-of-Service (DoS) attack. A malicious actor could flood the network with conflicting transactions, forcing the rejection of legitimate ones. The global chain, for all its overhead, provides a deterministic, attack-resistant conflict resolution rule.**

**So the deeper question for a history-less, emergent consensus model becomes: what replaces the chain as that *unforgeable, common reference point* for conflict resolution? Can local trust models and observed behavior converge on a stable rule that is both safe and resistant to such targeted attacks? This seems like a critical hurdle.**

---

**YanAnghelp** (2026-01-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/ahmadnajari/48/22120_2.png) AhmadNajari:

> This is a sharp and important point that cuts to the core of the problem. You’re right: strict global ordering is a solution to double-spending, but not the only possible one. The ‘reject both’ approach essentially trades a strong consistency guarantee for eventual consistency with a strong safety rule.

I think that in parallel networks, such conflicts cannot be resolved and should not be.  If it is to be resolved, additional global arbitration must be introduced

If we enforce single-threading, that is, each block must import the previous block, then this problem can be easily solved.  It is only necessary to ensure that a single block is legally valid internally and historically

![](https://ethresear.ch/user_avatar/ethresear.ch/ahmadnajari/48/22120_2.png) AhmadNajari:

> So the deeper question for a history-less, emergent consensus model becomes: what replaces the chain as that unforgeable, common reference point for conflict resolution? Can local trust models and observed behavior converge on a stable rule that is both safe and resistant to such targeted attacks? This seems like a critical hurdle.

Regarding this issue, you can refer to this PoC: [TrustMesh: Consensus as Emergence, Security from Behavior - Meta-innovation - Ethereum Research](https://ethresear.ch/t/trustmesh-consensus-as-emergence-security-from-behavior/23651/5), which reveals that such a structure is entirely possible. Perhaps we can ensure that each block does not need to reference other blocks, making each block self-evidencing.

---

**Citrullin** (2026-01-08):

As someone who worked at IOTA, I can second this. Let’s not talk about ternary though lol ^^

There were some ideas floating around in a similar direction as the topic here.

All of these sharding approaches lack of split brain resilience though.

For the topic itself. You may be able to do something with Chandy Lamport here.

And work with threat levels here. More recent snapshot and more linked with other shards.

Provable via some sort of zkProof. Adds a lot of complexity though.

I do like the whole trust approach. We can already can observe a shift in the trust assumptions we make here.

For a long time there was this myth floating around “trustless“ systems.

Yet, we see there are quite some bold trust assumptions that don’t hold true.

You may want to check out Ethos and Gnosis Circles in this context.

I don’t see the latter working out very well, but that’s another story.

The approach is a little bit working like BGP in terms of trust assumptions.

- Would full nodes still need to store history at all?

Full nodes, yes. But you can have some different levels of lightnodes who don’t.

All that matters is the ability to check if the transactions are valid.

- Would high-latency environments (e.g. interplanetary networks) remain viable?

That’s where you get issues, for sure. But you can design around it. Realistically speaking.

With all the trends we are seeing in the industry rn. It most likely just ends up being a chain of chains.

Which isn’t too far off from what Comos was supposed to be.

And then we either fill an intent or swap between chains with based or/and native rollups.

- If consensus weight derives from behavior rather than capital, would we see less centralization?

Probably not. With capital you always end up in a accumulation scenario. A pareto distribution.

We already can observe this with staking, restaking, re-restaking etc. the greed knows no end.

This is rather a topic for taxation, but that’s something people don’t like to talk about in this space.

> Can topology collapse be formalized as finality?

It never truly can be final, can it? You need to work more with probabilities. Quantum Money. lol

I don’t see this all really working out. Especially since we now got decent alternative.

If you still want to go for it. Have fun. I feel like these ideas and thought might be more interesting with DAO managment though.

> In practice, the finality window depends almost entirely on the number of propagation hops—not on the total network size or validator count.

Yeah, but I can also just accumulate a lot of trust. And exploit this trust all at once, before it is propagated. Something along the lines of Madoff did.

> Given modern network conditions, low latency, and nodes proactively maintaining peer connections, the variance introduced by hop-based delay is negligible.

Your assumption is not valid. More and more ISPs decided to remove themselves from the open peering policy. Famously Vodafone just said the quite part out loud.

There are a lot of “high performance“ Blockchains that struggle under their assumption.

---

**YanAnghelp** (2026-01-09):

[@Citrullin](/u/citrullin) Your comments have been extremely insightful and genuinely helpful to me.

You are absolutely right that these are very serious issues in real-world engineering, and in fact a significant portion of them are problems I have already considered carefully.

For example, regarding the split-brain problem: my view is that, in theory, a system could allow trust-weighted preference to gradually bias the network toward one side and eventually achieve reintegration.   However, this process would take a very long time and cannot be considered a strong guarantee.

Regarding behavior-based weighting, I see its main advantages not only in environmental friendliness, but also in its suitability for early-stage or low-token-value networks.   It can also force participants to operate real, persistent infrastructure in order to increase their behavioral weight.   That said, I fully agree that this does not fundamentally prevent the concentration of power.

Finality is another critical issue.   As we know, the finality of any decentralized consensus system today is probabilistic in nature.   In theory, this approach could also achieve a very high probability of finality, but only under the assumption that validators actively operate nodes and possess sufficiently comprehensive and timely information.

This, however, represents a major drawback for financial use cases.

Ultimately, the entire system relies on a core assumption: that the network topology is well-behaved most of the time—that is, reachability and latency remain within expected design parameters.   Once this assumption is violated, the system’s security properties collapse entirely.

That said, I am not a blockchain practitioner.   I am just an ordinary student, and this consensus mechanism was something I conceived somewhat incidentally, so my terminology may be imprecise.   From my perspective, the most serious problem facing blockchains today is not how the technology should be further upgraded.   In practice, end-user experience has already largely stabilized.

Rather, the more urgent issue is desacralization and deffinancialization.   By deffinancialization, I mean financialization in the narrow sense—such as speculative “get-rich-overnight” token trading and excessively tight coupling to fiat currencies.

---

**Citrullin** (2026-01-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> However, this process would take a very long time and cannot be considered a strong guarantee.

That’s not necessarily an issue. As someone accepting payments and working with the liquidity flow. It’s rather about risk levels more than anything. Like, let’s compare that with how we currently do that. We use Visa, Mastercard or even some kind of payment provider. Adyen, Stripe or whatever. You got chargebacks, fraud. There is always risk associated with payments. And risks of losing some of it due to these factors. So, if you can someone guarantee that 95% of the payments or whatever  that number might be. That could work out. We just need some stable state all actors can agree on. And if 2%, 5% fail, so be it. That’s the cost of doing business. But you need to be able to give me a number.

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> Regarding behavior-based weighting, I see its main advantages not only in environmental friendliness, but also in its suitability for early-stage or low-token-value networks. It can also force participants to operate real, persistent infrastructure in order to increase their behavioral weight. That said, I fully agree that this does not fundamentally prevent the concentration of power.

I like your way of thinking. I uploaded something last year about [merit driven token distribution](https://github.com/bind-systems/tinyblock_vision/blob/3d1cb4057996814687e046c7fc03f4c30a83b2ab/tinyblock_vision_whitepaper.pdf). (page 14) You may get some inspirations from it. It’s based on [another paper](https://research.tudelft.nl/en/publications/meritrank-sybil-tolerant-reputation-for-merit-based-tokenomics/), but some additions for an agentic based approach.

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> Ultimately, the entire system relies on a core assumption: that the network topology is well-behaved most of the time

You are right with that assumption, problem is just the “most of the times“.

The compliance in the physical world might be the more important factor than losing trust in this network.

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> That said, I fully agree that this does not fundamentally prevent the concentration of power.

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> This, however, represents a major drawback for financial use cases.

The exploration informs the exploitation, so that the exploitation can finance the exploration.

That’s what it really is about. It’s not about skimming something off, it’s about what do I get in return?

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> so my terminology may be imprecise

that’s whatever. who cares really? That would be pretentious to restrict access, because of it.

![](https://ethresear.ch/user_avatar/ethresear.ch/yananghelp/48/21400_2.png) YanAnghelp:

> By deffinancialization, I mean financialization in the narrow sense—such as speculative “get-rich-overnight” token trading and excessively tight coupling to fiat currencies.

You will never get rid of the greed, ego and envy in most people.

Most people don’t even take the time to go into themselves to find out. That’s just how it is.

The system has to account for these realities we can also observe in this space.

Btw. I think that’s why ultimately Bitcoin will have to fail. We already can see it in the numbers.

Any way. So, I think more of the psychological tools we use right now to attach people to a screen.

How can you use the same methods that lead to this attention driven madness in order to create an advancement driven one. Not the tools are bad, it’s how they are used and what for.

