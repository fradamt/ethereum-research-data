---
source: ethresearch
topic_id: 3812
title: Effectiveness of Shasper slashing
author: dlubarov
date: "2018-10-16"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/effectiveness-of-shasper-slashing/3812
views: 2518
likes: 2
posts_count: 12
---

# Effectiveness of Shasper slashing

Let’s say we have n shards, and s ETH is being staked. If an attacker with s/3 ETH wants to corrupt a single shard, causing two conflicting blocks to be finalized, they only need to vote illegally on that particular shard. So the maximum penalty is s/3n ETH, which seems rather insigificant for large n.

How much trouble could a single-shard attack cause? If shards accepted crosslinks directly from other shards, then a single-shard attacker could create ETH “out of thin air” by [yanking](https://ethresear.ch/t/cross-shard-contract-yanking/1450) the same account to two different shards. As long as the attacker had an extra s/3n ETH to fund a separate liquid account, the attack would be profitable.

My understanding is that, in the long term plan, all cross-shard communication would go through a Casper-based main chain. Is that right? That seems potentially better, but only if main chain committees are larger than shard committees. E.g. if the main chain committee consists of all registered validators, then the penalty for corrupting it would be s/3 ETH, which would be ideal. But such a large committee would present a scalability challenge.

Could you clarify what the long term plan is for main chain mechanics? I’m basically wondering if then penalty for a double spend attack would be on the order of s/3 ETH, or s/3n ETH, or something in between.

## Replies

**jannikluhn** (2018-10-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> If an attacker with s/3 ETH wants to corrupt a single shard, causing two conflicting blocks to be finalized, they only need to vote illegally on that particular shard.

Shard blocks are only indirectly finalized by getting crosslinked from a beacon chain block that is finalized itself. So finalizing a shard block in fact does require misbehavior of 1/3 of the whole validator set and you can slash all of them. As validators are light clients of all shard nodes, they would notice that they’re about to finalize two competing shard blocks.

What could happen though is that they finalize an unavailable shard block (they don’t check for availability), but for this to happen it would require a committee with a dishonest majority which is negligibly unlikely to get sampled if the attacker has only 1/3 of the total stake.

---

**dlubarov** (2018-10-17):

Thanks for clarifying, Jannik.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> the whole validator set

Does this mean that all validators will vote on the main chain? Seems like that would limit the size of the validator set.

---

**MihailoBjelic** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> So the maximum penalty is s/3n ETH, which seems rather insigificant for large n.

As far as I understand, they total amount that will be slashed in this situation is 32ETH x no. of malicious validators in that specific committee (it doesn’t depend or n or s). To put that into fiat perspective, it might be around 32 ETH x 150 validators x $200 = ~$960k. This indeed is not a big amount for a wealthy attacker, but in this case the attacker can not do any damage to the system (the conflicting block will simply get rejected, so she basically got slashed for nothing).

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> If an attacker with s/3 ETH wants to corrupt a single shard, causing two conflicting blocks to be finalized

Let’s assume that, instead of finalizing two conflicting blocks, the attacker wants to finalize a block with incorrect/malicious transactions in it (more likely option IMHO). If I’m not mistaken, she will not be slashed at all? As [@jannikluhn](/u/jannikluhn) noted above, validators are light clients of all shards, so they can not see what’s inside of any block? ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> So finalizing a shard block in fact does require misbehavior of 1/3 of the whole validator set and you can slash all of them.

I’m pretty convinced this won’t work this way. Or if it will, it will limit the validator set (as [@dlubarov](/u/dlubarov) noted), and AFAIK Eth 2.0 plans to have thousands of validators?

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> for this to happen it would require a committee with a dishonest majority which is negligibly unlikely to get sampled if the attacker has only 1/3 of the total stake

I think this is the main line of defense in sharding/Eth 2.0. The probability for a committee with a dishonest majority to be elected is really negligible. But if it happens, they can finalize block with malicious transactions without being penalized at all.

One interesting thing to note here is that Eth 2.0 threat model assumes that majority of validators are rational (not honest). If we really assume this, than it’s perfectly expected for a large group of validators to collude and validate invalid shard blocks (this would allow them to do beneficial things like double-spending without being punished at all). ![:see_no_evil:](https://ethresear.ch/images/emoji/facebook_messenger/see_no_evil.png?v=12)

---

**jannikluhn** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> Does this mean that all validators will vote on the main chain? Seems like that would limit the size of the validator set.

They do (albeit not at the same time), but thanks to signature aggregation the number of validators can still be quite large. See the [spec](https://github.com/ethereum/eth2.0-specs/blob/master/specs/beacon-chain.md) for details.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Let’s assume that, instead of finalizing two conflicting blocks, the attacker wants to finalize a block with incorrect/malicious transactions in it (more likely option IMHO). If I’m not mistaken, she will not be slashed at all?

It is possible to slash for that as well (and make the beacon chain aware of that to prevent/“revert” finalization), but it requires data availability and/or fraud proofs and is left for later the “phases” of the development roadmap. Keep in mind that the first phase doesn’t contain shard chains at all, and the next one(s) simply contain “data” without a notion of transactions.

---

**MihailoBjelic** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> They do (albeit not at the same time)

So basically, they do not. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) You can only slash the dishonest members of the specific committee.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> It is possible to slash for that as well (and make the beacon chain aware of that to prevent/“revert” finalization), but it requires data availability and/or fraud proofs

How can data availability help here? Fraud proofs theoretically can, but what should we do with them? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Force main chain validators to check them before accepting cross-links? That means we’re back to the single-chain scalability (main chain validators have to validate every transaction of the whole system). ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

What can really help in the long run are zk proofs. Actually, if we have efficient proofs for the whole shard activity between the two cross-links, than we don’t even need shard validators **at all**. We only need shard operators and a Dfinity-like main chain (we constantly sample committees from a highly decentralized validator pool) to validate proofs. That would be really good ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12), even though shard operators would remain SPOFs of the whole system, like they are know (primarily in terms of data availability, so there are definitely ways to mitigate that).

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> left for later the “phases” of the development roadmap

I’m thinking in terms of a complete, working system. If we’re building a house but, in the end, it turns out the roof is impossible to build, it’s just a waste of resources to continue with the construction (roadmap). ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Not saying that that is the case here.

---

**jannikluhn** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> So basically, they do not.  You can only slash the dishonest members of the specific committee.

Not sure what you mean, but it takes multiple committees to finalize a block. So to finalize two competing chains, multiple committees need to be dishonest and you can slash those.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> How can data availability help here?

Just mentioning it because publishing unavailable blocks is an important type of attack (and I believe before we get state execution in the shards pretty much the only one possible at that layer of the protocol).

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Force main chain validators to check them before accepting cross-links?

No, but one can use them to “whistleblow” from the shards to the beacon chain if something went wrong.

---

**MihailoBjelic** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Not sure what you mean

I was saying that you can only slash dishonest validators in a specific committee, not the 1/3 of the whole validator set as you said… And if we speak strictly about the main chain, than you’re right in that we need two dishonest main chain committees in a row to finalize two conflicting blocks on a shard. And you can slash only dishonest validators from those two committees, which again is far less than slashing 1/3 of the total stake (your original claim). Please correct me if I’m wrong.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> one can

This phrase/design philosophy keeps popping up in Ethereum research community, while IMHO it **really** shouldn’t. A serious, secure system should never rely on some **abstract** entity that **can** report misbehaviour, it should always have **specific** entities that **will** report it for sure if it happens (because they’re incentivized/bonded to do so).

Besides that, where can we keep fraud proofs for each block for thousands of shards? The only logical answer would be in the main chain (because we have to guarantee their availability), but this is impossible, of course.

---

**dlubarov** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> the attacker wants to finalize a block with incorrect/malicious transactions in it

That’s also a good point, although I don’t worry too much about those attacks since they would need 2/3 stake. If an attacker did get 2/3, I don’t think there’s much we could do to stop them. Let’s say they finalize an invalid block *and* with hold it. I don’t think availability proofs would help, since we would probably want a threshold of 2/3 availability (to tolerate 1/3 offline), and the attacker could prove availability for the 2/3 they control without leaking the block to honest validators.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> They do (albeit not at the same time), but thanks to signature aggregation the number of validators can still be quite large.

But whoever aggregates votes must download them all, right? Although I guess if it was necessary, vote aggregation could become a specialized role, handled by servers with gigabit connections.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> it takes multiple committees to finalize a block

Could you elaborate on that? I.e. I’m wondering

- Is the idea to break up vote data into small chunks, so that each chunk can be aggregated promptly?
- These committees could operate in parallel, right? (If they were sequential, then I don’t see an advantage over one huge committee.)
- Would the union of the multiple committees be the entire validator set, or still a smaller sample?

I just want to get a good sense of the penalties for a double spend attack. The rewards could be very large—in theory, an attacker could double their money (in a separate liquid account) via exchanges or cross-chain swaps—so I think the penalties would need to be on the order of s/3 in order to be really effective.

---

**MihailoBjelic** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> I don’t worry too much about those attacks since they would need 2/3 stake

Didn’t quite get this. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I thought we’re discussing the case where an attacker secures majority of validators in a single committee, and that’s possible with much less than 2/3 of total stake (with varying probabilities, of course)?

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> Could you elaborate on that?

I was convinced [@jannikluhn](/u/jannikluhn) was talking about “justify/finalize” thing, i.e. the fact that we need two committees in a row to finalize a block, but now I’m not sure anymore…  ![:thinking:](https://ethresear.ch/images/emoji/facebook_messenger/thinking.png?v=12) ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

---

**dlubarov** (2018-10-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> I thought we’re discussing the case where an attacker secures majority of validators in a single committee, and that’s possible with much less than 2/3 of total stake (with varying probabilities, of course)

True; I’ve been oversimplifying a bit by assuming that getting p voting power in a single committee requires p stake. It’s true as long as our committees are infinitely large! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Realistically if our shard size is 1000, the stake required to get 2/3 in a single committee would be 55-60%, depending on how lucky/patient the attacker is. 60% would give the attacker a probability of ~7.2e-6.

---

**MihailoBjelic** (2018-10-18):

Exactly, and the probability goes down as the % of malicious stake decreases (but it’s still > 0).

