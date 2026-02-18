---
source: ethresearch
topic_id: 4797
title: Secure transactions in light of a 51% attack
author: DB
date: "2019-01-11"
category: Security
tags: []
url: https://ethresear.ch/t/secure-transactions-in-light-of-a-51-attack/4797
views: 1980
likes: 3
posts_count: 11
---

# Secure transactions in light of a 51% attack

The recent 51% attack on ETC made me think that this is not that far away from Ethereum, as renting 20X more hash power today is mostly about money (unlike Bitcoin, where the use of specialized hardware makes it harder to buy). Is there a way to make some transactions more secure (for example larger moves) until PoS comes?

One solution (that may already be implemented without me knowing about it) is to commit the transfer to a chain via hash reference. Lets say Bob gave me 100 ETH in block …56 in exchange for 100 of my magic ERC20 coin. If I transfer coins to Bob (say at block …57), he may be able to rearrange the chain so his transaction never happened. Now let me make my transaction include an IF statement, that makes it valid only if the hash of block …56 is as I saw it. If he rearranges the chain, he will not be able to use my transaction, as he cannot reproduce the original hash. How hard will it be to implement something like this?

## Replies

**nourharidy** (2019-01-12):

A 51% can be conducted to reorganize the chain even with empty blocks. In this case, transactions that were previously confirmed can be removed from the chain. In other words, it matters more which transactions are no longer included than what new transactions are included. Consider the following scenario:

- Attacker makes a purchase using ETH
- Attakcer receives the counter product/service/asset
- Attacker launches 51% attack and reorgs the chain, replacing the block of his original transaction with another block
- Attacker signs and includes a different transaction with the same nonce in the block to completely invalidate his original transaction

What made ETC suffer from a loss of confidence was the fact that people could no longer trust it to keep the money they receive because a 51% attack is so cheap.

---

**DB** (2019-01-12):

The attacker needs to keep the new transaction as part of the new block, after removing an old one. If one can make the new transaction internally invalid, he cannot steal the funds. We replace a simple transaction with one that states that it is valid only a previous known block has such and such hash value (and thus includes the original “deletable” transaction). This cannot be forged by a 51% hash power. The attacker can include the new transaction in a block, but it is invalid, and noting moves.

---

**nourharidy** (2019-01-12):

Both transactions are signed and submitted by the attacker. The form of commitment that you are proposing can be itself removed from the chain during the reorg. Also, previous blocks do not have to be altered to double spend. The attacker only has to go back in time up to the transaction he’s looking to alter.

Did I get you wrong?

---

**DB** (2019-01-12):

The mechanism cannot be removed because it is part of the transaction. No simple transaction is signed, only a more complex code that requires the existence of the previous transaction in a specific block (via the hash of that block). An EVM looking at the new transaction in a chain that lacks the old one will not execute a transfer of anything, just exit. The attacker cannot separate the validation form the value transfer, as it comes as a single signed block of code.

It will probably be easier to implement with a smart contract: send funds and a specific block number hash to a contract, if hash is still true, move funds to target, else return to sender.

---

**flygoing** (2019-01-12):

This is definitely doable using a smart contract that validates tx dependencies, but like someone else said previously, this doesn’t cover the common instances of 51% attacks where someone deposits to an exchange, sells their eth for ltc, withdraws the ltc, and reorgs to replace the deposit of eth with a 0 eth transfer.

The actual easy way to mitigate what you’re referring to is atomicity. If you want Bob to send you ETH, and you send him dai, just do it atomically using a DEX like 0x.

---

**DB** (2019-01-12):

This is not a complete solution, it won’t work with other chains and even on the Ethereum chain, an attacker can still buy something, and undo the buy if value goes down (say a dice role, as a few hours won’t allow for much fluctuation in ETH value). But it may be important to secure large transactions, on-chain exchanges (DAI, wrapped BTC etc’) and smart contracts. Unlike an exchange, how will smart contracts, for example, be protected against someone draining all of the contract funds by double spending? How will people trust smart contracts once such attacks happen?

---

**flygoing** (2019-01-14):

> it won’t work with other chains

Isn’t this irrelevant? ethresear.ch doesn’t exist to solve issues that exist on the bitcoin blockchain. We’re trying to solve issues specifically for Ethereum.

> how will smart contracts, for example, be protected against someone draining all of the contract funds by double spending? How will people trust smart contracts once such attacks happen?

I’m not sure what you mean by this. Double spends don’t really apply to smart contracts since only 1 of the transactions will ever exist to the contract. Could you give an example?

---

**DB** (2019-01-17):

> Isn’t this irrelevant? ethresear.ch doesn’t exist to solve issues that exist on the bitcoin blockchain. We’re trying to solve issues specifically for Ethereum.

No, a lot of activity today (even if speculative) is about more than one chain. If transfers become reversible on multiple chains, that’s a problem for everyone.

My bad about the smart contracts, you are right. However, such “time control” is still a big problem for smart contracts. For example in Augur, anyone with such an ability can re-forge the blocks to be the sole disputer of markets as the time window arrives, undo disputes that happen within a short timeframe of the end of the disputing window etc’.

---

**Hither1** (2019-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/flygoing/48/2131_2.png) flygoing:

> Double spends don’t really apply to smart contracts since only 1 of the transactions will ever exist to the contract.

So can Double Spending ever happen between an attacker and a smart contract?If not, can smart contracts be used as agents between user and user to prevent double spending?![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**flygoing** (2019-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/db/48/1527_2.png) DB:

> No, a lot of activity today (even if speculative) is about more than one chain.

There’s a difference between speculating/learning about other chains and seeking to find solutions to those chain’s issues, especially when those solutions are vastly different than the solutions you would use on Ethereum.

![](https://ethresear.ch/user_avatar/ethresear.ch/db/48/1527_2.png) DB:

> For example in Augur, anyone with such an ability can re-forge the blocks to be the sole disputer of markets as the time window arrives, undo disputes that happen within a short timeframe of the end of the disputing window etc’.

It doesn’t sound like you want tx security, you want block finalization, which will happen in Eth2.0.

![](https://ethresear.ch/user_avatar/ethresear.ch/hither1/48/3102_2.png) Hither1:

> So can Double Spending ever happen between an attacker and a smart contract?If not, can smart contracts be used as agents between user and user to prevent double spending?

This is what I suggested earlier with atomicity:

![](https://ethresear.ch/user_avatar/ethresear.ch/flygoing/48/2131_2.png) flygoing:

> The actual easy way to mitigate what you’re referring to is atomicity. If you want Bob to send you ETH, and you send him dai, just do it atomically using a DEX like 0x.

To add to this, the atomicity can really be expanded to any 2 on-chain actions, not just “you give me eth and i’ll give you erc20 tokens”.

