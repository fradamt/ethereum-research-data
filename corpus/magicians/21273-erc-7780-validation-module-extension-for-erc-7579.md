---
source: magicians
topic_id: 21273
title: "ERC-7780: Validation Module Extension for ERC-7579"
author: kopykat
date: "2024-10-05"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7780-validation-module-extension-for-erc-7579/21273
views: 70
likes: 0
posts_count: 1
---

# ERC-7780: Validation Module Extension for ERC-7579

Discussions for [Add ERC: Validation Module Extension for ERC-7579 by kopy-kat · Pull Request #666 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/666)

This proposal introduces three new module types on top of the existing modules described in ERC-7579. The modules are policy, signer and stateless validator. None of these modules are required to be implemented by accounts, but accounts can choose to implement them or other modules can choose to make use of them for additional composability.
