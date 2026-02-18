---
source: ethresearch
topic_id: 15828
title: "Orbiter Cross Rollup Protocol: Optimistic For The Obedient Majority And Severe Arbitration For Malicious Minority"
author: ZeroKPunk
date: "2023-06-08"
category: Layer 2
tags: []
url: https://ethresear.ch/t/orbiter-cross-rollup-protocol-optimistic-for-the-obedient-majority-and-severe-arbitration-for-malicious-minority/15828
views: 1528
likes: 0
posts_count: 1
---

# Orbiter Cross Rollup Protocol: Optimistic For The Obedient Majority And Severe Arbitration For Malicious Minority

Hi, all! We are from [Orbiter Finance](https://www.orbiter.finance/), we are building a decentralized cross rollup bridge.

Vitalik had proposed a [Easy Decentralizd Cross-layer-2 Bridge](https://notes.ethereum.org/@vbuterin/cross_layer_2_bridges) , which described a very concise cross-chain bridge architecture based on rollup environment and largely inspired the design of the orbiter bridge.

The reason why we build **a Cross Rollup Bridge not a Cross Chain** Bridge is the same as [Vitalik’s points](https://old.reddit.com/r/ethereum/comments/rwojtk/ama_we_are_the_efs_research_team_pt_7_07_january/hrngyk8/).

In our design, we introduce maker as the LP provider of the destination domain, and zk spv based on the rollup mechanism, which can verify the validity of the specified Tx execution time, amount, and the terms of service bound by the maker. Cross-rollup transactions can be realized through these two roles, and the zk spv strictly restricts the behavior of the maker and punishes the evil behavior.

[![cross-rollup-flow](https://ethresear.ch/uploads/default/optimized/2X/d/dc2eacdaf75eb7854cf60475e7321cdcf096c8b5_2_553x500.png)cross-rollup-flow2472×2232 247 KB](https://ethresear.ch/uploads/default/dc2eacdaf75eb7854cf60475e7321cdcf096c8b5)

---

[![cross-tx-arbitration](https://ethresear.ch/uploads/default/optimized/2X/9/930364dfe9e0abf69a7c5456ef0b13def890da36_2_559x500.png)cross-tx-arbitration2766×2472 302 KB](https://ethresear.ch/uploads/default/930364dfe9e0abf69a7c5456ef0b13def890da36)

Recently, we released the yellow paper of our bridge, which contains detailed technical explanations. If you want to know more about it, go ahead for it !



      [github.com](https://github.com/Orbiter-Finance/papers/blob/main/yellowpaper/yellowpaper.pdf)



    https://github.com/Orbiter-Finance/papers/blob/main/yellowpaper/yellowpaper.pdf

###
