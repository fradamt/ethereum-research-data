---
source: ethresearch
topic_id: 2790
title: Use of https://gastoken.io/ - positive or negative for the network?
author: mkoeppelmann
date: "2018-08-03"
category: Economics
tags: [gas-token]
url: https://ethresear.ch/t/use-of-https-gastoken-io-positive-or-negative-for-the-network/2790
views: 5660
likes: 21
posts_count: 7
---

# Use of https://gastoken.io/ - positive or negative for the network?

We are thinking about using https://gastoken.io/ for https://safe.gnosis.io/

https://safe.gnosis.io/ is a multisig wallet and in a way a implementation of account abstraction with the current possibilities. A user might sign the (meta) transaction. An external service can post the signed message to the contract. The contract will execute the transaction and refund the external service.

In the beginning we will offer that external service (eventually miners should just do it) and we are thinking about the use of gastoken.

I am wondering what the consequences are - here are my assumptions:

a) gas token become liquidly tradable

b) gas tokens will regularly used when gas costs spike

The consequence of a) should be that all blocks will be 100% full since that is always demand for transactions that mine gas tokens. The gas token price will basically establish a gas price floor. If you want to do an “actual” transaction you will always need to pay more than that floor. Then there will be a second number (the soft ceiling) where it starts to make sense to spend gas tokens. In a way that would introduce a flexible block gas limit. If demand for transactions are high it temporarily “bigger blocks” can be produced (block-gaslimit + refund from gas token burn)

So we can expect that overall gas prices will spike a bit smoother than seen historically and owning gas tokens will further reduce that risk. On the other hand it creates negative externalities - the full nodes have to deal with a lot of completely unnecessary smart contracts.

So my overall question is about the sentiment. Is it a flaw and should be forked away or is it a useful thing?

## Replies

**vbuterin** (2018-08-03):

I’m inclined to say it’s positive on net, for exactly this reason:

> So we can expect that overall gas prices will spike a bit smoother than seen historically and owning gas tokens will further reduce that risk.

The marginal social cost of gas usage does not change 10x day by day the way gas prices do. Therefore anything that reduces the volatility of gas prices reduces deadweight losses considerably (note that because deadweight loss is quadratic, this is true even if average gas prices are mismatched to the social cost in an absolute sense; you can do the math yourself to confirm this).

---

**3esmit** (2018-08-03):

It would be positive for the nodes that would need to store junk in state? Maybe a specific OPCODE to accumulate gas in a storage, that instead of holding size, just burns gas and convert to a number.

I wonder if gas token would still be worthy with storage rent, I guess it would stop working.

---

**vbuterin** (2018-08-03):

GasToken can definitely design itself in a way such that the social externality of this is much lower. Specifically, it could fill contracts with storage trees that are exactly identical to each other (or a single contract with storage subtrees that are exactly identical to each other), which a client would automatically deduplicate and store only once.

---

**lorenzb** (2018-08-03):

> Specifically, it could fill contracts with storage trees that are exactly identical to each other (or a single contract with storage subtrees that are exactly identical to each other), which a client would automatically deduplicate and store only once.

We tried to make GasToken as “compressible” as possible within the current constraints of Ethereum:

- GST1 (the storage version) fills a contiguous segment of storage slots with 0x01s.
- GST2 (the contract/selfdestruct version) spawns byte-for-byte identical child contracts that don’t use storage.

So a client could relatively easily implement a compression scheme that deduplicates identical contracts/storage slots. (Although actually implementing this isn’t all that easy because of the need to update the stateRoot in a backward compatible manner.)

Alternatively, a hardfork could of course introduce a “better GasToken”. There is a wide spectrum of possible designs, starting with a simple pre-compile that doesn’t use any resources beyond a counter and ending with in-protocol futures like the ones Project Chicago is [working on](https://github.com/projectchicago/commodeth).

---

**phil** (2018-08-06):

There seem to be two questions here; whether it’s good for the network, and how to decide whether to use it.

## Is it good for the network?

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> So my overall question is about the sentiment. Is it a flaw and should be forked away or is it a useful thing?

This is a pretty complex question that we debate even inside the GasToken team.

On the one hand, you are correct; GasToken appears to have a natural smoothing effect and allows the quantity supplied to be more responsive to demand.  On the other hand, for UX, it’s not clear to me that this will be a positive shift; it’s entirely possible that the bounded stable gas price in a steady state system using GasToken *could be* higher than what users are paying today.

There are several factors worthy of consideration.

1. Influence of speculation: an efficient and liquid GasToken would imply speculation as a use case, where no direct/trustless speculation is possible on gas today (second layer speculation where users do not directly hold gas is possible through e.g. prediction markets, but GasToken is a more direct tokenization mechanism for the underlying computation).  Computation in Ethereum is relatively scarce (as recent gas issues indicate), leading to the possibility of upwards pressure on gas price worsening UX for users.  One analogy is the only scarce resource in EOS, RAM, representing storage, which was opened to speculation, and has seen uncertain market dynamics and hoarding as a result.  It is entirely possible that the eventual outcome is continuous releases of supply-by-decree, overinflated costs to users, or an accurate and robust pricing mechanism.  The latter would hint that speculation/hoarding is not a big issue.  One key difference is that GasToken represents (essentially) tokenized promises of computation subsidies, rather than tokenized storage.
2. Overall capacity reduction: If GasToken is used for every transaction, the overall capacity of the network will be reduced over the current market with full blocks, as GasToken incurs efficiency loss in accounting/call overhead.  Miners can vote the gas limit up to somewhat compensate for this, but after this becomes stable you run into the issues in (3).
3. Useless resource consumption: GasToken uses resources in the system.  If the platform is otherwise optimizing for whatever total capacity it would like to provide for a given security level (in terms of computation, network, and storage), this waste means reduced total capacity or reduced total security.  This could be partially mitigated through client-side optimizations, and possibly solved through a variety of hard fork changes (e.g., replacing GasToken with a simulated version, or more fundamental changes to the resource model).  It could also be mitigated by disabling GasToken through removal of the refund, or by making its use less attractive by e.g., decreasing the percentage of transaction fees that is refundable (though this would neuter refunds so severely the question of “why keep them” remains obvious; one nice property of GasToken is that in a liquid form it actually provides a super nice pathway for incentivizing cleanup).

So is GasToken good for the network? For now, perhaps. In the long run, it probably isn’t the optimal solution.

## Should you use it?

I think that should purely be a question of whether it is economically rational for you as a participant, not whether it is good for the network.  As long term holders and investors in the ecosystem, we all have an incentive to make sure the network survives.  That being said, we can’t continue to rely on or assume such altruism as the system grows.  *If an unpermissioned system is to survive, it must be able to tolerate economically rational behavior inside the platform.*  So personally, I would encourage whatever decision makes economic sense in the short to medium term.

Right now, using GasToken is clearly economically rational for short-term gas bidders such as arbitrageurs or serial ICO buyers, even in the absence of a liquid market (as mining yourself is practical here).  It is also clearly economically rational for businesses who plan on doing large gas transactions reasonably into the future and want to reduce risk surrounding a Cryptokitties or F-Coin-like event.  In all of these cases, we are dealing with sophisticated players who use large amounts of gas and thus have an incentive to put in the engineering effort to implement their own GasToken-like mechanism or integrate with GST. Anyone professionally trading on DEXes, sweeping contracts, doing an airdrop, etc. likely falls into this category. This isn’t just hypothetical — we are aware of users who are using GasToken-like mechanisms in their smart contracts *today*.

For general-purpose contract use (as in the case of Gnosis Safe), a liquid market would be required for maximum utility.  So whether you should use it really depends on whether such a market arises or not.  A handful of large-ish players like Gnosis would be required to make such a market truly robust.  The accounting/exchange overhead should also be minimal and the per-transaction gas usage relatively high to make such use viable; the [transaction calculator](https://gastoken.io/#calculator) can let you know whether this is the case today — I am sure that you did the math and determined that it would work in the case of Gnosis Safe.

Finally, there also is a “fairness” argument: sophisticated players are already taking advantage of GasToken/GasToken-like mechanisms. It would be nice if the benefits were also made available to the general public. Gnosis Safe might be a good starting point for this.

From a research perspective, there is a massive silver lining: we can learn a lot from GasToken deployment that will highlight fundamental issues in current resource models and help us design next-generation mechanisms (as Lorenz pointed out this is the aim of the overarching project, [Project Chicago](https://projectchicago.io/)).

**All the usual disclaimers on the GasToken site apply; there is substantial risk, especially in holding GST1/GST2 long term.**

(Thanks to GST team members Lorenz, Florian, and Ari for providing input/contributions on this post.)

---

**axic** (2018-09-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/lorenzb/48/1875_2.png) lorenzb:

> Alternatively, a hardfork could of course introduce a “better GasToken”. There is a wide spectrum of possible designs, starting with a simple pre-compile that doesn’t use any resources beyond a counter and ending with in-protocol futures like the ones Project Chicago is working on .

Have you thought about proposing a precompile design for this?

(Or perhaps one on ewasm where it can be a system contract?)

