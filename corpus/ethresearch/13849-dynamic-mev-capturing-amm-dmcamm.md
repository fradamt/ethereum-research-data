---
source: ethresearch
topic_id: 13849
title: Dynamic MEV Capturing AMM (DMcAMM)
author: markus_0
date: "2022-10-04"
category: Applications
tags: []
url: https://ethresear.ch/t/dynamic-mev-capturing-amm-dmcamm/13849
views: 3184
likes: 0
posts_count: 5
---

# Dynamic MEV Capturing AMM (DMcAMM)

Hey all, like these two other excellent threads which I recommend reading -



    ![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png)
    [MEV capturing AMM (McAMM)](https://ethresear.ch/t/mev-capturing-amm-mcamm/13336) [Applications](/c/applications/18)



> MEV capturing AMM (McAMM):
> A prevailing thought is that the power of transaction ordering is mostly in the hands of block-builders in the current MEV-Boost and PBS specifications. In this write-up, ideas for new AMM designs are presented that would shift the transaction ordering power, at least partly, to AMM designers and liquidity providers. These constructions would allow AMMs to capture part of the MEV that is currently only harvested by block-builders and proposers.
>
> High-level idea:
> New …



    ![](https://ethresear.ch/user_avatar/ethresear.ch/nikete/48/10338_2.png)
    [MEV Minimizing AMM (MinMEV AMM)](https://ethresear.ch/t/mev-minimizing-amm-minmev-amm/13775) [Applications](/c/applications/18)



> Towards minimal-MEV-AMM via Direct Elicitation
> I have been thinking about AMM designs that directly elicit initial prices to offers traders, as a way of reducing the amount of MEV that can be extracted from LPs. Attention conservation notice: very raw work in progress.
> Passive liquidity providers give away for free a  straddle to those who first trade with them. Directly ellicit the price vector that removes this free stradle seems possiblein principle: it is the final price vector in the bloc…

I’m proposing a new MEV Capturing AMM model that, while not quite as efficient at capturing MEV(reducing LVR), is significantly simpler than the versions discussed above. Basic motivation is the same as the other threads, AMM’s currently leak a lot of MEV/suffer from Loss-Versus-Rebalancing. I’m proposing using a dynamic fee AMM to address this rather than first right auctions, hence the name Dynamic MEV Capturing AMM(DMcAMM).

## High-level idea:

Liquidity pools use a dynamic fee that decays over blocks and resets every time someone swaps through the LP. This mechanism allows LPs to capture backrunning profits, is likely a more profitable fee mechanism than current static fee systems, and has the potential benefit of making sandwich attacks less feasible.

## Implementation:

The implementation would follow standard AMM implementations. However, instead of storing the swap fee in state, it would calculate the swap fee on the fly based on how many blocks have passed since the last swap through that pool. The pool would also have to record the block number every time a swap is performed. This would result in slightly more expensive swaps for the additional logic and write per swap.

**Note:** This implementation has the fairly significant issue of block number not being an especially granular or accurate measurement of the volume of market activity since the last swap. A potential fix would be adding an additional factor to the fee scaling, such as the number of swaps performed globally by the protocol since the last time the pool in question carried out a swap. However, granularity might not be an issue in low-blocktime environments like rollups, so maybe this is unnecessary.

## Discussion:

The main goal for this DMcAMM construction was to capture the majority of important MEV without adding significant complexity to the AMM. To this end, we can break AMM MEV into three types and analyze if/how this construction captures it:

1. Sandwiching -
The DMcAMM construction makes all but the largest sandwich attacks unprofitable because the frontrun swap raises the LP fee to its highest level for both the user and backrun swaps. Thus it doesn’t effectively capture sandwich MEV. That said, I don’t think it’s important to focus on capturing sandwich MEV as tools like COWswap and private builder transaction flow will make sandwiches significantly less common. Verdict: Unnecessary to Capture
2. Internal-Orderflow Arbitrage -
Here I’m referring to arbitrage from a user’s swap creating a backrun opportunity. Fees that decay over blocks allow the LP to take a significant cut of the MEV from backruns since the initial swap resets the LP fee to its highest level, effectively initiating a dutch auction between backrunners. Large backrun opportunities may not have large fee sharing since their profits can far exceed the LP’s pre-decay fee. However, I’m not convinced we should be concerned with large backrun opportunities as they are uncommon and will become even less common as execution and UX improve. Verdict: Captured
3. Stale-Price Arbitrage -
Here I refer to arbitrage created by the AMM offering an out-of-date swap quote that creates an arbitrage opportunity with a different market. Decaying fees capture this MEV fairly well in high volatility conditions since quotes frequently become stale, meaning frequent arbitrage swaps and consistently high fees. However, they do a very poor job internalizing this MEV in low volatility conditions as quotes will become stale slowly, meaning fees have time to decay quite low. I don’t think failure to capture in low-volatility conditions is a significant issue. First decaying fees mean the pool will likely capture organic flow before toxic flow, given that volatility is low. Furthermore, the vast majority of stale-price arbitrage occurs in high-volatility conditions. Verdict: Captured when most important

In conclusion, if parameters can be set correctly, a DMcAMM does a sufficiently good job capturing MEV (or reducing LVR, whichever term you prefer). That being said, there is one other benefit worth discussing. There has recently been a lot of discussion around dynamic fee AMMs, mainly thanks to research like Crocswaps. The main finding of that research is that high fees are better for LPs in high-volatility conditions. The DMcAMM construction raises fees in high-vol conditions since it resets the fee to its highest point every swap, conforming to research recommendations.

There are also a few downsides of this construction worth discussing. Primarily, AMM UX would be worse due to the constantly fluctuating fee. I don’t see this as a breaking issue as users will eventually swap mostly through routers which could hopefully handle the fee fluctuations behind the scenes, but it’s still worth considering. Secondly, as discussed previously, in slow-blocktime environments setting a starting fee and sane decay factor is likely difficult, if not impossible. Finally, killing sandwich attack viability could be bad as they subsidize low-fee LPs on-chain and may improve pricing.

Anyway, I hope people found this model interesting. Feel free to shoot me a DM or just respond here if you wanna discuss further.

## TLDR

**Solution:** Make AMM fees dynamic and have them decay over blocks, resetting them every swap through their pool.

**Pros:**

- Simple
- Captures most relevant MEV
- Conforms to recent dynamic fee research

**Cons:**

- Parameters are hard to set depending on the environment
- Could make UX worse
- Reducing sandwich attacks is maybe bad

**Other Related Work:**

Loss-Versus-Rebalancing: https://anthonyleezhang.github.io/pdfs/lvr.pdf

Dynamic Fee Research: [Designing a Dynamic Fee Policy that Outperforms All Uniswap ETH/USDC Pools | by CrocSwap | Medium](https://crocswap.medium.com/designing-a-dynamic-fee-policy-that-outperforms-all-uniswap-eth-usdc-pools-8948b0cc72ab)

## Replies

**vivien98** (2022-10-14):

[Kyberswap](https://files.kyber.network/DMM-Feb21.pdf) is an AMM that does something similar I think. They use dynamic fees that change based on the ratio of short term and long term volume, where each of these is calculated in an exponentially moving averaged way. So this effectively works like a decaying fee model where the increase in fee after any trade is proportional to volume.

However, a question here might be : what if an LP does wash trading to keep fees up artificially before an incoming swap from a user? In fact, does this not incentivize the LPs to do a sandwich attack?

---

**markus_0** (2022-10-19):

Hadn’t seen Kyber’s model before, that’s interesting. Definitely similar, I think using a straight-up dutch auction would be more efficient for capturing backrun MEV during low-vol periods though. The biggest issue with both of these models is they don’t do a great job capturing CEX<>DEX arb, which probably makes up most DEX flow atm

And yeah that’s definitely a concern, any AMM implementing this would have to allow users to choose a maximum_slippage+fee rather than just a maximum_slippage

---

**vivien98** (2022-10-19):

> The biggest issue with both of these models is they don’t do a great job capturing CEX<>DEX arb, which probably makes up most DEX flow atm

Didnt quite get why there is a difference between DEX<>DEX and CEX<>DEX arbitrage?

> And yeah that’s definitely a concern, any AMM implementing this would have to allow users to choose a maximum_slippage+fee rather than just a maximum_slippage

Agreed. One more question might be - what should the exact value of fee that it should increase to after a trade be so that it covers any possible [LVR/arbitrage loss](https://arxiv.org/abs/2208.06046#:~:text=In%20a%20frictionless%2C%20continuous%2Dtime,%2C%20pronounced%20%22lever%22).)? Kyber uses a specific formula, but that does not seem to be motivated by LVR.

---

**markus_0** (2022-10-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/vivien98/48/10496_2.png) vivien98:

> Didnt quite get why there is a difference between DEX<>DEX and CEX<>DEX arbitrage?

I suppose the DEX <> DEX vs CEX<> DEX arbs isn’t the correct comparison. It’s more about whether the arb was created by internal or external flow. Dutch auctions capture internal flow based arb really well since the fee is high (someone swapped) but not so much external flow arb since no one swapped before the arb.

![](https://ethresear.ch/user_avatar/ethresear.ch/vivien98/48/10496_2.png) vivien98:

> Agreed. One more question might be - what should the exact value of fee that it should increase to after a trade be so that it covers any possible LVR/arbitrage loss.)? Kyber uses a specific formula, but that does not seem to be motivated by LVR.

Not sure, it heavily depends on how liquid the pool and assets are. You can definitely pull historical arb data to optimize it, but I haven’t had a chance to yet

