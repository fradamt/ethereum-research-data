---
source: ethresearch
topic_id: 10266
title: Add a minimum burn per Block – No more 0 tx blocks. 🔥
author: CryptoKass
date: "2021-08-05"
category: Economics
tags: []
url: https://ethresear.ch/t/add-a-minimum-burn-per-block-no-more-0-tx-blocks/10266
views: 2750
likes: 12
posts_count: 13
---

# Add a minimum burn per Block – No more 0 tx blocks. 🔥

Zero transaction blocks are bad for a few obvious reasons, they are rare but still harm the practical throughput of the network.

The London update is live, I’m happy! However with reduced fees going to miners for each processed transaction we may see more zero transaction blocks. Transactions are worth less to miners than before. Perhaps we could solve this adding a minimum gas burn requirement for each block…

**Minimum burn per block**

Future valid blocks must burn at least X amount of WEI. This requirement can be satisfied by the transactions burn’t fees **or by burning from the block reward**. If the block is empty then X is burn’t from the reward.

**This increases the value of processing each transaction to the miner beyond the tip.**

Would this work? If not is there anything else we could do about zero transaction blocks?

- Edit: Perhaps the minimum burn could trigger when the average block capacity is over 50% - when the network is currently highly utilised, this is also when empty blocks can do the most harm.
- Edit 2: See MicahZoltu’s answer.
- Edit 3: See  Face-Shaver’s proposal to make miners pay in proportion to their block size.

## Replies

**CryptoKass** (2021-08-05):

**Examples using a minimum burn requirement**

Block A (empty):

- Block reward is 2 ETH
- 0 Transactions in block. 0 ETH Burn’t.
- Minimum Burn requirement is 0.5 ETH
- Miner receives 2 - 0.5 = 1.5 ETH

Block B (partially filled):

- Block reward is 2 ETH
- 50 transactions in block. 0.55 ETH burn’t.
- Minimum Burn requirement is 0.5 ETH
- Miner receives 2 ETH + tips

With 50 transactions in the block, each one is worth on average `0.5 ETH / 50 ` + tips to the miner.

- Increasing the incentives to include transactions without increasing the emission rate.
- Lower guaranteed emission rate compared to no minimum burn requirement.
- Doesn’t cause halting if there are genuinely fewer transactions to process.
- Introduces a hard cost to mining zero transaction blocks.

---

**joshuad31** (2021-08-05):

I cannot think of a way that this could potentially be abused and it does seem to deter miners from producing empty blocks.  Can you provide a steel-man argument for why this would not be a valid upgrade to the network?

---

**DimOK** (2021-08-05):

In case the minimal burn is set too high, or if network is not being used at full for some reason at particular moment, then miners will get penalized for nothing.

Moreover, the miner, who produced the empty block already penalized, by not earning tips from transactions he could have processed.

Empty blocks are awful and something need to be done with them, but this suggestion is too strightforward.

Can someone briefly explain, why blocks without transactions even exists? Is it miner decision (I don’t think there are any settings regarding transaction exclusion from blocks in any public miner software), software bug or some other circumstances?

---

**CryptoKass** (2021-08-05):

Thanks for your response,

**A block with transactions, is worth more to end users than an empty block, this suggestion is to utilise the EIP-1559 burn to value these blocks better.** Tips help this, but from the users wallet, the minimum burn increases the incentive, but from the block reward instead – better for users.

(Hmmm! Maybe tips really should just be for priority, in cases where the blocks are at capacity. This would mean we would have even more predictable transaction fees.)

**RE: Minimum burn too high**

The would definitely need some more thought/research to determine how the minimum burn is calculated. If its based on a percentage of the `blocks gas limit * base fee price`, then it will dynamically move up and down based on the current utilisation of the network. Ideally the minimum burn would no penalise the average miner at all, perhaps requiring only 10% block utilisation to unlock the full reward.

**RE: Why mine empty block?**

- I’m not 100% sure why they do it… but one reason could be that miners want to start mining the next block ASAP. Sometimes they start mining a block before fully downloading the previous block because the difference in profitability is quite small. Minimum burn per block doesn’t fully solve this, but it further disincentives this behaviour (potentially to a point where it may no longer be profitable to do it.)
- Some miners may also not find it feasible to store the full chain state, which is necessary to process new transactions. Additionally, with the move to proof-of-stake, validators may be running on ultra low end hardware, which may struggle to download and process transactions. This minimum burn disincentives these lazy validators, without leading to high end user costs.

I found this article about it, (it also leads a good bitmex article about this too).

https://medium.com/@ASvanevik/why-all-these-empty-ethereum-blocks-666acbbf002

I do think there may be a better solution for empty blocks… we just don’t know what it would be yet.

**(Edit: Perhaps the minimum burn could trigger when the average block capacity is over 50% - when the network is currently having high utilisation, this is also when empty blocks can do the most harm.)**

---

**Face-Shaver** (2021-08-05):

I think what you are suggesting is aligned with [my proposal to make miners pay in proportion to their block size.](https://ethresear.ch/t/who-pays-for-congestion-optimal-design-of-protocol-fees/10174)

The existence of empty blocks doesn’t necessarily bring down average throughput because they are balanced out by full blocks. However, if these oscillations continue (as I believe they are likely to),1559 is not making fees predictable for average price-sensitive users. That would mean we are incurring the costs of incentive misalignment without getting much out of it.

---

**DimOK** (2021-08-05):

As far, as I understand Ethereum miners incentives, rewarding “uncle” blocks effectively negates necessity to rush for block generation.

To solve the problem we should understand the reasons, why problem exists. That’s why I am interested in explanation behind not 100% full blocks while there are thousands of transactions in mempool.

If it is miners choice to produce empty blocks instead of getting smaller then usual processing fees - then economical incentives doesn’t work in this case, as miners prefer to earn less, than they can.

If it is some technical problem, like inability to quickly get necessary amount of transactions from mempool - it will be solved by miners sooner or later.

I don’t know the correct answer, but very curious.

---

**MicahZoltu** (2021-08-06):

Completely empty blocks (no transactions at all) are a side effect of the way mining works.  You generally have separate hardware crunching hashes from the hardware that is doing Ethereum stuff (e.g., video card, mining rig, etc.).  When a miner’s Ethereum client receives a block, it immediately wants to start building on top of that block and so it creates an initially empty block and sends it off to the mining hardware to start crunching.  While that is happening, the Ethereum client then builds a block full of transactions (a process that takes hundreds of milliseconds) and then sends that off to its mining hardware to start working on in place of the original block.

If we were to penalize miners for producing empty blocks, they instead would spend that time mining a fork block, which is unhealthy for the network.

---

Separate from the above, EIP-1559 makes it so blocks are **on average** 50% full.  This means that for every 100% full block there will be one 0% full block, or two 25% full blocks, etc to offset that.  This is by design and everything is functioning as intended.  When you see *mostly* empty (and sometimes all the way empty) blocks now that is completely normal and working as expected.  When we look at blocks in aggregate, we are seeing that they are around 50% full on average which means everything is working properly.

Also, as of London if a miner does produce an empty block for *any reason* it lowers the base fee which is likely to lead to subsequent blocks being fuller.  This block elasticity actually helps increase total throughput because where previously we would sometimes end up with empty blocks that were not offset by fuller blocks later, instead those empty blocks will now result in more full blocks coming after it.

---

**CryptoKass** (2021-08-06):

Thanks for this explanation!

More from EIP-1559 about empty blocks:

- > This EIP will increase the maximum block size, which could cause problems if miners are unable to process a block fast enough as it will force them to mine an empty block. Over time, the average block size should remain about the same as without this EIP, so this is only an issue for short term size bursts. It is possible that one or more clients may handle short term size bursts poorly and error (such as out of memory or similar) and client implementations should make sure their clients can appropriately handle individual blocks up to max size.
- > It is possible that miners will mine empty blocks until such time as the base fee is very low and then proceed to mine half full blocks and revert to sorting transactions by the priority fee. While this attack is possible, it is not a particularly stable equilibrium as long as mining is decentralized. Any defector from this strategy will be more profitable than a miner participating in the attack for as long as the attack continues (even after the base fee reached 0). Since any miner can anonymously defect from a cartel, and there is no way to prove that a particular miner defected, the only feasible way to execute this attack would be to control 50% or more of hashing power. If an attacker had exactly 50% of hashing power, they would make no Ether from priority fee while defectors would make double the Ether from priority fees. For an attacker to turn a profit, they need to have some amount over 50% hashing power, which means they can instead execute double spend attacks or simply ignore any other miners which is a far more profitable strategy.
> Should a miner attempt to execute this attack, we can simply increase the elasticity multiplier (currently 2x) which requires they have even more hashing power available before the attack can even be theoretically profitable against defectors.

Does anybody know how the move to PoS effect the rate of empty blocks? I guess we should see fewer.

---

**Face-Shaver** (2021-08-06):

> This block elasticity actually helps increase total throughput because where previously we would sometimes end up with empty blocks that were not offset by fuller blocks later, instead those empty blocks will now result in more full blocks coming after it.

That’s a good point. The multiplicative updating rule also puts an upward pressure on the average block size, so perhaps the long term average block size will be a few percentage points above pre-1559 levels.

> When we look at blocks in aggregate, we are seeing that they are around 50% full on average which means everything is working properly.

The oscillation was certainly expected, but is it desirable? It makes fee estimation more difficult for the average price-sensitive user. Also, some would argue that despite the average block size being (roughly) the same, 100% spikes are still bad for decentralization.

---

**MicahZoltu** (2021-08-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/cryptokass/48/5523_2.png) CryptoKass:

> Does anybody know how the move to PoS effect the rate of empty blocks? I guess we should see fewer.

The first class I mentioned will likely go away with PoS since block production is no longer a race.  The others will remain.

---

**MicahZoltu** (2021-08-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/face-shaver/48/6805_2.png) Face-Shaver:

> The oscillation was certainly expected, but is it desirable? It makes fee estimation more difficult for the average price-sensitive user. Also, some would argue that despite the average block size being (roughly) the same, 100% spikes are still bad for decentralization.

Block space isn’t (currently) a transferable resource.  We have `n` block space available at time point `a`, and we need to auction that off as efficiently as possible.  Smoothing prices would need to come from moving block space availability to times where people want it.  EIP-1559 does this a little bit, but it can really only move the block space around by essentially one or two blocks at a time.  This should improve things slightly, but possibly not noticeable.

I have discussed (I think on this forum somewhere) options for moving block space availability across larger sections of time, but it requires splitting up costs between storage, network, CPU which would further add even more complexity to Ethereum transactions for end users.

---

**Face-Shaver** (2021-08-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Block space isn’t (currently) a transferable resource. We have n block space available at time point a, and we need to auction that off as efficiently as possible. Smoothing prices would need to come from moving block space availability to times where people want it.

That’s a great framework. EIP-1559 transfers block space to some extent, but as you said, the base fee adjusts so quickly that we can’t have a few hours of full blocks during a volatile market. Another issue is that the block size scales too much in response to small variations in demand. I think having miners pay tax to the protocol when they create larger blocks can help in these regards, and in general allocate larger blocks to periods with high demand.

