---
source: ethresearch
topic_id: 15636
title: MEV for “Based Rollup”
author: sthwnd
date: "2023-05-18"
category: Economics
tags: [mev, zk-roll-up, layer-2]
url: https://ethresear.ch/t/mev-for-based-rollup/15636
views: 11961
likes: 4
posts_count: 3
---

# MEV for “Based Rollup”

**TLDR**

- We describe the L2 MEV mechanism for a Based Rollup. MEV naturally partially flows to Ethereum, strengthening L1 economic security and allowing searchers to extract cross-domain MEV.

*Special thanks to Justin Drake, Mike Neuder, and Toni Wahrstätter for great chat, valuable insights and review, and to Matthew Finestone and Brecht Devos for review, feedback, and discussions.*

### Introduction

A Based Rollup “outsources” sequencing to L1, inheriting the liveness guarantees of L1, the decentralization of the L1, and naturally reusing L1 searcher-builder-proposer infrastructure.

*Disclaimer: this approach was first described in [Vitalik’s article](https://vitalik.ca/general/2021/01/05/rollup.html#who-can-submit-a-batch) as a “Total Anarchy” rollup in early 2021, and in March 2023 Justin Drake wrote how this could work in practice with [“Based Rollups”](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016/11).*

### Brief protocol design overview

- Taiko is an Ethereum-equivalent (Type 1) ZK-EVM. That is, it makes no changes to the Ethereum spec;
- Both builders and provers are permissionless: anyone can start and stop running a proposing and proving node whenever they wish;
- Builder determines the transaction order in the L2 block and submits a transaction directly to Ethereum. The order of blocks on Ethereum (L1) is determined by the Ethereum node building that block;
- A block is finalized after it was successfully proposed. The prover has no impact on how the block is executed and what the post-block state is;

*Check the [Github repository](https://github.com/taikoxyz/taiko-mono) and [this article](https://taiko.mirror.xyz/y_47kIOL5kavvBmG0zVujD2TRztMZt-xgM5d4oqp4_Y) for a more detailed protocol design description.*

### L2 MEV flow mechanism

- L2 searchers collect L2 transactions into bundles and send them to L2 block builders;
- L2 block builders take these bundles and build a block. L2 block builders can run the mev-boost that L1 builders use;
- L2 block builder can also be an L1 searcher and include L2 blocks into L1 bundles on its own;
- L1 builders will include L2 blocks into their L1 blocks as long as there is at least a tiny of piece of MEV in this block (and the gas limit is not reached). And as long as there are any DEXs deployed on L2, there always will be some MEV additionally to transaction fees;
- Blocks from L2 go to L1 through Private Order Flow. Otherwise, MEV might be stolen;
- If a searcher monitors the Ethereum mempool, the Based Rollup mempool, and the state of both chains, it can build bundles with cross-chain Based Rollup <> Ethereum MEV. Cross-chain MEV can also be extracted between Based Rollups (e.g. between two Taiko L2s).

[![](https://ethresear.ch/uploads/default/optimized/2X/5/585377b175c203db0d8cf2673730608f156ffa83_2_690x382.png)1096×608 50 KB](https://ethresear.ch/uploads/default/585377b175c203db0d8cf2673730608f156ffa83)

### What if multiple L3s, L4s, etc.

The same structure works for L3, L4, etc. Based Rollup can be seamlessly deployed on a Based Rollup multiple times (scaling both vertically and horizontally).

In this case, each layer will have a mempool with searchers and builders (that can run mev-boost). And the block from layer n will land in the mempool on layer n - 1.

### Feedback is highly appreciated

Given that the L2 MEV design area is pretty new, we research and experiment with various design options and appreciate any feedback and questions about our current solution. Please join our research, and share ideas and feedback about the L2 MEV area, Based Rollups MEV mechanics, and anything related.

## Replies

**fewwwww** (2023-05-19):

It’s great to see more research on Based Rollup!

For the L3 and L4 scenarios you mentioned.

- Is the use of Based Rollup more difficult compared to L2, e.g. extra latency and excessive extra workload?
- L3 and L4 will probably mostly use Validium’s DA model, which is probably a Weakly-trusted “Rollup” in general, is it necessary to use Based Rollup?

---

**sthwnd** (2023-05-22):

Thank you for your questions!

Regarding the latency, block time for a Based Rollup equals to the Ethereum block time. Regarding excessive extra workload, from the L1 perspective, there is no much extra work.

And speaking about L3s, L4s – the solutions here depend on who deploy them and with what goal. Formally, they can do whatever they want. But Validium model is not obligatory for sure: if L2 posts Data Availability to L1, and L3 posts Data Availability to L2, then L3’s DA is guaranteed by L1.

In general, one considers using validium is Ethereum is assumed to be the scalability bottleneck. But it is not related to a specific type of rollup.

