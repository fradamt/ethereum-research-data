---
source: magicians
topic_id: 23789
title: "EIP-7935: Set default gas limit to 60M"
author: sophia
date: "2025-04-23"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7935-set-default-gas-limit-to-60m/23789
views: 325
likes: 4
posts_count: 3
---

# EIP-7935: Set default gas limit to 60M

EL client devs should test higher gas limits, recommend a new one that is safe, and update their default configs to use this value with their Fusaka releases.


      ![image](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7935)





###



Recommend a new gas limit value for Fusaka and update execution layer client default configs

## Replies

**MicahZoltu** (2025-05-04):

This EIP needs an actual gas limit proposal set before it can be usefully discussed.  At the moment it is basically just a placeholder saying “we should do something” without actually specifying what should be done.

The discussion is wildly different if this proposal is suggesting changing the default to 36M vs 1B and without an actual gas limit proposal everyone will just be straw manning each other and productive conversation will be extremely difficult.

---

**MicahZoltu** (2025-05-08):

This EIP should include mention of the effects that increased block sizes will have on all users of Ethereum, not only validators/builders.  I believe RPC nodes handle the vast majority of the work that Ethereum clients do, and they are arguably the most important nodes on the network as it is what roots trust of the system on end-users, yet this EIP nor most of the discussion around gas limit increases talks at all about how gas limit increases will affect those nodes.  Archive nodes should also be discussed and analyzed as well.

