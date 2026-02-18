---
source: ethresearch
topic_id: 1016
title: Guaranteed collation subsidies
author: JustinDrake
date: "2018-02-07"
category: Sharding
tags: []
url: https://ethresear.ch/t/guaranteed-collation-subsidies/1016
views: 1812
likes: 0
posts_count: 3
---

# Guaranteed collation subsidies

Miners in the main shard can grief validators in a child shard by censoring collation headers, i.e. not allowing them to be added to the VMC. (The period is only 5 blocks. The [loose periods](https://ethresear.ch/t/loose-sharding-periods/864) proposal only slightly mitigates the attack.)

Missing the period is costly for individual validators, and this can be used as leverage by miners to extort validators for profit (blackmail) or discourage them from participation. My proposal is to reward validators collation subsidies (not transaction fees) even if they miss adding a collation header in their period.

Site note: I got this idea to address the collation body withdrawal attack in [this scheme to separate proposers and validators](https://ethresear.ch/t/separating-proposing-and-confirmation-of-collations/1000/6). Effectively a backup empty collation is pushed at every period by default, and there is no data availability problem for this backup collation.)

## Replies

**vbuterin** (2018-02-07):

> Effectively a backup empty collation is pushed at every period by default

Pushed on top of what parent?

---

**JustinDrake** (2018-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Pushed on top of what parent?

Pushed on top of *all* collations (including other implicit backup collations) previously pushed to the VMC for the corresponding shard.

