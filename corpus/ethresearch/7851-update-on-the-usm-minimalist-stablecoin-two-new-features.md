---
source: ethresearch
topic_id: 7851
title: "Update on the USM \"minimalist stablecoin\": two new features"
author: jacob-eliosoff
date: "2020-08-17"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/update-on-the-usm-minimalist-stablecoin-two-new-features/7851
views: 2452
likes: 6
posts_count: 3
---

# Update on the USM "minimalist stablecoin": two new features

Just an update on the USM “minimalist stablecoin” design I [posted about last month](https://ethresear.ch/t/whats-the-simplest-possible-decentralized-stablecoin/7676).  A few of us have been poking at it and I have a fresh post, [USM “minimalist stablecoin” part 2: protecting against price exploits](https://medium.com/@jacob.eliosoff/usm-minimalist-stablecoin-part-2-protecting-against-price-exploits-a16f55408216), describing two new features:

1. Make large create/redeems more expensive, by moving price dynamically à la Uniswap.
2. When the system is underwater and needs funding (FUM buyers), make the FUM price decline over time.

With these changes, I’m actually pretty enthusiastic about this stablecoin design, and we’re going to try to get it into production!  Collaborators/feedback welcome, see the post.  The dream here is a very simple, easy-to-use, reliably-pegged stablecoin that’s truly permissionless/ownerless, in the way Uniswap is, so our whole ecosystem doesn’t end up built on top of semi-permissioned infra like USDT/USDC.  (Though if the market goes to DAI that works too!)

## Replies

**denett** (2020-08-20):

I am wondering how the mint_burn_adjustment and fund_defund_adjustment work when there is a big price change that is only reflected by the oracle after some time.

After the change, arbitragers take advantage of the discrepancy and buy/sell until the adjusted price is equal to the real price. When the oracle comes with the updated price, does that mean that the price is out of equilibrium again and the arbitragers have another opportunity?

This could be solved by changing the adjustments when the oracle updates the price, such that the on-chain price is unaffected. We still need to slowly reduce the adjustments to make sure the on-chain price cannot drift away from the real price.

You also might want to implement the front-running remedy proposed in here:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)
    [Improving front running resistance of x*y=k market makers](https://ethresear.ch/t/improving-front-running-resistance-of-x-y-k-market-makers/1281) [Decentralized exchanges](/c/decentralized-exchanges/17)



> Two years ago I made a post where I suggested that we could run on-chain decentralized exchanges in a similar way to what Augur and Gnosis were proposing for on-chain market makers (eg. LMSR), and Martin Köppelmann from Gnosis suggested a simple approach for doing so, that I call the “x*y=k market maker”. The idea is that you have a contract that holds x coins of token A and y coins of token B, and always maintains the invariant that x*y=k for some constant k. Anyone can buy or sell coins by ess…

---

**jacob-eliosoff** (2020-09-04):

It’s true that a significant risk is the oracle falling behind live exchange prices, allowing fast traders to front-run the system, and potentially drain it over time.  The Uniswap-like “sliding prices” mechanism introduced in post #2 above is intended to mitigate this…  We’ll have to see whether an on-chain oracle can be accurate enough to resist these exploits.

To your specific question about the adjustments, the short answer is that they only move one side of the market, not both - effectively widening bid-ask.  Eg, buying makes further buys more expensive; it doesn’t make sells cheaper.  So no, when the oracle’s price catches up with reality, that shouldn’t introduce another arbitrage opportunity.  Example:

1. Real-time price is $400, oracle price is $400, both mint_burn_adjustment and fund_defund_adjustment = +0% (no adjustment)
2. Real-time price drops to $390, oracle still $400.  Trader takes the opportunity to mint (aka sell ETH for USM) at $400.
3. Because of the “sliding-price” mechanism, this selling pushes mint_burn_adjustment to $390 / $400 = -2.5%.  At this point, users can sell ETH (mint) for $400 - 2.5% = $390, or buy ETH (burn) for $400 + 0% = $400.
4. Oracle price catches up to RT price: both $390.  So now, users can sell ETH for $390 - 2.5% = $380.25, or buy ETH for $390 + 0% = $390.  Neither of these opens up an arbitrage.
5. Over the next period (few minutes?) without trading, mint_burn_adjustment gradually shrinks back to +0%, so that soon the sell price has tightened back to $390 - 0% = $390.  Buy price is still $390.

An additional possible mitigation is to make our oracle support a distinction between buy price (the price buyers pay) and sell price.  Eg, the buy price could be the *highest* price from a few other oracles, and the sell price the *lowest.*  This would create an extra safety gap between the two, and cause the gap to widen when markets were volatile, which seems healthy.

And yes, the adjustments closely resemble Vitalik’s “virtual quantities” scheme, widening one side (but not the other) on trades.  I believe I read that post when it came out but tbh I’d forgotten about it - but maybe it influenced me subconsciously.  Or perhaps I was influenced by some Bitcointalk forum post from 2011 ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

