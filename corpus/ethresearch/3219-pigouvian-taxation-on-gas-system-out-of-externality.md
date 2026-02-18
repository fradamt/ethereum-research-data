---
source: ethresearch
topic_id: 3219
title: Pigouvian Taxation on Gas System out of Externality
author: Danny
date: "2018-09-04"
category: Economics
tags: [resource-pricing]
url: https://ethresear.ch/t/pigouvian-taxation-on-gas-system-out-of-externality/3219
views: 4590
likes: 4
posts_count: 19
---

# Pigouvian Taxation on Gas System out of Externality

Hey! I found that in Ethereum mainnet a highly estimated Tx Fee(gas price) in first-price auctioning mechanism is going to be a sort of FOMO stuffs to blockchain peers. In that, this phenomena was presented by Vitalik at Tech Crunch, the Blockchain session in July.

Is there anyone who considered the removal of Externality problem in Ethereum TX network?

How do you think the Pigouvian Tax mechanism? I think the taxation mechanism is quite similar mechanism in a terms of on-chain protocol like a difficulty mechanism which is an cryptoeconomic rule on a protocol layer. (though the difficulty mechanism has to be adjusted by the core dev)

In my opinion, the Tax Mechanism is quite a great incentive(if there is a beneficiary of tax revenue, but not to a central node) and simultaneously a disincentive as well… The revenue issue would far more to be researched, but the Sharding’s rent model(burning the rent fee revenue) may be an good answer.

P.S) This suggestion is not for the current Ethereum main network. I’m just asking about the alternative Tx Fee Mechanism. It’s hard to fork or edit the protocol rule in a huge Ethereum network.

## Replies

**vbuterin** (2018-09-05):

I actually wrote a draft paper on this!



    ![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)

      [DRAFT: Position paper on resource pricing](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838) [Economics](/c/economics/16)




> This covers:
>
> Prices vs quantities
> Social cost curves
> First and second-price auctions
> The adjustable minfee scheme
> Storage maintenance fees
> Why fixed fees are underused in general
>
> Requesting typo checks, math correctness checks, peer review, etc.
>
>
> ethpricing.pdf (730.2 KB)

Would be happy to get your feedback on any of it if you end up getting the chance to read through.

---

**Danny** (2018-09-05):

Okay ! I’ll check the paper and make an opionion if i could mention something. Thanks ! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**Planck** (2018-09-05):

(some quick comments on the paper)

It seems very well-reasoned. A few thoughts on empirical strategy:

1. Might be nice to analyze the cost curve by finding plausibly exogenous breakpoints in block size given the processing capacity of phones, Raspberry Pis, etc. (assuming that observations exist at these levels.) While this might be a little annoying in terms of finding the actual measures for these over time, I could probably wrangle a few RA hours for this if it helps. You could even use other (possibly forked) cryptocurrencies for difference-in-difference estimation here.
2. Using the arbitrary max for a Gas Limit vote for as a discontinuity around private benefit. This is similar to what the paper mentions, but I suspect that any gas limit vote for max increase or decrease provides a semi-arbitrary cutoff.

Obviously in any case you are right to urge caution given the presumed general equilibrium effects of any of these changes. There are also some tools like propensity score matching and structural modeling you could use to bolster some of the claims but these can be a little hand-wavey (and high in Kolmogorov Complexity…)

typos:

*page 4 has a LaTex ? error, probably a missing cite.

*page 14 says “dee” instead of “fee.”

---

**vbuterin** (2018-09-07):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/p/8dc957/48.png) Planck:

> Might be nice to analyze the cost curve by finding plausibly exogenous breakpoints in block size given the processing capacity of phones, Raspberry Pis, etc. (assuming that observations exist at these levels.) While this might be a little annoying in terms of finding the actual measures for these over time, I could probably wrangle a few RA hours for this if it helps. You could even use other (possibly forked) cryptocurrencies for difference-in-difference estimation here.

If you can come up with something would be happy to cite it!

> Using the arbitrary max for a Gas Limit vote for as a discontinuity around private benefit. This is similar to what the paper mentions, but I suspect that any gas limit vote for max increase or decrease provides a semi-arbitrary cutoff.

Not sure what you mean by this. If you mean, using situations where the gas limit was suddenly upvoted or downvoted to examine what happens when supply is changed but demand is unchanged, and by doing so estimate the private benefit curve, that is exactly what [Estimating cryptocurrency transaction demand elasticity from natural experiments](https://ethresear.ch/t/estimating-cryptocurrency-transaction-demand-elasticity-from-natural-experiments/2330) is doing.

---

**Danny** (2018-09-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Would be happy to get your feedback on any of it if you end up getting the chance to read through.

I have one important question on your paper doing my Pigouvian Taxation works! It has been a great guidance to me thanks ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

In terms of Micro-econ, the negative externality has two cases.

> i) Supply Shock : The externality is driven by the supplier(Miner) who products the pollution.
> ii) Demand Shock : The externality is driven by the buyer(Tx Sender) who consume the pollution.
> and they are commonly in a problem of the “Excessive” Q in market than the optimal Q (Q*).

So, which case do you think our externality debate is more proper with?

Reading your paper, on page 10, you deducted the private benefit curve which is a demand of **TX Senders.** (not miners). Also, on page 6, you quoted the *demand shock graph*. If I got you right, does it mean you targeted the demand shock and make a regulation to the buyers? Not the miners?

I’m just wondering who is the main reason for the pollution and whom to give a tax for removal of social cost. How do I fix the supplier and buyers? In my opinion, the TX senders who set the more gas price than the average or equilibrium are the main reason of the pollution, not the miners.

---

**vbuterin** (2018-09-12):

Externalities are caused by an *activity*, not by buyers or sellers specifically. *Changes* in externalities could be driven by changes in demand or changes in supply. The theory of [tax incidence](https://en.wikipedia.org/wiki/Tax_incidence) shows that charging a fee to the buyers and charging the same fee to the sellers leads to equivalent outcomes, because in either case price changes are ultimately “passed on” to whatever combination of the two results from the supply and demand curves, so we can’t really choose which group to target.

---

**Danny** (2018-09-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> charging a fee to the buyers and charging the same fee to the sellers leads to equivalent outcomes,

The result of tax incidence is equivalent only in a circumstance that *the price elasticity* of demand and supply is **exactly the same**. ([tax incidence and elasticity](https://www.khanacademy.org/economics-finance-domain/microeconomics/elasticity-tutorial/price-elasticity-tutorial/a/elasticity-and-tax-incidence))

In that, each elasticity level of the miner and TX sender is quite important for rational tax mechanism. Also, a circumstance that the elasticity is similar between miner and tx sender is not easy to agree within a Ethereum network. In this regard, I was referring to your [paper](https://ethresear.ch/t/estimating-cryptocurrency-transaction-demand-elasticity-from-natural-experiments/2330) to check the TX sender’s demand elasticity.

Is there any result of miner’s elasticity data too ?

---

**vbuterin** (2018-09-13):

> The result of tax incidence is equivalent only in a circumstance that the price elasticity of demand and supply is exactly the same . (tax incidence and elasticity)

No, that’s the condition for the tax incidence being 50/50 between buyers and sellers. What’s true in all cases is that charging the buyer and charging the seller leads to identical outcomes because outcomes are determined by tax incidence and not who the nominal payer is.

> Is there any result of miner’s elasticity data too ?

What do you mean by miner elasticity? Miner supply responds primarily to block reward (and hence coin price), not txfees, as block reward is much larger.

---

**Danny** (2018-09-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> No, that’s the condition for the tax incidence being 50/50 between buyers and sellers. What’s true in all cases is that charging the buyer and charging the seller leads to identical outcomes because outcomes are determined by tax incidence and not who the nominal payer is.

Okay I got you on this side. I agree with the economic outcome(i.e reduction of deadweight loss) of Pigouvian taxation is always same whatever which player is going to be taxed. But the problem of “real incidence” or “tax burden” is still to be discussed.

Let’s say, if miner’s elasticity is estimated double than the tx sender’s one, it directly means he/she has a power of tax avoidance twice than the tx sender.

As I mentioned above, for even taxation as possible as we can, we need a data of price elasticity from both miner and tx sender. The 50/50 circumstance could be seen as an equilibrium, but I don’t think each elasticity level would be the same. Probably the tax burden would be gone to the more un-elastic participant.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What do you mean by miner elasticity? Miner supply responds primarily to block reward (and hence coin price), not txfees, as block reward is much larger.

Then, what do you think the ***miner supply*** in TX Fee market? In my opinion, exactly in a single block, there is a Tx Fee market in which a blockchain resource(remained block gas limit in one block) is traded between the miner and tx senders, and there has been no relevance of block reward regarding their economic position. It’s just kind of extrinsic factor I think. What is the correlation between the block reward and miner in a tx fee market?

I thought the main factor of miner supply in tx fee market is “the level of TX fee(gas price)” they get, not the block reward. The block reward is not that influencial in tx fee market.

---

**vbuterin** (2018-09-14):

> Then, what do you think the miner supply in TX Fee market?

Ah, by “miner supply” do you just mean “the supply curve of block space”? That is, if there’s a gas liimt it would be a vertical supply curve with a hard limit, say, at 8 million, with a fixed fee the supply curve would be horizontal, etc.

So I suppose the question is, how do the changes in those variables (imposed hard limit, or imposed fixed fee) affect (i) the fees paid by tx senders, and (ii) the revenues of the miners? If the demand elasticity is lower than 1, then a reduction in an imposed hard limit can actually *increase* the revenues of the miners (eg. 1% fewer txs, but then each tx pays 1.5% more, so miner revenue goes up 0.5% and tx sender costs go up 1.5%, with the exception of the senders that drop out entirely).

In the case where an imposed fixed fee is used, miners gain no (or minimal) revenue from the mechanism, and so there is no way that miners can gain or lose from a tightening. If demand elasticity is x, then an increase in the fee of 1% would reduce txs by x%, which would affect the total revenue collected by the protocol by (1-x)%.

---

**Danny** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Ah, by “miner supply” do you just mean “the supply curve of block space”?

Yes, exactly. Basically I’m approaching this externality problem in a fact that the fee market is kind of a small market placed ***`in a single block space`*** whose total revenue is called block gas limit. That’s why the miner uses a strategy for [profit maximization](https://en.wikipedia.org/wiki/Profit_maximization) in a condition of volatile P and Q.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> That is, if there’s a gas liimt it would be a vertical supply curve with a hard limit, say, at 8 million,

Well it’s hard to understand this point. The 8 MM hard limit block, just a status quo of each block, doesn’t mean the fixed Q of commodity(computation resources). Since the total revenue of miner is estimated like this. (If wrong, plz tell me ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14))

![32](https://ethresear.ch/uploads/default/original/2X/5/5a3f29b8c2785be79d44382bfb8ab7444c0313f5.png)

In this regard, the Q of the commodity is not exactly the same one with the hard limited resources, so it’s not the fixed constant.

I mean, provided the fixed revenue of block gas limit, **the Q of commodity could be volatile** following the smart contract each tx sender writes. *So, even in a hard limit, miner’s supply would not be the vertical.* **Since the Q is always going to be volatile.** But if we regulates the Q(the gas used), as I’ve already talked with [@4000D](/u/4000d) , there would be no more sophisticated contracts like Bancor, MakerDAO, etc. It’s not that good way .

---

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So I suppose the question is, how do the changes in those variables (imposed hard limit, or imposed fixed fee) affect (i) the fees paid by tx senders, and (ii) the revenues of the miners?

So, if tx fee is decreased x %, there will be no difference of miner’s total revenue since there is always tx sender’s demand to be in a block.

Whatever the level of revenue(block gas limit) or tx fee is, miners will always try to fully fill their block gas limit to maximize their profit in general. But, if the demand elasticity is too high, when the tx fee is go upper, the total revenue would be decreased.

In this point, just using the theoretical approach, miner(seller)'s total revenue can be maximized *in two conditions.*

> i) Elasticity of demand equals 1.
> Using the demand elasticity, we can check the profit maximization condition. That means, in our world, the elasticity of tx senders has to be 1. That makes the miner’s total revenue maximized. But as you already estimated, the elasticity of tx senders was over 1.
>
>
> ii) “Marginal Cost = Marginal Revenue” condition of supplier.
> This is also a profit maximization condition of each supplier in every market whatever the type of market is. (I’m still researching on these..)

As I mentioned above, whatever the hard limit is, the Q and P are simultaneously the volatile variables. And the maximization strategy itself is not influenced either.

---

So, I wonder how the fixed fee(fixed gas price right?) scenario goes on. First it is possible for the miners to have horizontal supply.

But in this case, the pigouvian tax burden would substantially go to the tx senders. Since the elasticity of miner is infinite.

---

**vbuterin** (2018-09-16):

> I mean, provided the fixed revenue of block gas limit, the Q of commodity could be volatile following the smart contract each tx sender writes. So, even in a hard limit, miner’s supply would not be the vertical. Since the Q is always going to be volatile. But if we regulates the Q(the gas used), as I’ve already talked with @4000D , there would be no more sophisticated contracts like Bancor, MakerDAO, etc. It’s not that good way .

I’m not sure that I understand this. The gas limit **is** the limit on the quantity of commodity (gas, ie. computation resources) that could be consumed in each block.

> ii) “Marginal Cost = Marginal Revenue” condition of supplier.
> This is also a profit maximization condition of each supplier in every market whatever the type of market is. (I’m still researching on these…)

Currently, marginal cost for a miner is zero until the limit, at which point it is infinite. In the scheme I describe in the paper, marginal cost would be some constantly adjusting fee F until the limit, at which point it is infinite.

---

**Danny** (2018-09-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The gas limit is the limit on the quantity of commodity (gas, ie. computation resources) that could be consumed in each block.

Yes, this is the fact. The block gas limit (i.e. 8MM) is fixed *total tx fee(P*Q)* from every consumption, **not the quantity limit per each resource**. I think I’ve observed this market more in detail.

As you said, the gas limit is the sum of every TX consumption. **But, it’s not the Q in the market.**

In a single block, the Q between the miner and sender is exactly the **gas used** which is consumed **by each tx sender**, not a *block gas limit*.

![](https://ethresear.ch/user_avatar/ethresear.ch/danny/48/2151_2.png) Danny:

>

As I attached above, *Gas Used* is Q and *Gas Price* is P of computing resources in tx fee market per a single block. And the gas used is volatile following each gas usage of transaction. This was what I defined in a block space.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Currently, marginal cost for a miner is zero until the limit, at which point it is infinite

In PoW mining, I agree with the marginal cost is almost zero currently. Then, what is the certain point of infinite marginal cost? I couldn’t understand this point. Does it mean the difficulty bomb ?

---

**vbuterin** (2018-09-16):

> Yes, this is the fact. The block gas limit (i.e. 8MM) is fixed total tx fee(PQ)* from every consumption, not the quantity limit per each resource . I think I’ve observed this market more in detail. As you said, the gas limit is the sum of every TX consumption. But, it’s not the Q in the market.

Ah, I think you’re misunderstanding the concept of gas. The block gas limit is a limit on \sum Q_i; “gas” *is* Q. There is no in-protocol limit on the amount of revenue (or \sum P_i * Q_i) that can be earned by a miner in a block.

> Then, what is the certain point of infinite marginal cost?

That just means that there is no way to create a block with more than 8 million gas no matter how hard you’re willing to pay, so the cost curve to the miner can be said to shoot up to infinity at that point.

---

**Danny** (2018-09-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The block gas limit is a limit on ∑Qi\sum Q_i; “gas” is Q. There is no in-protocol limit on the amount of revenue (or ∑Pi∗Qi\sum P_i * Q_i) that can be earned by a miner in a block.

Cool it has been more clarified thx!! There could no fixed fee revenue. I totally misunderstood ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

But still, there is no change of volatile Q, not the fixed Q in the tx fee market I think. The block gas limit is just a sum of each Q(computation resource, the gas).

Now I understand why you thought the gas limit is a limited quantity and the miner supply is finally deducted as vertical, which means zero elasticity. You meant the [market supply curve](https://www.quora.com/What-is-a-market-supply-curve) in a block space, right?

`Let's say in a 8 million gas limit and there are three types of txs.`

> i) TX type 1: 50,000 gas used per tx * 100 txs = 5M gas
> ii) TX type 2 : 100,000 gas used per tx * 10 txs = 1M gas
> iii) TX type 3 :  200,000 gas used per tx * 10 txs = 2M gas
> ( Gas Price would be different per tx… )

Each type of gas(Q) is on trade and every tx sender pays a gas price per tx. Yet, as you can see, miner doesn’t sell fixed quantity of computing resources(gas) at each different price in a market. I think in a block space, the miner is a kind of *monopoly producer* and he has a power to choose the price and quantity ***arbitrarily.***

---

**vbuterin** (2018-09-16):

> Now I understand why you thought the gas limit is a limited quantity and the miner supply is finally deducted as vertical, which means zero elasticity. You meant the market supply curve in a block space, right?

I suppose the most accurate way to describe it would be as the miner’s cost function.

> I think in a block space, the miner is a kind of monopoly producer and he has a power to choose the price and quantity arbitrarily.

That is true, but because of the one-period nature of the game (the transactions are already broadcasted), the miner never has an incentive to do anything other than just accepting everything.

---

**yaliu14** (2018-09-23):

I’m wondering if you know of more resources on a few points in the paper that stood out to me:

p.8-10 - discussion of superlinear costs as the weight limit increases - are there insights from the discussion

of the blockchain network structure or other (e.g. https://arxiv.org/pdf/1801.03998.pdf by Gencer, Basu, et. al.) that can help us estimate the point at which superlinear terms begin to dominate the marginal social cost function?

p.11 - on real world experiments to estimate demand elasticity for transactions -

with respect to the discussion on an adjustment speed parameter on p. 20, what metric on the demand volatility

to use to determine/modify this parameter.

I’m new to mathematical finance (computational physicist here), but I worry that some feature of the stochasticity in the demand could lead to some sort of high frequency trading strategies - this is just my intuition, I’ve nothing

to back it up. Not sure if this needs to be worked into the pricing rule on p. 19-20.

Minor edits:

p.10 - perhaps cite [6] for the “Cornell study”, and perhaps mention the part of the study that suggests that

the marginal cost function is sublinear

---

**vbuterin** (2018-09-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/yaliu14/48/1478_2.png) yaliu14:

> p.8-10 - discussion of superlinear costs as the weight limit increases - are there insights from the discussion of the blockchain network structure or other (e.g. https://arxiv.org/pdf/1801.03998.pdf by Gencer, Basu, et. al.) that can help us estimate the point at which superlinear terms begin to dominate the marginal social cost function?

Here’s one possible model. Suppose there is a block time of 1 minute, and if blocks take N minutes to propagate and verify (we’ll use minutes as the common unit for simplicity; clearly N < 1), then if a block is received, there is a probability N that the next block will be created while that block is still being verified, creating an off-chain block, which would also need to be verified, but would not contribute to the chain. This already creates a cost of N + N^2, and following the logic further gets us to N + N^2 + N^3 + ... = \frac{N}{1-N}. In Ethereum’s case, N \approx 0.15 at present.

> with respect to the discussion on an adjustment speed parameter on p. 20, what metric on the demand volatility to use to determine/modify this parameter.

In the limit, if the parameter is too high (ie. approaches infinity) you’ll get unnecessarily large fee volatility, and if the parameter is too low you’ll get too many periods where blocks are full as the fee slowly adjusts upwards to a new demand level. If the goal is to maximally avoid the second problem, then you would want to set it as high as possible without creating unneeded instability or nullifying the advantage of short-term fee predictability. I feel like trading off between these goals is an art more than a science, though would definitely welcome any attempt at coming up with a more rigorous way of selecting the constant.

> I’m new to mathematical finance (computational physicist here), but I worry that some feature of the stochasticity in the demand could lead to some sort of high frequency trading strategies - this is just my intuition, I’ve nothing

What do you mean by “high frequency trading strategies”? The choice available to individual users is to either send a transaction at some particular time or not send one. It’s not a market of the same type as a financial trading market.

