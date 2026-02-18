---
source: ethresearch
topic_id: 16121
title: Improving User Experience for Time Sensitive Transactions with a Simple Change to Execution Logic
author: MaxResnick
date: "2023-07-15"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/improving-user-experience-for-time-sensitive-transactions-with-a-simple-change-to-execution-logic/16121
views: 2398
likes: 14
posts_count: 13
---

# Improving User Experience for Time Sensitive Transactions with a Simple Change to Execution Logic

As usage of the Ethereum network for DeFi has increased, more and more transactions are time sensitive. That is, there are transactions for which, if they are not executed in a timely manner users would prefer that they not be executed at all.

For example, consider a simple trade on UNIv3 ETH/USDC. If it executes quickly, then users get a reasonable price and they are happy. If it executes slowly however, it may become stale, users may get a worse price or get sandwiched because their slippage tolerance is no longer set correctly. If is not executed quickly, users might prefer it be automatically canceled so they can submit another transaction.

It is possible to get this kind of behavior currently; however, it requires costly on chain operations, and the transaction may be included on chain anyway, meaning that even though the transaction has been *killed*, the user still pays gas.

To accommodate these preferences, I suggest adding a new field to ethereum transactions `fillBy`. `fillBy` is an optional field where a user can choose a slot which if specified would make a transaction invalid after a certain slot has passed in the same way it would be invalid if the signature didn’t check out or if a transaction with the same nonce from the same user had already landed on chain.

This would be extremely useful for searchers particularly in preventing low carb crusader attacks over multiple blocks, which could eliminate the attack even without single slot finality.

## Replies

**meridian** (2023-07-15):

Deadline as a tx parameter already exists and is used by default for txs for uniswap/sushiswap

The problem is conceptual: every transaction is time sensitive in general. Users always want it executed as quickly as possible and this does not improve UX from their perspective: they now have to “track” the tx and confirm that it was executed. The coupling of submission to settlement in their minds is now even moreso.

On a sidenote I think in general this is a good idea as this is how we sort our mempool for txs, LIFO. Makes no sense to waste compute on txs that may not be viable for inclusion.

---

**llllvvuu** (2023-07-15):

Having this at the base layer [has been made as an EIP a few times](https://ethereum-magicians.org/t/eip-5081-expirable-transaction/9208) but has always been shot down due to concerns of DDoS.

But now it will be a feature of account abstraction. I guess Ethereum can’t make up it’s mind ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12)

---

**parseb** (2023-07-16):

It can be a feature of whatever, whenever need it.

Changing “execution logic” is overkill for something that is already possible.

If the benefits outweigh the costs, account providers will do it first. They haven’t.

(Currently used in delegation frameworks.)

Wouldn’t this 1 trillion x the mempool size? Potential good L2 differentiator.

---

**MaxResnick** (2023-07-16):

reading through the comments, the DDOS line of argument makes negative sense, you can already spam the chain with txs with the same nonce and only one can execute on chain.

---

**MaxResnick** (2023-07-16):

It’s not already possible though? If you use contract logic then the tx will fail and the user will still pay gas when the tx is included.

---

**MicahZoltu** (2023-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> reading through the comments, the DDOS line of argument makes negative sense, you can already spam the chain with txs with the same nonce and only one can execute on chain.

All current clients will ignore any transactions that that have the same nonce but do *not* have a significantly higher fee (I think 12.5% is normal).  This ensures that each transaction that is broadcast across the network has to pay *at least* 12.5% of the bottom of the mempool.  With expiration, you can construct a transaction that will almost certainly not be included ever and will eventually leave the mempool without ever paying anything.

---

**MicahZoltu** (2023-07-16):

Note: This can be mitigated to some extent by requiring that any transaction with a deadline be in the top 1 block of transactions in the mempool (sorted by max_priority_fee) and have a max_fee that is substantially higher than current base fee, and have a deadline that is at least `n` blocks in the future.  This way the chance of not getting included is near zero, so the chance for DOS is near zero.

This design has been proposed in the past, and I think it stands the best chance of inclusion.

---

**parseb** (2023-07-16):

Public mind-share is a rivalrous good. There’s no such thing as a free advertisement.

---

**llllvvuu** (2023-07-16):

I presume that restriction would only apply to propagating transactions and not to confirming transactions? It seems fine if nodes are free to join alternative networks (such as BDN) and for those networks to choose to relay with different criteria, and for nodes in that network to propose transactions that wouldn’t have been propagated in the “official” mempool.

---

**MicahZoltu** (2023-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> I presume that restriction would only apply to propagating transactions and not to confirming transactions?

Yes.  The DoS vector is around propagation of transactions in the mempool, not around propagation or inclusion in blocks.  We want to make sure that any transaction that is propagated must pay *something* for that propagation to happen.

---

**michaelscurry** (2023-07-27):

Sorry Max, not to hijack your proposal but I raised a similar one here: [Priority fee should be burned for reverted transactions - #3 by michaelscurry](https://ethresear.ch/t/priority-fee-should-be-burned-for-reverted-transactions/16186/3)

Wonder if that would help with the use case you mentioned here. I’m suggesting that the priority fee should be burned instead of given to validators for reverted transactions. In your example, txs that will revert due to being past deadline would be most likely ignored by proposers. However, if a malicious user tries to spam the network, they would still have to put funds at risk. While it may not benefit a proposer economically, they could still include the txns to unclog the network.

what do you think?

---

**MaxResnick** (2023-08-02):

Hmm, this is an interesting idea, after all, the priority fee should be for priority. But I think having the tx not pay a fee at all if it’s delayed might be a better way to deal with it from a user’s perspective, I also second [@barnabe](/u/barnabe) 's point about side contract proofs.

