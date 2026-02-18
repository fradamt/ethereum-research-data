---
source: ethresearch
topic_id: 12273
title: "Analyzing Ethereum Cryptoeconomics: the validator’s perspective"
author: umbnat92
date: "2022-03-28"
category: Economics
tags: []
url: https://ethresear.ch/t/analyzing-ethereum-cryptoeconomics-the-validator-s-perspective/12273
views: 1874
likes: 2
posts_count: 1
---

# Analyzing Ethereum Cryptoeconomics: the validator’s perspective

Big thanks to my colleagues at [Chorus One](https://chorus.one/about/) for their contributions to this report, especially to Felix Lutsch for his careful review of the content.

Below there is the abstract of the report, which you can find [here](https://docs.google.com/document/d/1r640UQOm2z-Q9nsJzqBq3BVgCtTL1_Yc7WnPp4jEBgk/edit?usp=sharing).

# Abstract

Ethereum’s Serenity upgrade aims to solve the scalability trilemma, which posits that there is an inherent tradeoff between scalability, security, and decentralization. This is not an easy task, and solving it comes with a bunch of challenges. Precisely, to guarantee the safety of the network, a complex consensus is needed, and accounting for all possible scenarios, by achieving the best outcomes in all of them, requires to state stringent rules. As the network is designed to survive several types of attacks, the complexity of the implemented reward and penalty mechanisms increases. Complexity, sometimes, means high exposure for validators. In this report, we summarize the Beacon Chain consensus protocol and associated reward and penalty mechanisms and take a look at how various scenarios may impact the APY and balance of a Beacon Chain validator.

We find that the expected annualized reward for an ideal validator is 5.44%. This decreases to 5.4% if we take into account a more realistic case. Furthermore, we investigate the impact on a validator that is caught making a slashable offense.
