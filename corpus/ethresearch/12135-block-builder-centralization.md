---
source: ethresearch
topic_id: 12135
title: Block builder centralization
author: jgm
date: "2022-03-01"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/block-builder-centralization/12135
views: 10303
likes: 30
posts_count: 19
---

# Block builder centralization

A [recent blog post by Vitalik](https://www.vitalik.ca/general/2021/12/06/endgame.html) stated that block production (building) will be “centralized” but does not provide any details about how centralized. Is it possible that we end up with a single block builder?

The ultimate goal for a block builder is to build the highest-value block that it can. To do this, it needs to build from high-value transactions. The combined value of MEV opportunities at any point in time will in general outweigh any delta that could be obtained by smart block building algorithms, so access to a high-value transaction pool will be the defining advantage for block builders.

There is a significant change to transaction inclusion in blocks post-merge. Because validators are considered untrusted, individual transactions or transaction bundles are no longer provided to proposers. Instead, validators are presented with the hash of a list of transactions by the builder. And because validators only have a hash of the full list of transactions the validator’s acceptance is all-or-nothing; it is not possible for a validator to alter the transactions. As such, if a new searcher finds an MEV opportunity they can either build a full block themself or they can submit it to an existing block builder. If they try to build a full block themself they need to build a higher-value block from their transactions and the public mempool than that made by a block builder with access to an existing MEV transaction pool, which is going to be tough. So they are most likely to submit it to existing block builders, increasing the value of the builders’ transaction pools and hence the blocks they build.

Which block builders are they likely to submit to? If they submit their bundle to more than one builder it is possible for one of the builders to reverse engineer the bundle without the searcher being able to identify which builder stole it. This is equally true of sandwich-style transactions, where the builder can remove the “meat” of the sandwich and wrap it with their own transactions, as with more generative transactions such as on-demand liquidity provision, where the builder can supply their own liquidity ahead of the transaction that requires it. If they only submit to a single block builder they need to pick the one that has the most chance of building a block that will be selected by the next block proposer (as many MEV opportunities are time-limited in some way). As such, the only logical choice is to send it to the single builder that already has the highest-value transaction pool. And as searchers are financially driven, they are all likely to make the same choice.

This appears to create a positive feedback situation, leading to the end result of a single large high-value transaction pool, and a single major builder. Smaller transaction pools may survive if backed by validators willing to sacrifice financial rewards for some other value, however for validators that are monetarily-driven they will end up taking the block from the single major builder.

There are various detrimental impacts to having a single block builder, however at this point I’m interested in hearing if others disagree with the above logic and can explain why we will not end up with a single dominant block builder.

## Replies

**MicahZoltu** (2022-03-02):

I think your assessment is sound.  The weak argument I will make is that it is not particularly important that there are many people building blocks regularly, but it is critically important that there are multiple people *trying* to build blocks regularly, even if some of them never succeed.

What we want to avoid is a single builder who goes offline (for any reason) and then all block production halts.  I believe the current plan in all execution clients to deal with this is to fallback to building a block from the public gossip transaction pool if no block builder proposes anything better.  However, I do worry about all transactions moving over to private channels with the one builder, and then when it goes offline there are no transactions in the public gossip pool.

Note: The above assumes that we have must-include transaction lists to protect against single-builder censorship.

---

**simbro** (2022-03-23):

If we reach the stage that for every block that a proposer proposes, they have the choice between taking a block from their local execution client, (based on transactions from the public mempool), or a block from some MEVA relayer.

If the blocks being offered by relayers are consistently worth more to proposers than the blocks they can get from their local execution clients, then the transactions in the public mempool just aren’t going to get processed.  It follows then that wallet vendors would stop sending transactions to the public mempool by default.  The public mempool would simply “dry-up”.

I’ve read through the [discussions](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980) around the implications of block builder centralization to censorship resistance, and where the author  explains very eloquently that it would be economically prohibitive for a block builder to censor a transaction indefinitely, this argument seems to be predicated upon the assumption there is a viable alternative that the sender can submit their transaction to.

Simply: if there is a single dominant block builder, AND if there isn’t sufficient transaction volume in the public mempool to compete against the blocks it produces, (to the extent that no blocks are ever proposed that contain public mempool transactions), then users will have no alternative but to submit their transactions to the dominant block builder.

If this block builder goes off-line, or decides to stop producing blocks for some reason, then everyone can just fall back to the public mempool, and everything keeps going.  But what about if we’re only talking about very specific transactions that are targeted by the block builder.  Surely they can be vulnerable to being censored under the above scenario?  In this case, the targeted users would probably need to broadcast to the public mempool with a hugely inflated priority fee, in the hope that it might get picked up by a proposer at some stage.

To my mind, the main question seems to be: if this scenario emerges, how long will that take and will there be enough time to decide on a mitigating approach and implement it (e,g, crLists or similar)?

---

**MicahZoltu** (2022-03-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/simbro/48/3821_2.png) simbro:

> In this case, the targeted users would probably need to broadcast to the public mempool with a hugely inflated priority fee, in the hope that it might get picked up by a proposer at some stage.

There has been discussion about making it so proposers would include a list of transactions when they propose a block that **MUST** be included in a future block if the transactions are still valid.  The idea here is that proposers can ensure that transactions from the mempool aren’t being censored by builders, even if there is only one builder that everyone uses.

---

**simbro** (2022-03-24):

I guess the question I was posing was whether anyone could confidentially speculate on how long a protocol level mitigation (such as crLists etc.) would take to roll-out vs. how much time we might have before the empty-mempool scenario is realized?  I know that it’s all just conjecture at this point, but probably worth thinking about nonetheless.

Thinking out loud: perhaps the most important step in the near-term would be to monitor the number of transactions in proposed blocks that weren’t detected in the public mempool. This could be an important velocity to track to indicate mempool health.

---

**MicahZoltu** (2022-03-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/simbro/48/3821_2.png) simbro:

> Thinking out loud: perhaps the most important step in the near-term would be to monitor the number of transactions in proposed blocks that weren’t detected in the public mempool. This could be an important velocity to track to indicate mempool health.

I’m a huge fan someone setting up monitoring of this and tracking it over time on a dashboard somewhere so we can see how big of a problem it is becoming.

---

**pmcgoohan** (2022-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> A recent blog post by Vitalik  stated that block production (building) will be “centralized” but does not provide any details about how centralized. Is it possible that we end up with a single block builder?

So I’m [probably responsible](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/2) for this (I’ll let Vitalik correct me if I’m wrong). Thank you for discussing the issue further.

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> There are various detrimental impacts to having a single block builder, however at this point I’m interested in hearing if others disagree with the above logic and can explain why we will not end up with a single dominant block builder.

That won’t be me! I’m afraid your concerns are valid.

If you haven’t read [my posts](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/2) on this I urge you to. Flashbots style full block auctions incentivize both private dark pools and the formation of censorship-as-a-service markets (bribes to exclude other people’s transactions). Both of these come with powerful network effects.

The dominant builder will be the most exploitative by definition, and the endgame is a perfect extortion economy (maximal taxes levied on transactors) that fails to compete with centralized alternatives.

CaaS undermines the whole idea that bribery ordering (and therefore Ethereum) can be censorship resistant because you can be bribed more to exclude a tx than to include it. That is not a small point, it’s fundamental. Getting paid to censor is MEV too (what I call Private MEV).

Flashbots position on MEV is that if it can be extracted, it will be. As such, they should believe more than me that CaaS is inevitable. By their own logic, they *must* allow censorship and censorship markets or they will be limiting MEV extraction and will therefore create an incentive for extractors to buy validators and centralize.

As significantly, because we have seperated block building from the need to own a validator, there is no requirement for the dominant builder to have an Eth denominated stake at risk. They can exchange the funds needed to win blocks in auction just-in-time. As a result, if the value they can extract from blocks results in damage to Ethereum/Eth price, it may actually be in their interests to do so (quite unlike the assurances of a 51% attack). I call this the Unstaked Hijack.

All of this comes from the long term issue of block content being fully trusted/centralized in Ethereum. Full block Flashbots auctions represent a full and final failure to address this and will have severe consequences.

I have been charged with organizing a discussion group about this with some Flashbots people and other interested parties in a few weeks time. Perhaps you’d like to take part?

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> Which block builders are they likely to submit to? If they submit their bundle to more than one builder it is possible for one of the builders to reverse engineer the bundle without the searcher being able to identify which builder stole it.

Yes, this is a very good point.

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> because validators only have a hash of the full list of transactions the validator’s acceptance is all-or-nothing; it is not possible for a validator to alter the transactions

It is literally banning altruism.

[@fradamt](/u/fradamt) proposed crList after I discussed these issues with him. It’s preferable to nothing, but formally non-existent in that it relies on altruism and is less censorship resistant than what we have under PoW now.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> The weak argument I will make is that it is not particularly important that there are many people building blocks regularly, but it is critically important that there are multiple people trying to build blocks regularly, even if some of them never succeed.

I’m glad you appreciate that is a weak argument. I would say that despite other people trying to build blocks regularly, it does not alter that a dominant builder will likely monopolize block content in the ways I have described above. Arguably, it just means they have to be more exploitative to maintain their position.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I’m a huge fan someone setting up monitoring of this and tracking it over time on a dashboard somewhere so we can see how big of a problem it is becoming.

You’ll be able to do that with my zeromev project (launching in a few weeks). It tracks exactly which transactions were inserted by miners and which are from the mempool in each block.

But why wait for it to happen? It’s like running Ethereum on a single node and waiting until it double-spends to decentralize it.

I think we need to look very seriously at base layer [decentralization of content](https://ethresear.ch/t/shutterized-beacon-chain/12249) proposals like this one instead (my only real objection to this being that it is optional).

---

**simbro** (2022-04-01):

After posting previous reply, I realized my thinking was totally flawed: so long as there are blocks that are less than full at any stage, then of course a block builder will take every available transaction to build a block, including those from the public mempool. I completely agree that there is definitely scope for censorship if there is a single block builder.  As such I think there’s  merit in tracking the change in public mempool volume in relation to total transaction volume over time, as a means to understand the growth of private channels. Very interested to find out more about zeromev.

---

**pmcgoohan** (2022-04-01):

I’ll take your word for it that your thinking was flawed, but [@jgm](/u/jgm)’s logic is solid.

I don’t see this as a maybe-this-might-happen-let’s-see kind of thing. The point is that MEV-Boost incentivizes block content centralization, and that this has gone unnoticed by the authors.

---

**jonreiter** (2022-04-18):

the phrase “perfect extortion economy” captures this very well.  and completely agreed this tendency may be very strong.

it’s not clear to me, however, that this is something to be solved *inside* the protocol.  if the market doesn’t value competition for block construction – if the market doesn’t care about the extortion thing – it’s not clear how you can force it in there.  if a single entity assembles blocks and there is high demand for blockspace: ok. if these monitors run and find problems and nobody cares: ok.

if the market does care then demand for blockspace depends on block-construction-competition and we find a level. and the users/providers subsidize the monitoring processes and additional block assembly resources etc.

if nobody is willing to stump up for this and blockspace is still expensive…that’s a pretty clear sign of something. raising the issue plays a role, sure.  and advocating to address it.  it is however hard, for me at least, to see a solution within the protocol.

---

**gavinyue** (2022-04-19):

I do not feel it is “extortion”.  The transaction owners, who are willing to pay more in gas for front-running, are also extracting value, aka making profits, from their perspectives. It requires them to invest more to gather all the information to gain the required insights for arbitrage.

So I understand why Auction-method is proposed to “solve” this problem.

By introducing builders,  builders also will go through the same process to implement the best strategy to benefit themselves and the proposers.  They will co-operate or even collude with proposers to find the perfect balance.  Operation-excellence here means 1. having the best intelligence infra to extract the most value and 2. can find the perfect balance with proposers to share the value.

So after a period of competition, the builder who operates best will start to dominate the block building business.

---

**gavinyue** (2022-04-19):

I feel we will end with three situations: 1. Dark TX pool, 2. Public Auction market, 3. Builder dominators.

And considering the current consensus rewarding, I feel the major problem is that the whole system is benefiting “RICH”.

So I propose a much simpler solution here,  in the single block, the transaction gas fee’s distribution must have a standard deviation larger than a value to be a valid block.  It means miners/validators can include transactions with higher gas to benefit themselves, but they must also include transactions with lower gas to democratize access.

---

**jonreiter** (2022-04-20):

to be clear i (and i suspect others) agree with you it is fine for your “transaction owners” to bid higher gas and there is no negative connotation intended. the concern is a monopoly block builder going the other direction: “pay me x or i won’t include your block.”  if there is a competitive market on both sides – much as some of what you describe – yeah all fine.

re the standard deviation thing: is that computationally feasible? it feels like a classic hard decision problem (to me at least) to even figure out if such a subset of transactions exists.

---

**gavinyue** (2022-04-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonreiter/48/8910_2.png) jonreiter:

> re the standard deviation thing: is that computationally feasible? it feels like a classic hard decision problem (to me at least) to even figure out if such a subset of transactions exists.

It is possible for a block-builder to take the majority, like more than 80%, of the block-building business. But it is unlikely there would be only one block-builder. So as long as there is one honest block-builder, your transactions will eventually be included.  And under the current design, validators could also outsource the block-building work to third parties privately.

And the standard-deviation idea is not mature yet.  I understand there are probably not enough suitable transactions available in the mempool to construct the valid block.

So here is one variation.  Let us assume EIP-1559 is ready. The fee includes the base fee plus the priority fee.  In each block, there should be a percentage, for example, 15%,  of transactions that do not have priority fee or the priority fee is not charged. If there is only one transaction in the block, then that transaction should not be charged with a priority fee.

This idea is mainly inspired by the solution in affordable housing that the newly built apartment building should a ratio of rooms for low-incomes.

---

**simbro** (2022-05-13):

This idea seems similar to the [Committee-driven MEV Smoothing](https://ethresear.ch/t/committee-driven-mev-smoothing/10408) proposal, is that similar to your thinking?

To my mind, there is a non-neglible risk of a single dominant block builder.  Who that block builder is may change over time, but the role will remain largely the same.  Hopefully the worst negative externalities of a monopolistic block builder will not come to pass, but if they do, they could include censorship-as-a-service techniques such as:

- Favoring one L2 over another (e.g.:  block builder:  “I’ll push all transactions with significant calldata into every third block, except your transactions - for a fee”)
- prioritizing withdrawals from certain exchanges over other ones (for a fee)
- delaying all transactions to one or two specific high-volume liquidity pools, and putting them all in one block to benefit fro a larger price impact
- demanding higher fees for time sensitive transactions
- etc.

I’ll admit I haven’t thought through these scenarios on a deep level so it would be great to get some other perspectives.  That being said, MEV smoothing techniques and other fair-ordering techniques may not fully solve these issues (if they do become issues of course - for now it’s purely theoretical).

---

**gutterberg** (2023-05-27):

Do you know whether a dashboard currently exists with information on the proportion of non-public transactions in proposed blocks?

---

**gutterberg** (2023-05-27):

Are you aware of whether such a dashboard has been created yet? Seems like very useful information to track.

---

**barnabe** (2023-05-27):

Here is such a dashboard, without the proportion but the absolute number: [Mempool Inslight | Privately Mined Transactions](https://mempool.guru/pmt)

---

**simbro** (2023-05-30):

I wasn’t aware of this dashboard, this is very useful (and in particular to [@gutterberg](/u/gutterberg) 's question).

Does anyone know of a consolidated list of relevant dashboard’s or datasources that are relevant to centralization?

