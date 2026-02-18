---
source: ethresearch
topic_id: 6263
title: Formalizing and improving eth2's approach toward finalization of invalid shard blocks
author: vbuterin
date: "2019-10-09"
category: Sharding
tags: []
url: https://ethresear.ch/t/formalizing-and-improving-eth2s-approach-toward-finalization-of-invalid-shard-blocks/6263
views: 5888
likes: 3
posts_count: 16
---

# Formalizing and improving eth2's approach toward finalization of invalid shard blocks

*This post requires understanding the general approach of publishing a Merkle root of erasure-coded data and having clients randomly sample Merkle branches to sample-check availability of the data, described [here](https://arxiv.org/abs/1809.09044) and [here](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding).*

### Describing the status quo

Currently, the de facto philosophy of eth2 is that, much like for non-sharded chains, the canonical chain is defined as the *fully valid and available* chain that scores highest on the fork choice rule. In the non-sharded case, the “fully valid and available” criterion is trivial: full nodes just check it automatically. In the sharded case, however, nodes cannot check validity and availability directly, because “fully valid and available” includes shard chain data (ie. crosslinks) and there is too much shard chain data to check. Instead, nodes rely on a series of heuristics:

- If 2/3 of a randomly sampled shard committee does not support a particular crosslink, then it cannot be included in the first place
- If a node sees a fraud proof showing how a given crosslink is invalid, it rejects it
- A node can run a data availability sampling check (see https://arxiv.org/abs/1809.09044) on any crosslink before accepting its legitimacy

These heuristics are imperfect. Hence, while in an abstract definitional sense the canonical chain is *defined* as being available and valid, it’s possible that some nodes will wrongly believe that some block B is the head, because they do not realize that some crosslink in B's history points to unavailable or invalid data. However, we expect the combination of heuristics to be highly robust in practice.

Note that fraud proofs are a *retroactive* heuristic: you may believe that some block B is valid, but then you see a fraud proof and after that point block B becomes invalid. In general, fraud proofs should be broadcasted quickly. However, in the worst worst case, where multiple security assumptions fail at the same time (there is an attacking majority in a crosslink AND there is a network latency of >6 minutes that affects fraud proofs but somehow NOT legitimate blocks), there’s a risk that an invalid block will get “finalized”, and then become “de-finalized” after the fact.

In this extreme case, because of Casper FFG’s rules, the validators that voted on the finalized block will not be able to vote on the new “correct” chain, and so they will lose a large portion of their balances until the inactivity leak leads to a minority finalizing the new correct chain. Arguably, this is okay; if a disaster happens, then whoever was responsible for the mistake should be penalized, even if their mistake was simply not trying hard enough to stay connected to fraud proof providers, or not running heuristics that stop making finalizing votes if network latency is too high. But there is also a “friendlier” approach.

### Layer 1 optimistic rollup

Consider a chain architecture that works as follows. The canonical chain is defined as being the *fully available and valid beacon chain pointing to fully available shard blocks* that scores highest on the fork choice rule. That is, there are availability and validity requirements on the beacon chain, but there are only availability requirements on the data pointed to by the crosslinks; as long as the crosslink root actually is a Merkle root of data that is all available and of the right length, including that crosslink does not compromise a chain’s validity.

We use a [STARKed merkle root](https://ethresear.ch/t/stark-proving-low-degree-ness-of-a-data-availability-root-some-analysis/6214) as a data availability proof mechanism. When a block is published, we can use the crosslink roots included in the block to compute a combined root of all crosslinks included in that block. We can then add a reward for someone to submit an erasure-coded extension of this Merkle root along with a STARK proving that the extended Merkle root is correct.

This proof may take minutes to produce; hence we allow and expect validators to at first build on top of some block B “optimistically” without verifying data availability, and only expect and require data availability validation when validators make blocks that treat B as *justified* in the Casper FFG vote, as it’s treating an invalid block as justified that is potentially very risky.

If a shard chain block with available data but “bad” contents (eg. wrong post-state root) gets included in a beacon chain, then this does not invalidate the chain. Instead, we add a mechanism where a fraud proof can be included in the beacon chain later, and *inside the chain* this rewinds that shard chain block and all shard chain blocks that depend on it. Validator-related state does not get rewound; shard state roots do. A chain can rewind a maximum of 2 days; after 2 days, a bad state root included in a chain and not removed really does make that chain invalid. This allows validators to deposit (move shard state -> beacon chain state) with only a 2 day waiting period.

In this construction, the heuristics needed to “fully validate” the chain are much lighter:

- Fully validating the beacon chain
- Data availability check on crosslinks via random sampling
- Watching out for fraud proofs with a 2 day synchrony assumption

Note that the STARKed data availability root is required for this construction to work. [Coded Merkle trees](https://eprint.iacr.org/2019/1139) or the [original 2D scheme](https://arxiv.org/abs/1809.09044) are not acceptable, as in the case where an erasure coded root is fraudulent, different validators may durably disagree regarding whether or not it is valid. If an erasure coded root is correctly constructed, then any one client successfully validating availability implies that >\frac{1}{2} of the data is available, which implies that the rest of the data can be recovered and so every other client’s availability checks will soon pass. But if an erasure coded root is incorrectly constructed, then some validators may see the errors and others may not see the errors, leading to a chain split. To avoid these issues, we need a STARKed data availability root to remove the possibility of incorrectly constructed data availability roots.

## Replies

**dankrad** (2019-10-11):

I agree that the status quo seems extremely harsh, especially given that it may not be the validators fault to not have seen the fraud proof (none might have been produced or a network split has occurred). I would say the proposal to increase this to two days would be very welcome, and I also like that it leads to continuity of the beacon chain.

> Note that the STARKed data availability root is required for this construction to work. Coded Merkle trees  or the original 2D scheme  are not acceptable, as in the case where an erasure coded root is fraudulent, different validators may durably disagree regarding whether or not it is valid.

I don’t quite understand this part: Surely this is also a problem in the status quo, where exactly does the new proposal differ so that this is now a fatal problem?

---

**vbuterin** (2019-10-13):

> I don’t quite understand this part: Surely this is also a problem in the status quo, where exactly does the new proposal differ so that this is now a fatal problem?

In the status quo, showing that a shard chain block is invalid (including erasure coding fraud) is sufficient to revert the chain. In this new scheme, it is not. And if erasure coding of a block is incorrect, we no longer have a synchrony-independent guarantee of consensus over whether or not it is valid.

---

**denett** (2019-10-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> But if an erasure coded root is incorrectly constructed, then some validators may see the errors and others may not see the errors, leading to a chain split.

Is this true? A validator could easily check if it is possible to reconstruct the erasure coded root using the reconstructed data. Two validators might reconstruct different block data, but would both conclude that the erasure coded root is invalid. If this is the case, the block is available, but invalid.

---

**vbuterin** (2019-10-17):

But the validators would not see the whole data, they would each just see a small slice that they sample for.

---

**denett** (2019-10-17):

I assumed that the validators that were assigned to a shard actually had to download the block data of their shard and validate whether the transactions in the block are valid.

Otherwise the honest shard nodes could reconstruct the block data and could prove that the erasure coding is incorrect. Just like they do when a block contains an invalid transaction or state root. They might need a STARK to proof the invalidity of the erasure coding, but then we only need to create a STARK when the block proposer is misbehaving.

---

**vbuterin** (2019-10-18):

> I assumed that the validators that were assigned to a shard actually had to download the block data of their shard and validate whether the transactions in the block are valid.

They do! But they don’t have to download all the other shards’ full data.

> Otherwise the honest shard nodes could reconstruct the block data and could prove that the erasure coding is incorrect.

The problem is that this approach is fraud-proof-dependent and so breaks down under high network latency. A big goal of this exercise is to make eth2 less network-latency-dependent.

---

**denett** (2019-10-18):

Maybe I am still missing a part of the puzzle, but isn’t it possible to also use the proof that the erasure coding is invalid in the Layer 1 optimistic rollup approach you describe above?

So the light-client-validators only have to check for data availability and can wait for 2 days for fraud-proofs. Fraud-proofs for invalid transactions, invalid state root and invalid erasure coding.

After the data availability sampling, the light-client-validators can trust that an honest shard node can either reconstruct the data or build an erasure coding fraud-proof. When a block is invalid they are able to roll it back within 2 days.

When we are using the STARK to proof the validity of the erasure coding, the light-client-validators will find out sooner that the erasure coding is correct, but still have to wait for fraud proofs to know that the block is actually valid. That does not seem to add much to the security.

---

**adlerjohn** (2019-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> isn’t it possible to also use the proof that the erasure coding is invalid in the Layer 1 optimistic rollup approach

Yes, that general approach is exactly what’s described [here](https://ethresear.ch/t/on-chain-non-interactive-data-availability-proofs/5715): exposing the ability to do data availability proofs (which need to be done as part of consensus for Eth 2.0!) through an FFI function, and having consensus on that. Useful for [optimistic rollups](https://ethresear.ch/t/minimal-viable-merged-consensus/5617).

---

**adiasg** (2019-10-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Instead, we add a mechanism where a fraud proof can be included in the beacon chain later, and inside the chain this rewinds that shard chain block and all shard chain blocks that depend on it.

In order to maintain consistency of the system, all blocks in other shards that have received cross-shard transactions dependent on the invalid block would also have to be reverted. Instead of handling all instances of this catastrophic failure within the protocol itself (and in this specific way), it would be more suitable to resolve these on the social level and on a case-by-case basis. Thoughts?

---

**vbuterin** (2019-10-25):

A single committee failure being able to force a social recovery seems like a bad idea; it basically means that the “cost of triggering a governance event” is only a few thousand ETH rather than a large chunk of the entire validator set. Also, case-by-case reversion could easily get into highly subjective judgements that affect specific people’s interests adversarially.

I think we can make EEs that try to replay original block data and get as many transactions as possible through.

---

**colingplatt** (2019-11-05):

Perhaps I’m missing something very obvious here, but imagine a situation where I make an outgoing transaction to another party in shard A, and a transaction from that other party is made in shard B to me.

Sometime between the confirmation of those transactions in their respective shards, someone submits a fraud proof for shard A which rewinds my transaction in shard A, but not the transaction in shard B. My transaction in shard A cannot be replayed.

As a result I have both the asset in shard B, and now the asset in shard A again. How would we protect against this?

---

**adiasg** (2019-11-06):

Atomic exchanges across shards remain a yet-unsolved problem (AFAIK). The expected workflow for this is to have both assets on a single shard, and have a contract to facilitate the exchange.

---

**colingplatt** (2019-11-06):

Thanks for that, I had understood something similar.

In a scenario where my transaction flow first yanked asset (abc) from my control Shard A to my control in Shard B, then an atomic swap occurred in Shard B a few moments later (I send abc, I receive def), and then Shard A was rewound (a few minutes later), reverting my transaction to myself for abc from Shard A > Shard B. Wouldn’t we arrive at the same outcome?

---

**adiasg** (2019-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Instead, we add a mechanism where a fraud proof can be included in the beacon chain later, and inside the chain this rewinds that shard chain block and all shard chain blocks that depend on it.

All blocks that have a dependency on the fraudulent block (including blocks in other shards) should be reverted, so that no footprint of the fraudulent block exists anywhere in the sharded system. So in your example, Shard B would be reverted appropriately to avoid the highlighted problematic situation.

---

**denett** (2019-11-06):

All transactions in Shard B that depend on a rolled back cross-link from Shard A have to be rolled back as well, so this could lead to a lot of rolling back. The optimistic rollup does not roll back all blocks in Shard B, but a rollback decision is made on a per transaction basis, keeping as many valid transactions as possible. Cross-links to other shards might be rolled back as well, so ultimately all shards could be affected.

How do we untangle this web? In new blocks, all shards have to publish their rolled back cross-links?

