---
source: ethresearch
topic_id: 15057
title: Reducing MEV with transaction auction
author: mkoeppelmann
date: "2023-03-15"
category: Proof-of-Stake
tags: [mev]
url: https://ethresear.ch/t/reducing-mev-with-transaction-auction/15057
views: 3304
likes: 10
posts_count: 5
---

# Reducing MEV with transaction auction

**Preface**

The goal of this concept is to reduce the amount of MEV that is currently given to validators and give more of it back to users who are responsible for it.

The concept is simple (and has been discussed in many forms before) but this post wants to mention a very simple implementation strategy that can be done right now. The idea is that for each transaction a user sends there is an auction for the right to back-run the transaction. For public mem-pool transactions, those auctions are already happening (not only for back-running, also for sandwiching) but the bids go to validators.

**Concept**

A simple RPC endpoint for users that want to keep the MEV value of their transaction. For each transaction, the RPC provider offers the transaction (without signature) to all searchers (can be permissionless). Searchers can “bid” to be included first after the transaction. Part of the transaction needs to be a simple ETH transfer to the user (msg.origin) - the amount of that transaction is essentially the bid. The provider takes the highest bid and creates a “bundle” out of the user+backrun/bid transaction and can send it to all trusted builders.

If builds perform as expected this means the user transaction can only land on-chain together with the back-run transaction. Of course, if there are no bids (not all transactions create MEV) the transaction can be sent to a builder without a back-run tx (still protecting the user from being front-run).

**Information leakage**

While searchers can not just take the transaction and get them into the chain outside of this mechanism they still learn about the transaction. In theory, they could use that information and still try to front-run a user (for example a user wants to buy a huge amount of an exotic token which would move the price significantly). This can be combated by adding fake transactions to the transactions presented to the searcher. If e.g. User A spends 10 ETH to buy token A the RPC provider could simply present 3 more transactions to searchers in which the user would buy token B, C, or D. Essentially the higher the % of fake data the lower the information value that gets leaked. It should thus be possible to find the % that is high enough to prevent searchers from attempting to front-run a user as the searcher bears the cost of each failed front-run attempt.

**Trust assumptions**

This approach is a strict improvement over services that already today try to offer frontrunning protection as this approach has the same trust assumptions (trusting the RPC provider, builders and relays) but in addition gives value back to the user.

## Replies

**llllvvuu** (2023-03-23):

I believe this is isomorphic to Flashbots’ SUAVE / mev-share, in the sense that advertising a set S of possible transactions is [the same as auctioning off a type T of possible transactions with extension S](https://cs.stackexchange.com/a/91345). The tricky thing is defining the contents/cardinality of the “anonymity set”. If there are too many, then searching becomes infeasible in terms of computation/bandwidth. If there are too few (e.g. each order is mixed only with an equal and opposite decoy order), then the flow may be decryptable (as you say, some amount of decryptability is OK, since the confidence must be enough to operationalize, i.e. outweigh costs)

Another note; backrunning each individual transaction allows you to compensate each user more precisely, but spends more gas vs backrunning (or perhaps better, JITing) a block of transactions. It’s not obvious which way one should fall on the tradeoff.

Another advantage of auctioning off combined flow is that there is less information content in the denoised flow, so less noise has to be added (in terms of bits) to the auction subject

---

**thogard785** (2023-03-28):

There’s a significant amount of front-running protection you can enable by simply not letting the searcher know that they’ve won the auction.  The searcher will be hesitant to take a guaranteed -value position (first leg of sandwich) if the ++value position that offsets it is not guaranteed, bringing down the total EV of the trade.  Once chance of winning drops to 50% or lower then users are quite safe as long as searchers are rational.

We use this method plus a max bundle size of two at FastLane (MEV relay on Polygon) and it has been working very well so far despite the non-deterministic execution environment (from the relay’s PoV, anyway) of the bundles.

Biggest issue, though, is the fact that a sandwicher can afford to bid higher if they know they’re profiting from a sandwich… which can asymmetrically raise their confidence in winning the auction back to a level at which sandwiching becomes the +EV decision for them.

Our solution to the “sandwichers can overbid and gain win-rate confidence, thereby affirming the sandwich as +EV strategy” dilemma is that we don’t allow private transactions.  Often times the first leg of the sandwich attack is, itself, backrunnable… and we’ve found that searchers are often the best defense against other searchers.  It is very rare to see a sandwich’s first leg in which the rate delta for the targeted pool is high enough to offset the fee for the volume but low enough to not be backrunnable by other searchers. Those that do meet that criteria are usually low value adds and, when measured against the uncertainty of winning the final leg of the sandwich, usually aren’t worth doing.  The lack of a  private relay means other searchers can always see the first leg of the attacker’s sandwich and get their own tx between it and the victim.  It’s an imperfect solution but it has been quite effective so far. It does, however, start to break down for *extremely* exotic tokens in which there is only one pool.

---

**bsanchez1998** (2023-04-13):

The idea of auctioning off the right to back-run a transaction is an interesting way to make the whole process more transparent and fair for everyone involved.

I can see some potential hurdles in making this work like making sure those fake transactions you mentioned are convincing enough to stop searchers from trying to front-run users. And managing trust between all the different players might get a bit messy.

Still, I think this is worth exploring more. If it ends up working well, it could maybe inspire other blockchain networks to try something similar.

---

**mkoeppelmann** (2023-04-17):

By the way - this concept has been implemented now: https://mevblocker.io/

You can find live data here: https://rpc.mevblocker.io/backruns

Those are transactions with a successful back run and thus a refund.

E.g. [zeromev ethereum frontrunning explorer - showing user losses from miner extractable value (MEV)](https://zeromev.org/block?num=17061871)

In this block, you can see that the very first transaction was a user trade. The second transaction is a back run with payment to the builder (which is eventually forwarded to the validator) and the 3rd transaction is the payment to the user (from the builder).

