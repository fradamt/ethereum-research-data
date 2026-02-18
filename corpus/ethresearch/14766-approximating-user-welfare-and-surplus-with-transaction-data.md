---
source: ethresearch
topic_id: 14766
title: Approximating User Welfare and Surplus with Transaction Data
author: dcrapis
date: "2023-02-06"
category: Economics
tags: []
url: https://ethresear.ch/t/approximating-user-welfare-and-surplus-with-transaction-data/14766
views: 2001
likes: 8
posts_count: 5
---

# Approximating User Welfare and Surplus with Transaction Data

*Thanks to Ciamac Moallemi, Barnabé Monnot, and Aditya Asgaonkar for discussions that led to this idea.*

When trying to evaluate the performance of a network or platform one of the simplest metrics that come to mind is *throughput*. For Ethereum this would be the amount of transactions processed. However, this is a raw metric that does not take into account the value of processed transactions. This post describes a method to estimate/approximate two more refined metrics of network performance: the amount of value generated (*welfare*) and the amount of value gained by users (*surplus*). These can be used in many ways, for example **evaluating a policy change** (like the introduction of EIP-1559) or **estimating how much value different apps in the ecosystem are generating and capturing**.

A proper estimation of user welfare and surplus requires experimental data that we don’t have in general. However, we can construct estimators using only observational data. Note that, based on reasonable assumptions, these approximations are most likely underestimating the actual welfare and surplus generated.

Given a set of blockchain transactions, we can use transaction data to specify two relevant metrics `value` and `cost`. For type 2 transactions we have

`value = max_fee * gas_used`

`cost = min(base_fee + max_priority_fee, max_fee) * gas_used`

The cost is exact, the value is an approximation which underestimates the true value to the user. To see this note that users will never set a `max_fee` higher than their private valuation since this is the expression of their willingness to pay. Also, Tim Roughgarden’s analysis of EIP-1559 proves that is typically user incentive compatible to set a `max_fee` that is equal or smaller than their private valuation.

There is still a non-trivial amount of type 0 legacy transactions for which the users set only the `gas_price`. In this case we estimate `cost = gas_price * gas_used` which is again exact and we estimate the value using the `max_fee` for similar type 2 transactions. In particular, *for each type 0 transaction we define a set of matched type 2 transactions* (matched on time and other transaction features) and then we estimate the `max_fee_0` for the type 0 transaction as the *median over the matched set `max_fee` params* and then `value = max_fee_0 * gas_used`.

Now for each transaction we have a measure of user `welfare = value` and of user `surplus = value - cost` and we can aggregate at any level we please.

**Examples**

Considering all Ethereum transactions from January 1st 2023 we can see that the network generated user welfare of 2,754 ETH and surplus of 943 ETH. Users paid for transactions 35% less than they were valuing them and gained in aggregate almost 1K ETH of economic value!

Similarly we can look at sum over all blocks in each hour of day and see that the network was consistently generating about 120 ETH of welfare and 40 ETH of surplus per hour. [See first chart below.]

As another example of things we can measure, we can look at the nature of transactions. Here we look at simple token transfers versus other types (but one measure specific contracts, apps and other parts of the ETHconomy). Here we see that the majority of value is more complex transactions, but while these are relatively expensive to users (surplus is only 30% of value on average) token transfers are quite cheap with user surplus ratio up to 50%. [See second chart below.]

[![two charts](https://ethresear.ch/uploads/default/optimized/2X/0/03b97cc32efa1f0c48e278ee1d8fe8026efb06f1_2_343x500.png)two charts460×670 35 KB](https://ethresear.ch/uploads/default/03b97cc32efa1f0c48e278ee1d8fe8026efb06f1)

## Replies

**llllvvuu** (2023-02-07):

This is an interesting idea. I would note:

1. The connection to policy change is not super clear because if the first-price auction had more bid-shading, then it had more hidden welfare. Although discontinuity analyses are not perfect, a discontinuity analysis on mean gas paid (where we assume that welfare is not discontinuous and therefore that surplus is discontinuous according to discontinuity in cost) is still probably a more accurate way to compare the surplus of policies.
2. Re: value = max_fee * gas_used, we have to consider winner’s curse, e.g. how many people are now regretting spending so much on gas to buy the top on tokens during the raging bull market. Incentive-compatibility analyses in mechanism design are almost always done in private-value settings with perfect information.
3. In my experience, “welfare” typically refers to surplus, but I’ve conformed to your definition in this response.

---

**dcrapis** (2023-02-08):

Thanks for the comments.

To the first point in 1., not considering bid shading is one of the reasons I called this method an approximation. To the other point, yes in the particular case of EIP-1559 a discontinuity design like the one you described may be more accurate. But actually I realized that case is a bad example for what I was trying to convey: I wanted to suggest that comparing surplus/welfare can be useful in general, whenever we make a system change that does not involve changing the type of mechanism entirely like we did (e.g., changing the learning rate of the update rule or making the rule multidimensional). In that case even if the surplus estimate is biased for the legacy transactions, if you are willing to assume the same bias pre- and post-change, then the delta surplus will be approximately correct. There are other nuances and could be interesting to do a proper estimation exercise to assess the goodness of this approximation, one idea is to use price discontinuity similar to https://www.nber.org/system/files/working_papers/w22627/w22627.pdf

To point 2., there are some transactions for which it is fine to assume private value (e.g., USDC transfers). For the ones related to trading it is more of a case of interdependent values for which analysis is more challenging. This actually shows up in many places in blockchain-related auctions and we need to advance the research on this.

---

**meridian** (2023-02-08):

Legacy transaction usage was recently retired by Wintermute. They used it intentionally as they saw the efficiency in gas usage was not sufficient compared to the risk of mispricing their transaction. Their transaction submissions include a deadline of n+1 blocks (literally no more than 2 blocks from tx generated).

Here is a sample of our internal grafana metrics that tracks dollar value of txs submitted via [SecureRpc.com](http://SecureRpc.com) endpoint. If you want access to this dataset can be arranged .

[![image](https://ethresear.ch/uploads/default/optimized/2X/1/1647fdb51063675ac7c4ac913ec90097aeb783a2_2_230x500.jpeg)image1290×2796 285 KB](https://ethresear.ch/uploads/default/1647fdb51063675ac7c4ac913ec90097aeb783a2)

---

**dcrapis** (2023-02-09):

This is interesting. By risk of mispricing you mean, for example, risk of having to pay higher base fee if tx gets included in later block when base fee is going up? And is limiting inclusion to current or next block the main way to mitigate that risk now?

