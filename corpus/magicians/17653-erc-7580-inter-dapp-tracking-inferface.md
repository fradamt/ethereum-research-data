---
source: magicians
topic_id: 17653
title: "ERC-7580: Inter dapp tracking inferface"
author: wartstone
date: "2023-12-26"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7580-inter-dapp-tracking-inferface/17653
views: 1262
likes: 0
posts_count: 3
---

# ERC-7580: Inter dapp tracking inferface

Discussion for [Add ERC: Inter dapp tracking inferface by wartstone · Pull Request #165 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/165).

This proposal aims to establish an inter-dapp tracking standard inferface for dapp interactions and support for more complicated business logics.

## Replies

**wartstone** (2023-12-26):

Imaging we have two roles here: promotion/ads business role and projects role who adopted the promotion service. And project contracts implemented the interface listed in the erc.

Currently the routine would go something like this:

1. projects get a seed id (hash) from promotion side
2. before the target promotion action starts, project contracts called the interface ‘onTrackStart(id, contract_address, function_hash)’
3. after the target promotion action ends, project contracts called the inferface ‘onTrackEnd(id, contract_address, function_hash)’
4. promotion contract collect the project action info and distribute the rewards back to projects

any interesting idea are welcome

---

**wartstone** (2024-01-18):

We’re ready to publish an example usage contract next if there’s no problems. could be exciting

