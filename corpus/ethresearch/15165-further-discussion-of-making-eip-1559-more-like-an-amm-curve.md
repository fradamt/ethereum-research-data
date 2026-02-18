---
source: ethresearch
topic_id: 15165
title: Further discussion of Making EIP 1559 more like an AMM curve
author: MaxResnick
date: "2023-03-28"
category: Economics
tags: []
url: https://ethresear.ch/t/further-discussion-of-making-eip-1559-more-like-an-amm-curve/15165
views: 3167
likes: 8
posts_count: 10
---

# Further discussion of Making EIP 1559 more like an AMM curve

I’m making this post because there was considerable discussion on a Twitter thread, but this seemed like a better venue for continuing the discussion. [Twitter thread](https://twitter.com/MaxResnick1/status/1639826752280350721)

Let me start by outlining the benefits of EIP 1559 over the old first price system as I see them:

1. EIP1559 allows for dynamic block size which may increase welfare by increasing capacity when demand is higher and lowering it when demand is lower
2. EIP1559 gives a clear bidding strategy (base fee) in each block.

Now let me outline the disadvantages as I see them (some of these things EIP1559 does better than the old model but still not perfectly):

1. The size of the block is path dependent in 1559, see ethresear.ch discussion 1.
2. The market clearing price is path dependent meaning the allocation may be inefficient in the current slot.
3. The cost to the proposer of censoring transactions is lower under 1559 because the base fee is burned.

Let me reintroduce the Bonding curve mechanism,  in terms of how I would implement it.

Instead of setting block size based on an updating rule, the block size is determined by the proposer. The proposer pays for additional block space based on a bonding curve `F`. The bonding curve is initialized such that its marginal `f` is the marginal cost to the network of having a larger block and the total amount of additional block space purchasable this way is capped. Proceeds from this bonding curve are redistributed (either through burning if it is determined that the cost of larger blocks is borne by the broader ETH community, or to the validator set if it is determined that they primarily bear the cost of larger blocks).

There are no base fees in my ideal model which roughly corresponds to [@vbuterin](/u/vbuterin) 1. in the second list in his post according to my understanding. Transactions simply include miner tips so the result is essentially a first price auction for block space, with the caveat that the proposer can purchase additional block space from the bonding curve.

This achieves the benefits of EIP1559 that I discussed above:

1. This obviously allows the block size to increase under load, since the proposer will purchase more block space when there are many high-tip transactions in the pool.
2. There is a clear bidding strategy determined by the marginal f(s) where s is the amount of block space purchased in the last block.

Now I will discuss how this design improves on the negatives:

1. & 2. Since the proposer chooses block size in each block, based on the transactions it has access to, the block size is not path dependent. In other words, if demand for block space spikes dramatically, from slot to slot, then this mechanism allows block size to immediately rise to accommodate it. Similarly, if demand falls sharply, the result is not an empty block. This is discussed more formally in the posts referenced above.
2. The cost of censoring under 1559 is the miner tip (which does not include the base fee). think of this as total_fee - base_fee and this is true regardless of how many transactions are censored. In the AMM model the cost of censoring for the first transaction is total_fee - f(s) which is similar if you consider that under static load, base_fee eventually converges to f(s); however, when censoring more than one transaction, the marginal cost of censoring is total_fee - f(s-n) where n is the number of transactions you censor, thus increasing censorship resistance when censoring a large number of transactions.

## Replies

**barnabe** (2023-03-28):

Thanks for writing it up [@MaxResnick](/u/maxresnick) !

What I am missing is how you achieve the gas target, since you don’t seem to set one. I’ll give my understanding to see if I get this right.

The marginal cost to the network is very low compared to the congestion cost that users pay to access scarce resources (see [this post](https://barnabe.substack.com/p/understanding-fees-in-eip1559), and also [this note](https://notes.ethereum.org/@barnabe/rk5ue1WF_) for an estimation of the marginal network cost based on PoW data). Let’s fix it in the following to 1 Gwei per gas unit.

If you set your cap to X gas and there is a demand Y < X gas willing to pay 1 Gwei, then the block producer can purchase Y units of gas for Y Gwei and there is a simple bidding strategy for users. If there is a demand Y > X willing to pay at least 1 Gwei, then the block producer cannot include all because of the cap and the block is full. Users must then compete via the tip. So to me it seems that the bidding strategy is clear only in the case where the demand is below the cap, which seems unlikely to hold very often at a reserve price equal to the marginal network cost (I believe at 1 Gwei gas price there would be much more than 15 million units of gas demanded).

If “the marginal cost to the network” is defined as the clearing price, then I fail to see how the bonding curve can target the 15 million gas average without essentially reproducing Vitalik’s proposal which prices the excess demand along the bonding curve.

---

**MaxResnick** (2023-03-28):

What is the reason for the gas target? I understand that you could get something that hits the gas target by adjusting the curve dynamically as in [@vbuterin](/u/vbuterin)’s post the reason I say the marginal cost to the network is that it immediately gives efficiency. Not sure why we would want smaller blocks than the efficient size.

Also doesn’t 1559 fail to produce a bidding strategy when the block size is at maximum? Or maybe the base fee continues to increase at that point, I’m not sure. But this could certainly be tacked on to my solution.

---

**barnabe** (2023-03-28):

The gas target is there because there are both burst constraints (we don’t want one-shot block processing to take too long) which a block limit address, but also long term constraints (eg we want the state size to grow by at most X GB per year). This is an important design constraint, though it can be made more efficient with multi-dimensional eip-1559, by applying finer burst and long term constraints to each resource type. State size has a long term cost on the network while execution does not for instance. Efficiency is obtained under constraints, so you are not making smaller blocks on purpose, you are making them as large as possible while respecting the long term targets and burst constraints. You can get more efficiency by having base fee track the clearing price more closely, eg by messing with the update rate, but then you have tradeoffs in terms of stability and bidding UX (we have a couple of papers on the topic).

And yes when the block is full there is no user incentive compatible bidding strategy (you want to revert to competition over the tip). But as the base fee is updated dynamically, it increases for the next block when the previous one is full, so it seems like you would be in the first price auction situation much more often in your proposal than in eip-1559, as base fee eventually adjusts. I suspect that if you add this to your solution it would look a lot more like eip-1559 than what you currently proposed, but it should be written up more properly to assess that.

---

**MaxResnick** (2023-03-30):

Hmm, this makes sense, I do wonder if it is more natural to treat the burst constraint as a threshold i.e. block size is less than some threshold rather than a more complicated one, then we can come up with a nice estimate for what the state growth cost is and use that to define the curve.

Even with a standard first price, it seems like there is a clear bidding strategy bc you can just take the lowest gas price that made it into the block.

My guess is that if we formalized what good UX meant we would see that the base fee doesn’t do much better than a standard first-price auction.

---

**llllvvuu** (2023-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> it seems like there is a clear bidding strategy bc you can just take the lowest gas price that made it into the block.

That is what wallets used to do, but people were missing more often. It does seem like pricing gas off of historical (or fancier stuff ppl used to do like Poisson regression) is theoretically and empirically slightly more likely to miss than pricing at 2x of historical (which would be a waste of money in first-price).

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> if we formalized what good UX

The usual model is waiting time (e.g. in [this work](https://arxiv.org/pdf/2201.05574.pdf))

---

**barnabe** (2023-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/llllvvuu/48/9687_2.png) llllvvuu:

> waiting time

Related to this, the distance between the clearing price and the true market price could also be a metric of good UX. e.g., if the market price is 1, but the clearing price keeps oscillating between 0 and 2, I would call that bad UX. We investigated this metric in simulations [here](https://ethereum.github.io/abm1559/notebooks/transition1559.html).

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> I do wonder if it is more natural to treat the burst constraint as a threshold i.e. block size is less than some threshold rather than a more complicated one, then we can come up with a nice estimate for what the state growth cost is and use that to define the curve.

Separating burst and running constraints does allow for such optimisations, e.g., you can price state growth much more precisely along some network harm curve vs burst resources which are either no problem load-wise until they cross a threshold and become a problem. The post by [@vbuterin](/u/vbuterin) on [Multi-dimensional 1559](https://ethresear.ch/t/multidimensional-eip-1559/11651) goes over this.

---

**bsanchez1998** (2023-04-07):

Hey Max, this is super interesting. I think your proposal for using a bonding curve makes sense and addresses some of the issues with EIP 1559. However, I would be concerned about the proposer determining block size. If the proposer is allowed to control the block size, there could be potential for centralization or manipulation, as larger players could influence block sizes with  their advantage.

Mitigating this risk, what if we introduced a weighted system that takes in to account multiple factors, like tx fees, network congestion, and historical block size to determine the optimal block size? That way we can still have a dynamic block size adapting to network demand while reducing the risk of manipulation, maintaining the benefits of your proposed mechanism while minimizing centralization concerns.

I’m interested to hear your thoughts on this idea and whether or not it is a viable addition to your proposal.

---

**meridian** (2023-04-11):

> in certain pathological scenarios, decomposable update rules can oscillate between two base fees rather than converge to a market-clearing base fee, even during a period of stable demand.
> – Remark 8.16 (Oscillatory Behavior of Decomposable Update Rules) RoughGarden20

---

**MaxResnick** (2023-04-14):

what attack are you worried about? Its a reasonable question I just cant think of anything particularly sinister off the top of my head.

