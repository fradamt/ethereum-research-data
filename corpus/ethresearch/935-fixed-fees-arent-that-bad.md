---
source: ethresearch
topic_id: 935
title: Fixed fees aren't that bad
author: vbuterin
date: "2018-01-28"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/fixed-fees-arent-that-bad/935
views: 8618
likes: 15
posts_count: 24
---

# Fixed fees aren't that bad

I think the cryptoeconomics research so far has an unwarranted aversion to cryptocurrency-denominated fixed transaction fees, at least in cases where the fees are for payment of a resource that does not have short-term moment-by-moment congestion effects (ie. things like long-term storage, NOT things like bandwidth, computation and IO costs of verifying a transaction in a block).

The easiest intuitive explanation for this aversion is simple: volatility. If you think the “just right” fee for some expense is $0.1, and ETH is currently $1000, then you might want to set the fee to 0.0001 ETH. But what if ETH then rises to $10000? The cost would rise to $1, which might make the blockchain too expensive. Or if ETH falls to $100, the cost would fall to $0.01, possibly inviting too much spam.

In the past, transactions fees have appeared reasonably stable, and have definitely risen slower than prices have in the long run. [BTC fees](https://bitinfocharts.com/comparison/bitcoin-transactionfees.html) stayed close to $0.05 all the way through 2013 until part of 2016; the ETH gasprice dropped from 50 to 20 then 4 as ETH prices rose from $1 to $10 then $300. I think that this gave many people, myself included, the false impression that transaction fees can be counted on to be stable, when in reality the stability was only there because blocks were not full and the main mechanism persuading miners to lower their minimum transaction fees was community political pressure, and this kind of politics actually worked, at least until blocks became full.

Now that blocks are full, however, transaction fees are **even more volatile** than cryptocurrencyp rices. BTC transaction fees increased by a factor of [over 40 within 4 months](https://bitinfocharts.com/comparison/bitcoin-transactionfees.html#6m), and Ethereum’s [average gas price](https://etherscan.io/chart/gasprice) in the last 6 months has been similarly volatile. Fees often rise or fall by a factor of 2-4 within a single day, and short-term spikes from ICOs have been even worse.

Hence, compared to current variable transaction fees, charging fixed fees in ETH may actually be a beacon of stability. Sure, if you set a fee now to target $0.1, and the ETH price rises by 10x, fees will increase to $1, and that resource on the blockchain will be more expensive than you had wanted. But if you set the fee in gas, and *interest in using Ethereum* increased by 10x, then fees will themselves rise by as much, and much more chaotically so.

How might fixed fees look in practice? Suppose that we were to market the Ethereum state as “the world computer’s hard drive”, and we determined that it would have a maximum possible storage of 120 TB. Suppose the maximum possible total supply of ETH was 120 million (ie. after full proof of stake it’s capped). Then, in order to create a contract that fills up one kilobyte of space, you would need to lock up 0.001 ETH. This would be true regardless of what the price of ETH is. If you later empty the contract, the ETH gets freed. I don’t necessarily advocate this kind of pseudo-rent-via-lockup, but this is one way to show what the mechanism would look like and what effects it would have.

Note that “diagonal” policies that specify ETH-denominated in-protocol fees, but have the fees start very low and then rise with usage, are also possible (I call these policies diagonal because you can interpret a block size limit as presenting a vertical supply curve, and a fixed in-protocol fee as a horizontal supply curve, so something in the middle would be diagonal; the simplest possible diagonal formula is where the in-protocol fee is proportional to the amount of existing usage).

**Objection**: but isn’t this “price fixing” and thus socialist central planning that will lead to poverty and breadlines?

**Answer**: unless you are willing to charge literally zero fees and allow unlimited usage of a resource, *any* other policy represents some kind of central planning, including the status quo of a vertical supply curve. The protocol offering a horizontal supply curve or a diagonal supply curve is not ipso facto more “central plan-y” than the protocol offering a vertical supply curve, though fundamental uncertainty is definitely a good argument for not trying to make the supply curve any more complex, so as to avoid accidentally overfitting to present conditions at the expense of future unknown unknowns.

This is also not the same thing as price fixing, because price fixing refers to attempts to control the price at which sellers sell to buyers, whereas this is a single virtual seller (the protocol) simply using the power that it already has to sell the resource that it controls to buyers, and we are debating the best way for this virtual seller to set the conditions.

That said, if you want to really try to reduce the number of economic variables set in stone in the protocol as much as possible, then you should really love the [stateless client proposal](https://ethresear.ch/t/the-stateless-client-concept/172), as it essentially marketizes the role of permanent storage, saying that it’s a user’s own responsibility to store and maintain witnesses (or delegate this task) for any accounts they care about.

## Replies

**SRALee** (2018-01-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> compared to current variable transaction fees, charging fixed fees in ETH may actually be a beacon of stability. Sure, if you set a fee now to target $0.1, and the ETH price rises by 10x, fees will increase to $1, and that resource on the blockchain will be more expensive than you had wanted. But if you set the fee in gas, and interest in using Ethereum increased by 10x, then fees will themselves rise by as much, and much more chaotically so.

Great post, I think the quoted part of your post above is the key that made it click for me and will probably be for many other people. Since most users of ethereum currently calculate their sunk costs in dollars/floating national currencies (for using any kind of limited resources in their lives such as food as well as the EVM space) this proposal seems fairly counter-intuitive unless you phrase it like you did above, where the volatility/uncertainty of the gas price is channeled through ethereum interest over time and not the pair value of ETH:USD. The former of which is much, MUCH more stable and growing and fairly predictable rates, the latter of which is always compared to a roller-coaster ride (and rightfully so). In fact, it could even be argued that the ETH:USD trading pair of ETH is mainly a function of speculation of the integral of all future adoption of ethereum and this estimation has a much wider range than the actual real life curve of adoption. With that said, it could be an uphill battle to get a sufficiently large part of the ethereum community to accept such a flat rate gas proposal since most people are used to calculating their sunk costs in USD rates, but great, insightful post as usual. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**Etherbuddy** (2018-01-28):

Currently, variable fees are very useful to avoid congestion of the network. When the network is overloaded, fees get higher.

In the future, under full POS and good scalability, I think every account should have a free rechargeable reserve of gas (gift of Ethereum), enabling a few free transactions every day.

As a result, ordinary users would enjoy a fixed fee of 0.

The free gas would be financed by a little bit of inflation, made easily possible since there would be no more inflation due to POW, and because each year a percentage of cryptocurrencies are lost due to private keys losses, bugs, hard drives problems …

---

**nootropicat** (2018-01-30):

There are two fundamentally separate fees here: for storage and runtime validation (ie. network bandwidth+validation time). The latter is inherently variable and making it fixed would be absurd, eventually leading to external fee markets where users directly pay stakers/miners the true market price. The former is currently tied to the variable cost which indeed doesn’t make much sense. So they would have to be explicitly separated - ie. only fixed fees for taking up storage.

I agree with the idea of a fixed storage cost. Fixed limits aren’t inherently bad, they are only bad if treated religiously as holy constants never to be changed lest we desecrate the blockchain.

Transaction size absolutely shouldn’t be included in it - you probably didn’t meant that - as under PoS’ ‘weak subjectivity’ storing sufficiently old blocks is fundamentally pointless. Imo it’s practically pointless even in PoW with utxo commitments/state root as a long-range 51% attack would destroy the network anyway.

**These storage fees would have to also apply to accounts - nonces are problematic.** Nonces can be used as storage because past accounts with balance history can’t be deleted currently; so either each account eats some weis permanently or old empty accounts with non-zero nonces have to be deleted after a set amount of time (ie. their nonces are reset to zero).

(Nonces can be accessed in contracts by passing in a state root of a recent block)

> How might fixed fees look in practice? Suppose that we were to market the Ethereum state as “the world computer’s hard drive”, and we determined that it would have a maximum possible storage of 120 TB. Suppose the maximum possible total supply of ETH was 120 million (ie. after full proof of stake it’s capped). Then, in order to create a contract that fills up one kilobyte of space, you would need to lock up 0.001 ETH.

That seems too high to me - imo it’s not likely that anything above 0.01% of the total supply would be locked in for storage. Additionally storage technology has gone 3d and physical size limits are astronomical; 15TB SSDs already exist today. Why not 12PB? Still way, way more expensive than external storage - 10.48ETH per GB vs ~$1.2/GB per year on ec2, rather than 1048ETH with 120TB total. High enough so that nobody is going to waste it pointlessly.

![](https://ethresear.ch/user_avatar/ethresear.ch/etherbuddy/48/586_2.png) Etherbuddy:

> Currently, variable fees are very useful to avoid congestion of the network. When the network is overloaded, fees get higher.
>
>
> In the future, under full POS and good scalability, I think every account should have a free rechargeable reserve of gas (gift of Ethereum), enabling a few free transactions every day.

That’s already going to be the case because staking accounts would earn fees proportionally to their share, so effectively their owners get free transactions for staking, just in a roundabout and stochastic way.

You were probably thinking of EOS but they are doing it in a really stupid way as (afaik) there’s no way to pay any fees if you want more than your ‘share’. So if I want to make a $100 worth of transactions in one day I would have to own (eg.) $100k worth of EOS? Absurd.

---

**gititGoro** (2018-01-30):

I really like that you emphasized that a protocol ALWAYS sets conditions, nullifying the central planning assertion. However, pricing isn’t just about rationing total supply. Variable pricing also allows the market to auction off scarce supply to the most ***urgent*** uses. This function is arguably more important than the total rationing argument.

In the case of capped fees, how would the miners(validators) correctly know which transactions to drop? Would it be simple FIFO?

I can imagine a black market of fees emerging. Perhaps miners could take side payments from certain addresses in return for prioritizing those addresses.

---

**vbuterin** (2018-01-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/gititgoro/48/404_2.png) gititGoro:

> Variable pricing also allows the market to auction off scarce supply to the most urgent uses … In the case of capped fees, how would the miners(validators) correctly know which transactions to drop? Would it be simple FIFO?

Fixed fees only work if they’re rationing a resource that does not have short-term scarcity (ie. only long-term scarcity), so if there’s a spike in usage it simply accepts everyone. Think of Ethereum state storage as one example; nobody cares that much if it goes up by 500 MB in a day, as long as it doesn’t do that *every* day.

---

**jamesray1** (2018-02-02):

You need to internalize the costs of storage somehow, or get others to take responsibility for it.

> How might fixed fees look in practice? Suppose that we were to market the Ethereum state as “the world computer’s hard drive”, and we determined that it would have a maximum possible storage of 120 TB. Suppose the maximum possible total supply of ETH was 120 million (ie. after full proof of stake it’s capped). Then, in order to create a contract that fills up one kilobyte of space, you would need to lock up 0.001 ETH. This would be true regardless of what the price of ETH is. If you later empty the contract, the ETH gets freed. I don’t necessarily advocate this kind of pseudo-rent-via-lockup, but this is one way to show what the mechanism would look like and what effects it would have.

This seems more reasonable than the current fee structure. The question is whether there will be any issuance, or not, but it seems like you are leaning towards no issuance.

https://twitter.com/VitalikButerin/status/955488317025419264

There’s a lot of comments on this topic in this thread as well:

https://twitter.com/VitalikButerin/status/957400121557307392

---

**jamesray1** (2018-02-02):

> I can imagine a black market of fees emerging. Perhaps miners could take side payments from certain addresses in return for prioritizing those addresses.

Good point, not sure how you’d prevent that completely, it seems like you can’t.

But you need to have variable fees for runtime validation (ie. network bandwidth+validation time), and fixed fees for storage.

> There are two fundamentally separate fees here: for storage and runtime validation (ie. network bandwidth+validation time). The latter is inherently variable and making it fixed would be absurd, eventually leading to external fee markets where users directly pay stakers/miners the true market price. The former is currently tied to the variable cost which indeed doesn’t make much sense. So they would have to be explicitly separated - ie. only fixed fees for taking up storage.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[Against replacing transaction fees with deposits](https://ethresear.ch/t/against-replacing-transaction-fees-with-deposits/940/1)

> Markets will exist whether you want them or not
> If you give an agent the power to choose from a list of transactions which ones to include in the next block, transaction senders naturally have the incentive to bribe that agent to make sure they get in first. The genius of traditional blockchains is that they simply accept this effect as a given, and even deliberately formalize it into the benign market of transaction fees. But even if you don’t “officially” put a transaction fee field into the transaction data format, underhanded ways to pay transaction fees will inevitably appear.

---

**jamesray1** (2018-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/nootropicat/48/258_2.png) nootropicat:

> old empty accounts with non-zero nonces have to be deleted after a set amount of time (ie. their nonces are reset to zero)

This has already been done with EIP 161 (State trie clearing).

---

**nootropicat** (2018-02-02):

Are you sure? The way it reads it’s only about clearing accounts with a nonce of zero. I read it before writing the previous post and understood it that way.

“An account is considered empty when it has no code and zero nonce and zero balance.”


      [github.com](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-161.md)




####

```md
---
eip: 161
title: State trie clearing (invariant-preserving alternative)
author: Gavin Wood
type: Standards Track
category: Core
status: Final
created: 2016-10-24
---

### Hard fork
[Spurious Dragon](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-607.md)

### Parameters
- `FORK_BLKNUM`: 2,675,000
- `CHAIN_ID`: 1 (main net)

### Specification

a. Account creation transactions and the `CREATE` operation SHALL, prior to the execution of the initialisation code, **increment** the **nonce** over and above its normal starting value by **one** (for normal networks, this will be simply 1, however test-nets with non-zero default starting nonces will be different).
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-161.md)

---

**jamesray1** (2018-02-02):

Ah yeah, I overlooked that, you said non-zero nounces, that only refers to clearing accounts with zero nonces, no code and no balance.

---

**waldercong** (2018-02-03):

I think the problem with fixed fees in this context is basically as stated: you’re going to have to keep “fixing” them as the underlying economics change or pricing will be completely out of whack.  I wouldn’t try to engineer rigid stability in pricing.  But I do think the economic forces could be modified slightly in a couple of ways to produce more favorable results for both the miners and those utilizing the EVM.

The blockchain users setting gas prices, and the miners choosing which gas offers to include in their blocks is a very efficient ruleset to manage supply and demand equilibrium.  On the surface, it achieves the maximum value for including data on the blockchain while allowing for fluctuation in the price of Ether.  More demand for space and processing on the EVM translates to higher prices for providing it.  Space on the chain is basically always valued at what it is worth.

But there are several factors that create an inefficiency in the market forces between miners and transaction prices, because it assumes equal knowledge, visibility, and understanding of the EVM to create a

First, Ethereum has a problem from Econ 101: There’s a Diamond-Water paradox.  Diamonds are basically useless (don’t tell my girlfriend), and water is essential for survival.  But diamonds cost more, because they are rare.  However, if water became rare, it would be infinitely more valuable than a diamond, even if there was only one diamond left on earth.

In Ethereum’s context, getting a transaction included in the next block is the diamond.  Getting a transaction processed eventually, is the water, and a sustained large transaction pool makes it scarce.  When the transaction pool is manageable, and there is reasonable confidence that a transaction will get processed at a lower gas price, eventually, even if it takes a while, then users will feel fine setting lower bids if they have confidence their transaction will get there eventually.

But a sustained transaction pool backlog with only gas prices above X ever getting through creates the potential for stuck transactions that may never be included in the EVM.  While it is possible to overwrite a pending transaction with a higher gas price if it gets stuck, it’s not exactly the most user-friendly thing to do (or common knowledge).  That “fear” of losing a transaction because of the gas price creates a soft advantage for miners that I could argue is an imbalance to finding efficient market equilibrium for gas prices.  There is also a “visibility” advantage for miners that creates an imbalance: Miners can see the transaction pool and choose the best prices for inclusion into their blocks.  Users can (technically) see the pool as well, but a retail user doesn’t really have the tools or know-how to do a probability analysis on the probability of their transaction processing within a given period… so, most probably take the average gas price and add a little to it.

The more users that do that from pure lack of visibility, the more gas prices will rise above a true equilibrium where both sides of the market have transparent access and usability to its economics.  That dynamic methodically creates a “new normal” price floor for gas that consistently increases as people accept it.  That also gradually moves Ether from something to transact immutable applications with into a pure store of value, and in my opinion, deteriorates the EVM value-proposition with each sustained increase in gas pricing (e.g. it might be worth $0.50 to pay the network to process a transaction between a taxi driver and a passenger for an $8-dollar ride from A to B to skip the 20% markup from the middleman.  But if that’s going to cost $8 + $8 in gas + some time to hang out in the car while that transaction is mined, put in a block, and confirmed… then the “blockchain puts Uber out of a job and lets the taxi drivers work with the customer directly” value proposition pretty much breaks.

I think that the basic dynamics of how the gas mechanism works with the EVM is “theoretically” an almost-optimal ruleset for pricing the EVM’s finite resources over time, and it would be really good if we could assume that both users and miners have equal technical expertise, visibility into the transaction pools, and the same depth of understanding of the protocol.  But I think it is more “perfect on paper” and less “perfect in practice.”  Because right now, miners can programmatically determine which transactions to include ranked by highest value, while users are making their bids for transactions with limited information and usually by hand.

To improve the market dynamics without making authoritative changes and opinions to the protocol related to price, I think there’s a few things that could be done to help softly encourage better gas pricing behavior.

The obvious ones are already being worked on: increasing transaction bandwidth and decreasing storage costs (i.e. sharding, POS, state channels, plasma).   Any/all of those increase the “supply” of “processing power” and “storage” on the blockchain, which makes the resource less constrained.  More capacity means transactions can be included in a reasonable amount of time with a lower cost.

But, the concept of “setting your own transaction fee” is kind of a very knew paradigm for users coming to blockchains from the old world.   As mentioned previous, I would theorize that the learning curve and fear associated with it is contributing to inefficiency in gas pricing for EVM resources that is nor reflective of efficient market pricing.

A non-protocol-changing path to help improve efficiency is to encourage wallets to make some improvements to their transaction functionality and support gas bidding and cost-savings as a primary feature set.

Most wallets provide a suggested value for gas prices, but they are generally very vanilla.  Web3 initiated transactions usually rely on the DApp to provide both the limit and cost, often static.

**For wallets:**

Provide probable transaction times for a given gas amount relative the pool and recent history would help.  Wallets will sometimes suggest a good gas price to get the transaction included, but for a user, it would be useful to know that 20 Gwei will most likely get it in with in 2 hours, 40 Gwei in 20 minutes, 1 Gwei might never be included, etc… so they can value the time appropriately.

Wallet providers could create a pool of transactions as a pre-pool that contributes transactions to the pool when the pool is low, or gas rates fall below a threshold, and allow transactions to be cancelled on their end if they haven’t been broadcasted yet without requiring on an overwriting transaction (and gas) to nullify a previous transaction.

Basically, increasing visibility and bidding utility for retail EVM users at the wallet and user experience level could definitely help gas prices find smoother equilibriums.

**At the protocol level (time-delayed gas increases):**

I think adding a time vector would even the playing field as well, and allow for more efficient market gas price negotiations.

For example, adding an additional variable that can modify the gas price relative to blocks mined passed the transaction broadcast block could help efficiency in gas pricing.

For example, a user could sign a transaction with:

> (gasPrice: 10, gasGrow: [gasIncr,blockAmount,blockNum])

Which can be interpreted by the protocol as authorization to increase the gas price over time as blocks are mined.  Where “gasIncr” = Gwei/gas to add, “blockAmount” = the number of blocks to add it after, and “blockNum” =  the block that starts the increasing gas amount.

So, as a transaction requester, I could send a transaction saying something like “I’m willing to pay 10 Gwei for gas, but I’m willing to increase that bid by 1 Gwei for every 10 blocks that my transaction is not included passed the current block number).

As blocks are mined, that transaction becomes more valuable to a miner and more likely to be included.  But if the network has a low period, the transaction will be processed to fill blocks.

This allows for a user to send a transaction through with the knowledge that it will eventually be included, without worrying about whether it will never be included and requiring an overwrite transaction.  I believe this would encourage lower gas bids uniformly and make the pool smoother by more efficiently recognizing “time” as a variable in the gas market dynamic.

**At the protocol level (Block Locking Transaction Validity):**

Another augmentation to the transaction data similar to the above would be to allow the transaction to invalidate itself at a block height in the future.

Allow a broadcaster to sign a transaction “I want to send X to Y” but “Only if it’s done before block Number Z.

If Block Number > Z, the transaction can’t be included in a block and is expunged from the pending pool.  Which effectively poisons the transaction if it takes too long.

A mining pool may choose to prioritize soon-to-expire transactions in the pool if its known that future blocks may not be filled.

At the protocol level (3rd party Gas Attachments to Transactions):

This may be on the roadmap or an EIP but allowing a 3rd party (e.g. a wallet service) to set and pay for gas on a transaction would open the door to allowing wallet providers to use their nodes on behalf of users to even the playing the field with the miners.  This could open some more wallet business models and allow a wallet node to “mass negotiate” with gas prices instead of passing user-chosen prices along and inflating the price.

**At the protocol level (Swim Lanes for Gas Bids):**

This is basically an authoritative change to the protocol that creates an opinion on gas pricing to ensure transactions will eventually be processed without necessarily required fixed pricing.

The idea would be to require each block to contain a % of gas cost in transactions below a Gas-Price threshold to create a fast lane and slow lane.

So, for example, in order for a block to be valid, it must contain at least 20% of the block’s gas limit with transactions priced at 1 Gwei.

This would basically make the pending pool into two pools: 1.) Transactions that are bidding for inclusion as quickly as possible, 2.) Transactions that don’t care when they are added, but care that they ARE added eventually.

This is not elegant and would need more thought, because there may not be enough transactions that low, it creates more overhead in validation, etc.  But the basic idea is to get to a point where ANY transaction will EVENTUALLY be included to solve the Diamond/Water problem.

**At the protocol level (Network Gas Payments with Respect to Time):**

Similar to allowing transactions to increase gas bids over time, the protocol itself could augment gas prices to make them more attractive to miners by adding gas to transactions as they age.  This could easily be abused, but again could help prices find and stabilize toward equilibrium if a user can opt to pay a small amount to know their transaction will be included, and further know they won’t have to pay more as the protocol will account for the cost in time, over time.

**At the protocol level (Using Broader “Bands” for Gas bids):**

This is similar to Swim Lanes, and may sound counter-intuitive, but removing flexibility in the market making aspects of the gas/miner relationships could yield more efficient pricing.

Right now, a transaction can bid whatever it wants in Gwei for a unit of gas.  So, by outbidding another transaction by 1 Gwei, it can be a make or break it decision for a transaction and spell the difference between inclusion soon, inclusion eventually, and never being included.  Because gas price bids can be done in any increments, it creates a natural inflationary pressure on the constrained EVM resource, which is good for miners, but not great for transaction gas prices.

By requiring “Bands” of Gas pricing, the protocol can make the choice to “bid higher” more significant.  For example, instead of being able to outbid another transaction by pricing gas at 1 more Gwei, the bands could be required to use 10 Gwei increments.

This will take all the bids between 10 Gwei and 20 Gwei (11, 12, 13, 14…etc.), and force them to choose up or down.

That choice and consolidation of transactions onto bands makes it so more transactions are priced evenly, which allows them to be picked up randomly by miners at the same price level instead of stack prioritizing Gwei bids against each other and causes inflationary pressure.

It’s kind of like if we were all in line for a sandwich shop, and the sandwich shop allow us all to bid on who got their sandwich first.

The most-hungry of us will bid high.  The rest of us will see each other’s bids and try to outbid each other based on how much we’re willing to spend and how hungry we are.  But since we can all see each other’s bids, it can be super attractive to add just “One more $0.01” to our bid to jump ahead of the next guy in line.

If we had to choose between $10 for a sandwich, $20 for a sandwich, and $30 for a sandwich, the choice to “bid higher” has much more meaning.  Those of us fine with $10 for a sandwich but would have paid a little more to get it sooner would just queue up in line for the $10 instead of raising the price.  Those of us who were SUPER hungry would just opt for $20 and shorter line/pool.  And the wealthy guy trying to get his sandwich so he can get into that sketchy ICO faster will opt for the $30.

But basically, the point is, that if prices can be economically banded more together, it will remove that inflation creep on gas when the bid consideration is more painful.

**At the protocol level (Randomization Rewards for Block Transactions):**

Last idea, and then I’m done.  But another way to get some more transactions processed and help control gas price inflation is to grant some “bonuses” for transactions included in blocks that fit some criteria relative to the block.  This is an extension of the protocol helping to cover low gas prices.

*Something simple would be:*

If the first 30 transactions in the block can be filled with transactions at GWei price equal to their transaction number, the protocol will price them at all 40 Gwei.

*Or:*

The protocol will double the gas price on transactions included that have transaction hashes that end in the same value as the previous block hash.

Many ways to do it, but what this could do is make break apart the pure GAS/Mine market into a dynamic where higher gas bids increase the probability of the transaction being included sooner, but there are factors that would bring a low price in sooner, and as all of the above suggestions, would guarantee that any transaction could and will eventually make it in over time.

---

**vbuterin** (2018-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/waldercong/48/484_2.png) waldercong:

> I think the problem with fixed fees in this context is basically as stated: you’re going to have to keep “fixing” them as the underlying economics change or pricing will be completely out of whack

This is quite plausible, but then gas limits have the exact same issue. I see no reason why the same mechanism that adjusts gas limits can’t be used to adjust fixed fees.

---

**kladkogex** (2018-02-04):

If one looks at the real life economy, there are both restaurants where you pay for each meal (poor customers), and all-you-can-eat restaurants (rich customers). There are pay-per-night hotels (poor customers) and timeshares (rich customers).

So one can argue that both economic models may be OK under some conditions.  The question is in which case which model works better.

For a network like Ethereum where the resource (TPS) is extremely scarce, and users are TPS-poor,  charging gas makes lots of sense. On the other hand for things like Filecoin or Golem, where the resource is overabundant, making things simple using the shared-ownership paradigm may make lots of sense …

EOS guys are saying they will have 10,000 transactions per second or several hundred million transactions per day.   May be they think that in this case the resource is overabundant and shared-ownerships model may be used. If you want to get to thousands of transactions per second,  gas accounting itself may become a performance bottleneck.

---

**waldercong** (2018-02-05):

I would agree that it’s the exact same issue in being a fixed constraint requiring an evolution mechanism, but I don’t think the same mechanism works for both separate issues.  The mechanism that adjusts gas limits may not be as appropriate for fees because it governs a supply constraint that affects the complexity of transactions types more than it affects the propensity for an EVM transaction requester to engage in a transaction.  It’s a supply rule, not a pricing rule–and pricing is more dangerous in this context and directly affects the economic balance of security and usability (too low, the network loses witnesses/protection, too high, the network loses transactions and utility).  While under PoW, hash power would probably move away from the EVM when fees are trending lower, which would consolidate power more at the same time transactions would be increasing from lower pricing (I do think there is a price elasticity effect in transactions which is hard to detach from network growth right now).  Less of an issue with PoS though.

I think my general point was that there’s two groups sharing the EVM and making a market under its resources: miners and transactors.  But its like playing a game of poker where the miners can see everyone’s hand, the next cards drawn from the deck, and then set the pot limits in every game.  If the transactors have capabilities and tools (either from improving interfacing technology or at the protocol) to be more informed and on an even playing field with the miners at each transaction, the problem could find a scale-able market solution without necessarily requiring additional influence by the protocol creating overt opinion’s on pricing.

For example, in the gas limit mechanism, we are expecting miners to react to the market forces of both groups and choose whether to increase it or decrease it accordingly.  Transaction creators are a proxy-group that influences that dynamic that with demand, but do not have a direct or overt authority.  A philosophical change in how that governance is deployed could be to consider EVM usage a valid contribution to the ecosystem and a first-class opinion on how its constraints may change over time (i.e. consider gas payments from transactors as a financial input into the ecosystem to use it on a similar level as miners devoting hash power or staking to secure it).

So, even if there was a “gas limit-style mechanism” for fixing but modifying gas prices over time, would still suggest that the transaction creators have an overt influence on its behavior to keep it in line with both sides of the market.

---

**vbuterin** (2018-02-06):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If you want to get to thousands of transactions per second,  gas accounting itself may become a performance bottleneck.

AFAIK this is absolutely not true; gas accounting overhead in both EVM and EWASM seems to be less than 10% or so. Also, gas accounting is still required even if you have a N-per-day fee system, as you have to make sure that transactions are not exceeding their limit.

> EOS guys are saying they will have 10,000 transactions per second or several hundred million transactions per day.

With sharding we get that too ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

That said, I still think that equilibrium fees will be in the $0.0001 to $0.01 range, where it still makes sense to create second-layer fee market protocols. If all you can eat restaurants allowed food sharing with non-customers (ie. all you can take-out), they would definitely break quite quickly.

---

**jacob-eliosoff** (2018-04-01):

I still think both fixed-in-ETH fees *and* tied-to-tx-fee fees are horrendously volatile/directional by any reasonable standard.  When the option is available, say via oracles or a working stablecoin, better to specify fixed values (fees, rewards, payment rates, …) in fiat terms (USD, IMF SDR, …) than in any crypto unit: they may still need to be tweaked sometimes, but much less often and urgently.

Of course very low-level values like block rewards may remain impractical to tie to fiat this way.

---

**bharathrao** (2018-04-22):

Fees are sensitive to marginal capacity. i.e. when tx space is close to full, fees will rise dramatically. We see this in commodity markets all the time. This is because a small number of desperate users will pay anything for urgency. Once these users are satisfied, price also drops drastically. This is the reason markets are unstable when prices move fast and sharp price moves up lead to deep retractions.

From an adoption viewpoint, fixed fee dramatically simplifies cost models and will accelerate adoption. However, fixed fees are only practical when the resource is abundant, ie, we never reach the margins of capacity. An example of well executed transition to fixed pricing from history: phone calls in the pre-internet era cost $0.25 domestic USA/Canada and up to $3.25 internationally. Once VOIP took off, the capacity exploded and flat pricing became practical.

Lets say with plasma/sharding we greatly increase capacity. While this pushes us towards making flat pricing practical, the flip side is that flat pricing will bring in huge amounts of new use cases which will eat up capacity. Therefore, we need to calculate what’s the abundance minimum for flat pricing to be practical.

I think it would depend a lot on price tiers. At $0.10 for example, we could assume 10 tx/day/person for 1 billion users. We would therefore, need 10 billion tx/day capacity. This capacity would not be reached of course, but is essential to prevent black marketing and other distortions that a forced price would precipitate. For a flat fee of $1.00, the number of transactions could be 1/10th of it since many use cases would be priced out. On the other side, $0.01/tx would bring in the IOT market which would require another couple of orders of magnitude capacity.

---

**jamesray1** (2018-10-03):

Fixed fees with a stablecoin are better than fixed fees with a volatile coin.

If you use a stablecoin, there is at least greatly reduced volatility, making it easier to [more closely approximate or equal the value of rewards to the true utility payout](https://twitter.com/VladZamfir/status/1014882947781087233), while having less need to dynamically adjust the rate of the reward, as will be the case with a much more volatile coin, which adds more complexity to design and implementation. With a volatile coin, to dynamically get the price you would need to use a price oracle to collect data from various decentralized and centralised exchanges in order to at least approximate the market price. Conversely, if you have a fixed rate of reward denominated against a volatile coin, then the true utility payout will actually not be (near) constant, which will be bad for validators, full nodes, etc., as well as for users and the whole network due to nodes being less likely to stick around due to uncertainty.

Compendium:

> Maker DAO a stablecoin that uses a utility and governance volatile MKR token, for holders to use in governing the DAI stable coin
> Havven: another stablecoin that involves issuing tokens against a distributed collateral pool. James Ray’s opinion: this seems simpler than DAI, while also intuitively seeming to be more desirable. See e.g. this Twitter thread for a related perspective.

---

**MaverickChow** (2018-10-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Answer: unless you are willing to charge literally zero fees and allow unlimited usage of a resource, any other policy represents some kind of central planning, including the status quo of a vertical supply curve.

Why can’t tx fees be determined from a % of the amount of ETH being transacted, regardless of the USD price of ETH?

For example, if I am sending 1 ETH and if the tx fee is 0.001% then the fee would be 0.00001 ETH. And if I am sending 1000 ETH, then the fee would be 0.01 ETH. Not only is this technically logical, it is also impartial to fiat value as the sender will only incur 0.001% fee for whatever the amount being transacted in whatever denomination he chooses, thus practically fair.

And that % can be determined from factors like your memory storage space example and this adjusts automatically on its own to future expansion and contraction, for example a sudden increase of storage space or sudden reduction of the same for whatever the reason be it due to nano tech or nuclear fallout.

---

**mratsim** (2018-10-08):

A transaction has a fixed cost to the network, the fact that there are 3 more or less zeroes will not cost more compute power.


*(3 more replies not shown)*
