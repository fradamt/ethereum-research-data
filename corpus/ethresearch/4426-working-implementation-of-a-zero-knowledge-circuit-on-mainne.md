---
source: ethresearch
topic_id: 4426
title: Working implementation of a zero knowledge circuit on mainnet (Paper + code)
author: ArnSch
date: "2018-11-29"
category: Applications
tags: []
url: https://ethresear.ch/t/working-implementation-of-a-zero-knowledge-circuit-on-mainnet-paper-code/4426
views: 1549
likes: 4
posts_count: 1
---

# Working implementation of a zero knowledge circuit on mainnet (Paper + code)

Hi!

I’m part of the AZTEC protocol team, and I thought I’d share our working proof of concept zero knowledge circuit on mainnet, which was created by Dr Zac Williamson. It uses range proofs and homomorphic encryption to validate notes and transactions.

The main advancement compared to similar past effort is it’s efficiency, currently sitting at around 800’000 gas per validated proof on main net.

https://github.com/AztecProtocol/AZTEC

To demo, we’ve deployed a contract which creates confidential DAI.

Looking forward to questions and comments!
