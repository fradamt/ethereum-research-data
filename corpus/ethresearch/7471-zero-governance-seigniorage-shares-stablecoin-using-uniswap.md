---
source: ethresearch
topic_id: 7471
title: Zero-Governance Seigniorage Shares Stablecoin Using Uniswap V2
author: nourharidy
date: "2020-05-26"
category: Economics
tags: []
url: https://ethresear.ch/t/zero-governance-seigniorage-shares-stablecoin-using-uniswap-v2/7471
views: 3363
likes: 2
posts_count: 9
---

# Zero-Governance Seigniorage Shares Stablecoin Using Uniswap V2

**Prerequisites**

- A Note on Cryptocurrency Stabilisation: Seigniorage Shares
- Spencer Applebau: Potential Soros Attack against SS stablecoins

**Motivation**

IOU stablecoins such as USDT and USDC carry counterparty risk. Collateralized-debt Stablecoins such as DAI carry collateral, governance and price feed oracle manipulation risks. In an attempt to mitigate these risks, the idea of Seignorage Shares Stablecoins has surfaced since 2014 as a third alternative but is yet to be proven.

SS Stablecoins have so far faced the following challenges:

- SS Stablecoins require a price feed oracle operated by a central operator, which requires trusting a private entity.
- Private entities maintaining SS Stablecoin systems are subject to securities regulations worldwide. Basis was shut down in 2018 due to regulatory pressure.
- SS Stablecoins may be susceptible to Soros Attacks, where long-term confidence can be broken by short-term peg fluctuations.

Previous work on SS Stablecoins attempted to create a peg between the stablecoin and the target currency (e.g. USD) by introducing a two-token model, a stablecoin token and a seigniorage share token.

If the price of the stablecoin rises above the pegged asset price, the smart contract mints more stablecoin tokens and offers them for sale in exchange for the share token. If the stablecoin price falls under the peg, new shares are minted and are offered for sale in exchange for the stablecoin token.

The mechanism above is susceptible to the Soros Attack because the peg may temporarily break to a degree where confidence in a future peg recovery may be lost. Therefore, investors become less willing to buy stablecoins from the contract the further down the price drops from the peg.

**Proposal**

I propose a hard-peg USD stablecoin algorithmically-priced by a smart contract that directly regulates the *price* instead of supply or demand. The on-chain price of USDC or any other IOU stablecoin may be used as an on-chain price oracle. Once deployed, no parameters or special roles on the smart contract need to be controlled by any operator or governance mechanism.

**Architecture**

When deployed, the stablecoin contract creates a Uniswap V2 token pair between the newly-created token and USDC. The contract then becomes responsible for ensuring that the liquidity available for both tokens is always identical.

The contract exposes a public `peg()` function that can be called at any time by externally-owned accounts. Contracts are forbidden in order to prevent flash loan market manipulations.

When called, `peg()` ensures that the token pair liquidity amounts are equal. If the USDC liquidity exceeds that of the stablecoin, the stablecoin contract mints the difference and *donates* it to the token pair contract. If the USDC liquidity is below that of the stablecoin, the contract *seizes* the difference directly from the token pair stablecoin balance and burns it. After either of these operations, Uniswap `Pair.sync()` is called to *force* the pair reserves to reflect the new balance.

This effectively transforms Uniswap pool tokens into seigniorage shares for the stablecoin. If market demand increases for the stablecoin, the value of a each pool share increases as more tokens are minted and donated to the pool. If market demand decreases, the value of each pool share decreases as more tokens are seized from the pool.

**Soros Attack Defensibility**

The goal of this design is for the smart contract to directly enforce the price of the stablecoin on the exchange by algorithmically adding and removing liquidity instead of creating any incentives for buyers. Therefore, the peg is not reliant on investor confidence which defends it against Soros Attacks.

Please note that this is obviously a simplistic initial design. I would appreciate some thoughts on potential flaws and attacks.

## Replies

**aliatiia** (2020-05-26):

It’s an interesting idea to harness Uniswap’s plumbing for creating an algorithmic stable coin. It can be broken though, here is how:

---

Suppose the initial Uniswap pool is:

x = 10 SSUSD (**S**eigniorage **S**hares USD)

y = 10 USDC

k = x\times y  = 10\times10 = 100 (pool’s constant function)

Soros borrows enough SSUSD from Compound, call that amount d, such that if it’s dumped in the pool there would remain only 1 USDC:

(10+d)\times 1 = 100 \rightarrow d = 100-10 = 90 SSUSD

So he borrows in one block, and dumps in another. Now the pool has 100 SSUSD and 1 USDC. Soros has 9 USDC. The market (really the next block’s miner because she can decide if she wanted, and the miner and Soros could be the same party) could do one of two things:

(1) Call `peg()` and `Pair.sync()` … which will burn Uniswap tokens, effectively burning 99 SSUSD so as to bring SSUSD up to parity with USDC. Hence effectively 99 SSUSD evaporate which means the **liquidity providers (LPs) got rekt**. They lost 98% of their tokens in the pool.

(2) Panic and try to dump more SSUSD, the market will be fighting over that remaining 1 USDC. This means Soros succeeded. He could buy back the 90 SSUSD for fractions of USDC and pays back Compound. Since there is only 1 USDC, the maximum buying back could cost him is 1 USDC. So **Soror profit is minimum 9-1 = 8 USDC.**

Even if Soros is not the miner, and the miners are not forcing scenario (2), **why would LPs choose to risk providing more liquidity if they suspect Soros is lurking around to defend his short?**

You could try to proof against this shorting attack by limiting trade sizes, but:

1. The pool becomes very capital inefficient. There would be so much SSUSD:USDC in the pool, but for safety only a tiny fraction can be traded. LPs would most certainly pool stablecoins on a platform like Curve instead.
2. Even ignoring (1), Soros would just submit multiple transactions. If he is also the miner, he would only be losing the burnt fees (once Ethereum starts burning part of fees),  negligible for large enough trade sizes.

**Notice that d doesn’t have to be that large, just large enough to cut the LPs deep, shake confidence, and cause a run on the remaining USDC or Dai in the pool.**

---

### TLDR:

- If the pool is left on its own Soros can and will break it.
- If capital controls are put in place, not enough fees can ever be generated to attract LPs.
- Holding SSUSD brings all the risks of its Uniswap counterpart (custody, governance, oracle risks of USDC or DAI) plus its own additional risks (e.g. shorting attack above). Hence it is objectively less risky to just hold USDC or Dai directly.

---

**nourharidy** (2020-05-26):

Thank you for taking the time to reply! You raise some very important points.

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> (10+d)×1(10+d)\times 1 = 100 →\rightarrow d=100−10=90d = 100-10 = 90 SSUSD

There needs to be 900% more **accessible** SSUSD liquidity available on Compound than in the liquidity pool reserve in order for the attacker to be able to bring the reserve to 10%. Just to put it in context, if there’s only $10k SSUSD in the pool, there needs to be at least $90k available for borrow at a collateralization ratio of 150%. The cost of the attack becomes $135k+collateral risk+borrow fees against a LP loss of $9k.

To completely prevent LP panic and incentivize even more liquidity into the pool, we can create an LP token staking mechanism where LPs can stake their LP token in return for an APR denominated in the stablecoin. This reward would not be added to the reserve and would be directly paid to their accounts.

This staking mechanism also completely blocks Soros from manipulating LP confidence on the sort term.

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> (1) Call peg() and Pair.sync() … which will burn Uniswap tokens, effectively burning 99 SSUSD so as to bring SSUSD up to parity with USDC. Hence effectively 99 SSUSD evaporate which means the liquidity providers (LPs) got rekt . They lost 98% of their tokens in the pool.

In order to further prevent this scenario, `peg()` can first attempt to increase the USDC liquidity by routing swaps between half the SSUSD excess and USDC via every other SSUSD reserve, the other half is burned. For example, SSUSD:ETH → ETH:USDC, etc. Therefore, the attacker would have to deplete SSUSD reserves on every SSUSD pool. The attack cost increases up to 900% of all SSUSD reserves instead of the SSUSD:USDC reserve only.

Another more extreme alternative that requires more research: When the USDC reserve is higher than SSUSD AND more USDC is still available via SSUSD routes, `peg()` can mint more SSUSD and and swap it across USDC routes until either (A) the SSUSD:USDC reserves reach parity or (B) all USDC routes are depleted, in which case it starts burning from the SSUSD:USDC.

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> Even ignoring (1), Soros would just submit multiple transactions. If he is also the miner, he would only be losing the burnt fees (once Ethereum starts burning part of fees), negligible for large enough trade sizes.

We can call `peg()` within ERC20 `transfer()`s in and out of the pool. And if USDC routing is added, it will put each SSUSD:USDC trade transaction directly against all SSUSD reserves.

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> Holding SSUSD brings all the risks of its Uniswap counterpart (custody, governance, oracle risks of USDC or DAI) plus its own additional risks (e.g. shorting attack above). Hence it is objectively less risky to just hold USDC or Dai directly.

You might be right about this. But there’s also a different use case of creating arbitrary synthetic assets using off-chain price oracles. For example, we can fetch the USD price of AAPL using Chainlink and enforce it as the ratio between SSAAPL:USDC pool instead of the 1:1 ratio between USDC:SSUSD.

---

**aliatiia** (2020-05-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/nourharidy/48/2143_2.png) nourharidy:

> There needs to be 900% more accessible SSUSD liquidity available

![](https://ethresear.ch/user_avatar/ethresear.ch/aliatiia/48/4784_2.png) aliatiia:

> Notice that d doesn’t have to be that large, just large enough to cut the LPs deep, shake confidence, and cause a run on the remaining USDC or Dai in the pool.

There is +3000% more [DAI liquidity](https://twitter.com/MakerDaiBot/status/1265390881135366144) today outside the [Uniswap’s ETH:DAI](https://uniswap.info/pair/0xa478c2975ab1ea89e8196811f51a7b7ade33eb11) pool so it’s reasonable to assume the liquidity will be available. Notice that the size of Soros GBP short is tiny compared to the size of the monetary base of GBP.

![](https://ethresear.ch/user_avatar/ethresear.ch/nourharidy/48/2143_2.png) nourharidy:

> To completely prevent LP panic and incentivize even more liquidity into the pool, we can create an LP token staking mechanism

IMO only greed can effectively thwart panic. And to have greed, there needs to be something irresistible for the market participants to jump in and catch a falling knife. That is why Dai worked but Bitshares failed: ETH’s monetary premium is the reason. When CDPs go under water, the greed to snatch the ETH collateral at a discount is the safety valve that  brings the facility back to 150% collaterlization ratio.

![](https://ethresear.ch/user_avatar/ethresear.ch/nourharidy/48/2143_2.png) nourharidy:

> the attacker would have to deplete SSUSD reserves on every SSUSD pool.

In the analysis you can think of all the pools as one big pool, so it reduces to the same case as 1 pool with bigger size. As indicated above, however, lack of enough borrow liquidity should not be relied upon as an assumption.

---

Nonetheless I still like your stimulating idea of somehow using Uniswap liquidity tokens as a claim on (and a responsibility for) **something larger than just the pool fees** - like an algorithmic stablecoin in this case; definitely worth exploring further.

---

**denett** (2020-05-28):

In this thread we have discussed multiple variants of Seigniorage Shares using an Uniswap like pool as an oracle:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/eazyc/48/5266_2.png)
    [Hybrid Seigniorage Shares Model, Fully Collateralized --> Algorithmic](https://ethresear.ch/t/hybrid-seigniorage-shares-model-fully-collateralized-algorithmic/7205) [Economics](/c/economics/16)



> I’ve been thinking a lot after the recent Maker drama about how no algorithmic stablecoins have ever gained much (any?) traction. I believe that part of the reason for this is all attempts/proposals for an algorithmic model start out as 0% backed stablecoin that’s doomed to instill any kind of confidence in users on day 1.
> So I thought of a hybrid design that I think has a good chance of potential success and wanted the community’s feedback. It starts as standard shares and coins 2 token system…

The main problem with adjusting the price of the pool by minting or burning stablecoins is that the liquidity providers lose money when there is a contraction and stablecoins are burned. They will therefore leave when a contraction is expected, emptying the pool. To solve this we could restrict leaving the pool in some way (timeslot, fees etc).

An other way is to make the contract own the pool. For the contract to acquire the USDC collateral, it could sell the Seigniorage Shares. These shares will then collect stablecoins, whenever the stablecoin is undervalued.

---

**EazyC** (2020-05-28):

As [@denett](/u/denett) mentioned, I created a very similar thread/idea awhile ago with good discussion about the Uniswap implementation in that thread. There are a lot of challenges/restrictions that come with being forced to use the Uniswap rules for creating a SS stablecoin. After thinking about it for a while, I personally came to the conclusion that it’s best to have a custom pool of USDC/collateral for the SS stablecoin itself within the SS contract. That way, you can create the rules around the redemption and minting of the stablecoin and collateral and then have the Uniswap pools be outside-protocol liquidity and support of the system (where you get the price feed of the stablecoin against USDC/collateral etc). I’m actually working on this type of hybrid SS stablecoin myself called Frax. You can read more about it at https://frax.finance/ and it’s what originally inspired the ethresearch post denett linked.

---

**dankrad** (2020-05-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/nourharidy/48/2143_2.png) nourharidy:

> The on-chain price of USDC or any other IOU stablecoin may be used as an on-chain price oracle.

I think that’s a terrible idea. This means your oracle is only as strong as USDC. Which is custodial and can break for all kinds of reasons. And it’s still centralized.

---

**nourharidy** (2020-05-29):

I created a small Telegram group for Seigniorage Shares to discuss the issues listed in this thread. Please join in https://t.me/joinchat/Gar4_Rqvps7-rJDigbBEvQ

---

**denett** (2020-05-30):

If a decentralized  ETH-USD oracle is available, an ETH-StableCoin Uniswap could be used as well. This Uniswap pool can then be used to nudge the price of the Stable coin in the direction of the Oracle price whenever there is a divergence.

