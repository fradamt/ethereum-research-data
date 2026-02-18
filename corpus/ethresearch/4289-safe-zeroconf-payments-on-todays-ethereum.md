---
source: ethresearch
topic_id: 4289
title: Safe zeroconf payments on today's Ethereum
author: DennisPeterson
date: "2018-11-17"
category: Applications
tags: []
url: https://ethresear.ch/t/safe-zeroconf-payments-on-todays-ethereum/4289
views: 3111
likes: 4
posts_count: 5
---

# Safe zeroconf payments on today's Ethereum

Recently I came across a proposal for [safe zero-conf transactions](https://www.youtube.com/watch?v=EsddVkR-MSs) on Bitcoin-style chains.

Basically it’s a way to post a bond, such that a doublespend results in the loss of the bond. It detects doublespends by reuse of UTXO inputs. Anyone (presumably miners) can submit the two transactions and collect the bond.

We could build this into a Plasma chain, letting the operators collect the bonds. But by tweaking the idea we can do something similar on the main chain today.

Instead of UTXOs, we just look for reuse of the same nonce from the same sender. We can write a contract that accepts two complete signed transactions, checks their senders and nonces, and if they match, awards a bond to msg.sender.

The merchant has to do a few simple checks to accept a zeroconf transaction:

- The sender must have adequate funds
- The transaction must have the sender’s current nonce, not a later one
- The sender cannot be a contract, since a multisig wallet could allow a different address to withdraw the funds
- The sender must have a deposit in the zeroconf contract, which is larger than the purchase amount

If all of these things are true, the merchant can safely accept a zeroconf payment. The transaction can be faster than a credit card approval if the merchant’s client maintains the necessary state: just the current balance and nonce of all addresses, and all the current zeroconf deposits. Then it’s a local lookup to approve the transaction. In a busy shop, this would be much better than waiting for a block, even with Ethereum’s fast blocks.

The merchant can monitor for doublespends and attempt to collect bonds, in case the miners fail to do it. But if the miners find it worthwhile, the merchant can simply enjoy fast transactions with low fraud rates and not worry about it.

Implementing the zeroconf contract would be reasonably simple. There are Solidity libraries for RLP but we don’t need them; the nonce is the first data field (aside from length indicators) and the signature is at the end. On each transaction check signature and nonce, and if the transactions match, award their signer’s bond to msg.sender.

Obviously this doesn’t work so easily with signature abstraction, but if the existing transaction format is still supported, the merchant can simply restrict zeroconf approvals to old-style transactions.

## Replies

**adiasg** (2018-11-25):

Interesting concept! I am assuming that the buyer will deploy it’s own zeroconf contract that the merchant looks up.

Here is one concern:

Assume that the zeroconf contract deposit is X. The attacker (buyer) signs off on multiple zeroconf transactions (with the same nonce) that sum to more than X, and shows it to different merchants before any of the transactions appear in the chain.

This would be tougher to do if miners are also looking out for zeroconf double spends, since now the attacker must use all those transactions before any 2 of them show up in the same miner’s mempool.

---

**DennisPeterson** (2018-11-25):

Yes, the idea is not so much to prevent doublespends or compensate the merchants, as to make doublespends unprofitable when miners (or others) detect them in the mempool and take the bonds.

If the buyer spends enough at multiple merchants with the same nonce he can come out ahead even after losing the bond. The larger the bond relative to the purchases, the more difficult this will be.

I’m mainly thinking of this for in-person purchases, where fast confirmation is important and a multi-merchant attack would be difficult. (Even with confederates, the timing would be challenging.) I think the typical zeroconf attack is just to buy something, walk out, and issue a doublespend to self. In this case any bond larger than the purchase will result in the attacker having a net loss, as long as someone submits the two transactions with the same nonce. The merchant can at least know that profitable attacks will be difficult, and fraud rates probably low.

A contract for each buyer is one possibility, but one contract for everybody would also work. That way it’d be easier to make a light client that holds all the necessary state locally.

---

**adiasg** (2018-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/dennispeterson/48/1675_2.png) DennisPeterson:

> I’m mainly thinking of this for in-person purchases, where fast confirmation is important and a multi-merchant attack would be difficult. (Even with confederates, the timing would be challenging.)

Yup, I was imagining a group of people coordinating to make a purchase at different merchants at (approx.) the same time. Even though there is a large coordination cost to it, this does seem like a major attack vector.

Questions:

- Is there a way to better disincentivize the attack above?
- What other types of attacks are possible?

---

**DennisPeterson** (2018-11-26):

So far, the only mitigations I can think of are:

- Increase the bond size relative to purchase amount. Each merchant can set their own requirement, and if the bond is too small then they just wait for a block; or…
- Merchant watches mempool to detect doublespend attempts, instead of just relying on deterrence. (Of course you could do this even without a bond.)

I think for any purchase where a doublespend is a disaster, zeroconf should definitely not be used. But for a coffee purchase, there’s not much reward for a group of attackers, and not much damage if an attack succeeds occasionally. We probably only need to get below the fraud rates that credit cards have today, and just preventing a single attacker from profitably doublespending to self might be enough for that.

Also, the stores that need zeroconf the most are the busiest ones, and when stores are busy, it will be more difficult to pull off a simultaneous doublespend because the attackers can’t predict how long they’ll wait in line.

Of course, if anyone can think of a better defense, that’ll be interesting!

