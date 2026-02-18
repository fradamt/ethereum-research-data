---
source: ethresearch
topic_id: 7676
title: "\"What's the simplest possible decentralized stablecoin?\""
author: jacob-eliosoff
date: "2020-07-12"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/whats-the-simplest-possible-decentralized-stablecoin/7676
views: 3310
likes: 13
posts_count: 7
---

# "What's the simplest possible decentralized stablecoin?"

I sketched a design for a [“minimalist” stablecoin](https://medium.com/@jacob.eliosoff/whats-the-simplest-possible-decentralized-stablecoin-4a25262cf5e8): basically just a pool of ETH tranched into two types of tokens, the stablecoin “USM” + a leveraged-ETH/USD “FUM”, with create/redeem operations for both and that’s it.

This is a work in progress: the most interesting challenges so far involve 1. how much to charge for FUM when the pool goes underwater and 2. how to avoid the ETH/USD price oracle being front-run during real-time ETH price swings, or just manipulated.  But I think it’s at least a base model anyone interested in stablecoins should understand.

"For a while I’ve had this question in the back of my mind and, inspired by projects I admire like MakerDAO and Uniswap, over the last week I took a crack at it.  In this post I go over:

- The proposed stablecoin design, here called USM (“minimalist USD”)
- Its minimalist set of four operations: mint/burn, which create/redeem the USM stablecoin, and fund/defund, which create/redeem a related “funding-coin”, FUM
- The biggest design hurdle I hit, and my proposed solution
- A proof-of-concept implementation in ~200 lines of Python

This is really just for kicks, but a real-world implementation could be cool too as long as it doesn’t lose shitloads of innocent users’ money."

## Replies

**EazyC** (2020-07-14):

Your design is pretty simply and intuitive. It reminds me of a previous basic design attempted with the same concept: the stable token and a volatile token (which accrues the delta of the collateral backing it, people can then bet/invest in the delta of the collateral). The name of the project escapes me, but I don’t think it ever got off the ground.

Our team is actually working on a somewhat similar stablecoin that goes from being 100% collateral backed to entirely algorithmic if that interests you, you can read the whitepaper for here: https://github.com/FraxFinance/frax-solidity/blob/3aa7063c70e89e570b79f21b34a12f1793457436/frax_whitepaper_v1.pdf

One feedback I have about your design is that you might want to consider a seigniorage shares type model where the volatile token (FUM) also has rights to future seigniorage/expansions of the network.

---

**denett** (2020-07-17):

I do not think you can recover after going underwater, because there is no incentive for anybody to fund the pool in that state. If you fund an underwater pool, all USM owners can burn their USM and then there is less ETH left in the pool than you have put in.

I think it will be necessary to give the USM owners some kind of haircut.

You could think of doing a debt-for-equity swap as soon as the fund goes under water. Two USM tokens can then be swapped for one USM2 token and one FUM2 token. The old FUM tokens will be worthless.

---

**jacob-eliosoff** (2020-08-17):

I can see haircut approaches, but I’m more optimistic than you about recovery when underwater.  Buying FUM is buying highly leveraged ETH: the deeper underwater, the cheaper the FUM.  So I’m hopeful that bottom-feeders would materialize.  If enough FUM buyers arrive to pull the debt ratio back below 100%, then USM holders can burn again - the pool will shrink, but the buffer between pool value and outstanding USM won’t: in fact, as long as debt ratio < 100%, burning USM *increases* the buffer size as a percent of the total pool.

But yes, there is some risk here.  Especially on a big price drop which is of course quite realistic.  See my [latest USM post](https://ethresear.ch/t/update-on-the-usm-minimalist-stablecoin-two-new-features/7851) for a feature intended to mitigate this risk.

---

**denett** (2020-08-20):

When the pool is underwater, the burning of USM should be halted (or only at a discounted price compared to the collateralization) to prevent a bank run. But even then, the leverage of new FUM is really low and stacked against you.

If the collateralization ratio is 90% (debt ratio 110%) and suppose you can add 10% capital at an extremely diluted price such that you almost get all the FUM.

Scenario 1: Price drops 10%, collateralization ratio is again 90%, meaning all FUM is worthless (somebody else can do what you did). Leverage is 10

Scenario 2: Price increases 10%, collateralization ratio is 110%, you break even. Leverage is 0.

Scenario 3: Price increases 20%, collateralization ratio is 120%, you gain 100%  Leverage is 5.

This sounds like a really bad proposition, there are probably a lot of less risky ways to get this kind of leverage.

I think it is better to try to save the ship while it is not yet under water. So at least we need heavy collateralization and I am afraid we will need some kind of stability fee such that FUM holders are compensated during a bear market when everybody wants to hold stable coins and nobody wants to hold leveraged ETH.

---

**jacob-eliosoff** (2020-09-04):

The system as described (see especially the proof[-of-concept Python code](https://github.com/jacob-eliosoff/usm-stablecoin/blob/master/usm_constproduct.py)) actually addresses most of what you say here.  `burns` are indeed [disabled](https://github.com/jacob-eliosoff/usm-stablecoin/blob/master/usm_constproduct.py#L145) when the pool is underwater.  And the [min_fum_buy_price](https://github.com/jacob-eliosoff/usm-stablecoin/blob/master/usm_constproduct.py#L115) mechanism is meant to make sure that even when underwater, FUM buyers aren’t getting *too* crazy a discount.  (After all, in principle when the pool is underwater the FUM price would be negative, ie, paying people to receive FUM…  Clearly it mustn’t do that.)

See also some of our outstanding [issues](https://github.com/jacob-eliosoff/usm-stablecoin/issues) on topics like this, eg [#9: Consider whether constants like MAX_DEBT_RATIO = 80% should be increased/decreased](https://github.com/jacob-eliosoff/usm-stablecoin/issues/9): “I lean towards `MAX_DEBT_RATIO` = 80% rather than 90%.  It’s a pretty big difference because 90% means that if the system goes underwater, new FUM buyers are paying half the price (total FUM valuation = 10% of pool) as they are if we set max to 80% (FUM valuation = 20% of pool).  So the tradeoff is, a lower, ‘more conservative’ max will trigger a warning state (eg, FUM redemptions paused) more frequently, perhaps worsening UX for USM users; but those warning states will be less hazardous - in particular, less likely to dilute/wipe out existing FUM holders.”

I remain optimistic that 1. FUM holders will get decent risk/reward and 2. the system will avoid/cleanly recover from going underwater, but it is certainly an experiment and a risky one!  I think the [FUM limit buy orders](https://github.com/jacob-eliosoff/usm-stablecoin/issues/7) mechanism would be particularly protective - we’ll see if we can get it done.

---

**cleanapp** (2020-09-08):

hi – big like on the concept & the idea of “simplest decentralized stablecoin” – !

not as a shill, but rather as a research question, if the design goal is the simplest possible decentralized stablecoin that’s pegged to, say, the USD, what do you think about the $based approach to asymptotic dollar-ization of a synthetic crypto token?

key problem (not unique to $based, but relevant across crypto) is how to generate organic ever-growing demand. Assuming there is a based-native demand engine, isn’t an automatically-rebasing crypto a simple and elegant solution to the USD-approximation problem? description of game design available at based [dot] money.

