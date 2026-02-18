---
source: ethresearch
topic_id: 23531
title: "Trustless payments: right vibe, more trust?"
author: alextes
date: "2025-11-25"
category: Consensus
tags: [mev]
url: https://ethresear.ch/t/trustless-payments-right-vibe-more-trust/23531
views: 438
likes: 16
posts_count: 4
---

# Trustless payments: right vibe, more trust?

opinion, not research.

**trustless payments might make ethereum *more* reliant on trust**

*disclosure: nice to meet you, alex, co-founder of ultra sound, we run a block relay. trustless payments may end relays. at least in their current form. i am therefore obviously biased. i try to be more truthful still. i’ll leave the judgement to you (:*

EIP-7732 buys us something real: pipelining. decoupling beacon and execution blocks gives builders more time, supports larger blocks and higher gas limits, and avoids increased hardware requirements for solo stakers.

bundled into that change is “trustless” builder payment. sounds like a strict improvement over trusting relays. may not be that simple.

## today: public relay auctions

most blocks come from a small set of builders (Titan ~50%, BuilderNet ~35%, Quasar ~15%), and relays (ultra sound ~40%, bloXroute ~30%, Titan ~30%). out-of-protocol blocks pay low hundreds of millions per year. protocol rewards are some ~4x - 10x higher still.

relays run **open first-price auctions** and have invested over many months to enable any anonymous builder, to submit any bid they’re able to pay, without collateral, to any proposer open to an out of protocol bid.

as these auctions are **fast and incremental**, builders can place thousands of tiny bid updates per slot, quickly converging to roughly a *second price,* landing the highest value block, while paying close to second price. caveat: insofar as top builders are competitive.

fair to note, relays are trusted intermediaries. far from ideal, and frankly against ethereum’s core values. this trust is spread across multiple operators, under strong reputational and economic pressure, and currently **open and relatively easy to enter** for new builders.

## what trustless payments change

trustless payments introduce a new option. a relay publishes an auction and reveals the best public bid. a selfish builder watches that and sends the proposer a *slightly higher, trustless* bid directly, and privately. the proposer rationally takes the higher bid; the relay and the present-day builder lose.

had that block gone through a relay, dominant builders would likely have outbid it. with public bids plus private, trustless outbidding, those dominant builders are now punished for revealing their valuations.

the rational response is to **stop revealing**. builders start bidding privately, trustlessly, directly to proposers instead of via relays.

in principle, this defensive behaviour could be limited to “slots where a relay is bypassed.” in practice, this may be hard to predict. so incentive spills over: stop revealing everywhere. the result looks like a **first-price sealed-bid auction direct to proposers and the set of builders equipped to compete blind**, instead of an open public auction on relays.

some therefore expect: worse price discovery, harder entry for new builders, and increased edge in trusted relationships with proposers.

it is fair to note this equilibrium collapse is possible today. eg titan runs a competitive relay and promises to keep it open today, but we should assume tomorrow is hard to predict. rumors exist some relays may attempt to offer builders sealed bid functionality. this warrants a larger discussion but imo the current equilibrium feels defensible. certainly more so without trustless payments.

to offer another fair counter, coordination failures can be overcome. eg builders and relays may be able to coordinate around **sealed-bid** **second-price** (Vickrey) auctions with strict policing of bids at the proposer level. note this feels complicated, brittle, and socially hard to enforce.

## trustless != low-trust, diverse

trustless payments fix a narrow problem: the trust we place in relays. they do *not* fix the broader forces that concentrate block building: winner-take-most dynamics, private orderflow, capital intensity, infra moats, and speed that compounds.

so while trustless payments make it *possible* for any builder to pay any proposer, they don’t make it *likely* that meaningful new builders will appear or thrive. if dominant builders switch to sealed-bid private strategies, the system may end up more concentrated and more reliant on trust between proposers and a few builders, not less.

## mechanical downsides of trustless bids

on top of the game theory, trustless bids have real operational limitations:

- can’t be cancelled when sent over p2p.
- must be rate-limited when sent over p2p, or they become a DoS vector.
- require deposited collateral (iiuc the sum of all promised payments in an epoch).
- builders must pay the full sum for missed blocks.
- they cannot promise additional preferences like eg OFAC filtering, or preconfs.

to alleviate some of these downsides, builders may encourage proposers to **whitelist** them to fetch sealed bids directly. an advantage for well connected builders. worse, all downsides above may be alleviated with tight integration and deeper trust still, allowing builders to offset risk and offer more competitive bids.

that’s a worse version of the uncomfy structure we worry about today: a handful of highly optimized builders, in tight loops with proposers, dominating a sealed-bid game that’s difficult for new entrants to crack. meanwhile, relays lose meaningful bid flow as those builders avoid exposing bids publicly and the relay layer withers.

## compelling upside

there *is* a strong upside story for trustless payments: imagine Ethereum under heavy attack, local block building is no longer feasible, existing builders and relays are censored or compromised, and new builders can only appear pseudonymously over the p2p network.

to some extent, we’re already partway there in practice: a lot of valuable flow is private, and many blocks are built downstream of opaque orderflow pipelines rather than by proposers themselves.

in the extreme case, trustless direct bidding from anonymous builders could help Ethereum keep producing blocks even when “official” builders and relays are toast. you might also imagine “pirate relays” that spring up in emergencies to coordinate this.

i do question how likely that world is, and whether we want to risk **re-shaping today’s relatively healthy equilibrium** for it.

## concluding

pipelining is great, ship it. imo the risk of increased missed slots may well be worth the scaling, and can be pushed back on both in-protocol, and even through trusted relays ha.

trustless payments otoh may come at a high cost. the worry of current out-of-protocol actors is that they may:

- weaken the incentive to participate in open, public relay auctions
- push dominant builders toward private, sealed-bid relationships with proposers
- counter-intuitively risk collapsing a multi-relay, multi-builder landscape into something smaller and more trusted, not broader and more trustless.

i don’t pretend to know the right course here but do personally feel the above perspective has been insufficiently explored. i for one can’t say landing trustless payments makes a trade-off which is understood and supported by a consensus view where differences of opinion have been heard and considered.

may sharing this view make a small contribution in helping ethereum forward  ![:heart:](https://ethresear.ch/images/emoji/facebook_messenger/heart.png?v=14)

–

notes i couldn’t help leave out ![:see_no_evil_monkey:](https://ethresear.ch/images/emoji/facebook_messenger/see_no_evil_monkey.png?v=14):

- if staked builders are dominant, they could be punished for exercising the free option inherent in pipelining. perhaps builders / relays should still be staked. requires further consideration imo.
- i’m aware of many fair counter arguments which impact the balance above but complicate the discussion and imo don’t change much about the core game theory.
- i spoke with a lot of folks to condense the above but also feel takes from core consensus client developers are still sorely lacking. i have many calls scheduled to try and improve this. i imagine the trustless payment upside section especially is still lacking. perhaps some readers may already contribute below.
- we should be careful giving out-of-protocol actors veto-like influence.
- i was too impatient to wait for review, expect some edits / corrections in the next few hours while i ask people smarter than me what i got wrong.

## Replies

**jcschlegel** (2025-11-26):

I don’t want to argue pro or contra, but thought it would it be helpful to dump some simple facts about auctions, hopefully somehow structured. Sometimes Ethereum discourse seems a bit un-informed by the technical game theory literature.

First of all, first-price sealed bid auctions are not better or worse than open bid auctions or second-price sealed bid auctions. It depends on context and your objectives. So what does this mean? Sealed bidding should be used in environments where there are relative few bidders, we fear that these bidders could coordinate/collude and we want to maximize revenue. The argument is very simple: through their public bids, bidders can signal to each other something about their willingness to pay, hence it makes collusion easier. See [here](https://www.nuffield.ox.ac.uk/users/klemperer/wrm6.pdf) why that matters in practice.

Do we actually want to maximize revenue in block auctions though? As a solo staker I would say yes :D, but my personal interests aside, I think there doesn’t seem to be a clear case for maximizing proposer welfare. What we should aim for is efficiency: we want to build the most valuable blocks. Do sealed-bid and open-bid auctions differ in efficiency? Usually not, but maybe in our case there are some efficiency difference due to up-stream effects, which I come to later.

Regarding entry: I don’t think one can make a case of open-bid auctions being friendlier to new entrants. Usually the opposite. In our case, however, the deposit requirements on builders for in-protocol bidding might increase barriers to entry, but that is a consideration orthogonal to the auction format.

Finally, regarding first vs. second price auction: the argument for second price because of strategic simplicity only works if the auction is of the independent private value type. In block auctions we have a mixed case: there is private value from exclusive flow and common value.

The term “price discovery“ gets thrown around a lot. What do we actually mean by it? We have an unknown common (!) value e.g. an asset price and we want to use an auction to incorporate all available information to determine this value.  Do we have price discovery in the block auction at the moment? I would say very little: price discovery happens offchain e.g. on Binance, and the chain just syncs to that external state. If there is on-chain price discovery. it happens on the searcher-builder level, so whether one of two competing bundles is included might contribute to price discovery and that only factors in indirectly into the block auction. For integrated searcher-builders this might be a bit different, as they might express their expectation of value in their block auction bid. If price discovery is a concern and we have enough competition in the auction, an open bid auction is preferable. The argument is again simple: public bids contain information about the common value and bidders can react to that. Is this happening in block auctions though? Not too much I would say.

Ethereum block auctions have the particular feature that there are up-stream effects. Searchers can multi-plex their bundles. I think the strongest case for open bidding is that bids give a signal to searchers where to send their bundles. And that might help us build the most efficient blocks, because it helps overcome flow fragmentation.

Finally, we should also care about latency. Open-bidding leads to more frequent bid updates, hence latency optimization is more important. I think that is a point against open-bid auction. Moreover, if the auctioneer is the proposer rather than a relay, co-location becomes harder, because the proposer changes from round to round. That seems to be a more desirable outcome in terms of geo-decentralization.

---

**ltitanb** (2025-11-28):

[@alextes](/u/alextes) regarding your point on deposited collateral for trustless payments I want to clarify that this won’t be just the payments over an epoch but potentially a lot longer, for comparison currently the deposit queue is ~14 days. Builders will have to both estimate the payments over the period and source the capital for it (as opposed to pay JIT as they do now). An unexpected increase in volatility might also cause a builder to run out of balance and preventing further bids until the new deposit is activated, so that a builder may need to decrease bids all else equal to avoid running out of staked balance. All of these factors make it more expensive to both start and operate a builder, which raises barriers to entry and decreases competition. In general I think some of the points you mentioned are relatively nuanced and may not be immediately obvious to unsophisticated proposers, who may just assume that trustless bids will be better because they are “permissionless”.

–

[@jcschlegel](/u/jcschlegel) thanks for sharing your thoughts, I think it would be helpful to contextualize the theory around auctions with the specifics about the current PBS market.

I do no think the example you linked as to why sealed auctions might be better to avoid colluding bidders applies to PBS. Regulated companies might leverage open bids to signal to each other their willingness to collude. However block building is not regulated (yet) and nothing prevents some builders to agree “offchain” to a certain bidding behavior - they don’t need the open auction to communicate this. In fact I would argue the opposite: with open bidding it’s easier to spot if two builders were bidding competitively and outbidding each other, while this becomes harder without having full access to open bidding, as we can’t see the “counterfactual” bids.

> I don’t think one can make a case of open-bid auctions being friendlier to new entrants

I think we can actually make this argument. New entrants often have to subsidize blocks to reach a certain market share that “unlocks” order flow. With an open auction it’s clear how much the new builder has to subsidize, while in a closed auction there’s a further source of uncertainty on what other builders will bid. This is a source of edge that favors established players and new builders will have to account for this uncertainty by increasing the premium they are willing to subsidize to win the block, thus overbidding more often and increasing the cost for entering the market.

Finally, I believe the “price discovery” mentioned above is regarding blockspace, not any particular token or asset being traded on chain. The proposer has a monopoly on its block and is willing to sell it, how much should builders pay for it? This price discovery currently happens during the relay auctions, as builders progressively outbid each other until the auction closes. Without access to each others’ bids, builders will have to act strategically and use models to predict their competitors’ bids. I think there’s a good argument that this additional source of uncertainty will lead to less efficient price discovery for the only “good” that proposers can sell: their block.

---

**jcschlegel** (2025-11-28):

Regarding your first point: I’m not a lawyer, but pretty sure that offchain agreements to coordinate bids would be pretty illegal in many jurisdictions, if enforced. Anyway we shouldn’t overindex on that I agree. (Your point that open bidding makes collusion more detectable, well yes, but it will be in any case detectable by the proposer, independently of whether they receive a public or private bid. So I don’t think that point is too important. ) The kind of coordination I had more in mind was algorithmic. At least anecdotally I have heard from searchers that they coordinate implicitly through some tit for tat strategy. They don’t bid the full value of their bundle and basically take random turns to win the opportunity , but if a competing searcher bids the full value, they  escalate in the next rounds and bid their full value. More importantly, it seems that in most cases, you only need to know the winning bids to coordinate in meaningful way, bc it’s a repeated auction. So I agree with you that the case for sealed bidding over open bidding based on higher revenue is very weak.

Regarding your second point: interesting, I haven’t considered that. But wouldn’t it again be sufficient to learn the winning bids to learn how to optimally size your bid to win enough rounds on average?

Regarding your third point: I still don’t buy it. Again to argue for open bidding bc of better price discovery would mean the builder learns from the other builder bids how valuable the block space should be to themselves. I don’t think there is much of that going on. Only thing they learn is  how much the other builder values it, but it won’t change how they value it. I mean you write it yourself implicitly: only thing the bidders learn from other bids it how much they need to pay to win. So the point you maybe want to make is that an open bidding auction is strategically simpler than sealed bidding.

