---
source: ethresearch
topic_id: 6548
title: Any platforms that do validator selection using pre-committed hash chains?
author: Byzant
date: "2019-12-01"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/any-platforms-that-do-validator-selection-using-pre-committed-hash-chains/6548
views: 1105
likes: 0
posts_count: 1
---

# Any platforms that do validator selection using pre-committed hash chains?

Has this mechanism for selecting validators been proposed and/or implemented in any distributed ledgers?

Validators pre-commit hash chains of length w. When creating a block, validators commit the pre-image to the current hash in their hash chain, and combines it with the random number Selector, hash(x) ⊕ Selector. This random number selects the next validator.

[![selectvalidator](https://ethresear.ch/uploads/default/optimized/2X/3/3eee5ea7b464b255c2b324b6ccb84bc3584a0d33_2_690x391.jpeg)selectvalidator2630×1494 144 KB](https://ethresear.ch/uploads/default/3eee5ea7b464b255c2b324b6ccb84bc3584a0d33)
