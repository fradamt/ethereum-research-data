---
source: ethresearch
topic_id: 17258
title: The Influence of CeFi-DeFi Arbitrage on MEV-Boost Auction Bid Profiles
author: tripoli
date: "2023-10-31"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/the-influence-of-cefi-defi-arbitrage-on-mev-boost-auction-bid-profiles/17258
views: 3280
likes: 20
posts_count: 4
---

# The Influence of CeFi-DeFi Arbitrage on MEV-Boost Auction Bid Profiles

# The Influence of CeFi-DeFi Arbitrage on MEV-Boost Auction Bid Profiles

Data Always - October 31, 2023

**Acknowledgements**. Thank you to [Comet Shock](https://twitter.com/cometshock) and [Justin Drake](https://twitter.com/drakefjustin) for feedback and discussions that spurred this analysis. The results should not be taken as a reflection of their opinions on the topic.

## Motivation

Previous modelling of MEV-Boost auctions has concentrated on generating a holistic picture of [builder behavioral profiles](https://ethresear.ch/t/empirical-analysis-of-builders-behavioral-profiles-bbps/16327), but has not accurately portrayed special cases resulting from market volatility. This analysis aims to shed light on the steep [rise in integrated builders](https://twitter.com/specialmech/status/1691178038640492544) and the class of action that they dominate.

| Related Works | Author |
| --- | --- |
| MEV burn—a simple design | Justin Drake |
| The path to and impact of MEV-Burn on Ethereum | Data Always |
| Empirical analysis of Builders’ Behavioral Profiles (BBPs) | Thomas Thiery |
| Time to Bribe: Measuring Block Construction Market | Anton Wahstätter et al. |
| In a post MEV-Burn world - Some simulations and stats | Anton Wahstätter |
| Bid cancellations considered harmful | Mike Neuder et al. |

## Methodology

We leveraged Binance [1-second interval K-line](https://www.binance.com/en/landing/data) ETH/USDT data to identify the slots with the highest intrablock volatility between January 1, 2023 and September 30, 2023. We also investigated the slots with the highest absolute price changes and found similar end results. We chose to focus on intrablock volatility to demonstrate that base asset price spikes and crashes are not the only contributing factor, and that improvements in CEX efficiency may not mitigate the dynamic. Further research should expand this methodology to consider other top ERC-20 tokens.

We calculated the trailing 12-second volatility and then resampled the dataset into 12-second intervals aligned to beacon chain slots intervals. We then sorted the slots by volatility and enriched the data with winning bid values and builder information from mevboost.pics. Finally, we downloaded corresponding auction bid data from the Flashbots, ultrasound, Agnostic and bloXroute relays to model the profile of block bids for known integrated builders (beaver, rsync and manta) against the rest of the builder market.

We modelled both mean and median bid profiles, but present median values here to remain in line with prior research.

We used a control sample of 12,000 slots (starting at slot 7,000,000) as a reference for bid distributions, projected burn share, and to model cancellation times. Ideally this sample would have been larger, but all findings in the control were in line with prior research. The control sample is only used for comparisons to tagged slots.

## Results

We found that integrated builders won a minority share (41%) of auctions between January and September 2023 but dominated the tagged high volatility slots, winning 65% of the top 2,500 auctions. These numbers should be treated as lower bounds of the current dynamic, as the share of all blocks won by integrated builders has increased throughout the year and currently sits at 52% for the past 14 days, despite manta-builder [ceasing operations in May](https://frontier.tech/builder-dominance-and-searcher-dependence). The relative share of builders can be seen in Figure 1.

[![01-integrated-builder-share-of-auctions](https://ethresear.ch/uploads/default/optimized/3X/1/2/12620eeb60c8b414b15431c93c41cfc86bdffbc3_2_690x314.png)01-integrated-builder-share-of-auctions1620×738 88.4 KB](https://ethresear.ch/uploads/default/12620eeb60c8b414b15431c93c41cfc86bdffbc3)

> Figure 1: Integrated builders won an outsized share of tagged high volatility slots, while all other builders saw sharp dropoffs in their share of blocks. Titan Builder’s share saw the largest decrease, but this is likely due to the higher concentration of tagged blocks early in the year (before Titan Builder began operating).

Prior research, which can be seen in Figure 7, demonstrated a linear increase in bid values. However, as seen in Figure 2, our tagged slots show that integrated builder bids follow a two-stage nonlinear profile when leveraging CeFi-DeFi arbitrages. Integrated builders tended to withhold their best bids until two seconds before the canonical block time, only matching the top non-integrated builders until the final moments of the slot. Until the divergence, integrated builder bid values likely contain no proprietary bids and consist of public mempool transactions and transactions sent in by other searchers.

[![02-bid-profiles-tagged](https://ethresear.ch/uploads/default/optimized/3X/4/9/49864d2cf9f582b714c90819e70b8aa2b59636b4_2_690x373.png)02-bid-profiles-tagged1500×812 68 KB](https://ethresear.ch/uploads/default/49864d2cf9f582b714c90819e70b8aa2b59636b4)

> Figure 2: In the median tagged auction, the leading integrated builder bid only surpasses non-integrated builder bids after the proposed MEV-burn cutoff. This suggests that the current proposal is blind to CeFi-DeFi arbitrage.

Under the current MEV-burn proposal, the size of the burn in these slots is determined by non-integrated builders, while the majority of the block value is generated by integrated builders after the burn has been decided. This framing is especially important because as frontends continue to work to eliminate sandwich transactions and to reduce overbidding of priority fees, CeFi-DeFi arbitrages will likely be unaffected and may begin to dominate a greater share of auctions.

If we consider all auctions, burning the first 10 seconds of bids would [historically have been effective](https://ethresear.ch/t/in-a-post-mev-burn-world-some-simulations-and-stats/17092). In our all-slots control sample, seen in Figure 3, only 7% of blocks would have burnt less than half of their MEV payout under the current proposal, and the mean burn for both integrated and non-integrated builders would have been 80%.

[![burn-share-all](https://ethresear.ch/uploads/default/optimized/2X/a/ac76fcb907085ef35790fbbc46f2b21f4a76ba33_2_690x373.png)burn-share-all1500×812 58.2 KB](https://ethresear.ch/uploads/default/ac76fcb907085ef35790fbbc46f2b21f4a76ba33)

> Figure 3: Our control sample shows that the current MEV-burn proposal captures the majority of MEV, and that only a small share of auctions have significant earnings after the 10-second cutoff. Columns farther to the left see a smaller relative share of their auction value captured by MEV burn.

Switching back to high volatility slots, those won by non-integrated builders retain a semblance of the all-slots profile, but these are generally false-positives in the data tagging; they are slots where integrated builders chose not to commit heavily to CeFi-DeFi abitrages.

The distribution for slots won by integrated builders, seen in Figure 4, is closer to a uniform distribution; the value burned is disconnected from the winning bid value. 41% of tagged high volatility slots won by integrated builders would have seen less than half their value burned versus 26% of slots won by non-integrated builders.

[![burn-share-tagged](https://ethresear.ch/uploads/default/optimized/2X/0/0a61aa209de1be70533728f30a90c0b9bf97f37d_2_690x373.png)burn-share-tagged1500×812 60.6 KB](https://ethresear.ch/uploads/default/0a61aa209de1be70533728f30a90c0b9bf97f37d)

> Figure 4: The current MEV-burn proposal is ineffective at capturing the value of our tagged special cases, particularly when examining auctions won by integrated builders. If the frequency of these special cases is expected to grow in the future, the MEV-burn proposal may need adjustment.

We can also model the sensitivity of burn efficacy to the choice of burn bid time delta. In Figure 5, we see that the efficacy for high volatility slots is nonlinear, and delays or modifications could result in drastic changes.

[![burn-efficacy](https://ethresear.ch/uploads/default/optimized/2X/e/e5fcb87c8d0bcbd23ff590c6d6cee2989e1bb099_2_690x373.png)burn-efficacy1500×812 89.6 KB](https://ethresear.ch/uploads/default/e5fcb87c8d0bcbd23ff590c6d6cee2989e1bb099)

> Figure 5: The efficacy of the MEV-burn proposal for our tagged slots is highly sensitive to the choice of cutoff time. These blocks do not conform to the linearity assumptions that underpin current efficacy estimates. One of the assumptions underpinning the leading MEV-burn proposal is that block proposers select the block with the maximum payout, but in historic data this is not always the case. This leads to a quirk in the data where if delta is set too aggressively would involve burning more than the realized payouts.

## Terminal Shape of Bid Profiles

With the potential for MEV-burn to lead to more timing games, it’s crucial to properly categorize the terminal shape of bidding profiles. Previous research has suggested that these bidding curves have a distinct peak. Thiery’s modelling (Figure 6), showed it to occur at approximately 2 seconds after the slot time and [Wahstätter et al.](https://arxiv.org/abs/2305.16468) obtained a quadratic function peaking at 2.78 seconds.

[![builder-profiles](https://ethresear.ch/uploads/default/optimized/2X/f/fe0615e964db670c1604d6ba7ac99c8e45c6fd56_2_690x329.jpeg)builder-profiles1920×918 154 KB](https://ethresear.ch/uploads/default/fe0615e964db670c1604d6ba7ac99c8e45c6fd56)

> Figure 6: Past research has categorized a definite peak in auction bid profiles. This implies that timing games are bound by both the ability of proposers to get enough attestations and the maximal bid value of the auction. We believe that these maxima are a mirage in the data. Source: Empirical analysis of Builders’ Behavioral Profiles

In our opinion, these maxima are mirages in the data. If the values were true peaks, then we should expect to see a flood of cancellations at and after the peak. However, other modelling demonstrates that this isn’t the case and that cancellations tend to occur much earlier in the slot.

We recreated this modelling and confirmed [Neuder et al.'s](https://ethresear.ch/t/bid-cancellations-considered-harmful/15500) findings, and then extended their modelling of bid cancellations to the special case of volatile slots, finding that the rate of late cancellations was even lower in our tagged blocks.

[![cancellations-tagged](https://ethresear.ch/uploads/default/optimized/2X/c/c04c8b2018c053e368d1297b88fb34ac922776ef_2_690x373.png)cancellations-tagged1500×812 40.6 KB](https://ethresear.ch/uploads/default/c04c8b2018c053e368d1297b88fb34ac922776ef)

> Figure 7: The majority of meaningful (i.e., leading) bid cancellations occur early in the slot. Very few slots see cancellations that would suggest that bid values are not monotonically increasing in time.

Our analysis, seen in Figure 7, shows that across the four relays, only 1 in 4.4 tagged high volatility auctions had its leading bid cancelled more than 1 second after the canonical block time, and only 1 in 25 slots had its leading bid cancelled more than 2 seconds after the canonical block time. These results demonstrate that prior bids would have remained valid, and that lower median incoming bids are primarily noise and not meaningful to auction dynamics.

The foundation of timing games research is that auction values trend up in time. Since builders have nothing at risk, it follows logically that their average bids should be monotonically increasing.

## Discussion

Although MEV-burn is a good idea, the leading proposal has significant gaps that the community must acknowledge and should consider addressing. The proposal [is blind](https://barnabe.substack.com/p/seeing-like-a-protocol) to the business model of the two fastest growing (and now largest) builders; combined, these builders win over half of auctions and [both censor](https://censorship.pics) OFAC non-compliant transactions.

The community expects the worst MEV offenders (sandwich transactions) to be solved out-of-protocol by changes to dApp frontends, however, this will also serve to weaken the competition faced by integrated builders and may further centralize the PBS landscape by increasing the relative importance of off-chain or cross-chain MEV. The hopeful solution to reducing CeFi-DeFi arbitrage seems to be to shift DEX liquidity onto L2, but this comes with significant trade-offs and relies on third parties to decentralize their platforms adequately.

Ethereum should only enshrine monetary policy changes that pass the highest bar, yet the ecosystem is evolving too rapidly and the potential ramifications around MEV-burn remain poorly understood.

## Open Questions

- How much of a role do other ERC-20s play in tagging high volatility slots?
- If DEX liquidity moves to L2s, what will be the effect on CeFi-DeFi arbitrage?
- As front-ends reduce the number of sandwich transactions, will integrated builders become more competitive in all slots?
- In an MEV-burn world, would integrated builders choose to further delay their bids to make the nominal difference a larger factor in auctions?
- Are proposers more willing to play timing games in low value auctions?
- If proposers begin to play more aggressive timing games, how much later will bids show up in the data? Where will the peak of the traditional bid profiles extend to?
- If bid cancellations become considered toxic and are removed from auctions, what will be the effect on MEV-burn efficacy?
- How does the distribution of bid cancellations change if we normalize the data for auctions that have already finished?

## Replies

**The-CTra1n** (2023-11-01):

Feels like there is a lot of interesting data here. As someone who does not know much about how OFAs are run, can you share some more information in this regard?

I’m particularly interested in how OFAs are settled. I guess OFA auctions would need to be settled some time before the proceeding beacon chain slot to allow builders to integrate the orderflow into their blocks. Instinctively, orderflow would be more toxic/informed/impactful during periods of high vol., so winning/losing the OFA will drastically affect the perceived profits in the MEV-Boost auction.

Handling orderflow during high vol is specialized, so it makes sense that it is dominated by the best builders. From reading the article, it feels like you think this is a bad thing? (at least, that you think it is bad for MEV-burn? The pivot to MEV-Burn confused me)

Do you have data on the bid-profile splits in the OFAs between integrated and non-integrated builders? This plus the MEV-burn proceeds would give a clearer view of the net MEV that is repaid by builders, right?

If non-integrated builders are highly uncompetitive in OFAs, users would be net worse off without integrated builders. If this were true, then even a small set of competing integrated builders would be better for the ecosystem than a gaggle of non-integrated builders. The data might show otherwise, but would be very interesting to see.

---

**tripoli** (2023-11-02):

> Instinctively, orderflow would be more toxic/informed/impactful during periods of high vol., so winning/losing the OFA will drastically affect the perceived profits in the MEV-Boost auction.

Yes, or at least that was the thesis here around identifying slots more likely to be won by integrated builders. I do regret confining the volatility tagging to the ETH/USDT pair. This analysis is better framed as a proof-of-concept that shows more research is needed, rather than a total picture.

> Handling orderflow during high vol is specialized, so it makes sense that it is dominated by the best builders. From reading the article, it feels like you think this is a bad thing?

If you check out a day like October 24, 71% of [MEV-Boost slots](https://mevboost.pics) were built by two integrated builders. This centralization is generally trending up not down, and with solo stakers + self-builders already getting squeezed by an increasing validator set and ideas like minimum viable issuance, I don’t really see it reverting naturally.

I personally wouldn’t consider this a good outcome.

> If non-integrated builders are highly uncompetitive in OFAs, users would be net worse off without integrated builders. If this were true, then even a small set of competing integrated builders would be better for the ecosystem than a gaggle of non-integrated builders.

If the flow is toxic or integrated builders are driving volatility on CEXs in order to profit from DEX inefficiency then I would suspect that most people will be worse off. If less efficient builders handled more of it then price efficiency might be a worse, but there would be LVR reduction and the dynamic would be healthier.

An interesting extension might be to look at the equivalent price volatility profiles on Binance and see if price volatility is uniformly distributed or correlates with slot times. If prices change more later in blocks that could suggest that arbitrage can drive CEX volatility.

> The pivot to MEV-Burn confused me

This is totally fair, it would have fit better as two topics, even if a lot of the data would have been shared. As of late, a lot of the conversation around MEV-burn has been framed by conversations on CeFi-DeFi arbitrage. For example, sound clips [like this](https://twitter.com/bloXrouteLabs/status/1703872705878020275), where researchers are assuming or circulating naive assumptions around bid profile linearity.

I’m not anti-burn, I actually really like most of its properties. Just want it to be done as effectively as possible.

---

**The-CTra1n** (2023-11-03):

An endgame with 2 integrated builders doesn’t sound great, but I’m not sure if 5 or more integrated builders is so bad. The centralization we are seeing might just be a result of existing builders being phased out, maybe we should be encouraging more integrated builders? It comes back to my questions around the inefficiencies of non-integrated builders. I’m not sure.

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> If the flow is toxic or integrated builders are driving volatility on CEXs in order to profit from DEX inefficiency then I would suspect that most people will be worse off.

I think this could be mixing up the causality of volatilty. Builders profit from CEX vol against DEXs because the external market price (“true” price at that instant) is typically far from the DEX price. Integrated builders are better at extracting because of lower latency/better pricing of vol, full-block oversight, etc. A builder causing vol would mean the builder is disagreeing with the external market price. This is a losing strategy.

The only time “causing vol” might make sense would be where the arbitrageur knows that moving a price up 1% in one market causes lots of market makers to move their prices, and provide enough liquidity at this fake price to create a net profitable opportunity by moving the price back down. This is market manipulation in TradFi. For this strategy to work against DEXs… I would assume it isn’t possible.

