---
source: magicians
topic_id: 12130
title: "EIP-6122: Forkid checks based on timestamps"
author: MariusVanDerWijden
date: "2022-12-13"
category: EIPs > EIPs networking
tags: []
url: https://ethereum-magicians.org/t/eip-6122-forkid-checks-based-on-timestamps/12130
views: 2013
likes: 1
posts_count: 2
---

# EIP-6122: Forkid checks based on timestamps

Discussion for EIP-6122

## Replies

**fjl** (2023-08-15):

I think there is a problem with the EIP when it comes to forks applied at genesis time. The forkID is supposed to uniquely identify the chain ruleset. So if there are two networks with the same genesis block, but different forks applied, the forkID should differ. This should be true even when all the forks are enabled at genesis time.

At the moment, the EIP says

> If a chain is configured to start with a non-Frontier ruleset already in its genesis, that is NOT considered a fork.

Some people interpreted this as a requirement to not write fork timestamps *before the genesis timestamp* into the CRC. But they really should be written. So I propose changing the EIP to remove that sentence.

