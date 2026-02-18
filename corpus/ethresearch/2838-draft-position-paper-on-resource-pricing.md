---
source: ethresearch
topic_id: 2838
title: "DRAFT: Position paper on resource pricing"
author: vbuterin
date: "2018-08-07"
category: Economics
tags: [resource-pricing]
url: https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838
views: 34900
likes: 36
posts_count: 40
---

# DRAFT: Position paper on resource pricing

This covers:

- Prices vs quantities
- Social cost curves
- First and second-price auctions
- The adjustable minfee scheme
- Storage maintenance fees
- Why fixed fees are underused in general

Requesting typo checks, math correctness checks, peer review, etc.


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/ethereum/research/tree/master/papers/pricing)





###



Contribute to ethereum/research development by creating an account on GitHub.










[ethpricing.pdf](https://ethresear.ch/uploads/default/original/2X/1/197884012ada193318b67c4b777441e4a1830f49.pdf) (730.2 KB)

## Replies

**androolloyd** (2018-08-08):

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/f49efd6e4c79442486288bf46ef7c86b6b23fe99_2_281x500.jpeg)image839×1491 407 KB](https://ethresear.ch/uploads/default/f49efd6e4c79442486288bf46ef7c86b6b23fe99)

Unsure where you want typo corrects. “Whe” should be “the”

---

**hahnmichaelf** (2018-08-08):

I commented with some grammar and spelling edits

[ethpricing (some grammar edits).pdf](https://ethresear.ch/uploads/default/original/2X/0/0c6d0b1759f055173821eab39777c38c062c1dd5.pdf) (584.8 KB)

---

**vbuterin** (2018-08-08):

Thanks a lot! Just fixed the typos.

---

**anthonyjk2** (2018-08-08):

Word before heading 5 on p14: “dee.” -> “fee.”

---

**ldct** (2018-08-08):

In the last paragraph of section 5 is it the case that for a “fixed price sale” the block producer only collects the fee paid above minFee ? The rest of the section seems to treat fees paid by txn senders (in first and kth price auctions) as being collected entirely by the block producer

Edit: defined on p19. Still think this should be defined just prior to the minFee + epsilon policy comment

---

**vbuterin** (2018-08-09):

Fixed again ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**labrav** (2018-08-09):

A comment to the storage pricing part from an economist with very little computer science background (sorry if I get something wrong): in addition to rent and hybernation, which might still not give the necessary peace of mind for some smart contracts that they will be live forever, without interruption, which might be critically important given the application, you could still maintain the present non-time-based (non-rent, forever, one-time) storage fee system along with the rent-based system at a much higher gas price. That higher one-time gas price could be calculated from extant parameters like the rent and the staking return based on the simple incentive consideration that from a return-on-investment point of view paying a rent should be less costly than the one-time fee, so it would only be resorted to for applications where the certainty of having the storage at all time, no matter what happens, is high. A slightly macabre real-life (…) simile would be how you can buy plots in a graveyard in my country: you can by them by 25-year renewal fees (rent) or forever but for a very high one-time price, making an attractive option available to those who very strongly believe that what happens to their bones in hundreds of years of time matters while maintaining a healthy turnover as far as the other plots are concerned to price in the cost of extending the cemetary :-). This could be useful for continuity/legacy considerations, too, as you maintain a previous option (albeit make it rather pricey), but that is for coders to be concerned with.

Keep up the astonishingly good work!

---

**phil** (2018-08-09):

IMO it’s an interesting idea to consider, but given that the network cost of providing the indefinite storage is directly proportional to the number of nodes on the network, it’s very hard to accurately price into the future such that the price reflects costs to the network.  In a way this is just the same commons model that is subsidizing storage today, just with a higher cost and bounded growth.

If you really need to hedge against market forces 100 years from now, you should be able to buy futures or set up the infrastructure to resurrect if necessary regardless of rent payments, but IMO there’s no other offer of digital storage on an infinite timeline for good reason.  Even Dropbox, who claims to offer this on the face of things, pruned my account after 3 years of inactivity, presumably because they were being bankrupted by the cost of carrying replicated data for users that weren’t actively paying costs (in an ad-based model, an inactive user is the equivalent of an up-front payment).

---

**nootropicat** (2018-08-09):

You wrote elsewhere that you think gas token is a net positive. An explicit gas token with no refund limit (up to negative!) could be traded, allowing people to arbitrage fees that are too low or too high, while keeping the average near the block limit. In contrast to any algorithmic policy like minFee, this would slowly rise fees before eg. a hot ico happens, leading to a much lower volatility overall.

By negative refund I mean a transaction that costs negative gas, ie. it increases the effective gas limit in block.

> That said, note that any transaction pricing policy, whether fee-based or limit-based, necessarily has centrally planned parameters.

Without the gas limit there would be no central planning and fees would react to market conditions.

Although I agree that storage, as long as it exists, has to be treated differently.

---

**phil** (2018-08-09):

I like the simplicity of a marketplace like that, though it does open up lots of market manipulation vectors / black swan events if you parameterize it badly.  You could pretty easily have gas bubbles that cripple the network, and it seems like there would be feedback between gas price in such a scenario and ETH/USD exchange rate (since gas price impacts network usability; I see it as similar to oil price and the stock market, but gas in ETH is a much more fundamental resource than even oil in industrialized economies).

The social cost curve @vitalik has in the paper would probably be argued by a lot of for example Bitcoiners to not be steep enough; at some point large blocks could definitely become catastrophic in PoW, if e.g. censorship results in a network partition.

Most of my comment specifically relies on the difference between UTXO storage and computation.  Storage seems to require rent, computation does not. Computation is a cost paid once by un-checkpointed validating nodes and peers on the network at the time of the transaction, where storage is persistent and must be kept in a fast-access medium for security.  It is an ongoing cost for every actor on the network, so I don’t think the same mechanisms can be used.

Also, just to clarify, I’m far from convinced GasToken is a net positive.  I think GasToken is an important experiment, and something like GasToken could be a net positive.  But there is a lot of modeling to be done before I’d personally be convinced of the optimality of *any* mechanism (even defining what that means is highly nontrivial).

My ideal market for both storage and computation would definitely include limited guaranteed issuance and restrictions on redemption that would enforce the lack of a network-killing capacity spike, and would also attempt to enforce a large percentage of capacity available on the spot market to reduce the profitability of cornering the market.  Limited issuance into the future should allow for enough liquidity to extract useful pricing information and allow for large players to hedge risk while not overselling capacity.

This is all somewhat separate from the “rent” issue though, and whether to have cash-backed extra-protocol futures or computation-backed in-protocol futures is an open question.  I think most would prefer the former for simplicity; curious to hear what people more versed in commodity markets than me think about that.

---

**0xpeter** (2018-08-16):

The second-price auction is a nice, simple mechanism for allocating a fixed set of space. It preserves the same ranking of transaction priority ranking as the current system, is simple from a user decision perspective, and reduces average txn fees vis-a-vis a pay your max offer system.

It is not incentive compatible with the current block miner takes all fees in block model, but it easy to imagine modifying other aspects of fee payment to accommodate auctions. For example, you could allocate x% of txn fees to the block miner and (100-x)% to future (or alternatively preceding) block miners. In this case, the miner must shoulder a portion of fees himself in order to increase the fees paid by others. The second price auction should become incentive compatible for a sufficiently low x. Would want to do some research to establish an appropriate choice of x, but I’m guessing 50% would work.

---

**vbuterin** (2018-08-16):

That doesn’t work; any scheme where anything less 100% of marginal changes to txfees go to block proposers is vulnerable to side channel payment attacks, as users can bribe miners to include their transactions and give miners 100% of the fees.

---

**0xpeter** (2018-08-17):

I understand what you mean by side channel attacks, but I think that the situation is not so simple and that there are at least two Nash equilibria here. Let’s work with a kth price auction, where the k highest fee offers get into the block and everyone pays the kth highest fee offer.

Suppose that the kth transaction fee under the kth price auction is y and thus that the miner receives y/2.

I could obtain get into the block by paying a fee y and a side payment ε, where ε is some small positive number.

Alternatively, I could go by the socially preferred route and get into the block by paying a fee y+ε.

The miner would accept either offer.

Thing get more interesting if I try to issue a side payment in lieu of a portion of the fee.

Suppose I pay a fee y-ε and a side payment ε, so that I am spending the exact same amount as the kth txn, but trying to exploit a side channel. Lowering the official fee reduces the auction price from y to y-ε. This price applies to the preceding (k-1) txns subject to the auction. If the miner accepts this txn he will lose (k)ε/2 via the official channel and gain ε via the side channel. Thus, the miner would not accept the side channel payment if k>2 and all other users are working with the auction. The implication here is that complying with the auction is a  Nash equilibrium. Unfortunately it is not unique.

Suppose that all users offer an official fee of 0 and that the kth side channel payment is y/2. In this case, a user can only obtain entry into the block by offering a side channel payment greater than y/2. Offering a fee will not affect the auction price. So working entirely via the side channel is also a Nash equilibrium. If users are able to collude to work exclusively via a side channel, then they can temporarily reduce fees. Very quickly, however, this would lead to increased txn volumes until the fee reaches something near to and potentially higher than the previous level.

There are lots of additional things to consider here. If the miner can append fees to existing txns rather than create de novo txns where he pays a full fee, this would cause problems.  But maybe the takeaway is that the use of auctions deserves a more thorough treatment in the paper.

---

**0xpeter** (2018-08-17):

On further consideration, I think that auctions are likely to be an improvement even under the scenario where 100% of marginal mining rewards go to the miner. Maybe we should set that idea of spreading the fee over multiple blocks aside. Regardless of whether that would work or not, it is probably unnecessary and the side channel issues add a lot of complexity.

What you are saying in the paper is that it is not incentive compatible to force the miner to auction off all gas available up to the gas limit. Instead, the miner will auction of whatever quantity of gas maximizes his revenue under the constraint that he must sell all gas use in the block at one uniform gas price. I think that’s fine. I believe that this type of auction (miner chooses how much gas to sell) would be a dramatic improvement over the current arrangement.

Essentially what this achieves is movement from a regime of perfect price discrimination by miners to one where mining operates under the law of one price.

Going from price discrimination to the law of one price has the following consequences:

1. The miner gets much less revenue from txn fees and thus is harmed.
2. High value users (rapid txns) will pay a dramatically lower average gas price.
3. Low value users (slow txns) may pay a slightly higher gas price and some activity could be priced out of the market.

In general, it is not possible to say whether the combination of three consequences is socially beneficial or socially harmful. There is a benefit from restricting the miner’s ability to extract rents from users. There is a loss when users are priced out of the market. You need to weigh these two sides and in order to do this one needs to look at the demand and cost structure, which vary across contexts. For gas pricing, I think we are in a situation where restricting miner’s rent extraction yields a large net social benefit.

I peeked quickly at a recent block 6165683. For this block, using an auction to set a uniform gas price would lead to a gas price of 3.011 Gwei for all txns and would not price any txns out of the market, so there would be no dead weight loss. Instead it is just a pure transfer harming miners and benefitting users. Miner fee revenue would drop to about 10% of the current level, with the 90% being returned to high value users. Would need to automate analysis of many blocks to determine how representative this is. I expect there would turn out to be some activity that is price out of the market in some blocks, but that this would be of minimal consequence.

The key consequences would be a huge drop in user costs and a very small % decrease in miner fees (since miner rewards mostly come from the block subsidy).

In short, I think that an auction like this (where each individual miner can choose how much gas to auction off up to the gas limit) is a very promising approach to gas pricing.

Useful link providing background slides on price discrimination:

[http://people.stern.nyu.edu/dbackus/1303/slides_prdisc1.pdf]

---

**jamesray1** (2018-10-03):

Use of a little grammar English checker wouldn’t hurt. I’ll make a pull request.

p. 15, first full para. (2nd para.) + fn. 3: I use ethgasstation’s safe low and am happy to wait for the safe low time, unless of course the fee will be too high to be worth it, as was the case with a [dock.io](http://dock.io) LinkedIn import transaction during an anonymous contract DOS attack a few months back.

“(to provide a slight incentive for the block producer to include the transaction)” p. 16, what’s the point of doing that “If being included in the blockchain simply requires paying some minFee, (which would be burned, rather than given to the miner, to prevent side-dealing between transaction senders and miners allowing free transactions)”.

---

**zawy12** (2018-10-12):

W is number of bytes in block. I assume D is a utility with a value from of decentralization or demand.

[![image](https://ethresear.ch/uploads/default/original/2X/9/9e2b66197a0c2811dea06919a4d5941fbe67a934.png)image673×124 28.9 KB](https://ethresear.ch/uploads/default/9e2b66197a0c2811dea06919a4d5941fbe67a934)

D stops increasing with large block size. A benefit per additional node (marginal benefit) is decreasing with larger blocks, so marginal total social cost is increasing, if R(W) and A(W) were constant.

Pages 5 and 6 are equally confusing, especially since the 2nd derivatives of the plots are all zero.  It’s like the plots are supposed to be marginal (per unit) instead of “cost” which throws the discussion out of whack with the 1974 paper. I would remove the word “marginal” from the paper, do all the math in terms of cost per unit (byte), and make sure everything is expressed as a cost such as “centralization” instead of “decentralization” and “utility loss” instead of “benefit” or “utility”.

I’m not sure the price and quantity controls of the 1974 paper are the same thing as fees (taxes) and cap-and-trade.

---

**clesaege** (2018-11-10):

> (p3) An equilibrium is established where users attach fees to their transactions which go to the validator that includes the transaction in a block, and validators select the transactions paying the highest fee per unit weight.

The equilibrium is not that simple. If we assume the weight of transactions to be known beforehand (like in Bitcoin), the equilibrium would be the validator including the set of transactions paying the highest total fees such that the total weight of accepted transactions is at most the weight limit.

That’s the [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem).

Ex:

Assume a weigh limit W=10 and transactions (under the form (f,w) (fee,weight)):

t_1=(8,6)

t_2=(5,5)

t_3=(5,5)

t_1 has the highest fee per unit, but for miners it’s better to include t_2 and t_3 which will pay 10 instead of 8 by including only t_1.

Just taking the TX with the highest fee per weigh is a greedy algorithm which may produce acceptable results but not optimal ones. I wonder if miners just use the greedy algorithm or effectively run a knapsack to optimize their fees.

Now for chains like Ethereum where the fee per weight (gasprice) is known but the weight is not known before trying execution (not all gas need to be consumed), the optimization seems harder. In particular because the amount of gas consumed by a transaction can depends of the execution of other transactions.

---

**vbuterin** (2018-11-13):

Most transactions in practice have small gas limits relative to the block gas limit, so it’s ok to treat them as being infinitely divisible. IMO we should just use this simplification; if we don’t then the problem becomes far too intractable…

---

**jvluso** (2018-11-13):

In section 9 you describe a scheme for preventing a double waking attack using a `MinInterval`. I think there are design patterns which will want to have contracts that put themselves to sleep in the same transaction that they wake up. This is something that should be encouraged as much as possible - These patterns will require very little storage in the network, and will halve the number of transactions to interact with them because they do not require a separate hibernate call. There is also a different scheme which would use an `EpochLength` instead of a `MinInterval` which would allow these design patterns.

At the end of every epoch of `EpochLength` blocks, a merkle tree and bloom filter of all the awoken contracts would be published. Those could be used, along with the merkle tree / bloom filters of the blocks in the current epoch to prove that the contract has not been awoken since it was last put to sleep. This would result in faster proofs with the bloom filters, and allow design patterns without storage costs.

---

**vbuterin** (2018-11-14):

Yeah, you can certainly do that and it would be slightly more efficient.

In fact, objects in UTXO architectures technically never need to be awake.


*(19 more replies not shown)*
