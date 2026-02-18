---
source: magicians
topic_id: 15682
title: A seemingly minor Capella change is what enables current LST and Re-Staking
author: payoffmatrices
date: "2023-09-05"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/a-seemingly-minor-capella-change-is-what-enables-current-lst-and-re-staking/15682
views: 368
likes: 1
posts_count: 1
---

# A seemingly minor Capella change is what enables current LST and Re-Staking

Hi All, long-time Ethresear.cher, first time Magician here. I hit a wall on this issue and [@EvanVanNessEth](/u/evanvannesseth) suggested I make a thread here to discuss.

Earlier this year I was researching re-staking and trying to figure out how validators are able commit to smart contract rules (as in re-staking and LST) when they can just change their withdrawal address later. Then I learned that Capella made it so validators are no longer allowed to switch their withdrawal addresses. It was previously specc’ed under 0x00 that they could change it multiple times.

This change allowed a sort of “protocol-enforced proposer commitment” (if you will) where now validators can set their withdrawal address to a smart contract and, since they can’t change it, thereby ~credibly commit to following the rules of that contract as enforced by slashing. The earlier 0x00 standard, with changeable withdrawal address, meant validators could *not* effectively commit to obey those additional rules. The reason for this is that validators, once “committed”, **could rug the smart contract by changing their withdrawal address**, leaving the contract with nothing to slash.

From discussions I’ve had with EF and EF adjacent folks, some people already knew this but it also seems that many do not. I personally don’t have a strong opinion on this stuff yet but, unless I’m missing something, it seems like this change should be more widely discussed given the prominent issues of the day.

Some open questions I have:

1. Are there viable near-term approaches to validator decentralization that operate fine under 0x00? Per the experts I’ve spoken to, DVT works just fine under 0x00.
2. Are there other cryptographic tricks that could re-create this commitment even under 0x00? If so, then this change is not so interesting. I’ve seen a few that could do something in this direction but nothing very general.
