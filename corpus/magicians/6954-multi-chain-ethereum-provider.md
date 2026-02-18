---
source: magicians
topic_id: 6954
title: Multi-chain Ethereum Provider
author: pedrouid
date: "2021-08-26"
category: Web > Wallets
tags: [evm, wallet, provider-ring, multi-chain]
url: https://ethereum-magicians.org/t/multi-chain-ethereum-provider/6954
views: 1603
likes: 10
posts_count: 2
---

# Multi-chain Ethereum Provider

EIP-1193 was a huge step for interoperability on Ethereum. Provider diversity exploded when EIP-1193 started being adopted and the line between integrating Metamask and WalletConnect became unnoticeable. Other providers followed and we saw many others showing up after. It also made possible for different developer libraries to exist like web3-react, Web3Modal and Blocknative’s onboard.js.

However this standard is explicitly designed for a single chain to be connected to which makes it very rigid and cumbersome in the current accelerating pace of L2 adoption and other EVM chains

In my opinion, there is a need for a new standard for Multi-Chain Ethereum Provider that is able to interface with multiple chains simultaneously therefore a wallet can expose accounts for different chains simultaneously as well. Additionally this would require that each JSON-RPC request is also targeted at a specific chainId.

EIP-1193 has already built much of the ground work for a new provider standard to exist and the existence of a Multi-Chain Ethereum Provider could easily eliminate for users to switch chains on their wallet based on dapp requirements

I would love to include in this discussion all the wallet providers but also javascript library developers.

cc [@greg](/u/greg) [@ricmoo](/u/ricmoo) [@danfinlay](/u/danfinlay) [@rekmarks](/u/rekmarks) [@NoahZinsmeister](/u/noahzinsmeister) [@lukasschor](/u/lukasschor) [@itamarl](/u/itamarl) [@brunobar79](/u/brunobar79)

## Replies

**greg** (2021-08-26):

I’m on mobile and not really thinking it totally through but Why not just extend the base 1193 to incorporate the addChain method included in metamask across every other wallets.

You could just emit something like `requestChangeNetwork`

The only thing that might be frustrating is managing multiple providers but perhaps I’m over thinking how wallets manage them.

