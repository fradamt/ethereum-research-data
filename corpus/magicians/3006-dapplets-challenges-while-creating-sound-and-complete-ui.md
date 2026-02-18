---
source: magicians
topic_id: 3006
title: "Dapplets: Challenges while creating \"sound and complete\" UI"
author: Ethernian
date: "2019-03-26"
category: Web > Wallets
tags: [wallet, ux, dapplets]
url: https://ethereum-magicians.org/t/dapplets-challenges-while-creating-sound-and-complete-ui/3006
views: 891
likes: 1
posts_count: 1
---

# Dapplets: Challenges while creating "sound and complete" UI

Today I had a brainstorming about ways to create a secure Wallet UI representing transactions in a “sound and complete” way. Where the “Sound UI” should prevent Views from rendering misleading representation, and the “Complete UI”  means an ability to define a “sound” View for any given type of data (pictures+text).

We came to conclusion, that existing Layout Managers implementation were built without “soundness” in mind: it is possible to supply specially prepared data, moving visual elements into invisibility at least partially (and without any notification for the user). Looks like the silent cropping of the visual representation is considered as not that bad.

Dear Wallet Devs: is the problem real? Do you use your own Layout Manager and Renderer to prevent misleading representations or you trust the usual one?
