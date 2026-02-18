---
source: ethresearch
topic_id: 7205
title: Hybrid Seigniorage Shares Model, Fully Collateralized --> Algorithmic
author: EazyC
date: "2020-03-27"
category: Economics
tags: []
url: https://ethresear.ch/t/hybrid-seigniorage-shares-model-fully-collateralized-algorithmic/7205
views: 2117
likes: 1
posts_count: 6
---

# Hybrid Seigniorage Shares Model, Fully Collateralized --> Algorithmic

I’ve been thinking a lot after the recent Maker drama about how no algorithmic stablecoins have ever gained much (any?) traction. I believe that part of the reason for this is all attempts/proposals for an algorithmic model start out as 0% backed stablecoin that’s doomed to instill any kind of confidence in users on day 1.

So I thought of a hybrid design that I think has a good chance of potential success and wanted the community’s feedback. It starts as standard shares and coins 2 token system like Robert Sams’ original idea but at first backed by either Dai/USDC/USDT.

1. The system starts 1 to 1 backed by Dai/USDT/USDC. Put in 1 USDC in the contract, get 1 stablecoin. This can always be redeemed back from the contract 1 to 1 at any time. Some share tokens are distributed/airdropped. Maybe share tokens can even be given away to people who bootstrap the system by minting the first stablecoins.
2. After a certain threshold market cap is reached, the system slowly moves to the seigniorage shares model in increments.
3. Every X blocks, Y coins are minted and auctioned for shares, increasing the supply of coins compared to the collateral in the contract.
4. If the price of coins remains stable, then step 3 repeats.
5. If the price of coins drop, then shares are minted to buy back Y coins and recover the price.
6. Step 3-5 repeat until the system is sufficiently algorithmic and virtually seigniorage shares so that the amount of collateral left in the contract is trivial. Or essentially the system remains at whatever fractional-collateral ratio the market supports to keep the price of coins at $1. Perhaps the market only has sufficient confidence that 30% of the coin supply can be stabilized algorithmically and the rest requires collateral. The system would remain in that band through steps 3-5 repeating.

Some problems with this setup:

- Requires a price feed for the coin and share tokens still. The onchain auctions aren’t sufficient enough to discover the price of each token. Perhaps share token holders can vote for price feeds a la MKR-type governance
- The collateral must be non-volatile crypto (Dai, USDC, USDT, but not ETH)
- There are some attack vectors in the redemption process whereby once the system is part algorithmic, a large actor could redeem a lot of coins for all of the collateral at 1 to 1 rates. A fix for this would be to change redemption during the algorithmic phase so that you can redeem partly for collateral and partly for newly minted shares. Ex: If the system is only 70% backed, then 1 coin is redeemable for 70% collateral and 30% shares to keep the ratio from deviating.

Thoughts and feedback? Improvements?

## Replies

**denett** (2020-03-29):

I think the easiest way to do seigniorage shares with partial collateralization is to use a simple Uniswap like exchange between the new stable coin and an existing stable coin like DAI. This exchange is used as the price oracle and the liquidity providers are the shareholders.

When the stable coin is overvalued, new coins are minted and added to the pool. When the stable coin is undervalued coins are removed from the exchange and burned. Everybody can provide liquidity by depositing DAI (the stable coin is minted and added as well).

Coins are created by exchanging DAI for the stable coin. This increases the price of the coin on the exchange, so over time extra coins are added to stabilize the price. The total value in the exchange is increased, so the liquidity providers make a profit. Coins can be redeemed via the exchange as well, in that case the total value in the exchange decreases and the liquidity providers are losing money.

The problem we have is that when there is a contraction nobody wants to be a liquidity provider, because then you lose money. So we need some kind of restriction on removing liquidity. We cannot restrict it fully, because then liquidity providers will not be able to extract their profits.

I was thinking of three possible restrictions:

- You can remove liquidity after a certain period (1 year?)
- You can only remove a small percentage per period (1% per week?)
- Liquidity providers earn a perpetual interest on the value of the exchange. (8% per year?)

After the liquidity providers have removed some liquidity, the system becomes under collateralized, but will still able to stabilize the value of the coin as long as the contraction is less than the value of the collateral DAI in the exchange.

---

**EazyC** (2020-04-01):

This is a really interesting setup and what I was proposing was already fairly similar in concept just without uniswap. Instead of the 1 to 1 pool of collateral, it can just be a uniswap pool of the stablecoin:collateral (which is another stablecoin like Dai). My thoughts about your setup: Why isn’t there a uniswap pool for coin:shares? Isn’t that how the system should expand or contract? Under normal seigniorage share model, the share tokens get the return from expansion of coin supply so there should be a uniswap pool for coins:shares where the system is the main liquidity provider. My slightly revised setup would look something like this:

1. Uniswap pool of COIN:SHARES
2. Uniswap pool of COIN:Collateral starting at 1:1. The collateral can be DAI or USDC etc. Anyone that provides liquidity at this rate earns SHARE tokens as a reward until some certain liquidity pool size is reached. This can be how shares get distributed at onset since there’s no ICO. The idea is that this collateral uniswap pool should reach sufficient size to establish confidence. The liquidity providers to this pool also earn fees through uniswap too so there’s double incentive.

The protocol becomes the main liquidity provider for the COIN:SHARE uniswap pool (since it can print either token at will so it’s trivial to provide liquidity and doesn’t require going out to exchanges to buy both tokens). The protocol also earns most of the liquidity revenue from this pool so there’s actual revenue coming into the system (which goes to the share token holders).

To retract stablecoin supply, the protocol provides liquidity at higher COIN to SHARE rates. To expand supply, the protocol provides liquidity at higher SHARE to COIN rates.

The protocol tries to keep the peg of COIN 1:1 to the collateral uniswap pool. More COIN:collateral pools can be added later to average out price fluctuations. The system can be designed to peg to a basket of uniswap COIN:collateral pools once it’s sufficiently large. No price feeds/oracles required.

It’s slightly different from your system the way that I understand it, but the idea is still the same. What do you think?

---

**denett** (2020-04-01):

My comments on your proposal:

- The  COIN:collateral Uniswap pool is a one-way street. You can add liquidity, but can not remove it. Because of the constant product formula, the collateral can only be retrieved at very discounted prices and can be partly stuck in the contract when all COIN has been exchanged.
- The COIN:SHARES Uniswap pool is used to reduce the supply of COIN when it is undervalued. But that does not happen when the contract is the main liquidity provider. Since participation of share owners is voluntary, it might not be possible to remove enough COIN from circulation to effect the price of COIN.

So I was thinking about the following setup:

- Anyone can buy shares from the contract using collateral. The number of shares you receive is proportional to your contribution to the collateral. So if you added 10% of the collateral, you end up with 10% of the shares.
- The collateral is put into a COIN:Collateral Uniswap pool that is used as the oracle.
- When COIN is overvalued, new COIN is minted and divided among the share holders.
- When COIN is undervalued, COIN is slowly removed from the COIN:Collateral pool, increasing  the price of COIN.

Note that:

- Because COIN is slowly removed from the pool, it is ultimately possible to extract all the collateral.
- There is no need to stop selling shares, having extra collateral when COIN grows seems logical.
- During a contraction the total collateral shrinks, this means that it will be cheaper to buy shares. So hopefully we can attract more collateral when we need it the most.
- There is no need for a COIN:SHARES pool, because we can adjust the price more efficiently by removing COIN from the COIN:Collateral pool.
- Compared to my previous proposal, the pool is now owned by the contract and newly minted COINs are simply airdropped. This way there is no longer a need to prevent the removal of liquidity.

---

**EazyC** (2020-04-04):

Thanks for your response!

> The COIN:SHARES Uniswap pool is used to reduce the supply of COIN when it is undervalued. But that does not happen when the contract is the main liquidity provider. Since participation of share owners is voluntary, it might not be possible to remove enough COIN from circulation to effect the price of COIN.

This is a good point that I hadn’t considered before. Since you can only add liquidity at the ratio, then it is not possible to change the ratio, the contract can’t expand or retract the price of the stablecoin unless it participates as an actual buyer/seller of the pool instead of liquidity provider.

With that in mind, perhaps going back to the original implementation might be simpler where the contract itself manages a fixed 1:1 coin:dai pool and independent uniswap pools that we are discussing exist as well. The contract itself is where the auction for shares and coins happen, and the uniswap pools are where arbitrage occurs.

Is there any actual advantage to natively building uniswap into the protocol instead? I feel like the restrictions of adding liquidity only at the ratio is prohibitive to expansion/retraction since that can happen inside the protocol contract itself.

---

**denett** (2020-04-06):

A contract owned uniswap pool between coin:shares can be used to do something like a Reverse Dutch Auction.

The contract will provide all the liquidity by depositing the coins and the shares. Whenever coin is undervalued the contract will slowly add shares and remove coins from the pool. This will lower the price of the shares, until the price is low enough that investors are willing to buy the shares, thus removing coin from circulation and increasing the price of coin.

I think this is more efficient than doing outright purchases on an external pool and has the added benefit that there always will be a pool available that has plenty of liquidity.

