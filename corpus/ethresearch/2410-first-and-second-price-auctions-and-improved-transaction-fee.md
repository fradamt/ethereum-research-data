---
source: ethresearch
topic_id: 2410
title: First and second-price auctions and improved transaction-fee markets
author: vbuterin
date: "2018-07-02"
category: Economics
tags: [fee-market, second-price-auction]
url: https://ethresear.ch/t/first-and-second-price-auctions-and-improved-transaction-fee-markets/2410
views: 34377
likes: 27
posts_count: 40
---

# First and second-price auctions and improved transaction-fee markets

*Special thanks to David Easley, Scott Kominers and others I talked to about these topics at [EC'18 || 19th ACM Conference on Economics and Computation](http://www.sigecom.org/ec18/), and to Vlad Zamfir for independently inventing and discussing the 50% targeting mandatory fee model.*

In blockchains like Bitcoin and Ethereum, transaction fees are both one of the ways in which miners (or more generally block proposers) get rewarded for processing transactions, as well as the mechanism for transaction prioritization: each transaction includes the fee that it is willing to pay, and miners are incentivized to select transactions with the highest fees in order to maximize their revenue. This means that users that really need high priority in the short run can get prioritized by including a much higher transaction fee, and it ensures that in the long run the blockchain is filled with higher-value use cases rather than lower-value use cases.

Currently, almost all blockchains use a mechanism that is equivalent to a [first-price auction](https://en.wikipedia.org/wiki/First-price_sealed-bid_auction): everyone submits a bid, and then if they get included they pay exactly the bid that they submit. The problem with this kind of mechanism is that there is no simple strategy for choosing the optimal bid price. For example, if you value a tx getting included right now at $1, you would be willing to bid anything up to $1, but if everyone else is bidding $0.05, then you could keep more money by bidding $0.08 instead; optimizing this requires complex models of the economy and real-time blockchain usage.

The usual alternative is a [uniform-price auction](https://en.wikipedia.org/wiki/Multiunit_auction#Uniform_price_auction), which involves charging every participant the same price as the price paid by the lowest bidder; that is, if for example the bids are:

```
0.02, 0.03, 0.05, 0.08, 0.13, 0.19, 1.00
```

And a miner has space for five transactions, they will include the top five, and each sender will pay only $0.05.

This has a much simpler strategy: bid whatever your valuation is. That is, someone who values a transaction getting included at $1 could just bid $1, and the fact that their bid is very high doesn’t mean they have to actually pay a large amount unless everyone else’s bid is similarly high.

Under the assumption that every user only wants a small portion of the space in each block, this is “truthful”: because each user only has a negligible impact on the price that they pay (which is almost entirely set by the mass of other users), and their bid only affects whether or not they get included in the block, you can show that bidding an amount equal to your valuation ensures an optimal outcome: if the clearing price ends up being lower than your valuation, you get included, and if it ends up being higher, you don’t, and so in both cases you’re happy with the outcome.

However, uniform-price auctions used in this context have two weaknesses (see [Credible Mechanisms](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3033208) for a “mainstream” treatment of some related ideas). First, a block proposer can include their own transactions in a block, and thereby increase the clearing price, increasing their own total revenue.

[![txfees](https://ethresear.ch/uploads/default/optimized/2X/d/d4d3a45aa14dd05c0bae7cfe97bbcc32e38348ab_2_460x193.png)txfees693×292 9.69 KB](https://ethresear.ch/uploads/default/d4d3a45aa14dd05c0bae7cfe97bbcc32e38348ab)

Second, a block proposer can collude with some portion of transaction senders, asking them to submit higher bids than their “actual” bids, and then refund them through a separate channel.

Both attacks are possible because, under the rules of this mechanism, a transaction sender increasing their bid by $1 can increase the block proposer’s total revenue by *more* than $1. First price auctions do not have these weaknesses.

Our goal is to discourage the development of complex miner strategies and complex transaction sender strategies in general, including both complex client-side calculations and economic modeling as well as various forms of collusion; the latter especially is dangerous as it creates an incentive for staking pools that can centrally manage the process of extracting gains from collusion.

The following is a proposal that makes some headway in that direction relative to the status quo, though it definitely does not achieve mathematically perfect optimality. It is an attempt to find the minimal protocol change that leads to a very significant improvement over the status quo.

The mechanism maintains a minimum fee F. Every transaction specifies a fee. For a transaction to be included in a block, the transaction must pay at least F. The fee is adjusted every block by the following formula, where \frac{prevBlockGas}{prevBlockMaxGas} is the portion of the previous block that was full, and k is a constant (0 < k < 2):

curBlockFee = prevBlockFee * (1 + k * (\frac{prevBlockGas}{prevBlockMaxGas} - \frac{1}{2}))

Miners receive the revenue from the transaction fee paid, minus the minimum fee. Transactions can include a minimum block number. That’s all there is to the mechanism.

Miners’ incentive is the same as it is in the first-price model: they try to gather up the most expensive transactions that they can, and include them into their block. One possible transaction sender strategy is as follows:

1. Check if the minfee is higher or lower than how much you value the transaction getting included. If it is higher, do not send the transaction. If it is lower, send a transaction, bidding the minfee plus 1% (or some other standard markup)
2. Publish an identical transaction, but with the minimum block number equal to two blocks in the future, and with the fee set by an imperfect heuristic algorithm as you would use today

In the normal case, blocks will be roughly half full, and so everyone’s transactions from case (1) would get in. Case (1) is “truthful” (in that it has a simple strategy that is trivially derived from a user’s valuation). In cases where blocks become full, case (2) would temporarily apply, though this would be rare; even in periods of very high demand, blocks being full would only last for a short time before the minfee catches up.

We can improve this further by allowing transaction senders to express their fee in the form of “whatever the minimum fee is, plus an increment F_i, up to a maximum of F_{max}”. Users could then express the preference “I don’t care as much about delays, I want to pay as little as possible, though I’m okay with anything up to some maximum”, or “try to get through with as little as possible for 5 blocks, then try to pay much more” or a number of other options.

Note also that this mechanism allows the protocol to “capture” most of the revenue from transaction fees, allowing it to be redistributed as the protocol deems optimal (or burned). There are a [number](https://www.cs.princeton.edu/research/techreps/TR-983-16) of [results](http://randomwalker.info/publications/mining_CCS.pdf) that show that block proposer revenue coming primarily from fees leads to high risk of micro-level incentive instability in blockchain protocols. If fees are captured by the protocol, the protocol can distribute the fees to different classes of participants (eg. proposers, attesters), spread the fees out over time, or otherwise more closely replicate a revenue-driven incentive model.

## Replies

**danrobinson** (2018-07-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Note also that this mechanism allows the protocol to “capture” most of the revenue from transaction fees, allowing it to be redistributed as the protocol deems optimal (or burned). There are a number of results that show that block proposer revenue coming primarily from fees leads to high risk of micro-level incentive instability in blockchain protocols. If fees are captured by the protocol, the protocol can distribute the fees to different classes of participants (eg. proposers, attesters), spread the fees out over time, or otherwise more closely replicate a revenue-driven incentive model.

I’m not sure if this has been written up but one advantage of protocol-captured-transaction-fees that’s specific to proof-of-stake is the increased ability to disincentivize censorship in a wider range of mechanisms.

A promising idea for discouraging validators from censoring each other (or censoring inclusion of new validators) is to have each validator’s reward be proportional to the total number of validators participating. Unfortunately this is impossible with a purely inflation-based reward system if the percentage of the tokens staked is close to 100% (because inflation becomes a zero-sum game among validators). If you can capture and burn a percentage of transaction fees, then you can burn them them proportionally to the number of non-participating validators, thus providing an in-protocol incentive for validators to support the inclusion of other validators.

(I think these may be pretty old ideas; thanks to [@benj0702](/u/benj0702) and [@sunnya97](/u/sunnya97) for pointing them out to me).

---

**sylvaingchassang** (2018-07-02):

May I ask: why not just keep a first-price auction, and offer proxy-bidding tools as part of the relevant API?

The FPA has some good properties, and is pretty legitimate. A proxy bid optimizer seems pretty self-explanatory… Bidders submit their value to the bidding tool which then computes a best-reply bid given their value.

Also, if people transact sufficiently frequently, you can use tools from online learning to make sure that your proxy-bidding scheme is robustly optimal. Like make sure that bidders have no regret vis-à-vis bidding lower or higher given the realized residual demand curve.

---

**PhABC** (2018-07-02):

I believe `K` needs to be smaller than 2, otherwise `curBlockFee` could be negative if a miner allows an empty block. This or use a rectified linear function such as `max(0, curBlockFee)`.

---

**vbuterin** (2018-07-02):

> May I ask: why not just keep a first-price auction, and offer proxy-bidding tools as part of the relevant API?

Because bidding algorithms are quite complicated, it’s already proven very hard to get right, and it’s a centralization pressure that can drive users toward centralized custody solutions. It also easily leads to mishaps like people accidentally paying hundreds of ETH in fees.

---

**vbuterin** (2018-07-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> I believe K needs to be smaller than 2, otherwise curBlockFee could be negative if a miner allows an empty block. This or use a rectified linear function such as max(0, curBlockFee) .

Agree fully. I was actually thinking values for k like 0.5. Will clarify.

---

**MicahZoltu** (2018-07-02):

In your proposal you introduce two separate things.  One is the min-fee concept, the other is the min-block concept.  I believe the min-fee concept is not adding any value, and all of the value you gain is coming from the min-block concept.

A client can already calculate (locally) the “min fee” (as you have described) and having everyone agree on the min fee formula doesn’t add any value and instead just calcifies it, preventing people from coming up with better formulas.

The min block proposal does have legs though IMO.  It allows a user to submit a series of transactions with the same nonce and have them replace-by-fee the longer the transaction sits.  As a user, I can submit a transaction with a low-ball price, followed by a medium price 2 blocks later, followed by a high price 10 blocks later.  This allows me to have confidence that my transaction will be mined eventually, while still trying for a lower price.

A potential improvement on this would be instead to have the fee be a user-supplied function based on block number.  So as a user my fee could be something like `block_number - 5900000 * 10^9` if the current block was `5900000`.  This automatically increases my fee by 1 nanoeth every block starting from current block, thus giving me a strong guarantee that my transaction will eventually be mined while still getting me close to the best price possible.  This also reduces the amount of gossip traffic compared to having to submit separate transactions with the same nonce over and over again.  Since we already have the EVM, we could make it so the fee is calculated via supplied EVM bytecode with some tight constraints on gas limits for fee calculation.  That way people can do whatever formula they wanted.

---

**gufmar** (2018-07-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> 0.02, 0.03, 0.05, 0.08, 0.13, 0.19, 1.00

if 0.02 is less or much or 1.00 is cheap or expensive depends mostly on if you live in Zug or Mumbai. So per definition a global fee structure/mechanism/auction is putting people in castes, and favourishing richer regions to have faster transactions, while poor regions have to wait, pray and hope.

The only solution I see - besides a global communism with all people with the same (basic) income - is that certain regions of the world can operate their own “regional” chains with fees that fit into the monetary possibilities of their people.

---

**DB** (2018-07-03):

Not sure I agree this is better on the philosophical level. Looking forward, on a full PoS blockchain, we can let fees be the only source of income for validators (pay to play). At this point, the security of the network is dependent on these fees (more fees - more incentive to act as a validator, harder to mount an attack), so the goal is to keep validator expanses low (no PoW) but fees reasonable. With sharding, the bandwidth also depends on it, as more validators can enable more shards. Minimizing the fees does not support these goals, specifically, users willing to pay higher fees will save money at the expense of lower bandwidth, preventing low-fee transactions from being processed.

Current software already informs of reasonable prices for timely execution. To prevent excess fees, software solutions showing actual ETH/USD prices and warning against unreasonable fees are needed (and to some extent exist). At most, we can limit the maximal fee to the 80th percentile (i.e. cut the top), but I’m not sure even that is needed.

---

**vbuterin** (2018-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I believe the min-fee concept is not adding any value, and all of the value you gain is coming from the min-block concept.

Disagree! The min fee concept ensures that most of the time, blocks are 50% full (or at least, less than 100% full), which ensures that paying one particular fee gives you a very high chance of getting in, and there’s no need to consider lower or higher fees.

I agree that your other approach is also an improvement; that said, I think it’s less effective because it forces people to wait longer to get the fee that they want.

![](https://ethresear.ch/user_avatar/ethresear.ch/gufmar/48/1591_2.png) gufmar:

> So per definition a global fee structure/mechanism/auction is putting people in castes … the only solution I see - besides a global communism with all people with the same (basic) income - is that certain regions of the world can operate their own “regional” chains with fees that fit into the monetary possibilities of their people.

I suppose theoretically, a basic income fund that pays enough to make sure everyone has enough for a few transaction fees shouldn’t be *that* hard…

Practically speaking though, the goal with sharding, plasma, channels, etc is to make txfees low enough that anyone can afford to participate in at least some applications on the blockchain. You could have regional plasma chains I suppose.

---

**gufmar** (2018-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I suppose theoretically, a basic income fund that pays enough to make sure everyone has enough for a few transaction fees shouldn’t be that hard…

definitively not from a technical point of view. The question is how is it meant and what it means for certain people?

Theoretically, If it’s a “real” basic income - in the meaning “enough to eat, stay healthy and buy the basic goods” - then we’re talking about a very fundamental thing and revolution, not just a blockchain and it’s tx fees… theoretically.

If it’s meant as a basic TX funding, automatically distributing a couple of gas units per day to “everyone” (identity who?) in order to pay - let’s say - 5 basic tx per day for free, it looks to me like every general rent subsidy: rental prices grow exactly by that amount.

So - practically - first it would need a move from “work” to something else like “stake” which in principle needs less energy. Then - not having that costs and ROI-goals at miners side anymore - it would need some game-theory rules implemented in the protocol to enforce/motivate minters to process also a certain amount of lower fees (staking allows way smarter incentives then rude raw hash rates).

So instead of giving a basic income to pay TX it should be possible to shorten this path and implement a basic LowCost TX per day per account.

A rich/whale could simply don’t care and continue with his usual TX fees. Or he could use one LC-TX-fee per day to split up his 1000 ETH into 1000 accounts. Then after around 10 days (2^10) he could use 1000 LC-TX per day (for example to to buy low-cost goods or day-trades which wouldn’t make sense because a few normal TX fees would be cheaper and easier to handle for his new Rolex, Lambo and Cote d’Azur holiday), while the normal-Joe owning one ETH can think about using his one LC-TX each day on supermarket, or if he want to split it up into blocks of 500 to 100 Finney’s. The lower limit would be a certain ratio to whatever level a LC-TX fee is defined (“*0.02, 0.03, 0.05, 0.08, 0.13, 0.19, 1.00*”) and also at what currency it’s bound. You used $ in the above example which - beside different wealth levels around the globe - is another factor that can change significantly over time for certain groups of people.

Remember: I put these ideas just on the table and I’m not sure if they were already discussed or if they bring significant drawbacks on other sides. By taking 1-2 steps back and looking at the whole story I see solutions by either finding a very small and tricky path between general low-cost TX-fees and ledger-stability, or by giving different regions the chance to run their regional infrastructure at an appropriate cost level.

---

**MicahZoltu** (2018-07-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The min fee concept ensures that most of the time, blocks are 50% full (or at least, less than 100% full), which ensures that paying one particular fee gives you a very high chance of getting in, and there’s no need to consider lower or higher fees.

As a user, I can already do this by targeting a price that would have gotten into the last `n` blocks plus some.  So if the lowest 50th percentile (gas price per gas in block) for the last `n` blocks was 50 nanoeth, I can simply pay 50 nanoeth and am just as “guaranteed” to get into the next block as I would be in your system.  The difference is that in your proposal I *cannot* choose 49 nanoeth.  The only way I would not get into the next block with such a price is if there was a sudden surge in congestion, which is the same scenario as in your proposed system.

In other words, any formula you come up with for enforcing min-price on a block such that blocks are 50% full could be implemented in each client without any consensus and allow users to still create transactions that are “lazy”.

I think what we are seeing is that people are cheap, but then they get surprised when their cheapness causes their transactions to sit pending for a long time.  Making it so users cannot be cheap just takes away their ability to express their preference for “lazily mined” transactions.

---

**vbuterin** (2018-07-04):

> As a user, I can already do this by targeting a price that would have gotten into the last n blocks plus some. So if the lowest 50th percentile (gas price per gas in block) for the last n blocks was 50 nanoeth, I can simply pay 50 nanoeth and am just as “guaranteed” to get into the next block as I would be in your system.

That’s really not how it works. Gas prices can adjust suddenly, there are difficulties in measuring, demand differs block by block, etc etc. First-price auctions really do put a lot of cognitive (or programming) load on users and wallets end up massively overpaying to avoid harming the user experience.

---

**MicahZoltu** (2018-07-04):

Lets say your proposed strategy is implemented (via consensus) and the min gas price is 10 nanoeth.  Blocks are currently all 50% full, and if you pay 11 nanoeth you know that you will be over the min gas price for the next block, because the min gas price between two blocks can only change by (example numbers) 0.1 nanoeth.

In a parallel universe the proposed strategy was not implemented as part of consensus but instead the exact same logic is used by some (or perhaps all) clients to decide what gas price to recommend to users.  The difference being that instead of looking to see whether the previous block was more or less than 50% full and adjusting min gas price based on that, it looks to see what gas price 50% of the gas spent in the block was at/above and compares that to its previous block gas recommendation and adjusts this block’s gas recommendation up/down by 0.1 nanoeth per block, just as the proposed strategy.

Under normal operations, when gas prices are not swinging by huge amounts between blocks, both strategies give users similar (possibly the same, but there are a few edge cases that I believe may cause the strategies to not be exactly equal) probability of getting their transaction into a block.  In fact, in both cases the user is guaranteed to get into the next block *unless* there is a sudden increase in block contention (e.g., crowdsale start block, poorly implemented air drop, etc.).

In the case of a sudden increase in block contention, both strategies will result in the user missing the next block, despite using a gas price that should be “plenty” to get into a block.  Over the next `n` blocks, the `min_gas_price`/`suggested_gas_price` will increase until such time as it reaches a point where it represents reality and the user can use it to get into the block.

The advantage of the latter strategy IMO is that it isn’t calcified in the consensus protocol and different clients can tune it to react faster/slower to gas price bursts, use different algorithms for calculating the 50% mark, change the block fullness target, etc.

The other advantage of the latter strategy is that it allows users to lowball gas prices and get in “next time there is a block that isn’t full”.  With the min gas price strategy, if the next block isn’t full (or rather, isn’t 50% full) then the min price decreases slightly but the user with the lowball gas price will not get included.  They will have to wait until the min-gas-price decreases all the way to their target, which could take a long time depending on how much they lowballed.

---

**vbuterin** (2018-07-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Under normal operations, when gas prices are not swinging by huge amounts between blocks

Here is a reading of the 90th percentile (ie. 10th from the bottom) of gasprice in gwei in a span of 100 blocks (5500000…5500099):

```
[1, 1, 2, 1, 1, 1, 1, 1, 20, 1, 1, 4, 1, 1, 1, 50, 1, 4, 1, 5,
 0, 1, 1, 1, 1, 1, 1, 1, 0, 2.2, 1, 1, 1, 0.646, 1, 1, 1, 5, 2.2, 1,
 1, 1, 1, 1, 22, 1, 0, 4, 1, 1, 1, 1, 22, 1, 1, 1, 1, 1, 0.646, 0.646,
 1.01, 1, 4, 1, 1, 1, 0.5, 1, 1.01, 4, 1, 5, 2, 1, 1, 1, 1, 6.71, 2, 1,
 1, 5, 1, 1, 1, 1, 1, 1, 5, 20, 1, 5, 1, 1, 5.6, 1, 5, 1, 2, 1]
```

So it definitely is volatile. And it’s volatile because block-by-block gas usage really is volatile. What I’m suggesting would turn that block-by-block price volatility into block-by-block usage volatility, reducing costs and delays for participants at fairly little cost. Also, the median gasprice paid is ~2.8x higher over that timespan, and the average is ~4.9 times higher. So plenty of people are overpaying quite significantly.

> With the min gas price strategy, if the next block isn’t full (or rather, isn’t 50% full) then the min price decreases slightly but the user with the lowball gas price will not get included. They will have to wait until the min-gas-price decreases all the way to their target, which could take a long time depending on how much they lowballed.

Not if you use the version where the user can specify “I’m ok with paying whatever the mingasprice is, up to a maximum of X, plus k%”. Then users really would be able to just fire and forget, and get a guarantee that their tx gets included as cheaply as it can be, unless the price goes above what they are willing to pay.

---

**liangcc** (2018-07-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Second, a block proposer can collude with some portion of transaction senders, asking them to submit higher bids than their “actual” bids, and then refund them through a separate channel.

Thanks for Vitalik’s explanation for how this work today. Contributing back.

[![txfees](https://ethresear.ch/uploads/default/original/2X/c/cf7acb5e420a4ed4382d8834958bf5d162876c29.png)txfees368×291 18.5 KB](https://ethresear.ch/uploads/default/cf7acb5e420a4ed4382d8834958bf5d162876c29)

A miner bribes users who value their tx less than `p1` to pay exactly `p1`. The miner then later refunds the users with `p1 - p2`. So the bribed users pay area `A + B + C` and refunded with `A + B`, and the miner is happy to earn a net revenue `C` from them.

---

**jacob-eliosoff** (2018-07-05):

As a related aside, earlier this year I did some poking at per-block fee auction mechanisms, to address the unpredictability/volatility problems [@vbuterin](/u/vbuterin) mentioned.  My intuition was to treat each tx fee as a “max” fee, and then charge less than that when the sender is egregiously overpaying.  Eg, if a block’s tx fees are:

> 5 5 5 5 5 5 5 5 5 5

then it makes sense to charge them each 5 (“actual” fees):

> 5 5 5 5 5 5 5 5 5 5 (max) →
> 5 5 5 5 5 5 5 5 5 5 (actual)

But if the specified fees are:

> 5 5 5 5 5 5 5 5 5 100

then you’d think the fee logic could just charge the last tx 55 (or 60, or something), rather than the specified 100:

> 5 5 5 5 5 5 5 5 5 100 (max) →
> 5 5 5 5 5 5 5 5 5 55 (actual)

This would reduce the pain of accidentally paying way over the market rate, and thus make life easier and safer for senders.

(Note we can’t charge that last tx *less* than 55, because then the miner is incentivized to drop the other nine txs and just keep the 100.  There are lots of little pitfalls like this…)

Anyway I wrote a bunch of code and stuff but I ended up hitting a brick wall, in the form of the spoofed txs problems Vitalik mentioned: if a tx specifies a fee of 100 and we charge it <<100, the miner is incentivized to insert other txs (to herself) with very high fees.  Eg:

> 5 5 5 5 5 5 5 5 5 100 10000 (max) →
> 5 5 5 5 5 5 5 5 5 100 9855 (actual)

Incentivizing miners to spoof txs, to induce real txs to pay higher fees (bring “actual” closer to specified “max”), seemed kinda fatal for my whole idea, alas.

---

**MoonMissionControl** (2018-07-05):

The gas prices are also volatile because a lot of miners pay their pool participants in the own blocks they mine. The average gas price is around 60 GWEI right now, but a lot of blocks have 1 GWEI lowest transactions in them. These transactions are actually miners paying their pool participants and pay 1 GWEI to themselves for this (from the account which is mining the block). This hence gives a wrong image about the actual gas price of a block. The miners don’t even send a pending txn, they simply queue their own tx’s and then mine them when they found a block.

---

**IkerAlus** (2018-07-05):

The author mentions two fundamental weaknesses. However I believe that there is a third weakness (very briefly mentioned in Example 5.5. of [this paper](https://arxiv.org/pdf/1709.08881.pdf)). I think it is easier to see it from an example:

Let’s assume the bids are:

`0.1, 0.1, 0.1, 0.1, 1.00`

The block producer (or miner) will have the incentive to add only the top bid (1.00) and ignore the rest. Therefore there will be (common) cases where block producers will maximize their profit by ignoring transactions and emptying blocks.

How is the proposed fee market system deal with this weakness?

---

**vbuterin** (2018-07-05):

In my proposed system, no transaction affects the fee paid by other transactions, so the miner has the incentive to accept all transactions that pay more than the minimum.

---

**nootropicat** (2018-07-06):

From a miner’s perspective fee is payment for an increased uncle risk, so decreasing the total received fee must lead to reduced capacity, assuming rational miners.

For this reason the minimum fee system would increase volatility of fees and reduce throughput, as fees would have to be the same as they are currently *on top* off minimum fee. It’s a dynamic tax creating a deadweight loss.

Fees are volatile because high fees don’t increase the gas limit, ie. ‘high’ fees are too low relative to the block reward. The moment fees attain level high enough to buy additional block space the market would stabilize and become predictable.

The simplest solution is to reduce the block reward, which has separate security considerations.

A weird one would be to allow miners to gift a portion of their rewards to *future* blocks, paying future miners to not orphan them.

A hybrid PoS/PoW with PoW chain for validator selection/joins/exist and PoS for block generation would also work.

Fee as a function of time and/or block height is a very good idea, although hypothetically it could incentivize intentional orphaning. The difference is that the current way of replacing transactions hides future pricing information.


*(19 more replies not shown)*
