---
source: ethresearch
topic_id: 11398
title: Frontend - Smart Contract safe interconnectivity
author: polipic
date: "2021-12-01"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/frontend-smart-contract-safe-interconnectivity/11398
views: 1400
likes: 1
posts_count: 2
---

# Frontend - Smart Contract safe interconnectivity

Hello everyone,

There is one particular topic that cannot go out of my mind, hopefully some of you have good solutions.

The topic is about users interacting with Dapps. If you quickly think about the layers that lie between the user and the smart contract, you have the frontend (through react, angular etc…) a bridge provider and the wallet.

The problem that I see, is that we are not focusing enough on the frontend’s security. Most of the security’s efforts goes to the smart contracts (this is completely fine) but leaving off guard the user’s main contact interaction.

There has been multiple hacks because of this issue, we saw the sushi-swap: [SushiSwap’s token launchpad, MISO, hacked for $3M](https://cointelegraph.com/news/sushi-s-token-launchpad-miso-hacked-for-3m) and there are multiple web-site clones that imitate the exact look & feel of the original one.

There a couple of assumptions that we need to take in consideration to understand the gravity of this problem:

1. The majority of the users will not check the details of the transaction.
2. Front end code is likely to be vulnerable.
3. The source of truth for the users is what they see on the frontend.

Users today trust the brands more than the protocol, they do not audit the contracts, they care about good “brands” like uni swap, aave etc…

The problem with all of this, is that if  you have access to the frontend code, it becomes extremely easy to trick the user to deposit funds to another address.

There must be a way to guarantee that what you are signing is what you are “seeing”, most likely, this would be a job that the wallets would need to be a part of.

Anyway, if any of you are working in something related to this, I would be very interesting to fund it and cooperate.

## Replies

**MicahZoltu** (2021-12-02):

[Trustless Signing UI Protocol · Issue #719 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/719) is a proposed solution to this problem (from 2017) that just needs someone passionate about it to flesh out the design, clearly specify it, and advocate its adoption by wallets and dapps.

