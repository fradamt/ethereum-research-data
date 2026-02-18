---
source: ethresearch
topic_id: 10174
title: Who pays for congestion? Optimal design of protocol fees
author: Face-Shaver
date: "2021-07-24"
category: Economics
tags: []
url: https://ethresear.ch/t/who-pays-for-congestion-optimal-design-of-protocol-fees/10174
views: 2891
likes: 3
posts_count: 14
---

# Who pays for congestion? Optimal design of protocol fees

**The Problem**

EIP-1559 will introduce a protocol fee on Ethereum transactions and allow the block size to be dynamically adjusted in response to congestion. Charging a protocol fee when the chain is congested is an efficient way to shift MEV from miners to ETH holders without hurting the users. Also, a flexible block size makes the allocation of block space more efficient. However, under the current fee structure, the wrong people can end up paying for congestion.

Suppose there are two blocks, and we target an average block size of one transaction per block. There are two users, Alice and Bob. Normally, Alice sends one transaction in Block 1, and Bob sends one transaction in Block 2.

Now, suppose Alice receives a shock and wants to send two transactions in Block 1. EIP-1559 allows her to do so; as long as she pays enough to compensate for the increased uncle risk, the miner will include both of her transactions in Block 1. This is great for Alice. However, because Block 1 was larger than the target size, the base fee is increased in Block 2. This means that Bob either has to pay the higher base fee or wait a block to send his transaction. Bob ends up paying for the congestion that Alice caused.

In general, when users congest a block, it is users of the subsequent blocks that pay for the congestion. This is undesirable for a couple of reasons.

**1. It is unfair.**

It is not fair that Bob should pay to allow Alice to send an extra transaction.

**2. It increases congestion.**

Because Alice does not care whether Bob pays more, she will congest her block whenever she has the slightest need to do so. In economics jargon, congesting a block exerts a *negative externality* on the users of future blocks. Because users do not pay for congesting their block, they will congest it too much relative to what is socially optimal.

**3. It intensifies gas auctions.**

Let us change our example and assume that Alice and Bob are competing to include their transactions in Block 1, which is expected to be congested. If Bob loses, he will not only have his transaction delayed, he will also pay a higher base fee in Block 2. So outbidding Alice becomes even more important. The same will hold for Alice, and as a result, the gas auction will become more intense. *Users will pay larger tips to miners to avoid paying higher base fees to the protocol.*

**A Solution**

I propose that when a block is congested, the users of that same block pay for the congestion. We can implement this by charging the miner a fee based on how much gas is used in his block. For example, a miner who uses x gas in his block might be required to pay f(x)=kx^2 gwei where k>0 is some constant. The marginal cost of including one additional gas is 2kx gwei, so the miner will include all transactions that pay him at least 2kx+\epsilon gwei per gas until he reaches the block limit, where \epsilon is compensation for uncle risk.

We can think of 2kx as a Pigouvian tax on block space. When the demand for block space is high, x will be large (block size will be large), kx^2 will be large (the protocol fee will be large), and 2kx will be high (users will have to pay more to be included). Hence block space will adjust to demand, and we can calibrate the fee function f(x) to target the average block size that we want.

**Technical Asides**

It should not matter in theory whether we charge the miner or the users. But charging the miner may be easier to implement.

To choose f(x), we could use a supply and demand model of block space where the social cost of centralization risk is an increasing function of the average block size. We would solve for f(x) that makes the agents internalize the social cost, while ensuring that users do not bear too much of the tax burden.

## Replies

**mtefagh** (2021-07-26):

I guess many have independently rediscovered and mentioned this point several times, but people are intentionally ignoring it! See:

https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/32?u=mtefagh



      [github.com/zcash/zcash](https://github.com/zcash/zcash/issues/3473#issuecomment-479684321)












####



        opened 10:38PM - 17 Aug 18 UTC



        [![](https://ethresear.ch/uploads/default/original/2X/8/882285f3628ea3784835c306639dd8f62179a6d9.png)
          vbuterin](https://github.com/vbuterin)





          D-economics


          A-consensus


          I-dos


          F-tx-fees


          Network Upgrade Wishlist







I've presented the ideas here online and at multiple events including most recen[…]()tly CRYPTO 2018 today, and I got a positive reception from some Zcash community members and it was suggested that I start a discussion on this topic, so here goes.

Currently, most public blockchains, including Ethereum, Bitcoin, and (as I understand) Zcash, use a block size limit and a fee market to regulate the inclusion of transactions and prevent users from spamming the blockchain, forcing transaction senders to pay for the costs they impose on the network. However, this cap-and-auction approach is only one of many ways of achieving this goal, and there are other mechanisms that are worth exploring, that I think are better for several reasons.

There are three major problems with the status quo of transaction fee markets:

* **Mismatch between volatility of transaction fee levels and social cost of transactions**: transaction fees on mature public blockchains, that have enough usage so that blocks are full, tend to be extremely volatile. On Ethereum, minimum fees are typically around 2 gwei (10^9 gwei = 1 ETH), but sometimes go up to 20-50 gwei and have even on one occasion gone up to over 200 gwei: https://etherscan.io/chart/gasprice. This clearly creates many inefficiencies, because it's absurd to suggest that the cost incurred by the network from accepting one more transaction into a block actually is 100x more when gas prices are 200 gwei than when they are 2 gwei; in both cases, it's a difference between 8 million gas and 8.02 million gas.
* **Inefficiencies of first price auctions**: see https://ethresear.ch/t/first-and-second-price-auctions-and-improved-transaction-fee-markets/2410 for a detailed writeup. In short, the current approach, where transaction senders publish a transaction with a fee, miners choose the highest-paying transactions, and everyone pays what they bid, is well-known in mechanism design literature to be highly inefficient, and so complex fee estimation algorithms are required, and even these algorithms often end up not working very well, leading to frequent fee overpayment. See also https://blog.bitgo.com/the-challenges-of-bitcoin-transaction-fee-estimation-e47a64a61c72 for a Bitcoin core developer's description of the challenges involved in fee estimation in the status quo.
* **Instability of blockchains with no block reward**: in the long run, blockchains where there is no issuance (including Bitcoin and Zcash) at present intend to switch to rewarding miners entirely through transaction fees. However, there are [known results](http://randomwalker.info/publications/mining_CCS.pdf) showing that this likely leads to a lot of instability, incentivizing mining "sister blocks" that steal transaction fees, opening up much stronger selfish mining attack vectors, and more. There is at present no good mitigation for this.

I will suggest an alternative mechanism that mitigates all three of the issues. The protocol internally maintains a fee level `f`, and a miner that creates a block that includes `d` bytes (or gas, or weight units, or whatever) must pay a fee of `f * d`, which gets put into a pot (in practice, this means that the miner will only accept transactions that pay that much in fees to compensate the miner). There is a maximum weight limit `M`. The protocol adjusts `f` so that long-run block space usage averages out to `M/2`; it can do this for example by adjusting `f[n+1] = f[n] * (1 + 0.25 * (w[n] / M - 0.5))`, where `f[n]` is the fee level in the current block, `f[n+1]` is the fee level for the next block, and `w[n]` is the total bytes/gas/weight consumed in the current block (that is, if the last block was 50% full, leave the fee unchanged, if the last block was 10% full, drop it by 10%, if the last block was 90% full, increase it by 10%). In every block, a miner gets a reward equal to 1/N (eg. 1/10000) of the money remaining in the pot (note that this amount does NOT depend on the transactions they include in their block).

This accomplishes the following goals:

* It mitigates the economic inefficiencies from social cost mismatch due to fee volatility. There is a fairly nuanced economic argument here; see particularly pages 16-20 of the paper linked in https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838 (though I recommend reading the whole paper) for a detailed argument of why this is the case. Intuitively, the adjusting fee mechanism works like a fixed fee in the short run and a cap in the long run, and it turns out that because of [arguments from Martin Weitzman's 1974 paper](https://scholar.harvard.edu/weitzman/files/prices_vs_quantities.pdf) fixed fees are likely better than a cap in the circumstances that basically all public blockchains are in today and will likely continue to be in.
* It replaces the auction with a fixed price sale (except during short periods where blocks fill up completely until fees catch up), eliminating first-price-auction inefficiencies and making fee estimation extremely simple: calculate the fee `f` for the next block, if you can afford it pay it, otherwise don't.
* It creates a mechanism similar to a permanent block reward (the 1/N coming from the pot), mitigating many of the instability issues with fee-only blockchains without requiring actual permanent issuance.

This is something that's being discussed in the context of Ethereum but is theoretically relevant to any public blockchain, so is certainly something that the Zcash community could consider.














      [github.com/zcash/zcash](https://github.com/zcash/zcash/issues/3473#issuecomment-485291119)












####



        opened 10:38PM - 17 Aug 18 UTC



        [![](https://ethresear.ch/uploads/default/original/2X/8/882285f3628ea3784835c306639dd8f62179a6d9.png)
          vbuterin](https://github.com/vbuterin)





          D-economics


          A-consensus


          I-dos


          F-tx-fees


          Network Upgrade Wishlist







I've presented the ideas here online and at multiple events including most recen[…]()tly CRYPTO 2018 today, and I got a positive reception from some Zcash community members and it was suggested that I start a discussion on this topic, so here goes.

Currently, most public blockchains, including Ethereum, Bitcoin, and (as I understand) Zcash, use a block size limit and a fee market to regulate the inclusion of transactions and prevent users from spamming the blockchain, forcing transaction senders to pay for the costs they impose on the network. However, this cap-and-auction approach is only one of many ways of achieving this goal, and there are other mechanisms that are worth exploring, that I think are better for several reasons.

There are three major problems with the status quo of transaction fee markets:

* **Mismatch between volatility of transaction fee levels and social cost of transactions**: transaction fees on mature public blockchains, that have enough usage so that blocks are full, tend to be extremely volatile. On Ethereum, minimum fees are typically around 2 gwei (10^9 gwei = 1 ETH), but sometimes go up to 20-50 gwei and have even on one occasion gone up to over 200 gwei: https://etherscan.io/chart/gasprice. This clearly creates many inefficiencies, because it's absurd to suggest that the cost incurred by the network from accepting one more transaction into a block actually is 100x more when gas prices are 200 gwei than when they are 2 gwei; in both cases, it's a difference between 8 million gas and 8.02 million gas.
* **Inefficiencies of first price auctions**: see https://ethresear.ch/t/first-and-second-price-auctions-and-improved-transaction-fee-markets/2410 for a detailed writeup. In short, the current approach, where transaction senders publish a transaction with a fee, miners choose the highest-paying transactions, and everyone pays what they bid, is well-known in mechanism design literature to be highly inefficient, and so complex fee estimation algorithms are required, and even these algorithms often end up not working very well, leading to frequent fee overpayment. See also https://blog.bitgo.com/the-challenges-of-bitcoin-transaction-fee-estimation-e47a64a61c72 for a Bitcoin core developer's description of the challenges involved in fee estimation in the status quo.
* **Instability of blockchains with no block reward**: in the long run, blockchains where there is no issuance (including Bitcoin and Zcash) at present intend to switch to rewarding miners entirely through transaction fees. However, there are [known results](http://randomwalker.info/publications/mining_CCS.pdf) showing that this likely leads to a lot of instability, incentivizing mining "sister blocks" that steal transaction fees, opening up much stronger selfish mining attack vectors, and more. There is at present no good mitigation for this.

I will suggest an alternative mechanism that mitigates all three of the issues. The protocol internally maintains a fee level `f`, and a miner that creates a block that includes `d` bytes (or gas, or weight units, or whatever) must pay a fee of `f * d`, which gets put into a pot (in practice, this means that the miner will only accept transactions that pay that much in fees to compensate the miner). There is a maximum weight limit `M`. The protocol adjusts `f` so that long-run block space usage averages out to `M/2`; it can do this for example by adjusting `f[n+1] = f[n] * (1 + 0.25 * (w[n] / M - 0.5))`, where `f[n]` is the fee level in the current block, `f[n+1]` is the fee level for the next block, and `w[n]` is the total bytes/gas/weight consumed in the current block (that is, if the last block was 50% full, leave the fee unchanged, if the last block was 10% full, drop it by 10%, if the last block was 90% full, increase it by 10%). In every block, a miner gets a reward equal to 1/N (eg. 1/10000) of the money remaining in the pot (note that this amount does NOT depend on the transactions they include in their block).

This accomplishes the following goals:

* It mitigates the economic inefficiencies from social cost mismatch due to fee volatility. There is a fairly nuanced economic argument here; see particularly pages 16-20 of the paper linked in https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838 (though I recommend reading the whole paper) for a detailed argument of why this is the case. Intuitively, the adjusting fee mechanism works like a fixed fee in the short run and a cap in the long run, and it turns out that because of [arguments from Martin Weitzman's 1974 paper](https://scholar.harvard.edu/weitzman/files/prices_vs_quantities.pdf) fixed fees are likely better than a cap in the circumstances that basically all public blockchains are in today and will likely continue to be in.
* It replaces the auction with a fixed price sale (except during short periods where blocks fill up completely until fees catch up), eliminating first-price-auction inefficiencies and making fee estimation extremely simple: calculate the fee `f` for the next block, if you can afford it pay it, otherwise don't.
* It creates a mechanism similar to a permanent block reward (the 1/N coming from the pot), mitigating many of the instability issues with fee-only blockchains without requiring actual permanent issuance.

This is something that's being discussed in the context of Ethereum but is theoretically relevant to any public blockchain, so is certainly something that the Zcash community could consider.

---

**Face-Shaver** (2021-07-26):

Thank you for the links! And apologies for not citing them properly. As I commented on the EIP-1559 thread on [ethereum-magicians.org](http://ethereum-magicians.org), I am a bit surprised that the posts such as the ones you made two years ago have not led to a wider discussion.

I saw Vitalik’s reply to your comment on the zcash page, let me reproduce it here:

[![image](https://ethresear.ch/uploads/default/optimized/2X/9/9d576980fcdd395652e57db360d5e84694a74a58_2_690x181.png)image2226×585 71.1 KB](https://ethresear.ch/uploads/default/9d576980fcdd395652e57db360d5e84694a74a58)

This is not true. In an efficient mechanism, users need to *pay the cost that they inflict upon others through their own actions.* This is the idea behind the VCG mechanism. The second price auction is an example: the winner pays the bid of the highest losing bidder, *because that is how much harm he has caused to everyone else by winning the object himself.*

What Vitalik referred to may have been the fact that in a VCG mechanism such as the second price auction, your payment *conditional on winning the good* does not depend on your bid. However, whether you win or not does depend on your bids, and hence so does your payment.

I also saw that you and others have raised concerns about a miner’s attack based on this incentive misalignment. Let me think more about this. It seems in line with the observation that a user of a block with a low basefee (such as Alice in my example above) will tend to congest it excessively because Bob, not Alice, suffers from it. One could even call this an attack by Alice.

---

**mtefagh** (2021-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/face-shaver/48/6805_2.png) Face-Shaver:

> This is not true. In an efficient mechanism, users need to pay the cost that they inflict upon others through their own actions.

Sure, see here for a discussion on price impacts which is related to your proposed solution as it is similar to a temporary price impact:

https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/366?u=mtefagh

---

**Face-Shaver** (2021-07-26):

That’s interesting. Given that a user can allocate his transactions across multiple blocks, the literature on order execution strategies seems closely related to how a user will respond to any gas pricing scheme that we design. Surge pricing a la Uber may also be relevant.

This is definitely something we should be looking at. I am not yet sure what the best design is, but I am pretty sure that charging the wrong users will lead to big inefficiencies.

---

**mtefagh** (2021-07-26):

Also, I wanted to add a fourth negative point to the problem section of your post. Continuing from your third point, both Alice and Bob will broadcast their transactions in the first block, and hence, the fee will go up afterward. Therefore, none of them will broadcast anything  in the second block, and then again, both Alice and Bob will broadcast their transactions in the third block and so on. This somehow creates and incentivizes an oscillating behavior, and whoever deviates from it will be penalized by paying substantially higher fees. Apart from the fact that this is an unnecessary volatility, see this:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/mtefagh/48/3417_2.png)
    [Path-dependence of EIP-1559 and the simulation of the resulting permanent loss](https://ethresear.ch/t/path-dependence-of-eip-1559-and-the-simulation-of-the-resulting-permanent-loss/8964) [Economics](/c/economics/16)



> Continuing the discussion from DRAFT: Position paper on resource pricing:
> There exists an unintentional and uncoordinated version of this attack which is inevitable due to its decentralized nature. Suppose that a small portion of users (e.g., 5%) are rational enough to pay less fee by waiting whenever their transactions are not an emergency. For instance, a wallet client has a built-in feature that asks how much the user is willing to wait if the base fee is currently declining. The simple stra…

---

**Face-Shaver** (2021-07-26):

Thanks, I was just starting to look at your paper on Github. It’s interesting that an additive updating can give us path independence.

There might be a way to combine things. The user who congests must pay the fees. However, the optimal fees would probably depend on both demand for Ethereum transactions and how much block size we can afford to have without raising centralization risk too much; the former will be volatile over time and not correlated with the latter. This means we might want to periodically adjust the fee parameters to hit the target block size, sort of like how the block difficulties are adjusted.

Things would depend on our objectives, though. If we just want a regular Pigouvian tax, the fee should just correspond to the negative externality that is caused by transactions, and the size of this externality may be constant over time. This would mean that we allow the average block size to fluctuate over time according to demand for transactions, which is a natural outcome of optimization in this case.

On the other hand, if we want to target a fixed level of long term average block size, we do need to adjust the fees according to demand. In this case, we could consider a model where each transaction pays a fee according to how much the current block is congested, and this fee is adjusted every epoch (say two weeks) depending on the average block size of the previous epoch.

---

On second thought, even with a standard Pigouvian tax, there is an obvious way to limit the average block size - set a hard gas limit. So I would suggest that the fee only depends on the congestion of the current block, and we allow the block size to fluctuate but set a hard bound (such as 2x the target size). Parameter updates can be done through governance.

---

**alidarvishi14** (2021-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/face-shaver/48/6805_2.png) Face-Shaver:

> I propose that when a block is congested, the users of that same block pay for the congestion. We can implement this by charging the miner a fee based on how much gas is used in his block. For example, a miner who uses x xx gas in his block might be required to pay f(x)=kx^2 f(x)=kx2f(x)=kx^2 gwei where k>0 k>0k>0 is some constant. The marginal cost of including one additional gas is 2kx 2kx2kx gwei, so the miner will include all transactions that pay him at least 2kx+\epsilon 2kx+ϵ2kx+\epsilon gwei per gas until he reaches the block limit, where \epsilon ϵ\epsilon is compensation for uncle risk.

You can simply make users pay for the congestion they make by replacing the “n-1 th block size” with “n th block size” in the formula of basefee for the n th block.

This is somehow an implementation of the concept of slippage. As a user wants to buy more space on a block, he makes the price of a unit of space on the very same block goes up (not only price of space on later blocks).

---

**Face-Shaver** (2021-07-26):

Good point. I think we should go further and make only the users of the very same block pay more, and not the users of future blocks. This means that as soon as a demand spike subsides, fees go back to normal levels and users do not need to wait for the fees to go down.

---

**pietjepuk** (2021-07-26):

Not linked yet here, but definitely related is [Make EIP 1559 more like an AMM curve](https://ethresear.ch/t/make-eip-1559-more-like-an-amm-curve/9082) .

> Good point. I think we should go further and make only the users of the very same block pay more, and not the users of future blocks. This means that as soon as a demand spike subsides, fees go back to normal levels and users do not need to wait for the fees to go down.

What is “normal level”? How is that level determined in a way that cannot be manipulated?

---

**Face-Shaver** (2021-07-26):

By normal level of fees, I just meant the fee that we want users to pay when the block size is the target size. But the marginal cost of gas (which is f'(x)) would determine everything. We figure out how much an extra transaction above the target size costs in terms of increased risk of centralization, and make the user pay that amount as a fee.

The only case in which it makes sense for users to pay for congestion in previous blocks is if there is a the cost of oversized blocks is supermodular across consecutive blocks. If a consecutive series of oversized blocks poses a greater risk to the system compared to the same blocks dispersed over time, then users of consecutive blocks are indeed competing over the same space. However, even if that were the case, users should still pay for their own congestion, and the impact of congestion on future blocks should phase out. I.e. if an oversized block is followed by a series of target-sized blocks, the fee should decrease across the target-sized blocks.

---

**mtefagh** (2021-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/face-shaver/48/6805_2.png) Face-Shaver:

> However, even if that were the case, users should still pay for their own congestion, and the impact of congestion on future blocks should phase out. I.e. if an oversized block is followed by a series of target-sized blocks, the fee should decrease across the target-sized blocks.

Back to my analogy with market impact theory, your suggestion is called a transient price impact. See:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/mtefagh/48/3417_2.png)
    [Should storage be priced separately from execution?](https://ethresear.ch/t/should-storage-be-priced-separately-from-execution/9101/2) [Economics](/c/economics/16)



> Transient and temporary price impacts for the ephemeral costs and permanent price impacts for the permanent costs seem like a much more natural solution to me. I get the point of your numerical example but note that constants don’t affect the asymptotic behavior. This means that the effects you get from constants are totally dependent on the numerical ranges.

---

**Face-Shaver** (2021-07-26):

That’s very interesting. If we charge separately for storage, that fee should definitely be persistent across time.

If the marginal price of storage is constant, one might argue that we want a constant fee per storage. But the incidence of the fee (who bears the burden) also matters, and an increasing slippage may help reduce the burden on users.

---

**mtefagh** (2021-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/face-shaver/48/6805_2.png) Face-Shaver:

> That’s very interesting. If we charge separately for storage, that fee should definitely be persistent across time.
>
>
> If the marginal price of storage is constant, one might argue that we want a constant fee per storage.

As you have suggested, the permanent price impact charged for the storage should be linear. Even for this, there is already a lot of evidence from the economic literature. See:

https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/367?u=mtefagh

