---
source: magicians
topic_id: 5755
title: "EIP-3416: Median gas premium"
author: hexzorro
date: "2021-03-18"
category: EIPs
tags: [gas, eth1x, core-eips]
url: https://ethereum-magicians.org/t/eip-3416-median-gas-premium/5755
views: 3874
likes: 17
posts_count: 26
---

# EIP-3416: Median gas premium

This [EIP (Median gas premium)](https://github.com/ethereum/EIPs/pull/3416) targets the following goals:

- Gas prices spikes are mathematically smoothed out. EIP1559 does not seems to really solve gas premium volatility.
- Maintain gas price preference, i.e. transaction senders willing to pay extra in fees will be rewarded with early preferential inclusion in the blocks, because the miners want to maximize their profits and include transactions with higher fee caps first to maximize the median.
- Final gas price paid by the sender is, most of the time, smaller than the maximum gas price specified by sender.
- Gas pricing is more robust to sender manipulation or miner manipulation.
- Avoid changes to wallets, be backward-compatible with existing wallets.

Any feedback will be appreciated.

## Replies

**mtefagh** (2021-03-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hexzorro/48/3607_2.png) hexzorro:

> Gas prices spikes are mathematically smoothed out. EIP1559 does not seems to really solve gas premium volatility.

I totally agree with this part and have had similar recommendations before, e.g., [here](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838/24). However, to reduce volatility we should also smoothen the base fee whose volatility is incentivized in EIP-1559 as described [here](https://ethresear.ch/t/path-dependence-of-eip-1559-and-the-simulation-of-the-resulting-permanent-loss/8964).

---

**hexzorro** (2021-03-26):

Let’s include your formula for BASEFEE in [EIP-3416](https://github.com/ethereum/EIPs/pull/3416), just edit and send a PR.

Cheers,

---

**hexzorro** (2021-03-26):

Already the fox for BASEFEE volatility in the latest PR [here](https://github.com/hexzorro/EIPs/blob/patch-2/EIPS/eip-3416.md).

---

**hexzorro** (2021-04-04):

UPDATE: we are removing the fees destination issue to focus on Median and Base Fee features, on this EIP.

---

**hexzorro** (2021-04-04):

NEW UPDATE on [EIP-3416](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3416.md) (Median Gas Premium): We *removed* the following changes and their impact:

1. No impact on how the fees are paid, including the decision or burning or not.
2. No impact on Block Size, Block Gas Limit, etc.

We hope we can get more reviews on the EIP to move forward. The two alternatives to implement this EIP are:

1. Continue proposing this EIP as an alternative to EIP-1559 with No Impact on Wallets, as only miners are affected. This might be pointless if there is already a big commitment to EIP-1559.
2. Add these changes after/with EIP-1559, so we can include the needs fields, so can be included in the following fork. Technically, even if we are not fans of the wallet changes, our EIP can be added on top of EIP-1559 as the two improvements: Premium Pricing and Base Fee calculation.

---

**timbeiko** (2021-04-04):

[@hexzorro](/u/hexzorro) I have a few questions from a first (somewhat quick!) read of the EIP. Apologies if these are dumb questions.

1. The EIP says “The gas premium, determined directly by a specified fee cap, can either be set to a fairly low value to compensate miners for uncle rate risk only with the base fee, or to a high value to compete during sudden bursts of activity.”. What does it mean to set the gas premium?
2. The EIP says “The median gas premium plus the base fee is given to the miner.” How does this square with your above statement of " No impact on how the fees are paid, including the decision or burning or not." Are you saying there is no impact compared to now (i.e. no fees will get burnt) or no impact compared to EIP-1559?
3. The EIP says " Set GASPRICE = BASE_FEE + median((tx_i.gasPrice - BASE_FEE) / 2) among all transactions tx_i included in the same block, weighted by gas consumed and not including the top 5% of outlier gas price in calculation." How do you expect to know in advance which transactions are included in a block? You basically need to build the block before you execute the transactions, right? If so, how do you keep that efficient for miners? How can they know in advance how many transactions can be included? Walking through the flow of how a miner picks txns from the pool, and build a block, would be valuable.

Thanks !

---

**barnabe** (2021-04-05):

Thanks for the write-up! To summarise, the proposal bundles two things:

1. Setting an additive update rule for basefee, as prescribed by @mtefagh to avoid incentive issues with the multiplicative rule
2. Having the gas premium fixed by the protocol, based on what the user declares as their max_fee.

Point 1. I think is fairly uncontroversial, there’s some evidence that the current multiplicative update rule isn’t optimal, though it’s unclear without data in which ways and what the best fix would be.

Point 2. is a much more fundamental change to the design of EIP-1559. First, there are claims at the beginning of this post that imo aren’t fully supported:

> EIP1559 does not seems to really solve gas premium volatility

This seems incorrect. It’s been shown that unless the effective demand is higher than the block limit (which is `slack` times the block target, with `slack == 2` currently), there is no incentive to set your gas premium to anything other than the miner marginal cost, meaning that most of the time gas premium estimation is actually really simple and offers good guarantees, even when congestion increases (I wrote about it [here](https://barnabe.substack.com/p/better-bidding-with-eip1559) for instance, curious to know your thoughts!)

> Final gas price paid by the sender is, most of the time, smaller than the maximum gas price specified by sender.

This is also the case in 1559, but 1559 has an additional guarantee: that you will pay the *smallest* possible gas price *at the time of inclusion*. By letting the protocol fix the premium to half the difference between your max fee and the current basefee, it’s not clear to me how that doesn’t induce overpayment.

To take an example, suppose between every two blocks you have the same distribution of users showing up, with users having intrinsic value distributed uniformly between 0 and 10, and users showing up at twice the rate necessary to fill blocks entirely, then you ought to price out 3/4-ths of these users, so that roughly only users with value > 7.5 can be included. In the “vanilla” 1559 design, `BASE_FEE` would settle around 6.5, assuming all bidders pay a gas premium equal to 1, which is roughly the miner marginal cost (this “stationary environment” is also developed in [our article](https://arxiv.org/abs/2102.10567), or [my simulations](https://barnabemonnot.com/abm1559/notebooks/stationary1559.html)). This is obviously an idealised representation but I think it’s good enough to show that the possibility exists, even in this simplest of all settings.

I’ll try to tease out what the situation would be in your proposal, because I think it might give insight into the inner workings of the median premium rule. To simplify, I’ll drop first the assumption that only 95% of transaction weight is considered to take the median over, and take the median over all included transactions. Let’s assume all users truthfully reveal their value as max_fee. Since the mechanism still targets inclusion of users with value above 7.5 (given our example that we have twice the gas limit worth of users), included users have max_fee set uniformly in the interval [7.5, 10]. Assume basefee is 7.5, then premiums are distributed uniformly in the interval [0, 1.25] and the median premium is 0.625, which is what the miner receives on top of basefee or not, depending on whether you are burning basefee, which isn’t clear as [@timbeiko](/u/timbeiko) pointed out.

Assume basefee isn’t burned and is given entirely to miners. In this stationary example, if basefee was lower than 7.5, there would be potentially more users included than the target allows for, and vice versa for basefee higher than 7.5, so 7.5 is indeed the value basefee would tend to. As long as users bid some max_fee greater than 7.5, they will be included, as the miner would receive positive profit. One equilibrium strategy in this stationary environment is for all users in the top quartile to bid max_fee = 7.5 + epsilon: they will all be included and pay epsilon/2 premium. Note that this equilibrium is identical (up to epsilon) to the equilibrium in the vanilla 1559 mechanism: top 25% users are included and pay 7.5 (+ epsilon/2). It is also an equilibrium for all users to declare truthfully their value, but that equilibrium would induce overpayment compared to the 7.5 + epsilon/2 equilibrium. This seems like a flaw that requires more justification as to why the proposed premium rule wouldn’t induce consistent overpayment from users, or wouldn’t naturally degrade back to the vanilla 1559 setting.

If instead basefee is burned, 0.625 premium isn’t quite enough to cover the miner marginal cost (assuming that cost is 1 Gwei). Note that the following strategy is actually an equilibrium in that case: users in the top quartile all declare max_fee = 8.5 such that basefee = 6.5 and users pay basefee + premium = 6.5 + 1 = 7.5. Users who are not in the top quartile don’t have an incentive to bid 8.5, since by definition they would pay more than their willingness to pay (which is lower than 7.5), but you still have a set of users for whom misrepresenting their willingness to pay is the correct strategy (in fact, users in the interval [7.5, 8.5] declare themselves willing to pay *above* their true willingness to pay!)

Sorry that was a bit verbose, but wanted to write it out also to convince myself ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) hopefully this sheds some light on expected behaviour.

---

**mtefagh** (2021-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> What does it mean to set the gas premium?

The user only sets the fee cap but as the median premium is computed based on (FeeCap - BaseFee)/2, they are indirectly setting the gas premium too. Moreover, the fee cap also represents the maximum total (base fee + gas premium) that the transaction sender would be willing to pay.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Are you saying there is no impact compared to now (i.e. no fees will get burnt) or no impact compared to EIP-1559?

We are open to both as we don’t want the gas-burning issue to be the main focus of this EIP. This sentence can also be changed. However, we can keep this sentence, and then the miner should also burn x% of gas where x is the average ratio of the base fee to the total fee. If you are interested to know what’s the point of it, have a look at the discussion [here](https://ethereum-magicians.org/t/why-should-we-make-miners-prefer-the-premium-and-hate-the-base-fee/5866). But again, not the main focus here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> How do you expect to know in advance which transactions are included in a block? You basically need to build the block before you execute the transactions, right? If so, how do you keep that efficient for miners? How can they know in advance how many transactions can be included?

The block producer can sort the transaction by the fee cap in the decreasing order and then use a greedy algorithm to include as many transactions as possible. However, to do it much more efficiently by exploiting the fact that the median is so robust, they can also estimate the median from a couple of transactions first. Then include all the transactions where the fee cap is more than this estimated median and start to adjust it by including or excluding transactions from there.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Walking through the flow of how a miner picks txns from the pool, and build a block, would be valuable.

The greedy algorithm is that you just keep adding transactions in the decreasing order of fee cap as long as the median of (FeeCap - BaseFee)/2 is less than the minimum fee cap. However, we can also add the details of the more efficient version in a future write-up if there is enough interest.

---

**mtefagh** (2021-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> Point 1. I think is fairly uncontroversial, there’s some evidence that the current multiplicative update rule isn’t optimal, though it’s unclear without data in which ways and what the best fix would be.

Of course, it should be discussed. However, just as a shortcut, if people can agree with me that [this](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/367) is the same problem, then we can just borrow the final solution from the economic literature. To me, it seems just like the exact same problem.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> This seems incorrect. It’s been shown that unless the effective demand is higher than the block limit

Sure, EIP-1559 is an improvement in this respect. However, we are talking about an additional improvement for the congestion times.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> In the “vanilla” 1559 design, BASE_FEE would settle around 6.5, assuming all bidders pay a gas premium equal to 1

I don’t agree with this part as I have shown that there also exist oscillatory equilibriums and I believe that mildly strategic users will converge to those, however, let’s skip this part as I have discussed this before.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> Assume basefee is 7.5, then premiums are distributed uniformly in the interval [0, 1.25] and the median premium is 0.625,

At equilibrium, the total fee will sum up to 7.5. Hence, the base fee will be 6.66666 and premiums are uniformly distributed in the interval [0, 1.66666] and the median premium is 0.833333.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> In this stationary example, if basefee was lower than 7.5, there would be potentially more users included than the target allows for, and vice versa for basefee higher than 7.5, so 7.5 is indeed the value basefee would tend to.

No, it is not true. The fee cap is on base fee + gas premium. I think the rest of this paragraph depends on this point.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> If instead basefee is burned, 0.625 premium isn’t quite enough to cover the miner marginal cost (assuming that cost is 1 Gwei).

If the miner’s marginal cost is 1 Gwei, the block producer won’t include transactions unless the base fee is lower than 6. This can’t converge to equilibrium until the transaction fees are raised from the uniform distribution over [0,10] to uniform over [0,12]. At this price, the equilibrium is reached by the base fee equal to 8 and the median premium equal to 1.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> users in the top quartile all declare max_fee = 8.5 such that basefee = 6.5 and users pay basefee + premium = 6.5 + 1 = 7.5.

This will only work under complete information about other transactions’ fees otherwise people in the interval [7.5,8.5] are risking loss. If I ignore the numerical errors that I have mentioned above, I think I get your overall overpayment point. If I am correct, you are trying to say that in any generalization of the second-price auction, if the bids are not sealed, people can cheat by overpayment. Yes, that’s true that the strategy of overbidding is dominated by bidding truthfully in the sealed-bid setting. There are several proofs for it given in game theory. But notice that even if you have some rough estimate about other fees from the mempool, manipulating the median is way harder than the second price and, as in your example, a significant portion of users should simultaneously attempt to manipulate it knowing almost everyone’s else bid.

---

**hexzorro** (2021-04-05):

I want to add something. Even if now the blocks are very small and is not important, lets an average of 200 Txs per block, if we have very big blocks the weighted median can be implemented in a efficient way so if the miner decides to drastically change a block its building before mining (for example to include a newly arbitrage found), the median can be implemented so removing and adding Txs to the structure is only complexity `log(#BlockTxs)` with `#BlockTxs` the current number of Txs in the block. (CC: [@mtefagh mtefagh](https://ethereum-magicians.org/u/mtefagh))

---

**hexzorro** (2021-04-05):

[@barnabe](/u/barnabe) Thanks for your detailed response! [@mtefagh](/u/mtefagh) responded earlier but I just want to add a few points regarding the *irrational* behaviour of actors on the *sender side* that helps understand the improvements of EIP-3146 over EIP-1559:

- The volatility of final gas prices is induced by a few high-price outliers. For example, these can be DeFi arbitrageurs that are very eager to include their transactions ASAP. This behavior can be rational from their arbitrageur short-term POV but it might damage their gas fee costs in the long term with current Fee Market, along with the costs of all regular users.
- The gas stations and gas price estimations many times or all the use average calculations that include the outliers showing a lot of volatility to the other regular tx sender users. These calculations are not robust to outliers.
- Regular users sending transactions engage in bidding wars after seeing crazy volatility and wanting to include their transations not ASAP but soon enough their UX can be smooth enough and not damaged. For example, they see volatility on gas price estimators jumping from 150Gwei
to recommending a price of 200Gwei so they decide to bid for 210 or 220GWei to have bigger chances of getting included in the next few blocks.

The Median Gas Premium will send a more robust signal to gas estimators and regular senders, so the sender side does not panic and engage in permanent bidding wars that are, most of the time, irrational and unnecessary. In a few cases, bidding wars are going to still be rational and expected.

---

**barnabe** (2021-04-05):

Thanks [@mtefagh](/u/mtefagh), this is super helpful!

> I don’t agree with this part as I have shown that there also exist oscillatory equilibriums and I believe that mildly strategic users will converge to those, however, let’s skip this part as I have discussed this before.

You could assume “vanilla” 1559 uses the additive basefee update rule and not the multiplicative update to rule out the oscillatory equilibria, and I think it would be correct that the basefee + 1 gwei strategy is an equilibrium in this idealised setting.

> Sure, EIP-1559 is an improvement in this respect. However, we are talking about an additional improvement for the congestion times.

This is where I fail to get an intuitive idea of the tradeoffs. Again, let’s assume we’ve fixed the basefee instability with a different update rule. In my mind I think “there is no free lunch”, so how does the median premium can give a strict improvement on congestion times? (or rather, if it does, at what cost?) Perhaps I am missing something here.

> At equilibrium, the total fee will sum up to 7.5. Hence, the base fee will be 6.66666 and premiums are uniformly distributed in the interval [0, 1.66666] and the median premium is 0.833333.

Agreed! I made a mistake there. So at the equilibrium of truth-telling (setting value = max fee) basefee does equilibrate at 6.6666 and the median premium at 0.83333. But I still believe this other equilibrium exists when basefee is given to the miner, where all agents with value above 7.5 set max fee = 7.5 + epsilon. Interestingly both equilibria have users pay 7.5, so I guess no overpayment. This is interesting!

> This can’t converge to equilibrium until the transaction fees are raised from the uniform distribution over [0,10] to uniform over [0,12]

I’ve assumed the values are between 0 and 10, so I am unclear how the transaction fees can go to 12. I do believe setting max_fee = 8.5 for all users with value above 7.5 is an equilibrium, and that in this equilibrium basefee would settle at 6.5. Once again, that equilibrium has the same payoff profile as the equivalent equilibrium in the “vanilla” 1559 design, so no overpayment there either.

> This will only work under complete information about other transactions’ fees otherwise people in the interval [7.5,8.5] are risking loss

I do assume complete information since I am interested in equilibrium behaviour first. I realise that it’s idealised, but it’s also an important benchmark that I think makes it easier to unroll the implications when assumptions are relaxed.

I was concerned about overpayment since it seemed the rule would have you bid “more than necessary”, but not in the sense of strategic overpayment (as in ex post irrationality where you bid non-truthfully and risk a negative payoff later on). For instance, why not use `(tx.max_fee - BASE_FEE) / 4` rather than `(tx.max_fee - BASE_FEE) / 2` ? would the former induce less overpayment than the latter? This is what I am unclear on. Now I am more convinced that at equilibrium, either taking a quarter or half of the max_fee minus basefee difference would yield the same payoffs as 1559, since basefee would “pick up the slack”. In a sense, that’s a good sanity check. So I guess I am still looking for evidence that it does improve upon what 1559 offers (possibly modulo the update rule change to root out the bad equilibria you uncovered, but which I don’t think the median premium rule avoids on its own). I need to spend more time thinking about it! Might bug you with more questions ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**mtefagh** (2021-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> You could assume “vanilla” 1559 uses the additive basefee update rule and not the multiplicative update to rule out the oscillatory equilibria, and I think it would be correct that the basefee + 1 gwei strategy is an equilibrium in this idealised setting.

True ![:+1:t2:](https://ethereum-magicians.org/images/emoji/twitter/+1/2.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> This is where I fail to get an intuitive idea of the tradeoffs. Again, let’s assume we’ve fixed the basefee instability with a different update rule. In my mind I think “there is no free lunch”, so how does the median premium can give a strict improvement on congestion times? (or rather, if it does, at what cost?) Perhaps I am missing something here.

If you prefer to think of it in the context of trade-offs, let’s say this can be the sweet spot in the trade-off between the first price auction and the second price auction. [@hexzorro](/u/hexzorro) mentioned a couple of points in his previous response. They are instances of the well-known problems with first-price auctions. Second-price auctions have their own problems like the overpayment scenario you just described. How about thinking about this median price as something in the middle?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> But I still believe this other equilibrium exists when basefee is given to the miner, where all agents with value above 7.5 set max fee = 7.5 + epsilon. Interestingly both equilibria have users pay 7.5, so I guess no overpayment. This is interesting!

True! But again, you are assuming complete information for the case where users are not bidding truthfully. And yes, the final base fee + gas premium is the same in either case. A sidenote in here: the same example shows that premium is an increasing function of volatility which is a good sanity check. Note how premium will be reduced if the fee distribution is concentrated.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> I’ve assumed the values are between 0 and 10, so I am unclear how the transaction fees can go to 12.

The point is that as I said before, “the block producer won’t include transactions unless the base fee is lower than 6.” Therefore, if the base fee is lower than this, a more than target full block will be mined and the base fee increases, but if the base fee is higher than this, the block will be empty and as a result, we won’t ever reach an equilibrium. The problem is that the uniform [0,10] distribution is too low. An equilibrium is reachable only if we consider the uniform [0,x] distribution for x >= 12. Of course, this is because in your example miner’s marginal cost is comparable to the base fee where in practice it will be smaller an order of magnitude.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> Once again, that equilibrium has the same payoff profile as the equivalent equilibrium in the “vanilla” 1559 design, so no overpayment there either.

True, because again we are studying the equilibrium and not congestion.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> For instance, why not use (tx.max_fee - BASE_FEE) / 4 rather than (tx.max_fee - BASE_FEE) / 2 ? would the former induce less overpayment than the latter? This is what I am unclear on.

Now that I have learned that you like thinking about trade-offs ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12), let me put it like this. Consider `(tx.max_fee - BASE_FEE) / alpha`. As alpha goes to one, we will include only the highest paying transaction in the block. As alpha goes to infinity, we will include any transaction paying more than the base fee. The higher the alpha, the less the premium the miner receives from every single transaction but there are more of them. The lower the alpha, the higher the premium the miner receives from every single transaction but there are fewer of them.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> So I guess I am still looking for evidence that it does improve upon what 1559 offers (possibly modulo the update rule change to root out the bad equilibria you uncovered, but which I don’t think the median premium rule avoids on its own).

During times of network congestion, we temporarily revert to first-price auctions which we don’t like. This replaces them with something like second-price auctions but much more robust.

---

**mdalembert** (2021-04-05):

Hi [@barnabe](/u/barnabe), nice to hear from you!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> You could assume “vanilla” 1559 uses the additive basefee update rule and not the multiplicative update to rule out the oscillatory equilibria,

Why do you assume that switching EIP-1559 to the additive base fee update rule will rule out oscillatory equilibria?  The path-dependence of its current multiplicative update rule is at the root of *some* of the negative consequences of oscillatory equilibria (namely the associated state growth and downwards base fee drift), but it is not the ultimate cause of its oscillatory behavior.  Switching to an additive update rule will roughly give us the logarithm of the preexisting oscillations while making them slightly less harmful thanks to its path-independence, but they can still be expected to be present and have a comparable effect on usability giving users an incentive to bid below their marginal utility in order to avoid overpayment.

---

**hexzorro** (2021-04-13):

[@barnabe](/u/barnabe) [@mtefagh](/u/mtefagh) Made this diagram to compare UI for different Market Fee proposals:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/89a4db2535a8cab6c782360d6ddda500b6ba53cb_2_690x388.png)image960×540 87.8 KB](https://ethereum-magicians.org/uploads/default/89a4db2535a8cab6c782360d6ddda500b6ba53cb)

Hope it helps make out point in the future.

---

**barnabe** (2021-04-14):

Thanks! Another question, what happens if your transaction cannot cover the determined `GASPRICE`? For instance, say we have three transactions in a block and basefee is 10.

| Fee cap | Premium | Payment |
| --- | --- | --- |
| 20 | 5 | 12.5 |
| 15 | 2.5 | 12.5 |
| 12 | 1 | 12.5? |

Since the median of premiums is 2.5 (assuming we don’t do the 95% weighted median, but simple median), we should have `GASPRICE = BASEFEE + median = 12.5`

What happens to the third transaction? They cannot cover 12.5, but afaict the eip as written doesn’t mention that case. Is it that the user pays `min(FEECAP, BASEFEE + GASPRICE)`, so 12?

---

**mtefagh** (2021-04-14):

No, at the end of the day, everyone pays the exact same price which means that the third transaction will be excluded and the other ones will pay 13.75 which will be the base fee plus the median of the first two transactions. Note that, here the median changes a lot when excluding one single transaction unlike in real-world simulations in which it doesn’t change at all because of the high number of transactions.

---

**barnabe** (2021-04-14):

Ok but since you assume that under your mechanism users would behave truthfully (declaring their own value as maxfee) what you noticed in the simulation may not hold anymore under the mechanism.

It’s also true that sometimes eip1559 rules out transactions that could legitimately be included (e.g., when basefee is too high but decreasing, so there is block space but the constraint that maxfee > basefee isn’t met), and this seems to be even more the case here: a user declares a maxfee that could cover the basefee and the miner opportunity cost and yet cannot be included.

Curious also to hear your thoughts on miners moving the median by including their own transactions, possibly rejecting valid transactions in the process. By including own transactions with high enough maxfee, it seems possible best strategies for the miner exist where they charge a monopolistic price, even if basefee is burned. It’s mentioned in the EIP as a passing comment but I suspect more analysis would be required here

---

**mtefagh** (2021-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> Ok but since you assume that under your mechanism users would behave truthfully (declaring their own value as maxfee) what you noticed in the simulation may not hold anymore under the mechanism.

I am only using the estimation that it seems like the transaction fees obey a power law, i.e., there are very few transactions paying a lot more than average and many transactions paying in the same range. This observed exponential distribution of fees is consistent with the well-known power-law behaviors in many other financial phenomena.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> It’s also true that sometimes eip1559 rules out transactions that could legitimately be included (e.g., when basefee is too high but decreasing, so there is block space but the constraint that maxfee > basefee isn’t met), and this seems to be even more the case here: a user declares a maxfee that could cover the basefee and the miner opportunity cost and yet cannot be included.

In this example, base fee and premium are of the same order of magnitude and that is the root of the problem. In reality, the premium is just a small fraction of the base fee. Therefore, with high probability, whether your transaction is included or not only depends on the ratio of fee cap and base fee and premium almost doesn’t change this ratio at all.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> Curious also to hear your thoughts on miners moving the median by including their own transactions, possibly rejecting valid transactions in the process. By including own transactions with high enough maxfee, it seems possible best strategies for the miner exist where they charge a monopolistic price, even if basefee is burned. It’s mentioned in the EIP as a passing comment but I suspect more analysis would be required here

This is the same well-known attack for the second-price auctions. However, note that changing the median for a wide range of well-known distributions requires changing not a constant number of transactions (like the case there) but instead a fraction of them. For example, if you want to increase the median by x% you need to forge y% of transactions where x and y are of the same order of magnitude for a wide variety of distributions (including the exponential distribution that I mentioned earlier or Gaussian or …). This means that you should pay the base fee for y% of transactions in order to increase the premium by x% and because the base fee is an order of magnitude larger, it doesn’t make sense for a wide range of x and y.

---

**barnabe** (2021-04-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mtefagh/48/1890_2.png) mtefagh:

> In this example, base fee and premium are of the same order of magnitude and that is the root of the problem. In reality, the premium is just a small fraction of the base fee.

That would hold for basefee = 110 and max fees 120, 115, 112?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mtefagh/48/1890_2.png) mtefagh:

> This means that you should pay the base fee for y% of transactions in order to increase the premium by x% and because the base fee is an order of magnitude larger, it doesn’t make sense for a wide range of x and y.

This is what would merit closer inspection, because I don’t think it’s necessarily true for “a wide range”. In fact, the more power-law-ish the fee max distribution is the more I suspect this is an issue, since it means there is more premium to extract at the tail. In EIP-1559 at least this attack surface doesn’t exist.


*(5 more replies not shown)*
