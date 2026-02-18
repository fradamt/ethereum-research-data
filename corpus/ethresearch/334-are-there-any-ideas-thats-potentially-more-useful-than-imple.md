---
source: ethresearch
topic_id: 334
title: Are there any ideas that's potentially more useful than implementing sharding?
author: jamesray1
date: "2017-12-17"
category: Sharding
tags: []
url: https://ethresear.ch/t/are-there-any-ideas-thats-potentially-more-useful-than-implementing-sharding/334
views: 7897
likes: 8
posts_count: 15
---

# Are there any ideas that's potentially more useful than implementing sharding?

If you know of anything that would be potentially more useful for Ethereum than sharding, please let me know.

## Replies

**jamesray1** (2017-12-17):

Maybe this: [Accumulators, scalability of UTXO blockchains, and data availability](https://ethresear.ch/t/accumulators-scalability-of-utxo-blockchains-and-data-availability/176)

---

**JustinDrake** (2017-12-17):

I think of quadratic sharding as a “uniform” scaling solution which addresses all computational bottlenecks (storage, I/O, computation, bandwidth) simultaneously, and in a similar amount. If we have, say, 100 shards then we get a roughly 100x increase in scalability (ignoring overheads such as cross shard communication). In practice I expect the “main shard” to handle a fixed number of “children shards”, so in practice we may only scale by a multiplicative constant. (I’m hoping this constant is >100, but Vitalik probably has better intuition on this.)

I’ve been exploring scaling approaches that are fundamentally “non-uniform”. The idea is to look at the individual bottlenecks separately, and shoot for exponential scaling (vs multiplicative scaling).

- Storage and I/O: At this point I’m very bullish on stateless clients. Great progress has been made, including miner-updated witnesses, Merkle Mountain Ranges, witnesses in miner data, partial statelessness, accumulator sharding, fancy accumulator schemes, witness provision markets, and storage rent.
- Computation: Two approaches I can see working here are SNARKs/STARKs and interactive verification (TrueBit). Theoretically SNARKs/STARKs are the ultimate solution but we may be years away (maybe 3-10 years) from practicality for scalability purposes. Interactive verification is the low tech solution, but relies on data availability for a large class of applications.
- Bandwidth: This is possibly the hardest one theoretically, and boils down to the data availability problem. I think I have made some good theoretical progress on this front which I will publish on ethresear.ch shortly. My gut feel is that SNARKs/STARKs will play a key role in the solution, making data availability hard both theoretically and practically.

In short, I think the low-hanging fruit is stateless clients. This is especially good news because Ethereum’s current bottlenecks are largely related to I/O for transaction processing (and storage to a smaller extent for the initial sync time). In addition, stateless clients are somewhat of a prerequisite for sharding because they allow for frequent validator shuffling. Given this, I think there is an argument to be made to augment the [sharding roadmap](https://github.com/ethereum/sharding/blob/develop/docs/doc.md#subsequent-phases) with “Phase 0” that implements the stateless client on a *single* shard (i.e. minimal sharding).

---

**jamesray1** (2017-12-17):

Sounds good; there’s lots of ideas and work to do! I started reading Vitalik’s STARKs post today, but then when I got to the link to Matthew Green’s blog post series on zero knowledge I started reading that, then when I got to the link in that series to the random oracle I read that series, plus with lots of reading of other links, which link to other topics, and so on!

I think I’ll finish reading through the sharding doc and the code on Github, then continue with ZKPs and STARKs, then read the rest of your post and the thread, and accompanying links e.g. to the data availability problem. After that I’ll also keep an eye out for more research! I’ve already read Vitalik’s post on the stateless client concept, and yes, it seems relatively simple and nice.

---

**jamesray1** (2017-12-27):

Justin, have you quantified how much different features could improve Ethereum’s scalability, or of storage and I/O, computation and bandwidth? Where can I find more information for all of this research? For instance, if I search for “Merkle Mountain Ranges” in https://github.com/ethereum/research, I get no results. Maybe it’s in the private repo: https://github.com/ethresearch/main, that I and the public don’t have access to? (If I could get access that’d be great.) I remember seeing stuff on storage rent (which would still be useful with stateless clients e.g. for archival purposes), and I know there are articles by Christian Reitwessner and Vitalik on SNARKS & STARKs, which I’m still reading through. I’ve also seen data availability posts on this site, as well as stateless clients. I haven’t read anything about a lot of the topics that you listed for storage and I/O.

---

**kladkogex** (2017-12-27):

justin:

> Storage and I/O: At this point I’m very bullish on stateless clients. Great progress has been made, including miner-updated witnesses, Merkle Mountain Ranges, witnesses in miner data, partial statelessness, accumulator sharding, fancy accumulator schemes, witness provision markets, and storage rent.

Justin - can you explain  how do you see  the witness storage part of  stateless clients?

When a collation is created, the collation will include a header and witnesses - where will the witnesses go?

Will they be stored on a separate “storage market” ?   How is it going to be guaranteed that everyone has access to witnesses?

Let me give you an example.  Lightning Network relies on public availability of all data on the blockchain.  If User X closes a channel in a malicious way,  user Y can monitor the blockchain and react.

How can I monitor events on the blockchain in the stateless client approach?  If  user X issues transactions, how does user Y monitor transactions issued by user X? Should user Y constantly call APIs of  the storage market, because this is where the witnesses will be stored? Or it will be a subset of nodes that stores witnesses and state for a particular shard?

The second big question for me is security of the shards.   Shards per se will be much less secure than the main chain.  If one allows upstream ETH transfers between the shards and the main chain, then if one manage  a zillion of ETH one of the shards, and transfer it to the main chain, then the entire ETH network is going to be compromised.

To compromise a shard though one only needs to compromise validators of this shard.  So it seems to me that allowing any kind of upstream transfers of ETH can severely affect the security model - you will need to only  hack validators of a single shard to compromise the entire network.

---

**JustinDrake** (2017-12-27):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Justin - can you explain  how do you see  the witness storage part of  stateless clients?

Sure. Before I answer the more specific points below, I’ll note that “data availability” is a bit like “decentralisation” in that it can be somewhat of a nebulous term. (It is not an objective thing like validity, it takes different qualitatively forms, and can vary along quantitative continuums.) I will focus specifically on *real-time* data availability, which is the public access to freshly produced mining data (blocks or collations) via network gossip. Real-time data availability emerges from miner incentives, and is present in both the sharded and non-sharded contexts.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> When a collation is created, the collation will include a header and witnesses - where will the witnesses go?

Whenever miner data is created (be it a block or a collation) that data is published to a public gossip feed. In the non-sharded context there’s a single real-time gossip feed, whereas in the sharded context there is one real-time gossip feed per shard. In short, the witnesses get gossiped. A validator cannot build on top of a collation header published on the main shard for which it does not have the corresponding collation body.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Will they be stored on a separate “storage market” ?

Thanks to real-time data availability, anyone who cares about specific witnesses can maintain those witnesses. There are no restrictions as to where storage happens, and there are many setups (such as storage markets) that make sense. To illustrate consider the witnesses for [Kitty #417398](https://www.cryptokitties.co/kitty/417398):

- The owner of #417398 is incentivised to maintain witnesses to maintain effective ownership of the cat.
- The developers and maintainers of cryptokitties.co are incentivised to maintain witnesses e.g. to feed their for-profit marketplace, avoid angry users with unspendable kitties.
- Miners are incentivised maintain witnesses to unlock mining fees by “fillling in” transactions with missing/stale witnesses (c.f. this post).
- Other participants (volunteers who want to support Ethereum pro bono, academics, archive.org, etc.) may also maintain witnesses.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> How is it going to be guaranteed that everyone has access to witnesses?

The point is not for *everyone* to have access to *all* witnesses *at any time*. That’s overkill. It is sufficient to have those who care about specific witnesses have access to those when they need them, and real-time data availability unlocks the possibility for that.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Let me give you an example.  Lightning Network relies on public availability of all data on the blockchain.  If User X closes a channel in a malicious way,  user Y can monitor the blockchain and react.

The same thing works in the stateless client paradigm. Real-time data availability allows user Y to monitor for malicious activity and react.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> To compromise a shard though one only needs to compromise validators of this shard.

That’s not how sharding works (see [rough spec here](https://github.com/ethereum/sharding/blob/develop/docs/doc.md)). Basically every validator works on *all* shards. The validators form a pool and individual validators are given the right to create blocks on random shards. Every “period” the validators are “shuffled”. Stateless clients allow for the period to be kept very short, and for the randomisation process to have a “lookahead” of just a few minutes. So to compromise a given shard an attacker would need the ability to compromise enough validators from the whole validator pool, and compromise individual validators at a few minutes notice.

---

**kladkogex** (2017-12-28):

Justin - thank you very much!!  I understand this much better now!

> The point is not for everyone to have access to all witnesses at any time. That’s overkill. It is sufficient to
> have those who care about specific witnesses have access to those when they need them, and real-time
> data availability unlocks the possibility for that.

Under the system you are describing if I want to transfer my token to Alice, I need to have witnesses for the token contract.  But where am I going to get the witnesses from ?))  If I have 10 tokens of token XYZ I want to get rid of,  I will not be able to to do it unless I have witnesses for the corresponding contract ?))

I am a bit confused how is this going to work,  looks like owneship of a token XYZ is not going be enough, token owners will need to keep on monitoring real-time data for witness updates, otherwise they will not be able to use tokens …

---

**JustinDrake** (2018-01-03):

Yes, effective ownership of tokens in the stateless model requires **both** a private key and a (public) witness. This is certainly a significant shift compared to how things work today, and will require work from the overall community (users, developers, tooling, service providers, …).

We have several pieces of good news:

- Witnesses are a byproduct of real-time data availability
- Witnesses are publicly available
- Individual witnesses are very small
- As I was trying to illustrate with the CryptoKitties example, many parties can be incentivised one way or another to maintain witnesses

Combined, all four points above mean that it is doable to build “L2” infrastructure above the core blockchain to provide anyone who needs a specific witness with access to it. From a research standpoint, we’re trying to make witnesses “friendly” (less frequent udpates, append-only, smaller witnesses, …) to reduce friction for the community.

At a high level, I expect sharding to come with two significant costs for developers: witness management and cross-shard asynchrony. These are real tradeoffs, but IMO they are worth it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**kladkogex** (2018-01-03):

Justin - thank you - just to clarify

Lets assume I have a witness for ownership of a particular ERC-20 token, then at least in the current model, since the Merkle root is changed everytime there is a token transfer, I will have to update my witness everytime someone touches this ERC-20 contract - correct ?)  So I will constantly have to monitor the ERC-20 contract then.

This is something you are thinking about fixing, essentially the idea of a stateless client is not compatible with the current Merkle tree design for the state of a contract, so you want to find an alternative accumulator design so people do not have to update witnesses all the time ?)

---

**JustinDrake** (2018-01-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> since the Merkle root is changed everytime there is a token transfer, I will have to update my witness everytime someone touches this ERC-20 contract - correct ?)  So I will constantly have to monitor the ERC-20 contract then.

With the current trie accumulator, every time someones touches the ERC-20 contract the witness changes. The good news is that we have witness auto-updates (as discovered by Vitalik I think, see [here](https://ethresear.ch/t/the-stateless-client-concept/172)) so users won’t have to make the most recent updates:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[The Stateless Client Concept](https://ethresear.ch/t/the-stateless-client-concept/172/1)

> we put the witness outside the signed data in the transaction, and allow the miner that includes the transaction to adjust the witness as needed before including the transaction. If miners maintain a policy of holding onto all new state tree nodes that were created in, say, the last 24 hours, then they will necessarily have all the needed info to update the Merkle branches for any transactions published in the last 24 hours.

(This was then improved slightly with account abstraction and miner data; see [here](https://ethresear.ch/t/account-abstraction-miner-data-and-auto-updating-witnesses/332).)

IMO at least as powerful as witness auto-updating are Merkle Mountain Ranges (see [here](https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385) and [here](https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287)). They offer the following amazing properties:

[A cryptoeconomic accumulator for state-minimised contracts](https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385/1)

> Low frequency updates—witnesses are updated log(#{updates after insertion}), as opposed to once per insertion for tries
>
>
>
>
> Extend-only updates—the witnesses (Merkle paths) only get extended, as opposed to having internal nodes be modified from unrelated object updates in the trie (this is great for parallelism)
>
>
>
>
> Marginal memory overhead—witness maintenance requires only log(#{objects}) overhead, as opposed to #{objects} overhead for tries
>
>
>
>
> Shorter average-case witnesses—size log(#{updates after insertion}), as opposed to size log(#{objects}) for tries
>
>
>
>
> Shorter worst-case witnesses—size log(#{updates after insertion}), as opposed to size #{objects} for tries

---

**jamesray1** (2018-01-04):

Thanks for the info Justin, keep it coming [as requested above](https://ethresear.ch/t/are-there-any-ideas-thats-potentially-more-useful-than-implementing-sharding/334/5).

For instance, “partial statelessness, accumulator sharding, fancy accumulator schemes”.  However, for accumulators and partial stateleness, there are plenty of search results on this site, so nevermind.

---

**kladkogex** (2018-01-04):

justin:

> we put the witness outside the signed data in the transaction, and allow the miner that includes the transaction to adjust the witness as needed before including the transaction. If miners maintain a policy of holding onto all new state tree nodes that were created in, say, the last 24 hours, then they will necessarily have all the needed info to update the Merkle branches for any transactions published in the last 24 hours.

I see - - this is an interesting idea!)

---

**JustinDrake** (2018-01-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> Where can I find more information for all of this research?

A lot of it is on ethresear.ch now. I’ll try to point out specific references below.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> For instance, if I search for “Merkle Mountain Ranges” in GitHub - ethereum/research, I get no results.

MMRs were first informally described [here](https://github.com/opentimestamps/opentimestamps-server/blob/master/doc/merkle-mountain-range.md), and more formally described under the name of “asynchronous accumulators” (see [here](https://eprint.iacr.org/2015/718.pdf)). I suggest reading these two ethresear.ch threads ([here](https://ethresear.ch/t/a-cryptoeconomic-accumulator-for-state-minimised-contracts/385) and [here](https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287)).

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> Maybe it’s in the private repo: https://github.com/ethresearch/main, that I and the public don’t have access to?

I’d say the research is now pretty transparent and most material is publicly available. Having said that, I don’t have access to that private repo so I can’t tell for sure.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> I haven’t read anything about a lot of the topics that you listed for storage and I/O.

For storage and I/O it’s basically just the stateless client model. There are several posts on ethresear.ch (see [here](https://ethresear.ch/search?q=stateless)).

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> For instance, “partial statelessness, accumulator sharding, fancy accumulator schemes”.

Yeah, terminology gets invented on the fly and I understand it’s hard for an observer to keep track of it. Accumulator sharding is the idea of using multiple accumulators, and [multi-tries](https://ethresear.ch/t/multi-tries-vs-partial-statelessness/391) are a specific instantiation of that. Partial stateless is the idea of maintaining partial witnesses, e.g. in the context of a 2-level state trie where the first level goes as deep as contract addresses, and the second level is for stuff contained *under* the contract addresses (mostly storage), which is itself maintained as a trie. Fancy accumulator schemes is terminology from Vitalik which basically means accumulator schemes with cryptographic assumptions that go beyond secure hashes (e.g. [RSA-based accumulators](https://ethresear.ch/t/accumulators-scalability-of-utxo-blockchains-and-data-availability/176), or pairing based accumulators). It’s euphemistic terminology for “too insecure for the core protocol” ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**jamesray1** (2018-01-04):

![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=9) Haha, OK, thanks. I’ll add all of this to my reading list. At the moment I’m just going through [elliptic curve pairing](https://medium.com/@VitalikButerin/exploring-elliptic-curve-pairings-c73c1864e627).

