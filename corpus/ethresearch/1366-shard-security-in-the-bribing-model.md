---
source: ethresearch
topic_id: 1366
title: Shard security in the bribing model
author: JustinDrake
date: "2018-03-12"
category: Sharding
tags: [security]
url: https://ethresear.ch/t/shard-security-in-the-bribing-model/1366
views: 4343
likes: 1
posts_count: 7
---

# Shard security in the bribing model

**TLDR**: We play devil’s advocate ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9) and consider that the security of sharding may be broken in practice.

**Background**

For the security analysis of a protocol it is natural to consider two types of participants:

1. Honest: A participant following protocol rules.
2. Rational: A participant maximising profit.

I’ll call a participant “malicious” if it is neither honest nor rational. It is intuitively reasonable to assume that the vast majority of participants are non-malicious, i.e. either honest or rational. In the context of a bribing attacker we cannot both have an honest majority and a rational majority. The reason is that honesty and rationality are at odds. A non-malicious participant either needs to be honesty-favouring or rationality-favouring when a briber offers a financial incentive to deviate from the protocol rules.

The rational majority assumption is strictly stronger than the honest majority assumption. Intuitively we know that decentralised protocols are incentive-driven, hence that we should ideally be assuming a rational majority. The security of Ethereum under the bribing attacker model is proportional to the block rewards (protocol subsidies plus transaction fees). The reason is that, in a rational majority, it suffices for a briber to outbid the block rewards to have the majority of miners mine on the briber’s fork.

Because the block rewards in Ethereum are high (over $10 million per day) the main chain enjoys a decent amount of security. Moreover, there is significant friction for a bribing attacker to build good-enough bribing infrastructure. These two considerations are probably why bribing attacks have stayed in the realm of academia and were never attempted in practice. In other words, the honest majority assumption was never put to test, and we don’t know if it holds in practice.

From a theoretical standpoint, attacking an individual shard is similar to attacking the main chain. Unfortunately, in practice, the situation for an individual shard is much worse than for the main chain, both in terms of cost of attack and in terms of bribing infrastructure.

**Cost of attack**

Let’s first look at the cost of attack.

- Subsidies: The COLLATOR_REWARD is provisionally set at 0.001 ETH per collation. In the best case a collation is created once every 5 blocks, corresponding to 1.152 ETH per day. The current subsidy in the main chain is over 20,000 ETH per day, so subsidies are about 17,500 times lower in an individual shard compared to the main chain. At current market prices, subsidies would provide $0.72 per 5 blocks per shard, i.e. $829 per day per shard. Note also that in the medium-term the collator subsidies are “virtual ETH” in the sense that they are non-fungible with ETH, and so will likely be worth less than “real” ETH.
- Transaction fees: As a scaling solution sharding should dramatically reduce transaction fees. Vitalik estimates that fees for a collation should not exceed $50. Assuming conservatively that all collations in a shard have $50 transaction fees, that’s $57,600 per day.

Adding subsidies and transaction fees, it seems that the cost of a bribing attack on a single shard is on the order of $100,000-$1,000,000 for a full day of transactions.

**Bribing infrastructure**

In the context of proposer-validator separation, the proposal scheme provides excellent infrastructure for a bribing attacker to take advantage of. The bidding mechanism allows a briber to pay rational validators to build on the fork of the briber’s choosing.

The bribing infrastructure is ideal for several reasons:

- Trustless: Validators can receive bribes trustlessly.
- Free: The infrastructure comes out of the box for free with sharding phase 1.
- Quality: It was designed, built and tested to a high standard by a world class team before release.
- In-band: It is an “in-band” bribe, as opposed to being an ad hoc out-of-band bribe, e.g. coming from some other blockchain.
- Protocol-level: Validators do not need to follow an ad hoc smart contract.
- Plausible deniability: The validators benefit from some level of plausible deniability because of fork choice subjectivity.

**Conclusion**

The proposal mechanism makes attempting a bribing attack on a shard technically easy. Combined with the low cost of attack, it seems likely that bribing attacks will eventually be attempted on individual shards. When this happens the honest majority assumption will be put to test and we may discover it is inadequate in practice.

## Replies

**djrtwo** (2018-03-12):

An attack, in practice might look like the following:

- attacker spends coins on shard N in collation Z
- 50 collations are built on top of the collation Z so the recipient of attacker’s coins assumes they are ‘confirmed’. Head of shard chain is collation (Z+50)
- attacker takes on the role of proposer and begins proposing a new collation Z’ on top of collation (Z-1). The proposer bids greater than ~$50, thus outbidding all rational proposers who’s bids would not be greater than the transaction fees in a collation.
- attacker continues to propose and build on Z’ until attacker has gotten collators to build up to collation (Z+51)’, resulting in a new head of that shard, reverting the previous spend of the attacker’s coins.

The cost to the attacker would be C * 51, where C is some number greater than the rational proposer bid which has been estimated at no greater than $50. The cost to the attacker to perform a 50 collation revert under a rational validator majority assumption would be on the order of $2500.

Very cheap compared to reverting on the main-chain. Taking this into account, we would likely see standards in a shard transaction being considered “confirmed” be much much longer than a main chain confirmation.

---

**vbuterin** (2018-03-12):

Two immediate thoughts:

1. This is a good argument for (i) adopting JMRS, so validators do need to care about collation unavailability, and (ii) paying proposer -> validator fees in-shard-chain rather than in-main-chain. If we do this, then the value of an “in-protocol bribe” to build on for some off-head collation C* would only be equal to fee * probability_that_C*_becomes_main_chain, and generally for any collation that’s not the head that probability is quite low. It becomes higher if you assume everyone starts taking the bribe at the same time, but even still this requires coordination, so it’s a significant security boost.
2. The only solution I know of for increasing the cost of bribing validators for being inactive, or for building on the wrong chain, further is the Casper FFG leak mechanism, where if the chain detects a high degree of non-participation then every validator not building on the head chain gets penalized a greater and greater amounts until that stops being the case.

---

**erikryb** (2018-11-19):

What is the status of this? Is the current sharding proposal considered secure in the bribing model, and if not, what are the possible solutions as for now?

---

**vbuterin** (2018-11-19):

A lot of the issues brought up here have to do with an older protocol which no longer applies.

I think in general, our approach is to patch up any issues related to committees being bribeable with [data availability proofs](https://arxiv.org/abs/1809.09044) and fraud proofs.

---

**JustinDrake** (2018-11-19):

The situation is better with the latest design for a couple reasons:

1. As Vitalik points out, we moved away from the proposer-validator separation paradigm which had a bribing vulnerability baked in.
2. With the advent of proofs of custody the cost of bribing to break data availability includes deposits (in addition to the significantly smaller subsidies and transaction fees).

The main defence we have against bribing is infrequent shuffling of persistent committees which secures against a “slowly adaptive attacker”. Things that can help address adaptive attacks:

- Data availability proofs: Allows for clients to be aware of availability, securing the data layer.
- Stateless clients: Allows for ultra-fast shuffling of executors, securing the state layer.
- More stake: A larger validator pool increases the stake of proposer committees.
- Reduced randomness lookahead: Lowering the amount of time randomness is known by an attacker before it is used.
- Private leader election: Helpful for censorship attacks, especially networking DoS.
- Join-leave attack mitigations: Following Dfinity’s latest research we may add defences such as the “Cuckoo rule”.

---

**dlubarov** (2018-11-19):

Using similar techniques to the ones you mention, isn’t it possible to defend against a perfectly adaptive attacker? That is, assume that bribers and bribees coordinate attacks using a lightning fast protocol. I think we can still design things in such a way that attackers have no influence over the shards they’re assigned to.

If validators are stateless, we can do something like

1. In epoch t - 3, validators who wish to register for epoch t register to do so.
2. In epoch t - 2, everyone contributes a VDF input for epoch t's seed.
3. In epoch t - 1, the VDF is computed, resulting in a seed r.
4. In epoch t, each validator who registered is assigned a shard based on r.
5. In epoch t + 1, each of these validators is evicted.

(To avoid gaps, we can allow validators to register for epoch `t` while they’re currently staking, as long as they’ll be evicted before `t`.)

If validators are stateful, we won’t want to evict them all at once, but we can just keep them in a shard for, say, 5 epochs. The timing of validators entering and exiting shards should naturally be staggered, since different validators started at different times. We can even let validators decide how long they wish to stay in a shard, as long as they make that decision before `r` is known.

The key thing is that validators must register before knowing `r`, and must never be given a choice about when to withdraw. As long as that’s the case, it shouldn’t matter how quickly or slowly attackers can adapt, right? The best they can do is repeatedly register all their accounts for the minimum duration, and hope to get lucky.

