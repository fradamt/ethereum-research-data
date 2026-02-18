---
source: ethresearch
topic_id: 19964
title: Execution Consensus Separation
author: MaxResnick
date: "2024-07-03"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/execution-consensus-separation/19964
views: 5497
likes: 23
posts_count: 8
---

# Execution Consensus Separation

## Execution Consensus Separation

**[![](https://ethresear.ch/uploads/default/optimized/3X/4/b/4b9eb4b7bcec14c8b9a8aee948a332d9d48013e4_2_500x500.jpeg)1024×1024 228 KB](https://ethresear.ch/uploads/default/4b9eb4b7bcec14c8b9a8aee948a332d9d48013e4)**

MEV is fundamentally about control. The proposer has control of which transactions make it into blocks and which order they appear in. In other words MEV is all about censorship and reordering. All of the goals on the Ethereum roadmap related to MEV are therefore impossible without fixing these things. The good news is that fixing these things is possible, the bad news is that the solution requires us to work together to study and prove the security of some meaningful upgrades to both consensus and execution.

Current work on the [“Scourge” section](https://x.com/VitalikButerin/status/1741190491578810445) of the [Ethereum roadmap](https://ethereum.org/en/roadmap/) has been siloed. People work on individual problems and sometimes lose the broader scope of what we are ultimately trying to achieve. [ePBS](https://ethresear.ch/t/epbs-design-constraints/18728), [Inclusion Lists](https://ethereum-magicians.org/t/eip-7547-inclusion-lists/17474), [MEV Burn](https://ethresear.ch/t/mev-burn-a-simple-design/15590), [Distributed Block Building](https://github.com/flashbots/mev-boost/issues/139), and [Application-layer MEV minimization](https://x.com/VitalikButerin/status/1741190491578810445), are examples of ideas that require censorship resistance and control over ordering, but we haven’t yet addressed the pre-requisites. Solving these allows us to kill 5 birds with 1 stone. But to do this we need to think from first principles and work on the underlying root causes rather than tinkering with a thin veneer on top of the protocol.

Solving MEV at the protocol level requires buy in from all three levels of the chain:

1. Consensus Layer: Multiple concurrent proposers.
2. Execution Layer: Delayed execution and deterministic scheduling rules.
3. Application Layer: Order-agnostic applications.

## Consensus layer

We cannot get anywhere without vastly improved censorship resistance at the consensus layer. This is what allows us to hold auctions and prevent censorship of competing bids. The root cause of Ethereum’s weak censorship resistance is the fact that only a single entity can include transactions during each 12 second slot. **Multiple concurrent proposers (MCP)** fixes this problem. Instead of coming to consensus on an ordered block of transactions from a single block proposer, each of the K proposers propose a set of transactions at the same time. The protocol then aggregates these proposals using a **common subset** primitive (or a similar algorithm, this is an active area of research), yielding an unordered set of transactions which are to be included in the block.

MCP solves the problem of censorship-resistant inclusion, achieving the goals of [Inclusion Lists](https://ethereum-magicians.org/t/eip-7547-inclusion-lists/17474) in a more natural way. The output is an unordered set of transactions, so it does not solve the problem of reordering. That will be the responsibility of the execution layer.

MCP is an area of active study and we encourage people to get involved. See SMG [SPEC-01](https://mechanism.org/spec/01) for a theoretical description of MCP. Work is currently underway at SMG to formally specify MCP and create a proposed implementation of a gadget for use in the Ethereum protocol. Contact us if you are interested in working on this.

## Execution layer

Ethereum’s execution layer must be upgraded to solve the problem of transaction reordering. To do this, we must delay the calculation of the state root to the next block so that the execution layer has time to implement a deterministic ordering rule.

Once it has the transactions, the execution layer has a new important job: figuring out how to order them. To do this, we need to select a **deterministic scheduling rule**. This is an area of active study where we encourage people to get involved. There are many promising candidates: [priority fee ordering](https://www.paradigm.xyz/2024/06/priority-is-all-you-need), as-needed execution, and [distributed block building](https://github.com/flashbots/mev-boost/issues/139). We will elaborate on the last two in an upcoming article.

With delayed execution and a deterministic scheduling rule, Ethereum’s execution layer will determine the order of transactions in a block, allowing it to achieve the same goals as [distributed block building](https://github.com/flashbots/mev-boost/issues/139) and [ePBS](https://ethresear.ch/t/epbs-design-constraints/18728) in a more natural way. In addition, since the ordering is enforced by the logic of the protocol, not by the goodwill of any particular validator, the protocol can burn all the fees at this stage, achieving the goals of [MEV Burn](https://ethresear.ch/t/mev-burn-a-simple-design/15590).

## Application layer

Assuming we succeed in the above upgrades, Ethereum’s application layer will be free to upgrade their applications to be natively MEV-resistant while remaining totally onchain. We call the class of things they will do **order-agnostic applications** or order-agnostic mechanisms.

For example take the problem of liquidation MEV. For the sake of argument, suppose we have 1000 ETH that needs to be liquidated for DAI. We don’t know what the appropriate price is for the ETH, so we have two options: we can guess the right price and have a posted price available to the first person who claims it, which is how Compound and Aave work, and leads to tremendous value leaked to liquidation races, reducing UX. Or, we can hold a Dutch auction, which leads to slightly less value leakage, but doesn’t allow us to clear the distressed debt right away. But now, with MCP and deterministic scheduling, these protocols can simply hold an onchain auction for the right to liquidate 1000 ETH and elicit the price that way.

Order agnostic application design has a number of benefits, and there are many more examples of places where MEV leaks that can be solved. Future posts will elaborate on this.

## Conclusion

The successful implementation of these upgrades will result in a much friendlier Ethereum for both developers and users. The first step of this research program is fleshing out and proving the security of a multi proposer design with simultaneous release. Other blockchains have multiple proposers, but are not designed in the same way or for the same purpose. If you are a consensus researcher interested in working on this topic, please reach out, we have funding available for this.

## Replies

**The-CTra1n** (2024-07-04):

If there is short-term censorship resistance on the consensus layer, either one of the other two functionalities might be sufficient on their own to remove MEV.

- deterministic sequencing
- order-agnostic applications.

Are there any examples where you need both?

---

**MaxResnick** (2024-07-04):

The right execution rule makes it easier to run auctions because you don’t need to hold stuff in escrow till the end of the block for all bids to come in.

---

**M1kuW1ll** (2024-07-05):

What if multiple concurrent proposers choose to auction off their task of payload construction to builders, and censoring builders win most or even all the payload space?

---

**awmacp** (2024-07-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> For example take the problem of liquidation MEV. For the sake of argument, suppose we have 1000 ETH that needs to be liquidated for DAI. We don’t know what the appropriate price is for the ETH, so we have two options: we can guess the right price and have a posted price available to the first person who claims it, which is how Compound and Aave work, and leads to tremendous value leaked to liquidation races, reducing UX. Or, we can hold a Dutch auction, which leads to slightly less value leakage, but doesn’t allow us to clear the distressed debt right away. But now, with MCP and deterministic scheduling, these protocols can simply hold an onchain auction for the right to liquidate 1000 ETH and elicit the price that way.

The combination of “ordering agnostic” and “deterministic scheduling rule” here is confusing, so maybe you could explain what is meant by these terms in the context of your example?

For instance, it is clearly possible to design the liquidation auction so that the execution does not depend on the order in which bids are registered, so this part could indeed be called “ordering agnostic.” Is this the kind of intuition you’re building on?

But the settlement must be sequenced after the last bid, so that part is not ordering agnostic — perhaps this is where the scheduling rule comes in? But then again, apps can already enforce this, for example by setting a block number cutoff for the bidding phase. I’m not seeing how delayed execution is being used either.

---

**parseb** (2024-07-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> To do this, we must delay the calculation of the state root to the next block so that the execution layer has time to implement a deterministic ordering rule.

would use the previous block hash as ordering rule determinant for transaction hashes order.

delay need doesn’t compute for me (did not go to computer school)

---

**kosunghun317** (2024-07-26):

Since the cost of censoring grows linearly w.r.t. number of cocurrent proposers the possibility of censorship will go down. Now censoring builder have to win 1 auction; after MCP they have to win (1-c)N auctions, if we set the rule to adopt the transaction that is accepted by c portion of proposers.

---

**klntsky** (2024-07-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> The protocol then aggregates these proposals using a common subset primitive (or a similar algorithm, this is an active area of research),

Common subset would not provide censorship resistance, set union would. But then it requires some way to aggregate the results for singing. Could you link some research around this topic?

