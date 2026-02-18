---
source: magicians
topic_id: 7053
title: Native flash minting
author: jessielesbian
date: "2021-09-13"
category: EIPs
tags: [evm, opcodes]
url: https://ethereum-magicians.org/t/native-flash-minting/7053
views: 1222
likes: 0
posts_count: 2
---

# Native flash minting

Native flash minting allows ETH, the native cryptocurrency of Ethereum, to be flash minted. Native flash minting addresses the gas intensity of other alternatives like wrapped Ethereum flash loans and allows flash minting past the normal Ethereum total supply.

Native flash minting will introduce 2 new EVM instructions: `FLASHMINT (0xb3)` and `FLASHBURN (0xb4)`. The `FLASHMINT` EVM instruction would increase the debt counter and mint ETH to the current account, while the `FLASHBURN` instruction would decrease the debt counter and burn ETH from the current account. If the smart contract call returns with a non-zero debt counter, `FLASHMINT` running into a balance overflow, or if the amount being burned by `FLASHBURN` exceeds the debt counter and/or the account balance, the EVM will revert the execution.

Native flash minting saves gas by not having to call other smart contracts for flash loans, which can make capital-free arbitrage in decentralized finance more profitable.

[I got the idea from here](https://blog.openzeppelin.com/flash-mintable-asset-backed-tokens/)

## Replies

**axic** (2021-09-13):

Your main motivation seems to be gas savings. Have you checked what is the flash minting/burning cost of [WETH10](https://github.com/WETH10/WETH10) and how much that affects such arbitrage opportunities? Is the main bottleneck the adoption rate (it does not seem to be adopted) of WETH10?

The odds are not in the favour of introducing new opcodes which address specific use cases, when those use cases can be well addressed on upper layers. There can be of course exceptions, but a somwhat similar proposal (to have an ERC20-compatible native Eth wrapper in the system) has not been adopted for years.

