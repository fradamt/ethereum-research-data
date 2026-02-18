---
source: ethresearch
topic_id: 20060
title: Sealed execution auction
author: aelowsson
date: "2024-07-13"
category: Proof-of-Stake > Block proposer
tags: [mev]
url: https://ethresear.ch/t/sealed-execution-auction/20060
views: 4476
likes: 11
posts_count: 7
---

# Sealed execution auction

# Sealed execution auction

[![Sealed execution auction](https://ethresear.ch/uploads/default/optimized/3X/3/e/3e0cf08f2021a1cbbe0156d52c8482dba0a00ba6_2_690x394.jpeg)Sealed execution auction1792×1024 356 KB](https://ethresear.ch/uploads/default/3e0cf08f2021a1cbbe0156d52c8482dba0a00ba6)

By [Anders](https://x.com/weboftrees).

*While working on the [dynamic pricing auction](https://ethresear.ch/t/mev-resistant-dynamic-pricing-auction-of-execution-proposal-rights/20024) I though of another way to hold the auction that also seems interesting. Posting a rough sketch here, although I am not yet certain of its viability. Thanks to [Justin](https://x.com/drakefjustin), [Barnabé](https://x.com/barnabemonnot) and [Terence](https://x.com/terencechain).*

## Introduction

In the process of enshrining proposer–builder separation ([ePBS](https://github.com/ethereum/EIPs/pull/8711)), it has been [suggested](https://mirror.xyz/barnabe.eth/LJUb_TpANS0VWi3TOwGx_fgomBvqPaQ39anVj3mnCOg) that attesting and execution proposing should be more fully separated. Proposals such as [execution tickets](https://ethresear.ch/t/execution-tickets/17944) (ETs) and [execution auctions](https://mirror.xyz/barnabe.eth/QJ6W0mmyOwjec-2zuH6lZb0iEI2aYFB9gE-LHWIMzjQ) (EAs) strive to allocate the right to propose execution blocks to entities other than the validators. This also facilitates [MEV burn](https://ethresear.ch/t/mev-burn-a-simple-design/15590). There have been concerns ([1](https://ethresear.ch/t/mev-burn-a-simple-design/15590/4), [2](https://ethresear.ch/t/mev-burn-a-simple-design/15590/23), [3](https://ethresear.ch/t/dr-changestuff-or-how-i-learned-to-stop-worrying-and-love-mev-burn/17384/3)) around insufficient early bidding in the MEV pricing auctions with a base fee floor used in EA. By [considering the staking metagame](https://ethresear.ch/t/burn-incentives-in-mev-pricing-auctions/19856), this issue is potentially resolved, but the resulting attester–builder integration can then by itself be [problematic](https://ethresear.ch/t/burn-incentives-in-mev-pricing-auctions/19856#risks-associated-with-attester-builder-integration-14). There is also a general concern that the decided-upon auction design will [induce MEV](https://mirror.xyz/barnabe.eth/QJ6W0mmyOwjec-2zuH6lZb0iEI2aYFB9gE-LHWIMzjQ), and no definite specification among [several alternatives](https://ethresear.ch/t/on-block-space-distribution-mechanisms/19764#preliminaries-12) for the auction design in ET. For this reason, it seems fruitful to explore an auction that facilitates true separation and does not induce MEV. One such mechanism recently proposed is the [MEV resistant dynamic pricing auction](https://ethresear.ch/t/mev-resistant-dynamic-pricing-auction-of-execution-proposal-rights/20024). In the context of Vickrey auctions of execution rights, [Timeboost](https://forum.arbitrum.foundation/t/constitutional-aip-proposal-to-adopt-timeboost-a-new-transaction-ordering-policy/25167) under consideration by Arbitrum can also be mentioned.

This post proposes a [Vickrey](https://en.wikipedia.org/wiki/Vickrey_auction) slot auction in two rounds to select a forthcoming execution proposer (akin to EA), referred to as a sealed execution auction (SEA). Staked builders make sealed bids for the right to propose an execution block. Bids are observed by attesters and then collated by the beacon proposer. In subsequent steps, builders reveal their bids, attesters observe the revealed bids, and the proposer once again collates them. The right to propose a forthcoming execution block is awarded to the highest bidder, paying according to the second-highest bid, with the payment burned.

## Auction

### Staked builders

Builders are staked at a level sufficient for the protocol to penalize them if they fail to reveal committed bids. The stake can also serve as a deposit account to pay for winning bids, or this account can be managed separately.

### Sealed bids

Figure 1 gives an overview of the auction. In the first round, each builder has the opportunity to make one sealed bid over a public P2P layer. There might be a small fee for making a bid, as a further anti-Sybil measure. Attesters observe the sealed bids that have come in at time T_1. Around two seconds later, at T_2, the beacon proposer collates sealed bids (including any bids it finds after T_1), and broadcasts them in a structure. This structure may be a beacon block if the auction proceeds over two slots (see [Timeline](https://ethresear.ch/t/sealed-execution-auction/20060#timeline-15)). At T_3, attesters observe the structure and make sure that all previously observed bids at T_1 have been included. If the bids were included in a beacon block, they will attest to the block contingent on correct and timely collation. If not included in a beacon block and the proposer equivocates on the structure, the subsequent block must be rejected.

[![Figure 1](https://ethresear.ch/uploads/default/optimized/3X/e/9/e9efaf529cceda171c770e9160ed477ff7093303_2_690x347.png)Figure 12386×1202 297 KB](https://ethresear.ch/uploads/default/e9efaf529cceda171c770e9160ed477ff7093303)

**Figure 1.** Sealed execution auction. Staked builders submit sealed bids before T_1 and the proposer collates them at T_2. At T_3 attesters ensure that all bids they observed at T_1 are part of the collated structure. Builders unseal the bids after T_3 and attesters observe them at T_4. The proposer then collates bids in a beacon block at T_5 and attesters attests to the block at T_6 contingent on correct collation. The highest unsealed bid wins, paying a fee corresponding to the second highest bid. The fee is burned. Builders that did not unseal their bids are penalized.

### Revealed bids

In the second round, after the T_3 deadline, builders unseal their bids. They should not release before T_3, because then the proposer can collude with other builders to release a bid structure with some bids placed after other bids were revealed. However, they do not need to observe the proposer’s structure before release, and can proceed right after the T_3 mark.

Attesters observe unsealed bids at T_4. The proposer collates all unsealed bids it can find, including them in the beacon block at around T_5. It may also include bids that were never unsealed, so that the associated builder can be penalized (this is a strict requirement in the single-slot design, because then the sealed bids have not been included in a previous beacon block). The highest bid is selected as the forthcoming execution proposer, and the second highest bid value is deducted from the winner’s balance and burned. At T_6, attesters attest to the beacon block, contingent on a correct collation by the beacon proposer.

## Rationale

Collusion between builders and proposers to reduce the burn as in the MEV burn design is arguably resolved; without stakers actively burning each others’ MEV revenue.

- There is no longer a stable equilibrium to rely on for colluding parties, such as late bidding.
- The proposer no longer has leverage to punish early bidders by electing another builder.
- Chiseling at a cartel is trivial, simply by truthful bidding.
- Every bid fulfills a real purpose, as opposed to early bids in MEV pricing auctions.
- There is no avenue for discouragement attacks, since there is no substantial proposer revenue to remove.

## Penalization

Several actions must be penalized. If the proposer omits an observed sealed bid in the first round or an observed revealed bid in the second round, the proposer’s block must be rejected by attesters. If the proposer fails to release the structure of the sealed bids in the first round or the revealed bids in the second round in a timely manner (reaching attesters before T_3 and T_6 respectively), the proposer’s block must also be rejected by attesters. *Edit 18-07-24:* As mentioned in the previous section and also further discussed in the next, a builder that does not unseal its bid on time will be penalized. This is facilitated in Figure 1 by including the sealed bid in the beacon block.

It is possible that a builder made a mistake and will be unable to pay for its bid, if the bid is higher than its staked amount. This will be penalized by burning some proportion of the stake, for example corresponding to the amount of the actual winning bid, some fixed amount of ETH, or its entire stake. In any case, if its unbacked bid is the highest, the builder will not win the auction. The second highest bid will instead be selected as the execution proposer, paying the third highest bid, etc. If the bid underpinning the fee (normally the second highest bid) lacks funds, the bid below it will be set to underpin the fee.

## Builder–proposer collusion and possible remedies

A potential cause for concern is the following scenario: a builder determines that it would not like to unseal its bid (potentially after observing other builders’ unsealed bids). It does not want to subject itself to a penalty, so it colludes with the proposer to have it miss the slot. Is this a cause for concern? This ultimately depends on if the builder benefits more by *not* revealing its bid than the proposer loses from a missed proposal. This could be the case when bidding for the right to propose the current or next slot, and the expected MEV falls drastically between bid commit and reveal (i.e., a [value-in-flight](https://mirror.xyz/barnabe.eth/QJ6W0mmyOwjec-2zuH6lZb0iEI2aYFB9gE-LHWIMzjQ) problem). Another potential cause for concern is if the value instead increases drastically. The proposer might then pose an ultimatum to the winning builder: “send me some part of expected profits, or I will fail to propose”. A failed proposal would leave the builder without rights for the slot. An [ultimatum game](https://en.wikipedia.org/wiki/Ultimatum_game) emerges. The other builders might also be inclined to pay the proposer, in order to starve off competition, and the winning builder would then also need to pay the proposer to ensure it proposes.

While the outlined collusion scenarios may be a bit speculative, it can still be interesting to explore possible remedies. A few directions then spring to mind:

#### 1. Penalize beacon proposers for missed beacon blocks

Proposers already lose out on revenue if they miss their block. However, this loss might not be a sufficient deterrent. It would therefore be beneficial to also penalize proposers if they miss their blocks. Otherwise, if the penalty applied to a builder is substantially higher than the loss from missed proposals for the proposer, that builder penalty will be less meaningful. Builders could seek to collude to let the proposer take the fall. In essence, if the value to the builder, its competitors, or the proposer, of having the builder not win the auction, is higher than the loss to the proposer of not proposing, then collusion or an ultimatum game may emerge.

#### 2. Require subsequent beacon proposers to conclude the auction

Is it possible to have the next beacon proposer conclude the auction? This depends to some extent on the [Timeline](https://ethresear.ch/t/sealed-execution-auction/20060#timeline-15) of the auction.

- Single-slot design: In the single-slot design, attesters do not signal if they rejected a block because of an incorrect initial structure, a late structure, or an incorrect or missing beacon block. A way to deal with this is that the next proposer presents the correct outcome of the auction, in its own view, and that the attesters of n+2 either reject or confirm the new block based on the proposed outcome. But this means that these attesters must also have tracked events in the previous slot as they unfolded, and any split views (e.g., from a rather late sealed builder bid) may persist for several blocks in a row.
- Two-slot design: If the auction commences over two slots, there will be an agreed-upon set of committed sealed bids, or the first beacon block will have been rejected. The second step of the auction can then be concluded in a subsequent slot without requiring attesters to have observed the commit-phase. The requirement is to still have attesters make an observation of unsealed bids sometime before the proposer deadline. But that point need not necessarily be taken from the earlier slot. A benefit is that this might starve off split views.

One thing to note is that if a builder finds it worthwhile to pay the first proposer to not propose, in order to avoid revealing a bid without being penalized, it might be willing to pay also a second proposer for not proposing. However, the price will go up, and the number of potential collusion partners scheduled to propose in a row may not be too large. It should also be noted that when auctioning off rights for slot n+i, there is a requirement that the delay until the conclusion of the auction does not surpass i. In other words, it will only be possible to repeat a failed auction around i times. Note that this requirement is also due to the fact that the order in which auctioned off execution rights are provided cannot be altered ex post, since the expected MEV for slots may vary.

#### 3. Skip the beacon proposal reveal

Is it possible to skip the beacon proposal reveal? If all bids are unsealed, the outcome will be evident to every participant. The mechanism can then be designed such that the winning builder safely can propose its block at the assigned slot, even if a proposer has not collated the outcome and presented a winner. The previous option 2 is focused on concluding the auction via a beacon proposal in time before the execution proposal, but the point here is that the auction does not need to be concluded by the proposer as long as the outcome is evident to the builder and can be verified by attesters when the builder proposes its block. The sealed bids must then have been included in a beacon block, as in the two-slot design.

[Threshold decryption](https://en.wikipedia.org/wiki/Threshold_cryptosystem) via a committee of attesters (h/t Barnabé) is one option here. The bids are decrypted by a committee, and the winner made evident to the builders/forthcoming proposer and attesters. There would still be liveness concerns, but collusion would be more difficult. It can be noted that as long as all builders unseal their bids in a timely manner (even without threshold decryption), the winning builder can proceed with the proposal. Always penalizing builders that do not unseal their bids before T_4 could then seem sufficient, but the issue is that split views would emerge in potential designs. In any case, the outcome would also at some point need to be included in a block, to process payment and penalties.

#### 4. Auction of a future slot to reduce value-in-flight

The Vickrey auction is truthful, allowing builders to bid their true value at the commit deadline. Since value-in-flight is the most likely cause for collusion, auctioning off a slot further removed from the present will temper the issue.

#### Auctioning off multiple slots

Note that to avoid having a failed beacon proposal result in a missing execution proposal, there is also the option to sell the right to two execution proposals in the subsequent slot (with builders bidding their [inverse demand curve](https://en.wikipedia.org/wiki/Vickrey_auction) and paying according to the second and third highest bids).

## Timeline

This section presents two hypothetical timelines for the auction, either when only including unsealed bids in the beacon block (single-slot auction) or when including both sealed and unsealed bids in separate beacon blocks (two-slot auction).

### Single-slot auction

Example of a slot auction with a tight schedule enacted mostly during a single slot n, auctioning off execution proposal rights for a later slot n+i.

| T_x | Time | Overview | Description |
| --- | --- | --- | --- |
| T_1 | 4s | Sealed bid deadline | Attesters of slot n+1 observe all sealed bids. Builders must have broadcast them some time before this point to ensure eligibility. |
| T_2 | 6s | Proposer collates bids | The proposer of slot n+1 releases a structure containing all sealed bids it can find. |
| T_3 | 8s | Attesters observe collation | Attesters of slot n+1 observe the proposer’s structure to ensure it contains all bids they had seen at T_1 and that the release of this structure is timely. |
|  |  |  |  |
| T_4 | 10s | Revealed bid deadline | Attesters of slot n+1 observe unsealed bids. Builders must have broadcast them some time before this point (but after T_3) to ensure eligibility. |
| T_5 | 0s (12s) | Proposer collates in beacon block | The proposer of slot n+1 includes every unsealed bid it can find in the  block, also indicating sealed bids that were never unsealed. A winner is declared. |
| T_6 | 4s (12+4s) | Attesters confirm collation | Attesters of slot n+1 confirm that the proposer fulfilled its role and collated bids in a timely manner by attesting to the block. |

Note that builders can unseal their bids directly after T_3. This should allow attesters of slot n+1 to observe revealed bids at 10s. However, if needed, the entire schedule could be pushed back slightly.

### Two-slot auction

Here is an example of a schedule for the two-slot auction:

| T_x | Time | Overview | Description |
| --- | --- | --- | --- |
| T_1 | 10s | Sealed bid deadline | Attesters of slot n+1 observe all sealed bids. Builders must have broadcast them some time before this point to ensure eligibility. |
| T_2 | 0s (12s) | Proposer collates bids | The proposer of slot n+1 includes all sealed bids it can find in its beacon block. |
| T_3 | 4s (12+4s) | Attesters confirm collation | Attesters of slot n+1 confirm that the proposer fulfilled its role and collated bids in a timely manner by attesting to the block. |
|  |  |  |  |
| T_4 | 8s (12+8s) | Revealed bid deadline | Attesters of slot n+2 observe unsealed bids. Builders must have broadcast them some time before this point (but after T_3) to ensure eligibility. |
| T_5 | 0s (12+12s) | Proposer collates in beacon block | The proposer of slot n+2 includes every unsealed bid it can find in the  block, potentially indicating sealed bids that were never unsealed. A winner is declared. |
| T_6 | 4s (12+12+4s) | Attesters confirm collation | Attesters of slot n+2 confirm that the proposer collated all unsealed bids by attesting to the block. |

## Replies

**quintuskilbourn** (2024-07-15):

Nice post.

1. I realise the architecture you propose doesn’t need to be tied to the Vickrey auction, but since you mention it, I would point out that the incentives for the Vickrey auction aren’t that clean cut in this setting as argued in this paper. The problem is basically that you can force people to bid higher by placing a bunch of sealed bids and then revealing them conditionally on what everyone else reveals (e.g. so that you don’t win but force them to pay more or maybe because you want to deal with adverse selection in a certain way)
2. this design relies on censorship resistance derived from attesters operating based on their local view of (effectively mempool) messages. How realistic is this? Is there research into these kinds of approaches? Eclipse attacks and just shoddy gossip layers could be problematic
3. there could be very many bids and its not clear how we could do congestion pricing in this setting since we require attesters to view bids before they are “collated”. Also, if sealed bids pay congestion fees then this could reveal info about the underlying bids, as argued in this paper

---

**aelowsson** (2024-07-16):

Thanks for the good feedback and references.

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> I realize the architecture you propose doesn’t need to be tied to the Vickrey auction, but since you mention it, I would point out that the incentives for the Vickrey auction aren’t that clean cut in this setting as argued in this paper . The problem is basically that you can force people to bid higher by placing a bunch of sealed bids and then revealing them conditionally on what everyone else reveals (e.g. so that you don’t win but force them to pay more or maybe because you want to deal with adverse selection in a certain way)

It seems that the linked paper deals with an auction setting where the auctioneer derives the proceeds of the auction. However, there is no revenue for the auctioneer in the sealed execution auction (the revenue is burned), strongly limiting the incentives for placing bids that are revealed conditionally in an attempt to take advantage of the Vickrey design. I therefore assume that the outlined concern is not applicable. Correct me if I am wrong.

Note that I am in my answer specifically referring to (my interpretation of) the context in which [Ferreira and Weinberg](https://arxiv.org/pdf/2004.01598) investigate online auctions, and [Chitra, Ferreira, and Kulkarni](https://arxiv.org/pdf/2301.12532) extend this to an open ledger in the link you provided. The concern of proposer—builder collusion [outlined in the post](https://ethresear.ch/t/sealed-execution-auction/20060#builder-proposer-collusion-and-possible-remedies-9) instead emerges from value-in-flight, and/or the desire to grief the winning builder among losers, or an ultimatum game.

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> this design relies on censorship resistance derived from attesters operating based on their local view of (effectively mempool) messages. How realistic is this? Is there research into these kinds of approaches? Eclipse attacks and just shoddy gossip layers could be problematic

The auction design is an alternative to what I will refer to as the [English MEV burn](https://ethresear.ch/t/mev-burn-a-simple-design/15590) auction, which also relies on validators attesting in accordance with their local view of bids. There are then two questions; (a) if Vickrey MEV burn is more viable in this regard than an English MEV burn, and (b) if any of these designs are viable.

(a) A benefit of English MEV burn is that the proposer only needs to get one bid right, picking a bid that has an equal or higher base fee than the highest base fee before the observation deadline. In the Vickrey design, the proposer must include all received bids. In English MEV burn, builders should try to be attentive to the level of the base fee floor as they continue bidding, making many, if not all, of the last incoming bids eligible. There may however be [circumstances](https://ethresear.ch/t/mev-burn-incentivizing-earlier-bidding-in-a-simple-design/17389/7) where the proposer has an incentive to “gamble” on the bid base fee floor, even when not interacting with a colluding bidder.

A downside of English MEV burn is that there probably will be a higher quantity of bids. The quantity of bids in the Vickrey auction should be rather modest, as long as there is a small fee attached for bidding (and each builder only can place one bid). The English MEV burn design does not naturally lend itself to taking out a bid fee or penalizing builders that place more than one bid (although it can be modified).

(b) The P2P layer is not my expertise, and I would welcome feedback on viability. Your and Barnabé’s discussion on FOCIL from yesterday seems relevant ([1](https://x.com/barnabemonnot/status/1812908129534779713), [2](https://x.com/0xQuintus/status/1812908597086724441)).

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> there could be very many bids and its not clear how we could do congestion pricing in this setting since we require attesters to view bids before they are “collated”.

When it comes to the bid fee, there are many designs that are viable. As a basic example, we could rely on a similar mechanism as in the [dynamic pricing auction](https://ethresear.ch/t/mev-resistant-dynamic-pricing-auction-of-execution-proposal-rights/20024#h-42-dynamic-pricing-mechanism-11), such that the bid fee increases with the quantity of bids, but still keep the fee rather modest. The bid fee curve could for example be designed to reach 1/50th of the average sales price of the previous auctions at a desirable quantity of bids. The fee curve can peak well below the average sales price even at a large quantity of bids.

I am not perfectly sure which phase you refer to concerning attesters viewing bids before collation, but assuming here you are referring to P2P handling before commitments are collated at time T_2. In this case, my assumption is that attesters could verify the commitment and its signature using the builder’s public key, e.g., \text{Verify}_{pk}(C, \sigma), and only propagate valid commitments. Does it make sense? The point is to ensure that anything propagated across the P2P layer would eventually incur a fee. There is then a further nuance to this around if the proposer might be more likely to see its block rejected in the case where valid bids are spammed. I would actually find it reasonable to still take out the fee for all bids even if the auction fails to conclude, even if it might marginally hurt honest builders, because it would hurt dishonest spamming builders more. Note also that if builders are staked with 32 ETH each, then placing 100 bids requires 3200 ETH (over 10 million dollars worth of capital). Our experience with staked entities in general has been that they do not wish to pursue the outlined activities en masse due to implicit risks. Further note that placing more than one bid can be associated with a penalty much higher than the bid fee.

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> Also, if sealed bids pay congestion fees then this could reveal info about the underlying bids, as argued in this paper

The sealed execution auction does not allow the proposer to exclude bids from the auction (if propagated before T_1), and thus does not lead to tips or bribes as described in the linked post. I therefore assume that the outlined concern is not applicable. Correct me if I am wrong. The purpose of SEA is to strip the proposer of autonomy when dealing with timely builders: to restrict its extractable MEV for facilitating the auction. It can be noted that MEV burn in general derives from oversight of attesters. Note further the parallels to multiple concurrent proposers, and its potential viability.

---

**quintuskilbourn** (2024-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> It seems that the linked paper deals with an auction setting where the auctioneer derives the proceeds of the auction. However, there is no revenue for the auctioneer in the sealed execution auction (the revenue is burned), strongly limiting the incentives for placing bids that are revealed conditionally in an attempt to take advantage of the Vickrey design. I therefore assume that the outlined concern is not applicable. Correct me if I am wrong.

Yes the auctioneer (proposer) doesn’t have a revenue incentive, but in reality different bidders have incentives to grief each other by forcing higher bids from the winner.

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> The quantity of bids in the Vickrey auction should be rather modest

This isn’t obvious to me. If the item being auctioned off has a value that changes rapidly through time there are incentives for single bidders to place many sealed bids and then only reveal the most appropriate bid when revelation time comes or even revealing several bids in response to other revelations seen in the P2P layer reminiscent of a PGA.

I realise now from your response that you can strongly reduce these number of bids by requiring a staked identity per bid. We may want to think this through a bit more since the return of having more capital (and therefore more identities) might impact market structure in an undesirable way.

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> The sealed execution auction does not allow the proposer to exclude bids from the auction (if propagated before T_1T1T_1)

You need to exclude bids since the collated block of bids is of finite size

---

**aelowsson** (2024-07-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> Yes the auctioneer (proposer) doesn’t have a revenue incentive, but in reality different bidders have incentives to grief each other by forcing higher bids from the winner.

Right but that is much weaker (the more applicable in my view is then when they grief each other due to value in flight). The results in the paper you linked depend on the proposer deriving the proceeds of the auction, which is not the case. Therefore, those results do not apply. I’m also a bit hesitant about how well it would apply anyway with a reasonable penalty (that is burned).

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> This isn’t obvious to me. If the item being auctioned off has a value that changes rapidly through time there are incentives for single bidders to place many sealed bids and then only reveal the most appropriate bid when revelation time comes or even revealing several bids in response to other revelations seen in the P2P layer reminiscent of a PGA.

As long as the auction is concluded, every sealed bid that is collated but not revealed will result in a penalty. This penalty can be made prohibitively large. Thus, if we ensure that auctions are concluded, bids will be revealed. There are then nuances pertaining to the conclusion of the auction discussed in the original post.

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> I realise now from your response that you can strongly reduce these number of bids by requiring a staked identity per bid. We may want to think this through a bit more since the return of having more capital (and therefore more identities) might impact market structure in an undesirable way.

Right. This was specified in the original post:

“Builders are staked at a level sufficient for the protocol to penalize them if they fail to reveal committed bids… In the first round, each builder has the opportunity to make one sealed bid over a public P2P layer”.

A builder will only require one staked identity and can simply bid truthfully in the Vickrey auction by placing one single bid. Thus, capital requirements will not be prohibitively large.

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> You need to exclude bids since the collated block of bids is of finite size

In the case of a DoS attack on the P2P layer, there will indeed need to be a condition stipulating that a beacon proposer that has “filled” the beacon block should get a pass on including more bids (for obvious reasons). It should however be possible to apply the fee on every valid bid that has been placed ex-post (proposers of subsequent blocks could pick them up just to apply the fee). In either case, as long as we ensure that the aggregate fee when the beacon block is filled becomes prohibitively large, concerns should be alleviated. It is also generally a bad idea to pursue this action when you are a staked entity and must put many millions of dollars on the line in order for a sufficient quantity of bids to propagate across the P2P layer.

---

**aelowsson** (2024-07-18):

Please note that I have added a clarification to the post.

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png) Anders Elowsson:

> Edit 18-07-24: As mentioned in the previous section and also further discussed in the next, a builder that does not unseal its bid on time will be penalized. This is facilitated in Figure 1 by including the sealed bid in the beacon block.

This penalty was mentioned in other parts of the text and also included in Figure 1 and its figure text, but  not mentioned in the penalization section for some reason. My failure to mention this in that section could explain this comment:

![](https://ethresear.ch/user_avatar/ethresear.ch/quintuskilbourn/48/10413_2.png) quintuskilbourn:

> …there are incentives for single bidders to place many sealed bids and then only reveal the most appropriate bid…

---

**aelowsson** (2024-09-22):

### Protecting solo stakers when penalizing beacon proposers

A concern mentioned in the post is that builders who do not wish to unseal their bids after placing them could [collude with the beacon proposer](https://ethresear.ch/t/sealed-execution-auction/20060#builder-proposer-collusion-and-possible-remedies-9) to have it miss the slot, thereby avoiding the penalty. This can of course be resolved by [penalizing beacon proposers](https://ethresear.ch/t/sealed-execution-auction/20060#h-1-penalize-beacon-proposers-for-missed-beacon-blocks-10) for missed slots. However, one reason to hesitate with this approach is that it could harm solo stakers whose validators have gone offline. A staking service provider (SSP) can have employees on stand-by around the clock to quickly resolve any issues with their validators, but a home staker may be unable to resolve issues for several days. This [quote from Nixo](https://x.com/nixorokish/status/1830380790850724039) is a typical example of a situation where it is important to not penalize the solo staker heavily:

> I run validators in two locations, at friends’ houses & pay both for upgraded internet
>
>
> One turns off my validator’s internet access for an hr/day for an important meeting
>
>
> I just found out the other intentionally closed ports I need open cuz it was interfering with his streaming

A solution to this problem, directly applicable to the single-slot auction (but which can also be adapted to the two-slot auction), is to let the beacon proposer’s commit structure released at T_2 function as a proof of readiness (\text{PoR}). Only beacon proposers who have issued a \text{PoR} will receive a larger penalty if they fail to propose the block (at T_6).

This significantly reduces the disparity between SSPs and solo stakers and decreases the frequency with which penalties need to be applied overall. The main concern with SEA outlined in the post is thus resolved.

There is an ongoing discussion of moving forward with a proposer penalty for missed proposals for other purposes as well, unrelated to the SEA. A \text{PoR} could then potentially prove useful. There are however pitfalls with a general \text{PoR}, and the design space is rather large.

