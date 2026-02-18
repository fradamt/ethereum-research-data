---
source: ethresearch
topic_id: 5851
title: Spam resistant block creator selection via burn auction
author: barryWhiteHat
date: "2019-07-21"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/spam-resistant-block-creator-selection-via-burn-auction/5851
views: 7813
likes: 26
posts_count: 25
---

# Spam resistant block creator selection via burn auction

## Introduction

In a bunch of different contexts we want to select who is allowed to create a block.

Currently we have a compeition (pow, pos) to decide who is allowed to create a block. This is to

1. Rate limit the blocks that a node needs to check.
2. Provide a level of censorship resistance by randomly selecting this block creator so that censorship efforts need to involve a large percentage of the network to prevent a transaction from being minded for a long time.

These schemes are wasteful in that they require a large amount of stake to be deposited or work to be done. Both are costs that need to be reimbursed via fees. It creates this monopoly where a single person is created for creation of block x and they are insentivized to extract as much funds as possible in the form of transaction fees.

Here we propose a method to auction the right to create a new block to the person willing to burn the most eth. This results in a cencorship resistant block creation that requires that an amount == fee of the transaction they are consoring, be burned in order to censor it.

## Mechanizim

We have an auction where everyone bids the amount of eth they are willing to burn in order to get the right to create the next block.

The winning bid is the highest amount of eth. This address is assigned teh right to create the next block.

## Incentives

Every block proposer has the following properties

`target_profit` the profit they want to make mining this block.

They also have a list of transactions that can be included in a block they calculate

`sum_total_fees` = SUM (tx1.fee , tx2.fee, tx3.fee … txN.fee) where tx1 to txN are the transactions ordered by fee.

They caculate their `burn_bid` =  `sum_total_fees` - `target_profit`

and publish this as they bid.

1. If everyone has the same sum_total_fees we select the bid that has the lowest target_profit
2. If bidders have a different view of sum_total_fees we select either highest overall bid. This means that if a block creator wants to censor tx.2 they need to
reduece their target profit by tx.2.fee in order to win the auction.

## Incentives to relay transactions

This mechanizim reduces the incentives to relay transactions around the p2p network. Because having transactions that no one else is helpful during this bidding process.

This puts the users strongly in control of who they relay their transactions to which also means that they are able to select the winning block creator if they work together.

## Conclustion

We are unable to know in protocol how many transaction of what fees are available to go in a block.

We want to include the transaction with the highest economic value.

We use the fee burn to show us in protocol who is going to add the most economically valuable transactions.

## Replies

**Mikerah** (2019-07-26):

Have you looked into [Fidelity Bonds](https://en.bitcoin.it/wiki/Fidelity_bonds)?  In the context of Bitcoin, Fidelity bonds burn Bitcoins in order to make it hard to create new identities on chain. They have applications in making mixers sybil-resistant. You can read more about applying fidelity bonds to joinmarket [here](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2019-July/017169.html)

---

**vbuterin** (2019-07-27):

There’s actually a lot of real benefit that could come from this kind of scheme. Particularly, it completely turns block proposal into a separate functionality from being a validator, so validators don’t need to care about collecting fees. This solves a big part of our fee market challenges, because the whole concept of relayer markets etc can go away; relayers just become block producers.

Need to explore this more.

---

**vbuterin** (2019-07-27):

The first nontrivial issue I can come up with is that this creates a very different fee market dynamic from EIP 1559 for users, and it’s worth exploring exactly what this fee market dynamic looks like. I do fear it could be more complicated for users to work their way around. Though maybe if you had the EIP 1559 tax *on top of* the auction that could solve it…

---

**barryWhiteHat** (2019-08-02):

This is a mechanism that finds the actor who is willing to execute the transaction ordering in a way that

1. Includes the highest transaction fees
2. Burns the most of the profit from this

So it should be applicable to any fee mechanism with minimal changes.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The first nontrivial issue I can come up with is that this creates a very different fee market dynamic from EIP 1559 for users, and it’s worth exploring exactly what this fee market dynamic looks like. I do fear it could be more complicated for users to work their way around. Though maybe if you had the EIP 1559 tax on top of the auction that could solve it…

EIP1559 seems like a special case because we need to adjust the blocksize. We could adjust the auction slightly.

We have a variable block size that can be adjusted up or down by the bidders. But to adjust its size by 1/8th they need to burn an extra `bigger_block_burn`. So if i want to create a block with 8,000,000 gas i bid my price and it is treated as is. But if i wanted to create a 9,000,000 gas block. I would bid and my bid would be reduced by `bid - bigger_block_burn`

So the 1,000,000 gas of transactions would have to result in more transaction fees than `bigger_block_burn` in order to win the auction.

This bigger block burn is treated like a difficulty and is updated so that we have an average block size of 8,000,000 gas per block.

Also we should use a all pay lowest price auction in this mechanism and their should be no major changes. This would also make things much simpler for the users.

---

**barryWhiteHat** (2019-08-02):

Ah this is interesting. I think that burning is an under utilized tool in our cryptoeconomic toolbox.

---

**Mikerah** (2019-08-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> all pay lowest price auction

Why an all pay auction instead of a second price auction? Is this to induce a form of sybil-resistance by requiring everyone to pay their bid price even if their bid isn’t the highest one?

---

**kivutar** (2019-08-02):

Is it possible that everybody sends the same bid? If the input is the same, similar nodes will produce similar output, isn’t it?

---

**barryWhiteHat** (2019-08-03):

In that case we can select the bidder who made that bid first. Or else we could flip a coin.

---

**adlerjohn** (2019-08-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> Or else we could flip a coin.

How would you flip a coin? If you had a source of unbiasable, unpredictable, verifiable randomness, then couldn’t you just…use that for leader selection?

---

**Mikerah** (2019-08-03):

There are many n-party coin flipping protocols. [This paper by Ben-Or et al](https://pdfs.semanticscholar.org/fca7/ef8bf80b01f4de19c4d86e92b973f5612f7b.pdf) summarizes the method that some blockchain protocols like Polkadot uses.

---

**adlerjohn** (2019-08-03):

Unless I’m mistaken, that paper is basically RANDAO with output modulo 2 (*i.e.*, \in \{F, T\}), no?

---

**vbuterin** (2019-08-03):

That would be a parity function. There’s a class of functions called “low-influence” functions that the paper talks about that try to go beyond what RANDAO and parity functions do by creating outputs that usually would not be influenced by any single bit. The simplest low-influence function is the “majority function”, f(x_1 ... x_n) = 1\ if\ \sum x_i \ge \frac{n}{2}\ else\ 0, where the probability that a single actor can flip an output is \frac{1}{\sqrt{n}} and the expected number of actors needed to flip the output is \sqrt{n}.

There are other low-influence functions but you have to make tradeoffs, eg. the first example function that they give (called TRIBES in a different paper) has the property that each individual actor has a very low (\frac{log(n)}{n}) probability of being influential, but if an attacker has a substantial fraction they can influence the result by flipping 1 \le b \le O(log(n)) of the bits that they control, so the *cost of attack* is very low.

---

**barryWhiteHat** (2019-08-04):

We don’t need to have strong randomness here. Because we know that both bidders are either

1. Bidding to make the same block
or
2. One is burning some of their own funds in order to censor a transaction. And that this attack needs to be continued with that same burn per block in order to keep that transaction out.

---

**tbrannt** (2019-08-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> this attack needs to be continued with that same burn per block in order to keep that transaction out

Wouldn’t it then be quite cheap to censor a specific transaction for quite some time?

---

**barryWhiteHat** (2019-08-05):

If you want to censor tx1. Then each block you need to burn tx1.fee. This is decided by the user so they can decide how much this costs. Also note that the attacker has to do this burn for every block. So this attack requires burning money constantly so over time it becomes quite expensive.

---

**tbrannt** (2019-08-05):

So thinking about this nice quote by Vitalik: “The Internet of Money should not cost 5 cents per transaction.” I assume the goal is to have quite low fees for simple transactions. How low? I’m not sure but let’s say around 0.05 cents (cheaper by a factor of 100).

With block times of 5 seconds it would only cost you around $8 per day to keep a specific transaction out of the blockchain. That sounds quite cheap to me.

---

**barryWhiteHat** (2019-08-06):

The user who is censored also has the option to increase their fee in order to try and break the attack. If i broadcast at 0.05 cent transaction and i get censored the i can rebroadcast with the still quite reasonable 0.5 cent and that will cost $800 per day to censor.

It does get more complicated when we have the all pay auction. That would mean that you could include a higher price transaction but could still get censored because including your transaction would not give a real increase in the profit that the block creator gets. Because they have to charge the lowest price in a block to all transactions. I need to think more on this point.

---

**barryWhiteHat** (2019-08-06):

When i say all pay auction i mean. That a block creator makes a block and charges everyone the fee of the lowest fee transaction in that block. I used that because i think its a reasonable way to price transactions in a block. But the two ideas are independent.

---

**tchitra** (2019-08-11):

One slight thing to note about this, however, is that Tribes only achieves the worst case bounds when n is a power of 2.

---

**ashishrp** (2019-08-12):

In the case of Ethereum where we have inflation already, burning sounds like a viable option.

Miners can compete for 3 ETH(X ETH) reward and burn Y ETH(less than computational costs) till it’s economically profitable, that would help with free-market price and inflation control.


*(4 more replies not shown)*
