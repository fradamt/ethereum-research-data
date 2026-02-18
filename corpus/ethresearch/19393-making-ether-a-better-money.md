---
source: ethresearch
topic_id: 19393
title: Making Ether A Better Money
author: pantheraes
date: "2024-04-28"
category: Economics
tags: []
url: https://ethresear.ch/t/making-ether-a-better-money/19393
views: 2348
likes: 1
posts_count: 2
---

# Making Ether A Better Money

## TL;DR

In its current form, Ether (ETH) is not a good form of money. This is due to one critical limitation: its value is highly unstable. However, ETH can become stable by adjusting the rewards to validators (and thus the supply of ETH) to changes in demand for ETH. We can target a 0% inflation rate while ensuring validators are paid sufficiently to ensure network security. This new monetary policy can be called Stable Ether Monetary Policy (SEMP). With SEMP, ETH holders would have a great currency, and ETH validators would have exposure to the adoption of ETH.

## Why should ETH be stable?

It is widely accepted that a currency (i.e., a form of money) needs to function as a medium of exchange, a unit of account, and a store of value. ETH has the potential to excel at these functions, and ETH has many large advantages over existing currencies. However, ETH is not a good form of money for one reason: its value is highly unstable. **Instability makes ETH a poor unit of account and a poor store of value.**

## Why is ETH unstable?

Currently, ETH is simultaneously an investment and a form of money (for more detail, see [Bankless’ triple point asset thesis](https://www.bankless.com/ether-a-new-model-for-money)). ETH, as an investment, needs to have the potential to increase in value over time (i.e., it must be unstable). But ETH, as a money, needs stable value. **Clearly, ETH cannot be both stable and unstable, and thus it cannot simultaneously be a good investment and a good form of money.** Of course, to date, the value of ETH has varied over time, making it more of an investment than a form of money.

## What are the implications of ETH’s instability?

First, **the adoption (and market cap) of ETH is held back by it being a poor form of money.** There seems to be consensus that “monetary premium” (the value of something based on it being a form of money) is a more important driver of ETH’s value than the value it derives from burned ETH in a discounted cash flow (DCF) model. For example, in [polynya’s ranking of the top 10 drivers of ETH demand](https://polynya.mirror.xyz/GPC26Y_rlwCyPpj_N3HeW_izY1-pIVwKW5bjuPNrGeQ), four of the top five drivers rely on ETH being a good form of money. **The value of ETH is heavily dependent on it being a good form of money.**

In particular, the value of ETH is held back by it being a poor store of value. The monetary premium from being a good medium of exchange is minimal. When something is a good medium of exchange but not a good store of value, it will be bought for transactions. But it will often be sold by the recipient because it doesn’t store value. **Monetary premium comes from the demand to buy and hold the currency, which requires it being a good store of value.**

The second implication of ETH’s instability is that **liquid staking tokens (LSTs) are threatening ETH as “the de facto money of the network”** (see [this Ethereum Research post](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751)). This “leads to Ethereum users being exposed to counterparty risk inherited by the LST by default.” As explained above, ETH is currently more of an investment than a form of money. And because many view an LST as an even better investment than ETH (more upside with small additional risk), it is no surprise that LSTs could become more popular than ETH itself.

The third issue is the rise of stablecoins. Stablecoins are useful, but they have limitations. Stablecoins expose users to inflation and leave users dependent on the goodwill of centralized actors (central banks). Even though stablecoins lose value to inflation, they are still seen by many as a better store of value than ETH. This is reasonable; stablecoins’ value is much more stable than ETH’s. Stablecoins also suffer from [a trilemma](https://fortunafi.beehiiv.com/p/the-stablecoin-trilemma). **Nobody to date has figured out how to design a stablecoin that is stable, decentralized, and capital efficient.**

## What is our current goal?

**We want to transform ETH into a better form of money while maintaining a way for people to financially benefit from Ethereum’s success.**

**We want ETH to have 0% inflation, so that it is a better store of value and unit of account than other currencies.** ETH would be a programmable, credibly neutral, censorship resistant, permissionless, and decentralized form of money that is a great store of value, medium of exchange, and unit of account. **This would increase the market cap of ETH, avoid LSTs becoming the de facto money of the network, and solve the stablecoin trilemma.**

## What is the proposed solution?

**I think we can achieve our goals by constantly adjusting the ETH supply to target 0% inflation.** As ETH is bought or burned, its price increases. The price increase could be counteracted by inflating the ETH supply in the form of rewards to validators until the price of ETH arrives back at the target 0% inflation. In the reverse direction, as ETH is sold, its price decreases. The price decrease could be counteracted by offering fewer rewards to validators for some time. The overall supply of ETH can decrease from burned ETH until the price of ETH arrives back at the target 0% inflation. We can call this new monetary policy Stable Ether Monetary Policy (SEMP).

![image](https://ethresear.ch/uploads/default/original/3X/8/7/875db8dd59ac47e5111aa5623ef56dcedfb90aff.svg)

## How do we ensure validators will always secure the network?

Like today, we would need a minimum issuance curve, which states the minimum rewards to validators depending on the percent of ETH staked. The optimal minimum issuance curve needed to maintain Ethereum’s security would need to be determined by research, just as it is today.

The rewards should be in units of inflation-adjusted value. If ETH halves in value relative to the global cost of living, the ETH rewards should double. This ensures that we are paying enough for security even if ETH decreases in value.

## Would it be better to target some level of deflation?

Most economists agree that a deflationary currency is harmful to an economy. Deflation disincentives spending and makes debt more expensive to repay. In addition, it may be difficult to maintain both a level of deflation and network security. Lower levels of inflation (or higher levels of deflation) require fewer rewards to validators, but we need validators to receive enough rewards to incentivize them to secure the Ethereum network.

## Would it be better to target a low level of inflation (e.g., 2%)?

This would provide more incentive for ETH holders to become validators, providing greater assurance of the security of the network.

However, one would expect that the increase in the adoption of ETH from targeting 0% rather than 2% inflation will lead to more demand for ETH. This will provide more value for validators and help secure the network. With 0% inflation, I believe ETH validators will be rewarded sufficiently from an increase in demand for ETH as a form of money. Later, ETH could have a high and stable level of adoption. At that time, I believe fee burn would allow us to sufficiently reward validators while still maintaining 0% inflation.

**However, if we discover through research or experience that the minimum issuance curve makes 0% inflation unrealistic, we can adjust our goal to a stable and low level of inflation. In that case, ETH would still be a great currency because it would have low and predictable inflation.**

## How should we calculate inflation?

[Frax Finance’s FPI](https://docs.frax.finance/frax-price-index/overview-cpi-peg-and-mechanics) is a stablecoin designed to have 0% inflation and it “uses the CPI-U unadjusted 12 month inflation rate reported by the US Federal Government: https://www.bls.gov/news.release/cpi.nr0.htm. A specialized Chainlink oracle commits this data on-chain immediately after it is publicly released.”

Rather than relying on an external service (a Chainlink oracle), validators could serve as oracles for inflation data.

We could also improve the FPI approach by calculating a global measure of inflation, rather than one based on the US Dollar and the US economy. For example, we could calculate global inflation using country price/inflation data provided by [Numbeo](https://www.numbeo.com/cost-of-living/), [The World Bank](https://www.worldbank.org/en/research/brief/inflation-database), and/or, [the IMF](https://www.imf.org/en/Publications/WEO). We could create a global average of inflation, weighted by population.

## When the price of ETH increases beyond the target inflation rate, how do we know how much ETH to print (i.e., reward to validators)?

The Ethereum protocol can monitor prices on DEXs. Validators could serve as oracles to provide this data (in addition to inflation data). Validators that provide ETH price data and inflation data would be rewarded more than those that don’t serve as oracles. Validators that provide non-consensus price or inflation data can be penalized. These rewards and penalties can be determined by research.

When issuance needs to be increased, validators would be rewarded based on a schedule until the price hits the target. The schedule of extra issuance can be determined by research.

## What if Ethereum network activity becomes very low? Could there be a death spiral?

In this case, little to no ETH would be burned. Assuming no net buy pressure, all ETH rewarded to validators would cause positive inflation (i.e., a decrease in value).

A death spiral is possible where Ethereum network activity decreases, ETH inflates, more ETH is issued to validators, ETH supply increases, ETH inflates more, there is less demand for ETH as money, network activity decreases, and the cycle repeats (as shown below).

![image](https://ethresear.ch/uploads/default/original/3X/9/4/9416c5c93b48a5cfaa43650071bfb363cf63a54d.svg)

**The possibility of a death spiral may seem like a major drawback of this new monetary policy (SEMP), but this is no different than today.** If Ethereum network activity slowed greatly with the existing monetary policy, the value of ETH would continue to decrease. This would occur both because ETH would become a less popular form of money and because there is less burned ETH, reducing its value in a DCF model. **The value of ETH depends on people using the Ethereum network or buying it as a store of value. That is true with the existing monetary policy and with SEMP.**

**However, there is reason to believe the likelihood of a death spiral is lower with SEMP.** Because ETH would be designed to have stable value, it’s much more likely that it inflates less when network activity decreases. As the value of ETH decreases, the expectation that it will return to the target inflation rate will provide economic incentive for ETH to be purchased at a discount, increasing its value. With the existing monetary policy, ETH is designed to vary in value (as an investment), so there is less of an expectation that ETH will return to higher prices, providing less economic incentive to buy it when its value decreases.

The threat of a death spiral is not unique to ETH.. Any fiat currency can also enter a death spiral. A situation can arise where a currency inflates, people lose trust in the currency as a store of value, people sell more of the currency, inflation increases, and the cycle repeats (as shown below).

![image](https://ethresear.ch/uploads/default/original/3X/8/5/851388c38df8bf7819ca55972c18c14b5685121a.svg)

## What if a large amount of ETH is sold in a short time period?

Like the scenario above (decreased network activity), a large selling event will cause the price of ETH to decrease, which could cause both of the death spirals shown above.

However, everything stated above remains true. A large selling event could also cause a death spiral with the existing monetary policy. And there is reason to believe the likelihood of this death spiral is lower with SEMP. As stated above, there will be greater economic incentive to buy ETH at a discount with SEMP.

However, there are differences with the scenario above (decreased network activity). A large selling event could drop the price of ETH quicker than decreased network activity. But economic incentives make this scenario less likely. The seller will incur large financial losses in the form of slippage. The more they sell, the larger the financial losses will be. This disincentivizes large selling events.

## What if the supply of ETH remains constant over a long time period?

There will be no value added to ETH from net buying. Thus, to achieve 0% inflation, all validator rewards will need to be offset by the burn. This is likely to be possible at high levels of ETH adoption. However, if the burn doesn’t offset validator rewards, the ETH supply will inflate because the validators still need to be paid enough to secure the network (see the section above about the possibility of a low level of inflation). Inflation above the target rate would decrease the value of ETH, which could cause a death spiral, as described above.

Again, this is no different than with the current monetary policy. If there is an equal amount of buying and selling of ETH, there are no net inflows, and thus the price of ETH is not increased from buy pressure. In that scenario, ETH rewards to validators are either offset by the burn or the value of ETH will decrease in the long run. This could cause a death spiral, just like with SEMP.

## Is there something we can do to reduce the likelihood of a death spiral?

With SEMP, when ETH increases in value above the target rate of inflation, more ETH is rewarded to validators to increase the supply of ETH and return ETH to the target inflation rate. **To decrease the likelihood of a death spiral, we could delay the increase in supply of ETH.** To protect against a large sell event or lull in network activity, the extra ETH above the minimum issuance curve that would have been issued to validators can simply not be issued. In practice, this delay manifests as very minor levels of deflation and small reductions in validator rewards. But it would provide a buffer limiting the chances of a death spiral. The ideal amount of delay/deflation could be researched.

Note that a buffer like this is not possible with the existing monetary policy. When ETH is bought or burned, there is no way to prevent that demand from being reflected immediately in the price of ETH. **Thus, with the delay proposed above, a death spiral might be less likely under SEMP than under the existing monetary policy.**

## Replies

**pantheraes** (2024-11-09):

# Maintaining ETH’s value in Stable Ether Monetary Policy

## TL;DR

In the post above, I argued that Ether (ETH) could become a better form of money by having a stable value. This would be achieved by adjusting the rewards to validators (and thus the supply of ETH) to changes in demand for ETH. I call this Stable Ether Monetary Policy (SEMP).

The main concern with this proposal is how to maintain the value of Ether after a large selling event. To address this concern, I propose that validators be able to stake liquidity provider (LP) tokens from pools with ETH and certain ERC-20 tokens. This would provide ETH with ample liquidity, preventing a substantial decrease in the value of ETH during a large selling event.

## Would users still be able to stake ETH?

Yes, nothing would change about existing ETH-only staking.

## Which LP tokens would be accepted?

Etthereum would need to build an in-protocol automated market maker (AMM) so that validators remain in control of the protocol. EIPs can be used to determine which ETH-based trading pairs are allowed on the AMM (i.e., which LP tokens can be staked).

## What happens if a validator is slashed?

If a validator is slashed, the Ethereum protocol will redeem the LP token for the assets in the AMM and immediately sell the non-ETH (ERC-20) asset for ETH. That ETH will then be burned, like with typical slashing.

## What if the ERC-20 becomes worthless?

In this case, there would still be some ETH that can be recovered and returned to the validator. The validator would then only be staking ETH and will have lost the value of USDC that their LP token represented. Moreover, if the value of their ETH is below the staking requirement, they must be forced to unstake their ETH. This is clearly a bad outcome. To prevent it as much as possible we must be selective with which trading pairs are allowed on the in-protocol AMM. And we must provide incentive for people to stake with an LP token, given the additional risks.

## How would we incentivize the staking of LP tokens vs. ETH?

We want users to stake LP tokens, rather than just ETH, as it secures the network while providing stability to ETH. However, LP stakers must be rewarded more than ETH-only stakers because they bear more risk (as explained in the previous section).

Only half of the value that LP stakers are staking will be ETH (with the other half being one or more ERC-20 tokens). Thus, the reward per ETH would need to be double the reward to ETH-only validators. However, because of the additional risks for LP stakers and our desire to incentivize them, they must be rewarded with more than double the reward to ETH-only validators. The exact multiple can be researched and then adjusted over time once LP staking is live. Fortunately, there is a natural incentive for LP stakers in the form of trading fees from the AMM.

