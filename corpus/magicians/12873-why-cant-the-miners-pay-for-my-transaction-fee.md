---
source: magicians
topic_id: 12873
title: Why can't the miners pay for my transaction fee?
author: ERC20s
date: "2023-02-08"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/why-cant-the-miners-pay-for-my-transaction-fee/12873
views: 514
likes: 0
posts_count: 4
---

# Why can't the miners pay for my transaction fee?

Let’s say I only want to sell 2200 DAI for 1 ETH.

Let’s say that the transaction will give a miner $100 in profit via MEV.

Why can’t I just put 0 gwei and let the miner find the transaction, pay my gweis and take the profit from the top?

## Replies

**Alex-Klasma** (2023-02-08):

Already possible with some gas-less exchanges, like some 0x routes, CoW Swap, etc.

---

**matt** (2023-02-08):

To add on, since EIP-1559 started requiring txs to burn an amount of eth, it isn’t possible to move tx inclusion payment to another layer.

---

**ERC20s** (2023-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/erc20s/48/6820_2.png) ERC20s:

> Why can’t I just put 0 gwei and let the miner find the transaction, pay my gweis and take the profit from the top?

I guess I’m more just speculating on why this element isn’t implemented on the mainchain as a new EIP… I don’t see a downside for end-users…

It would make invaluable transactions like NFTs more expensive to transfer… And ERC20s more desirable…

