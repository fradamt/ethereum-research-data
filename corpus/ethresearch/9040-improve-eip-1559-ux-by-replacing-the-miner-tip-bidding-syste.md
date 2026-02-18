---
source: ethresearch
topic_id: 9040
title: Improve EIP-1559 UX by replacing the miner tip bidding system
author: kristofgazso
date: "2021-03-29"
category: Economics
tags: [eip-1559]
url: https://ethresear.ch/t/improve-eip-1559-ux-by-replacing-the-miner-tip-bidding-system/9040
views: 2246
likes: 3
posts_count: 7
---

# Improve EIP-1559 UX by replacing the miner tip bidding system

## What is the Problem?

If the `BASE_FEE` that is included in the transaction is burned, then the miners would not have any incentive to include transactions in mined blocks. This would clearly be an existential problem for the Ethereum blockchain, however the creators of EIP-1559 have thought of this and therefore they have implemented a miner’s tip system, where users can submit tips to miners alongside the `BASE_FEE` in order to get their transaction included.

This miner’s fee is the problem. **If the point of EIP-1559 was to improve UX, then having one fee-bidding system replace another fee-bidding system is underwhelming**. Users would still have to bid to get their transactions included even alongside the `BASE_FEE`, so from a UX standpoint, this EIP is less effective than it could be.

## The Proposed Solution

We should get rid of the miner’s fee bidding system entirely. Instead of having to include tips alongside the `BASE_FEE`, a `MINER_TIP` should, similarly to the `BASE_FEE`, be calculated based on supply and demand mechanics once per block. I would propose that this `MINER_TIP` be a value that is a percentage of the `BASE_FEE`, with the percentage being a function of the total hashing power of the network under PoW and, or the total ETH staked after PoS.

I propose that this percentage, similarly to ETH staking rewards in ETH 2.0, could be `MINER_TIP = MINER_TIP_PERCENTAGE*BASE_FEE`, where `MINER_TIP_PERCENTAGE = min(1, a/sqrt(b*TOTAL_TERA_HASHING_POWER))`. `a` and `b` would be some constants.

The following graph represents how `MINER_TIP_PERCENTAGE` would look for different TH/s of hashing power using the previous equation with `a = b = 1`.

[![](https://ethresear.ch/uploads/default/optimized/2X/3/394218b51e34a366f591507d221e4a570a970947_2_690x445.png)2334×1506 236 KB](https://ethresear.ch/uploads/default/394218b51e34a366f591507d221e4a570a970947)

The entire equation could be changed if need.

For ease of explanation, I would define `TOTAL_TX_COST` just in this post

`TOTAL_TX_COST = BASE_FEE + MINER_TIP`

If there are more transactions, `BASE_FEE` would automatically increase until blocks are only 50% filled just as before. Given that `MINER_TIP` is a percentage of `BASE_FEE` that is constant in the short term (i.e. hashing power stays constant), it would always move alongside `BASE_FEE` in the short term. Vice versa for when the number of transactions temporarily decrease. Therefore the `TOTAL_TX_COST` stabilizes in the short run.

In the long-run, the total hashing power can also change. Starting from an equilibrium, if the `MINER_TIP` decreases, miners/stakers will earn less fees per block, some miners/stakers will quit the network and total hashing power will decrease. Consequently, the percentage of the `TOTAL_TX_COST` that consists of the `MINER_TIP` increases, resulting in higher fees going to miners/stakers until the hashing power of network stabilizes. Therefore the `TOTAL_TX_COST` stabilizes in the long run as well.

Counterpoint:

**But under EIP-1559, the miner-tip will usually be stable at around, say, 1 gwei, and only `BASE_FEE` will change**

For new users, I believe the added complexity of paying a tip in addition to paying a base transaction fee is unnecessary. It would be a lot simpler from a UX perspective if they only had to worry about one number.

## Conclusion

The advantages:

- Anyone transacting would have to pay TOTAL_TX_COST, which would be known beforehand, completely eliminating the need for a bidding system.
- Assuming an effective function to determine MINER_TIP, Miners/stakers would be reliably compensated for their work and would always have a direct incentive to include transactions in blocks.
- The deflationary policy of Ethereum (a likely outcome of EIP-1559) will not change.

The disadvantages:

- If the MINER_TIP function is not appropriate, it could lead to either the overpayment of miners or, if the tip is too low, a network security risk due to low hashing power/ETH staking.
- If the network reaches maximum gas capacity, we will have no way of prioritizing transactions in the short-term by bidding miner tips up unlike in the current EIP-1559 proposal, and we will have to rely on the adjustment of BASE_FEE. Perhaps a modification to my proposed system can alleviate this.

### Contact

If anyone is interested in drafting an EIP proposal with me, please reach out to my EthResearch account or my Twitter [@kristofgazso](/u/kristofgazso)

## Replies

**mtefagh** (2021-03-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/kristofgazso/48/5717_2.png) kristofgazso:

> If the network reaches maximum gas capacity, we will have no way of prioritizing transactions in the short-term by bidding miner tips up unlike in the current EIP-1559 proposal, and we will have to rely on the adjustment of BASE_FEE. Perhaps a modification to my proposed system can alleviate this.

One possible solution to this problem is to remove the “maximum gas capacity” and make it unlimited. However, it is absolutely necessary to include slippage (by simply replacing excess gas usage of the previous block with the excess gas usage of the current block) before this can be done, otherwise one can simply buy tons of gas at a fixed price. See [here](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/363?u=mtefagh) for more details.

---

**kristofgazso** (2021-03-29):

Thank you for the suggestion! Forgive my ignorance, but even after reading through the link, I am a bit confused about how it works and how that could solve the problem. Could you give a concrete example of how ‘replacing excess gas usage of the previous block with the excess gas usage of the current block’ would work?

---

**mtefagh** (2021-03-30):

Sure, no problem at all. There are countless arguments against increasing block size and why extra-large blocks are harmful. I skip this part and assume that we agree on the necessity of implicitly limiting the block size even if the explicit hard cap is removed.

Now, suppose that we have omitted the requirement that the total gas cost should be less than or equal twice the target. Currently, the base fee is only a function of the gas usage of the previous block.

![](https://ethresear.ch/uploads/default/original/2X/0/098d4d25c141908ce7173f279d89189ac2669fdf.svg)

![](https://ethresear.ch/uploads/default/original/2X/3/3e82da67a5a430560c2d971a8142d6ce81e84647.svg)

Hence for example, if I want to buy tons of storage, I will be charged a constant price for the gas fee per gas cost. To be more concrete, I have to pay gas cost times base fee where the base fee is constant. Therefore, my total fee payment is a linear function of my gas cost.

However, assume that the formula for the base fee is modified in the following way

`delta = "current" gas used - target gas used`

and the rest remains the same. Now, delta is a linearly increasing function of my gas usage in the current block. Thus, the current base fee is also a linearly increasing function of my own gas cost imposed on the network.

Altogether, the fee price per gas cost is no longer constant, and the more gas I use, the higher the price I have to pay for it. This means that if someone tries to buy a big chunk, this action will affect the price in a negative way (they get a worse price), which is exactly the same as the good old slippage concept from the economy.

Moreover, if someone wants to attack the network, this rising price will soon surpass every other honest guy’s bid. Therefore, the attacker has to pay all this money alone, which grows quadratically with respect to the block size.

---

**kristofgazso** (2021-03-30):

That seems like a great suggestion for stopping destructive third parties from getting a lot of gas at a fixed price. On the other hand, I wonder what sort of effect this would have on the move to Layer 2. L2 solutions are most efficient when they batch their transactions into one L1 transaction, which generally uses a lot of gas. Don’t you think your system would disincentivize larger, more complicated transactions (complicated contract execution like L2 anchoring) in favour of smaller ones (like L1 transfers) which is exactly what we are trying to move away from with our more rollup centric roadmap? Perhaps I have missed something however

Also, regarding my original proposal, this seems like it would make it a lot less likely that the gas limit would be reached, which is a good way to solve the problem it had. When, occasionally, it still does, do you think it is acceptable that there is no way to prioritize transactions?

---

**mtefagh** (2021-03-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/kristofgazso/48/5717_2.png) kristofgazso:

> Don’t you think your system would disincentivize larger, more complicated transactions (complicated contract execution like L2 anchoring) in favour of smaller ones (like L1 transfers) which is exactly what we are trying to move away from with our more rollup centric roadmap?

Yes, your point is true. On one hand, spreading transactions across different blocks helps in avoiding network congestion. On the other hand, sometimes the user pays less fee if they execute certain transactions together. However, there is a trade-off between UX and the pressure incurred on the network and full nodes. This can be, to some extent, mitigated by executing L2 anchoring in under-used blocks to avoid creating extra-large blocks.

![](https://ethresear.ch/user_avatar/ethresear.ch/kristofgazso/48/5717_2.png) kristofgazso:

> When, occasionally, it still does, do you think it is acceptable that there is no way to prioritize transactions?

First of all, you can remove the gas limit altogether by relying on the fact that slippage makes a potential attack too costly. But apart from that, even right now, some strategic miners prioritize miner extractable value (MEV) over collecting fees. I believe that in the scenario you mentioned, miners will choose transactions in order to optimize for MEV.

---

**barnabe** (2021-03-31):

Nice writeup! An issue however is that any fixed tip rule means the mechanism is no longer off-chain agreement-proof. See [Tim Roughgarden’s report](http://timroughgarden.org/papers/eip1559.pdf), for instance section 8.5 on the “tipless mechanism”. It’s sort of a degenerate version of your proposal, where the tip is fixed to zero.

If miners receive some fixed quantity, either zero or in your case a quantity determined by the total hashrate/amount staked (btw, I am not clear why that’s a good proxy for the tip level), then users who really want to get ahead, or MEV users, are incentivised to enter into off-chain agreements with miners, since the tip grammar you suggest (a fixed value based on hashrate) is insufficient to let them express their preferences.

In a sense this is already true for MEV, with bundles being negotiated off-chain, but there is no clear UX improvement to disallowing non-MEV users to quote their own tips. As you mention it will be most of the time 1 Gwei, and this is due to the inherent dynamics of 1559, which targets an effective demand equal to the block target size always (see [here](https://barnabe.substack.com/p/understanding-fees-in-eip1559) for instance). However a UX need not show users two numbers, basefee and the tip, they could simply show the expected total and ask the user whether they want to transact at that price or not (see [the end of this post](https://barnabe.substack.com/p/better-bidding-with-eip1559) for my thoughts on wallet UX).

As you also point out choosing the wrong function to determine the appropriate tip also exposes the fee market to inefficiencies. But since letting it “float” means it is in fact fixed most of the time (to 1 Gwei) and the UX doesn’t suffer, a floating tip seems like a strictly better option, that doesn’t introduce biases to the market.

