---
source: ethresearch
topic_id: 20160
title: Rollup-Centric Considerations of Based Preconfimations
author: CeciliaZ030
date: "2024-07-27"
category: Layer 2
tags: [preconfirmations]
url: https://ethresear.ch/t/rollup-centric-considerations-of-based-preconfimations/20160
views: 1728
likes: 8
posts_count: 1
---

# Rollup-Centric Considerations of Based Preconfimations

*Special thanks to [Brecht Devos](https://x.com/Brechtpd), [Lin Oshitani](https://twitter.com/linoscope), [Conor McMenamin](https://twitter.com/ConorMcMenamin9), [Jonas Bostoen](https://medium.com/@jonas.bostoen), [Christian Matt](https://twitter.com/ccpamatt) for the reviews ![:tada:](https://ethresear.ch/images/emoji/facebook_messenger/tada.png?v=14)*

TLDR;

This article presents [Gwyneth](https://x.com/gwyneth_taiko) from the [Taiko Labs](https://x.com/taikoxyz).  We outline the Taiko chain setup, discuss the profitability and timeliness of L2 block building, and explore how implementations of preconfirmations can configure blocktime and more efficient data publishing. We also address the issue of nondeterministic proposals caused by multiple preconfirmers through leader election, which affect UX for builders and users. The designs in this article are subject to change.

## Background: The Simplest Taiko Chain

At present, Taiko Labs is subsidizing block production by running proposers, effectively burning ETH to maintain a fast and inexpensive network. With that in mind, our effort on preconfirmations needs to be expedited, as we aim to facilitate profitable block building in the community without compromising security and throughput. This is the basic setup of the Taiko chain:

[![Untitled (4)](https://ethresear.ch/uploads/default/optimized/3X/f/1/f196c6e6be939ac54173b7e6802df9776c2728b6_2_517x294.png)Untitled (4)2063×1178 155 KB](https://ethresear.ch/uploads/default/f196c6e6be939ac54173b7e6802df9776c2728b6)

- Decentralized proposers run their taiko-geth to sync with the L2 mempool.
- When a batch of Tx constitutes a profitable block, the rational proposer submits this block to L1.

The profitable criteria is the total tip collected from all Tx plus their MEV covers the costs to interact with L1 and prover:
Screen Shot 2024-07-05 at 12.54.04 PM1764×128 12.5 KB

Taiko smart contract on L1 contains the decentralized ledger of L2 Tx batches. These batches will, inevitably, contain invalid Tx with vanilla proposing strategy, since the sequencing is not coordinated. For example:

- L2-75 has a Tx transferring 100 ETH from Alice to Bob without Alice’s correct signature
- L2-76 and 77 both contain a Tx from Cassy with nonce equaling 9;

In such cases,  [taiko-client](https://github.com/taikoxyz/taiko-mono/tree/ec6c179967b9ac93cd967ff3a1fe8b331fdb8256/packages/taiko-client), similar to Ethereum’s consensus client, will witness the invalid Txs from the L1 ledger and exclude them from the actual block being synced to L2.

Back to L2, each [taiko-client](https://github.com/taikoxyz/taiko-mono/tree/ec6c179967b9ac93cd967ff3a1fe8b331fdb8256/packages/taiko-client) (fork of Ethereum’s consensus client), witnesses the L1 ledger and applies a deterministic rule that invalidates the above Txs. Subsequently, the client can form a correct batch constituting the next block and construct the blockhash.

This blockhash is considered finalized when a prover submits proof of the execution of valid Txs, as well as the exclusion of invalid Txs from the state of the ledger.

As Vitalik noted, a based rollup can be a [“total anarchy”](https://vitalik.eth.limo/general/2021/01/05/rollup.html) amid the chaos, but it remains functional as long as the decentralized ledger persists and the L2 network maintains synchronization. Taiko will continue to progress by inheriting **L1 security and finality**. However, proposers may still encounter challenges, resulting in a **liveness** issue due to lack of profitability.

## Challenges and Solutions

### Profitability & Timing Game in L2 Block Building

In the diagram below proposer Alice observes L2-75 upon confirming L1-100, and she creates L2-76 with blockhash 0xabc. Proposer Bob, attempting the same, causes a fork with an alternate blockhash 0xf3c. Both submit proposals to L1-100 and pay the current L1 transaction fee. However, since Alice’s transactions were incorporated first, Bob’s transaction reverts due to L1_UNEXPECTED_PARENT(), causing Bob to lose his proposing fee. Alice successfully earns the tip and MEV of L2-76, but she still needs to compensate the prover to validate her block afterward.

[![Untitled (5)](https://ethresear.ch/uploads/default/optimized/3X/c/8/c8a72e51d5473fb6e20d1824d69e4a3baf4c6921_2_517x303.png)Untitled (5)2425×1422 124 KB](https://ethresear.ch/uploads/default/c8a72e51d5473fb6e20d1824d69e4a3baf4c6921)

An L2 block is proposed to the rollup Contract as a raw transaction batch. Consequently, each node subscribing to the event derives the blockhash in their own execution clients. Despite this, the **rollup state is finalized when the proposal is confirmed on L1 because block hash derivation is deterministic.** We still need a proof to validate the block hash to rollup’s L1 ledger, enabling light clients to fetch the states and users to perform withdrawals. Hence, real-time proving solutions such as SGX are important because they enforce L2 state finality with high probability. Let’s recall:

[![Screen Shot 2024-07-05 at 12.54.04 PM](https://ethresear.ch/uploads/default/optimized/3X/2/6/261274c74370de26d6ec593f649377533be6ea83_2_690x50.png)Screen Shot 2024-07-05 at 12.54.04 PM1764×128 12.5 KB](https://ethresear.ch/uploads/default/261274c74370de26d6ec593f649377533be6ea83)

Solving for MEV is a knapsack problem - the larger the knapsack, the more value extracted. It’s been well-studied that L1 proposers will play [the timing game](https://ethresear.ch/t/timing-games-implications-and-possible-mitigations/17612) to extend the MEV solving window as much as possible; the same logics apply to L2. Even worse, because L2 users typically tip much lower in an ecosystem with significantly less liquidity, the current 12s block time on Taiko is far less than enough for anyone to profit, which results in a **liveness issue for decentralized proposing**. This is why Taiko Labs operates an unprofitable proposer to sustain the 12s block time. Without taking measures, the L2 blocktime would be arbitrarily long if rational proposers play the timing game.

[![Untitled (6)](https://ethresear.ch/uploads/default/optimized/3X/9/e/9ea87c99a3e43e4879c1d6de369b3bb71d885276_2_495x375.png)Untitled (6)2226×1682 174 KB](https://ethresear.ch/uploads/default/9ea87c99a3e43e4879c1d6de369b3bb71d885276)

### Solving Blocktime & Data Publishing with Preconfirmations

Essentially, we’re facing a conflict in a **UX property of L2 (blocktime) versus decentralized block building**. In centralized L2, timeliness is easily managed by the centralized sequencer, while on L1, the beacon attestation enforces the time to publish the execution payload. Thus, we observe that timeliness must be enforced by some mechanism other than builders in the game. Whoever facilitates preconfirmations could also mandate blocktime.

**A preconfirmer can periodically issue preconfirmations to builders for smaller sequenced batches, then batch publish the batches to reduce the data publishing costs.** The periodic issuance of batches now constitutes L2 blocks. The L2 protocol, which allows the preconfirmer to opt in, can facilitate timeliness by ensuring preconfirmed blocks are released every T second. Now, we define **T as the L2 blocktime**, which can be adjusted faster to improve user experience.

[![Untitled (7)](https://ethresear.ch/uploads/default/optimized/3X/d/2/d204bb354780b7e25543312984493e2f719d2f72_2_690x387.png)Untitled (7)3296×1849 500 KB](https://ethresear.ch/uploads/default/d204bb354780b7e25543312984493e2f719d2f72)

Regarding data publishing, Taiko currently publishes all encoded L2 transaction lists in blobs. This requires the proposer to cover the L1 gas fee for a whole blob regardless how much data is actually necessary, further reducing the block’s profitability. In Gwyneth, preconfirmations will allow for **more batching of L2 blocks into blobs** if the preconfirmer is assigned multiple L1 slots, which also implies the separation of sequencing commitment and data availability:

- Preconfirmations Issuance ⇒ commit L2 sequencing
- Preconfirmations Delivery ⇒ data publishing to L1

Now we can characterize the L1 preconfirmer as the de facto L2 proposer, and the existing decentralized sequencer who submits batches as L2 builders - we just migrate the PBS architecture to L2. Moreover, this L2 PBS mechanism can use a similar pipeline as on L1, because the L2 proposer is exactly an L1 validator who runs something like [MEV-boost](https://github.com/flashbots/mev-boost.git) with a preconfirmation add-on. The new fee model functions as follows:

[![Screen Shot 2024-07-11 at 2.46.47 AM (1)](https://ethresear.ch/uploads/default/optimized/3X/c/7/c7f1262f29380aea940d4c5152693be272949797_2_460x212.png)Screen Shot 2024-07-11 at 2.46.47 AM (1)744×344 14.4 KB](https://ethresear.ch/uploads/default/c7f1262f29380aea940d4c5152693be272949797)

For clarification, L2 proposers are the preconfirmers who opt into the Gwyneth protocol to propose L2 blocks, and the preconfrmers are the L1 validators who can issue preconfirmations.

![Screen Shot 2024-07-11 at 2.47.22 AM (1)](https://ethresear.ch/uploads/default/original/3X/f/0/f01ebd831084ad709d4805fe4ff1b83327b3ce73.png)

Overall, preconfirmations enable Gwyneth blocks to be built in short and steady intervals by decentralized participants, while not compromising profitability. A deficiency of liveness caused by lacking liquidity on L2 will not jeopardize blocktime; in other words, users can always enjoy fast transaction confirmation. It also provides a clear model for L2 MEV compatible with the existing PBS pipeline.

### Decentralized Block Proposing with PBS

We have discussed how preconfirmation benefits L2 proposers. Now, let’s consider **proposal inclusion** from the perspective of L1 validators.

Initially, we have a distinct group of L2 participants who compete to propose the next L2 batch by calling the `ProposeBlock` function in the Taiko smart contract. Their proposal transactions with encoded L2 batches are exposed in the public mempool, and L1 validators or builders will choose to include these proposals. Apparently, t**he L1 parties can easily capture the transactions, stealing the L2 tip and MEV when producing the L1 block.** We’re revisiting the PBS playbook. Rollup with permissionless sequencing can implement similar mechanisms to mitigate block stealing.

[![Untitled (8)](https://ethresear.ch/uploads/default/optimized/3X/d/1/d17ee918d3b13e915483a110c04c22af49e6fe0e_2_517x260.png)Untitled (8)1406×709 77.2 KB](https://ethresear.ch/uploads/default/d17ee918d3b13e915483a110c04c22af49e6fe0e)

However, there’s no need for mitigation following the [definition](https://ethresear.ch/t/based-preconfirmations/17353) of base rollup:

> A rollup is said to be based, or L1-sequenced, when its sequencing is driven by the base L1.

In other words, all L2 proposers are L1 validators. Given access to both mempools, a builder can incorporate L2 batches in her L1 bundles, which is by far the most **efficient paradigm for Gwyneth block-building**

[![Untitled (9)](https://ethresear.ch/uploads/default/optimized/3X/6/8/68eae50a088bf3c631d1fb23e52d49855f0a0ad5_2_517x249.png)Untitled (9)1406×679 53.4 KB](https://ethresear.ch/uploads/default/68eae50a088bf3c631d1fb23e52d49855f0a0ad5)

Recall also in PBS, validators have a choice to build the block natively without using [MEV-boost](https://github.com/flashbots/mev-boost.git) connecting to external builders. The L1 validator, who’s also an L2 proposer, can issue consecutive preconfirmations to self-produce L2 blocks until her slot to propose. In this case, we may also omit the separate role of builders, and rewrite the fee model for L2 proposers:

[![Screen Shot 2024-07-11 at 2.46.17 AM](https://ethresear.ch/uploads/default/optimized/3X/1/2/1291f379205c49d484fda26e97169d2671738cdd_2_517x90.png)Screen Shot 2024-07-11 at 2.46.17 AM916×160 7.55 KB](https://ethresear.ch/uploads/default/1291f379205c49d484fda26e97169d2671738cdd)

With the inclusion model much simplified, we note that the L1 validator who includes the L2 proposal is the deterministic proposer of L2. Given Taiko’s current 12s blocktime, there is a one-to-one correspondence between each L1 and L2 block, hence the state of the chain at any slot is deterministic.

### Nondeterministic Proposer and Leader Election

Now, as we decouple the L1-to-L2 block correspondence with preconfirmation, we argue that **nondeterminism is also introduced because, during the L1 epoch, multiple preconfirmers exist to perform sequencing concurrently.**

[![Untitled (10)](https://ethresear.ch/uploads/default/optimized/3X/b/2/b24f24e1ef4885e714897d2f95d25f8c1f2582fb_2_660x500.jpeg)Untitled (10)1920×1454 164 KB](https://ethresear.ch/uploads/default/b24f24e1ef4885e714897d2f95d25f8c1f2582fb)

If these preconfirmers are the subset of L2 proposers who produce blocks natively, everyone will start building on top of the latest finalized parent. This continues until the set of preconfirmations is settled, updating the head of the chain. Then, a proposer will restart with the new head and **abandon their local ledger, resulting in previous preconfirmed transactions being reverted upon delivery**. If the proposer does not restart and proposes the local fork with data publishing during their slot, **that proposal will also revert**. In such a case, the L2 will miss a slot to update; users will experience the **chain halting** until the next proposer comes on board. The malfunctioning proposer might be slashed depending on the protocol implementation.

Considering builders in the PBS setting, who can send their sequenced batches to all L2 proposers in the current epoch, **the head of the chain will appear nondeterministic** to them, as all proposers will endorse different forks simultaneously. However, only the next-in-line proposer holds the source of truth, since her ledger will be settled first. **Therefore, a rational builder should request preconfirmation only from the next-in-line proposer**. Nonetheless, the protocol cannot prevent a malicious proposer from forcing his fork proposal through a regular transaction on Ethereum.

There are two possible solutions: 1)  **define the ledger held by the next-in-line proposer as canonical, which yields a leader selection protocol;** 2) disable block proposals at the non-preconfirmed L1 slots, then fork proposals will likely be excluded by a rational next-in-line preconfirmer. The latter solution is sub-optimal because we still want to preserve the option of non-preconfirmed block proposals unless there are enough preconfirmers to achieve our desirable liveness.

#### On Leader Election

In a decentralized setting at anytime, **only one L1 validator should have exclusive write access to the L2 state**, even if all opt-in participants can issue preconfirmations. **Such systems are inherently finalized without any external finality gadget**.

[![Untitled (11)](https://ethresear.ch/uploads/default/optimized/3X/2/3/23c6258764b5d1c0ec9df8be0a3db5b6cd2132a8_2_690x231.png)Untitled (11)4029×1350 410 KB](https://ethresear.ch/uploads/default/23c6258764b5d1c0ec9df8be0a3db5b6cd2132a8)

On the other hand, an L2 builder who’s building the latest Gwyneth chain can only write to preconfirmed L1 block space from the next opt-in validator. Requesting preconfirmations from others is strictly prohibited because that creates a gap in the slot.

[![Untitled (12)](https://ethresear.ch/uploads/default/optimized/3X/3/d/3d2b9b203eda188c0ebc6520cdb249d14b114b14_2_690x251.png)Untitled (12)3699×1350 407 KB](https://ethresear.ch/uploads/default/3d2b9b203eda188c0ebc6520cdb249d14b114b14)

Essentially, we create a just-in-time market for exchanging L1/L2 block space. Instead of a JIT auction, Some suggest using [execution tickets](https://ethresear.ch/t/execution-tickets/17944) for an ahead-of-time auction, which means in the diagram above, the L1-104 proposer can sell L2-79 block space simultaneously while the L1-102 proposer sells L2-78. This establishes a one-to-one correspondence between L1/L2 slots in a more controlled manner, and since it allows all participants to buy and sell these rights, an ahead-of-time auction aligns better with the preconfirmation market. From the L2 perspective, the protocol’s sale of execution tickets can imply new fee models for value-capturing. [XGA-style preconfirmations](https://ethresear.ch/t/preconfirmations-on-splitting-the-block-mev-boost-compatibility-and-relays/19837) can be a good implementation.

## Summary

Taiko started as a rollup with decentralized proposers, with a protocol that deterministically derives L2 state as long as the ledger is finalized on L1. We realized that based sequencing, which unites L1 and L2 proposers, transforms our framework into something more simple and powerfull. Based sequencing will work, naively, with finality and security inherited from L1.

Based sequencing may not work, in practice, considering builder profitability, bootstrapping liveness, and the configuration of fast blocktime. We discuss preconfirmations to tackle these challenges with some tweaks on timeliness and proposal mechanisms. However, having multiple validators who issue preconfirmations can cause the concurrent building of L2 forks. This introduces nondeterminism for the spectators of chains including builders, exchanges, and users, although fortunately, nondeterministic sequencing does not affect finality - **most obstacles in based sequencing relate to essential UX properties for builders and users.**

Despite some controversy, leader election could be a practical middle-ground solution. We anticipate a significant number of L1 proposers opting in as preconfirmations gain adoption. Consequently, **proposer decentralization still remains close to the (at least theoretically) maximal achievable decentralization offered by a vanilla based rollup.**

[![Untitled (13)](https://ethresear.ch/uploads/default/optimized/3X/4/0/40dd31cbef98940c5ba5f843d943f08e9ab8a7e2_2_690x339.png)Untitled (13)4131×2034 354 KB](https://ethresear.ch/uploads/default/40dd31cbef98940c5ba5f843d943f08e9ab8a7e2)
