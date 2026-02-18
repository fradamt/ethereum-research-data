---
source: magicians
topic_id: 3630
title: Window.ethereum.disable() for logging out of provider
author: miguelmota
date: "2019-09-06"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/window-ethereum-disable-for-logging-out-of-provider/3630
views: 5398
likes: 4
posts_count: 4
---

# Window.ethereum.disable() for logging out of provider

Currently web3 providers offer an `.enable()` method for allowing the dapp to connect but there doesn’t exist a method to disconnect. Standardizing around a `.disable()` method on the provider would allow dapps to display a logout button if this disable method is available. This would be beneficial for providers that offer standard login experiences like Portis, Squarelink, Authereum, etc. and as a dapp developer you don’t have to think about how to handle logging out for each provider. I believe web3connect does something similar with a [.close()](https://github.com/web3connect/web3connect/blob/97595c3d4ce6ccc5fb5788230a0723ab6e9e8bd9/example/src/App.tsx#L339) method on the provider.

What are your thoughts on standardizing around an optional `.disable()` method on the provider for disconnecting and logging users out of the provider on the dapp?

## Replies

**wighawag** (2019-09-18):

Hi [@miguelmota](/u/miguelmota)

I agree this would be useful. I actually proposed the same thing to be added to 1102 :  [EIP-1102: Opt-in provider access](https://ethereum-magicians.org/t/eip-1102-opt-in-provider-access/414/59)

---

**EvilJordan** (2020-06-24):

Following up here… Obviously `disable()` hasn’t yet made it to the library, but are there any proven methods to disconnect?

If not… how does one disconnect for testing purposes? I don’t see anything in the local browser indicating `ethereum` is “active”.

---

**NellalinkHQ** (2020-09-22):

We kindly await this feature

