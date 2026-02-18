---
source: ethresearch
topic_id: 20091
title: Based Preconfirmations with Multi-round MEV-Boost
author: linoscope
date: "2024-07-18"
category: Layer 2
tags: [mev, preconfirmations, based-sequencing, sequencing]
url: https://ethresear.ch/t/based-preconfirmations-with-multi-round-mev-boost/20091
views: 14342
likes: 11
posts_count: 5
---

# Based Preconfirmations with Multi-round MEV-Boost

[![image](https://ethresear.ch/uploads/default/original/3X/f/b/fb1798cc79775d7958124717d6ba5cc97c1aa008.jpeg)image719×411 59.8 KB](https://ethresear.ch/uploads/default/fb1798cc79775d7958124717d6ba5cc97c1aa008)

By [Lin Oshitani](https://twitter.com/linoscope) ([Nethermind Switchboard](https://switchboard.nethermind.io/), [Nethermind Research](https://www.nethermind.io/nethermind-research)). Many thanks to [Conor](https://twitter.com/ConorMcMenamin9) for the detailed back-and-forth on crafting this document and to [Aikaterini](https://www.linkedin.com/in/aikaterini-panagiota-stouka/), [Elena](https://x.com/ElenaPetreska0x), [Ahmad](https://twitter.com/smartprogrammer), [Anshu](https://twitter.com/aj_jalan), [Swapnil](https://twitter.com/swp0x0), [Tomasz](https://twitter.com/tkstanczak), [Jinsuk](https://twitter.com/totorovirus), [Quintus](https://twitter.com/0xQuintus), [Ceciliaz](https://x.com/ceciliaz030), and [Brecht](https://twitter.com/Brechtpd) for the helpful comments and/or review. This work was partly funded by Taiko. The views expressed are my own and do not necessarily reflect those of the reviewers or Taiko.

# TL;DR

As we outlined in our previous post [Strawmanning Based Preconfirmations](https://ethresear.ch/t/strawmanning-based-preconfirmations/19695), naive implementations of based preconfirmations introduce many negative externalities that require thoughtful consideration.

In this post, we will expand on the negative externalities of based preconfirmations by examining them through the lens of the L1 PBS pipeline. Then, we propose *multi-round MEV-Boost*, a modification of MEV-Boost that enables based preconfirmations by running multiple rounds of MEV-Boost auctions within a single slot. This approach inherits the L1 PBS pipeline and mitigates the negative externalities of based preconfirmations as a result.

# Motivation

As Justin Drake [defines](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016#:~:text=a%20based%20rollup%20is%20one%20where%20the%20next%20L1%20proposer%20may%2C%20in%20collaboration%20with%20L1%20searchers%20and%20builders%2C%20permissionlessly%20include%20the%20next%20rollup%20block%20as%20part%20of%20the%20next%20L1%20block) in the original post, based rollups are rollups “where the next L1 proposer may, in collaboration with L1 searchers and builders, permissionlessly include the next rollup block as part of the next L1 block”. Using the [MEV supply chain](https://flashbots.mirror.xyz/bqCakwfQZkMsq63b50vib-nibo5eKai0QuK7m-Dsxpo) diagram, based rollups can be illustrated below:

[![Based Rollups (5) (1)](https://ethresear.ch/uploads/default/optimized/3X/a/c/ac29f931cf332c1b1b38334158920d6807f499f1_2_690x346.png)Based Rollups (5) (1)961×482 10.9 KB](https://ethresear.ch/uploads/default/ac29f931cf332c1b1b38334158920d6807f499f1)

Notice that the L2 transactions, represented as the red line, go through the same process as the L1 transactions, represented as the black line. By effectively “piggybacking” the L1 PBS pipeline, based rollups provide two key benefits:

- Benefit 1: Since no additional actors (and thus no additional choke points) are introduced for L2 sequencing, based rollups fully inherit L1 censorship resistance, liveness, and credible neutrality.
- Benefit 2: Since the L1 and L2 transactions are sequenced by the same entity (the builder), based rollups enable not only synchronous L2-L2 composability but also synchronous L1-L2 composability.

Based rollups are great. They solve L2 fragmentation and sequencer decentralization while enabling L1 composability and inheriting L1’s censorship resistance, liveness, and credible neutrality. They are the only rollups that can have these properties simultaneously.

However, they have one large drawback: they also inherit the 12-second L1 block time. To address the slow confirmation time, Justin introduced [base preconfirmations](https://ethresear.ch/t/based-preconfirmations/17353). In this approach, L1 proposers can opt into providing preconfirmations for based rollup L2 transactions, as shown below:

[![Based Preconf (2) (1)](https://ethresear.ch/uploads/default/optimized/3X/6/e/6e65221a830715cead4428b2724688ce66d7520c_2_690x346.png)Based Preconf (2) (1)961×482 16.4 KB](https://ethresear.ch/uploads/default/6e65221a830715cead4428b2724688ce66d7520c)

Since providing preconfirmations requires technical sophistication, most based preconfirmation designs include a delegation mechanism that allows validators to outsource the preconfirmation duty to a designated preconfer, as illustrated below:

[![Based Preconf with delegation (2)](https://ethresear.ch/uploads/default/optimized/3X/f/9/f9346fd068da5aa3ae0e57fceccc6c2af223b958_2_690x346.png)Based Preconf with delegation (2)961×482 19.8 KB](https://ethresear.ch/uploads/default/f9346fd068da5aa3ae0e57fceccc6c2af223b958)

Notice that L2 and L1 transactions no longer share the block-building pipeline. As such, the benefits of based rollups are diminished:

- On benefit 1: We introduced an additional choke point to the system, the preconfer, which can censor L2 transactions or degrade L2 liveness by going down. As a result, the inheritance of L1 censorship resistance and liveness are degraded.
- On benefit 2: We now have two parallel block-building entities: one for L1 (the builder) and another for L2 (the preconfer). Consequently, L1-L2 composability now requires coordination between the builder and the preconfer. This adds complexity and can lead to builder-preconfer integration, where the proposer delegates not only their preconfirmation right but also the whole block-building right to the preconfer ahead of their slot.

In summary, by introducing preconfirmations, we lost the below structure:

[![Based Rollups (5) (1)](https://ethresear.ch/uploads/default/optimized/3X/a/c/ac29f931cf332c1b1b38334158920d6807f499f1_2_690x346.png)Based Rollups (5) (1)961×482 10.9 KB](https://ethresear.ch/uploads/default/ac29f931cf332c1b1b38334158920d6807f499f1)

As a result, many of the benefits of based rollups are diminished.

So, what if we keep this pipeline but run it multiple times within a slot to achieve fast preconfirmations? This brings us to the main contribution of this document: *Multi-round MEV-Boost*.

# Multi-round MEV-Boost

At a high level, Multi-round MEV-Boost, or *MR-MEV-Boost* (pronounced “*mister-mev-boost*”, h/t [Conor](https://twitter.com/ConorMcMenamin9) for the idea on the pronounciation :)) for short, works as follows:

- Split each slot into a fixed number of rounds, e.g., 4 rounds with 3 seconds each.
- Within each round, run a single MEV-Boost auction. As a result of the auction, a single partial block (a.k.a partial payload) will be signed and published, i.e., the partial block will be preconfirmed.
- The full block is created and published at the end of the slot. The full block should contain the partial blocks in the exact order they were preconfirmed without inserting any transactions before or in between.

## Refresher: MEV-Boost

Before diving deeper into the proposed protocol, let’s quickly review today’s [MEV-Boost](https://docs.flashbots.net/flashbots-mev-boost/introduction) PBS pipeline used in L1 Ethereum.

[![MEV-Boost](https://ethresear.ch/uploads/default/original/3X/f/e/fe199d4c844c9230a675292724deb29c9e03a3df.png)MEV-Boost715×587 12.5 KB](https://ethresear.ch/uploads/default/fe199d4c844c9230a675292724deb29c9e03a3df)

1. Builders send the header, payload, and bid to the relayer.
2. The relayer checks the validity (the bid is correct, the payload does not contain invalid transactions, etc), stores the payload, and then sends the header and bid to the proposer.
3. The proposer selects the header with the highest bid, signs it, and then sends the signed header to the relayer.
4. The relayer propagates the signed header and corresponding payload to the network.

## Protocol Description

In this section, we describe the MR-MEV-Boost protocol.

### Protocol Flow Overview

To incentivize proposers to provide preconfirmations, we introduce a *preconf transaction*, where the payment of a *preconf tip* is conditioned on being preconfirmed. It will include the following information on top of the transaction payload itself:

- tip: The preconfirmation tip paid for being preconfirmed.
- target_slot: The latest slot in which the preconf transaction can be included.
- target_round: The latest round within the target_slot in which the preconf transaction can be included.

The [Preconf Transaction](#preconf-transaction) section will discuss the encoding and enforcement of these conditions.

Using this new transaction type, MR-MEV-Boost works as follows:

[![MR-MEV-Boost](https://ethresear.ch/uploads/default/optimized/3X/7/a/7a4dc3f4c38b4184016390e2e48dc44e5630da74_2_252x500.png)MR-MEV-Boost1132×2243 202 KB](https://ethresear.ch/uploads/default/7a4dc3f4c38b4184016390e2e48dc44e5630da74)

1. Users submit preconf transactions to the builders. The submission can be through any order flow pipeline used in current L1, such as:

Public mempool.
2. Private order flow.
3. Order flow auctions on MEVBlocker, MEV-Share, SUAVE, etc.
4. The builders build partial_payloads. The partial payload built by the builders should only include preconf transactions with target_slot and target_round at or after the current block/round. To commit to this, the builder signs the merkle_root (denoted as sig_b ) and becomes subject to builder slashing condition 1, described in the slashing condition section.
5. The relayer checks the validity (e.g., the bid is correct, the partial_payload does not contain invalid transactions, etc.), stores the partial_payload, and then sends the merkle_root and bid to the proposer.
6. Proposer signs (denoted as sig_p) and returns the selected merkle_root together with the current round.
7. The relay publishes the selected partial_payload and the associated round and signatures to the preconf network. Note that the preconf network is different from the existing L1 p2p network. Only entities interested in the preconfirmed state (partial block builders, relays, full-node providers, etc.) must subscribe to the preconf network.
8. End users—or, more precisely, the L2/L1 full nodes to which they are connected—verify that the merkle_root is signed by the proposer and is associated with the current round. Upon confirmation, they accept the partial_payload as preconfirmed and execute it to update to the latest preconfirmed state.
9. to 6. is repeated multiple rounds within the slot. The number of rounds within each slot will be fixed. The final round will run concurrently with the full block MEV-Boost auction at 8.-11.

to 11. The MEV-Boost auction is conducted for the full block. An important difference with the usual L1 MEV-Boost auction is that the `merkle_proofs` are propagated from the builder to the proposer. These proofs prove that the `partial_payload`s are included in the full block in the order they were preconfirmed without any other transaction being inserted before or between them. By validating these proofs, the proposer can ensure that the proposer slashing condition 2, described in the [slashing conditions section](#slashing-conditions), is not violated without needing to trust the relayer (h/t to [Brecht](https://twitter.com/Brechtpd) for the idea of using Merkle proofs here).

### Preconf Transaction

Let’s consider the encoding of the preconf transactions. For L2s, the additional fields can be introduced as custom encodings of the transactions. For L1, they can be implemented through an [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)-style entry point contract that wraps the contract calls with additional information.

To enforce the expiration, the L2 execution layer (or [derivation layer](https://github.com/ethereum-optimism/specs/blob/b1c9b7985b65bd2d065a414f5ad0552f36e48540/specs/protocol/derivation.md#deriving-the-transaction-list)) and L1 entry point contract will filter out preconf transactions with expired `target_slot`. On the other hand, since the L1 is unaware of the concept of rounds, expiration based on `target_round` will be enforced via builder slashing condition 1, explained in the next section.

### Slashing Conditions

To ensure that the full block matches with the preconfed partial blocks, the proposer will be subject to:

- Proposer slashing condition 1: The proposer must not sign two conflicting merkle_roots within the same round.
- Proposer slashing condition 2: The final full_payload should contain all the partial_payloads in the order they are signed and published without any other transaction being inserted before or in between.

Furthermore, to crypto-economically enforce the expiration of preconf transactions, the builder will be subject to:

- Builder slashing condition 1: Each partial_payload must only include preconf transactions with target_slot and target_round at or after the current slot/round.

We impose this condition on the builder rather than the proposer because the proposer does not see the partial payload when signing. An alternative approach would be to make this a proposer slashing condition and require the relayer to ensure the condition is not violated. However, this would necessitate the proposer trusting the relayer to avoid being slashed rather than only relying on the relayer to avoid missing a slot, as is currently done in L1 MEV-Boost.

### User Actions

To mitigate the [fair exchange problem](https://ethresear.ch/t/strawmanning-based-preconfirmations/19695#problem-4-fair-exchange-7), wallets or full nodes to which end users are connected should take the actions below:

- User action 1: Stop submitting preconf transactions if preconfirmed partial_payloads are not published in a timely manner. For example, if we have 4 rounds in a slot, then stop submitting preconf transactions if a partial_payload is not published every 3 seconds.
- User action 2: Set target_slot and target_round to a reasonably close block and round (e.g., one or two rounds ahead). By doing so, builders are required to respond in a timely manner to preconfirmation transactions to avoid the preconfirmation transactions being invalidated.

More on how the fair exchange is addressed is described in the [analysis section](#analysis).

### L1-L2 Composability

Since the partial payloads can contain both L1 and L2 transactions, builders can ensure L1-L2 composability by including L1-L2 transaction bundles in the partial payloads.

### Non-opted-in Slots

When the current L1 slot’s proposer has not opted in as a preconfer, L1 transactions will be proposed by the current proposer, while L2 transactions will be proposed by the next opted-in preconfer in the lookahead (we follow Justin’s [original based preconfirmation design](https://ethresear.ch/t/based-preconfirmations/17353#:~:text=proposer%20lookahead%E2%80%94higher%20precedence%20for%20smaller%20slot%20numbers) here). This results in two simultaneous MEV-Boost auctions: the usual L1 MEV-Boost auction signed by the current L1 proposer and the MR-MEV-Boost auction signed by the next preconfer. As a result, L1-L2 composability and L1 preconfirmation will be lost during these non-opted-in slots. Note that this limitation applies to all off-protocol preconfirmation designs.

# Analysis

In this section, we will perform an initial analysis of the proposed protocol and identify its drawbacks.

### Have we solved the problems?

Let’s revisit the problems raised in the [Strawmanning Based Preconfirmations](https://ethresear.ch/t/strawmanning-based-preconfirmations/19695) post and see if and how MR-MEV-Boost addresses them.

**Problem 1: Latency race**

Latency races are when searchers fight to be the first to access the preconfer, leading to colocation or vertical integration. With MR-MEV-Boost, this issue is largely mitigated by preconfirming batches and conducting auctions within the batch, as it promotes competition based on price rather than speed. It is generally acknowledged that batch auctions help reduce latency wars compared to continuous first-come, first-served ordering, as described in [this paper](https://academic.oup.com/qje/article/130/4/1547/1916146) and [this post](https://ethresear.ch/t/latency-arms-race-concerns-in-blockspace-markets/14957).

**Problem 2: Congestion**

Congestion issues arise when searchers flood the rollup with probabilistic arbitrage attempts. With MR-MEV-Boost, this issue is mitigated as searchers are incentivized to participate in auctions rather than resort to spam.

**Problem 3: Tip pricing**

The MEV-Boost auction will handle the tip pricing of the preconfirmation. Furthermore, by introducing batching and auctions within the batch, proposers can price the preconfirmation tips more effectively (hence capturing revenue) than by providing a continuous stream of per-transaction preconfirmations.

**Problem 4: Fair exchange**

Let’s see how MR-MEV-Boost addresses the [fair exchange problem](https://ethresear.ch/t/strawmanning-based-preconfirmations/19695#problem-3-tip-pricing-6), where the proposer withholds publishing preconfirmations to the user. Note that preconfers are incentivized to withhold preconf promises as much as possible to maximize their opportunity to reorder and insert transactions, thereby increasing their MEV.

There are two cases to consider:

- If the proposer withholds preconfirming partial payload (i.e., stops signing merkle_roots of partial_payloads), users will stop sending preconfirmation requests (user action 1), reducing the proposer’s order flow and, consequently, revenue.
- If the proposer intentionally publishes empty partial payloads, pending preconf transactions will expire after a few rounds (user action 2 and builder slashing condition 1), reducing the proposer’s order flow and, consequently, revenue.

In summary, end users monitor and enforce proposers’ honest behavior by linking the proposers’ revenue to the timely preconfirmation of partial payloads.

A potential alternative would be to introduce a committee to monitor and attest to the timely releases of partial payloads. However, this would require additional trust assumption to an external committee unless we enshrine the protocol into the L1. More on enshrinement in the [future direction section](#future-direction).

**Problem 5: Liveness**

With existing based preconfirmation designs where preconfirmation duties are delegated ahead of the slot, liveness relies on this single external entity for the duration of the preconfer’s slot(s). On the other hand, with MR-MEV-Boost, liveness concerns are reduced as we do not introduce such “lock-in” to a specific entity before the slot. If some builders or relayers are unavailable, others can step in to maintain functionality. Moreover, even if the entire multi-round MEV-Boost pipeline fails, proposers still have the option to construct their own partial blocks and preconfirm them independently.

**Problem 6: Early auctions**

Early auctions are not introduced as preconfirmations are provided through the MEV-Boost JIT auctions.

## Round Interval

How short can each round in MR-MEV-Boost be? If it is too long, it will degrade the user experience; if it is too short, it will impose excessive network and hardware requirements on builders and relays, thus hurting decentralization.

In each round, the relayer has two tasks:

- (A) Run the partial block auction.
- (B) Propagate the partial block.

Task (A) consists of the time it takes the builder to construct the block, the time it takes the relay to validate the block, and two network round-trips: one between the builder and the relay and another between the relay and the proposer. Assuming that [block construction](https://x.com/SheaKetsdever/status/1808509437700665543), validation, and network round-trips take 500 milliseconds each, we get a ballpark estimate of 2 seconds.

For task (B), considering L1 allocates 4 seconds for block propagation and 8 seconds for consensus, and no consensus is needed for partial blocks, a good upper bound for propagation time is 4 seconds. In practice, it should be much shorter because only block builders, relays, and full-node providers need to receive these partial blocks, and they have better network bandwidth and lower latency than average validators. Let’s assume 1-2 seconds for this analysis.

Combining 2 seconds for (A) and 1-2 seconds for (B) gives us 3-4 seconds per round.

These estimates are highly approximate, and further research and analysis are needed. Additionally, making the interval too short will intensify latency races toward the end of the batch duration, as described [here](https://ethresear.ch/t/latency-arms-race-concerns-in-blockspace-markets/14957#auction-designs-for-transaction-ordering-2), and should be considered.

## Drawbacks

Next, we will outline the drawbacks of this protocol when compared to existing based preconfirmation designs, such as the one described in the [original post](https://ethresear.ch/t/based-preconfirmations/17353). An analysis of more general drawbacks of preconfirmations will be reserved for future work.

### No Speed-of-light Continuous Preconfirmations

MR-MEV-Boost does not provide speed-of-light preconfirmations with hundreds of milliseconds latency, like [Arbitrum’s first-come-first-serve sequencer](https://docs.arbitrum.io/how-arbitrum-works/sequencer). Instead, it offers preconfirmations in batches with a few seconds of latency between them, similar to [Optimism’s approach](https://docs.optimism.io/connect/resources/glossary#time-slot).

[Solana](https://solana.com/) and [Jito](https://www.jito.wtf/) provide an interesting case study on continuous versus batched preconfirmations. In Solana’s “continuous block building,” the leader streams (i.e., preconfirms) processed transactions continuously. Combined with Solana’s fixed low fee, continuous block building led to network spamming and latency races, causing validators to [waste 58% of their time processing failed arbitrages](https://www.jito.network/blog/solving-the-mev-problem-on-solana-a-guide-for-stakers/). Jito addressed this by introducing a 200ms “speed bump” (batches) and a mev-geth style bundle auction for batches, achieving an 80% share with their Jito validator client. This example indicates that that continuous preconfirmations are likely unsustainable due to spam and that batching and some auction for each batch are required. For more details, watch this informative talk by Zano Sherwani, co-founder of Jito, [here](https://www.youtube.com/watch?v=c-O_JZI2QAA).

### Relay Burden

MR-MEV-Boost introduces additional burdens to the relays without incentives. Instead of managing a single round of MEV-Boost auctions, relayers must handle multiple rounds within a single slot, each within a limited timeframe. If the cost of operating a relayer increases too much, it may lead to further relayer centralization and [builder-relay integration](https://collective.flashbots.net/t/builderelay/2688/1), or alternatively, no relayer may opt to support MR-MEV-Boost. Relayer incentives are a [long-lasting problem](https://www.gate.io/learn/articles/the-pursuit-of-relay-incentivization/1257) in L1, and MR-MEV-Boost likely worsen this situation.

One way to mitigate the issue is to incorporate [optimistic relay](https://frontier.tech/optimistic-relays-and-where-to-find-them) schemes to reduce the relayer’s operational costs. With this approach, relayers optimistically assume the honesty of the block-builder and skip the validation work for payloads sent from the builder. If the builder is later found to deviate from honest behavior, their collateral will be used to refund the proposer. Optimistic relaying would be especially helpful as it allows relayers to bypass the need to validate the based rollup transactions when verifying partial blocks.

Another potential solution is for the proposers to share the preconfirmation tip revenue with the relay to compensate for the additional workload.

### Blob Efficiency

So far, we have blurred the line between L1 and L2 preconfirmations. This is somewhat intentional, as L2 transactions are included within L1 transactions. However, there are cases where the difference becomes important.

Consider a scenario where the L2 transactions within a round cannot fill an entire blob. If we only support preconfirmations for L2 transactions by preconfirming the L1 transactions that contain them, we face a problem. Proposers would either have to preconfirm partially filled blob transactions at the end of the round or wait for another round to collect enough transactions to fill the blob.

One solution is to allow proposers to commit to a batch of L2 transactions without linking them to a specific L1 transaction. This would let the builder of the final full block aggregate the L2 transactions into one or more L1 blobs at the end of the slot.

### Issues with MEV-Boost

MR-MEV-Boost inherits the existing L1 MEV-Boost pipeline, which also means that we inherit many of MEV-Boost’s downsides, such as [reliance on a handful of relays and builders](https://arxiv.org/pdf/2305.19037). However, based rollups aim to inherit the security of L1, not to exceed it. Therefore, being “as bad as” L1 is the best we can do as a based solution.

# Future Direction

MR-MEV-Boost can be generalized as *partial-block preconfirmations*, where the proposer incrementally builds the block by committing to and publishing partial blocks during their slot.

One future direction would be to enshrine partial-block preconfirmations into the L1 protocol to achieve faster block times. This aligns with Vitalik’s [recent post](https://vitalik.eth.limo/general/2024/06/30/epochslot.html) and offers several benefits over off-protocol designs like MR-MEV-Boost:

- Removes “non-opted-in” proposers, enabling L1 preconfirmations and L1-L2 composability for all slots.
- Fully utilizes Ethereum’s validator set, potentially introducing lightweight PTC-like attestations for timely partial payload releases.
- Opens doors to increase the block times without degrading UX, which may help enable single-slot finality.

# Related Work

In his [latest post](https://dba.xyz/were-all-building-the-same-thing/), Jon Charbonneau explains in great detail how based rollups/preconfirmations work and the centralization risk of based preconfirmations.

Furthermore, partial-block preconfirmations are closely related to [inclusion list](https://ethresear.ch/t/how-much-can-we-constrain-builders-without-bringing-back-heavy-burdens-to-proposers/13808) research, as both can be viewed under the broader concept of “partial-block building,” where different parts of a block are constructed at different times by different entities. For example, the [MEV-Boost++ proposal](https://research.eigenlayer.xyz/t/mev-boost-liveness-first-relay-design/15) from Kyodo (EigenLayer) resembles MR-MEV-Boost, as both enable early commitment to partial blocks by imposing additional slashing conditions on the proposer.

# Conclusion

We introduce MR-MEV-Boost, a design that enables based preconfirmations by running multiple rounds of MEV-Boost auctions within a single slot. By inheriting the L1 PBS pipeline, MR-MEV-Boost mitigates many of the negative externalities of based preconfirmations while retaining the benefits of based rollups.

At [Nethermind Switchboard](https://switchboard.nethermind.io/), we actively research and tackle the open challenges of based preconfirmations. We are also collaborating closely with Taiko to develop [a PoC for based preconfirmations](https://github.com/NethermindEth/Taiko-Preconf-AVS/blob/6b21d85d329986a2a9725048e56be3a45d463dcc/Docs/design-doc.md) compatible with L2 PBS, including MR-MEV-Boost. Stay tuned for more updates!

## Replies

**murat** (2024-07-18):

Great post and suggested direction. It would be interesting to understand the implications of the multi round suggestion on L1 dynamics; for example a current top of block tx may become multiple smaller ToB txs as a result, rounds may fit smaller bundles of txs (like a TG bot bundle itself could be a single round), EIP-1559 fee market may have to be updated between the rounds (or not but this may create more blockspace pressure / higher fees) etc.

Improving these dynamics with some privacy measures where round blocks are private until a group of rounds are confirmed or something similar would be a great direction to further explore and can mitigate newly arising mev vectors.

---

**Evan-Kim2028** (2024-07-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/linoscope/48/13681_2.png) linoscope:

> ### Blob Efficiency
>
>
>
> So far, we have blurred the line between L1 and L2 preconfirmations. This is somewhat intentional, as L2 transactions are included within L1 transactions. However, there are cases where the difference becomes important.
>
>
> Consider a scenario where the L2 transactions within a round cannot fill an entire blob. If we only support preconfirmations for L2 transactions by preconfirming the L1 transactions that contain them, we face a problem. Proposers would either have to preconfirm partially filled blob transactions at the end of the round or wait for another round to collect enough transactions to fill the blob.
>
>
> One solution is to allow proposers to commit to a batch of L2 transactions without linking them to a specific L1 transaction. This would let the builder of the final full block aggregate the L2 transactions into one or more L1 blobs at the end of the slot.

are you suggesting that relays add a feature to aggregate the L2 transactions into blobs?

---

**linoscope** (2024-07-19):

Thanks for the comment! All good points.

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> It would be interesting to understand the implications of the multi round suggestion on L1 dynamics

I agree! Many interesting topics to consider like the ones you mention.

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> for example a current top of block tx may become multiple smaller ToB txs as a result,

Yes, I imagine we will have ToB for each of the partial blocks and that most cross-domain MEV, including CEX-DEX arbs, will be captured on top of partial blocks. This would greatly change the dynamics of how MEV is extracted as a result.

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> rounds may fit smaller bundles of txs (like a TG bot bundle itself could be a single round), EIP-1559 fee market may have to be updated between the rounds (or not but this may create more blockspace pressure / higher fees)

I think these depends on whether proposers would want to limit the size of each partial blocks. For instance, if proposers want only 20% of the block to consist of these preconfed partial blocks, it would make sense to introduce a fee mechanism similar to EIP-1559 that adjusts between rounds. I can’t think of a specific reason why proposers would want to do this off the top of my head, but there might be reasons I’m not considering.

![](https://ethresear.ch/user_avatar/ethresear.ch/murat/48/12986_2.png) murat:

> Improving these dynamics with some privacy measures where round blocks are private until a group of rounds are confirmed or something similar would be a great direction to further explore and can mitigate newly arising mev vectors.

Sounds interesting! Since these rounds are outside of the L1 protocol we do have more flexibility on expirementing with such things.

---

**linoscope** (2024-07-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/evan-kim2028/48/15875_2.png) Evan-Kim2028:

> are you suggesting that relays add a feature to aggregate the L2 transactions into blobs?

I was thinking that builders, particularly the builder of the final full block, will handle the aggregation. This would require the builder to provide the proposer with some proof or crypto-economic commitment when bidding, ensuring that the blobs in their block indeed contain the preconfirmed L2 transactions. Relays can also do the aggregation, but I think we want to keep their role as much as possible.

Furthermore, we might be able to utilize any general “blob sharing” services if builders provide them. The issue of not being able to pack a blob efficiently seems like a general problem, not limited to base rollups or preconfs, so there may be a more general solution that we can leverage.

