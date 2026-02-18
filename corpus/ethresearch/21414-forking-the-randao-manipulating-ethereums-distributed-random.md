---
source: ethresearch
topic_id: 21414
title: "Forking the RANDAO: Manipulating Ethereum's Distributed Randomness Beacon"
author: seresistvanandras
date: "2025-01-10"
category: Consensus
tags: [random-number-generator]
url: https://ethresear.ch/t/forking-the-randao-manipulating-ethereums-distributed-randomness-beacon/21414
views: 725
likes: 5
posts_count: 1
---

# Forking the RANDAO: Manipulating Ethereum's Distributed Randomness Beacon

*TL,DR:* In our latest paper, we analyse the manipulability of RANDAO, Ethereum’s distributed randomness beacon (DRB) protocol. Before our work, the only known manipulation strategy was selfish mixing. Toni wrote a [nice ethresear.ch post](https://ethresear.ch/t/selfish-mixing-and-randao-manipulation/16081) about it.

In our work, we identify a new class of manipulation strategies that a RANDAO manipulator can employ: forking the blockchain. In the paper, we show that the forking strategy combined with selfish mixing yields the most powerful RANDAO manipulation strategy.

E-print: https://eprint.iacr.org/2025/037.pdf

Github: [GitHub - nagyabi/forking_randao_manipulation: Researching RANDAO manipulation in Ethereum mainnet.](https://github.com/nagyabi/forking_randao_manipulation)

We refer to the paper or [this Twitter thread](https://x.com/Istvan_A_Seres/status/1877648087277047931) for the gory technical details.

[![image](https://ethresear.ch/uploads/default/original/3X/3/8/387c8819b7435fba8b6932fd886455e6ed8d418d.png)image707×534 28.7 KB](https://ethresear.ch/uploads/default/387c8819b7435fba8b6932fd886455e6ed8d418d)

Here, we only include open research questions and some food for thought.

**Short-term countermeasures**

The community could apply various short-term countermeasures to counter forking attacks, though none of these mitigations solve entirely the issue of RANDAO’s biasability.

1. Making the epochs longer. Longer epochs decrease the manipulative power of the tail slots.
2. Decrease proposer boost. A decreased proposer boost would require higher stakes to pull off our identified RANDAO forking manipulations.
3. Single-slot finality or other shorter finality mechanisms would also make longer forkings impossible.

**Long-term countermeasures**

The end goal must be an unbiasable distributed randomness protocol that is scalable and efficient at Ethereum’s scale.

1. Dishonest majority setting: verifiable delay functions are required as a recent paper has shown that delay functions are necessary for dishonest-majority coin-flipping
2. Honest majority setting: since Ethereum (and Bitcoin) already operates in the honest majority setting, maybe could be content with other unbiasable DRB constructions, e.g., weighted threshold VRFs.

(The ideal conservative, long-term solution should also be post-quantum secure)

**Open research directions**

- Analysing the game-theoretical properties of a RANDAO bribery market. The idea is that validators could auction off their manipulative power to bribers. This market could be implemented trustlessly using smart contracts.
- Studying RANDAO manipulation in a model incorporating MEV, i.e., block rewards and transaction fees are not uniformly distributed.
- We did not cover all possible forking attacks. Evaluating them would allow us to claim a little higher RANDAO manipulation percentages.
- Is there any other manipulation strategy a RANDAO manipulator validator could use? Perhaps manipulating the sync committees?

Any feedback, comments, or questions are welcome!
