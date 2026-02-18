---
source: ethresearch
topic_id: 4104
title: In defense of PoW
author: nagydani
date: "2018-11-03"
category: Economics
tags: []
url: https://ethresear.ch/t/in-defense-of-pow/4104
views: 1970
likes: 2
posts_count: 7
---

# In defense of PoW

After bubbles, PoW cryptocurrencies have a tendency to enter prolonged low-volatility periods. It is hypothesized that the fundamental reason behind it is a negative feedback mechanism tied to electricity consumption by miners:

Bubbles result in a build-up of miner capacity in excess of post-bubble demand; the crash of the market price of the PoW cryptocurrency results in some of the less efficient miners reaching the so-called shut-down point, where mining revenues do not cover opex costs (mostly electricity).  This also implies that the profit margins on mining are thin and the miners are forced to sell the majority of the newly minted coins on the market. Thus, market price fluctuations are closely followed by the hash rate because of marginally efficient miners going online and offine with ups and downs, respectively. Therefore, the value of freshly minted coins showing up on the supply side of the market, measured in electricity consumption, closely follows the price, increasing and decreasing the supply with the price. The total amount of freshly minted coins entering the market is roughly constant, as miners spend almost all of their revenue on opex.

Strong speculative forces can and sometimes do jolt the market out of this equilibrium, but in their absence the observable volatility is remarkably low over extended periods of time. Abrupt advances in miner efficiency and other situations where miners cannot be brought online sufficiently fast following increases in market price can disrupt this equilibrium permanently. However, sharp declines in market value usually result in a new equilibrium of similar nature at a price point different from the previous one.

Without PoW, PoS validators are not forced to sell almost all their revenues, as their opex is almost negligible compared to the revenue and even more importantly unrelated to the price of the coin in which they are rewarded for validation. The absence of the above described feedback mechanism anchoring opex to the market price as measured in a commodity in the physical world severes the link of PoS cryptocurrencies to value in physical reality.

## Replies

**nagydani** (2018-11-04):

More on the negative feedback mechanism [here](http://superposition.hu/en/blog/ethereum-fundamental-analysis).

[![ethereum_price_and_hash_rate](https://ethresear.ch/uploads/default/original/2X/3/3b77148efd1420bfe7e9a8e3f6005195f66050aa.jpeg)ethereum_price_and_hash_rate958×530 47.5 KB](https://ethresear.ch/uploads/default/3b77148efd1420bfe7e9a8e3f6005195f66050aa)

---

**vbuterin** (2018-11-04):

I actually got the opposite conclusion from this fact!

In an upturn, miners only need to sell only a portion of their revenues, but in a downturn miners need to sell close to all of their revenues, which means selling pressure is higher in downturns than in upturns, which exacerbates cycles.

> Therefore, the value of freshly minted coins showing up on the supply side of the market, measured in electricity consumption, closely follows the price, increasing and decreasing the supply with the price. The total amount of freshly minted coins entering the market is roughly constant, as miners spend almost all of their revenue on opex.

I agree that this is true during downturns, but I don’t see how it makes the price more stable. The value of **all** coins showing up on the supply side of the market goes up and down with the price, so that’s an effect that exists in all assets.

---

**nagydani** (2018-11-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I actually got the opposite conclusion from this fact!
>
>
> In an upturn, miners only need to sell only a portion of their revenues, but in a downturn miners need to sell close to all of their revenues, which means selling pressure is higher in downturns than in upturns, which exacerbates cycles.

I think that there are two clearly distinct situations:

1. Rallies when the prices are growing so fast that hashing power can only be added by investing in additional hardware which necessarily lags behind the price. This can be observed in the price & hashrate chart before April, 2018. During such rallies, miners can (and do) keep a substantial part of their revenue, because profit margins are wide, even inefficient miners are profitable. All mining hardware is online, running at full steam.
2. Upturns, when mining is marginally profitable and there is large offline mining capacity for which the operating costs (mostly electricity consumption) do not justify operation at the given price, but can be brought quickly online as soon as the price goes up. In such upturns, profit margins on mining are thin, miners spend most of their revenue on electricity.

The latter can only occur after buildups caused by the former. Indeed, empirical evidence seems to suggest that extended periods of low volatility (when the negative feedback mechanism works both ways) happen after major crashes.

I agree that when speculative pressure cause the price to go high enough to eat up all available mining capacity, the negative feedback loop is broken and the rally is egged on by a positive feedback of miners HODLing an increasing fraction of their revenue that thus fails to show up on the supply side of the market.

Similarly, when mining is highly profitable, downturns simply eat into the profit margins without forcing excess miner capacity offline (between January and August, 2018), which, as you correctly state, is a positive feedback mechanism exacerbating the crash. However, after the shutdown point of the least efficient miners is reached, the downturn slows down, leaving behind a lot of mining capacity that can be brought online as soon as the price goes up, even a little bit. At this stage, a negative feedback loop is established, keeping volatility low for long periods of time.

I argue that for PoS assets, the economics is similar to high miner profit periods (between November and April, 2018) of PoW assets, when the hashrate is increasing even during downturns (e.g. beginning with January). These are high-volatility periods with positive feedbacks at work. However, unlike PoW assets, there is nothing to stabilize the price after a long downturn and there is no direct link to any physical value (like electricity).

---

**bharathrao** (2018-11-05):

Market value does not just depend on selling pressure of the producers (ie miners/stakers) but the demand/supply of the entire market. In a bear market *everything* will go down, regardless of costs of production. (Check NEO and other staking coins.)

---

**oliverbeige** (2018-11-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In an upturn, miners only need to sell only a portion of their revenues, but in a downturn miners need to sell close to all of their revenues

To make things a bit more complicated, some of the more successful miners might sit on both fiat and crypto reserves which they could spend to prop up prices, while the marginal miners will only shut down when revenue falls below variable costs (mostly electricity, I assume), esp. if they have debt to serve. So you’re looking at contribution margins, not profit margins.

So that’s a bunch more variables to juggle, but casual empiricism would suggest that the miners with deep pockets buy up coins whenever they drop below MC.

---

**dlubarov** (2018-11-08):

If we accept that ASICs will eventually take over any PoW algorithm, aren’t ASIC miners be unlikely to hold tokens anyway? They already hold a long position due to their hardware investment, and holding mined tokens would mean doubling down on that long position, increasing their risk.

If anything, I would expect sophisticated ASIC miners to sell token futures when purchasing hardware, to hedge against downturns. They can’t predict exactly how difficulty will change in the future, so they can’t eliminate all risk, but selling futures would minimize it.

