---
source: magicians
topic_id: 13152
title: "Draft EIP: Abstract Token Standard"
author: chriswalker
date: "2023-03-03"
category: EIPs
tags: [token, signatures, cross-chain]
url: https://ethereum-magicians.org/t/draft-eip-abstract-token-standard/13152
views: 1916
likes: 1
posts_count: 2
---

# Draft EIP: Abstract Token Standard

What if we could securely and freely mint tokens off-chain?

What if token holders could trustlessly migrate these tokens on-chain as desired?

What if token contracts included a built-in mechanism to move tokens between contracts or even between blockchains?

Abstract tokens define a simple, standard way to:

- Mint tokens off-chain as messages
- Reify tokens on-chain via smart contract
- Dereify tokens back into signed messages

Abstract tokens are free to mint off-chain but preserve on-chain composability. They are compatible with existing standards like ERC20, ERC721, and ERC1155, and are designed for high-volume use cases such as:

- airdrops
- POAPs / receipts
- identity / access credentials

Please check out the [EIP](https://github.com/ethereum/EIPs/pull/6604) or [Medium post.](https://medium.com/p/d4396465f233/edit) to see more. Feedback is welcome!

## Replies

**Kir_Os** (2023-03-19):

Sounds very promising! When will we be able to see all this in practice?

