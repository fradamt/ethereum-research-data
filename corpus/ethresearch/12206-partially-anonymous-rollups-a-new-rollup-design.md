---
source: ethresearch
topic_id: 12206
title: Partially anonymous rollups - a new rollup design
author: OlivierBBB
date: "2022-03-14"
category: Layer 2
tags: [zk-roll-up, rollup]
url: https://ethresear.ch/t/partially-anonymous-rollups-a-new-rollup-design/12206
views: 2684
likes: 9
posts_count: 1
---

# Partially anonymous rollups - a new rollup design

*Olivier Bégassat, Alexandre Belling, Nicolas Liochon*

Hi all, this note contains a specification for a rollup design with anonymity and scalability properties halfway between (transparent) rollups and [(fully anonymous) zk-rollups](https://ethresear.ch/t/account-based-anonymous-rollup/6657). It can have full data availability (both for users and operators), leaks relatively little user information on chain (account activity is leaked through updated account state hashes but transaction details are opaque to anyone but the relevant parties). Operators know what they are doing and are auditable (whence the “partially anonymous” tag.) The rollup state has bounded size (two depth 32 sparse Merkle trees) and can fully hold in memory.

We would greatly appreciate any feedback you may have!

[partially_anonymous_rollups_with_encryption.pdf](/uploads/short-url/AsrhWaVycPPWpwGIL39KWybtTem.pdf) (371.1 KB)
