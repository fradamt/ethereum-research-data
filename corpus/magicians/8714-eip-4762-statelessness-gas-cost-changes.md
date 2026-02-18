---
source: magicians
topic_id: 8714
title: "EIP-4762: Statelessness gas cost changes"
author: dankrad
date: "2022-03-25"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-4762-statelessness-gas-cost-changes/8714
views: 2094
likes: 2
posts_count: 4
---

# EIP-4762: Statelessness gas cost changes

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/4762)














####


      `master` ← `dankrad:verkle-gas-cost`




          opened 09:31PM - 03 Feb 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/c/cc63c5d10a473c2079ea4ee24ce896c0942d6825.jpeg)
            dankrad](https://github.com/dankrad)



          [+308
            -0](https://github.com/ethereum/EIPs/pull/4762/files)







This EIP introduces changes in the gas schedule to reflect the costs of creating[…](https://github.com/ethereum/EIPs/pull/4762) a witness. It requires clients to update their database layout to match this, so as to avoid potential DoS attacks.

## Replies

**Zoltan** (2024-09-18):

Those gas charges will be valid for accessing EOF data section too?

---

**ihagopian** (2024-10-05):

Some weeks ago, I drafted changes around 4762 (and other EIPs) regarding EOF.

https://github.com/jsign/EIPs/pull/2/files

---

**gballet** (2025-01-30):

they will, as the data section will be stored in the tree and appear in the witnesses

