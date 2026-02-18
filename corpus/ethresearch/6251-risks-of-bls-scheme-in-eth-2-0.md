---
source: ethresearch
topic_id: 6251
title: Risks of BLS scheme in eth 2.0
author: kaibakker
date: "2019-10-06"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/risks-of-bls-scheme-in-eth-2-0/6251
views: 1332
likes: 1
posts_count: 3
---

# Risks of BLS scheme in eth 2.0

Hi everyone,

I am not a BLS expert. But this scheme seems to be pretty new and therefore could potentially contain bugs and exploits. Is there a way to recover from potential exploits in phase 0? How is security guarenteed?

## Replies

**kladkogex** (2019-10-18):

You a totally correct. BLS is based on pairing security which is way less studied than algs based on Diffie-Hellman problem or RSA.

We all have to live with it for a while …

---

**kaibakker** (2019-10-21):

If BLS is exploited, an attacker could potentially steal funds in the beacon contract. Is that the risk you take as an early staker? Is there a bounty for finding an exploit between now and phase 0 launch?

