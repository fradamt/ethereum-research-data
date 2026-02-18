---
source: ethresearch
topic_id: 6399
title: "Another simple Gas fee model: The \"Escalator Algorithm\" from the Agoric Papers"
author: danfinlay
date: "2019-11-01"
category: Economics
tags: [fee-market]
url: https://ethresear.ch/t/another-simple-gas-fee-model-the-escalator-algorithm-from-the-agoric-papers/6399
views: 10710
likes: 22
posts_count: 44
---

# Another simple Gas fee model: The "Escalator Algorithm" from the Agoric Papers

It seems the Eth community may have missed some valuable prior art, from 1988 by Mark Miller and Eric Drexler:

https://agoric.com/papers/incentive-engineering-for-computational-resource-management/full-text/

The premise is simple, resembles current patterns emerging in the eth ecosystem, reduces network traffic, and results in a highly efficient gas market.

You can think of it as “[spectrum transactions](https://medium.com/authereum/gas-spectrum-transactions-bd34b65107b)” in a single message (if you’re familiar with those).

## Proposed change

- The gasPrice field is now optional, but if missing must be replaced by the following fields:
- firstValidBlock: The first block this transaction is valid to be processed on.
- minGasPrice: The lowest price a person is offering to mine their transaction, eligible on firstValidBlock.
- gasIncreasePerBlock: A gas price increase per block.
- maxGasPrice the ceiling gas price that this transaction can be processed for.

Effectively, this allows a person to determine the max price and the max time that they would like to wait for a transaction, and ensures they get a fast and cheap transaction otherwise.

This image shows a hypothetical price market over time:

[![gas price market](https://ethresear.ch/uploads/default/original/2X/0/042795efa4c2680d644bc66386cd2984a70293f8.gif)gas price market340×290 4.22 KB](https://ethresear.ch/uploads/default/042795efa4c2680d644bc66386cd2984a70293f8)

The various triangles represent various transactions waiting for the current highest offered price to lower to them, at which point they “break through” the ceiling and are processed.

I just thought it would be valuable to put this out there for consideration, since there is active discussion on improved gas price models.

## Replies

**vbuterin** (2019-11-01):

I’ve thought about such ideas before. I think it still offers higher wait times in practice than EIP 1559, which most-of-the-time guarantees inclusion within one block.

---

**danfinlay** (2019-11-01):

This “most of the time next block” claim would seem to depend on the network not usually being congested. If we imagine a state where there are always three times as many pending transactions as can be processed, it seems clear to me that most of these will not be in the next block under any gas model.

Instead, my impression is that eip 1559 trades market efficiency for price consistency, and is only justified when measuring “overpayment of what would have been mined”, but changes the definition of “what would have been mined” to be more expensive (by the base fee), and so actually there is overpayment still, in the form of high prices during low congestion.

I’m not saying this is definitely better, just trying to highlight tradeoffs.

---

**vbuterin** (2019-11-02):

> If we imagine a state where there are always three times as many pending transactions as can be processed, it seems clear to me that most of these will not be in the next block under any gas model.

But under EIP 1559 such a situation is impossible. In the long run, you cannot have more than 50% of blocks that are full, because if more than 50% of blocks are full then on average the basefee will be increasing, so it will keep increasing until blocks stop being full. And that’s a pathological case where the blocks that are not full are completely empty; if we OTOH model transactions as a Poisson distribution, then only ~13% of blocks would be full (and if we set max = target * 3 instead of max = target * 2, that drops to ~5%).

> Instead, my impression is that eip 1559 trades market efficiency for price consistency

Strongly disagree! As I [argue in my original paper](https://ethresear.ch/t/first-and-second-price-auctions-and-improved-transaction-fee-markets/2410), EIP 1559 *improves market efficiency by increasing price consistency* because prices being more consistent than the supply-consistency-maximizing model (ie. fixed block sizes that are generally full) provide is the efficient thing to do!

---

**danfinlay** (2019-11-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> But under EIP 1559 such a situation is impossible. In the long run, you cannot have more than 50% of blocks that are full, because if more than 50% of blocks are full then on average the basefee will be increasing, so it will keep increasing until blocks stop being full

Sorry if I’m missing something, but seems like there’s a hard ceiling, the blockchain bandwidth, which prevents endless gas limit escalation.

---

**AFDudley** (2019-11-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> if we OTOH model transactions as a Poisson distribution

It’s these sorts of assumptions seem extremely dangerous to me. Without the capacity to do more than hand wave about the impact of the changes, I don’t think it much matters which proposal we use. I’m far more concerned about having a sane model to test our assumptions against than what the proposed changes are… these changes seem extremely difficult to reason about without simulations of some sort.

---

**hammadj** (2019-11-02):

I can definitely see the need for / value of “opting in” to defer transactions for applications/use cases that don’t necessarily need things to be mined ASAP. What about a hybrid approach where we combine the good parts of each? Allow for  specifying those custom fields for applications/users that want to, and for the rest have the dynamically adjusting value like in 1559.

---

**vbuterin** (2019-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> Sorry if I’m missing something, but seems like there’s a hard ceiling, the blockchain bandwidth, which prevents endless gas limit escalation.

It’s *gas price escalation*, not gas limit escalation that I am talking about here.

> these changes seem extremely difficult to reason about without simulations of some sort.

What kind of simulations would help here? Getting a reading of the probability distribution of transactions that get included in the chain and their gas limits, so that we can try running it against EIP 1559 and see how often blocks are full? I would certainly love to see the output of that!

---

**danfinlay** (2019-11-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It’s gas price escalation , not gas limit escalation that I am talking about here.

Oh right, I can’t believe I still make that mistake sometimes.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What kind of simulations would help here? Getting a reading of the probability distribution of transactions that get included in the chain and their gas limits, so that we can try running it against EIP 1559 and see how often blocks are full? I would certainly love to see the output of that!

Yeah, that may be very helpful, although it’s hard to know what people *would have been willing to pay*. Maybe someone can suggest a reasonable way of approximating that from what was paid.

I guess I may be an outlier here where gas price efficiency/volatility seems like a feature to me, because it allows prices to reflect actual demand, but I’m happy to separate opinions like that from the things we can build concrete data on, like possible simulations.

---

**vbuterin** (2019-11-03):

> because it allows prices to reflect actual demand

I disagree that EIP 1559 makes this no longer the case! The BASEFEE continues to give readings of what the demand level is. In fact, I think EIP 1559 *strengthens* the extent to which observed prices reflect demand, because it solves the attack where miners manipulate observed fees by including high-gasprice transactions to themselves (as with EIP 1559 that attack becomes very costly). Plugging that hole also allows smart contracts to automatically use gasprice info, enabling eg. gas price derivatives.

Probably the one piece of information we lose is how much people are willing to pay to get their tx included 1 min earlier, but then delaying people’s transactions by 1 min is almost always a pure social waste in the first place so that doesn’t seem like too big a deal.

> Maybe someone can suggest a reasonable way of approximating that from what was paid.

If you want estimates of how the demand curve works, there is this analysis from exogenous shocks to the gas limit: [Estimating cryptocurrency transaction demand elasticity from natural experiments](https://ethresear.ch/t/estimating-cryptocurrency-transaction-demand-elasticity-from-natural-experiments/2330)

---

**dankrad** (2019-11-05):

Just to jump in here: My impression is that the misunderstanding comes from two different views of the capacity of blockchains. [@danfinlay](/u/danfinlay) assumes that the main capacity is a hard limit, say bandwidth/computation limit of nodes at any instant in time. However, EIP1559 assumes that the limit is more to do with the overall size/computation of the chain, and a temporary increase of resource usage even by a factor of 3-4 is acceptable if the average bears this out. These two viewpoint impose different cost models (instant vs average prices).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Probably the one piece of information we lose is how much people are willing to pay to get their tx included 1 min earlier, but then delaying people’s transactions by 1 min is almost always a pure social waste in the first place so that doesn’t seem like too big a deal.

So EIP1559 will ensure a good pricing model for all those participants that want their transactions included immediately. This is great as long as it does not become too costly. In the context of Eth2.0, where more fixed block sizes (at least in terms of the data availability/custody story) will mean that some resources will be wasted, it would be very interesting if there is a model in which you can allow for cheaper transactions that would only be included in “block waste”, and are likely to be included somewhat delayed. My gut feeling is that it’s probably impossible as it would break the incentives of EIP1559, but maybe there is a clever way to circumvent this.

---

**vbuterin** (2019-11-05):

> In the context of Eth2.0, where more fixed block sizes (at least in terms of the data availability/custody story) will mean that some resources will be wasted

This is why the block roots are stored as lists of chunks representing 128 kB each; this removes most of the inefficiency that arises from this.

---

**dankrad** (2019-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This is why the block roots are stored as lists of chunks representing 128 kB each; this removes most of the inefficiency that arises from this.

I’m talking about the partially filled 128 kB chunks. If we could fill them, that would be almost “free”. Of course that’s difficult. Maybe one idea would be to have a transaction type that is always executed with a 10 block delay, at half the price. But how to get the rewards for block proposers right, that is the problem.

---

**danfinlay** (2020-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think it still offers higher wait times in practice than EIP 1559, which most-of-the-time guarantees inclusion within one block.

Revisiting this claim, as I think we talked past each other before, and I’ve re-read all your content on this issue:

I’ll concede that “most of the time” many algorithms may work fine, and so I think much of my motivation comes from how the protocol would perform under various types of strain (I recommend talking to wallet devs who supported users during the various 2017 booms).

If we imagine a large backlog of transactions whose submitters have widely varying preferences of the highest price they would pay, then I think it should be simple to prove that:

Under 1779:

- The very highest bidders’ transactions may wait a number of blocks until the BASEFEE increases to a level that excludes other transactions, making the tip a sort of single-price auction within each block that reproduces all the problems of the current market but with the additional complexity of this one.
- Once the price has increased to a point where the highest price transactions are cleared, and the BASEFEE is going to lower again, the lower-priced transactions remaining will need to wait additional blocks for the price to fall to be eligible for inclusion.

Under the Escalator algorithm:

- The highest bidders’ transactions would be cleared as quickly as possible, and then the lower-priced transactions would be processed. No block lag to discover price, no unfull-blocks-with-pending-transactions, and only one or two parameters would need to ever be shown to the user (cap and max_duration).

---

**vbuterin** (2020-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> The very highest bidders’ transactions may wait a number of blocks until the BASEFEE increases to a level that excludes other transactions,

Miners would still accept transactions with the highest tip first before the BASEFEE rises to new-equilibrium levels, so I don’t think the property that highest paid transactions get included first gets sacrificed.

> Once the price has increased to a point where the highest price transactions are cleared, and the BASEFEE is going to lower again, the lower-priced transactions remaining will need to wait additional blocks for the price to fall to be eligible for inclusion.

What’s the model here? An instantaneous spike of transactions, way too large to fit in one block, with a wide distribution of fee levels? It’s definitely true that lower-priced transactions will have to wait, though I think you have to be careful with the analysis: while the gas/block will be <10m as the basefee climbs down, the gas/block will be 20m while the basefee is climbing up, and that would reduce the wait time for lower-fee txs by as much as if not more than the extra delay on the way down.

---

**moodysalem** (2020-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> making the tip a sort of single-price auction within each block that reproduces all the problems of the current market but with the additional complexity of this one.

This feels like a salient point. What value does the base fee add over completely user-specified gas prices? The fee already dynamically adjusts via supply (block gas limit) and demand. The user just can’t adequately express the fee they wish to pay with a fixed price.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> while the gas/block will be <10m as the basefee climbs down, the gas/block will be 20m while the basefee is climbing up

It seems like this desired stretch capacity could be achieved in some other way. E.g.: You could allow miners to include transactions in excess of the block gas limit by burning the fee. This would effectively compensate other miners for their CPU by deflating ETH.

---

**danfinlay** (2020-04-13):

By the way, I’ve posted this as an EIP here:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2593)














####


      `master` ← `danfinlay:Escalator`




          opened 01:08AM - 11 Apr 20 UTC



          [![](https://ethresear.ch/uploads/default/original/3X/a/3/a3d334102b3048180496eddd2da152520318fd38.jpeg)
            danfinlay](https://github.com/danfinlay)



          [+131
            -0](https://github.com/ethereum/EIPs/pull/2593/files)







Submitting a draft of a version of the escalator algorithm applied to the Ethere[…](https://github.com/ethereum/EIPs/pull/2593)um network, which I suspect has superior qualities to EIP-1559 in several regards.

Opening this PR so that the algorithms can more easily be compared side by side.

Full text available for easy reading here:
https://github.com/danfinlay/EIPs/blob/Escalator/EIPS/eip-x.md

You can read some previous discussion on it here:
https://ethresear.ch/t/another-simple-gas-fee-model-the-escalator-algorithm-from-the-agoric-papers/6399

---

**vbuterin** (2020-04-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Just to jump in here: My impression is that the misunderstanding comes from two different views of the capacity of blockchains. @danfinlay assumes that the main capacity is a hard limit, say bandwidth/computation limit of nodes at any instant in time.

Yeah, my original paper that proposed EIP 1559 was very explicit about this: it had as a key assumption that the costs of shifting some capacity between T and T + 5 minutes or T - 5 minutes are not high. The main argument for this is basically:

1. Uncle rates are at  E.g.: You could allow miners to include transactions in excess of the block gas limit by burning the fee.

So basically have an EIP-1559-style basefee that only starts kicking in for blocks with >=10,000,001 gas? That seems unlikely to be correct; what’s the rationale for why the marginal cost to the network of adding one unit of gas is zero below 10m but suddenly spikes up above 10m?

> The user just can’t adequately express the fee they wish to pay with a fixed price.

The user definitely can express the fee they wish to pay; that’s what the fee cap is for.

---

**dankrad** (2020-04-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Yeah, my original paper that proposed EIP 1559 was very explicit about this: it had as a key assumption that the costs of shifting some capacity between T and T + 5 minutes or T - 5 minutes are not high. The main argument for this is basically:

I wonder if it’s even true if it’s not about minutes but hours or days. At least at the moment, I don’t think that the bottleneck is current bandwidth at all; the bottleneck seems to be trying to sync nodes that have been offline for a long time. And they don’t even care if load is shifted by a day or two.

The reason I’m bringing it up is that there is the narrative that EIP1559 is useless because it would not have prevented fees spiking on “black Thursday” ([x.com](https://twitter.com/paddypisa/status/1254465123248418818)). Of course, that’s not at all an argument against EIP1559 in it’s current form – but could we have allowed larger blocks for a few hours or even days in order to keep fees much lower?

In other words, is there a possibility to adapt the time constants in EIP1559 to make it smooth over linger timescales?

---

**danfinlay** (2020-04-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> My impression is that the misunderstanding comes from two different views of the capacity of blockchains. @danfinlay assumes that the main capacity is a hard limit, say bandwidth/computation limit of nodes at any instant in time.

Oh hi, I didn’t address this. I think this is a mischaracterization of my concerns with EIP 1559. Rather than implying I believe in a fixed capacity blockchain, I think you could more accurately say I believe in a finite-capacity blockchain with occasional dramatic spikes in usage that exceed that capacity, during which users have transactions of varying value and varying urgency.

In my opinion, EIP 1559 does not gracefully account for varying urgency, and so during a high usage spike that exceeds the network capacity for a number of blocks (a scenario that is rare but happens, and when it happens there is heightened importance), some users with high urgency transactions will find themselves waiting for transactions with much lower urgency, unless they begin manipulating the `tip` parameter, which re-introduces much of the complexity that EIP-1559 is designed to avoid.

I cover this comparison in detail in [the EIP I opened](https://github.com/ethereum/EIPs/pull/2593).

---

**dankrad** (2020-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> In my opinion, EIP 1559 does not gracefully account for varying urgency, and so during a high usage spike that exceeds the network capacity for a number of blocks (a scenario that is rare but happens, and when it happens there is heightened importance), some users with high urgency transactions will find themselves waiting for transactions with much lower urgency, unless they begin manipulating the tip parameter, which re-introduces much of the complexity that EIP-1559 is designed to avoid.

But you seem to engineer for this one very specific usecase (getting in high urgency transactions) without addressing everything else that EIP1559 does. EIP1559 actually makes sure that the amount of times blocks are full is very small, so this should be an exceedingly rare situation, whereas with your algorithm, this would still be the case most of the time (assuming a future network that is well used and so there are always low-value transactions that could fill up any “cheap” capacity).

It seems that your idea would be more of a possible extension of EIP1559: If blocks are full (as in actually 100% full), then you can add an escalating tip to your transaction to indicate it’s urgency. This seems to be much better than your proposal (but I don’t really know if it’s worth it because blocks being full for more than a few blocks can’t really happen in EIP1559 unless someone wants to pay through their nose for it).


*(23 more replies not shown)*
