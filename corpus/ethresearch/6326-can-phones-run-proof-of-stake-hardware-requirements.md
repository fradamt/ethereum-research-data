---
source: ethresearch
topic_id: 6326
title: Can Phones run proof of stake? Hardware requirements?
author: Econymous
date: "2019-10-14"
category: Layer 2
tags: []
url: https://ethresear.ch/t/can-phones-run-proof-of-stake-hardware-requirements/6326
views: 1201
likes: 1
posts_count: 3
---

# Can Phones run proof of stake? Hardware requirements?

Are phones enough hardware to run a proof of stake sidechain off of the ethereum mainchain?

## Replies

**lacker** (2019-10-17):

I’m not sure whether you are talking about the eth2 proof-of-stake or some other proof of stake sidechain algorithm. But in general, it doesn’t seem like a good idea to run proof-of-stake algorithms on a phone. Proof-of-stake requires that you be persistently online, and both iOS and Android phone operating systems are designed so that applications cannot generally rely on being running persistently. The operating system will kill processes that are backgrounded, and if it kills the app that is running proof of stake, you’ll lose money.

I think hardware capability is less of an issue than the general persistence of phone apps.

---

**Econymous** (2019-10-18):

Thank you so much. Yeah I meant POS in general.

This is great to know.

The only immediate patch i could think of is having a bundle of phones operate as the same node or something for redundancy.

Good stuff though. Love it. Thanks!

Simple answers compound with elegant solutions

