---
source: magicians
topic_id: 20551
title: Supporting EIP-3085 with a ERC-4337 wallet
author: ajhodges
date: "2024-07-15"
category: Magicians > Primordial Soup
tags: [wallet, json-rpc, eip-4337]
url: https://ethereum-magicians.org/t/supporting-eip-3085-with-a-erc-4337-wallet/20551
views: 387
likes: 1
posts_count: 4
---

# Supporting EIP-3085 with a ERC-4337 wallet

There is currently a gap in the interface between dapps and ERC-4337 wallets; support for network addition via [EIP-3085 wallet_addEthereumChain](https://eips.ethereum.org/EIPS/eip-3085). In order for a 4337 wallet to function with an arbitrary chain, it needs to be provided with an RPC URL that can serve the [4337-specific RPC methods](https://eips.ethereum.org/EIPS/eip-4337#rpc-methods-eth-namespace).

I see a few potential paths forward here:

1. Reuse EIP-3085 EthereumChainAddRequest.rpcUrls by leveraging the fact that a dapp can already provide multiple RPC providers with the existing interface

We could specify the ordering of these URLs, i.e. the first one is always the bundler, and subsequent ones are always general-purpose RPCs
2. We could define a prefix to be added the bundler URL so that the wallet can identify it

Standardize around a single RPC URL - the RPC provider passed via 3085 should handle both traditional as well as 4337-specific RPC methods

- Some bundlers such as Alchemy already work in this way. Others (i.e. Pimlico) expressly do not.
- Dapps may need to build a JSON RPC reverse proxy depending on their bundler provider.

Extend EIP-3085 `EthereumChainAddRequest`

1. Add an rpcMetadata mapping of RPC URLs to metadata (maybe a dictionary with e.g. "supports4337": true)
2. Add a bundlerRpcUrls parameter

I would love to hear from anyone else who is already thinking about this!

## Replies

**spencerstock** (2024-07-15):

Nice ideas.I like 1 and 3, slight lean towards 1.

It may be a can of worms from a security perspective, given that the bundler can act maliciously and attack users who send userOps to them. When a wallet saves a malicious bundler it would use that bundler for all future userOps across all dapps.

One angle to consider because of the security benefits would be to have bundlers expose a method for adding arbitrary ethereum chains. This would more closely mirror the risk profile of today’s implementation. Not saying this is the way forward, just an angle to discuss.

---

**darion** (2024-08-15):

Are bundlers uniquely dangerous compared to a normal RPC node that broadcasts transactions?

---

**dror** (2024-08-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/spencerstock/48/12779_2.png) spencerstock:

> It may be a can of worms from a security perspective, given that the bundler can act maliciously and attack users who send userOps to them

A bundler can’t attack a user, more than a node can attack: it can’t modify the UserOp in any way. The only thing it can do is (just like a node) to drop the UserOp, and thus performs a denial-of-service.

In such case, the user should switch to a more reputable bundler.

A bundler is intended to be an extension api to a node. It is a separate RPC since (by design) erc-4337 doesn’t require any change to existing nodes.

A bundler can support the entire RPC calls range, but it would require it to proxy all non-4337 requests to a real node, which might be a burden. We defined only the eth_chainId as a required duplicate RPC call, to determine the bundler is for the right chain.

Reporting bundlers in the “urls” list might be good, though the app should be able to detect which URLS support which API.

possible suggestion is to mark a bundler by appending `#erc4337` at the end of the url.

