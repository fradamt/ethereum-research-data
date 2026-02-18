---
source: ethresearch
topic_id: 13825
title: MEV minimization using randomness
author: cybertelx
date: "2022-10-02"
category: Economics
tags: [mev, rollup]
url: https://ethresear.ch/t/mev-minimization-using-randomness/13825
views: 3800
likes: 21
posts_count: 16
---

# MEV minimization using randomness

I’ve been thinking of this simple idea for combating MEV on layer 2 that isn’t completely fleshed out yet and it’s probably flawed in many ways.

The rollup sequencer(s) would be able to choose transactions to add in their block, however they don’t get to choose the ordering. Instead, the order of transactions in a block is random (perhaps chosen using a VRF on L1)

Would that work and are there any potential issues with this idea?

## Replies

**MicahZoltu** (2022-10-03):

This incentivizes shotgun transactions, where you just fire off a lot of transactions with different randomness seeds (e.g., transaction hashes) so that at least one of them will land before the target and one after the target.

This leads to excessive/unnecessary gas utilization with all of the “failed” transactions landing on chain and then being no-ops, so is generally frowned on as a solution to transaction ordering.

---

**Pandapip1** (2022-10-03):

The other issue with this is that if the block proposers are the ones extracting MEV, then they can just try different nonces until they get the correct orders.

[@MicahZoltu](/u/micahzoltu) I don’t see what’s wrong with frontrunners having to execute a bunch of failed transactions. If they have to spend a bunch of gas, then that’s a good thing since it disincentivizes trying to frontrun, right?

EDIT: Split into two comments.

---

**Pandapip1** (2022-10-03):

I propose the following alternative, which would make MEV very hard for block proposers:

- Block proposers can pick which transactions to include or not to include in advance. The hash of all these transactions is computed. Let these be the initial orders for those transactions.
- A block is only valid if the following is true:

The transaction with a median order (treated as binary numbers) is the next transaction included in a block. The median can be efficiently found in O(n) time with a selection algorithm.
- The orders of the remaining transactions are XOR’d with the above hash.
- Rinse and repeat.

The above is `O(n^2)` to compute, but a lot more complicated to front run/MEV extract since a transaction needs to be generated so that it **and** the next transaction are medians. This is computationally infeasible.

---

**MicahZoltu** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/pandapip1/48/9697_2.png) Pandapip1:

> @MicahZoltu I don’t see what’s wrong with frontrunners having to execute a bunch of failed transactions. If they have to spend a bunch of gas, then that’s a good thing since it disincentivizes trying to frontrun, right?

If there is a $1M MEV opportunity, front runners are willing to spend up to $1M in gas to capture that opportunity.  If this is spread out over 10s of thousands of transactions being thrown at the chain, that results in a huge amount of block space used that no one actually benefits from.  By allowing searchers to compete off-chain and only the winner lands on-chain with the minimal gas used, we don’t waste gas space for something that was going to be captured anyway.

Essentially, we want the gas used by MEV to be as low as possible for any given opportunity, and making it so you can only capture the opportunity by spending huge amounts of gas, or flooding the network, turns a minor problem (MEV extraction) into a major problem (DoS attack).

---

**MicahZoltu** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/pandapip1/48/9697_2.png) Pandapip1:

> I propose the following alternative, which would make MEV very hard for block proposers:
>
>
> Block proposers can pick which transactions to include or not to include in advance. The hash of all these transactions is computed. Let these be the initial orders for those transactions.
> A block is only valid if the following is true:
>
> The transaction with a median order (treated as binary numbers) is the next transaction included in a block. The median can be efficiently found in O(n) time with a selection algorithm.
> The orders of the remaining transactions are XOR’d with the above hash.
> Rinse and repeat.
>
>
>
>
> The above is O(n^2) to compute, but a lot more complicated to front run/MEV extract since a transaction needs to be generated so that it and the next transaction are medians. This is computationally infeasible.

If it is sufficiently hard to predict order, then the shotgun approach will be used which is worse.

---

**Pandapip1** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If there is a $1M MEV opportunity, front runners are willing to spend up to $1M in gas to capture that opportunity. If this is spread out over 10s of thousands of transactions being thrown at the chain, that results in a huge amount of block space used that no one actually benefits from. By allowing searchers to compete off-chain and only the winner lands on-chain with the minimal gas used, we don’t waste gas space for something that was going to be captured anyway.

Is there data on the distribution of MEV per transaction?

---

**Pandapip1** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If it is sufficiently hard to predict order, then the shotgun approach will be used which is worse.

Could you formalize the shotgun approach? Remember, the expected MEV has to be greater than the opportunity costs of all those priority fees, both for producer-validators and for external MEV bots.

Assuming the need for exactly one transaction before another transaction (best case MEV), a priority gas cost of p, and a MEV of m, then an upper bound for the number of transactions for the best shotgun EV (t) is naïvely given by

p*t<m*\frac{t}{t+1}

setting the cost to benefit. Solving for t, we get:

t<\frac{m}{p}-1

Therefore, any transaction with MEV less than twice the priority fee will never be shotgunned. A slippage of 0.5\% is standard and the priority fee is about \$2 right now. Therefore, under my system, any trade less than \$800 is not worth extracting the MEV of.

EDIT: It’s important to note that this is a lower bound. The above equation makes a few unrealistic assumptions in favor of the MEV extractor. The true minimum value is probably \gg\$800.

---

**MicahZoltu** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/pandapip1/48/9697_2.png) Pandapip1:

> Is there data on the distribution of MEV per transaction?

My guess is Flashbots has the data somewhere, you may want to ask around on their forum.

![](https://ethresear.ch/user_avatar/ethresear.ch/pandapip1/48/9697_2.png) Pandapip1:

> Therefore, any transaction with MEV less than twice the priority fee will never be shotgunned. A slippage of 0.5% 0.5%0.5% is standard and the priority fee is about $2 $2$2 right now. Therefore, under my system, any trade less than $800 $800$800 is not worth extracting the MEV of.

I’m not sure where you are getting $2 priority fee as I pay ~$0.03 for an ETH send and maybe 10x that for normal-ish contracts, but everything should be done in ETH not USD as that is the underlying currency of the system.

The point of my argument against encouraging shotguns isn’t that *all* MEV is profitable.  It is that when high value MEV does show up the chain will get hammered by competition for it via shotgunning transactions.  There have been MEV opportunities worth 100+ ETH before and they were not incredibly rare, with 10 ETH being somewhat regular and 1 ETH being “common”.  I haven’t paid attention recently, but all of these would get shotgunned, likely by multiple competing bots, and each time one of these happens the chain gets flooded with transactions that no one actually wants to land.

---

**Pandapip1** (2022-10-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I’m not sure where you are getting $2 priority fee as I pay

I can’t replicate the $2 priority fee anymore either… but I’m definitely not getting ~$0.03 for a simple ETH transfer (I’m getting roughly $1). For a uniswap swap, I’m getting upwards of a $3 fee (of which a few millionths of a dollar is the priority fee). Not sure why I was obsessed by the priority fees; fees in general apply here.

(Yes, I know these discussions should be in ETH. But people tend to execute swaps in terms of USD, so that’s what I’m using here).

Since each failed transaction will cost at least as much as an ETH transfer (which will probably not drop below \$0.5) we get that any trade under \$200 with normal slippage is not worth trying to shotgun. Worst case. Right now, uniswap trades wouldn’t be worth trying to shotgun unless they are trading more than \$1200.

---

**MicahZoltu** (2022-10-05):

`1 nanoeth per gas * 21000 gas / 10^9 nanoeth per eth = 0.000021 ETH`.  This is the lower bound we have seen recently on gas price, though 5x that is more common.  If you include a priority fee of 1 (which I suspect is too high), double those numbers, and they are still lower than your estimates.

---

**Pandapip1** (2022-10-06):

I don’t know where you’re getting those numbers from. I’m getting my data from https://ethgasstation.info/ and wallet estimates. Admittedly, the data on ethereum gas station is certainly lower than what’s given by my wallet, and I could absolutely see gas fees dropping below $0.5. I still don’t see them dropping below $0.25, which still gives a (worst-case) $100 shotgun threshold and a $150 threshold for using more than a single trasaction.

Either way, using your numbers, we still have that trades under $50 aren’t worth shotgunning with more than a single transaction. Trades under $35 aren’t worth shotgunning at all. Worst case.

I’m looking up the uniswap analytics. But I suspect that my proposal is much better than the status quo.

---

**Pandapip1** (2022-10-06):

Okay, so this is a really rough estimate.

Flashbots says that the total amount of MEV in the history of Ethereum is $675,524,491. The current block number is 15688561, and there have been historically about 380 transactions per block.

\$675,524,491*\frac{1}{15688561\text{block}}*\frac{1 \text{block}}{380 \text{transactions}}=\frac{\$0.11331160512}{transaction}

So, not a lot of MEV per transaction. That’s the equivalent of a trade of about $22.

---

**MicahZoltu** (2022-10-07):

We generally don’t care/worry about the status quo.  We worry about attacks.  The data you need to find is how frequently there is MEV worth significant amounts of money, because historically we have seen up to 95% of MEV rewards go to paying gas fees (in some cases over 100% of MEV goes toward fees across all participants).

This means that if there is a 1000 ETH MEV opportunity, we should assume that people will be shotgunning with ~1000 ETH spent on gas *at the current gas price* (not considering increased base fee).  Assuming 10 nanoeth / gas (which is normal these days), that is over 3,000 100% full blocks, which is a *lot* of congestion.  Even if that sort of thing only happens once every couple of years, that is still very significant.  100 ETH is still hundreds of blocks worth of shotgunned transactions that will eventually be included on-chain, taking up valuable real estate that legitimate transactions could take up.

---

**cybertelx** (2022-10-08):

Just came up with a new idea: random ordering + user has to create a small proof-of-work or a short VDF for each transaction sent. This should make shotgunning much harder.

However, the tradeoff is that we would have to lose compatibility with the standard JSON-RPC API, or maybe the RPC node could run VDFs for users, but with strict ratelimits

---

**MicahZoltu** (2022-10-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/cybertelx/48/10158_2.png) cybertelx:

> random ordering + user has to create a small proof-of-work or a short VDF for each transaction sent. This should make shotgunning much harder.

Proof of Work in this context would just be a way of charging the user for something without needing them to have anything other than money and a computer.  Charging more for transaction inclusion doesn’t fix the problem, and if it did we could just increase the fee directly which would be more amenable to using from a mobile device than some kind of PoW.

