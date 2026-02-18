---
source: ethresearch
topic_id: 2674
title: One Plasma Cash Block Per Deposit? Why?
author: simondlr
date: "2018-07-24"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/one-plasma-cash-block-per-deposit-why/2674
views: 2841
likes: 0
posts_count: 8
---

# One Plasma Cash Block Per Deposit? Why?

Hey.

I’ve been trying to figure out why it’s necessary to have a block per deposit in Plasma Cash. None of the documentation explains *why*. Only says it makes it cheap/faster to exit, but not sure why.

If deposit transactions are included amongst other transactions, then if you are verifying history as a client, then it should be sufficient to just specify the block number in a similar manner? Or am I missing something?

## Replies

**gakonst** (2018-07-24):

During exits, instead of having to verify a whole merkle branch, you can just verify that the deposit block root matches the transaction hash, which is much cheaper in terms of gas (when exiting a transaction involving a deposit block).

---

**ldct** (2018-07-24):

The deposit blocks are produced (and appended to the list of plasma block root hashes) by the plasma smart contract, in that the smart contract calculates what the root hash would be of a transaction tree that contains just the deposit.

It seems to me that it is possible to modify this to allow multiple deposits to be combined into one block. However it seems impossible for the plasma smart contract to calculate a root hash of a block that contains both p2p transactions as well as deposits, since the plasma contract doesn’t have the data for the p2p transactions.

---

**danrobinson** (2018-07-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> During exits, instead of having to verify a whole merkle branch, you can just verify that the deposit block root matches the transaction hash, which is much cheaper in terms of gas (when exiting a transaction involving a deposit block).

That’s true, although you don’t have to prove anything about the deposit tx when you withdraw in the normal case, right?

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> It seems to me that it is possible to modify this to allow multiple deposits to be combined into one block. However it seems impossible for the plasma smart contract to calculate a root hash of a block that contains both p2p transactions as well as deposits, since the plasma contract doesn’t have the data for the p2p transactions.

You probably could do it where the user deposits into the Plasma Cash contract, and the Plasma chain operator notices the deposit and includes a deposit transaction soon after in a block. You could probably even skip including the deposit transaction in the Plasma Cash chain and just store the time of deposit in the mapping on the main chain. But in both these cases, you’re basically storing data on the parent chain rather than as part of the Plasma chain, so it may actually be worse.

It’s almost certainly doable, but it doesn’t really help you with anything—the extra block isn’t really an inefficiency, as Georgios pointed out.

---

**ldct** (2018-07-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> It’s almost certainly doable, but it doesn’t really help you with anything—the extra block isn’t really an inefficiency, as Georgios pointed out.

The main thing I think is worth avoiding is the 5000 gas cost per deposit (the minimum cost of an `SSTORE` on the current gas fee schedule; if it changed to something more rent-based we can use [Double Batched Merkle Log Accumulators for Efficient Plasma Commitments - #2 by vbuterin](https://ethresear.ch/t/double-batched-merkle-log-accumulators-for-efficient-plasma-commitments/2313/2) and I wouldn’t bother to optimize this anymore)

---

**simondlr** (2018-07-25):

Thanks everyone.

So as I understand, it’s mostly that you essentially have a cheaper verification/check when exiting with a Deposit tx, because otherwise it has to check the whole membership, when it’s not really necessary. You could technically just include it amongst other txes in the side-chain, but then you’d need to do a full membership check when exiting with a Deposit tx?

Right?

---

**boolafish** (2018-10-10):

Recently, we have a similar discussion.

We are more tending toward the solution as [@danrobinson](/u/danrobinson) described, having a flag on contract and let operator listen to deposit event and put the tx into block.

One problem of smart contract building the block itself is that, operator might submit block the same time as somebody deposits. In the case that deposit block got merged first, operator has to re-build the whole data and resubmit it. Also, if the plasma chain is having smaller block time then root chain, issue might be even bigger. eg, tx in block2 specified that its previous block is block1. However, now a deposit tx takes the spot of block1, so block1need to become block2 and block2 need to be block3, and the previous block pointer would be wrong, so…all users will need to re-sign the tx and send it.

---

**ritikm** (2018-10-11):

Having the root chain smart contract create a Deposit Block also allows the user to withdraw their deposited funds in the event that the (malicious or buggy) child chain does not include the deposit in their chain. Otherwise, the user can be left in a scenario where it’s impossible for them to ever retrieve the funds.

