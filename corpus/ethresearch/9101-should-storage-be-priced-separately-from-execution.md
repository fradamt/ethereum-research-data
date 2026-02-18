---
source: ethresearch
topic_id: 9101
title: Should storage be priced separately from execution?
author: vbuterin
date: "2021-04-05"
category: Economics
tags: []
url: https://ethresear.ch/t/should-storage-be-priced-separately-from-execution/9101
views: 6438
likes: 9
posts_count: 16
---

# Should storage be priced separately from execution?

*Special thanks to [@barnabe](/u/barnabe) for suggesting a similar idea at some point earlier*

As discussed at length in [my older position paper on resource pricing](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838), gas usage in Ethereum actually pays for three distinct kinds of resources:

- Bandwidth (data in transactions that must be downloaded)
- Computation (time to verify and execute transactions)
- Storage (history but more importantly state, eg. account balances, nonces, contract code, contract storage)

Storage is not like the other two costs. Bandwidth and computation are *ephemeral costs*, that brush up against *ephemeral limits*: there is a bound on how much computation or data downloading a node can do within the span of one block, and once that block passes, the effort needed to download and verify that block is mostly gone (only a few syncing nodes will need to process it in the future). Storage, on the other hand, is a *persistent cost*. If a single block increases state size by 100 MB, that block can be processed just fine *in the moment*, but a series of blocks like that for an entire month will render Ethereum entirely unusable. The “burst” impact of heavy state growth is negligible, but the long-term impact is the most severe of all, because a piece of state created once burdens the network forever.

With [state expiry and weak statelessness](https://hackmd.io/@vbuterin/state_expiry_paths), the long-term impact of state will certainly be greatly reduced: instead of burdening the network forever, a piece of state will only burden it for about a year, and even for that year only a smaller portion of nodes would need to actually store that state. But even still, this long-term cost continues to be real, and will continue to need to be priced.

## Average case vs worst case storage size

One of the weaknesses of modeling state, both in the current protocol (broadly agreed to be unsustainable) and the improved protocol with state expiry, is the enormous difference between *average* and *worst-case* state growth. Consider the current protocol. Today, the total size of the state is about 550 million objects, or about 32 GB (not including trie overhead). If we took out all state that was not touched in the previous year, that would easily drop by more than half.

Now, what is the worst case? Contract code creation is charged at 200 gas per byte, so if we split a block into three transactions each of which creates a contract, we can make three 20558-byte contracts for 12334800 gas plus 3 * 55000 gas for contract creation overhead. Thus, in a single block storage size can increase by ~20600 * 3, or 61800 bytes. Assuming an [average block time of  13.1s](https://etherscan.io/chart/blocktime), there’s `31556925 / 13.1 = 2408925` blocks per year, so in total, the state can grow by `~61800 * 2408925 = 148871600381.67938` bytes, or about 138 GB.

This difference, a factor of ~10, is very significant! Particularly, 16 GB can fit within realistic consumer hardware RAM (if not we can tweak gas prices or the state expiry period to make it fit), 138 GB cannot. It would be nice if we could force the worst case to be closer to the average case.

## Dual-track EIP 1559

A natural solution to the problem is to use EIP 1559 pricing for both ephemeral and permanent costs, *but make the adjustment period different*. In the ephemeral case, prices can adjust by over 10% in a single block. For permanent costs, however, we would make the price adjust much more slowly. If we take the [AMM cost curve mechanism](https://ethresear.ch/t/make-eip-1559-more-like-an-amm-curve/9082) as a base, for storage we could consider a curve where the target rate is 1 GB per month, and costs increase depending on how far above the target we are: for example, for every 1 GB over target, storage costs could double. It would take ~3 days of worst-case blocks for the price of storage to double in this parameter. If storage growth were to go 10 GB over target, storage costs would be 1000x higher than normal, making it economically infeasible to fill storage any further.

There are two ways to implement this:

1. Purchase storage with gas. That is, using SSTORE to create a new storage slot would consume gas as it does today, but the quantity of gas consumed would be variable. This has the weakness that it preserves timing mis-incentives (users would prefer to fill storage on weekends when gas prices are lower, despite the fact that this does not benefit the network)
2. Purchase storage with ETH. Transactions (and calls) would be required to supply another resource in addition to gas (we could call it mana ), and this resource would be charged with a similar mechanism to gas, except with different parameters. This has the weakness that it complicates calling rules and requires adding a new CALL opcode.

There are also two hybrid options:

1. We can price storage in ETH, but charge in gas (so if the basefee went up by 2x then the gas needed to fill a storage slot would automatically halve). We can exclude ETH used to expand storage from EIP 1559 gasprice update rules or even the block gas limit.
2. Reform gas more comprehensively, into three concepts: gas, execution points, and storage points. 1 gas = 1 wei; a transaction allocating gas just means that it’s transforming some of its wei into a special form that can be used to pay for resources. This form works the same way as gas in terms of how it passes between calls and subcalls. However, there are now two costs that are managed by the AMM: the cost of an execution point and the cost of a storage point. When the execution processes an opcode that currently costs N gas, it instead costs N execution points, meaning that N * execution_point_cost gas is charged. Filling a storage slot costs 1 storage point, so storage_point_cost gas is charged.

Note also that the state expiry roadmap is expected to remove refunds. This is because for technical reasons storage slots cannot “become empty” and become eligible for a refund; they can only be set to zero, and the zero record has to remain in the state until that epoch ends and the state can expire. This greatly reduces the complexities that plagued [older](https://github.com/ethereum/EIPs/issues/35) [attempts](https://github.com/ethereum/EIPs/issues/87) at storage rent.

## Replies

**mtefagh** (2021-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A natural solution to the problem is to use EIP 1559 pricing for both ephemeral and permanent costs, but make the adjustment period different.

*Transient* and *temporary* price impacts for the *ephemeral* costs and *permanent* price impacts for the *permanent* costs seem like a much more natural solution to me. I get the point of your numerical example but note that constants don’t affect the asymptotic behavior. This means that the effects you get from constants are totally dependent on the numerical ranges.

---

**vbuterin** (2021-04-06):

Post-state-expiry, the costs are not truly permanent (they’re just long-lasting, 1 year to be precise), so price impacts lasting longer than a year doesn’t really make sense. And that’s roughly what an AMM with a slow adjustment rate already does.

---

**mtefagh** (2021-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> so price impacts lasting longer than a year doesn’t really make sense. And that’s roughly what an AMM with a slow adjustment rate already does.

Again, changing adjustment speed does not change the fact that all the currently used AMMs in Ethereum have only implemented permanent price impacts. For example, all constant function market makers remember the cumulative effect of all the previous trades from the beginning of the time unless you manually reset them at some point. Moreover, they only support permanent price impacts as the final price is only a function of this cumulative sum of all the previously exchanged amounts and the initial reserves which together determine the current reserves and hence the current price.

---

**dlubarov** (2021-04-08):

At a high level, this makes a lot of sense! Glad to see this inefficiency being addressed.

As someone who tends to favor simple solutions, I imagined that this could be addressed by just burning a certain amount of ETH per byte stored, at a rate loosely based on the network’s overall storage costs. That would at least remove the timing issue.

I don’t really see a strong reason why long-term state growth needs to stay within a particular range. All other things being equal, it seems best to let storage supply scale with demand; roughly fixing the supply could lead to storage being under- or over-priced relative to the network’s actual costs.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> 16 GB can fit within realistic consumer hardware RAM (if not we can tweak gas prices or the state expiry period to make it fit), 138 GB cannot

This is an interesting point, but in practice it seems like caching a small number of frequently accessed accounts (and keeping the rest on an SSD) gives good enough performance. It looks like Parity’s default account cache is just 25mb.

---

**realisation** (2021-04-08):

You could design a constant product AMM to have a virtualized price attenuated by a time weighted average reserves which would have the effect of slowly migrating the price and retaining price depth while doing so - i.e. a trade of 10% of the pool would yield the correct slippage you’d expect from a standard constant product trade, but the next trade would start from only a few basis points or whatever calibration above the initial point of the previous trade, rather than the 10% adjustment.

---

**mtefagh** (2021-04-08):

This time-weighted average reserve that you mentioned is exactly an instance of the *transient* price impact that I suggested in my first comment ![:+1:t2:](https://ethresear.ch/images/emoji/facebook_messenger/+1/2.png?v=9)

---

**vbuterin** (2021-04-08):

> in practice it seems like caching a small number of frequently accessed accounts (and keeping the rest on an SSD) gives good enough performance

It actually doesn’t! The problem is that you need to be able to survive not just regular usage but also worst-case DoS attacks. And a DoS attack is going to focus on accessing the *least recently accessed* storage slots (or even outright empty slots) to be as painful as possible.

I agree there’s some nice simple properties of a fixed price, but I think the costs of highly unpredictable storage size are too high; essentially, nodes need to make sure they have enough disk space for the worst case scenario but then in actual reality most of that space will almost never end up being used.

---

**imkharn** (2021-04-12):

Seems like there is a single issue: appropriate pricing of miner hard drive space. Yet 2 mechanisms are proposed to solve the same issue. To me this implies there is a way to combine or have only one mechanism to solve. e.g. either state expiration alone has enough impact, or variable storage cost is designed to have enough impact by itself, or the two can be combined into a single mechanism.

Regarding the combined, have you considered setting the state expiration epoch length by GB instead of time per epoch?

With light consideration, my proposal is to have 1GB epochs, and require miners to keep 12 epochs. In this case I am considering a target of 1GB per month with current hardware. Then a constant product curve adjusts the storage cost each 1 GB possibly settling at a rate of less than 1 month per GB with storage costs higher than they are currently, or if you don’t allow for any elasticity just endlessly increment the storage cost until usage is always eventually brought back in line to 1GB per month. Also, perhaps include a GB/month natural growth rate similar to Moore’s law, but modeled after expected RAM growth in consumer laptops.

---

**vbuterin** (2021-04-12):

> With light consideration, my proposal is to have 1GB epochs, and require miners to keep 12 epochs. In this case I am considering a target of 1GB per month with current hardware.

The problem with this is that witnesses for resurrecting old state become 12x bigger.

---

**GustavHAlbrecht** (2021-04-12):

Different pricing for execution and storage makes perfect sense to me. One argument against increasing the gas limit is a larger state growth. So one should limit state growth by introducing a “block storage gas limit”. Often blocks have fewer transactions because they require the SSTORE operation, which costs a lot of gas. But why shouldn’t these blocks contain even more transactions that only consume computing power? It would help to scale a little bit.

Regarding the pricing of such a resource i just note that it is impossible to achieve a constant price as the gas price moves and a fixed gas solution (like paying a fixed amount of ETH) doesn’t work as the price of ETH changes.

---

**imkharn** (2021-04-12):

I doubted that my example proposal numbers had the correct tradeoffs, but the point is to spur thought about the idea of epochs being measured in GB instead of time. I chose 1GB to allow the price to update more often. It could continuous instead with 12GB epochs on a target of occurring once per year where the storage price along the way varies in attempt to meet the year target.

The witness size would be less than 12x for recoveries less than 12 epochs of time into expiration. Two epochs into expiration would only be 2x witness. Either way more frequent epochs should increase witness size. Makes me wonder though:

Is it possible for witness size to be reduced by running through multiple epochs of history while acting as if the protocol had a longer epoch time? For example, if epochs were one month, and expired in 6 month batches, that batch could be rolled up by a miner into a multi epoch that will only take a single witness to recover from before erasing those 6 months from hard drive.

---

**Mister-Meeseeks** (2021-04-23):

Conceptually, I think there should be a third resource type distinct from gas. The closest real world analogy would be “land”. Gas is a good metaphor for computation or bandwidth, because it’s  consumed to make something happen. But land is the better mental framework to think about storage.

Practically speaking, here’s how I imagine it would work. Land comes in two flavors: “developed” land which is attached to current storage and “undeveloped” land which is a fungible resource and is used to pay for new storage. Deleting storage turns developed land back into undeveloped land, which can be used for storage later. Every address has a non-negative balance of undeveloped land, which starts at zero.

Land is created at a fixed rate per block. The land rewards would go directly to the miner, the same way that block rewards currently do. The land reward size would be chosen based on the targeted state space growth rate of the network. This assures that storage requirements never grow faster than a pre-determined rate.

Because undeveloped land is fungible, unlike gas, users don’t need to purchase it directly from the miner. Therefore that avoids the need to build land pricing into the protocol layer. That avoids all the complexity of having two resource prices in each transaction, or needing to build in a AMM at the protocol layer. Miners would be free to sell land rewards in whatever marketplace they wanted.

When a transaction calls a storage operation, the caller will need to supply land. The simplest approach would be for the caller to send land from his own address. However smart contracts could also own land. DApps would most likely handle this by maintaining their own internal “land bank” and/or going to external “land brokers” (external marketplaces that sell land) as needed.

This gives the application layer the freedom to experiment with different land marketplace structures, instead of hardcoding a storage marketplace at the protocol layer. In practice most ordinary users will never have to worry about buying or pricing land. DApp authors will transparently handle land mechanics inside their application code. Periods of high storage demand will be accommodated by land speculators that buy-and-hold during periods of low storage demand.

This also encourages much more careful state management than the current delete gas refund mechanics, which is barely used for its intended purposes. The problem with that prudent deletion only benefits the transaction sender in the form of lower gas, and the vast majority of those users are unsophisticated. By making land a fungible and persistent resource, DApp authors will be highly incentivized to delete storage, because they can profit by selling the reclaimed land.

Finally this scheme is nicely extendable to notions of recency and access cost. Land could be sub-divided into types based on “zoning”. Storage that’s frequently accessed could be created with high activity “zoned land”, which would give lower gas costs for read operations. Vice versa for infrequently access storage. When needed storage could be “upzoned” by swapping out land types.

Thoughts?

---

**mohamedmansour** (2021-04-26):

I like this proposal! Shouldn’t storage be ephemeral, for example coupling storage with expiration should be together. This is to eliminate hogging storage at early prices, causing rent seeking behavior.

---

**thatbeowulfguy** (2021-04-27):

With EIP-3298, how might someone hog land and “squat”?

If the full state is land, and using that land is ephemeral, are we back to something land produces (ie mana)

---

**samueldashadrach** (2021-09-21):

This post doesn’t focus much on pricing of calldata versus state - is this intentional?

