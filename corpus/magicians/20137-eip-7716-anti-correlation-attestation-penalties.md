---
source: magicians
topic_id: 20137
title: "EIP-7716: Anti-correlation attestation penalties"
author: Nerolation
date: "2024-05-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7716-anti-correlation-attestation-penalties/20137
views: 882
likes: 2
posts_count: 1
---

# EIP-7716: Anti-correlation attestation penalties

[EIP-7716: Anti-correlation attestation penalties](https://github.com/ethereum/EIPs/pull/8598)

- Adjust penalties for missed attestations based on in-slot correlation of missed attestation

The rational behind this EIP is the following:

- Economics of scale come with correlations

no matter if running many validators from the same node, in the same country, on servers of the same cloud providers, the same ISP provider, the same client, etc.

Economies of scale make it harder for solo stakers to compete with large node operators.
With in-protocol incentives that foster diversivication, decentralization (and increased fault-tolerance thorugh, e.g. DVTs), the protocol can become more decentralized/credible neutral/censorship resistant.
Escaping high-correlations comes with costs (moving nodes into a diverse set of geo locations, using different cloud providers, setting up a fault-tolerant DVT cluster, etc).
Based on [prior analysis](https://ethresear.ch/t/analysis-on-correlated-attestation-penalties/19244), the impact on large centralized parties is negative while small-scale participants (e.g. solo stakers or rocketpool node operators) benefit.

**More content on the EIP [here](https://github.com/dapplion/anti-correlation-penalties-faq) (EthBerlin hackathon project)**:

[![penalty_factor_chart](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a4f4959d338c31570bbd19ebb8e7897ff526143a_2_690x259.png)penalty_factor_chart1854×698 28.5 KB](https://ethereum-magicians.org/uploads/default/a4f4959d338c31570bbd19ebb8e7897ff526143a)

**Find the EIP here:**


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7716)





###



Adjust penalties for missed attestations based on in-slot correlation of missed attestation
