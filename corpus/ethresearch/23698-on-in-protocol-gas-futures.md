---
source: ethresearch
topic_id: 23698
title: On In-Protocol Gas Futures
author: Julian
date: "2025-12-19"
category: Economics
tags: []
url: https://ethresear.ch/t/on-in-protocol-gas-futures/23698
views: 286
likes: 4
posts_count: 5
---

# On In-Protocol Gas Futures

*Thanks to Barnabé Monnot, Caspar Schwarz-Schilling, and Charles St. Louis for feedback on this post.*

Blockchain users must pay gas fees to transact. Variation in gas fees leads to bad UX. Users of Ethereum need to have funds set aside in case fees spike and businesses take fee volatility into account when deciding where to deploy. These problems are very real and have come up repeatedly over the years: Ed Felten, founder of Offchain Labs and Arbitrum, mentioned fee volatility as a problem for L2s in a [talk](https://www.youtube.com/watch?v=JfaxBythV4Q&list=PLTLjFJ0OQOj5PHRvA2snoOKt2udVsyXEm&pp=iAQB) in 2022, and Barnabé Monnot [describes the problem](https://barnabe.substack.com/p/understanding-rollup-economics-from) around the same time. [Arc](https://www.arc.network/litepaper), Circle’s planned chain, [Arc](https://www.arc.network/litepaper), argues price volatility is exacerbated by ETH price volatility. Finally, Vitalik’s recent [tweet](https://x.com/vitalikbuterin/status/1997279838252531823?s=61) inspired this post:

[![vitalik_tweet](https://ethresear.ch/uploads/default/optimized/3X/7/0/707fb6531b507fd83e98301b1bff4c58c47286bb_2_500x500.png)vitalik_tweet2160×2160 425 KB](https://ethresear.ch/uploads/default/707fb6531b507fd83e98301b1bff4c58c47286bb)

Markets for future blockspace are clearly desirable. Many parties have tried to structure a product to achieve it. I have chatted with around a dozen individuals and companies that tried to launch such a product. Still, we don’t have it today. In my 2022 posts on structuring blockspace derivatives ([here](https://paragraph.com/@julianma/structuring-blockspace-derivatives) and [here](https://paragraph.com/@julianma/next-block-base-fee-options-towards-a-practical-implementation)), I point out two main reasons why these products are hard to create:

1. The majority of the gas fee proceeds, the base fee, is burnt. No party will receive base fees in the future, as a result, no party that has a natural long position on gas futures. Therefore, only speculators can supply the short side of gas futures. Because the base fee is burnt, gas futures only shift risk from one party to another instead of reducing overall risk.
2. The base fee is manipulable. EIP-1559 sets a rule that determines the next-slot base fee price based on the current slot’s gas usage. Holders of gas futures could manipulate the base fee to their benefit.

In this post, we explore how EIP-1559 is the core cause of these problems and sketch a possible solution. In summary, EIP-1559 and gas futures are two mutually exclusive tools that try to solve a similar issue: improving predictability of fees. EIP-1559 does so for the current slot whereas gas futures would do so for any slot. To allow gas futures, Ethereum would need to remove EIP-1559 and create in-protocol gas futures market. The main contribution of this post is a sketch for such an in-protocol gas futures market.

## Incompatibility between EIP-1559 and Gas Futures

Gas futures require a buyer and a seller. There is clear buyer demand for these products as mentioned before. L2s would want to buy blob futures, users, dapps, and wallets may want to buy regular gas futures. The problem is that there is no seller of these financial products because no single person receives the gas fees, instead they are burnt. Speculators would need to step in to provide these products which has not happened yet despite repeated attempts.

Perhaps you could even prove that EIP-1559 and gas futures are incompatible. We attempt to do so, very informally, with a proof by contradiction. EIP-1559 satisfies three properties: users pay no more or less than the base fee, proposers accept any transaction that pays the base fee, and users and proposers cannot profitably collude. For those familiar with Tim Roughgarden’s [paper](https://arxiv.org/abs/2106.01340) related to EIP-1559, these properties are DSIC, MMIC, and OCA-proofness respectively.

Suppose, for the sake of contradiction, that base fee futures exist. There is a holder of the future who paid some price for it previously and will now receive some amount of blockspace at no additional cost. The seller of the derivative was previously paid by the buyer and must pay for the blockspace today.

Consider the special case in which the proposer is the holder of the base fee future. You can interpret this as the case in which base fees are not burnt but given to the proposer. Normally, the proposer would not accept a transaction that pays less than the base fee. However, if it’s also the holder of the base fee derivative, it could sell the base fee derivative to the marginal user even if their maximum willingness-to-pay is less than the base fee.

By selling the gas future to the marginal user, the proposer at least gains the marginal user’s willingness-to-pay which is higher than zero even if lower than the base fee. This is a profitable collusion between the proposer and user to include a transaction below the base fee price, breaking Roughgarden’s OCA-proofness, and therefore the base fee.

Even if not the proposer, but some other entity holds the base fee future, the holder could sell to a user who wants to include their transaction for some value. The sale happens even if the price is below the base fee. Therefore, a functional base fee derivatives market would defeat EIP-1559’s properties, but today EIP-1559 prevents a functional base fee derivatives market.

To create a functional base fee derivatives market, I believe EIP-1559 must be materially changed. Ethereum could go back to a first-price auction as it had before EIP-1559 was implemented. Then proposers know they will receive the gas fee proceeds and could be sellers of gas futures. There are two problems with this: First, it depends on proposers opting in to becoming gas futures sellers. Ensuring the market has large proposer adoption is a difficult cold-start problem. Secondly, the futures could only be sold up to about 13 minutes in advance as it is unknown who would be the proposer before then. Such a market would not provide certainty to builders deciding where to deploy their application. For a proper gas futures market, Ethereum needs to implement it into the protocol itself.

## In-Protocol Gas Futures

In this section, we assume for simplicity that no in-protocol transaction fee mechanism exists and sketch how a gas futures market may work. In the last section we discuss the interaction between a transaction fee mechanism, which allows regular users to submit transactions, and the futures market.

An in-protocol gas futures market has three phases.

1. Primary Market. Futures for gas units of slot N must be initially sold from the Ethereum protocol to users, for example, in slot N-k.
2. Secondary Market. Participants who bought futures in the primary market may want to trade gas futures, we call this the secondary market. The protocol must keep track of who the futures holders are.
3. Settlement. The gas fee future holder must be given access to blockspace.

We sketch how these three phases may look.

*Primary Market.* Futures must initially be sold in slot N-k. The sale could occur via a system contract on the execution layer. Potential buyers send orders with the form `(bid_per_gas, units_of_gas)` where `bid_per_gas` is the amount of ETH the user is willing to pay per unit of gas future they receive and `units_of_gas` is the amount of gas they want to receive. The system contract then runs an auction to allocate to the highest bidders.

*Secondary Market.* When the futures have been issued and have initial holders, they can start freely trading. Two things that may need to be tracked during trading are 1) public keys of holders and 2) market price per unit of gas. Public keys of holders allows the system contract to deliver the inclusion list proposing rights. This is in principle only necessary at the end so instead of continuously tracking this as holders change, it could be possible that holders are only updated just before block N. The market price per unit of gas may have to be tracked in-protocol to help a transaction fee mechanism as described in the *Other Considerations* section.

*Settlement*. Holders of gas futures must receive access to blockspace for the units of gas their futures represent. Ethereum could provide physically settled gas futures by giving future holders access to blockspace for the units of gas they hold futures for. This could for example be done by giving a holder of 10M worth of gas futures the right to propose an inclusion list of 10M units of gas. This is similar to the [IncluderSelect](https://paragraph.com/@julianma/includerselect-leveraging-external-incentives-in-focil) proposal which allows people to buy the right to become an includer in [FOCIL](https://eips.ethereum.org/EIPS/eip-7805). IncluderSelect works by letting anyone send an execution layer transaction that specifies how many units of gas the user needs and how much they are willing to pay per unit of gas. A system contract takes these bids as inputs and outputs which users receive what size inclusion list proposing rights.

## Other Considerations

The goal of this post is to get a temperature check on whether Ethereum may consider a drastic change to its transaction fee mechanism from EIP-1559 to a gas futures market. It leaves important details like the auction settlement out of scope. Still, we highlight some important future considerations here.

*Spot Transaction Inclusion.* To buy futures in both the primary and secondary market, buyers must be able to get their transactions on-chain. More generally, many users today do not care to hedge against gas fee volatility and may want to send their transactions to the public mempool for inclusion as they do today. To allow both regular users and futures buyers to interact with Ethereum, it may be necessary to sell less gas fee futures than there is gas in the block. For example, if the gas limit is 60 million gas units, 30 million could be sold in a futures market and the other 30 million could be filled up with regular user demand. Ensuring that the prices for both forms of inclusion are in tandem with each other is a hard problem that requires careful transaction fee mechanism design.

*Why futures?* Users may want to hedge their exposure to gas fees via other instruments than futures. I believe offering standard futures is the best fit for Ethereum though since it matches the delivery via inclusion lists. Moreover, offering futures in the primary market allows traders to structure different products in the secondary market. It is a well-known result of finance, [the put-call parity](https://www.investopedia.com/terms/p/putcallparity.asp), that with futures it is possible to construct other financial derivatives like put and call options.

*Squatting and Allocative Efficiency.* A goal of Ethereum’s transaction fee mechanism is to ensure that the users that value blockspace the most receive it. When selling blockspace far in advance, it may be allocated to someone who valued it the most a year ago but does not do so anymore today. That is, the allocative efficiency of blockspace goes down. In the worst case, someone may simply not use their blockspace (i.e. someone may squat) and Ethereum throughput would be decreased. A decrease in allocative efficiency is inherent to gas fee futures. What Ethereum loses in allocative effiency it gains in investment efficiency. People are more likely to invest in building on Ethereum if they are ensured they can access blockspace in the future.

[Unconditional Inclusion Lists](https://ethresear.ch/t/unconditional-inclusion-lists/18500). FOCIL is currently suggested with conditional inclusion lists. That means that if the block is full, inclusion list transactions may be excluded. If inclusion lists are sold far in advance as a means to hedge against gas volatility, the inclusion list should become unconditional. Unconditional inclusion list transactions must be included in the block and have priority over others if the block is full.

## Replies

**Xiawpohr** (2026-01-07):

Instead of designing an in-protocol gas future market, why not reconsider in-protocol GasToken? GasToken used to met market demand, remains compatible with EIP-1559, and avoids the no-seller problem.

I’d like to brainstorm an alternative solution to broaden our discussion. Here is my preliminary idea: **Gas Credit**

- Gas Credit represents the amount of gas that can be spent in the future blocks.
- The GASCREDIT opcode retrieves the gas credit balance of a given account.
- The GASCREDITDEPOSIT opcode allows users to deposit gas credit at the current base fee price, with ETH payment being burned.
- A gas-credit-spendable transaction is a new transaction format that includes a gas_credit_used field. Users can specify gas_credit_used to apply gas credit to reduce gas fees. The effective gas fee is calculated as: (tx.gas_used - tx.gas_credit_used) * block.base_fee_per_gas.
- [Optional] The GASCREDITTRANSFER opcode enables users to transfer gas credit to another account.

The basic use case is to deposit gas credit when base fee is low, and then to spend it when base fee going to high. With the help of Opcode `GASCREDITTRANSFER`, we can implement more interesting applications such as wrapped gas credit tokens, AMM integration for secondary markets, gas gift cards, single-use gas credit cards and so on.

Additionally, this mechanism is similar to GasToken. It maintains EIP-1559 compatibility, and sidesteps the no-seller problem entirely.

If anyone finds this idea promising, I’d be happy to draft an EIP with further technical details.

---

**Julian** (2026-01-07):

Hey [@Xiawpohr](/u/xiawpohr) ! Thanks for your comment, very exciting to see!

I like most of the GasToken mechanism and indeed we can use large parts of it.

However, they are not compatible with EIP-1559 since it means the base fee is not a credible measure of congestion anymore. For example, say someone is not willing to pay the base fee but can buy a GasToken for less than the base fee, then their transaction would be included which breaks 1559.

I think it would be ideal if the GasTokens live as ERC-20 tokens on the execution layer so that they can easily be incorporated into AMMs as you suggest.

---

**Xiawpohr** (2026-01-09):

Thanks for bringing up the historical context. I understand that GasToken exploited the refund mechanism, causing state bloat and undermining the base fee as a credible measure of congestion.

My point is that the concept of tokenizing gas doesn’t inherently conflict with EIP-1559. It’s simpler than financial derivatives and demonstrated clear product market fit in the past. Unlike GasToken, which misused the refund mechanism, Gas Credit functions more like a presale of future gas. Rather than inflating block state, it simply affects block space revenue. Block revenue may decrease when people spend their gas credits, but this is offset by the additional revenue generated when people deposit during low gas price periods.

---

**Citrullin** (2026-01-10):

Interesting topic, that’s for sure. Okay, from a users perspective. I would even go further than just having future markets. As an user I prefer a subscription based system that can guarantee a specific amount of transactions or rather gas. It’s not even about making the best deal. It’s about predictability.

Your perspective seems quite a lot on the other side. I would love you to attack this topic more from the users side. Like an ISP. I pay them x amount and I get a bank account with some amount, ideally practically unlimited, of gas. Like my Internet access. For the gas company, pun intended, to do the future trading of commodities or space in a pipeline. I don’t care. Why should I even know that futures on gas even exist?

That’s the kind of markets these standards need to be able to create. And the level you should measure yourself to.

If you now are even able to add a free tier to that. That makes it painful to use, but not impossible. That’s when the real economic magic starts to happen.

