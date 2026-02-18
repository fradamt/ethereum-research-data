---
source: ethresearch
topic_id: 9912
title: How is Plasma Chain's security better than Side Chain's?
author: chrixp
date: "2021-06-23"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/how-is-plasma-chains-security-better-than-side-chains/9912
views: 1196
likes: 0
posts_count: 1
---

# How is Plasma Chain's security better than Side Chain's?

According to the [blockstream sidechain paper](https://blockstream.com/sidechains.pdf), blockheaders are published to the mainchain and users use SPV proof so that users can exit. According to [Vitalk’s Plasma paper](https://www.plasma.io/plasma.pdf), merkleized commitments are published on the mainchain and users use merkle proof on mainchain to exit. From my understanding, SPV Proof and merkle proof are the same.  Given that knowledge, isn’t the only thing valuable about Plasma’s security is their exit mechainism or am I missing something?
