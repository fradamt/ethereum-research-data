---
source: magicians
topic_id: 19632
title: "EIP-7684: Return deposits for distinct credentials"
author: dapplion
date: "2024-04-12"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7684-return-deposits-for-distinct-credentials/19632
views: 1144
likes: 1
posts_count: 2
---

# EIP-7684: Return deposits for distinct credentials

Discussion thread for EIP-7684

https://github.com/ethereum/EIPs/pull/8408

## Replies

**etan-status** (2024-05-05):

- How relevant is this still with EIP-4788 exposing to the EL whether a validator has correct credentials before releasing the 31 ETH from the staking pool (see rocket pool scrub check)? With EIP-6110 the delay is only ~12 minutes before deposit credentials are locked (on finality). With EIP-7688 the smart contract verifying the beacon root proof could further made forward compatible. That way it could be make sure that the 31 ETH transaction is only valid on branches that have the correct withdrawal credential.
- How quickly could someone fill up the deposit contract slots (2^32) with instant withdrawals becoming a thing here? Or is the penalty large enough to make it too costly?
- How would this EIP interact if a top up happens while a validator is switching between withdrawal credential types (0x00 → 0x01 capella, or 0x01 → 0x02 consolidation)?
- EIP-6110 as is introduces race between the old-style deposits and the new-style deposit receipts during the Electra transition period, btw.

