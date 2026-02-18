---
source: ethresearch
topic_id: 1829
title: Setup PoS private network
author: d00m178
date: "2018-04-25"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/setup-pos-private-network/1829
views: 1748
likes: 0
posts_count: 2
---

# Setup PoS private network

Hi.

We need to setup PoS private network with Caspeк protocol.

There are only couple links which uses this git repo: https://github.com/karlfloersch/docker-pyeth-dev

which contains already configured docker files with necessary files.

We have checked this variant and seems there are some issues with pyethapp client.

Probably because of pretty outdated sources from which it was built.

Is there some new versions or how to build it from scratch?

Please advice.

## Replies

**liangcc** (2018-04-26):

that’s a little bit outdated, and we are working on a new one. Meanwhile you can try playing with the harmony containers https://github.com/mkalinin/harmony-docker/tree/master/casper

