---
source: magicians
topic_id: 2948
title: DevP2P modular layer stack proposal
author: ferranbt
date: "2019-03-20"
category: Working Groups > Ethereum 1.x Ring
tags: []
url: https://ethereum-magicians.org/t/devp2p-modular-layer-stack-proposal/2948
views: 733
likes: 3
posts_count: 1
---

# DevP2P modular layer stack proposal

https://github.com/ethereum/devp2p/issues/71

I made a proposal for a new devp2p stack. This approach follows the abstraction layers model where each layer of the stack is independent from each other. Each layer provides a transparent input without any specific format. An example of this approach would be the TCP layer. Many applications with different logic like SSH, FTP or TLS are built on top TCP without much friction.

Right now, the devp2p stack provides applications with a fixed message format  (code, message). This limits the functionality the protocols can have. This proposal provides a transparent interface for the applications so that they can build any type of communication mechanism they find suitable for each use case. This would make it easy to build new protocols and iterate fast on their design.
