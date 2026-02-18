---
source: ethresearch
topic_id: 17169
title: SubnetDAS - an intermediate DAS approach
author: fradamt
date: "2023-10-23"
category: Sharding
tags: []
url: https://ethresear.ch/t/subnetdas-an-intermediate-das-approach/17169
views: 3556
likes: 15
posts_count: 9
---

# SubnetDAS - an intermediate DAS approach

# SubnetDAS – an intermediate DAS approach

*By [Francesco](https://twitter.com/fradamt) and [Ansgar](https://twitter.com/adietrichs). Thanks to [Mark Simkin](https://twitter.com/Simk1n) for discussions and help in the security analysis, and to various members of the EF research team for feedback.*

This is a *subnet-based* DAS proposal, meant to bridge the gap between EIP-4844 and full Danksharding, much like [peerDAS](https://ethresear.ch/t/peerdas-a-simpler-das-approach-using-battle-tested-p2p-components/16541). We propose a DAS construction where there is a subnet for each sample, and nodes get their samples by connecting to them. We think that it can give us more scale without jeopardizing the liveness of the whole network or increasing node requirements *compared to EIP-4844*.

For this, we do sacrifice something, i.e., **unlinkability of queries**, or rather the possibility of later addressing this issue within this DAS framework. To retrieve samples, a node has to join the corresponding subnets, and, while attempting to do so, it exposes its queries. This allows an attacker to only publish those samples, thus convincing it that the data is available while it is not. Linkability of queries is a problem faced by all DAS constructions, but it is particularly hard to see how it could be solved in a subnet-based one. It *does not affect the availability guarantees of the whole chain, and thus the safety of rollups*, but it does weaken the safety of full nodes against double spends. We discuss this issue in detail [later](#Client-safety-and-query-unlinkability), and argue that this weakening is not as significant as it may seem, and that it might be a sensible trade-off for an intermediate DAS solution.

## Why SubnetDAS

There’s a few reasons why we think that subnets are a sensible candidate for the main networking structure of an intermediate solution:

- Little networking unknowns: Subnets are a tried and tested piece of the Ethereum networking infrastructure, as attestation subnets have been used since day one of the Beacon Chain. The novelty would be that a higher number of subnets is used, but this would be counterbalanced by full nodes joining in multiple subnets each, so that each subnet should still contain sufficiently many nodes.
- Scale: with bandwidth requirements similar to EIP-4844, we think subnetDAS can achieve similar scale to full Danksharding. With the example parameters we give later, the througput would be 16 MiBs per slot, while requiring full nodes to participate in subnets whose total data assignment is 256 KiBs per slot, and validators 512 KiBs per slot, roughly in line with 4844.
- Future-compatibility: we think that the subnet infrastructure will be used even in future iterations of DAS, so that the effort is reusable:

Whatever the final networking construction for DAS might be, the networking structure of full Danksharding will likely involve subnets where rows and columns of the Danksharding square are distributed and which at least validators join to download the rows and columns they are assigned to custody (this is also assumed in peerDAS)
- Even in a later iteration, it might still make sense to use some form of subnetDAS for the fork-choice of validators, which does not need to use the same DAS construction that full nodes use in their fork-choice, to follow the chain and confirm transactions (see here for details). When used for this purpose, the weaknesses of subnetDAS are acceptable or irrelevant:

Linkability of queries does not matter, because for the fork-choice of validators we only care about global availability guarantees instead of individual ones (there’s no concerns about double spend protection, as this is not used to confirm transactions).
- Validators can be expected to have higher bandwidth requirements than full nodes, so even for the long term it is probably ok to keep bandwidth requirements similar to 4844 for validators.

Even in a later iteration, it might alternatively make sense to use subnetDAS as a fork-choice filter, while some additional sampling is used *only as part of the confirmation rule* (again, see [here](https://notes.ethereum.org/@fradamt/DAS-security-notions) for details). For example, full nodes could follow the chain (and validators participate in consensus) by only using subnetDAS for their fork-choice, while doing some peer sampling only to confirm transactions. A liveness failure of peer sampling would then only affect a full node’s ability to confirm transactions, leaving the p2p network, consensus and the transaction confirmations of super full nodes unaffected. This additional sampling could even be optional, letting full nodes choose their own tradeoff between confirmation safety and liveness. As in the previous bullet point, linkability of queries would not matter because of the additional sampling done as part of the confirmation rule.

## Construction

#### Example parameters

| Parameter | Value | Description |
| --- | --- | --- |
| b | 128 | Number of blobs |
| m | 2048 | Number of column subnets = Number of samples |
| k | 16 | Samples per slot = column subnets per node |
| r | 1 | Row subnets per validator |

Blobs are 128 KiBs, as in EIP-4844, for a total throughput of 16 MiBs per slot of non-extended data.

#### Data layout

- We use a 1D extension, instead of 2D. The blobs are extended horizontally and stacked vertically. As in the Danksharding matrix, but without a vertical extension.
- The resulting rectangle is subdivided into m columns. With the example parameters, each column is of width 4 field elements (each extended blob is 256 KiBs, or 8192 field elements). Each column is a sample.  With the example parameters, a sample has size 128*4*32 bytes  = 16 KiBs

#### Subnets

- Column subnets: Each column (sample) corresponds to a column subnet. Column subnets are used for sampling, and all full nodes connect to k of them.
- Row subnets: Each row (an extended blob) corresponds to a row subnet, which is used for reconstruction. Only validators need to connect to row subnets, and they connect to r of them.

With the example parameters, each column subnet has k/m = 1/128 of all full nodes, and each row subnet has r/n = 1/128 of all validators

[![](https://ethresear.ch/uploads/default/original/2X/3/333956ef6b2d09501b57e6c3fc69978352c1246f.png)641×277 24.4 KB](https://ethresear.ch/uploads/default/333956ef6b2d09501b57e6c3fc69978352c1246f)

#### Distribution

Blobs are distributed in the row subnets and samples in the column subnets, at the same time.

#### Sampling

Full nodes query k samples per slot, by connecting to the corresponding subnets. This is just sampling over a 1D extension, but where the samples are “long” (columns instead of points).

[![](https://ethresear.ch/uploads/default/original/2X/0/0442506d1cb1d8a0cab67ad326b499a8e1be232f.png)492×177 5.89 KB](https://ethresear.ch/uploads/default/0442506d1cb1d8a0cab67ad326b499a8e1be232f)

With the example parameters, this is a total of 16^2 = 256 KiBs, even lower than EIP-4844 (for validators there’s the added load of downloading r=1 extended blob from a row subnet, for an extra 256 KiBs).

#### Subnet choice and data retrievability

Data retrievability within the retention period raises similar questions as [here](https://ethresear.ch/t/peerdas-a-simpler-das-approach-using-battle-tested-p2p-components/16541#public-deterministic-selection-7). To address them, rotation of the subnets can be staggered and happen in the timescale of the data retention period. The effect of doing so in subnetDAS is quite different than in peerDAS, because the choice of subnets *is* the choice of samples, so not rotating the choice of subnets every slot means always sampling the same indices.

To address this, we could have nodes connect to 2k subnets instead, k stable ones and k which are rotated every slot. Connecting to the former is purely to help with subnet density and data retrievability, while the latter are actually for sampling. Nonetheless, subnetDAS is anyway particularly vulnerable to *linkability of queries*, so even a stable choice of subnets might make sense in this context.

#### Reconstruction

Local reconstruction can happen in row subnets. If some data is missing in a row subnet but exists in a column subnet, validators that are in both subnets gossip the missing data in the row subnet. Once > 50% of the extended blob is available, all validators in the row subnet reconstruct it locally, and then carry to their column subnets any data from this row which they are missing.

## Security

We analyze two aspects of the security of this construction (again, see [here](https://notes.ethereum.org/@fradamt/DAS-security-notions) for more details on the security notions):

- Global safety: except with negligible probability, unavailable data is refuted by all except a small minority of full nodes (concretely, we can set a maximum tolerable fraction of full nodes which might not refute unavailable data).
- Client safety: a client cannot be convinced that unavailable data is available, except with negligible probability.

These parallel the two roles of full nodes: contributing to enforce the rules of the network, and allowing trust-minimized interaction with the chain. The first security property is what allows full nodes to contribute to enforce the rules *of rollups built on Ethereum*, ultimately guaranteeing their safety, under the assumption that a chain which is only seen as canonical by a small minority of full nodes could never end up becoming *the* Ethereum chain, even if all validators were malicious. Importantly, this holds *even if the adversary knows all the queries in advance*.

#### Client safety and query unlinkability

The second notion is quite a bit stronger: we require that no sampling node can be tricked *at all* (except with negligible probability). To achieve it, we cannot assume that the adversary knows all queries in advance. In fact, it requires *query unlinkability*, the ability to hide that a set of queries comes from the same node/actor, because without that an adversary can always only make available exactly the data that a single node asks for.

Why do we want this stronger safety notion, if rollups are safe with the weaker one (global safety), and the whole point of a data availability is for it to be used by rollups? This is because the DA layer is *tighly coupled* with the rest of the Ethereum chain: full nodes simply ignore a chain where some blob data is not available. Tricking a full node into thinking that unavailable data is available can then subject them to a safety violation, i.e., a double spend: they confirm a transaction in a valid chain which looks safe and available, but which is actually unavailable and therefore does not end up being the canonical Ethereum chain. This holds for the confirmation of Ethereum transactions as well as rollup transactions, since rollup state is derived from the canonical Ethereum chain.

##### Ethereum transactions

I would argue that introducing DAS without query unlinkability does *not* change the security of Ethereum full nodes against double spends *too much*. There are two cases, bases on which *confirmation rule* a full node uses to begin with:

- Synchronous confirmation rule: these nodes do not wait for finality, and instead use a rule (e.g. this one) which makes synchrony assumptions and honest majority assumptions. If the latter are not satisfied (i.e. in a 51% attack), then the rule is anyway unsafe, and double spends can happen. If the latter is satisfied, we are guaranteed that the confirmed chain is available, because only a small portion of honest validators can be tricked into voting for an unavailable chain. In other words, an honest majority can only be slightly weakened due to DAS failures. Therefore, the synchronous confirmation rule is still safe under the same assumptions it requires without DAS.
- Finality: if a node waits for finality today, it gets the assurance that it will not be subject to a double spend unless there are two conflicting finalized blocks, which requires 1/3 of the validator set to commit a slashable offense. With DAS, it is also possible that a finalized block simply is not available, without there being a conflicting finalization. Note that this still requires nearly a malicious supermajority, again because only a small portion of honest validators could be convinced to vote for an unavailable chain. On the other hand, it does not seem to give economic finality guarantees against double spends. A full node might fail to recognize the finalized chain as not available, and confirm a transaction in it. If it never becomes available, social consensus would eventually have to intervene and coordinate a fork starting from a fully available chain, resulting in a safety violation for the full node. In principle, this does not need to involve any slashing, negating any economic finality. In practice, social consensus could choose to slash any validator which voted to finalized the unavailable chain and which fails to produce the data they were supposed to custody by a certain deadline. If the chain really turns out to be unavailable, this would mean that nearly a supermajority of validators has failed to produce their custodied data, and is liable to be slashed.

Moreover, keep in mind that running a super full node which downloads all the data would be an option, and certainly not a prohibitively expensive one for those who transact a lot of value and want the same exact security guarantees against double spend that a full node has today. It is perhaps at least worth discussing whether this (in our opinion minor) security reduction in the transaction confirmation security of full nodes is truly a hill to die on.

##### Rollup transactions

The picture for the security when confirming rollup transactions is quite similar, but with a few more considerations centered around validity, again depending on which confirmation rule the rollup node is using. Let’s assume that the baseline confirmation rule is Ethereum finality, which is then enhanced with some rollup-specific conditions.

For a validity rollup, the sensible choice is clearly to wait for a validity proof before confirming, though not necessarily for it to be posted and verified on Ethereum itself. Such a node does indeed get the same exact security guarantees that an Ethereum full node gets when confirming a finalized transaction (modulo issues with the proof system or the implementation of the verifier), since validity is guaranteed. In other words, the only attack vector is a double spend of the same kind we have discussed in the previous section.

For an optimistic rollup, there are multiple options. One could run a rollup full node and simply verify all state transitions, in which case clearly there are no extra concerns. This is of course not ideal since rollup nodes could in principle be much heavier than Ethereum nodes. It could also just wait for the rollup bridge to confirm the transaction, which is equally safe but would require a longer confirmation period due to the fraud proof period. Another alternative is to listen for (messages initiating) fraud proofs on a p2p network, which could be done with a shorter fraud proof period than what is appropriate for the bridge. A node operating such a fast confirmation rule could in principle be induced to confirm an invalid transaction if unavailable data is finalized and it is tricked into thinking it is available.

#### Global safety

*Tldr: even an adversary that knows all queries in advance cannot convince more than a small percentage of sampling nodes that unavailable data is available*

For an adaptive adversary, which considers *all queries at once* before deciding which data to make available, the probability that a fraction \epsilon of n nodes is successfully targeted when downloading k samples out of a total of m can be union-bounded by \binom{n}{n\epsilon}\binom{m}{m/2} 2^{-kn\epsilon}: the adversary chooses a subset of n\epsilon nodes, out of \binom{n}{n\epsilon} possible subsets, a subset consisting of at least \frac{m}{2} samples to not make available, out of \binom{m}{m/2} such subsets, and given these choices has a success probability of 2^{-kn\epsilon}. [Approximating the binomial cofficients](https://en.wikipedia.org/wiki/Binomial_coefficient#n_much_larger_than_k), we get \left(\frac{2^{n}}{\sqrt{\frac{n\pi}{2}}}e^{-\frac{\left(n\ -\ 2n\epsilon\right)^{2}}{2n}}\right)\frac{2^{m}}{\sqrt{\frac{m\pi}{2}}}2^{-kn\epsilon} = \left(\frac{2^{n}}{\sqrt{\frac{n\pi}{2}}}e^{-\frac{\left(n\ -\ 2n\epsilon\right)^{2}}{2n}}\right)\frac{2^{\left(m-kn\epsilon\right)}}{\sqrt{\frac{m\pi}{2}}}, and we want this to be < 2^{-30} or something like that. That gives us (n + m - kn\epsilon) - \log_{2}\left(e\right)\frac{n\left(1\ -\ 2\epsilon\right)^{2}}{2} < \log_2(\sqrt{nm}\frac{\pi}{2})-30

In the following plot, we set k = 16 and m = 2048. On the y-axis we have n, the number of nodes, and on the x-axis \epsilon, the maximum fraction of nodes which can be tricked (here in particular with probability \ge 2^{-30}, but the result is almost insensitive to the chosen failure probability). As long as we have at least 2000 nodes, less than 10% of the nodes can be fraudulently convinced of the availability of data which is not available. Moreover, the fraction of attackable nodes drops between 5% and 4% between 6000 and 10000 nodes.

[![graph](https://ethresear.ch/uploads/default/optimized/2X/b/b71be9f03de1fe241092074220fbaec290d6d17b_2_500x500.png)graph800×800 52.1 KB](https://ethresear.ch/uploads/default/b71be9f03de1fe241092074220fbaec290d6d17b)

(You can play with the parameters [here](https://www.desmos.com/calculator/6dwg556j77))

It is perhaps worth noting that the full Danksharding sampling with m = 512^2 (sampling on the square) and k = 75 does not do better in this kind of analysis, which considers an adversary that knows all of the queries in advance. In fact, it fares much worse, simply due to how large m is. This should not come entirely as a surprise, since nodes in this construction are required to download a much bigger portion of the data (0.256 KiBs/32 MiBs, or 1/128, vs 37.5 KiBs/128 MiBs, or ~1/3000). That said, this is just a bound which might not be tight, so a bad bound does not necessarily imply bad security. If on the other hand the bound were shown to be tight, it would mean that global safety with such a high m does not hold against a fully adaptive adversary, and instead requires some assumption about unlinkability of queries as well.

##### Security-Throghput-Bandwidth tradeoff

Naturally, we could improve any of bandwidth requirements, security and throughput by worsening  one or both of the other two. For example, halving the number of blobs to b = 64 and doubling the number of samples to k=32 would keep the bandwidth requirement the same while halving the throughput, but give us a *much better* security curve. On the other hand, we could double the throughput while keeping the bandwidth requirements the same, by setting b = 256 and k = 8, sacrificing security. Here we compare the security for k=8,16,32, i.e., corresponding to max throughput 32MiB, 16MiB and 8MiB.

[![graph1](https://ethresear.ch/uploads/default/optimized/2X/e/eefedaab19f4f8ca476b738d60788beb061e75d5_2_500x500.png)graph1800×800 42.1 KB](https://ethresear.ch/uploads/default/eefedaab19f4f8ca476b738d60788beb061e75d5)

(You can play with the parameters [here](https://www.desmos.com/calculator/8kqjzubmpq))

## Replies

**djrtwo** (2023-10-23):

Awesome design direction and accompanying analysis! ![:pray:](https://ethresear.ch/images/emoji/facebook_messenger/pray.png?v=12)

**I have a handful of questions –**

> each row subnet has r/n=1/128 of all validators

validators – or nodes-with-validators attached? I’m assuming the latter given the target values. You could try to enforce that *all validators* download/custody `r`. This is nice that it scales responsibility with # of validators, but it ends up not really being enforceable wrt purely p2p perspective. But it is natural to then roll that into a crypto-economically enforceable scheme with proof-of-custody.

---

> Blobs are distributed in the row subnets and samples in the column subnets, at the same time.

Are extensions sent in the row subnets? or should just the entire Blob payload be dropped in and sent contiguously? In 4844, we send entire blobs (rather than streaming points), I could imagine on these row subnets to just do the same and forwarding validity condition is just that the blob is fully there and correct. Potentially lose some p2p parallelization/streaming optimizations though

Another thing to consider in the event of sending individual points on subnets is anti-dos/validity conditions. If you already have the block, then you can check validity before forwarding, but if you don’t necessarily (e.g. like the 4844 decoupling), then you need proposer signatures over each point (or whatever amount the data is bundled) for some amount of anti-dos.

---

> To address this, we could have nodes connect to 2k subnets instead, k stable ones and k which are rotated every slot.

This is a good and clever idea to combine stability and quick obfuscation.

It is still linkable apriori (even if just for a short sub-slot period) due to subnet announcement/peer grafting, to know what a node is about to “query”, but it becomes much less difficult to grief a consistent set if you have the described rotation. That is, if you have purely stable choice, you can for-many-slots convince some consistent subset about availability problems, whereas if nodes are constantly shuffling, you could not keep a consistent, significant subset (barring tracking just a few particular targets) fooled for many continuous slots.

---

What does a node do to “catch up” on prior slots that they cannot follow live via gossip? I assume you need some sort of req/resp interface for querying this data up to the pruning period (similar interface to PeerDAS). If that’s the case, you almost support PeerDAS “for free” when implementing SubnetDAS.

> which makes synchrony assumptions and honest majority assumptions.

---

right, but if the honest majority assumption fails, then with linkability some nodes could be tricked to confirm unavailable data, whereas this is not the case with unlinkability. So it’s not that you are making different assumptions, it’s that when comparing linkability and unlinkability as a paradigm *within DAS*, the extent to which you break under the failure of that assumption fails.

---

> In the following plot,

I think you are missing an intended graph in this post

---

> less than 10% of the nodes can be fraudulently convinced of the availability of data which is not available. Moreover, the fraction of attackable nodes drops between 5% and 4% between 6000 and 10000 nodes

In the event that something like SubnetDAS, PeerDAS, or for that matter, any other DAS solution beyond 4844 is rolled out, then I would suspect that the data gas limit is stepped up over time using the new constructions, rather than going all-out to “full danksharding”.

Does this number – 10% can be fraudulently convinced – significantly change at lower data throughputs (e.g. 1/4 or 1/8 of the full amount) or do any other considerations of the analysis change in meaningful ways?

You mention “blobs, # of samples to download, security” as the trade-off space. Is this complete or are there other factors? I suppose security catches other concepts than just how-many-nodes-can-be-fooled – such as how populated subnets are wrt node count.

---

Can you explain more about if/where a 2D encoding can fit into this scheme?

---

Do you have any intuition or analysis on what the options are for a node that does miss a single sample? Can they increase the amount of samples they are querying with an acceptable miss rate?

---

Do the number of super-full-nodes (download everything at every slot) on the network impact any of your analysis or potential design space? E.g., if we assume there are 1000 of these on the network, would it change any of your design or selection of parametrizations wrt the various security trade-offs?

---

**fradamt** (2023-10-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> validators – or nodes-with-validators attached? I’m assuming the latter given the target values. You could try to enforce that all validators download/custody r. This is nice that it scales responsibility with # of validators, but it ends up not really being enforceable wrt purely p2p perspective. But it is natural to then roll that into a crypto-economically enforceable scheme with proof-of-custody.

I was thinking the former, i.e., a per-validator custody assignment

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Are extensions sent in the row subnets? or should just the entire Blob payload be dropped in and sent contiguously? In 4844, we send entire blobs (rather than streaming points), I could imagine on these row subnets to just do the same and forwarding validity condition is just that the blob is fully there and correct. Potentially lose some p2p parallelization/streaming optimizations though
>
>
> Another thing to consider in the event of sending individual points on subnets is anti-dos/validity conditions. If you already have the block, then you can check validity before forwarding, but if you don’t necessarily (e.g. like the 4844 decoupling), then you need proposer signatures over each point (or whatever amount the data is bundled) for some amount of anti-dos.

I think it would be preferable to gossip blobs in the row subnets, rather than extended blobs, just to save on bandwidth. Nodes can re-do the extension locally.

For local reconstruction, it would be necessary to allow gossiping of individual points (here meaning a cell, the intersection of a row and a column, which would be 4 field elements with the example parameters) in row subnets. For this, I think it would be ok to wait to have the block (or at least a header and the commitments, if they were to be gossiped separately) so that you can validate whether or not you should forward.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> What does a node do to “catch up” on prior slots that they cannot follow live via gossip? I assume you need some sort of req/resp interface for querying this data up to the pruning period (similar interface to PeerDAS). If that’s the case, you almost support PeerDAS “for free” when implementing SubnetDAS.

For column subnets, I think it would be ok to just choose k subnets, join them and request historical samples from them, regardless of whether there is supposed to be some subnet rotation when you’re doing sampling “live”. For row subnets, I think in the latter case (e.g. if as a validator you are meant to be in 1 stable row subnet and in 1 which rotates) you probably want to join one row subnet at a time, out of the rotating ones which you have been assigned to in the period you couldn’t follow live, and request all blobs you need from that subnet. Basically catching up subnet by subnet instead of slot by slot, so you don’t have to keep hopping between subnets.

Either way yes, I think the kind of req/resp interface mentioned in PeerDAS seems like the right tool here, and I guess peer sampling would be supported as long the same interface can also be used without being in the same subnet. think that supporting peer sampling would be great, because, as I mentioned in the “Why SubnetDAS” section, it could (potentially optionally) be used only as part of a confirmation rule, which I think retains all its added security value while preventing any negative effect on the liveness of the network.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> right, but if the honest majority assumption fails, then with linkability some nodes could be tricked to confirm unavailable data, whereas this is not the case with unlinkability. So it’s not that you are making different assumptions, it’s that when comparing linkability and unlinkability as a paradigm within DAS, the extent to which you break under the failure of that assumption fails.

It’s true that, when the honest majority assumption fails, unlinkability still prevents any full node from seeing an unavailable chain as canonical. What I am questioning is whether or not this is actually very useful. For the safety of rollups, I don’t think this is very important at all, because anyway it’s hard to imagine that *the* canonical Ethereum chain could end up being one which only a small minority of full nodes see as available. I also don’t think we should rely on query unlinkability for the safety of rollups, unless there’s a bulletproof way to achieve it, which is not so clear, so I think that the “honest minority of full nodes” argument is anyway the best defense we have there.

For the synchronous confirmation rule, a malicious majority can cause reorgs, and thus safety failures for full nodes which use that rule, regardless of whether queries are linkable or not. If a full node confirms chain A and then reorgs to chain B, unlinkability still guarantees that chain A was available. But why does it matter whether it was? It seems to me that the safety violation due to the reorg is what matters here.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Does this number – 10% can be fraudulently convinced – significantly change at lower data throughputs (e.g. 1/4 or 1/8 of the full amount) or do any other considerations of the analysis change in meaningful ways?

If the throughput (number of blobs) is reduced by a factor of x without changing anything else, then the security is exactly the same, we just decrease the bandwidth requirements by x as well, because samples (columns) are x times smaller. Of course one could allocate part of the throughput decrease to lowering requirements and part of it to boosting security.

For instance, with 1/4 of the throughput one could double the number of samples while still halving the bandwidth requirements. This is the full graph for the resulting security, with k=32, m = 2048. Even with 2000 nodes, the attackable fraction is below 5%.

[![graphk=32](https://ethresear.ch/uploads/default/optimized/2X/b/be0523483bb99e3af821443db92a3fcf3e74ab82_2_500x500.png)graphk=32800×800 57 KB](https://ethresear.ch/uploads/default/be0523483bb99e3af821443db92a3fcf3e74ab82)

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> You mention “blobs, # of samples to download, security” as the trade-off space. Is this complete or are there other factors? I suppose security catches other concepts than just how-many-nodes-can-be-fooled – such as how populated subnets are wrt node count.

Yes, subnet population is also part of the trade-off space.

With b = \text{number of blobs}, n = \text{number of nodes}, s = \text{blob size}, we have these:

Throughput: s * b

Bandwidth per node: k/m*(2*\text{throughput}) = 2sb*k/m

Subnet population: k/m*n

k/m is both the percentage of the extended data which is downloaded by each full node and the percentage of full nodes which are in each column subnet, so, for fixed n, we can’t increase subnet population without equally increasing bandwidth per node.

For fixed n and s, the levers we have are basically:

- Increase b, which proportionally increases throughput and bandwidth requirements and leaves everything else unchanged
- Increase k, which increases safety and proportionally increases bandwidth per node and subnet population
- Increase m, which decreases safety and proportionally decreases bandwidth per node and subnet population

(Here safety = how-many-nodes-can-be-fooled)

Given a maximum bandwidth per node and minimum subnet population, we can get the maximum supported throughput. The only wiggle room we have is that we can increase safety by increasing k and m while keeping k/m fixed (increasing k has more of a positive effect than the negative effect of increasing m).

Something that is not clear to me here is what are the effects of increasing m while keeping k/m fixed. With 10000 nodes, how does having 100 subnets where each node joins 1 (100 nodes per subnet) compare to having 1000 subnets where each node joins 10 (also 100 nodes per subnet)? Is there significantly more overhead (or some other notable problem) in the second case?

Also not clear to me, what is the impact of the number of nodes? Do we care about the absolute number of nodes per subnet (k/m * n) or the relative one (k/m)? In other words, does having more nodes overall mean that we can increase throughput without making anything worse, or do we anyway always need to keep k/m somewhat high?

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Can you explain more about if/where a 2D encoding can fit into this scheme?

The issue with a 2D encoding in this context is that the number of subnets is the number of samples, and this would be very high if we use points as samples, e.g. with a 256x256 square (128 blobs, vertically extended, split into equally sized columns) we’d get 64k samples/subnets. We could do the 2D extension but still use thin columns as samples, but then I am not sure there is any benefit, and we still double the amount of data?

A reason to do a 2D encoding could be if we want to also support a cheaper kind of sampling, with much smaller samples, e.g. columns are used as samples by SubnetDAS, so the number of subnets is still low, but points are used as samples by PeerDAS. Although even in this case, I don’t see why we couldn’t just use even thinner columns as samples for PeerDAS? For example, here the red columns still correspond to subnets, are used for distribution and for subnetDAS, and are somewhat large because we don’t want too many subnets. They can then further be broken down into thinner green columns, which are used by some other lighter form of DAS that does not use subnets.

[![subnetDAS2](https://ethresear.ch/uploads/default/original/2X/9/962f32847dcd7830f9209d714e98c033a536be00.png)subnetDAS2502×182 69.9 KB](https://ethresear.ch/uploads/default/962f32847dcd7830f9209d714e98c033a536be00)

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Do you have any intuition or analysis on what the options are for a node that does miss a single sample? Can they increase the amount of samples they are querying with an acceptable miss rate?

For example, one could tolerate a single miss out of the k queries. That would make the failure probability for each node \binom{k}{0}2^{-k} +\binom{k}{1}2^{-k} = (k+1)2^{-k}, and the failure probability for n\epsilon nodes ((k+1)2^{-k})^{n\epsilon}, adding a factor of (k+1)^{n\epsilon} compared to the analysis from the post. The expression we care about then becomes: \ (n+m\ +\ \log_{2}\left(k+1\right)n\epsilon\ -kn\epsilon)-\log_{2}\left(e\right)\frac{n\left(1\ -\ 2\epsilon\right)^{2}}{2}-\log_{2}(\sqrt{nm}\frac{\pi}{2}) - 30, with (\log_{2}\left(k+1\right)-k)n\epsilon instead of just -kn\epsilon. To get the same security as before, we then need to increase k roughly by \Delta k = \log_{2}{k}, e.g. we get roughly the same security with k=16 and no tolerance for misses or k=20 and tolerating a single miss. You can check this out [here](https://www.desmos.com/calculator/sqybzxaet7).

Playing around with the parameters, it’s pretty clear that tolerating multiple misses is not really practical, because it ends up requiring a significant number of additional samples. This is because, to tolerate t misses, the failure probability for a node blows up to \sum_{i=0}^{t}\binom{k}{i}2^{-k}.

---

**BirdPrince** (2023-10-26):

Would you consider commercializing this idea?

Are differentiated incentives or a means of balancing incentives needed for the nodes in the subnet?

---

**djrtwo** (2023-10-27):

This a proposal for core protocol. Nodes are on subnets so they can do DA checks and follow the chain. This isn’t a product

---

**Nashatyrev** (2023-11-08):

Here is kind of a slightly alternative view on networking organization and the potential approach to reliable and secure push/pull sampling: [Network Shards - HackMD](https://hackmd.io/_nNU5x-tQQOUDtkjUdSu6A)

---

**dankrad** (2023-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> #### Reconstruction
>
>
>
> Local reconstruction can happen in row subnets. If some data is missing in a row subnet but exists in a column subnet, validators that are in both subnets gossip the missing data in the row subnet. Once > 50% of the extended blob is available, all validators in the row subnet reconstruct it locally, and then carry to their column subnets any data from this row which they are missing.

I think we need to talk about reconstruction more, because it is actually crucial for the safety of DAS, where we want the property of *convergence*: Once the DA threshold (e.g. 50% in this proposal) is reached, we want *all* nodes to agree that the data is available. This property should be robust even if a majority of validators is malicious, for obvious reasons.

I am assuming reconstruction on SubnetDAS works like this:

1. Samples are sent on subnets, we assume >50% are available.
2. Let’s assume row subnets start off empty. Individual samples are transferred to row subnets by those nodes at the intersections.
3. Each row subnet will reach >50% of samples, and nodes on it will perform reconstruction.
4. Nodes at the intersections will transfer their samples to column subnets that didn’t originally have samples transmitted [Note this also requires individual samples to be gossiped on column networks]
5. Eventually, all column networks will have 100% of samples gossiped, allowing all nodes to confirm that the data is available.

Since columns are not extended, we need 100% of the data to be transmitted in order to be able to confirm availability in step 5. This means that any single disrupted row network would actually disrupt the convergence property.

Let’s see how this works out in the current proposal. A validator row subnet has 1/128 of all validators. Assuming a malicious majority is attacking the chain, at least 2/3 of these are malicious. So far so good: Even at a very conservative 128k validators (much less than today), we would still have >300 honest validators in this case, and even at 90% malicious it would still be 100. This sounds like a lot – in practice most validator nodes run 100s of validators so they would join all the column subnets.

The relevant question then becomes – is a subnet with 66% [90%, 95%] malicious nodes reliable? This I am currently unsure about. I think this would be an important topic to research.

Note that under the given construction, it suffices to disrupt a single row subnet to completely stop reconstruction – all samples would be incomplete if that subnet is not able to do its part. (One of the advantages of a 2d construction would be that even disruption of some rows and columns could be worked around) So this is where it is potentially brittle, and more generally attack conditions for subnets would have to be researched since they would have to be very reliable for this to be safe.

(To make it more robust, we can add backup supernodes just as in PeerDAS – however making these lightweight would require an additional RPC protocol, which goes against the idea of SubnetDAS which is to mainly reuse existing networking primitives)

---

**pop** (2023-11-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> Something that is not clear to me here is what are the effects of increasing m mm while keeping k/m k/mk/m fixed. With 10000 nodes, how does having 100 subnets where each node joins 1 (100 nodes per subnet) compare to having 1000 subnets where each node joins 10 (also 100 nodes per subnet)? Is there significantly more overhead (or some other notable problem) in the second case?

It’s quite hard to answer what is the maximum number of subnets a node can handle. The best way to estimate it is to do the simulation with the real software.

Intuitively, I think 1 subnet per node is not different from 10 subnets per node. I think it can probably reach 100, but probably not 1,000.

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> Also not clear to me, what is the impact of the number of nodes? Do we care about the absolute number of nodes per subnet (k/m * n) (k/m∗n)(k/m * n) or the relative one (k/m)? (k/m)?

We care about the relative one. Sometimes I mention the number of nodes in subnets because we usually assume that the number of nodes is 5,000-10,000 and it’s very likely that it will not go much higher (probably 20,000, but not 100,000).

The reason is that, if the ratio is too low, it will be very hard to find the subnet peers in discv5. Imagine that you randomly walk into the crowd and ask people if they are subscribed to something, let’s say Netflix. If the ratio of its subscribers to the population is high, you can find some in the crowd and start talking about Netflix.

---

**pop** (2023-11-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> #### Reconstruction
>
>
>
> Local reconstruction can happen in row subnets. If some data is missing in a row subnet but exists in a column subnet, validators that are in both subnets gossip the missing data in the row subnet. Once > 50% of the extended blob is available, all validators in the row subnet reconstruct it locally, and then carry to their column subnets any data from this row which they are missing.

I have a concern on this one. This can lead to congestion in the subnets and potentially lead to the DoS if too many nodes do reconstruction at the same time.

The nature of gossipsub is broadcasting, in contrast to DHT which is unicast. That is, if you send a single message, everyone in the subnet will receive it. That means, if you use x bandwidth to upload a message, the whole subnet will use nx bandwidth to download/forward that message (the amplification factor is n). In contrast to the DHT, if you want to have n nodes to have your message, you need to send it directly to those nodes one by one and use nx bandwidth (the amplification factor is 1).

Because the amplification factor is higher in gossipsub, the subnet will be quite congested, if many nodes want to do the reconstruction at the same time.

There are two ways that I can think of to resolve this problem:

1. Allow only some validators to do reconstruction in any epoch. This can limit the congestion because the number of reconstructors is limited, but, in case we need to do reconstruction, we have to assume that some validators in the allowed list will do it. (Probably we should incentivize them if there is a way to do so)
2. Set the message id to include the epoch number and not depend on the publisher.

When the message id doesn’t depend on the publisher, it doesn’t matter how many nodes do the reconstructions because the reconstructed messages from all the reconstructors are treated as a single message and will be downloaded and forwarded only once.
3. The epoch number is included so that we allow only one reconstruction per epoch. Since the message id doesn’t depend on the publisher anymore, the nodes may not forward the messages if there is another later reconstruction. Including the epoch number indicates that this is another round of reconstruction, not the same one as the previous one.

I think the second way is better than the first one in every aspect, but include both to throw ideas.

