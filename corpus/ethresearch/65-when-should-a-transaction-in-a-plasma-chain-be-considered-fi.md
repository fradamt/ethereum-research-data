---
source: ethresearch
topic_id: 65
title: When should a transaction in a Plasma chain be considered final?
author: maiavictor
date: "2017-08-29"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/when-should-a-transaction-in-a-plasma-chain-be-considered-final/65
views: 1725
likes: 4
posts_count: 3
---

# When should a transaction in a Plasma chain be considered final?

On Plasma, suppose someone creates a token contract as a separate chain. Suppose then that I am a merchant selling goods/services for that specific token. How many blocks should I wait before giving an user the purchased goods/services? I’m specifically wondering whether this can safely be done before the transaction is finalized on the underlying root chain.

## Replies

**RoboTeddy** (2017-09-11):

It depends on the consensus rules of the plasma sidechain, and how those rules are rooted in the main chain.

As soon as you can generate a proof of ownership that would convince the main chain contract that the coins are yours, you can consider the transaction final. This can definitely happen before the transaction is finalized on the root chain. For some types of plasma sidechains, it could happen near instantly! (milliseconds).

---

**vbuterin_old** (2017-09-11):

It depends heavily on the consensus rules of the plasma sidechain. If we assume a simple plasma chain run by the dictator algorithm (“a block is finalized if and only if (i) Bob signed it, and (ii) the block header got included in the main chain”). We assume that the contract on the main chain only accepts block headers with increasing nonces, like transactions, so there is no possibility of forking and you have instant finality. Then, you can consider a payment final if (i) it was included in a finalized block, (ii) that block, and all previous blocks, are fully available, and (iii) that block, and all previous blocks, are valid.

You can show that in this case, you will be able to get your money out. This is because the only move the adversary (ie. a hostile dictator) has available is to create new blocks on top of that block which also spend your money, but then you can challenge them by showing the Merkle branch of your own block, which takes precedence because it is earlier in the chain.

