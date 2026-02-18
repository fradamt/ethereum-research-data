---
source: magicians
topic_id: 5752
title: Gas Subsidy for low gas transactions
author: MaestroKongrio
date: "2021-03-18"
category: Magicians > Primordial Soup
tags: [gas]
url: https://ethereum-magicians.org/t/gas-subsidy-for-low-gas-transactions/5752
views: 536
likes: 0
posts_count: 2
---

# Gas Subsidy for low gas transactions

An idea come to my mind, and I was instructed to discuss here before proceed with EIP or such stuff… maybe someone has the same idea before…

It’s no secret that gas cost are making Ethereum a network for riches and whales. With fees over USD 10 for just an Ether transfer, network is becoming unpayable for many users. It’s always possible to send a low gas price tx and wait until network process it, but right now you can wait almost forever and your tx may not be processed.

Like governments collect taxes from riches to help poors (in theory), my idea is to collect some sort of tax from higher gas price transactions, to help fund lower gas prices ones. The idea isn’t fully ready, but the main points are:

1. We know whats the gas price for every transaction in a block. So, we can apply a certain tax to the higher gas price txs. Just as an example, lets says we tax the 20% higher prices tx with a 10% fee. Let’s call this “the poor people gas pool”
2. The miner who process the block, add a new item to it: a hash of the content of his mempool of pending txs (Merkle Trees already solve this issue).
3. To get funds from the pool, a user can make a request. A score can be computed from the gas cost and how many blocks away from the original submisssion is the tx (with the hash, this can be easily verified), so the user can get funds from the fund to help him pay for his transactions using funds from high paying whales.

The main benefits is that the Ethereum network will be a real alternative for low price transactions willing to wait a long time. Right now, low gas price txs are never processed.

I’m not a protocol expert, but I realize this is a big change, because it required to change the block structure, and it will require some several  wallets mods to make this usable.

Anyone think this is a viable idea?

## Replies

**esaulpaugh** (2021-03-19):

Adding more computation to the protocol is a tax on the network as a whole. Also, this would end up being a tax on privacy since privacy-preserving transactions are high-gas. And no taxation without representation.

