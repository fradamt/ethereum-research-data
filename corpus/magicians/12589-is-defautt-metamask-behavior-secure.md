---
source: magicians
topic_id: 12589
title: Is defautt Metamask behavior secure?
author: kladkogex
date: "2023-01-16"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/is-defautt-metamask-behavior-secure/12589
views: 497
likes: 3
posts_count: 2
---

# Is defautt Metamask behavior secure?

I found an interesting  thing about Metamask  recently

If you connect Metamask to a custom network node (say you have been using ETH mainnet and now you connect to a Goerllie node), Metamask  will immediately send all user’s public keys to this node by doing multiple eth_getBalance() queries , essentially deanonymizing all user keys and funds stored in Metamask on the Eth Mainnet

So if the user has 1000 keys in her wallet, Metamask will send all the keys to the node, the first time you connect to the network essentially fully deanomizing the user.

I wonder if wallets should behave like this.

## Replies

**xinbenlv** (2023-01-16):

1. That’s interesting. Love to join the conversation
2. Topic-wise, this seems to better fit in the MetaMask forum.
3. Product feature wise, it seems it’s better MetaMask ask user to confirm they trust the Custom Node they are connecting to. But this will be hard.

