---
source: ethresearch
topic_id: 1430
title: Decentralized Casper Validator Proposal
author: kladkogex
date: "2018-03-19"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/decentralized-casper-validator-proposal/1430
views: 3015
likes: 17
posts_count: 12
---

# Decentralized Casper Validator Proposal

Here is an interesting proposal how many poor people can pull money together to create  a decentralized Casper validator:

1. 100 users contribute 15 ETH each to a “Decentralized Validator Smart Contract”. The total is 1500 ETH, which is enough to create a single Casper validator.
2. ECDSA threshold signatures are used to split a “Validator ECDSA Key” into 100 pieces.   Each key piece belongs to a single poor validator.  The resulting signature is indistinguishable to from a “real” ECDSA signature.
3. The threshold signature requires a majority of poor validators to sign
4. Since the signature is indistinguishable from a real ECDSA signature,  there will be no way for the Casper smart contract to block the “Decentralized Validator”
5. For each Casper epoch poor validators agree on the Casper checkpoint link to sign.   Then they do the threshold signature protocol  and post the signed checkpoint to the Casper smart contract. The Casper smart contract thinks it is a single validator and pays out the bounties.
6. The bounties are split among participants.
7. Note that the entire scheme can be implemented in an anonymous decentralized way using an ETH smart contract.

The question is then whether such decentralized validators should be considered good or bad ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)?  Since to create a threshold signature one needs a majority of validators to agree, the “Decentralized Validator” may be more secure than a regular one …

## Replies

**Lars** (2018-03-19):

Looks like a nice idea!

The question is how to manage exit requests. How do you leave Validator agreement?

Would it be possible to have a shareholder token that you can trade?

---

**kladkogex** (2018-03-20):

Good question ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) Adding / removing “poor validators” would require regeneration of the 'Decentralized Validator" ECDSA key.

If Casper supported validator key rotation (which is does not support now, but probably will), you could add/remove poor validators  at anytime, so then you could tokenize membership in the validator contract.

In the current implementation you could also tokenize by requiring the validators to rotate the ECDSA key say each month,  the “Decentralized Validator” would have to withdraw and re-join at the end of each month.

I would be happy to put 15 ETH for an experiment like this, if there are 99 more people interested.  This could be a way for security researchers to jointly run a validator to experiment with Casper once it is live. Note that this is very different from running a pool because all decisions are made by joint votes.

---

**toliuyi** (2018-03-27):

I think the idea is brilliant. Count me in if you put it into practice. I do have some ether and dev time:)

---

**schaeff** (2018-03-27):

I like the idea. Due to the round of signatures, a Decentralized Validator is likely to be slower to commit actions than a centralised one. While this doesn’t seem problematic in Casper FFG, I wonder if it would have an effect in Casper CBC?

---

**MicahZoltu** (2018-03-29):

All this is doing is changing the trusted actor in the system to a conglomerate.  Unless you have some way of guaranteeing that your pool isn’t 51% (or whatever the threshold is) controlled by a malicious actor you are back in the same boat.  Also, unless I misunderstand the idea, it creates a new problem in that if threshold of signatures isn’t achieved then the validator will be considered “offline” and suffer whatever penalties are associated with no-show validators.

I think you would be better off with a pool where the person validating the blocks can be shown to have 51% of the pool, thus any damage they do to others they are guaranteed to do *more* damage to themselves.  This model is basically a whale allowing minnows to piggy back on his large stake, presumably for some small fee.

---

**nootropicat** (2018-03-29):

Very good idea, unfortunately multiparty ECDSA generation is very slow. It would work much better with schnorr signatures.

---

**kladkogex** (2018-03-30):

I think once account abstraction is implemented one could do Schnorr signatures (or BLS threshold signatures) …   Hopefully the account abstraction thing should happen soon …

---

**nootropicat** (2018-03-30):

That’s the nice general solution, but schnorr works on the same curve, so adding one bit to v would be enough. Trivial change imo

---

**kladkogex** (2018-03-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/nootropicat/48/258_2.png) nootropicat:

> so adding one bit to v would be enough.

What do you mean by “adding one bit to v”?))

---

**kladkogex** (2018-03-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Also, unless I misunderstand the idea, it creates a new problem in that if threshold of signatures isn’t achieved then the validator will be considered “offline” and suffer whatever penalties are associated with no-show validators.

If you have a 51% whale then if the whale is hacked and its deposit is slashed then everyone is hurt including the small guys.

With majority voting you will need to hack the majority of the small guys to issue a slashing violation. So the system is arguably more secure.

The small guys will have little incentive to stay offline since this will mean they will not be making any money.

---

**nootropicat** (2018-03-30):

ECDSA signature in an eth transaction has three data fields, (r,s) makes the signature itself and v is a number that tells you which one of the four possible public keys that could generate the signature is the valid one.

From

https://github.com/ethereum/pyethereum/blob/develop/ethereum/transactions.py#L84

I see that only two possibilities are allowed (the remaining two are very rare and apparently forbidden), it’s also used to encode transactions that are only valid on one network id. 27 is an arbitrary constant that was copied from bitcoin.

There are three possibilities to put a marker for schnorr signatures in there. One is to include new v values - 0 and 1 - which would limit network ids for schnorr signatures to 12, but allow existing code that expects only ecdsa signatures to function unchanged.

The second is to change v’s encoding so that the lowest two bits are for the signature-v and all higher bits for the network id. Potentially three or more if needed for other signature types. The disadvantage is that it would make v’s interpretation dependent on the hardfork status and create a discontinuity during it.

The third one is to make a magic value (eg. 0) and put v for schnorr in a subsequent data field.

