---
source: ethresearch
topic_id: 2286
title: Casper FFG leniency tweak
author: dlubarov
date: "2018-06-19"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/casper-ffg-leniency-tweak/2286
views: 2455
likes: 7
posts_count: 5
---

# Casper FFG leniency tweak

This is a pretty minor tweak, but it could give faster finality in certain cases. Commandment II states

> a validator must not vote within the span of its other votes.

Note that this is stricter than necessary. For the safety proof to work, a validator must be prohibited from casting a *finalization* vote within the span of another vote; it’s not necessary to prohibit *any* vote within the span of another vote. (A “finalization vote” is a vote from some checkpoint c to a direct child of c.)

Here’s a combination of votes which would be prohibited by the current Commandment II, but permitted by the more lenient variant. The gray nodes are justified, and the green arrows represent votes.

[![casper](https://ethresear.ch/uploads/default/original/2X/2/25c4ab0021108c154fdd5ad40990c7fb4d19e597.png)casper253×443 21.6 KB](https://ethresear.ch/uploads/default/25c4ab0021108c154fdd5ad40990c7fb4d19e597)

For this pattern of voting to be rational, we also need to tweak the fork choice rule. It currently states

> FOLLOW THE CHAIN CONTAINING THE JUSTIFIED CHECKPOINT OF THE GREATEST HEIGHT

If we interpret this 100% literally, it’s not quite optimal. Block creators want to maximize the weight of their fork after their own block is added, not before. So if a block creator sees a supermajority for `1 -> 5b`, they should follow `5b` and make it justified, even though `5a` had the greater weight before.

Consider a voter who has already voted `2a -> 4a`. It’s time to vote for \text{h} = 5, and they observe that `1 -> 5b` is close to a supermajority. (This wouldn’t happen if all validators had perfect information, but most of the network might not be aware of `2a`’s justified status.)

With the previous rule, this validator’s vote has no use. They can either abstain, or vote `2a -> 5a` which is doomed to fail. With the more lenient rule, they can vote `1 -> 5b` to increase the chance that `5b` becomes justified. If it does, that’s good for the network, since it creates an opportunity to finalize a checkpoint next time.

I’m thinking of using this Casper variant in a new protocol, so please let me know if anything doesn’t seem right ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) .

## Replies

**vbuterin** (2018-06-23):

Seems reasonable to me.

---

**dahliamalkhi** (2018-09-19):

Nice post.

I believe that you can find relevant material [here](https://dahliamalkhi.wordpress.com/2018/03/13/casper-in-the-lens-of-bft/): The weaker voting/slashing rule is already assumed in this post. The post sheds further insight on Casper using a BFT lens.

---

**dlubarov** (2018-09-20):

Thank you for the link! It sounds like these are the differences between Hot-Stuff and Casper?

1. The weaker voting rule is used.
2. Votes are sent to an aggregator, who broadcasts a threshold signature.
3. Commit certificates are presented on-chain.

Re #2, it seems alright for Casper to do n-to-n propagation within a shard, since there’s only one round of voting per block (or 100 blocks?), and the votes would probably be small compared to transaction data. But I think the Ethereum devs are planning to use BLS (or possibly SNARKs?) for vote aggregation, so that small certificates can be presented to other shards, and maybe to light clients.

---

**dahliamalkhi** (2018-09-22):

yes, good summary! and indeed, 1, 2, and 3 are orthogonal, you can have each one without the others.

