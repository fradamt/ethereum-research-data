---
source: magicians
topic_id: 473
title: "IDEA: allow contract addressing by ENS instead of conract address"
author: Ethernian
date: "2018-05-29"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/idea-allow-contract-addressing-by-ens-instead-of-conract-address/473
views: 1300
likes: 2
posts_count: 2
---

# IDEA: allow contract addressing by ENS instead of conract address

From [ether-router](https://github.com/PeterBorah/ether-router) manual:

> Allows you to have a contract with a stable address, but fully controllable and upgradeable behavior.

It looks like a nasty workaround for deeper problem in ethereum architecture, isn’t it?

Guys, we should stop use ethereum addresses as a public ids for mutable entities! We have ENS for that.

It should be possible to address a contract (or even contract+function callpoint) by ENS name.

I know, it requires low-level ENS integration into ethereum core and there are challenges here, but now I am asking you just about the idea.

Does it make sense?

What do you think?

## Replies

**Ethernian** (2019-03-23):

It were objections, that ENS lookup may be prohibitive high.

I would suggest to introduce a global ENS resolution cache for that updated by resolver.

