---
source: ethresearch
topic_id: 14206
title: "Yet Another Three-layer Architecture: Base Layer <- Sidechain <- Rollup"
author: nanfengpo
date: "2022-11-15"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/yet-another-three-layer-architecture-base-layer-sidechain-rollup/14206
views: 2151
likes: 1
posts_count: 1
---

# Yet Another Three-layer Architecture: Base Layer <- Sidechain <- Rollup

# Layer 3

There are a lot of blockchain scalability solutions: sidechains, optimistic and zk rollups. They build up layer 2s with much lower gas than layer 1, but still not enough for high-throughput applications like games. Starkware came up with the concept of “layer 3” in their [blog](https://medium.com/starkware/fractal-scaling-from-l2-to-l3-7fe238ecfb4f), and later Vitalik compared possible [architectures](https://vitalik.ca/general/2022/09/17/layer_3.html) for layer 3. These architectures rely on a rollup-based layer 2 for security: rollups can inherit the full security of layer 1.

But rollups also have some intrinsic problems. Rollups store their compressed data and verify their state transitions on layer 1. So their performance is limited by layer 1 as an upper bound. Furthermore, each transaction running on the rollup finally requires a gas fee on layer 1 for data availability and proof verification. These problems hold back applications from using rollups to solve scalability problems. For example, the Axie game and dYdX DEX choose to launch their owner chains for scalability.

# Another Architecture

Let’s consider another three-layer architecture for applications. Its layer 2 is a sidechain connecting to layer 1 through bridges, and layer 3 is a bunch of rollups running on layer 2, aka `base layer <- sidechain <- rollup`. Based on this architecture, layer 2 gains asset variety from bridges and infinite scalability from rollups, providing a more friendly running environment for applications.

[![layer3 architecture](https://ethresear.ch/uploads/default/original/2X/1/16b0e03f240a2103e1a28bb4a94da8eba0311c86.png)layer3 architecture353×233 4.84 KB](https://ethresear.ch/uploads/default/16b0e03f240a2103e1a28bb4a94da8eba0311c86)

The tradeoff is that its security relies on layer 2 rather than layer 1. Think about a Polygon-like sidechain. The sidechain’s validators are responsible for generating blocks of layer 2, maintaining bridges to layer 1, and verifying data from layer 3. So the security of the entire system depends on the decentralization of layer 2.

# Advantages & Disadvantages

From the aspect of applications, one advantage of this architecture is that layer 1 gas fees are only paid for token transfers between layer 1 and layer 2, rather than every transaction on layer 2. It benefits high-throughput applications. Another advantage is that by building bridges to different layer 1 chains, asset variety on layer 2 and layer 3 can be improved.

From the aspect of security, the architecture shows lower security on layer 2 but higher security on layer 3. Compared to StarkNet’s `base layer <- rollup <- validium`, the sidechain-based layer 2 can not inherit the security of layer 1, but it can provide data availability to layer 3. We can also compare the architecture with `base layer <- data availability layer <- rollup` in Celestia. The sidechain-based layer 2 additionally provides execution environment on layer 2 which can enable more functionalities in the future, like cross-rollup transactions and zk-related precompiled contracts.

# Conclusion

The proposed `base layer <- sidechain <- rollup` architecture has the advantage of asset variety and infinite scalability, with the tradeoff of lower security on layer 2 but higher security on layer 3. It could be another choice to solve the scalability problems of web3 applications. Compared to expensive rollup-based layer 2s, it is more suitable for high-throughput applications like games.
