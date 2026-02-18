---
source: ethresearch
topic_id: 15054
title: RISC-V for L2 state transition computation by Goshen
author: 0xDanRobins
date: "2023-03-15"
category: Layer 2
tags: []
url: https://ethresear.ch/t/risc-v-for-l2-state-transition-computation-by-goshen/15054
views: 929
likes: 0
posts_count: 1
---

# RISC-V for L2 state transition computation by Goshen

Hello, this is Dan from Goshen Network. We building an Optimistic rollup to scale transaction throughput with lower gas cost while maintaining decentralization and security from Ethereum.

The protocol uses a RISC-V machine to support on chain computing and in the event of challenges, it’s only necessary to identify “one step” in the RISC-V-Chain program to execute prune fraud state.

What makes us different from other optimistic rollups is that Goshen Network ensures simplicity and versatility with a layered architecture. At the bottom layer is a general-purpose computing environment for the L2, based on RISC-V, migrating L1 computations off-chain in a trustless manner. With this, L2 implements L1’s state transition logic, ensuring full compatibility with the L1 ecosystem. A reliable cross-layer message communication mechanism is further constructed to provide interoperability between L1 and L2 for building upper-layer applications such as a token bridge. For on-chain challenges, the interactive challenge protocol does not only reduce on-chain cost, but also improve the robustness of the protocol.

We’ve finished the 1st draft of Goshen’s whitepaper in August 2022. And for the past months, we’ve made some initials including (https://goshen.network/) website and the Bridge for L1-L2 transactions.

We are still working on the 4844 currently, but we think it’s the time to be here and hope to get more feedbacks from the Ethereum community.

If you are interested in working together with us, collaborating or giving suggestions, please do reach me via ([0xdanrobins@gmail.com](mailto:0xdanrobins@gmail.com)). Let’s build a better layer2 with better user experience and safety.
