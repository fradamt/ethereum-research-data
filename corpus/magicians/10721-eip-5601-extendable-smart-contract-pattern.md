---
source: magicians
topic_id: 10721
title: EIP-5601 Extendable smart contract pattern
author: 0xpApaSmURf
date: "2022-09-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5601-extendable-smart-contract-pattern/10721
views: 539
likes: 2
posts_count: 2
---

# EIP-5601 Extendable smart contract pattern

This thread is for discussion of the Extendable smart contract pattern as described in this EIP: [Add EIP-5601: The Extendable Pattern by 0xpApaSmURf · Pull Request #5601 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5601)

It introduces a flexible, modular, method for smart contract development and management allowing upgradeability and future-proof smart contracts.

More documentation can be found here: [Introduction - Extendable Contract Pattern](https://violet-co.gitbook.io/extendable-contract-pattern/)

There has been a lot of prior work on proxy patterns and upgradeability patterns, but there needs to be some greater sophistication in the way we handle this to support the growing number of use-cases and their heightened complexity.

## Replies

**SamWilsn** (2022-09-20):

Have you checked out the Diamond pattern? It seems to solve similar problems.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-2535)





###



Create modular smart contract systems that can be extended after deployment.

