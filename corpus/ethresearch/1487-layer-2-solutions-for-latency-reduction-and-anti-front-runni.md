---
source: ethresearch
topic_id: 1487
title: Layer-2 solutions for latency reduction and anti-front-running
author: vbuterin
date: "2018-03-24"
category: Layer 2
tags: [front-running]
url: https://ethresear.ch/t/layer-2-solutions-for-latency-reduction-and-anti-front-running/1487
views: 3168
likes: 2
posts_count: 5
---

# Layer-2 solutions for latency reduction and anti-front-running

Just like we can have applications that run under alternative execution engines (cf [@JustinDrake](/u/justindrake)’s recent ideas) that have different tradeoffs and properties from the main execution engine, we can also have applications individually choose their block proposal mechanisms.

Anyone can create a second-layer proposal mechanism, that consists of two parts. The first part is an off-chain layer consisting of various participants that actually performs block creation. The second is an on-chain contract which is capable of interpreting and verifying the output of the first layer, and then forwarding it - that is, the transactions sent to the off-chain layer would be of the form `[to, data]`, and the contract would make a series of internal transactions (aka calls), sending the desired data to the desired recipient for each transaction that the proposal mechanism accepted, in the order that the proposal mechanism specifies.

The proposal mechanism would be able to cryptoeconomically commit to including transactions potentially much faster than the block time. Additionally, to preserve censorship resistance a mechanism could be added where a user can call the contract with a transaction, and the proposal mechanism would be required to include it within some number of blocks. Alternatively, commitments could be based on internal order: the proposal mechanism could safely make an absolute cryptoeconomic commitment to include some transaction T before including any other transactions outside of some list of transactions that have been committed to already.

Unlike Plasma, this *does not* improve scalability, but it does improve latency, as well as front-running resistance. This could be useful for on-chain decentralized exchanges, auctions and other highly time-dependent systems. That said, Plasma itself can also be used as an engine for experimentation in alternative proposal mechanisms with similar properties.

## Replies

**phil** (2018-03-24):

Can you give a concrete example of the “proposal mechanism”?  It seems perhaps to be punting ordering to another system that would then be vulnerable to the same kinds of frontrunning, which I’m unsure is an improvement over status quo.  In general, frontrunning resistance requires data hiding from the orderers, and it’s not clear yet to me what a concrete scheme would be for accomplishing this.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> it does improve latency

This sounds somewhat similar to Thunderella, an off-chain fast confirmation layer that falls back on a blockchain when it fails.  In the specific context of ETH sharding, my main concern is the size of the barrier to fake confirms in this model.  Specifically, the proposal mechanism may not get a chance to include the proposed body in a collation before a conflicting body is included, invalidating all the confirmed transactions (the cost of this attack in the current sharding model seems to be only the size of the total fees + 1, aka the amount required to outbid this collation on a block before it).  Of course, if collators could commit cryptoeconomically in advance to accepting a collation body from a particular proposal for prepayment, you can perhaps mitigate this somewhat.

---

**vbuterin** (2018-03-24):

> Can you give a concrete example of the “proposal mechanism”?

1. Dominic Williams’s leader-free asynchronous consensus algorithms.
2. PoS on top of data that’s encrypted by time-lock encryption, or alternatively some kind of commit-reveal scheme.
3. Sticking transactions encrypted by time-lock encryption directly into the blockchain, and then cryptoeconomically requiring the propose to decrypt them within some period of time; a transaction can only be forwarded once it is decrypted and once every transaction before it has been forwarded.

I’m not suggesting “enshrining” any of these; I’m simply pointing out that this is a somewhat fungible class of service, and there can be a second-layer market for such services.

---

**phil** (2018-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I’m not suggesting “enshrining” any of these; I’m simply pointing out that this is a somewhat fungible class of service, and there can be a second-layer market for such services.

Ah, I see.  So this post is saying “no need to enshrine frontrunning resistance, let mechanisms compete on Layer 2”.  I totally agree, though this doesn’t really need to be done at the proposal level.  You can have transactions in a single block leveraging multiple such mechanisms.  I’ve discussed “frontrunning resistance contracts” based on everything from commit-reveal to EIP86/Submarine to etc.  Of course the only issue is censorship based on destination contract, but collator-level censorship against proposal mechanisms they don’t like is a natural analogue in this model.

I agree that no such mechanism should be enshrined because there are a number of trade-offs that need to be made.  e.g. for some applications, the existence of a transaction is too much information to leak (Hydra bounty claim / bug withholding), whereas for others, a lighter weight commit/reveal scheme is plenty.

---

**zmanian** (2018-04-02):

Honeybadger style leader free block proposers with threshold encryption are also very compelling.

My principal worry in this area is the ability for a small stake participant in the the threshold signatures to eliminate protection by aborting the distributed generation for the threshold pub key creation.

Most schemes for the DKG I’ve seen don’t permit strong attribution of parties the send malformed messages.

