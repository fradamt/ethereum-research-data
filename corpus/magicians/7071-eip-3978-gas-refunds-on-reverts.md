---
source: magicians
topic_id: 7071
title: "EIP-3978: Gas refunds on reverts"
author: k06a
date: "2021-09-16"
category: EIPs
tags: [gas, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-3978-gas-refunds-on-reverts/7071
views: 3072
likes: 4
posts_count: 6
---

# EIP-3978: Gas refunds on reverts

Let’s discuss this: https://github.com/ethereum/EIPs/pull/3978

## Replies

**poma** (2021-09-17):

Makes sense to count all SSTOREs as SLOADs if a transaction reverts since the storage is accessed but not modified.

---

**jessielesbian** (2021-09-22):

Good idea! I believe that this idea will reduce the cost of reverted transactions.

---

**k06a** (2021-09-22):

[@poma](/u/poma) I like the approach!

---

**k06a** (2021-12-29):

Anyone have experience in pushing EIPs right into upcoming hard forks?

---

**k06a** (2022-02-11):

Extended this EIP to other state-modifying operations: https://github.com/ethereum/EIPs/pull/4790

