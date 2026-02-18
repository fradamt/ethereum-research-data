---
source: ethresearch
topic_id: 17384
title: "Dr. changestuff or: how i learned to stop worrying and love mev-burn"
author: mikeneuder
date: "2023-11-10"
category: Proof-of-Stake
tags: [mev, proposer-builder-separation]
url: https://ethresear.ch/t/dr-changestuff-or-how-i-learned-to-stop-worrying-and-love-mev-burn/17384
views: 7492
likes: 54
posts_count: 18
---

# Dr. changestuff or: how i learned to stop worrying and love mev-burn

# dr. changestuff or: how i learned to stop worrying and love mev-burn

[![upload_39c555a766cf8bbfbc67f0e26bad0aad](https://ethresear.ch/uploads/default/optimized/2X/9/9408cd020665a2dee893b011e101b04bf79a9568_2_339x500.jpeg)upload_39c555a766cf8bbfbc67f0e26bad0aad1788×2636 205 KB](https://ethresear.ch/uploads/default/9408cd020665a2dee893b011e101b04bf79a9568)

^^^ any Kubrick fans?!?

\cdot

*by [mike](https://twitter.com/mikeneuder), [toni](https://twitter.com/nero_eth), & [justin](https://twitter.com/drakefjustin)*

*friday – november 10, 2023*

\cdot

***tl;dr;*** *mev-burn is misunderstood. While critics poke fun at [ultra sound money](https://ultrasound.money/) and craft [vignettes](https://twitter.com/GwartyGwart/status/1714744651373035605) about Vitalik, Hayden, and Justin, the benefits of mev-burn extend far beyond the meme. We present four protocol benefits of mev-burn: (1) improving validator economics, (2) lessening the ePBS builder liquidity requirements, (3) increasing the cost of censorship, and (4) improving the protocol resilience under exposure to a “mass MEV” event. Additionally, we address two of the biggest misconceptions about mev-burn: (1) proposer-builder collusion, and (2) late-in-slot MEV.*

\cdot

***Related work***

| Article | Description |
| --- | --- |
| MEV burn – a simple design | Justin’s design |
| In a post MEV-Burn world - Some simulations and stats | Toni’s analysis |
| Relays in a post-ePBS world | High-level ePBS discussion |

***Acronyms***

| source | expansion |
| --- | --- |
| ePBS | enshrined proposer-builder separation |
| ToB | top of block |
| EL | execution layer |
| CL | consensus layer |

\cdot

> mike’s editorial note: Justin’s post uses the “MEV burn” (all caps) notation. I find the capitalized letters ~unaesthetic~ and more likely to be read as “EM-EE-VEE” (three syllables) instead of “mĕv”/“m(eh)v” (one syllable). I suggest we adopt the “mev-burn” notation for ease of reading and speaking. Justin hates the hyphen and suggested the following alternatives (i) mevburn, (ii) mev burn, (iii) mèvburn, & (iv) mev’burn, all of which are ngmi in my opinion. Please DM me your preference – ymmv. (and yes … we did indeed spend more time debating this than any other part of the article)

### mev-burn summary

To set the stage, we present a high-level description of the mechanism; for the latest on the mev-burn design, see Justin’s [“MEV burn – a simple design”](https://ethresear.ch/t/mev-burn-a-simple-design/15590). The figure below encapsulates the key elements.

[![upload_84eeb52e6c596bea3fec4601554a646e](https://ethresear.ch/uploads/default/optimized/2X/e/ecb0344d8c47c4607d310b1a479609563030a2b6_2_648x313.png)upload_84eeb52e6c596bea3fec4601554a646e2718×1318 237 KB](https://ethresear.ch/uploads/default/ecb0344d8c47c4607d310b1a479609563030a2b6)

We assume an ePBS instantiation, which is a prerequisite for mev-burn.

- Before the slot starts, the bids are circulated in the “bidding” phase.
- A builder bid is composed of (1) the base fee (the amount of ETH that a block will burn) and (2) a tip (the amount of ETH paid to the proposer).
- D seconds before the beginning of the slot (we usually use D=2), the attesting committee locally sets a “base fee floor” according to the bid with the highest base fee that they have observed.
- At the beginning of the slot, the proposer selects and signs a bid, publishing it to the network.
- When the attestation deadline arrives, the attesting committee votes for the proposer block if (1) it arrives on time, and (2) the base fee of the bid exceeds their local floor.
- As the attestations for the proposer’s block arrive, the builder gains confidence that their bid is the unique winner of the auction, and they publish the payload (the actual list of transactions in the block).
- The payload receives attestations if it was revealed on time and accurately honors the base fee by burning an appropriate amount of ETH.

### Benefits beyond “ultra sound money”

[Gwart](https://twitter.com/GwartyGwart/status/1719368168693526549), [0xBalloonLover](https://twitter.com/0xBalloonLover/status/1719893928751599694), [BeckyFromHR](https://twitter.com/BeckyFromHR/status/1720233347010703790), and other “orthogonal thinkers” poke fun at the meme of “burning more `ETH`”. Though funny, these jokes miss the reality that the benefits from mev-burn extend far beyond making `ETH` “more” ultra sound (hyper-ultra sound?!?). mev-burn improves validator economics, lessens the builder liquidity requirements in ePBS, increases the cost of censorship, and improves the protocol resilience under exposure to a “mass MEV” event. Let’s go through each of these individually.

#### Validator economics

The amount of `ETH` staked is a key metric in the consensus layer. Currently, this has stabilized around [23\%](https://www.validatorqueue.com/) of the `ETH` supply. In return for their participation, validators are compensated with rewards from the consensus layer (abbr. CL rewards) and through the transaction fees and MEV extracted during their slot (abbr. EL rewards). In low volatility periods, the EL rewards may constitute a relatively minor fraction of the overall allocation. The figure below shows that EL rewards account for about 25\% of the total validator rewards over the past few months.

[![upload_41480e3479e040c7c67ce2f3d8386b72](https://ethresear.ch/uploads/default/optimized/2X/8/89ba869374586ffedd115aeb5e6fc1c1e875f9bc_2_690x258.jpeg)upload_41480e3479e040c7c67ce2f3d8386b72965×361 26.6 KB](https://ethresear.ch/uploads/default/89ba869374586ffedd115aeb5e6fc1c1e875f9bc)

When trading volumes and volatility increase, this proportion can change significantly; on March 11, 2023, when `USDC` traded at a discount, EL rewards accounted for 75\% of validator rewards. During a bull market, we should expect EL rewards to remain significantly higher than today, incentivizing the deployment of more `ETH` into the consensus layer. By burning some of the EL rewards through mev-burn, we reduce the value and the variance of validator rewards. While it’s not clear exactly “how much” is the right amount of stake, 23\% of the supply (\approx 56 billion `USD` at today’s price) feels like plenty, and entering a situation where massive staking demand leads to sharp growth in the validator set is an undesirable outcome. If the protocol “overpays for security” with unnecessary issuance, the amount of `ETH` staked exceeds what is deemed necessary. The figure below shows the distribution of rewards before and after mev-burn.

[![diagram-20231110 (1)](https://ethresear.ch/uploads/default/optimized/2X/c/c8b03ac8cc029b6673d13f98141f484a70f1fae5_2_552x396.png)diagram-20231110 (1)954×685 73.4 KB](https://ethresear.ch/uploads/default/c8b03ac8cc029b6673d13f98141f484a70f1fae5)

**tl;dr;** *mev-burn reduces validator rewards without changing the protocol issuance.*

#### Builder liquidity requirements

[“Relays in a post-ePBS world”](https://ethresear.ch/t/relays-in-a-post-epbs-world/16278) distills an ePBS mechanism into,

1. a commit-reveal scheme to protect the builder from the proposer, and
2. a payment enforcement mechanism to protect the proposer from the builder.

Another way to think about (2) is that each bid must be accompanied by some “builder liquidity” to guarantee that the proposer is paid even if the builder doesn’t produce a valid block. The figure below shows three different cases for builder liquidity in ePBS.

[![upload_8224121556fb46cd37630323ca6d6515](https://ethresear.ch/uploads/default/optimized/2X/2/2fe2e79d2015e05180ff2c2540aed258d967eb5c_2_552x254.png)upload_8224121556fb46cd37630323ca6d65151065×492 71.2 KB](https://ethresear.ch/uploads/default/2fe2e79d2015e05180ff2c2540aed258d967eb5c)

1. uncapped w/o mev-burn – In the vanilla ePBS design without mev-burn, the entire value of a block bid goes to the validator. Accordingly, the builder’s liquidity must match the size of the bid to avoid a griefing attack on the proposer. A builder who promises to pay 100 ETH for a block must be able to make that payment at the top of the block (ToB). It doesn’t make sense to cap the bid value of a block, because that encourages side-channel payments from the builder to the proposer.
2. uncapped w /mev-burn – With mev-burn, part of the bid is burned and the remainder is used to tip the proposer. Here, if we don’t cap the builder liquidity, it accounts for the entire bid value. A builder who promises to burn 80 ETH and tip 20 ETH must be able to make that full 100 ETH payment at the top of the block (ToB).
3. capped w /mev-burn – With mev-burn, we can take advantage of the fact that only the tip needs to be fully collateralized. By capping the liquidity of the burn, we can reduce the capital requirements of running a builder that competes for large blocks. A builder who promises to burn 80 ETH and tip 20 ETH must be able to fully collateralize the 20 ETH tip at the ToB, but can be bonded for a capped amount in the burn liquidity (e.g., 32 ETH). If they fail to build a valid block that burns the full 80 ETH, then their 32 ETH is slashed and the remaining 48 ETH that was supposed to be burned is ignored (by not burning that ETH, the value is socialized across all ETH holders and/or likely burned during the next slot).

With mev-burn we should take advantage of case (3) above to limit the capital requirements of running a builder.

> Aside: by capping the liquidity requirements, we also cap the amount that a builder would have to pay for an empty slot. Under extreme circumstances, builder A could execute the following strategy:
>
>
> builder A observes builder B is willing to burn 1000 ETH and tip 1 ETH for a given slot, implying the existence of a huge opportunity to capture some MEV.
> builder A makes a bid of 1000 ETH burned and a 1.1 ETH tip and wins the slot with no plans of actually making a block.
> builder A is slashed 32 ETH for missing the slot, but bought 12 seconds to find the opportunity that builder B is bidding based on.
>
>
> Essentially, the price of a missed slot becomes 32 ETH. While this strategy is feasible, it seems likely that this wouldn’t occur frequently enough to pose a significant risk to the liveness of the chain. Even if it does occur, builder A would still need to compete with builder B for the MEV in the subsequent slot. Additionally, raising the cap of builder liquidity further increases the cost of a missed slot.

**tl;dr;** *mev-burn lowers capital requirements for builders in ePBS.*

#### Cost of censorship

One feature of PBS with EIP-1559 is the reduced cost of censoring a transaction. SMG pointed [this out](https://twitter.com/specialmech/status/1674482046826328065) by censoring a block in June 2023, but Vitalik [discussed this](https://notes.ethereum.org/@vbuterin/pbs_censorship_resistance#What-are-the-censorship-resistance-challenges-in-PBS-vs-status-quo) in the beginning of 2022 (many such cases lol). The key takeaway point:

> “Note that in both cases, the attacker loses P per slot for censoring”,

where P is the priority fee of the victim transaction. Thus blocks built in a PBS regime have worse censorship resistance than in a self-building regime (see [censorship.pics](https://www.censorship.pics/)). mev-burn can help alleviate this. If we include `ETH` burned through the base fee of EIP-1559 transactions in the overall burn associated with a block bid, then the cost of censorship is the full fee that the victim transaction pays. The figure below captures this.

[![upload_7081c6c7604f60670dcb5948ca594b13](https://ethresear.ch/uploads/default/optimized/2X/7/7385f38caad098fe86119ff600eb39492b876e1b_2_552x360.png)upload_7081c6c7604f60670dcb5948ca594b131005×656 63.1 KB](https://ethresear.ch/uploads/default/7385f38caad098fe86119ff600eb39492b876e1b)

On the left, the uncensored block includes transactions `a, b, & c`, which together burn a total of 0.6 `ETH`. The builder bids an additional 1 `ETH` for a total of 1.6. On the right, the builder is censoring `txn c`, which burns 0.2 `ETH`. To burn the same amount as the uncensored block, the builder needs to subsidize that burn through their bid of 1.2 `ETH`. Now the cost of censorship is no longer just the priority fee of the censored transaction, but also includes the base fee. If a builder attempts to censor many transactions, the margin of their burn floor compared to non-censoring builders is reduced, making it harder for them to compete in the auction.

**tl;dr;** *mev-burn increases the cost of censorship by including the base fee of the victim transaction.*

#### Resilience in the presence of mass MEV events

We should expect that DeFi, bridge, or rollup hacks may lead to mass MEV events (on the order of hundreds of millions of dollars) – we have [seen it](https://rekt.news/leaderboard/) before (e.g., the [nomad hack](https://rekt.news/nomad-rekt/) during which hundreds of copy-cat transactions continued to exploit the bridge for several hours). mev-burn improves the protocol’s ability to withstand such turbulence in several ways, all of which derive from the fact that in a mass MEV event, most of the `ETH` will be burned instead of paid to the proposer of the slot.

1. mev-burn reduces the incentive for a “rugpool”. With large node operators running significant portions of the validators in Ethereum, there is a risk that the node operators steal MEV if the value exceeds their reputational and legal cost from doing so.
2. mev-burn reduces the incentive to reorg for profit. Some staking pools might have logic built into their consensus clients to reorg for profit during a mass MEV event. This affects Ethereum’s short-term consensus security.
3. mev-burn reduces the incentive to DoS attack. Beyond trying to reorg the chain, network-level DoS attacks might also be feasible and profitable during a mass MEV event.

We should expect chaotic amounts of activity during these periods, so improving the stability of the protocol in the face of such disruption is a huge benefit.

**tl;dr;** *mev-burn decreases the scale of a mass MEV event, improving the protocol resilience.*

### Common misconceptions

You might now be thinking, “OK OK, we get it. mev-burn has some nice features, but what about all the problems it causes.” Well, dear reader, we think some of these problems you mention are misconceptions. In particular, the two most common critiques of mev-burn are

1. “If we burn validator rewards, won’t they collude with the builders to avoid the burn and kickback some of the rewards to the builder?”
2. “With the two-second delay between when the attesters set their bid floor and the end of the slot, mev-burn will miss out on all the late-in-slot bids. Isn’t most of the CEX-DEX arbitrage value captured during that period?”

Great questions, let’s think through each.

#### Proposer-Builder Collusion (PBC?!)

The idea here is simple. Without mev-burn, a builder bid of 1 `ETH` is paid in full to the proposer; with mev-burn, the same bid may burn 0.9 `ETH` and tip the proposer 0.1 `ETH`. A rational proposer will want to minimize the burn to maximize their rewards, thus having an incentive to try to get builders to side-channel bids to them to avoid the burn mechanism. Notice that the builder is paying the full 1 `ETH` either way (i.e., burning vs. paying looks the same from the builder’s perspective), so they only care about interacting with the proposer if the proposer rebates them some of the bid. Consider the game with 3 players: `proposer, builder A, & builder B`. Let’s play out a few situations.

***Without mev-burn***

- builder A bids 0.9 ETH.
- builder B bids 1 ETH.
- proposer selects builder B’s  bid.
- builder B pays the 1 ETH.

This is our base case.

***With mev-burn and no collusion***

- builder A bids 0.9 ETH with 0.8 ETH burned and a 0.1 ETH tip.
- builder B bids 1 ETH with 0.8 ETH burned and a 0.2 ETH tip.
- proposer selects builder B’s bid.
- builder B pays 0.2 ETH to the proposer and burns 0.8 ETH.

With no collusion, it’s all the same from the builders’ view, while the proposer only makes 0.2 `ETH` instead of the full 1 `ETH`.

***With mev-burn and `proposer <-> builder A` collusion***

- builder A bids 0.9 ETH with 0 ETH burned and a 0.9 ETH tip (the collusion has them set the burn to zero to get rebated by the proposer).
- builder B bids 1 ETH with 0.8 ETH burned and a 0.2 ETH tip.
- The proposer is forced to select builder B’s bid, because it is the only one that the attesting committee will consider valid (it sets the floor to 0.8 ETH).
- builder B pays 0.2 ETH to the proposer and burns 0.8 ETH.

With `proposer <-> builder A` collusion, `builder B` sets the floor and thus nullifies the benefits.

***With mev-burn and `proposer <-> builder A, builder B` collusion***

- builder A bids 0.9 ETH with 0 ETH burned and a 0.9 ETH tip.
- builder B bids 1 ETH with 0 ETH burned and a 1 ETH tip.
- proposer happily selects builder B’s bid, because the burn floor is 0, and rebates builder B for colluding.

With `proposer <-> builder A, builder B` collusion, we finally have a benefit for all parties involved.

This doesn’t feel like a stable equilibrium for two reasons:

1. Each builder is incentivized to defect to set the bid floor at the last moment and be the only valid bid. If the builder successfully gets the bid to the attesting committee right before the floor is set, their bid will be the only valid bid and thus the winner by default.
2. To combat the issue above, the builders would explicitly need to cooperate to ensure the floor never gets set above 0. With the builders directly colluding, there is no need to pay rent to the proposer in the first place (not to mention the higher coordination effort, latency costs, and legal risks incurred from expanding the collusion set). They could collude and avoid paying the proposer while sharing their revenues.

The key here is that (2) above is already possible today. Thus mev-burn doesn’t *increase* the probability of collusion (adding the validator to the colluding set strictly decreases the rewards of the builders).

#### Late-in-slot MEV is not captured

Many have [pointed out](https://twitter.com/specialmech/status/1714748986492699115) that a significant portion of the MEV derived from the CEX-DEX arbitrageurs comes at the end of a slot. The reason for this is quite simple: as the end of the slot approaches, there is more certainty about the delta between the CEX vs. DEX price. Arbitrageurs can reflect this reduction in risk by bidding more aggressively without worrying about the price moving against them. Since the mev-burn design sets the bid floor at`t=10`, any MEV that arrives after the cutoff time won’t be burned. **This is the most compelling critique of mev-burn.** The natural questions that follow are,

1. “What percentage of the MEV do we think mev-burn will capture?”
2. “What percentage is ‘enough’ to make this mechanism worth enshrining?”

(1) we can try to estimate by looking at historical data. The figure below shows the 90\% confidence interval of the bid value as a function of time in the slot under `mev-boost`.

[![upload_5e9f2f4354bffe3c7b8b291a3ae90c34](https://ethresear.ch/uploads/default/optimized/2X/3/3922a5d6ed991b89d2ea8a0d1259bcb7ecd12949_2_690x355.jpeg)upload_5e9f2f4354bffe3c7b8b291a3ae90c34969×499 31.6 KB](https://ethresear.ch/uploads/default/3922a5d6ed991b89d2ea8a0d1259bcb7ecd12949)

This data represents the bid value (as a percentage of the winning bid value) across `mev-boost` relays during the previous 30 days (Oct. 8 - Nov. 8, 2023). The key value of t=-2 shows that the median slot would burn around 80\% of the total bid, whereas the lowest 5\% of slots would only burn around 25\% of the total bid.

(2) is more of a philosophical question. In a perfect world, we would burn exactly 10/12 = 83.\overline{3}\% of the MEV of the slot. The builders would stop bidding up the base fee at t=10 because they know that most of the attesters will have fixed their view of the bid floor by then. Since the bid values scale super-linearly in time, we shouldn’t expect a perfect burn, but despite this, it still seems worthwhile considering the above benefits.

With the advent of OFAs, it is also possible that a large percentage of MEV-producing transactions move off-chain. If that is the case, then the CEX-DEX arbitrage would constitute a smaller portion of the overall MEV of a slot, diminishing the late-in-slot value.

### How do we get there?

By now, you may be thinking, “OK I am sold, let’s do mev-burn”. Great, we are glad you think so ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) . One incredible thing about mev-burn is it directly follows from ePBS. While ePBS has been a topic du jour, there are still many [open questions](https://notes.ethereum.org/@mikeneuder/infinite-buffet). With the benefits of mev-burn, solving these questions and design considerations should be a high priority. Interestingly, mev-burn might be the most compelling reason to do ePBS after all!

[![upload_77c5b4bbd2dba76ec3191b0034aecd65](https://ethresear.ch/uploads/default/original/2X/b/bcadf6049a8f2f8c7606b41cda733b931429bf23.gif)upload_77c5b4bbd2dba76ec3191b0034aecd65321×474 16.1 KB](https://ethresear.ch/uploads/default/bcadf6049a8f2f8c7606b41cda733b931429bf23)

tyvm for reading <3

## Replies

**Mister-Meeseeks** (2023-11-10):

Thanks for putting this together. Probably the best succinct summary of mev-burn so far.

But one thing that’s not clear to me, is what’s the incentive for the attesting committee to behave honestly? All of the collusion examples assume the attesting committee follows the rules. But besides social convention, I don’t see any disincentive for members of the committee to censor proposals.

Yes, you could say that the attestation committee is very large and diversified, so coordination around collusion is a challenge. But, the cost to misbehavior is zero unless I’m missing something. That would make it relatively easy for a coalition of “dissenter validators” to slowly build up its stake in public over time. It would be easy to imagine a liquidity mining incentive, where the dissenters emit tokens to incentivize joining the coalition, the value of which is the future value of redirected mev if/when the coalition starts regularly taking over majorities of attestation committees.

A similar dynamic exists, that works at cross purposes to the original reason for PBS. Attestation committee censorship potentially increases returns super-linearly for parties as they control a higher percentage of stake. A small validator would never control the majority of an attestation committee. Whereas a major validator could control some percent of attestation committees, and therefore be able to harvest higher returns from mev capture. That would obviously lead to centralization forces on the validator set.

---

**jasalper** (2023-11-10):

I have comments on the benefits - but will leave those for another day to focus on the “common misconceptions”.

The two issues are actually the same, and they’re being brushed under the rug when they’re a much bigger issue than they’re made out to be.

Collusion doesn’t have a cost and doesn’t require not bidding like the example shows. Collusion only requires not bidding before the payload observation deadline. If a builder defects to set the bid floor, the other builders can bid at that bid floor after the payload observation deadline. Bids are still accepted after the payload base fee snapshot so defecting doesn’t give you any benefits such as guaranteeing you’d win the block.

This results in collusion being a stable dominant strategy for builders – builders get no benefit by bidding early, but they lose ETH in the case where the validator is offering mev-burn refunds. You really only have 2-3 builders with the ability to build “full value” cex-dex blocks right now - and bidding late is minimal effort, any builder could implement it in an hour if that. It seems obvious to me that both builders will immediately start doing so, if not on their own, the second a validator makes the offer to refund some portion of the mev-burn.

Finally, the historical estimation is no good. You can look at current graphs and say that the block value is bid 80% of the total bid by the deadline. But that’s because there’s a very weak incentive to bid late now (hiding your bids from competitors). This will only get worse as a real incentive to bid late appears (maximizing your validator refund). At best this should be looked at as a generous upper bound.

---

**terence** (2023-11-10):

1. In the section discussing ‘Builder liquidity requirements,’ it appears that we assume the builder is also a validator and has staked Ether, leading to the possibility of 32 ETH being slashed. I believe the situation where the bid is capped with MEV burn can be considered a loophole. This is because a builder could potentially gain 48 ETH by deliberately getting slashed. Assuming the builder is staked, it would make sense to require the builder to maintain a balance sufficient to cover both the bid burn and tip amount; otherwise, the entire block should be deemed invalid. It’s worth noting that achieving consensus payment is more straightforward in this context compared to execution payment, especially concerning implementation and future compatibility with SSLE.
2. Similar to the previous comments, I share the same view that builders are not obligated to bid before the 10-second mark. Currently, builders do this for reasons that can change in the future. Even if builders were to alter their behavior to start bidding at 9 seconds, many aspects of their behavior would likely change as well. Additionally, it’s important to acknowledge that we assume this bid originates from a P2P source, which is not the most efficient form and may introduce delays. In ePBS, I assume that most builders will run their own relayer and provide an RPC endpoint for validators to query.
3. Regarding the Attester committee incentive, I personally don’t believe it’s a significant issue that this role is not incentivized. I prefer keeping the protocol simple in this regard. The attributability of the Attester committee for a specific slot is clear, and any obvious collusion would be easy to detect.
4. Potuz and I have been collaborating on the ePBS specification, and the latest design can be found here. Both of us have pull requests in our respective repositories. It wouldn’t be challenging to extend what we are working on to incorporate MEV burn. Please feel free to reach out with any questions: link

---

**Nero_eth** (2023-11-11):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> I believe the situation where the bid is capped with MEV burn can be considered a loophole.

Could you expand on this case?

I like thinking of the cap as a **fixed punishment for not contributing to the burn**. The tip still goes to the proposers so nothing changes from the proposers’ perspective. Proposers are compensated the full EL rewards (the mev-burn tip). The compromise between socializing the costs of a missed burn vs. lowering the entry barriers for builder does make sense to me and choosing a large enough penalty should be enough to avoid builders bidding unrealisticly high to then not deliver.

As an example: The proposer sees one bid b at second 10 in the slot that promises to burn 1000 ETH and tip 1 ETH. The proposer sees another bid b' at second 10 that burns 10 ETH and tips 2 ETH. As the proposer saw the 1000 burn bid in time, he can trust that the upcoming attestation committée will set their burn floor to 1000 ETH too. So the proposer will ignore b' and select b.

If the builder is not able to come up with 1001 ETH (because he only has 33 ETH (32 + 1), then the tip still goes to the proposer while 32 ETH are slashed.

In the end, the validator lost 1 ETH (as he could have chosen the honest bid b'  and receive 2 ETH instead of 1. On the other hand, the attack costed the builder 32 ETH and instead of burning 10 ETH, we burn/slash 32.

Regarding 2, I agree with you and the comment from [@jasalper](/u/jasalper), that one cannot naively assume that changing something in the rules wouldn’t impact the builder behavior. So, the actual burn, assuming having mev-burn implemented can only be roughly estimated as of now.

Also regarding the incentives to bid early, I agree that this is a valid point.

At the moment, we see some validators requesting a block header from the relay way too early when certain builders have not even started bidding. These validators would probably run into problems if they continue being early as their chosen block might then not be able to satisfy the burn.

---

**michaelsproul** (2023-11-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Could you expand on this case?

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> If the builder is not able to come up with 1001 ETH (because he only has 33 ETH (32 + 1), then the tip still goes to the proposer while 32 ETH are slashed.

I think [@terence](/u/terence) is referring to the case where the malicious builder reveals a payload that *does* contain a 1000 ETH opportunity, but which they exploit for their own benefit (while paying the 32 ETH slashing penalty). My understanding of mev-burn’s solution to this is that **any payload that doesn’t burn the amount bid is invalid**, so this payload would not become part of the canonical chain. At least that’s what I infer from the wording:

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> If they fail to build a valid block that burns the full 80 ETH, then their 32 ETH is slashed and the remaining 48 ETH that was supposed to be burned is ignored

And in Justin’s post:

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png)[MEV burn—a simple design](https://ethresear.ch/t/mev-burn-a-simple-design/15590/1)

> The payload is deemed invalid (with transactions reverted) if the post-execution builder balance is not large enough to cover the payload base fee.

Is that right?

---

**Nero_eth** (2023-11-12):

Oh I see. You’re right, yeah.

If the builder bids 1000 ETH as a tip and offers to burn 1 ETH, while the burn is actually at e.g. 2 ETH, then the builder’s payload (together with the 1000 ETH MEV extraction) wouldn’t make it to the canonical chain and the builder would loose it’s stake while getting nothing in return.

---

**terence** (2023-11-12):

Understood. The concept of ‘not making it to the canonical chain’ is akin to the ePBS design I’ve previously worked on. I’d be wary of adding a slashing condition to the specification and client design, as it’s not always straightforward. Ideally, avoiding slashing would be preferable. If the builder lacks sufficient base balance to cover the cost of the burn, we could just immediately fail the block

---

**tripoli** (2023-11-12):

Cool post.

I think it makes sense to round out the data a bit by talking about the sources of execution layer rewards to understand how it could change if the incentive structure changes as well.

Over the period, [October 8, November 8) MEV-Boost rewards were [21,674 eth](https://mevboost.pics/). Priority fees accounted for [13,294 eth](https://dune.com/queries/3192847) during the period, with [4,380 eth](https://dune.com/queries/3192794) from public mempool transactions (characterized by Flashbots mempool dumpster), which leaves 8,914 eth from private mempools. Priority fees on sandwich transactions contributed [3,306 eth](https://dune.com/queries/3192632) (37% of private mempool priority fees).

About [93% of blocks](https://mevboost.pics/) used MEV-Boost, so about 7% of the public mempool transaction fees should have been captured by solo builders (306 eth).

This leaves us with about 8,074 eth in rewards that are unaccounted. My impression is that this is mostly from integrated builders, but I haven’t dived into the data. Considering that [Wintermute and SCP](https://www.searcherbuilder.pics/) send ~ $2 billion (1,000,000 eth) of volume to rsync and beaver per month, this seems more than possible to me. Is there anything I’m missing here?

---

MEV-Burn should have 10/12 vision of public mempool fees and probably of sandwiches too (although hopefully sandwiches will decrease in time with better wallet ux). To capture most the rest of the private order-flow (65%) requires us to assume that builders do not change their habits and that the mechanisms involved have vision into non-public flow.

Considering how unaligned builders are today, this assumption seems a little naive to me.

Further, why do builders even bother submitting bids early right now? Only about 1 in 400 winning MEV-Boost blocks are received by any relay before the proposed 10-second cutoff. Since there’s almost no incentive for builders to bid early the dynamic is fragile, and as soon as there’s any disincentive to early bidding I imagine we’ll see change.

[![slot-time-distribution](https://ethresear.ch/uploads/default/optimized/2X/4/425156ea4b32da1f9728ac9360b589cdb3106cac_2_690x345.png)slot-time-distribution2600×1300 128 KB](https://ethresear.ch/uploads/default/425156ea4b32da1f9728ac9360b589cdb3106cac)

---

**CometShock** (2023-11-13):

## Attester Questions and Incentives

As mentioned by [@Mister-Meeseeks](/u/mister-meeseeks), I think we need more specific details regarding the attesters. Some of this might already be answered and I’m just missing the details from somewhere.

As we obviously know, block production is an infinite game. Attesters are validators, and thus rationally would like to maximize their rewards in both attesting and proposing (while minimizing slashing). Where possible, rational attesters would want to establish a minimal payload base fee precedent so this behavior is reciprocated during their turn in proposing. If possible, clawing back rewards from being burnt is a better financial outcome for validators. Because of this incentive (and some others to follow later in this response), I am curious about the following questions:

1. Is there punishment for any attester misbehavior? Under what circumstances is it considered misbehavior, and what is the punishment?
2. Are attesters required to broadcast their local base fee floor by some deadline?
3. Can attesters broadcast their local base fee floor and then update it prior to some deadline?
4. Is there some point in which attesters are absolutely committed to a base fee floor prior to their attestation, or is this just a soft definition that they can individually update prior to the proposal attestation?

Without these answers, it’s a little harder to wargame the nuanced incentives each party has. I’ll continue on with some of my other points, but many of them may be subject to how the above questions are answered.

## Potentially Overgenerous Assumptions

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> This doesn’t feel like a stable equilibrium for two reasons:
>
>
> Each builder is incentivized to defect to set the bid floor at the last moment and be the only valid bid. If the builder successfully gets the bid to the attesting committee right before the floor is set, their bid will be the only valid bid and thus the winner by default.

**Information**

This defection strategy is assuming the builder has more information than they would in reality:

1. Builders do not know with certainty the total extractable value each other bidder has while the auction is ongoing.
2. Due to cross-domain MEV (ex: CEX-DEX arbs), builders do not know with certainty the total extractable value they themselves will have, but the certainty increases as time passes.

With the potential uncertainties above, a reasonably confident competitive builder should attempt to not defect, as they still have the opportunity to be the winner. What’s left are very unconfident builders, who almost by definition are likely to not have as much value to be captured.

**Latency**

This defection strategy to win the auction also assumes some timing games are a certainty. For simplicity, assume latency includes processing time for the endpoint.

(D + excess\_proposal\_window) < (latency_{defection\_to\_competitor} + latency_{competitor\_to\_proposer})

*sidenote: adjust the left side of the inequality depending upon how Attester Questions are answered.*

If this latency assumption is violated, the non-defectors can still update their bids to include the expected base fee floor (as mentioned by [@jasalper](/u/jasalper)). Thus, the probability of winning selection is only minimally increased and the incentive to defect is minimized.

**Synthesis**

If both the information and latency assumptions are violated, there exists a very large incentives gap between honest and rational builders. Honest builders will earn little to nothing (many of which may discontinue operations), and rational builders will continue to persist by their profitability.

## Structured Bids

There is a possibility that the latency assumption doesn’t need to be violated in order for a rational builder to minimize burn for the benefit of themselves and the proposer alike. Consider this example, under the assumption that bids are not required to be observed by attesters prior to proposal:

An independent relay is constructed, similar to what is shown in the graphic below from [Relays in a post-ePBS world](https://ethresear.ch/t/relays-in-a-post-epbs-world/16278). As seen in the graphic, the bids from relays to proposer are not by default visible to outside parties such as attesters.

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png)[Relays in a post-ePBS world](https://ethresear.ch/t/relays-in-a-post-epbs-world/16278/1)

> upload_098ebda4f1832e6b5f69dccf7e4e68da1831×985 137 KB

Because of mev-burn, builder B likely wants to keep their bids hidden from attesters unless the relay is unreliable, or they want to defect. In order to mitigate being usurped by a last-minute defection from other bidders, the relay announces that it will accept and relay structured bids. When the relay submits bids to the proposer, it just submits multiple bids to counter other defections only when necessary. Here’s roughly what a simplified structured bid could look like:

[![image](https://ethresear.ch/uploads/default/original/2X/1/14705773f54371cbfe123d922fdc38b64dcf70bb.png)image608×142 17 KB](https://ethresear.ch/uploads/default/14705773f54371cbfe123d922fdc38b64dcf70bb)

Each builder’s actual block contents are functionally the same, with the exception of varied payments. Notice that the proposer is still incentivized to select the lowest payload base fee bid possible, and both proposer and builder stand to benefit. Of course, the marginal changes in rewards don’t have to be split 50/50. As seen in the following table, both proposer-favored and builder-favored environments can still result in bid structures that incentivize minimal payload base fee for the benefit of both parties.

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/f820eccb751d319b7b77849f2026394632a6d58e_2_690x117.png)image1289×220 38 KB](https://ethresear.ch/uploads/default/f820eccb751d319b7b77849f2026394632a6d58e)

There are some additional configuration details for relays that would still need to be finalized, but this model appears possible to minimize payload base fee more than intended by design of mev-burn. Note that the relay only needs to anticipate what the attesters will require for the base fee floor – not necessarily what the highest payload base fee in a bid is. Note that this relay design is increasingly more useful the more centralized the builder set is. Today there are very few highly skilled builders, thus we can likely assume that they will be attracted to solutions such as this (or similar via vertically integrated builder/relay).

## Historic Data Does Not Necessarily Apply to a New System

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> (1) we can try to estimate by looking at historical data. The figure below shows the 90% 90%90% confidence interval of the bid value as a function of time in the slot under mev-boost.

As also mentioned by [@tripoli](/u/tripoli), the assumption that past data applies to this new proposed system seems highly flawed. You’re completely altering an incentive mechanism, therefore you should expect observant and rational agents to behave according to the new system – not the old one.

Assuming honest attesters, mev-burn signals that it will attempt to burn the majority of value observed from all bids D seconds prior to the beginning of the slot. Unless you as a builder are nearly certain that you will lose the auction before it has concluded (see *Potentially Overgenerous Assumptions*), there is no reason to defect before D. And even if you choose to defect before D, your defection bid’s success is still contingent on the *Latency* assumption. Obviously your defection bid does force additional burn, but we can likely assume that its direct value add to you is *de minimis*. The most convincing argument to defect (when you believe you will lose the auction) is forcing burn deprives your competition of future capital that they could use to improve themselves.

That’s a lot of conditions to rely on, and depending upon how the *Attester Questions and Incentives* section is addressed, may further layer on more conditions surrounding what the payload base fee floor looks like in reality.

---

**fradamt** (2023-11-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> This doesn’t feel like a stable equilibrium for two reasons:
>
>
> Each builder is incentivized to defect to set the bid floor at the last moment and be the only valid bid. If the builder successfully gets the bid to the attesting committee right before the floor is set, their bid will be the only valid bid and thus the winner by default.

Even if your bid is the only one seen by attesters before the floor-setting deadline, that does not guarantee that it will win by default. All it does is force other builders to match it with later bids, which does not really benefit you. It’s not so clear then that you’d have an incentive to publish before the floor-setting deadline.

---

**aelowsson** (2023-11-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> Are attesters required to broadcast their local base fee floor by some deadline?
> Can attesters broadcast their local base fee floor and then update it prior to some deadline?
> Is there some point in which attesters are absolutely committed to a base fee floor prior to their attestation, or is this just a soft definition that they can individually update prior to the proposal attestation?

The local base fee floor is never broadcast and the base fee floor as such remains unknown during the entire process. Attesters only roughly imply the base fee floor by rejecting or accepting a block. You may find the discussion in the separate [post](https://ethresear.ch/t/mev-burn-incentivizing-earlier-bidding-in-a-simple-design/17389) on a proposed change to the mechanism useful.

![](https://ethresear.ch/user_avatar/ethresear.ch/aelowsson/48/7611_2.png)[MEV burn: Incentivizing earlier bidding in "a simple design"](https://ethresear.ch/t/mev-burn-incentivizing-earlier-bidding-in-a-simple-design/17389/7)

> There is never a consensus on the burn base fee floor (in any of the designs), and it is not necessary. Each attester simply rejects any block below their subjective floor.

---

**The-CTra1n** (2023-11-16):

Nice analysis [@mikeneuder](/u/mikeneuder) . I echo these concerns though from [@jasalper](/u/jasalper) though. I’m also a bit confused about this comment:

![](https://ethresear.ch/user_avatar/ethresear.ch/mikeneuder/48/11832_2.png) mikeneuder:

> mev-burn reduces the incentive to reorg for profit.

Doesn’t a required attester committee quorom make it ~impossible to reorg? In line with some of the other comments, I’d like to see more clarity on the attester roles.

---

**mikeneuder** (2023-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/mister-meeseeks/48/5638_2.png) Mister-Meeseeks:

> But one thing that’s not clear to me, is what’s the incentive for the attesting committee to behave honestly?

this is a super important question! I do agree with you that rationale attesters might behave differently. but rationale attesters could also try to reorg for profit, and we don’t see that happening presently. I generally feel that at some point we have to rely on the honest majority of the protocol to do things, otherwise it is just impossible to reason about it at all. but I for sure understand the perspective of taking an adversarial lens to the committees.

---

**mikeneuder** (2023-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/michaelsproul/48/1060_2.png) michaelsproul:

> so this payload would not become part of the canonical chain. At least that’s what I infer from the wording:

Right. If the bid promised to burn 80 ETH and the resulting block doesn’t do so, it is invalid and the builder is slashed.

---

**mikeneuder** (2023-12-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> Considering how unaligned builders are today, this assumption seems a little naive to me.

I agree with you and [@jasalper](/u/jasalper) that assuming the market structure doesn’t evolve given a major protocol change is naïve! I think if we do go this route for mev-burn, we need to have a clear story for why the builders will bid before the cutoff.

---

**mikeneuder** (2023-12-15):

hey comet ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) hope you are well buddy. thanks for the thoughtful comment – let me answer these questions directly.

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> Is there punishment for any attester misbehavior? Under what circumstances is it considered misbehavior, and what is the punishment?

The only punishment mechanism is still slashing conditions! So equivocations are the only thing that the protocol would have visibility into. Obviously the bigger meta question is what the social layer is willing to enforce. The examples Barnabé presents in [Seeing like a protocol - by Barnabé Monnot](https://barnabe.substack.com/p/seeing-like-a-protocol) are useful to consider, especially in light of recent timing games stuff.

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> Are attesters required to broadcast their local base fee floor by some deadline?

Nope! that would add another round of communication and I am not sure who would even consume that data. Maybe the other attesters? Idk, doesn’t seem to fit IMO.

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> Can attesters broadcast their local base fee floor and then update it prior to some deadline?

They don’t communicate it! it’s just a local view

![](https://ethresear.ch/user_avatar/ethresear.ch/cometshock/48/12127_2.png) CometShock:

> Is there some point in which attesters are absolutely committed to a base fee floor prior to their attestation, or is this just a soft definition that they can individually update prior to the proposal attestation?

Same as above. They choose it locally. There is no enforcement.

Again the meta point here is what we expect protocol participants to do. If we decide we are fully giving up on the attesting committee, then most of the protocol assumptions fall apart. E.g., if attesters were fully rationale they would auction off bribery rights to the proposers around their slot to decide which block they vote on. It quickly becomes a slippery slope. I think figuring out what the fences are in the attesting committee behavior is going to be a really important excercise, and Barnabé started thinking about that in those examples he lists here: [Seeing like a protocol - by Barnabé Monnot](https://barnabe.substack.com/i/95811604/case-studies-in-upgrading-the-fence).

---

**aelowsson** (2024-06-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/jasalper/48/13925_2.png) jasalper:

> I have comments on the benefits - but will leave those for another day to focus on the “common misconceptions”.
>
>
> The two issues are actually the same, and they’re being brushed under the rug when they’re a much bigger issue than they’re made out to be.
>
>
> Collusion doesn’t have a cost and doesn’t require not bidding like the example shows. Collusion only requires not bidding before the payload observation deadline. If a builder defects to set the bid floor, the other builders can bid at that bid floor after the payload observation deadline. Bids are still accepted after the payload base fee snapshot so defecting doesn’t give you any benefits such as guaranteeing you’d win the block.
>
>
> This results in collusion being a stable dominant strategy for builders – builders get no benefit by bidding early, but they lose ETH in the case where the validator is offering mev-burn refunds. You really only have 2-3 builders with the ability to build “full value” cex-dex blocks right now - and bidding late is minimal effort, any builder could implement it in an hour if that. It seems obvious to me that both builders will immediately start doing so, if not on their own, the second a validator makes the offer to refund some portion of the mev-burn.
>
>
> Finally, the historical estimation is no good. You can look at current graphs and say that the block value is bid 80% of the total bid by the deadline. But that’s because there’s a very weak incentive to bid late now (hiding your bids from competitors). This will only get worse as a real incentive to bid late appears (maximizing your validator refund). At best this should be looked at as a generous upper bound.

This concern, which seemed to render uncompensated ePBS MEV pricing auctions (such as [EA](https://mirror.xyz/barnabe.eth/QJ6W0mmyOwjec-2zuH6lZb0iEI2aYFB9gE-LHWIMzjQ)) ineffective, has now been [resolved](https://ethresear.ch/t/burn-incentives-in-mev-pricing-auctions/19856). The builders we know today indeed derive no benefit from bidding early. However, a new type of builder will emerge, the *staker–builder*. Staking service providers must ensure that competitors do not derive a higher yield than them under equilibrium, and will run builders that bid away competitive MEV in slots where they do not propose. Anticipated attester–builder integration warrants some caution.

