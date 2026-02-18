---
source: ethresearch
topic_id: 13775
title: MEV Minimizing AMM (MinMEV AMM)
author: nikete
date: "2022-09-27"
category: Applications
tags: [cryptoeconomic-primitives]
url: https://ethresear.ch/t/mev-minimizing-amm-minmev-amm/13775
views: 4840
likes: 11
posts_count: 14
---

# MEV Minimizing AMM (MinMEV AMM)

# Towards minimal-MEV-AMM via Direct Elicitation

I have been thinking about AMM designs that directly elicit initial prices to offers traders, as a way of reducing the amount of MEV that can be extracted from LPs. Attention conservation notice: very raw work in progress.

Passive liquidity providers give away for free a  straddle to those who first trade with them. Directly ellicit the price vector that removes this free stradle seems possiblein principle: it is the final price vector in the block. The block builder is in the perfect position to compute such starting prices. They seem like the natural agent to execute this price setting.

I conjecture that direct elicitation of final in block prices and their use as starting prices,  with a deposit that collateralizes the max net exposure the AMM is taking at any point on that block, is optimal for passive liquidity providers.

The AMM  can pre comit to pay the builder a small share of the profits for this service. If it only offer liquidity on blocks in which a builder has set its prices, the AMM would not appear to be exposed to the volatility in-between blocks. It seems possible to build such a AMM with mevboost already.

## A Simple mechanism

The AMM only provides liquidity in a block if it has already interacted with the initial price setting transaction from the builder setting its initial price and placing a deposit.

- The AMM takes all transactions as long as its net position entered on that block is not higher in value than the deposit
- A fee plus the deposit is given to the builder on the next block if the final price is equal to the starting price the builder reported.
- If the final price did not match the initial then the deposit is given to the LPs of the AMM and no fee.

## a variation for partial fills and inter-block liquidity

The value of the deposit is the net position the AMM is taking in the block (this allows for example to provide liquidity to bigger orders that cant be exactly balanced). Note that to the extent the trades inside a block balance perfectly there is no risk for the builder of losses in the deposit.

To accept order types that cannot be patially filled the net-bond mechanism seems like it should extends naturally by using prices of the AMM in future blocks to price the value of the taken positon at the end of the previous block.

## related work: LVR, McAMM

The free stradle perspective is in https://moallemi.com/ciamac/papers/lvr-2022.pdf

A closely related idea recently in the forum is the [MEV capturing AMM (McAMM) - #20 by josojo](https://ethresear.ch/t/mev-capturing-amm-mcamm/13336/20)  . It auctions off the first trade right, to recapture of the MEV that is emited due to the initial prices being different from the end prices.

- Like it, the Min-MEV-AMM relies on builders ordering a specific transaction in the block before those that trade with the AMM.
- Like the McAMM all trades would revert if the intiial price vector call with bounty was not used on a block.
- Unlike it, it does not require those with information about prices to trade into positions to move prices. It tries to not emit the extractable value in the first place.

So far have only been thinking about eliciting the starting prices, not the fee level. But the block builder knows the realized volatility in the block, so could also set the optimal fee level (aka bid-ask spread) to extract profits form the orderflow it is including in that block.  The net fee paid to the builder would then be a linear share in the fee plus LVR the AMM collected.

## Replies

**josojo** (2022-09-27):

Nice, I like! It solves the LVR-redistribution challenge that McAMMs have not really solved. It’s also way more gas efficient than auctioning off MEV.

![](https://ethresear.ch/user_avatar/ethresear.ch/nikete/48/10338_2.png) nikete:

> If the final price did not match the initial then the deposit is given to the LPs of the AMM and no fee.

How do you set the tolerances for stating `initial price == final price`? E.g. assuming there is only one trade in block from a normal retail user, then the intital price will always be different from the final price, right?

Also, for the example with 1 trade on an AMM pair in one block, how do you prevent that the price-setter is setting the price such that the slippage tolerance of the one trade is fully exploited, and then in the next block, the price setting mechanism sets it back to the normal price?

---

**nikete** (2022-09-27):

Glad you liked it [@josojo](/u/josojo) !

If there is a single trade then in the simplest version of the mechanism there has to be a wait until a opposing trade comes along and both get included in a block, and you have no tolerances so you need partial fill to be able to in practice do much. I present that version of the mechanism for conceptual simplicity, but with partial orders for heavily traded markets it seems practical.

In the more practical version if there is a single trade, the builder that puts it into the block is effectively taking the other side of it with their deposit; the tolerance is how big of a deposit they can put in. That deposit will be held until the next time the market trades and is effectively taking the other side of the trade. So the builder is the one effectively taking the risk of the inter-block liquidity in this design.

So this design minimizes the MEV it exposes by not providing any liquidity in between blocks (since effectively the builders deposit is the thing at risk in between the blocks).

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Also, for the example with 1 trade on an AMM pair in one block, how do you prevent that the price-setter is setting the price such that the slippage tolerance of the one trade is fully exploited, and then in the next block, the price setting mechanism sets it back to the normal price?

The price setter can’t guarantee that they will be next blocks builder, and if they leave the price outside of the equilibrium price they are opening themselves up for someone else to pay a higher fee to build that block and take their deposit when correcting the price.

---

**alexnezlobin** (2022-09-27):

In which token(s) should the block builder deploy the collateral? And which prices will be used to determine if the collateral is sufficient?

The questions above appear to be tricky given that the block builder supplies the prices. Looks like the only way to make it risk-free to LPs is to make sure that the builder contributes enough collateral in each token to cover the max deviation of that token’s balance in the AMM. But then the block builder essentially ends up filling all the orders. This may generally be a good idea, but not all builders have the skills/tools/liquidity to be market-makers.

---

**nikete** (2022-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexnezlobin/48/9749_2.png) alexnezlobin:

> In which token(s) should the block builder deploy the collateral? And which prices will be used to determine if the collateral is sufficient?

In the simplest version the block builder can deploy the deposit in the token that the AMM is net selling on the block. There is no need to price it.

Note the builder is never risking it since they control the block so they can make sure the initial price equals final price condition is not violated. They only need to use the net collateral during the transactions.

If it is possible to check that a transaction is at the end of block, then it might be possible to not need to have the deposit across blocks, and a flash loan could be used, so it ca be capital free. I would be keen to hear form people who know the EVM better than me how plausible that is.

![](https://ethresear.ch/user_avatar/ethresear.ch/alexnezlobin/48/9749_2.png) alexnezlobin:

> This may generally be a good idea, but not all builders have the skills/tools/liquidity to be market-makers.

The builders can provide expressive languages for searchers that specialize in this market making subtask, it is basically just saying in a bundle that some memory slots cant be accessed by any transactions outside the bundle.

---

**alexnezlobin** (2022-09-27):

> In the simplest version the block builder can deploy the deposit in the token that the AMM is net selling on the block. There is no need to price it.

But how does the AMM know *during* the block which side is going to be the net seller by the end of the block? The block builder may know that some token, let’s call it Loona, has crashed. Then they can report its price as very high and make the deposit in Loona. After that, they can sell a bunch of Loona to the AMM at the high price and give up the deposit.

Looks like the only solution would be to make sure that the AMM never touches any liquidity except for the amounts provided by the builder.

---

**nikete** (2022-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexnezlobin/48/9749_2.png) alexnezlobin:

> But how does the AMM know during the block which side is going to be the net seller by the end of the block?

A example may be in order.

4 trades are in the mempool, two buys of ETH worth 3 dai  each, and two sells of ETH worth  6 dai.

Now if the buidler sequences so the AMM gets

[buy of 3 dai worth of eth, sell of  6 dai worth of eth, buy of 3 dai worth of eth]

The deposit at the begining can be 3 dai worth of eth, and 3 dai. The net position of the AMM  going through the sequence of trades above is never higher than either of those, so it is never running any risk.  The builder knows that the start and end price are the same since the buy and sell net out, so his deposit has no risk.

Note that there was no need to price anything in this simplest case. Note also one of the 6 dai sells is left unmatched in the mem pool.

---

**alexnezlobin** (2022-09-27):

Yes, but in your example, can’t all these trades be filled from the deposit alone? Precisely in the sequence in which you ordered them?

In other words, what is the role of AMM liquidity if the block builder needs to provide enough liquidity for all trades?

---

**nikete** (2022-09-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/alexnezlobin/48/9749_2.png) alexnezlobin:

> In other words, what is the role of AMM liquidity if the block builder needs to provide enough liquidity for all trades?

Yes in that example I simplified far enough that there is effectively no role being played by the liquidity in the AMM, indeed. However, note that you can use the prices of the AMM itself plus some overcolateralization ratio, so that the deposit could be just the safe asset (i.e. the lowest volatility one in the pair). this could be generalized to not holding either asset but a third safe asset that thereis a path through these AMMs to convert into the two in the specific pool.

More generally, I expect that in practice some flash loan like construct can be made where the builder is borrowing and repaying the liquidity from the AMM itself so hold neither token nor has to put up any deposit if there is no liquidity being provided between blocks (the buys and the sells net out in the block).

---

**alexnezlobin** (2022-09-27):

Yes, if builders could take out a loan for the duration of their block, one could develop some interesting mechanisms. I think that overcollateralization might be the only way to ensure that they return it though.

Let me throw in one more thought: it may be non-trivial for the builder to find an initial price and a set of transactions such that the ending price is the same. It is relatively easy to do with static swaps, but with smart contracts this problem is essentially unsolvable. They would be looking for a fixed point of some program, and it would be easy to DoS them.

---

**nikete** (2022-09-28):

I think a proof that the builder carried out the right algorithm when building the block is more likely than a loan to be part of the end-state of MEV minimimized AMM. This could be implemented either cryptographically or economically via an optimistic contract.

A couple of implicit conjectures in the construction above that might help to spell out. The MEV minimized AMM has:

1. uniform pricing, offering liquidity in two mass points and the bid and the ask.
2. cant take any risk; since doing so would emit some MEV when the risk is realized to the builder that is updating it’s oracle.

The seccond in particular poses quite severe limits of the welfare any MEV minimized AMM can achieve. I think it is important to understand this limit well to be able to structure AMMs that have better efficiency and welfare characteristics while being aware of MEV in their design; they will not minimize MEV but instead to structure it appropriately to create permisionless incentives that maximize their objective.

The complexity of finding a fixed point is intrinsic to mechanisms that need to have good incentive properties in equilibrium. Nash equilibria are fixed points.

In terms of what this provides; the liquidity that is compatible with minimizing MEV is that which happens inside the block; the same net matching could be achieved without any passive LPs but it would break composability inside the block. Minimal MEV AMM structures can only use the LPs passive liquidity in a riskless way so can only be used inside the block,  It basically buys you composability with other contracts relative to matching the orders onchain without the passive liquidity.

---

**nikete** (2022-10-02):

One thing that came up on a side conversation with [@josojo](/u/josojo) is that for the liquidity provisioning between blocks, ideas related to [[1112.0076] Bandit Market Makers](https://arxiv.org/abs/1112.0076) might make sense

---

**eljhfx** (2022-10-12):

If this is just shifting the costs of LVR onto block builders (away from LPs), it seems like you’d still need some highly efficient (probably off-chain) auction or exclusive order-flow sale in order for this to be effective - since builders won’t want to take on the risk unless they were being amply compensated by searchers/institutions.

The nice part is definitely that it gives the application more control over the distribution than current models.

---

**nikete** (2022-10-12):

The builders can already run an auction for searchers bundle inclusion. The auction that the Flashbots builder currently runs is not quite expressive enough to make it safe for a searchers to participate in this protocol as described, but it would be easy to make it so. At a minimum what would be needed was for a bundle to say that for it to be included in a block some memory slots cant be touched before or after the bundle. This could be implemented in the contract and use current flashbot bundles if you used not only a “open market at these prices” transactions at the start of the bundle but also a “close market for the block” transaction at end of block.

It also combines well with ideas around orders starting with negative fees that then increase with the block number. Effectively an ascending price procurement auction for orderflow inclusion. This is IIUC also currently implementable by a searcher.

