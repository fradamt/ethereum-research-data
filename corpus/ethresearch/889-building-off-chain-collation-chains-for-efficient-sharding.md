---
source: ethresearch
topic_id: 889
title: Building off-chain collation-chains for efficient sharding
author: denett
date: "2018-01-24"
category: Sharding
tags: []
url: https://ethresear.ch/t/building-off-chain-collation-chains-for-efficient-sharding/889
views: 2981
likes: 3
posts_count: 7
---

# Building off-chain collation-chains for efficient sharding

My goal is to come up with a ***sharding scheme*** that has a ***high collation rate***, without sending every collation to the main chain. This to ***save on gas*** and get ***better scaling***.

The idea is to let the validators create a chain of collations ***off-chain*** and only send a combination header containing all off-chain collations once every X collations. Note that you still want to publish the header on a regular basis for cross shard communication and finality.

**Building the collation chain**

The order of the validators is known in advance and a validator is only allowed to build an off-chain collation on top of a collation of his direct predecessor. If lot of validators in row participate we can build a long collation-chain. Every participator in the chain is allowed to send the combination header to the main chain at any time. We want to avoid that a validator sends an older version to the main chain, so all participators have to sign the latest combination header to let them commit not to send any older headers.

**Skipping validators**

If a validator does not participate or is offline, one participant of the collation-chain sends the combination header to to main chain. If the non-participating validator does not send a collation header within a certain number of blocks, the next in line validator can send its header to the main chain and the non-participating validator is skipped. After that, the validators can start building a new collation-chain off-chain. A validator is allowed to skip previous validators that have not send a header to the chain, but has to wait a certain number of blocks per skipped validator. This waiting period per validator is a few factors longer than the off-chain collation interval, so the off-chain collation-chain builders do not have to worry about being skipped.

**Attack by censoring**

An attacker could try to revert a collation-chain by censoring the combination header transaction for a long enough period to be able to send a header and skip all participants.

As an extra safety measure, it is possible for a combination header to revert collations headers on the main chain from the validators that skipped the collation-chain builders as long as the collation-chain contains more collations than the number of reverted collation headers.

Because we do not allow building an off-chain collation-chain on top of a collation header that might be reverted and there is a minimum block interval between headers, we give the censored validators more time to get their combination header confirmed and withstand the attack.

## Replies

**vbuterin** (2018-01-25):

So the N off-chain collations that are submitted to the main chain can have different validators? That indeed would not sacrifice on any security, but it would also not lead to gas savings, as you’d have 5x the content in 1 transaction instead of over 5 transactions (note that with the latest updates, the overhead of the transaction itself is not that large; we’re making the transaction sig play the role of the header sig so it doesn’t duplicate data anymore).

---

**denett** (2018-01-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So the N off-chain collations that are submitted to the main chain can have different validators?

Indeed the N off-chain collations are from the N different validators whose turn it is in the validator queue. Instead of sending them all to the main-chain on by one, a combination collation, signed by all N validators, is send.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> it would also not lead to gas savings, as you’d have 5x the content in 1 transaction instead of over 5 transactions

The combination collation transaction should be smaller than the total size of the N individual transactions, because you only need one transaction root, one state root and an aggregate of the signatures of the N validators. Although the contract still has to validate all N signatures.

---

**vbuterin** (2018-01-27):

OK, I can see how it can give some small factor of concrete efficiency gains; possibly 2-3x. But I still don’t feel it’s worth the cost of the added protocol complexity.

---

**denett** (2018-01-27):

The efficiency gains depend on the number of collations you take off-chain. If you only go back to the main chain every 25 collations, you get a higher factor of efficiency gains.

You can even go up to 50 without missing finally of the main chain. Cross shard communications will be a lot slower, because they will depend on collations headers on the main chain.

Adding complexity is indeed a concern, at least for the first version keep it as simple as possible.

Question: Do the non proposing validators have to sign the collations as well? How are these signatures send to the contract? Is it possible to aggregate the signatures off-chain and and let the proposing validator send them together with collation header?

---

**vbuterin** (2018-01-27):

The efficiency gains are bounded above by (gas cost of including and verifying signatures) / (total gas cost). The numerator there is something like 10000.

---

**denett** (2018-01-28):

I am not familiar with the specifics of signature aggregation, but I have read that in some cases the size of an aggregated signature containing N signatures still has the size of one signature. I don’t know it that would be possible for the signatures of the validators, but it could safe space.

We could use a scheme similar to the “Partial validation and slashing condition” scheme in [this](https://ethresear.ch/t/fork-choice-rule-for-collation-proposal-mechanisms/922) post, to do the do the verifying of the signatures off-chain. If a whistleblower misses a validators signature, it can proof it on-chain, burn half the validator’s deposit and keep the other half.

