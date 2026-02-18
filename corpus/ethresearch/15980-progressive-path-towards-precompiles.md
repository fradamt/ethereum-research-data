---
source: ethresearch
topic_id: 15980
title: Progressive path towards precompiles
author: xinbenlv
date: "2023-06-26"
category: Cryptography
tags: [precompile]
url: https://ethresear.ch/t/progressive-path-towards-precompiles/15980
views: 1198
likes: 3
posts_count: 2
---

# Progressive path towards precompiles

Hi research,

Hi, friends, we have an idea for your feedback:

Historically proposing a precompile contracts has been challenging due to chicken-and-egg problem: one has to convince the client’s willingness to build them before they can get more adoption, while lack of adoption reduces the convincingness that such precompile is necessary, mature and useful. DC([@dcposch](/u/dcposch) ) and I propose a middle ground and a progressive path towards precomile: Make it a non-precompile first, and then when widely adopted, move to petition it as precompile.

We like to seek your feedback on this idea on FEM [Progressive precompiles via CREATE2 shadowing - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/progressive-precompiles-via-create2-shadowing/14821)

(Cross-posting here because many precompiles are cryptography related and originated from discussions here)

## Replies

**dcposch** (2023-06-26):

Nice, thanks for posting.

Another goal of this proposal is to allow smooth deployment. We have many important EVM chains now, each of which will ship a precompile (or any EIP) at different times.

This proposal lets user contracts rely on a function everywhere. They just become more gas efficient once a given chain implements the precompile.

